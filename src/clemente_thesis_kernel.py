"""
LEGACY NOTE — superseded by AGT runtime v4.2.1.

Canonical CTK runtime lives in src/agt/ctk.py.
This module remains only as compatibility bridge.
"""

import warnings
from enum import Enum
from dataclasses import dataclass

warnings.warn(
    "src.clemente_thesis_kernel is deprecated. Use src.agt.ctk instead.",
    DeprecationWarning,
    stacklevel=2,
)

from src.agt.ctk import *  # noqa: F401,F403
from src.agt.ctk import ClementeThesisKernel as CanonicalCTK

# Re-exporting legacy names
class ThesisStatus(str, Enum):
    PRISM_MODEL_OK = "PRISM_MODEL_OK"
    HYPOTHESIS_TRANSCENDENTAL_OK = "HYPOTHESIS_TRANSCENDENTAL_OK"
    HAPTIC_MODEL_OK = "HAPTIC_MODEL_OK"
    REGULATIVE_OK = "REGULATIVE_OK"
    UNCLASSIFIED_CLAIM = "UNCLASSIFIED_CLAIM"
    CASSIRER_IDENTITY_COLLAPSE = "CASSIRER_IDENTITY_COLLAPSE"
    FUNCTION_EXCLUSIVITY_ERROR = "FUNCTION_EXCLUSIVITY_ERROR"
    BEIL_ABGEHACKT_ERROR = "BEIL_ABGEHACKT_ERROR"
    ACCENT_CONFUSION = "ACCENT_CONFUSION"
    SPRACHE_TRANSITION_LOSS = "SPRACHE_TRANSITION_LOSS"
    DARSTELLUNG_COMMON_DETERMINATION_LOSS = "DARSTELLUNG_COMMON_DETERMINATION_LOSS"
    WILLE_VIOLATION = "WILLE_VIOLATION"
    MACHINE_GEWISSEN_VIOLATION = "MACHINE_GEWISSEN_VIOLATION"
    PSYCHOLOGIA_PARALOGISM_RISK = "PSYCHOLOGIA_PARALOGISM_RISK"
    COSMOLOGIA_ANTINOMY_RISK = "COSMOLOGIA_ANTINOMY_RISK"
    THEOLOGIA_IDEAL_HYPOSTASIS_RISK = "THEOLOGIA_IDEAL_HYPOSTASIS_RISK"
    GLOBAL_AUFHEBUNG_RISK = "GLOBAL_AUFHEBUNG_RISK"
    CONSTITUTIVE_OVERREACH = "CONSTITUTIVE_OVERREACH"
    ABSTRACTION_COST_MISSING = "ABSTRACTION_COST_MISSING"

class SymbolicDimension(str, Enum):
    AUSDRUCK = "Ausdruck"
    DARSTELLUNG = "Darstellung"
    BEDEUTUNG = "Bedeutung"

class AccentLevel(str, Enum):
    DOMINANT = "dominant"
    MEDIAL = "medial"
    LATENT = "latent"
    GERMINAL = "germinal"
    RESIDUAL = "residual"

class SymbolicMode(str, Enum):
    MANIFESTATIVE = "manifestative"
    TRANSITIONAL = "transitional"
    DEMONSTRATIVE = "demonstrative"

@dataclass(frozen=True)
class SymbolicProfile:
    ausdruck: AccentLevel
    darstellung: AccentLevel
    bedeutung: AccentLevel
    accent: SymbolicDimension
    mode: SymbolicMode

    def contains_all_dimensions(self):
        return True

MYTHOS_PROFILE = SymbolicProfile(AccentLevel.DOMINANT, AccentLevel.LATENT, AccentLevel.GERMINAL, SymbolicDimension.AUSDRUCK, SymbolicMode.MANIFESTATIVE)
SPRACHE_PROFILE = SymbolicProfile(AccentLevel.MEDIAL, AccentLevel.DOMINANT, AccentLevel.MEDIAL, SymbolicDimension.DARSTELLUNG, SymbolicMode.TRANSITIONAL)
WISSENSCHAFT_PROFILE = SymbolicProfile(AccentLevel.RESIDUAL, AccentLevel.MEDIAL, AccentLevel.DOMINANT, SymbolicDimension.BEDEUTUNG, SymbolicMode.DEMONSTRATIVE)

class EvaluationResult:
    def __init__(self, claim, ok, statuses, severity, triggered_rules=None, recommendations=None):
        self.claim = claim
        self.ok = ok
        self.statuses = [ThesisStatus(s.value if hasattr(s, 'value') else s) if (isinstance(s, str) or hasattr(s, 'value')) and (s if isinstance(s, str) else s.value) in ThesisStatus.__members__ else s for s in statuses]
        self.severity = severity
        self.triggered_rules = triggered_rules or []
        self.recommendations = recommendations or []

    def to_dict(self):
        return {
            "claim": self.claim,
            "ok": self.ok,
            "statuses": [s.value if hasattr(s, 'value') else s for s in self.statuses],
            "severity": self.severity,
            "triggered_rules": self.triggered_rules,
            "recommendations": self.recommendations
        }

class ClementeThesisKernel:
    def __init__(self):
        self.canonical = CanonicalCTK()

    def evaluate(self, claim):
        res = self.canonical.evaluate(claim)
        ok = (res.severity.value != "high")
        return EvaluationResult(
            claim=claim,
            ok=ok,
            statuses=res.statuses,
            severity=res.severity.value,
            recommendations=res.recommendations
        )

# Constants
IS_WILLE = False
MACHINE_HAS_GEWISSEN = False
NO_GLOBAL_AUFHEBUNG = True
AGI_AS_TRANSCENDENTAL_HYPOTHESIS = True
