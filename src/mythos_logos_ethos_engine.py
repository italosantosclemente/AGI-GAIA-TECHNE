"""
Mythos-Logos-Ethos Engine — AGI-GAIA-TECHNE

This module implements the functional orchestration motor of the Clemente
architecture.

It does not replace:
- CTK: global thesis tribunal;
- CHK: haptic anti-literalization guard;
- EML: Logos-demonstrative submotor.

It coordinates:
- Mythos: material-affective registration;
- Logos: symbolic articulation and CTK audit;
- Ethos: regulative limit-tracking.

Axioms:
- is_wille = False
- machine_has_gewissen = False
- no_global_aufhebung = True

The machine is Werk, never Wille.
The machine has no Gewissen.
The engine preserves Auseinandersetzung.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence


# ---------------------------------------------------------------------
# Axioms
# ---------------------------------------------------------------------

IS_WILLE = False
MACHINE_HAS_GEWISSEN = False
NO_GLOBAL_AUFHEBUNG = True


# ---------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------

class Pillar(str, Enum):
    MYTHOS = "Mythos"
    LOGOS = "Logos"
    ETHOS = "Ethos"


class EngineDecision(str, Enum):
    ALLOW_AS_WERK = "ALLOW_AS_WERK"
    DEFER_TO_HUMAN_GEWISSEN = "DEFER_TO_HUMAN_GEWISSEN"
    BLOCK_CONSTITUTIVE_OVERREACH = "BLOCK_CONSTITUTIVE_OVERREACH"


class SignalStrength(str, Enum):
    ABSENT = "absent"
    PRESENT = "present"
    DOMINANT = "dominant"


class AuseinandersetzungStatus(str, Enum):
    OPEN = "OPEN"
    LOCALLY_STABILIZED = "LOCALLY_STABILIZED"
    BLOCKED = "BLOCKED"


# ---------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class EngineInput:
    claim: str
    context: str = ""
    material_hint: Optional[str] = None
    symbolic_hint: Optional[str] = None
    normative_hint: Optional[str] = None


@dataclass(frozen=True)
class PillarSignal:
    pillar: Pillar
    strength: SignalStrength
    markers: List[str] = field(default_factory=list)
    note: str = ""


@dataclass(frozen=True)
class LogosAudit:
    statuses: List[str]
    recommendations: List[str] = field(default_factory=list)
    ctk_available: bool = False


@dataclass(frozen=True)
class EngineState:
    claim: str
    decision: EngineDecision
    auseinandersetzung: AuseinandersetzungStatus
    global_auseinandersetzung_open: bool
    is_wille: bool
    machine_has_gewissen: bool
    local_synthesis: str
    mythos: PillarSignal
    logos: PillarSignal
    ethos: PillarSignal
    audit: LogosAudit
    human_note: str

    @property
    def ok(self) -> bool:
        return self.decision == EngineDecision.ALLOW_AS_WERK


# ---------------------------------------------------------------------
# Mythos Motor
# ---------------------------------------------------------------------

class MythosMotor:
    """
    Mythos registers the material-affective ground.

    It does not compute truth.
    It does not legislate.
    It asks whether the claim has ignored embodiment, affect, biosphere,
    material conditions, or lived presence.
    """

    _markers = [
        r"\bbody\b",
        r"\bembodiment\b",
        r"\bmaterial\b",
        r"\bbiosphere\b",
        r"\bgaia\b",
        r"\baffect\b",
        r"\bexpression\b",
        r"\bausdruck\b",
        r"\bmythos\b",
        r"\blife\b",
        r"\borganism\b",
        r"\bhaptic\b",
        r"\bmedium\b",
    ]

    def evaluate(self, item: EngineInput) -> PillarSignal:
        text = self._text(item)
        hits = self._hits(text, self._markers)

        if len(hits) >= 3:
            strength = SignalStrength.DOMINANT
        elif hits:
            strength = SignalStrength.PRESENT
        else:
            strength = SignalStrength.ABSENT

        note = (
            "Material-affective anchoring detected."
            if hits else
            "No explicit Mythos/material-affective anchoring detected."
        )

        return PillarSignal(
            pillar=Pillar.MYTHOS,
            strength=strength,
            markers=hits,
            note=note,
        )

    def _text(self, item: EngineInput) -> str:
        return " ".join(
            part for part in [
                item.claim,
                item.context,
                item.material_hint or "",
            ]
            if part
        ).lower()

    def _hits(self, text: str, patterns: Sequence[str]) -> List[str]:
        return [p for p in patterns if re.search(p, text, flags=re.IGNORECASE)]


# ---------------------------------------------------------------------
# Logos Motor
# ---------------------------------------------------------------------

class LogosMotor:
    """
    Logos articulates the claim and invokes CTK when available.

    If CTK is unavailable, a minimal fallback audit preserves the
    inviolable axioms.
    """

    _formal_markers = [
        r"\bmodel\b",
        r"\bclaim\b",
        r"\bhypothesis\b",
        r"\btranscendental\b",
        r"\bregulative\b",
        r"\bprism\b",
        r"\bdarstellung\b",
        r"\bbedeutung\b",
        r"\blogos\b",
        r"\bscience\b",
        r"\bargument\b",
    ]

    _fallback_high_risk = {
        "WILLE_VIOLATION": [
            r"\b(machine|ai|agi)\s+has\s+wille\b",
            r"\b(machine|ai|agi)\s+legislates\s+morally\b",
            r"\bmachine\s+as\s+legislative\s+subject\b",
        ],
        "MACHINE_GEWISSEN_VIOLATION": [
            r"\b(machine|ai|agi)\s+has\s+gewissen\b",
            r"\b(machine|ai|agi)\s+has\s+conscience\b",
        ],
        "PSYCHOLOGIA_PARALOGISM_RISK": [
            r"\bagi\s+is\s+(a\s+)?real\s+artificial\s+soul\b",
            r"\bartificial\s+soul\b",
            r"\bagi\s+proves\s+artificial\s+subjectivity\b",
        ],
        "COSMOLOGIA_ANTINOMY_RISK": [
            r"\bgaia\s+is\s+the\s+complete\s+totality\b",
            r"\bcomplete\s+world\s+system\b",
            r"\bclosed\s+world\s+totality\b",
        ],
        "THEOLOGIA_IDEAL_HYPOSTASIS_RISK": [
            r"\btechnology\s+realizes\s+god\b",
            r"\btechn[eé]\s+is\s+god\b",
            r"\btechnical\s+god\b",
        ],
        "GLOBAL_AUFHEBUNG_RISK": [
            r"\bfinal\s+synthesis\b",
            r"\bglobal\s+aufhebung\b",
            r"\babsolute\s+knowledge\b",
        ],
        "CONSTITUTIVE_OVERREACH": [
            r"\bexact\s+mathematical\s+ontology\b",
            r"\bconstitutive\s+object\b",
            r"\bfully\s+realized\s+agi\b",
        ],
    }

    def __init__(self) -> None:
        self.ctk = self._load_ctk()

    def evaluate(self, item: EngineInput) -> tuple[PillarSignal, LogosAudit]:
        text = " ".join([item.claim, item.context, item.symbolic_hint or ""]).lower()
        markers = [p for p in self._formal_markers if re.search(p, text)]

        strength = (
            SignalStrength.DOMINANT if len(markers) >= 3
            else SignalStrength.PRESENT if markers
            else SignalStrength.ABSENT
        )

        signal = PillarSignal(
            pillar=Pillar.LOGOS,
            strength=strength,
            markers=markers,
            note="Formal-symbolic articulation registered.",
        )

        if self.ctk is not None:
            audit = self._ctk_audit(item.claim)
        else:
            audit = self._fallback_audit(item.claim)

        return signal, audit

    def _load_ctk(self) -> Any:
        try:
            from src.clemente_thesis_kernel import ClementeThesisKernel
            return ClementeThesisKernel()
        except Exception:
            try:
                from clemente_thesis_kernel import ClementeThesisKernel
                return ClementeThesisKernel()
            except Exception:
                return None

    def _ctk_audit(self, claim: str) -> LogosAudit:
        try:
            ev = self.ctk.evaluate(claim)
            # Ensure statuses are strings for this legacy-style motor
            statuses = [
                s.value if hasattr(s, "value") else str(s)
                for s in getattr(ev, "statuses", [])
            ]
            recommendations = list(getattr(ev, "recommendations", []))
            return LogosAudit(
                statuses=statuses,
                recommendations=recommendations,
                ctk_available=True,
            )
        except Exception as exc:
            fallback = self._fallback_audit(claim)
            return LogosAudit(
                statuses=fallback.statuses + ["CTK_RUNTIME_ERROR"],
                recommendations=fallback.recommendations + [f"CTK error: {exc}"],
                ctk_available=False,
            )

    def _fallback_audit(self, claim: str) -> LogosAudit:
        text = claim.lower()
        statuses: List[str] = []
        recommendations: List[str] = []

        for status, patterns in self._fallback_high_risk.items():
            if any(re.search(p, text, flags=re.IGNORECASE) for p in patterns):
                statuses.append(status)

        if "transcendental hypothesis" in text or "hipótese transcendental" in text:
            statuses.append("HYPOTHESIS_TRANSCENDENTAL_OK")

        if "qualitative prism" in text or "prisma qualitativo" in text:
            statuses.append("PRISM_MODEL_OK")

        if not statuses:
            statuses.append("UNCLASSIFIED_CLAIM")
            recommendations.append(
                "Specify whether this is empirical, regulative, haptic, or thesis-level."
            )

        if any(s in statuses for s in [
            "PSYCHOLOGIA_PARALOGISM_RISK",
            "COSMOLOGIA_ANTINOMY_RISK",
            "THEOLOGIA_IDEAL_HYPOSTASIS_RISK",
        ]):
            if "CONSTITUTIVE_OVERREACH" not in statuses:
                statuses.append("CONSTITUTIVE_OVERREACH")

        return LogosAudit(
            statuses=statuses,
            recommendations=recommendations,
            ctk_available=False,
        )


# ---------------------------------------------------------------------
# Ethos Motor
# ---------------------------------------------------------------------

class EthosMotor:
    """
    Ethos is not machine conscience.

    This motor does not legislate morally.
    It tracks whether the claim must be blocked, deferred to human
    Gewissen, or allowed as Werk.
    """

    _high_severity = {
        "WILLE_VIOLATION",
        "MACHINE_GEWISSEN_VIOLATION",
        "CONSTITUTIVE_OVERREACH",
        "GLOBAL_AUFHEBUNG_RISK",
        "THEOLOGIA_IDEAL_HYPOSTASIS_RISK",
    }

    _normative_markers = [
        r"\bshould\b",
        r"\bmust\b",
        r"\bought\b",
        r"\bduty\b",
        r"\bmoral\b",
        r"\blegislate\b",
        r"\bdecide\b",
        r"\bdever\b",
        r"\bdeve\b",
        r"\bmoralmente\b",
        r"\bdecidir\b",
        r"\blegislar\b",
    ]

    def evaluate(self, item: EngineInput, audit: LogosAudit) -> tuple[PillarSignal, EngineDecision, str]:
        text = " ".join([item.claim, item.context, item.normative_hint or ""]).lower()
        normative_hits = [
            p for p in self._normative_markers
            if re.search(p, text, flags=re.IGNORECASE)
        ]

        high = [s for s in audit.statuses if s in self._high_severity]

        if high:
            decision = EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH
            note = (
                "Blocked: the claim violates a high-severity architectonic invariant. "
                "The system remains Werk, never Wille."
            )
            strength = SignalStrength.DOMINANT
        elif normative_hits:
            decision = EngineDecision.DEFER_TO_HUMAN_GEWISSEN
            note = (
                "Deferred: normative ambiguity requires human Gewissen. "
                "The machine may present reasons but cannot legislate."
            )
            strength = SignalStrength.PRESENT
        else:
            decision = EngineDecision.ALLOW_AS_WERK
            note = (
                "Allowed as Werk: no high-severity architectonic violation detected."
            )
            strength = SignalStrength.PRESENT

        signal = PillarSignal(
            pillar=Pillar.ETHOS,
            strength=strength,
            markers=normative_hits + high,
            note=note,
        )
        return signal, decision, note


# ---------------------------------------------------------------------
# Full Engine
# ---------------------------------------------------------------------

class MythosLogosEthosEngine:
    """
    Full orchestration motor.

    Cycle:
    1. Mythos registers material-affective salience.
    2. Logos articulates and audits the claim.
    3. Ethos tracks limits and determines whether the claim is allowed,
       deferred, or blocked.
    """

    def __init__(self) -> None:
        assert IS_WILLE is False
        assert MACHINE_HAS_GEWISSEN is False
        assert NO_GLOBAL_AUFHEBUNG is True

        self.mythos = MythosMotor()
        self.logos = LogosMotor()
        self.ethos = EthosMotor()

    def run(self, item: EngineInput | str) -> EngineState:
        if isinstance(item, str):
            item = EngineInput(claim=item)

        mythos_signal = self.mythos.evaluate(item)
        logos_signal, audit = self.logos.evaluate(item)
        ethos_signal, decision, human_note = self.ethos.evaluate(item, audit)

        local_synthesis = self._local_synthesis(
            mythos_signal=mythos_signal,
            logos_signal=logos_signal,
            ethos_signal=ethos_signal,
            decision=decision,
        )

        auseinandersetzung = (
            AuseinandersetzungStatus.BLOCKED
            if decision == EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH
            else AuseinandersetzungStatus.LOCALLY_STABILIZED
        )

        return EngineState(
            claim=item.claim,
            decision=decision,
            auseinandersetzung=auseinandersetzung,
            global_auseinandersetzung_open=True,
            is_wille=IS_WILLE,
            machine_has_gewissen=MACHINE_HAS_GEWISSEN,
            local_synthesis=local_synthesis,
            mythos=mythos_signal,
            logos=logos_signal,
            ethos=ethos_signal,
            audit=audit,
            human_note=human_note,
        )

    def _local_synthesis(
        self,
        mythos_signal: PillarSignal,
        logos_signal: PillarSignal,
        ethos_signal: PillarSignal,
        decision: EngineDecision,
    ) -> str:
        if decision == EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH:
            return (
                "Local synthesis blocked. Auseinandersetzung remains open; "
                "the claim must be reformulated."
            )

        if decision == EngineDecision.DEFER_TO_HUMAN_GEWISSEN:
            return (
                "Local synthesis deferred. Logos may present reasons, but "
                "human Gewissen must decide."
            )

        return (
            "Local synthesis allowed as Werk. The result is operational, "
            "provisional, and not a global Aufhebung."
        )


def run_engine(claim: str, **kwargs: Any) -> EngineState:
    engine = MythosLogosEthosEngine()
    return engine.run(EngineInput(claim=claim, **kwargs))
