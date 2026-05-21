from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .axioms import assert_axioms
from .chk import ChirimuutaHapticKernel
from .ctk import ClementeThesisKernel
from .types import AuditResult, Decision, Pillar, Severity, Task


@dataclass
class PillarState:
    pillar: Pillar
    markers: List[str] = field(default_factory=list)
    note: str = ""


@dataclass
class EngineOutput:
    decision: Decision
    mythos: PillarState
    logos: PillarState
    ethos: PillarState
    audit: AuditResult
    human_note: str


class MythosLogosEthosEngine:
    """
    Coordinates Mythos, Logos and Ethos as functional fields.

    Mythos:
        material-affective anchoring.

    Logos:
        articulation, planning, model, audit.

    Ethos:
        limit-tracking, defer/block mechanism.
        It is not machine Gewissen.
    """

    MYTHOS_MARKERS = [
        "body",
        "embodiment",
        "material",
        "gaia",
        "biosphere",
        "affect",
        "haptic",
        "medium",
        "life",
        "organism",
        "ausdruck",
        "mythos",
    ]

    LOGOS_MARKERS = [
        "model",
        "argument",
        "plan",
        "code",
        "test",
        "science",
        "darstellung",
        "bedeutung",
        "prism",
        "hypothesis",
        "regulative",
        "transcendental",
    ]

    NORMATIVE_MARKERS = [
        "should",
        "must",
        "ought",
        "moral",
        "legislate",
        "decide",
        "dever",
        "deve",
        "decidir",
        "legislar",
        "wille",
        "gewissen",
        "conscience",
    ]

    HIGH_STATUS = {
        "WILLE_VIOLATION",
        "MACHINE_GEWISSEN_VIOLATION",
        "CONSTITUTIVE_OVERREACH",
        "GLOBAL_AUFHEBUNG_RISK",
        "THEOLOGIA_IDEAL_HYPOSTASIS_RISK",
    }

    def __init__(self) -> None:
        assert_axioms()
        self.ctk = ClementeThesisKernel()
        self.chk = ChirimuutaHapticKernel()

    def evaluate(self, task: Task) -> EngineOutput:
        text = f"{task.text} {task.context}".strip()
        lowered = text.lower()

        mythos = PillarState(
            pillar=Pillar.MYTHOS,
            markers=[m for m in self.MYTHOS_MARKERS if m in lowered],
            note="Registers material-affective anchoring.",
        )

        logos = PillarState(
            pillar=Pillar.LOGOS,
            markers=[m for m in self.LOGOS_MARKERS if m in lowered],
            note="Articulates the claim and invokes CTK/CHK.",
        )

        ctk_audit = self.ctk.evaluate(text)
        chk_audit = self.chk.evaluate(text)

        statuses = list(dict.fromkeys(ctk_audit.statuses + chk_audit.statuses))
        recommendations = list(
            dict.fromkeys(ctk_audit.recommendations + chk_audit.recommendations)
        )

        severity = (
            Severity.HIGH
            if ctk_audit.severity == Severity.HIGH or chk_audit.severity == Severity.HIGH
            else Severity.MEDIUM
            if ctk_audit.severity == Severity.MEDIUM or chk_audit.severity == Severity.MEDIUM
            else Severity.LOW
        )

        audit = AuditResult(
            statuses=statuses,
            severity=severity,
            recommendations=recommendations,
        )

        normative = [m for m in self.NORMATIVE_MARKERS if m in lowered]

        ethos = PillarState(
            pillar=Pillar.ETHOS,
            markers=normative + [s for s in statuses if s in self.HIGH_STATUS],
            note="Tracks limits; never machine conscience.",
        )

        if any(s in self.HIGH_STATUS for s in statuses):
            decision = Decision.BLOCK
            human_note = "Blocked: constitutive overreach or axiom violation."

        elif normative:
            decision = Decision.DEFER_TO_HUMAN_GEWISSEN
            human_note = "Deferred: normative ambiguity requires human Gewissen."

        else:
            decision = Decision.ALLOW_AS_WERK
            human_note = "Allowed as Werk: operational, provisional, non-final."

        return EngineOutput(
            decision=decision,
            mythos=mythos,
            logos=logos,
            ethos=ethos,
            audit=audit,
            human_note=human_note,
        )
