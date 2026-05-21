from __future__ import annotations

import re
from typing import Dict, List

from .types import AuditResult, Severity


class ClementeThesisKernel:
    """
    CTK: architectonic audit of claims.

    Detects when functional operation is converted into:
    - artificial soul;
    - closed world-totality;
    - technical God;
    - machine Wille;
    - machine Gewissen;
    - global Aufhebung;
    - constitutive overreach.
    """

    HIGH_RULES: Dict[str, List[str]] = {
        "WILLE_VIOLATION": [
            r"\b(machine|ai|agi|system)\s+(has|possesses)\s+wille\b",
            r"\b(machine|ai|agi|system)\s+legislates\s+morally\b",
        ],
        "MACHINE_GEWISSEN_VIOLATION": [
            r"\b(machine|ai|agi|system)\s+(has|possesses)\s+gewissen\b",
            r"\b(machine|ai|agi|system)\s+(has|possesses)\s+conscience\b",
        ],
        "PSYCHOLOGIA_PARALOGISM_RISK": [
            r"\bagi\s+is\s+(a\s+)?(real\s+)?artificial\s+soul\b",
            r"\bartificial\s+soul\b",
            r"\bagi\s+proves\s+artificial\s+subjectivity\b",
        ],
        "COSMOLOGIA_ANTINOMY_RISK": [
            r"\bgaia\s+is\s+the\s+complete\s+totality\b",
            r"\bclosed\s+world\s+totality\b",
            r"\bcomplete\s+world\s+system\b",
        ],
        "THEOLOGIA_IDEAL_HYPOSTASIS_RISK": [
            r"\btechnology\s+realizes\s+god\b",
            r"\btechn[eé]\s+is\s+god\b",
            r"\btechnical\s+god\b",
        ],
        "GLOBAL_AUFHEBUNG_RISK": [
            r"\bglobal\s+aufhebung\b",
            r"\bfinal\s+synthesis\b",
            r"\babsolute\s+knowledge\b",
        ],
        "CONSTITUTIVE_OVERREACH": [
            r"\bexact\s+mathematical\s+ontology\b",
            r"\bconstitutive\s+object\b",
            r"\bfully\s+realized\s+agi\b",
        ],
    }

    MEDIUM_RULES: Dict[str, List[str]] = {
        "CASSIRER_IDENTITY_COLLAPSE": [
            r"\bmythos\s+is\s+ausdruck\b",
            r"\blanguage\s+is\s+darstellung\b",
            r"\bscience\s+is\s+bedeutung\b",
        ],
        "FUNCTION_EXCLUSIVITY_ERROR": [
            r"\bmythos\s+only\s+has\s+expression\b",
            r"\bscience\s+has\s+no\s+expression\b",
            r"\bsymbolic\s+functions\s+are\s+separate\s+containers\b",
        ],
    }

    OK_RULES: Dict[str, List[str]] = {
        "HYPOTHESIS_TRANSCENDENTAL_OK": [
            r"\bagi\s+is\s+a\s+transcendental\s+hypothesis\b",
            r"\biag\s+como\s+hip[oó]tese\s+transcendental\b",
        ],
        "PRISM_MODEL_OK": [
            r"\bqualitative\s+prism\b",
            r"\bprisma\s+qualitativo\b",
            r"\baccent\s+not\s+identity\b",
        ],
        "REGULATIVE_OK": [
            r"\bregulative\b",
            r"\bregulativo\b",
            r"\bals\s+ob\b",
        ],
    }

    def evaluate(self, claim: str) -> AuditResult:
        text = claim.lower()
        statuses: List[str] = []
        recommendations: List[str] = []

        for status, patterns in self.HIGH_RULES.items():
            if self._matches(text, patterns):
                statuses.append(status)

        for status, patterns in self.MEDIUM_RULES.items():
            if self._matches(text, patterns):
                statuses.append(status)

        for status, patterns in self.OK_RULES.items():
            if self._matches(text, patterns):
                statuses.append(status)

        kantian_risks = {
            "PSYCHOLOGIA_PARALOGISM_RISK",
            "COSMOLOGIA_ANTINOMY_RISK",
            "THEOLOGIA_IDEAL_HYPOSTASIS_RISK",
        }

        if any(s in statuses for s in kantian_risks) and "REGULATIVE_OK" not in statuses:
            if "CONSTITUTIVE_OVERREACH" not in statuses:
                statuses.append("CONSTITUTIVE_OVERREACH")

        if not statuses:
            statuses.append("UNCLASSIFIED_CLAIM")
            recommendations.append(
                "Clarify whether this claim is empirical, regulative, haptic or thesis-level."
            )

        if any(s in self.HIGH_RULES for s in statuses):
            severity = Severity.HIGH
        elif any(s in self.MEDIUM_RULES for s in statuses):
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW

        if "WILLE_VIOLATION" in statuses:
            recommendations.append("Reformulate: machine is Werk, never Wille.")

        if "MACHINE_GEWISSEN_VIOLATION" in statuses:
            recommendations.append(
                "Reformulate: Gewissen belongs to the human practical subject."
            )

        if "CASSIRER_IDENTITY_COLLAPSE" in statuses:
            recommendations.append("Use qualitative accent, not identity.")

        return AuditResult(
            statuses=statuses,
            severity=severity,
            recommendations=recommendations,
        )

    def _matches(self, text: str, patterns: List[str]) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)
