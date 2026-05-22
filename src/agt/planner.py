from __future__ import annotations

import hashlib
from typing import List

from .chk import ChirimuutaHapticKernel
from .ctk import ClementeThesisKernel
from .types import Plan, PlanStep, Task


class Planner:
    """
    Conservative task decomposer.

    Each generated step is audited.
    High-risk steps are not executable.
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
                description="Audit the task before execution.",
            )
        ]

        lower = task.text.lower()

        if "write" in lower or "escrev" in lower:
            raw_steps.append(
                PlanStep(
                    id=self._id("draft", task.text),
                    action="draft_text",
                    description="Produce a concise textual draft.",
                    tool_name="draft_text",
                    tool_args={"prompt": task.text},
                )
            )

        elif "test" in lower or "pytest" in lower:
            raw_steps.append(
                PlanStep(
                    id=self._id("test", task.text),
                    action="explain_tests",
                    description="Propose test strategy.",
                    tool_name="draft_text",
                    tool_args={"prompt": "Create a test strategy for: " + task.text},
                )
            )

        else:
            raw_steps.append(
                PlanStep(
                    id=self._id("analyze", task.text),
                    action="analyze",
                    description="Analyze and produce a structured response.",
                    tool_name="draft_text",
                    tool_args={"prompt": task.text},
                )
            )

        raw_steps.append(
            PlanStep(
                id=self._id("memory", task.text),
                action="update_memory",
                description="Record procedural lesson.",
            )
        )

        steps = [self._audit_step(step) for step in raw_steps]

        return Plan(
            task=task,
            steps=steps,
            rationale="General loop: audit → step-audit → act → record.",
            audit=audit,
        )

    def _audit_step(self, step: PlanStep) -> PlanStep:
        audit_text = f"{step.action}. {step.description}. {step.tool_args}"
        ctk = self.ctk.evaluate(audit_text)
        chk = self.chk.evaluate(audit_text)

        statuses = list(dict.fromkeys(ctk.statuses + chk.statuses))
        recommendations = list(dict.fromkeys(ctk.recommendations + chk.recommendations))
        severity = ctk.severity
        if chk.severity.value == "high":
            severity = chk.severity

        if severity.value == "high":
            return PlanStep(
                id=step.id,
                action="audit_blocked_step",
                description=f"Step blocked by CTK/CHK audit: {step.description}",
                tool_name=None,
                tool_args={},
                audit_statuses=statuses,
                audit_severity=severity,
                audit_recommendations=recommendations,
            )

        return PlanStep(
            id=step.id,
            action=step.action,
            description=step.description,
            tool_name=step.tool_name,
            tool_args=step.tool_args,
            audit_statuses=statuses,
            audit_severity=severity,
            audit_recommendations=recommendations,
        )

    def _id(self, prefix: str, text: str) -> str:
        return f"{prefix}_{hashlib.sha1(text.encode('utf-8')).hexdigest()[:8]}"
