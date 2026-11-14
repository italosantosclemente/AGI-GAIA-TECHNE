"""Model adapters: what stands where the generator stands.

The architecture is model-agnostic. A local LLM, a statistical model or a
human typist can produce the text; what the architecture fixes is what any
produced text may count as. An adapter therefore has two duties only:

- `generate(task, premises)` returns text, nothing else. Whether the text is a
  claim, what reach it has and whether it may be used is decided by the canon
  and by others, never by the adapter;
- `ground()` (optional) declares the ground the adapter itself draws on, such
  as the processors and energy of one call, so that the formative power the
  system seems to have keeps the names of those who maintain it.

A plain function `(task, premises) -> str` is accepted and wrapped.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Protocol, runtime_checkable

from .ethos.premises import Premise
from .koinos.ground import GroundDependency


@runtime_checkable
class GeneratorAdapter(Protocol):
    name: str

    def generate(self, task: str, premises: List[Premise]) -> str: ...


@dataclass
class FunctionAdapter:
    """Wraps a function as an adapter, with the ground it declares for each call."""

    fn: Callable[[str, List[Premise]], str]
    name: str = "model"
    declared_ground: List[GroundDependency] = field(default_factory=list)

    def generate(self, task: str, premises: List[Premise]) -> str:
        return self.fn(task, premises)

    def ground(self) -> List[GroundDependency]:
        return list(self.declared_ground)


def as_adapter(generator: Any, name: str = "model") -> GeneratorAdapter:
    if isinstance(generator, GeneratorAdapter):
        return generator
    if callable(generator):
        return FunctionAdapter(generator, name=name)
    raise TypeError("a generator is a function (task, premises) -> str or an object with generate()")


def declared_ground(adapter: Any) -> List[GroundDependency]:
    ground = getattr(adapter, "ground", None)
    return list(ground()) if callable(ground) else []
