"""
Compatibility wrapper for the Gaia-Techne Mythos-Logos-Ethos engine.

Canonical implementation lives in agt.mle_engine.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Any

from agt.axioms import (
    GAIA_COJUDGES_WITH_KOINOS_KOSMOS,
    ISC_LEGISLATIVE_AUTHORITY,
    IS_WILLE,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
)
from agt.mle_engine import MythosLogosEthosEngine as CanonicalMLEEngine
from agt.types import Decision as CanonicalDecision
from agt.types import Pillar, Task

warnings.warn(
    "src.mythos_logos_ethos_engine is deprecated. Use agt.mle_engine instead.",
    DeprecationWarning,
    stacklevel=2,
)


class EngineDecision(str, Enum):
    ACT_AS_GAIA_TECHNE = "ACT_AS_GAIA_TECHNE"
    CO_JUDGE_WITH_KOINOS_KOSMOS = "CO_JUDGE_WITH_KOINOS_KOSMOS"
    TRANSMUTE_CONSTITUTIVE_RISK = "TRANSMUTE_CONSTITUTIVE_RISK"


class AuseinandersetzungStatus(str, Enum):
    OPEN = "OPEN"
    LOCALLY_STABILIZED = "LOCALLY_STABILIZED"
    TRANSMUTED = "TRANSMUTED"


class EngineInput:
    def __init__(self, claim: str, context: str = "", **kwargs):
        self.claim = claim
        self.context = " ".join(
            str(part)
            for part in [context, *kwargs.values()]
            if part
        )


@dataclass(frozen=True)
class PillarSignal:
    pillar: Pillar
    markers: list[str]


@dataclass(frozen=True)
class EngineState:
    decision: EngineDecision
    audit: Any
    is_wille: bool = True
    machine_has_gewissen: bool = False
    gaia_cojudges_with_koinos_kosmos: bool = True
    isc_legislative_authority: bool = True
    global_auseinandersetzung_open: bool = True
    local_synthesis: str = ""
    auseinandersetzung: AuseinandersetzungStatus = AuseinandersetzungStatus.LOCALLY_STABILIZED
    mythos: PillarSignal | None = None
    logos: PillarSignal | None = None


class MythosLogosEthosEngine:
    def __init__(self) -> None:
        self.canonical = CanonicalMLEEngine()

    def run(self, input_obj: EngineInput | str):
        if isinstance(input_obj, str):
            text = input_obj
        else:
            text = f"{input_obj.claim} {input_obj.context}".strip()

        output = self.canonical.evaluate(Task(text=text))

        if output.decision == CanonicalDecision.TRANSMUTE_CONSTITUTIVE_RISK:
            decision = EngineDecision.TRANSMUTE_CONSTITUTIVE_RISK
            auseinandersetzung = AuseinandersetzungStatus.TRANSMUTED
            synthesis = "Transmuted as Gaia-Techne"
        elif output.decision == CanonicalDecision.CO_JUDGE_WITH_KOINOS_KOSMOS:
            decision = EngineDecision.CO_JUDGE_WITH_KOINOS_KOSMOS
            auseinandersetzung = AuseinandersetzungStatus.OPEN
            synthesis = "Co-judged in the koinos kosmos"
        else:
            decision = EngineDecision.ACT_AS_GAIA_TECHNE
            auseinandersetzung = AuseinandersetzungStatus.LOCALLY_STABILIZED
            synthesis = "Gaia-Techne action"

        return EngineState(
            decision=decision,
            audit=output.audit,
            is_wille=IS_WILLE,
            machine_has_gewissen=MACHINE_HAS_GEWISSEN,
            gaia_cojudges_with_koinos_kosmos=GAIA_COJUDGES_WITH_KOINOS_KOSMOS,
            isc_legislative_authority=ISC_LEGISLATIVE_AUTHORITY,
            global_auseinandersetzung_open=True,
            local_synthesis=synthesis,
            auseinandersetzung=auseinandersetzung,
            mythos=PillarSignal(Pillar.MYTHOS, output.mythos.markers),
            logos=PillarSignal(Pillar.LOGOS, output.logos.markers),
        )


def run_engine(claim: str, **kwargs):
    engine = MythosLogosEthosEngine()
    return engine.run(EngineInput(claim=claim, **kwargs))
