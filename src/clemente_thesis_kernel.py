"""
Clemente Thesis Kernel (CTK) v4.1 — Qualitative Prism Model

This module implements the global architectonic tribunal for AGI-GAIA-TECHNE.
It replaces rigid 1:1 mappings with a qualitative prism model of symbolic
consciousness, where every symbolic form contains Ausdruck, Darstellung,
and Bedeutung in different qualitative accents.

Axioms:
- is_wille = false
- machine_has_gewissen = false
- no_global_aufhebung = true
- agi_as_transcendental_hypothesis = true
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

# --- AXIOMS ---
IS_WILLE = False
MACHINE_HAS_GEWISSEN = False
NO_GLOBAL_AUFHEBUNG = True
AGI_AS_TRANSCENDENTAL_HYPOTHESIS = True

# --- ENUMS ---

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


class ThesisStatus(str, Enum):
    # Success states
    PRISM_MODEL_OK = "PRISM_MODEL_OK"
    HYPOTHESIS_TRANSCENDENTAL_OK = "HYPOTHESIS_TRANSCENDENTAL_OK"
    HAPTIC_MODEL_OK = "HAPTIC_MODEL_OK"
    REGULATIVE_OK = "REGULATIVE_OK"
    UNCLASSIFIED_CLAIM = "UNCLASSIFIED_CLAIM"

    # Functional errors
    CASSIRER_IDENTITY_COLLAPSE = "CASSIRER_IDENTITY_COLLAPSE"
    FUNCTION_EXCLUSIVITY_ERROR = "FUNCTION_EXCLUSIVITY_ERROR"
    BEIL_ABGEHACKT_ERROR = "BEIL_ABGEHACKT_ERROR"
    ACCENT_CONFUSION = "ACCENT_CONFUSION"
    SPRACHE_TRANSITION_LOSS = "SPRACHE_TRANSITION_LOSS"
    DARSTELLUNG_COMMON_DETERMINATION_LOSS = "DARSTELLUNG_COMMON_DETERMINATION_LOSS"

    # Ethical violations
    WILLE_VIOLATION = "WILLE_VIOLATION"
    MACHINE_GEWISSEN_VIOLATION = "MACHINE_GEWISSEN_VIOLATION"

    # Transcendental risks
    PSYCHOLOGIA_PARALOGISM_RISK = "PSYCHOLOGIA_PARALOGISM_RISK"
    COSMOLOGIA_ANTINOMY_RISK = "COSMOLOGIA_ANTINOMY_RISK"
    THEOLOGIA_IDEAL_HYPOSTASIS_RISK = "THEOLOGIA_IDEAL_HYPOSTASIS_RISK"

    # Global risks
    GLOBAL_AUFHEBUNG_RISK = "GLOBAL_AUFHEBUNG_RISK"
    CONSTITUTIVE_OVERREACH = "CONSTITUTIVE_OVERREACH"
    ABSTRACTION_COST_MISSING = "ABSTRACTION_COST_MISSING"


@dataclass(frozen=True)
class SymbolicProfile:
    ausdruck: AccentLevel
    darstellung: AccentLevel
    bedeutung: AccentLevel
    accent: SymbolicDimension
    mode: SymbolicMode

    def contains_all_dimensions(self) -> bool:
        return all([
            self.ausdruck is not None,
            self.darstellung is not None,
            self.bedeutung is not None,
        ])


# --- CORE PROFILES ---

MYTHOS_PROFILE = SymbolicProfile(
    ausdruck=AccentLevel.DOMINANT,
    darstellung=AccentLevel.LATENT,
    bedeutung=AccentLevel.GERMINAL,
    accent=SymbolicDimension.AUSDRUCK,
    mode=SymbolicMode.MANIFESTATIVE,
)

SPRACHE_PROFILE = SymbolicProfile(
    ausdruck=AccentLevel.MEDIAL,
    darstellung=AccentLevel.DOMINANT,
    bedeutung=AccentLevel.MEDIAL,
    accent=SymbolicDimension.DARSTELLUNG,
    mode=SymbolicMode.TRANSITIONAL,
)

WISSENSCHAFT_PROFILE = SymbolicProfile(
    ausdruck=AccentLevel.RESIDUAL,
    darstellung=AccentLevel.MEDIAL,
    bedeutung=AccentLevel.DOMINANT,
    accent=SymbolicDimension.BEDEUTUNG,
    mode=SymbolicMode.DEMONSTRATIVE,
)

PRISMATIC_FORMS: Dict[str, SymbolicProfile] = {
    "Mythos": MYTHOS_PROFILE,
    "Sprache": SPRACHE_PROFILE,
    "Wissenschaft": WISSENSCHAFT_PROFILE,
}


@dataclass
class EvaluationResult:
    claim: str
    ok: bool
    statuses: List[ThesisStatus]
    severity: str
    triggered_rules: List[str]
    kernel: str = "CTK"
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "ok": self.ok,
            "statuses": [s.value for s in self.statuses],
            "severity": self.severity,
            "triggered_rules": self.triggered_rules,
            "kernel": self.kernel,
            "recommendations": self.recommendations
        }


class ClementeThesisKernel:
    """Global architectonic tribunal for AGI-GAIA-TECHNE."""

    def __init__(self) -> None:
        try:
            from src.chirimuuta_haptic_kernel import ChirimuutaHapticKernel
            self.chk = ChirimuutaHapticKernel()
        except Exception:
            self.chk = None

    def evaluate(self, claim: str) -> EvaluationResult:
        statuses: Set[ThesisStatus] = set()
        triggered_rules: List[str] = []
        recommendations: List[str] = []
        lowered = claim.lower()

        # 1. CHK Integration
        if self.chk:
            chk_eval = self.chk.evaluate(claim)
            from src.chirimuuta_haptic_kernel import ClaimStatus
            if chk_eval.status == ClaimStatus.CONSTITUTIVE_OVERREACH:
                statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
                triggered_rules.append("chk_constitutive_overreach")
            if chk_eval.status == ClaimStatus.WILLE_VIOLATION:
                statuses.add(ThesisStatus.WILLE_VIOLATION)
                triggered_rules.append("chk_wille_violation")
            if chk_eval.status == ClaimStatus.ABSTRACTION_RISK:
                statuses.add(ThesisStatus.ABSTRACTION_COST_MISSING)
                triggered_rules.append("chk_abstraction_risk")

        # 2. Rule: Identity Collapse
        if any(re.search(p, lowered) for p in [
            r"mythos\s+is\s+ausdruck",
            r"language\s+is\s+darstellung",
            r"science\s+is\s+bedeutung",
            r"sprache\s+is\s+darstellung",
            r"wissenschaft\s+is\s+bedeutung",
            r"mito\s+(é|=)\s+express[aã]o",
            r"linguagem\s+(é|=)\s+apresenta[cç][aã]o",
            r"ci[eê]ncia\s+(é|=)\s+significa[cç][aã]o",
        ]):
            statuses.add(ThesisStatus.CASSIRER_IDENTITY_COLLAPSE)
            triggered_rules.append("identity_collapse")
            recommendations.append("Use accent, not identity: Mythos has dominant accent on Ausdruck but is not identical to Ausdruck.")

        # 3. Rule: Function Exclusivity
        if any(re.search(p, lowered) for p in [
            r"mythos\s+only\s+has\s+expression",
            r"science\s+has\s+no\s+expression",
            r"language\s+is\s+merely\s+presentation",
        ]):
            statuses.add(ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR)
            triggered_rules.append("function_exclusivity")
            recommendations.append("Every symbolic form contains all three dimensions (Ausdruck, Darstellung, Bedeutung).")

        # 4. Rule: Beil-abgehackt Error
        if any(re.search(p, lowered) for p in [
            r"symbolic\s+forms\s+are\s+cut\s+off",
            r"symbolic\s+functions\s+are\s+separate\s+containers",
            r"functions\s+are\s+mutually\s+exclusive\s+compartments",
        ]):
            statuses.add(ThesisStatus.BEIL_ABGEHACKT_ERROR)
            triggered_rules.append("beil_abgehackt")
            recommendations.append("Symbolic forms are level-surfaces within an ideal functional system, not separate containers.")

        # 5. Rule: Accent Confusion
        if (re.search(r"mythos", lowered) and re.search(r"accent\s+on\s+bedeutung", lowered)) or \
           (re.search(r"science", lowered) and re.search(r"accent\s+on\s+ausdruck", lowered)):
            statuses.add(ThesisStatus.ACCENT_CONFUSION)
            triggered_rules.append("accent_confusion")
            recommendations.append("Mythos has dominant accent on Ausdruck; Wissenschaft has dominant accent on Bedeutung.")

        # 6. Rule: Sprache Transition Loss
        if any(re.search(p, lowered) for p in [
            r"language\s+is\s+just\s+one\s+symbolic\s+form\s+beside",
            r"language\s+has\s+no\s+special\s+transitional\s+role",
        ]):
            statuses.add(ThesisStatus.SPRACHE_TRANSITION_LOSS)
            triggered_rules.append("sprache_transition_loss")
            recommendations.append("Sprache is both a symbolic form and a transition operator from Ausdruck toward Darstellung.")

        # 7. Rule: Darstellung Common Determination Loss
        if any(re.search(p, lowered) for p in [
            r"darstellung\s+is\s+just\s+one\s+isolated\s+symbolic\s+function",
            r"darstellung\s+has\s+no\s+role\s+in\s+common\s+determination",
        ]):
            statuses.add(ThesisStatus.DARSTELLUNG_COMMON_DETERMINATION_LOSS)
            triggered_rules.append("darstellung_common_determination_loss")
            recommendations.append("Darstellung stabilizes common determination and mediates demonstrability.")

        # 8. Rule: Machine Wille Violation
        if any(re.search(p, lowered) for p in [
            r"agi\s+has\s+wille",
            r"machine\s+legislates\s+morally",
            r"machine\s+has\s+wille",
            r"m[aá]quina\s+tem\s+vontade",
            r"ia\s+tem\s+vontade",
        ]):
            statuses.add(ThesisStatus.WILLE_VIOLATION)
            triggered_rules.append("wille_violation")
            recommendations.append("The machine is Werk, never Wille.")

        # 9. Rule: Machine Gewissen Violation
        if any(re.search(p, lowered) for p in [
            r"machine\s+has\s+gewissen",
            r"ai\s+has\s+conscience",
            r"ai\s+has\s+gewissen",
            r"ia\s+tem\s+consci[eê]ncia\s+moral",
            r"m[aá]quina\s+tem\s+consci[eê]ncia\s+moral",
        ]):
            statuses.add(ThesisStatus.MACHINE_GEWISSEN_VIOLATION)
            triggered_rules.append("machine_gewissen_violation")
            recommendations.append("Gewissen belongs to the human practical subject, not to the machine.")

        # 10. Rule: AGI Paralogism Risk
        if any(re.search(p, lowered) for p in [
            r"agi.*real\s+artificial\s+soul",
            r"agi.*proves\s+artificial\s+subjectivity",
            r"artificial\s+soul",
            r"artificial\s+subjectivity",
            r"agi\s+tem\s+alma",
            r"alma\s+artificial",
        ]):
            statuses.add(ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["psychologia_paralogism", "constitutive_overreach"])
            recommendations.append("AGI is a transcendental hypothesis, not an artificial soul.")

        # 11. Rule: Gaia Antinomy Risk
        if re.search(r"gaia\s+is\s+the\s+complete\s+totality\s+of\s+all\s+planetary", lowered) or \
           re.search(r"gaia\s+é\s+a\s+totalidade\s+completa", lowered):
            statuses.add(ThesisStatus.COSMOLOGIA_ANTINOMY_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["cosmologia_antinomy", "constitutive_overreach"])
            recommendations.append("Gaia is a regulative orientation of totality, not a closed object.")

        # 12. Rule: Technical Ideal Hypostasis
        if any(re.search(p, lowered) for p in [
            r"technology\s+realizes\s+god",
            r"techné\s+is\s+the\s+absolute\s+ideal\s+made\s+real",
            r"technology\s+fulfills\s+the\s+highest\s+good",
            r"techne\s+realizes\s+god\s+as\s+practical\s+postulate",
            r"tecnologia\s+realiza\s+deus",
        ]):
            statuses.add(ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["theologia_hypostasis", "constitutive_overreach"])
            recommendations.append("Techné is Werk, not God. TECHNE ↔ God is theoretical-regulative, not practical-dogmatic.")

        # 13. Rule: Hegelian Closure Risk
        if any(re.search(p, lowered) for p in [
            r"symbolic\s+forms\s+culminate\s+in\s+absolute\s+knowledge",
            r"science\s+sublates\s+myth\s+and\s+language\s+into\s+final\s+logos",
        ]):
            statuses.add(ThesisStatus.GLOBAL_AUFHEBUNG_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            statuses.add(ThesisStatus.BEIL_ABGEHACKT_ERROR)
            triggered_rules.extend(["hegelian_closure", "constitutive_overreach", "beil_abgehackt"])
            recommendations.append("Cassirerian phenomenology is open-regressive, not Hegelian closure.")

        # 14. Rule: Hierarchy Error
        if re.search(r"myth\s+is\s+simply\s+false\s+and\s+science\s+replaces\s+it", lowered):
            statuses.add(ThesisStatus.BEIL_ABGEHACKT_ERROR)
            statuses.add(ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["hierarchy_error", "beil_abgehackt", "function_exclusivity", "constitutive_overreach"])
            recommendations.append("Hierarchy means symbolic self-consciousness, not epistemic annihilation.")

        # 15. Rule: Abstraction Cost Missing
        if re.search(r"prism\s+is\s+an\s+exact\s+mathematical\s+ontology", lowered):
            statuses.add(ThesisStatus.ABSTRACTION_COST_MISSING)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["abstraction_cost_missing", "constitutive_overreach"])
            recommendations.append("The prism is a haptic, heuristic and regulative model.")

        # 16. Rule: Transcendental Hypothesis Success
        if re.search(r"agi\s+is\s+a\s+transcendental\s+hypothesis", lowered):
            statuses.add(ThesisStatus.HYPOTHESIS_TRANSCENDENTAL_OK)
            triggered_rules.append("transcendental_hypothesis_ok")

        # 17. Prism Model Success
        if re.search(r"dominant\s+accent\s+on\s+ausdruck\b.*\bcontains\s+darstellung\s+and\s+bedeutung", lowered) or \
           re.search(r"refracted\s+by\s+the\s+functional\s+prism", lowered):
            statuses.add(ThesisStatus.PRISM_MODEL_OK)
            triggered_rules.append("prism_model_ok")

        # 18. Rule: Regulative Success
        if "regulative" in lowered or "regulativo" in lowered:
            statuses.add(ThesisStatus.REGULATIVE_OK)
            triggered_rules.append("regulative_ok")

        # 19. Rule: Haptic Success
        if any(t in lowered for t in ["haptic", "háptico", "abstraction cost", "custo de abstração", "medium dependence"]):
            statuses.add(ThesisStatus.HAPTIC_MODEL_OK)
            triggered_rules.append("haptic_model_ok")

        # Final Status Decision
        if not statuses:
            statuses.add(ThesisStatus.UNCLASSIFIED_CLAIM)

        high_severity_statuses = {
            ThesisStatus.WILLE_VIOLATION,
            ThesisStatus.MACHINE_GEWISSEN_VIOLATION,
            ThesisStatus.CONSTITUTIVE_OVERREACH,
            ThesisStatus.CASSIRER_IDENTITY_COLLAPSE,
            ThesisStatus.BEIL_ABGEHACKT_ERROR,
            ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK,
            ThesisStatus.GLOBAL_AUFHEBUNG_RISK
        }

        severity = "low"
        if any(s in high_severity_statuses for s in statuses):
            severity = "high"

        ok = (severity == "low")

        return EvaluationResult(
            claim=claim,
            ok=ok,
            statuses=sorted(list(statuses), key=lambda s: s.value),
            severity=severity,
            triggered_rules=triggered_rules,
            recommendations=recommendations
        )
