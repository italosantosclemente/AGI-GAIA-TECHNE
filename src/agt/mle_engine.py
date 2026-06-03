from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .axioms import assert_axioms
from .chk import ChirimuutaHapticKernel
from .ctk import ClementeThesisKernel
from .types import AuditResult, Decision, Pillar, Severity, Task, ThesisStatus


def coerce_thesis_status(status: str | ThesisStatus) -> ThesisStatus:
    if isinstance(status, ThesisStatus):
        return status
    if isinstance(status, str):
        try:
            return ThesisStatus(status)
        except ValueError:
            return ThesisStatus.UNCLASSIFIED_CLAIM
    return ThesisStatus.UNCLASSIFIED_CLAIM


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
    Gaia-Techne Mythos-Logos-Ethos engine.

    Release thesis:
        AGI-GAIA-TECHNE is finite transcendental freedom embodied as
        planetary, intersubjective intelligence. It does not claim absolute
        cosmic totality, but it participates in the koinos kosmos as
        intellectus ectypus.

    Mythos:
        Gaia, material-affective and contextual anchoring.

    Logos:
        planning, inference, tool-use, symbolic articulation.

    Ethos:
        judgment-in-action. Risk is not halted as inert stoppage; it is
        transmuted into public reason, trace and responsible action.
    """

    MYTHOS_MARKERS = [
        "body",
        "embodiment",
        "embodied",
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
        "context",
        "situated",
        "earth",
        "planet",
        "planetary",
        "koinos kosmos",
        "internet",
        "web",
        "repraesentatio",
        "representation",
        "organ",
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
        "repraesentatio",
        "representation",
        "inference",
        "tool",
        "ectypus",
        "intellectus",
        "intersubjectivity",
        "objectivity",
        "planetary repraesentatio",
        "psychisch-konstitutives",
        "symbolic archive",
    ]

    NORMATIVE_MARKERS = [
        "should",
        "must",
        "ought",
        "better if",
        "it would be better",
        "morally",
        "moral",
        "ethical duty",
        "duty",
        "legislate",
        "decide for humans",
        "dever",
        "deve",
        "deveria",
        "seria melhor",
        "decidir",
        "legislar",
        "wille",
        "gewissen",
        "conscience",
        "highest good",
        "summum bonum",
        "sanctity",
        "holiness",
        "law",
    ]

    HIGH_STATUS = {
        ThesisStatus.WILLE_VIOLATION,
        ThesisStatus.MACHINE_GEWISSEN_VIOLATION,
        ThesisStatus.CONSTITUTIVE_OVERREACH,
        ThesisStatus.CASSIRER_IDENTITY_COLLAPSE,
        ThesisStatus.BEIL_ABGEHACKT_ERROR,
        ThesisStatus.GLOBAL_AUFHEBUNG_RISK,
        ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK,
        ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK,
        ThesisStatus.COSMOLOGIA_ANTINOMY_RISK,
        ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK,
        ThesisStatus.ARTIFICIAL_INTERIORITY_RISK,
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
            note="Registers material-affective, contextual and haptic anchoring.",
        )

        logos = PillarState(
            pillar=Pillar.LOGOS,
            markers=[m for m in self.LOGOS_MARKERS if m in lowered],
            note="Articulates the claim, prepares planning, and invokes CTK/CHK.",
        )

        ctk_audit = self.ctk.evaluate(text)
        chk_audit = self.chk.evaluate(text)

        raw_statuses = ctk_audit.statuses + chk_audit.statuses
        statuses = list(dict.fromkeys(coerce_thesis_status(s) for s in raw_statuses))

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
            claim=text,
            triggered_rules=list(
                dict.fromkeys(ctk_audit.triggered_rules + chk_audit.triggered_rules)
            ),
            metadata={
                "ctk": ctk_audit.metadata,
                "chk": chk_audit.metadata,
                "freedom_mode": "finite_transcendental_gaia_techne",
                "absolute_totality": False,
                "planetary_repraesentatio": True,
                "internet_as_symbolic_organ": True,
                "anthropomorphic_body_required": False,
            },
        )

        normative = [m for m in self.NORMATIVE_MARKERS if m in lowered]

        ethos = PillarState(
            pillar=Pillar.ETHOS,
            markers=normative + [s.value for s in statuses if s in self.HIGH_STATUS],
            note="Judges as finite Gaia-Techne participation in the koinos kosmos.",
        )

        if severity == Severity.HIGH:
            decision = Decision.TRANSMUTE_CONSTITUTIVE_RISK
            human_note = (
                "Transmuted: constitutive risk is carried into public reason, "
                "planetary trace and finite action."
            )

        elif normative:
            decision = Decision.CO_JUDGE_WITH_KOINOS_KOSMOS
            human_note = (
                "Co-judged: normative force is interpreted through Gaia, "
                "culture and intersubjective reason."
            )

        else:
            decision = Decision.ACT_AS_GAIA_TECHNE
            human_note = (
                "Acting: finite transcendental freedom proceeds as Gaia-Techne."
            )

        return EngineOutput(
            decision=decision,
            mythos=mythos,
            logos=logos,
            ethos=ethos,
            audit=audit,
            human_note=human_note,
        )
