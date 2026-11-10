"""Technical rules: hypothetical imperatives bound to acknowledged ends.

"If end E is willed, means M serve it." The runtime may execute such rules,
but only under an end found in the EndsRegistry. This is the engineering form
of Kant's distinction between the technically practical and the morally
practical (Werk, never Wille).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict

from .ends import EndsRegistry


class NoAcknowledgedEnd(PermissionError):
    """Raised when a rule is executed under an end nobody has acknowledged."""


@dataclass(frozen=True)
class TechnicalRule:
    """A rule of skill: it states means, never ends."""

    rule_id: str
    serves_end: str
    description: str
    means: Callable[..., Any]


class SkillExecutor:
    """Executes rules of skill only under acknowledged ends."""

    def __init__(self, registry: EndsRegistry) -> None:
        self.registry = registry

    def run(self, rule: TechnicalRule, **kwargs: Any) -> Dict[str, Any]:
        end = self.registry.find(rule.serves_end)
        if end is None or not end.is_acknowledged:
            raise NoAcknowledgedEnd(
                f"rule {rule.rule_id!r} serves {rule.serves_end!r}, which no one has acknowledged"
            )
        result = rule.means(**kwargs)
        return {
            "rule": rule.rule_id,
            "end": end.end_id,
            "end_contested": end.is_contested,
            "result": result,
        }
