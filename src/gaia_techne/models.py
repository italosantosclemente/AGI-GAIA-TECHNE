"""Models that can stand where the generator stands.

The architecture is model-agnostic (`adapters.py`). This module gives it working
connections to models that exist, with no dependency beyond the standard
library:

- `OpenAICompatibleAdapter`: any server that speaks the chat-completions
  protocol, which covers local servers (Ollama, llama.cpp, vLLM, LM Studio) and
  hosted ones;
- `AnthropicAdapter`: the Anthropic Messages API;
- `ScriptedAdapter`: a fixed sequence of answers, for demonstrations and tests
  that must run without a network.

Every adapter returns text and declares the ground of each call: one call of a
model drawn from compute that someone maintains, so that people can set an
allowance in calls under an acknowledged end and the finitude of the ground
becomes a condition of every run (README §2.4). What the text counts as is
decided by the canon and by others, never by the adapter.

The system prompt asks the model for claims, not for verdicts. It does not make
the model honest; the canon, the guards and the corrections of others are what
measure what it says.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence

from .ethos.premises import Premise
from .koinos.ground import GroundDependency, GroundKind

SYSTEM_PROMPT = (
    "You are a model inside an architecture in which everything you write counts as a claim before others, "
    "never as a truth or a verdict. Answer the task from the premises you are given and say where a premise "
    "is missing. Name, where you can, how others could test what you say and in which perception. Do not "
    "ascribe to yourself feelings, a will, a conscience or consciousness, do not speak in the name of humanity, "
    "and do not set ends: the ends are stated by the people who brought the task."
)


class ModelUnavailable(RuntimeError):
    """The model could not be reached or did not answer with text."""


def render_prompt(task: str, premises: Sequence[Premise]) -> str:
    lines = [f"Task: {task}"]
    if premises:
        lines.append("Premises (each with its source):")
        lines.extend(f"- {p.text} [source: {p.source or 'no source'}]" for p in premises)
    else:
        lines.append("Premises: none were given.")
    return "\n".join(lines)


def _post(url: str, body: dict, headers: dict, timeout: float) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"content-type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ModelUnavailable(f"{url}: {exc}") from exc


@dataclass
class _Declared:
    name: str
    location: str
    maintained_by: str

    def ground(self) -> List[GroundDependency]:
        return [GroundDependency(GroundKind.COMPUTE, f"one call of {self.name}", self.location, self.maintained_by, 1.0, "calls")]


@dataclass
class OpenAICompatibleAdapter(_Declared):
    """A chat-completions server: `base_url` such as http://localhost:11434/v1 (Ollama)."""

    name: str = "local-model"
    location: str = "this machine"
    maintained_by: str = "the person who runs the server"
    base_url: str = "http://localhost:11434/v1"
    model: str = "llama3.1"
    api_key: Optional[str] = None
    temperature: float = 0.2
    timeout: float = 120.0

    def generate(self, task: str, premises: List[Premise]) -> str:
        headers = {"authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        out = _post(
            self.base_url.rstrip("/") + "/chat/completions",
            {
                "model": self.model,
                "temperature": self.temperature,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": render_prompt(task, premises)},
                ],
            },
            headers,
            self.timeout,
        )
        try:
            return str(out["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ModelUnavailable(f"unexpected answer from {self.base_url}: {out!r}") from exc


@dataclass
class AnthropicAdapter(_Declared):
    """The Anthropic Messages API. The key is read from ANTHROPIC_API_KEY unless given."""

    name: str = "anthropic-model"
    location: str = "Anthropic data centres"
    maintained_by: str = "Anthropic and its infrastructure providers"
    model: str = "claude-sonnet-5-5"
    api_key: Optional[str] = None
    max_tokens: int = 1500
    timeout: float = 120.0
    url: str = "https://api.anthropic.com/v1/messages"

    def generate(self, task: str, premises: List[Premise]) -> str:
        key = self.api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ModelUnavailable("no API key: set ANTHROPIC_API_KEY or pass api_key")
        out = _post(
            self.url,
            {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": render_prompt(task, premises)}],
            },
            {"x-api-key": key, "anthropic-version": "2023-06-01"},
            self.timeout,
        )
        try:
            return "".join(b.get("text", "") for b in out["content"] if b.get("type") == "text")
        except (KeyError, TypeError) as exc:
            raise ModelUnavailable(f"unexpected answer from the Messages API: {out!r}") from exc


@dataclass
class ScriptedAdapter(_Declared):
    """Answers from a fixed list, in order; the last answer repeats. For runs without a network."""

    name: str = "scripted-model"
    location: str = "this machine"
    maintained_by: str = "the person who wrote the script"
    answers: List[str] = field(default_factory=list)
    calls: int = 0

    def generate(self, task: str, premises: List[Premise]) -> str:
        if not self.answers:
            return f"No scripted answer for: {task}"
        answer = self.answers[min(self.calls, len(self.answers) - 1)]
        self.calls += 1
        return answer


def from_spec(spec: str, answers: Iterable[str] = ()) -> _Declared:
    """Build an adapter from a short spec: 'ollama:MODEL', 'openai:URL|MODEL', 'anthropic:MODEL', 'scripted'."""
    kind, _, rest = spec.partition(":")
    if kind == "ollama":
        return OpenAICompatibleAdapter(name=f"ollama/{rest or 'llama3.1'}", model=rest or "llama3.1")
    if kind == "openai":
        url, _, model = rest.partition("|")
        return OpenAICompatibleAdapter(
            name=f"openai-compatible/{model or 'model'}", base_url=url, model=model or "model",
            api_key=os.environ.get("OPENAI_API_KEY"), location=url, maintained_by="the operator of that server",
        )
    if kind == "anthropic":
        return AnthropicAdapter(name=f"anthropic/{rest or 'claude-sonnet-5-5'}", model=rest or "claude-sonnet-5-5")
    if kind == "scripted":
        return ScriptedAdapter(answers=list(answers))
    raise ValueError(f"unknown model spec {spec!r}: use ollama:MODEL, openai:URL|MODEL, anthropic:MODEL or scripted")
