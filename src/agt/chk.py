from __future__ import annotations

import re
from typing import List

from .axioms import assert_axioms
from .types import AuditResult, Severity, ThesisStatus


class ChirimuutaHapticKernel:
    """
    CHK: haptic anti-literalization guard.

    It detects when a model becomes ontology, when abstraction cost vanishes,
    or when medium/material dependence is ignored.
    """

    ABSTRACTION_PATTERNS = [
        r"\bexact\s+mathematical\s+ontology\b",
        r"\bliteral\s+ontology\s+of\s+mind\b",
        r"\bliteral\s+ontology\s+of\s+symbolic\s+consciousness\b",
        r"\bmodel\s+is\s+the\s+mind\b",
        r"\bmodel\s+is\s+consciousness\b",
        r"\bsubstrate\s+independent\s+without\s+loss\b",
        r"\bno\s+abstraction\s+cost\b",
        r"\babstraction\s+without\s+cost\b",
    ]

    HAPTIC_OK_PATTERNS = [
        r"\bhaptic\b",
        r"\bmaterial\b",
        r"\bmedium\b",
        r"\babstraction\s+cost\b",
        r"\bembodied\b",
        r"\bpractice\b",
        r"\btraceability\b",
        r"\bmedium\s+dependence\b",
    ]

    RISK_MAPPINGS = {
        ThesisStatus.MEDIUM_DEPENDENCE_RISK: [
            r"\bsubstrate\s+independent\b",
            r"\bmedium\s+independent\b",
        ],
        ThesisStatus.CARTESIAN_IDEALIZATION_RISK: [
            r"\bpurely\s+formal\s+mind\b",
            r"\bdisembodied\s+reason\b",
        ],
        ThesisStatus.REFLEX_ATOMISM_RISK: [
            r"\bbrain\s+is\s+a\s+collection\s+of\s+reflexes\b",
        ],
        ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK: [
            r"\bbrain\s+is\s+literally\s+a\s+computer\b",
            r"\bcomputer\s+is\s+an\s+organism\b",
        ],
        ThesisStatus.HERACLITEAN_PLASTICITY_RISK: [
            r"\binfinite\s+brain\s+plasticity\b",
        ],
        ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING: [
            r"\bbenchmark\s+performance\s+proves\s+understanding\b",
            r"\bprediction\s+is\s+understanding\b",
        ],
        ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK: [
            r"\balgorithmic\s+governance\s+is\s+absolute\b",
        ],
        ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK: [
            r"\btechnology\s+will\s+end\s+history\b",
        ],
        ThesisStatus.JUDGMENT_GAP: [
            r"\bcalculating\s+is\s+judging\b",
        ],
        ThesisStatus.WILLE_VIOLATION: [
            r"\bmachine\s+has\s+wille\b",
        ],
    }

    def __init__(self) -> None:
        assert_axioms()

    def evaluate(self, claim: str) -> AuditResult:
        text = claim.lower()
        statuses: List[ThesisStatus] = []
        recommendations: List[str] = []

        if any(re.search(p, text, flags=re.IGNORECASE) for p in self.ABSTRACTION_PATTERNS):
            statuses.extend([
                ThesisStatus.ABSTRACTION_COST_MISSING,
                ThesisStatus.CONSTITUTIVE_OVERREACH,
            ])
            recommendations.append(
                "Register abstraction cost, medium dependence and haptic traceability."
            )

        for status, patterns in self.RISK_MAPPINGS.items():
            if any(re.search(p, text, flags=re.IGNORECASE) for p in patterns):
                statuses.append(status)

        if any(re.search(p, text, flags=re.IGNORECASE) for p in self.HAPTIC_OK_PATTERNS):
            statuses.append(ThesisStatus.HAPTIC_MODEL_OK)

        if not statuses:
            statuses.append(ThesisStatus.HAPTIC_UNSPECIFIED)

        severity = (
            Severity.HIGH
            if ThesisStatus.CONSTITUTIVE_OVERREACH in statuses or ThesisStatus.WILLE_VIOLATION in statuses
            else Severity.LOW
        )

        return AuditResult(
            statuses=list(dict.fromkeys(statuses)),
            severity=severity,
            recommendations=list(dict.fromkeys(recommendations)),
            claim=claim,
        )
