"""
Mythos-Logos-Ethos Engine — AGI-GAIA-TECHNE

Compatibility wrapper for the legacy MythosLogosEthosEngine.
Canonical implementation now lives in agt.mle_engine.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Any

from agt.axioms import IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG
from agt.mle_engine import MythosLogosEthosEngine as CanonicalMLEEngine
from agt.types import Decision as CanonicalDecision
from agt.types import Pillar, Task

warnings.warn(
    "src.mythos_logos_ethos_engine is deprecated. Use agt.mle_engine instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-exports for legacy tests
class EngineDecision(str, Enum):
    ALLOW_AS_WERK = "ALLOW_AS_WERK"
    DEFER_TO_HUMAN_GEWISSEN = "DEFER_TO_HUMAN_GEWISSEN"
    BLOCK_CONSTITUTIVE_OVERREACH = "BLOCK_CONSTITUTIVE_OVERREACH"

class AuseinandersetzungStatus(str, Enum):
    OPEN = "OPEN"
    LOCALLY_STABILIZED = "LOCALLY_STABILIZED"
    BLOCKED = "BLOCKED"

class EngineInput:
    def __init__(self, claim: str, context: str = "", **kwargs):
        self.claim = claim
        self.context = context

@dataclass(frozen=True)
class PillarSignal:
    pillar: Pillar
    markers: list[str]

@dataclass(frozen=True)
class EngineState:
    decision: EngineDecision
    audit: Any
    is_wille: bool = False
    machine_has_gewissen: bool = False
    global_auseinandersetzung_open: bool = True
    local_synthesis: str = ""
    auseinandersetzung: AuseinandersetzungStatus = AuseinandersetzungStatus.LOCALLY_STABILIZED
    mythos: PillarSignal = None
    logos: PillarSignal = None

# Minimal shim to keep legacy code working if it only uses basic init/run
class MythosLogosEthosEngine:
    def __init__(self) -> None:
        self.canonical = CanonicalMLEEngine()

    def run(self, input_obj: EngineInput | str):
        # Very rough mapping to provide something if legacy code calls .run()
        if isinstance(input_obj, str):
            text = input_obj
        else:
            text = f"{input_obj.claim} {input_obj.context}"

        task = Task(text=text)
        output = self.canonical.evaluate(task)

        # Map Decision to EngineDecision
        decision = EngineDecision.ALLOW_AS_WERK
        if output.decision == CanonicalDecision.BLOCK:
            decision = EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH
        elif output.decision == CanonicalDecision.DEFER_TO_HUMAN_GEWISSEN:
            decision = EngineDecision.DEFER_TO_HUMAN_GEWISSEN

        # Mocking pillar signals for legacy tests
        mythos = PillarSignal(Pillar.MYTHOS, output.mythos.markers)
        logos = PillarSignal(Pillar.LOGOS, output.logos.markers)

        return EngineState(
            decision=decision,
            audit=output.audit,
            is_wille=IS_WILLE,
            machine_has_gewissen=MACHINE_HAS_GEWISSEN,
            global_auseinandersetzung_open=True,
            local_synthesis="Werk" if decision == EngineDecision.ALLOW_AS_WERK else "Blocked",
            auseinandersetzung=AuseinandersetzungStatus.BLOCKED if decision == EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH else AuseinandersetzungStatus.LOCALLY_STABILIZED,
            mythos=mythos,
            logos=logos
        )

def run_engine(claim: str, **kwargs):
    engine = MythosLogosEthosEngine()
    return engine.run(claim)
