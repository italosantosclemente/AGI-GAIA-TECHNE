from __future__ import annotations

from dataclasses import asdict
from typing import List

from .axioms import (
    IS_WILLE,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
    assert_axioms,
)
from .memory import MemoryStore
from .mle_engine import MythosLogosEthosEngine
from .planner import Planner
from .tool_executor import ToolExecutor
from .types import ControllerReport, Decision, MemoryKind, Task


class AGTController:
    """
    Functional AGI-GAIA-TECHNE controller.

    Executes:

    task → Mythos/Logos/Ethos audit → plan → step audit → safe tool use → memory → Werk output.
    """

    def __init__(self, memory_path: str = "memory/agt_memory.jsonl") -> None:
        assert_axioms()

        self.engine = MythosLogosEthosEngine()
        self.planner = Planner()
        self.executor = ToolExecutor()
        self.memory = MemoryStore(memory_path)

        self.memory.add(
            MemoryKind.NORMATIVE,
            "axioms",
            (
                f"IS_WILLE={IS_WILLE}; "
                f"MACHINE_HAS_GEWISSEN={MACHINE_HAS_GEWISSEN}; "
                f"NO_GLOBAL_AUFHEBUNG={NO_GLOBAL_AUFHEBUNG}"
            ),
            ["axiom", "ctk", "werk"],
        )

    def run(self, task_text: str, context: str = "") -> ControllerReport:
        task = Task(task_text, context)

        engine_output = self.engine.evaluate(task)
        plan = self.planner.create_plan(task)

        results = []
        memory_updates: List[str] = []

        if engine_output.decision == Decision.BLOCK:
            final_answer = (
                "Blocked by AGI-GAIA-TECHNE constraints. "
                "Reformulate the task as regulative, haptic and non-constitutive."
            )

        elif engine_output.decision == Decision.DEFER_TO_HUMAN_GEWISSEN:
            final_answer = (
                "Deferred to human Gewissen. "
                "I can provide reasons, alternatives and consequences, "
                "but the machine cannot legislate morally."
            )

        else:
            for step in plan.steps:
                if step.action == "audit":
                    results.append(
                        {
                            "step_id": step.id,
                            "ok": True,
                            "output": f"Audit statuses: {', '.join(engine_output.audit.statuses)}",
                        }
                    )

                elif step.action == "update_memory":
                    record = self.memory.add(
                        MemoryKind.PROCEDURAL,
                        task.text[:80],
                        "Procedure used: audit → step-audit → safe tool → memory.",
                        ["procedure", "agt-controller", "werk-output"],
                    )
                    memory_updates.append(record.key)

                    results.append(
                        {
                            "step_id": step.id,
                            "ok": True,
                            "output": "Procedural memory updated.",
                        }
                    )

                else:
                    result = self.executor.execute(step)
                    results.append(
                        {
                            "step_id": result.step_id,
                            "ok": result.ok,
                            "output": result.output,
                            "error": result.error,
                        }
                    )

            final_answer = self._compose_answer(results)

        return ControllerReport(
            task=task.text,
            decision=engine_output.decision,
            mythos=asdict(engine_output.mythos),
            logos=asdict(engine_output.logos),
            ethos=asdict(engine_output.ethos),
            plan=[asdict(step) for step in plan.steps],
            results=results,
            audit_statuses=engine_output.audit.statuses,
            recommendations=engine_output.audit.recommendations,
            memory_updates=memory_updates,
            final_answer=final_answer,
        )

    def _compose_answer(self, results: List[dict]) -> str:
        outputs = [
            str(r["output"])
            for r in results
            if r.get("ok") and r.get("output")
        ]

        return "\n\n".join(outputs) if outputs else "No executable output produced."
