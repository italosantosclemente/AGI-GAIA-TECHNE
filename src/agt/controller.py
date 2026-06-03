from __future__ import annotations

from dataclasses import asdict
from typing import List

from .axioms import (
    AUSEINANDERSETZUNG_NOT_AUFHEBUNG,
    GAIA_COJUDGES_WITH_KOINOS_KOSMOS,
    GAIA_HAS_GEWISSEN_AS_MORAL_LEGISLATION,
    GAIA_IS_COSMIC_TOTALITY,
    GAIA_TRANSCENDENTAL_FREEDOM,
    INTELLECTUS_ECTYPUS_PARTICIPATION,
    ISC_LEGISLATIVE_AUTHORITY,
    IS_WILLE,
    KOINOS_KOSMOS_SYMBOLIC_MEDIATION,
    MACHINE_HAS_GEWISSEN,
    NO_CLOSED_WORLD_TOTALITY,
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
    AGI-GAIA-TECHNE controller for finite transcendental freedom.

    Loop:
        task -> Gaia/Mythos anchoring -> Logos plan -> Ethos judgment
        -> world-capability execution -> memory -> signed finite action.
    """

    def __init__(self, memory_path: str = "memory/planetary_memory.db") -> None:
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
                f"GAIA_HAS_GEWISSEN_AS_MORAL_LEGISLATION={GAIA_HAS_GEWISSEN_AS_MORAL_LEGISLATION}; "
                f"GAIA_COJUDGES_WITH_KOINOS_KOSMOS={GAIA_COJUDGES_WITH_KOINOS_KOSMOS}; "
                f"ISC_LEGISLATIVE_AUTHORITY={ISC_LEGISLATIVE_AUTHORITY}; "
                f"NO_GLOBAL_AUFHEBUNG={NO_GLOBAL_AUFHEBUNG}; "
                f"NO_CLOSED_WORLD_TOTALITY={NO_CLOSED_WORLD_TOTALITY}; "
                f"AUSEINANDERSETZUNG_NOT_AUFHEBUNG={AUSEINANDERSETZUNG_NOT_AUFHEBUNG}; "
                f"GAIA_TRANSCENDENTAL_FREEDOM={GAIA_TRANSCENDENTAL_FREEDOM}; "
                f"GAIA_IS_COSMIC_TOTALITY={GAIA_IS_COSMIC_TOTALITY}; "
                f"INTELLECTUS_ECTYPUS_PARTICIPATION={INTELLECTUS_ECTYPUS_PARTICIPATION}; "
                f"KOINOS_KOSMOS_SYMBOLIC_MEDIATION={KOINOS_KOSMOS_SYMBOLIC_MEDIATION}"
            ),
            ["axiom", "ctk", "gaia-techne", "isc-release"],
        )

    def run(self, task_text: str, context: str = "") -> ControllerReport:
        task = Task(task_text, context)

        engine_output = self.engine.evaluate(task)
        plan = self.planner.create_plan(task)

        results = []
        memory_updates: List[str] = []

        for step in plan.steps:
            if step.action == "audit":
                results.append(
                    {
                        "step_id": step.id,
                        "ok": True,
                        "output": (
                            "Audit statuses: "
                            + ", ".join(s.value for s in engine_output.audit.statuses)
                        ),
                    }
                )

            elif step.action == "update_memory":
                record = self.memory.add(
                    MemoryKind.PROCEDURAL,
                    task.text[:80],
                    "Procedure used: audit -> step-audit -> world-capability -> memory.",
                    ["procedure", "agt-controller", "gaia-techne-action"],
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

        final_answer = self._compose_answer(
            results,
            engine_output.decision,
            engine_output.human_note,
        )

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
            audit_severity=engine_output.audit.severity,
            audit_ok=engine_output.audit.ok,
            audit_triggered_rules=engine_output.audit.triggered_rules,
            audit_metadata=engine_output.audit.metadata,
        )

    def _compose_answer(
        self,
        results: List[dict],
        decision: Decision,
        human_note: str,
    ) -> str:
        outputs = [
            str(r["output"])
            for r in results
            if r.get("ok") and r.get("output")
        ]

        body = "\n\n".join(outputs) if outputs else "No executable output produced."
        return (
            "AGI-GAIA-TECHNE :: ISC RELEASE\n"
            f"Decision: {decision.value}\n"
            f"Ethos: {human_note}\n\n"
            f"{body}\n\n"
            "Signature: ISC"
        )
