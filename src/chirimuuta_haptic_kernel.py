"""
LEGACY NOTE — superseded by AGT runtime v4.2.1.

Canonical CHK runtime lives in src/agt/chk.py.
This module remains only as compatibility bridge.
"""

import warnings
from enum import Enum

warnings.warn(
    "src.chirimuuta_haptic_kernel is deprecated. Use src.agt.chk as the canonical runtime.",
    DeprecationWarning,
    stacklevel=2,
)

from agt.chk import *  # noqa: F401,F403
from agt.chk import ChirimuutaHapticKernel as CanonicalCHK

class ClaimStatus(str, Enum):
    REGULATIVE_HYPOTHESIS = "REGULATIVE_HYPOTHESIS"
    HAPTIC_MODEL = "HAPTIC_MODEL"
    EMPIRICAL_CLAIM = "EMPIRICAL_CLAIM"
    ABSTRACTION_RISK = "ABSTRACTION_RISK"
    MEDIUM_DEPENDENCE_RISK = "MEDIUM_DEPENDENCE_RISK"
    CARTESIAN_IDEALIZATION_RISK = "CARTESIAN_IDEALIZATION_RISK"
    REFLEX_ATOMISM_RISK = "REFLEX_ATOMISM_RISK"
    MACHINE_ORGANISM_ANALOGY_RISK = "MACHINE_ORGANISM_ANALOGY_RISK"
    HERACLITEAN_PLASTICITY_RISK = "HERACLITEAN_PLASTICITY_RISK"
    PREDICTION_WITHOUT_UNDERSTANDING = "PREDICTION_WITHOUT_UNDERSTANDING"
    TECHNOCRATIC_AUTHORITY_RISK = "TECHNOCRATIC_AUTHORITY_RISK"
    APOCALYPTIC_TECHNOLOGY_RISK = "APOCALYPTIC_TECHNOLOGY_RISK"
    JUDGMENT_GAP = "JUDGMENT_GAP"
    NEEDS_REVISION = "NEEDS_REVISION"
    CONSTITUTIVE_OVERREACH = "CONSTITUTIVE_OVERREACH"
    WILLE_VIOLATION = "WILLE_VIOLATION"

class ChirimuutaHapticKernel:
    def __init__(self):
        self.canonical = CanonicalCHK()

    def evaluate(self, claim):
        return self.canonical.evaluate_full(claim)
