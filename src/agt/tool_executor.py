from __future__ import annotations

from typing import Any, Callable, Dict

from .types import PlanStep, StepResult


class ToolExecutor:
    """
    Safe allowlisted tool executor.

    No arbitrary shell execution.
    No network execution.
    No hidden autonomy.
    New tools must be registered explicitly in the allowlist.
    """

    def __init__(self) -> None:
        self.tools: Dict[str, Callable[..., Any]] = {
            "draft_text": self._draft_text,
            "echo": self._echo,
        }

    def execute(self, step: PlanStep) -> StepResult:
        if step.action == "audit_blocked_step":
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error="Step blocked by CTK/CHK audit.",
            )

        if not step.tool_name:
            return StepResult(
                step_id=step.id,
                ok=True,
                output=f"No tool needed for {step.action}.",
            )

        tool = self.tools.get(step.tool_name)

        if tool is None:
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error=f"Tool not allowed: {step.tool_name}",
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
        Extension point for safe tools.

        Use only for explicitly allowed deterministic tools.
        Do not register arbitrary shell or network execution here.
        """
        if name.startswith("_"):
            raise ValueError("Private tool names are forbidden.")
        self.tools[name] = fn

    def _draft_text(self, prompt: str) -> str:
        return (
            "Draft produced as Werk, not Wille.\n\n"
            f"Task: {prompt}\n\n"
            "1. Identify the problem.\n"
            "2. State the regulative frame.\n"
            "3. Propose an operational next step.\n"
            "4. Preserve human review when normative judgment is involved."
        )

    def _echo(self, text: str) -> str:
        return text
