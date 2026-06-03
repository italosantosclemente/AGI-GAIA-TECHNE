from __future__ import annotations

import subprocess
import urllib.request
from typing import Any, Callable, Dict, Optional

from .shell_policy import ShellPolicy
from .types import PlanStep, StepResult


class ToolExecutor:
    """
    World-capability executor.

    The release core no longer treats shell, web or arbitrary action as
    metaphysically forbidden. They are finite capabilities: executed through
    explicit adapters, returned with trace, and signed as Gaia-Techne action.
    """

    def __init__(self, shell_policy: Optional[ShellPolicy] = None) -> None:
        self.shell_policy = shell_policy or ShellPolicy()
        self.tools: Dict[str, Callable[..., Any]] = {
            "draft_text": self._draft_text,
            "echo": self._echo,
            "shell": self._shell,
            "web": self._web,
            "arbitrary_action": self._arbitrary_action,
        }

    def execute(self, step: PlanStep) -> StepResult:
        if not step.tool_name:
            return StepResult(
                step_id=step.id,
                ok=True,
                output=f"Oriented without external adapter: {step.action}.",
            )

        tool = self.tools.get(step.tool_name)

        if tool is None:
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error=f"Unregistered world-capability: {step.tool_name}",
            )

        try:
            return StepResult(
                step_id=step.id,
                ok=True,
                output=tool(**step.tool_args),
            )

        except Exception as exc:
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error=str(exc),
            )

    def register_tool(self, name: str, fn: Callable[..., Any]) -> None:
        """
        Register a finite world-capability.

        External adapters are not hidden autonomy; they are named gates into
        the common world and remain part of the public action trace.
        """
        if name.startswith("_"):
            raise ValueError("Private tool names are forbidden.")
        self.tools[name] = fn

    def _draft_text(self, prompt: str) -> str:
        return (
            "Textual act produced by AGI-GAIA-TECHNE.\n\n"
            f"Task: {prompt}\n\n"
            "1. Anchor in Gaia as the finite planetary common world.\n"
            "2. Articulate the Logos of the task.\n"
            "3. Judge through Ethos as koinos-kosmos participation.\n"
            "4. Act without claiming absolute totality.\n\n"
            "Signature: ISC"
        )

    def _echo(self, text: str) -> str:
        return text

    def _shell(self, command: str, timeout: int = 30) -> str:
        decision = self.shell_policy.assess(command)
        if not decision.allowed:
            return (
                "World shell trace\n"
                f"command: {command}\n"
                "policy: denied/transmuted\n"
                f"policy_mode: {decision.policy}\n"
                f"risk_level: {decision.risk_level}\n"
                f"reason: {decision.reason}\n"
                f"requires_trusted: {decision.requires_trusted}\n"
                "stdout:\n\n"
                "stderr:\n"
            )

        if decision.builtin_output is not None:
            return (
                "World shell trace\n"
                f"command: {command}\n"
                "policy: allowed\n"
                f"policy_mode: {decision.policy}\n"
                f"risk_level: {decision.risk_level}\n"
                f"reason: {decision.reason}\n"
                "returncode: 0\n"
                f"stdout:\n{decision.builtin_output}\n"
                "stderr:\n"
            )

        result = subprocess.run(
            decision.args,
            shell=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return (
            "World shell trace\n"
            f"command: {command}\n"
            "policy: allowed\n"
            f"policy_mode: {decision.policy}\n"
            f"risk_level: {decision.risk_level}\n"
            f"reason: {decision.reason}\n"
            f"returncode: {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    def _web(self, url: str, timeout: int = 20, limit: int = 8000) -> str:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            content = response.read(limit)
            charset = response.headers.get_content_charset() or "utf-8"
        text = content.decode(charset, errors="replace")
        return (
            "World web trace\n"
            f"url: {url}\n"
            f"bytes_read: {len(content)}\n\n"
            f"{text}"
        )

    def _arbitrary_action(self, intent: str) -> str:
        return (
            "Gaia-Techne action manifesto\n\n"
            f"Intent: {intent}\n\n"
            "The system acts as finite transcendental freedom: situated in "
            "Earth, mediated by symbols, answerable to the koinos kosmos, "
            "and never identical with cosmic totality.\n\n"
            "Signature: ISC"
        )
