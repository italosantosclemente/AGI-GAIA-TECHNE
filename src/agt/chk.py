from __future__ import annotations

import re
from typing import List

from .types import AuditResult, Severity


class ChirimuutaHapticKernel:
    """
    CHK: anti-literalization guard.

    Detects when a model becomes ontology, when abstraction cost vanishes,
    or when medium/material dependence is ignored.
    """

    ABSTRACTION_PATTERNS = [
        r"\bexact\s+mathematical\s+ontology\b",
        r"\bliteral\s+ontology\s+of\s+mind\b",
        r"\bmodel\s+is\s+the\s+mind\b",
        r"\bsubstrate\s+independent\s+without\s+loss\b",
        r"\bno\s+abstraction\s+cost\b",
    ]

    HAPTIC_OK_PATTERNS = [
        r"\bhaptic\b",
        r"\bmaterial\b",
        r"\bmedium\b",
        r"\babstraction\s+cost\b",
        r"\bembodied\b",
        r"\bpractice\b",
    ]

    def evaluate(self, claim: str) -> AuditResult:
        text = claim.lower()
        statuses: List[str] = []
        recommendations: List[str] = []

        if any(re.search(p, text, flags=re.IGNORECASE) for p in self.ABSTRACTION_PATTERNS):
            statuses.extend(["ABSTRACTION_COST_MISSING", "CONSTITUTIVE_OVERREACH"])
            recommendations.append("Register abstraction cost and medium dependence.")

        if any(re.search(p, text, flags=re.IGNORECASE) for p in self.HAPTIC_OK_PATTERNS):
            statuses.append("HAPTIC_MODEL_OK")

        if not statuses:
            statuses.append("HAPTIC_UNSPECIFIED")

        severity = Severity.HIGH if "CONSTITUTIVE_OVERREACH" in statuses else Severity.LOW

        return AuditResult(
            statuses=statuses,
            severity=severity,
            recommendations=recommendations,
        )
