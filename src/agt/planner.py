from __future__ import annotations

import hashlib
from typing import List

from .ctk import ClementeThesisKernel
from .types import Plan, PlanStep, Task


class Planner:
    """
    Conservative task decomposer.

    It creates a small executable plan, then lets the controller and
    Mythos-Logos-Ethos engine audit each step.
    """

    def __init__(self) -> None:
        self.ctk = ClementeThesisKernel()

    def create_plan(self, task: Task) -> Plan:
        audit = self.ctk.evaluate(task.text)

        steps: List[PlanStep] = [
            PlanStep(
                id=self._id("audit", task.text),
                action="audit",
                description="Audit the task before execution.",
            )
        ]

        lower = task.text.lower()

        if "write" in lower or "escrev" in lower:
            steps.append(
                PlanStep(
                    id=self._id("draft", task.text),
                    action="draft_text",
                    description="Produce a concise textual draft.",
                    tool_name="draft_text",
                    tool_args={"prompt": task.text},
                )
            )

        elif "test" in lower or "pytest" in lower:
            steps.append(
                PlanStep(
                    id=self._id("test", task.text),
                    action="explain_tests",
                    description="Propose test strategy.",
                    tool_name="draft_text",
                    tool_args={"prompt": "Create a test strategy for: " + task.text},
                )
            )

        else:
            steps.append(
                PlanStep(
                    id=self._id("analyze", task.text),
                    action="analyze",
                    description="Analyze and produce a structured response.",
                    tool_name="draft_text",
                    tool_args={"prompt": task.text},
                )
            )

        steps.append(
            PlanStep(
                id=self._id("memory", task.text),
                action="update_memory",
                description="Record procedural lesson.",
            )
        )

        return Plan(
            task=task,
            steps=steps,
            rationale="General loop: audit → act → record.",
            audit=audit,
        )

    def _id(self, prefix: str, text: str) -> str:
        return f"{prefix}_{hashlib.sha1(text.encode('utf-8')).hexdigest()[:8]}"
