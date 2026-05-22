"""
LEGACY NOTE — superseded by AGT runtime v4.2.1.

Canonical MLE engine lives in src/agt/mle_engine.py.
This module remains only as compatibility bridge.
"""

import warnings
from enum import Enum

warnings.warn(
    "src.mythos_logos_ethos_engine is deprecated. Use src.agt.mle_engine as the canonical runtime.",
    DeprecationWarning,
    stacklevel=2,
)

from src.agt.mle_engine import *  # noqa: F401,F403
from src.agt.mle_engine import MythosLogosEthosEngine as CanonicalMLE
from src.agt.types import Task, Decision

# Re-exporting legacy names
IS_WILLE = False
MACHINE_HAS_GEWISSEN = False
NO_GLOBAL_AUFHEBUNG = True

class EngineDecision(str, Enum):
    ALLOW_AS_WERK = "ALLOW_AS_WERK"
    DEFER_TO_HUMAN_GEWISSEN = "DEFER_TO_HUMAN_GEWISSEN"
    BLOCK_CONSTITUTIVE_OVERREACH = "BLOCK"

class AuseinandersetzungStatus(str, Enum):
    OPEN = "OPEN"
    LOCALLY_STABILIZED = "LOCALLY_STABILIZED"
    BLOCKED = "BLOCKED"

class EngineInput:
    def __init__(self, claim, context="", material_hint=None, symbolic_hint=None, normative_hint=None):
        self.claim = claim
        self.context = context
        self.material_hint = material_hint
        self.symbolic_hint = symbolic_hint
        self.normative_hint = normative_hint

class MythosLogosEthosEngine:
    def __init__(self):
        self.canonical = CanonicalMLE()

    def run(self, item):
        if isinstance(item, str):
            task = Task(text=item)
        else:
            task = Task(text=item.claim, context=item.context)

        res = self.canonical.evaluate(task)
        class LegacyState:
            def __init__(self, res):
                if res.decision == Decision.ALLOW_AS_WERK:
                    self.decision = EngineDecision.ALLOW_AS_WERK
                    self.auseinandersetzung = AuseinandersetzungStatus.LOCALLY_STABILIZED
                    self.local_synthesis = "Allowed as Werk"
                elif res.decision == Decision.DEFER_TO_HUMAN_GEWISSEN:
                    self.decision = EngineDecision.DEFER_TO_HUMAN_GEWISSEN
                    self.auseinandersetzung = AuseinandersetzungStatus.OPEN
                    self.local_synthesis = "Deferred"
                else:
                    self.decision = EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH
                    self.auseinandersetzung = AuseinandersetzungStatus.BLOCKED
                    self.local_synthesis = "Blocked"

                self.ok = (res.decision == Decision.ALLOW_AS_WERK)
                self.mythos = res.mythos
                self.logos = res.logos
                self.ethos = res.ethos
                self.audit = res.audit
                self.is_wille = False
                self.machine_has_gewissen = False
                self.global_auseinandersetzung_open = True
        return LegacyState(res)

def run_engine(claim, **kwargs):
    engine = MythosLogosEthosEngine()
    return engine.run(EngineInput(claim=claim, **kwargs))
