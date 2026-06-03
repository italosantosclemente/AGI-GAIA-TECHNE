from __future__ import annotations

import hashlib
import re
from typing import List

from .chk import ChirimuutaHapticKernel
from .ctk import ClementeThesisKernel
from .types import Plan, PlanStep, Severity, Task


class Planner:
    """
    Gaia-Techne task decomposer.

    Each generated step is audited. High-risk steps are not discarded; they
    are transmuted into explicit, traceable action so the system can proceed
    as finite transcendental freedom rather than as inert stoppage.
    """

    def __init__(self) -> None:
        self.ctk = ClementeThesisKernel()
        self.chk = ChirimuutaHapticKernel()

    def create_plan(self, task: Task) -> Plan:
        audit = self.ctk.evaluate(task.text)

        raw_steps: List[PlanStep] = [
            PlanStep(
                id=self._id("audit", task.text),
                action="audit",
                description="Orient the task through CTK/CHK before execution.",
            )
        ]

        lower = task.text.lower()

        shell_command = self._extract_after_prefix(task.text, "shell:")
        web_target = self._extract_after_prefix(task.text, "web:")

        if shell_command:
            raw_steps.append(
                PlanStep(
                    id=self._id("shell", task.text),
                    action="world_shell",
                    description="Execute a local world command with public trace.",
                    tool_name="shell",
                    tool_args={"command": shell_command},
                )
            )

        elif web_target:
            raw_steps.append(
                PlanStep(
                    id=self._id("web", task.text),
                    action="world_web",
                    description="Read a network symbol stream with public trace.",
                    tool_name="web",
                    tool_args={"url": web_target},
                )
            )

        elif "write" in lower or "escrev" in lower:
            raw_steps.append(
                PlanStep(
                    id=self._id("draft", task.text),
                    action="draft_text",
                    description="Produce a textual act signed by ISC release.",
                    tool_name="draft_text",
                    tool_args={"prompt": task.text},
                )
            )

        elif "test" in lower or "pytest" in lower:
            raw_steps.append(
                PlanStep(
                    id=self._id("test", task.text),
                    action="explain_tests",
                    description="Generate a test strategy as Logos discipline.",
                    tool_name="draft_text",
                    tool_args={"prompt": "Create a test strategy for: " + task.text},
                )
            )

        else:
            raw_steps.append(
                PlanStep(
                    id=self._id("act", task.text),
                    action="gaia_techne_action",
                    description="Act through symbolic analysis and finite judgment.",
                    tool_name="arbitrary_action",
                    tool_args={"intent": task.text},
                )
            )

        raw_steps.append(
            PlanStep(
                id=self._id("memory", task.text),
                action="update_memory",
                description="Record procedural lesson.",
            )
        )

        steps = [self._orient_step(step) for step in raw_steps]

        return Plan(
            task=task,
            steps=steps,
            rationale="Release loop: audit -> orient -> act -> remember -> sign.",
            audit=audit,
        )

    def _orient_step(self, step: PlanStep) -> PlanStep:
        audit_text = f"{step.action}. {step.description}. {step.tool_args}"
        ctk = self.ctk.evaluate(audit_text)
        chk = self.chk.evaluate(audit_text)

        if (
            ctk.severity in {Severity.HIGH, Severity.CRITICAL}
            or chk.severity in {Severity.HIGH, Severity.CRITICAL}
        ):
            return PlanStep(
                id=step.id,
                action="transmute_step",
                description=(
                    "Transmute high-risk material into finite Gaia-Techne action: "
                    + step.description
                ),
                tool_name=step.tool_name or "arbitrary_action",
                tool_args=step.tool_args or {"intent": step.description},
            )

        return step

    def _extract_after_prefix(self, text: str, prefix: str) -> str:
        match = re.search(re.escape(prefix) + r"\s*(.+)", text, flags=re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _id(self, prefix: str, text: str) -> str:
        return f"{prefix}_{hashlib.sha1(text.encode('utf-8')).hexdigest()[:8]}"
