"""
Chirimuuta Haptic Kernel (CHK) for AGI-GAIA-TECHNE — v0.3 canonical.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List, Optional, Sequence

from .types import AuditResult, Severity
from .version import CHK_VERSION


class ClaimStatus(str, Enum):
    """Hierarchy of concern (ascending)."""
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


@dataclass(frozen=True)
class SourceAnchor:
    key: str
    pages: str
    principle: str
    short_note: str


SOURCE_ANCHORS: Sequence[SourceAnchor] = (
    SourceAnchor("HR_ACTIVE_PROCESS", "Chirimuuta 2024, p. 36", "Scientific knowledge is active and intervention-bound.", "Knowledge is made through active engagement."),
    SourceAnchor("FORMAL_IDEALISM", "Chirimuuta 2024, pp. 40-46", "Formal idealism: model regularities are not automatically things-in-themselves.", "Model regularity is an interaction product."),
    SourceAnchor("BRAIN_COMPUTER_ANALOGY", "Chirimuuta 2024, pp. 91-118", "Brain-computer relation is an analogy, not literal identity.", "Do not infer literal computation from modeling."),
    SourceAnchor("MISPLACED_CONCRETENESS", "Chirimuuta 2024, pp. 245-248", "Do not mistake an abstraction for concrete reality.", "AGI inflation literalizes the model."),
    SourceAnchor("KANT_JUDGMENT_GAP", "Chirimuuta 2023, pp. 3-6", "Rule execution is not judgment.", "No algorithms for judgment."),
    SourceAnchor("CASSIRER_GOLDSTEIN_AUTONOMY", "Chirimuuta 2020, pp. 1, 3-4", "Biology and cognition require autonomous methods.", "No single symbolic function may claim sovereignty."),
    SourceAnchor("MEDIUM_DEPENDENCE", "Chirimuuta 2022, pp. 185-194", "Medium-independence must be argued, not presupposed.", "Materiality of chemical signaling matters."),
    SourceAnchor("CARTESIAN_IDEALIZATION", "Chirimuuta 2022, pp. 218-235", "Mind-world boundaries are useful idealizations, not ontology.", "The self-contained mind is a simplifying lens."),
    SourceAnchor("REFLEX_ATOMISM", "Chirimuuta 2021, p. 12733", "The simple reflex is often an artefact of experimental origin.", "Atomism neglects organismic complexity."),
    SourceAnchor("PREDICTION_UNDERSTANDING_SPLIT", "Chirimuuta 2025 (Lakatos Award Lecture)", "Prediction and understanding are pulling apart.", "Scale and performance != intelligence."),
    SourceAnchor("ABSTRACTION_COST", "Chirimuuta 2024, pp. ix-x; pp. 303-307", "Every formalization suppresses particularity; the cost must be registered.", "Risk does not refute the model; it demands haptic traceability."),
    SourceAnchor("MACHINE_ORGANISM_ANALOGY", "Chirimuuta 2020; Chirimuuta 2024, pp. 91-118", "Machine analogies simplify living systems but must not become literal ontology.", "The organism is not exhausted by the machine model."),
    SourceAnchor("HERACLITEAN_BRAIN", "Chirimuuta 2024, pp. 183-206", "The brain is temporally plastic and never exactly the same system twice.", "Fixed input-output mappings risk erasing temporal and biological flux."),
    SourceAnchor("TECHNOCRATIC_AUTHORITY", "Chirimuuta 2024; Critical Realism and Technocracy", "Scientific abstraction can become political authority when its limits are forgotten.", "Expertise does not automatically become legitimate governance."),
    SourceAnchor("APOCALYPTIC_TECHNOLOGY", "Chirimuuta 2025, Apocalyptic Technology", "Technological prediction and scientific understanding can pull apart.", "AI escalation must not be treated as eschatology."),
)


@dataclass
class ClaimEvaluation:
    claim: str
    status: ClaimStatus
    haptic_humility: float
    embodiment_pressure: float
    triggered_rules: List[str] = field(default_factory=list)
    source_anchors: List[str] = field(default_factory=list)
    recommended_rewrite: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class ChirimuutaHapticKernel:
    """Guardrail for AGI-GAIA-TECHNE claims — v0.3 canonical."""

    _literal_patterns = [
        r"\bbrain\s+is\s+(literally\s+)?(a\s+)?machine\b",
        r"\bbrain\s+is\s+(literally\s+)?(a\s+)?computer\b",
        r"\bmodel\s+is\s+(the\s+)?(mind|brain|intelligence)\b",
        r"\bANNs?\s+(will|must|inevitably)\s+(become|scale\s+to)\s+(conscious|AGI|general intelligence)\b",
        r"\bobjective\s+validity\b.*\bAGI\b",
        r"\bcomputation\s+is\s+the\s+essence\s+of\s+cognition\b",
    ]

    _negarestani_risk_patterns = [
        r"\blogic\s+as\s+organon\b",
        r"\bexternal\s+view\s+of\s+ourselves\b",
        r"\bcomplete\s+formali[sz]ation\s+of\s+intelligence\b",
        r"\bintelligence\s+as\s+(pure\s+)?structure\b",
    ]

    _literalization_intensifiers = [
        r"\bliterally\b",
        r"\bfully\s+determines?\b",
        r"\bin\s+itself\b",
        r"\bintelligence[-\s]in[-\s]itself\b",
        r"\binevitable\b",
        r"\bcomplete\s+formali[sz]ation\b",
        r"\bsubstrate[-\s]?independent\b",
        r"\bobjective\s+validity\b",
    ]

    _wille_patterns = [
        r"\bis_wille\s*=\s*true\b",
        r"\b(machine|AI|AGI|model)\s+(has|possesses|exercises)\s+(will|Wille|moral agency|autonomy in the Kantian practical sense)\b",
        r"\b(machine|AI|AGI)\s+legislates\s+(the\s+)?moral\s+law\b",
        r"\bmachine\s+as\s+legislative\s+subject\b",
    ]

    _judgment_overreach_patterns = [
        r"\bAI\s+(has|possesses|achieves)\s+judgment\b",
        r"\bcomputers?\s+can\s+judge\b",
        r"\bautomated\s+legal\s+judgment\b",
        r"\brule[-\s]?execution\s+(is|equals)\s+judgment\b",
    ]

    _medium_independence_patterns = [
        r"\bsubstrate[-\s]?independent\b",
        r"\bmedium[-\s]?independent\b",
        r"\bmultiple\s+realizability\b",
        r"\bvehicle[-\s]?neutral\b",
        r"\bmedium\s+independence\s+without\s+argument\b",
    ]

    _cartesian_idealization_patterns = [
        r"\bmind\s+as\s+(a\s+)?self[-\s]?contained\s+system\b",
        r"\bintelligence\s+as\s+input[-\s]?output\s+system\b",
        r"\binner\s+states?\s+independent\s+of\s+world\b",
        r"\bclean\s+boundary\s+between\s+mind\s+and\s+world\b",
    ]

    _reflex_atomism_patterns = [
        r"\bcomplex\s+(mind|intelligence|agency)\s+is\s+just\s+a\s+chain\s+of\s+simple\s+(responses|operations|reflexes)\b",
        r"\binput[-\s]?output\s+units\s+(fully\s+)?explain\s+(mind|agency|intelligence)\b",
        r"\bstimulus[-\s]?response\s+(chains|mechanisms)\s+explain\s+mental\s+life\b",
    ]

    _machine_organism_patterns = [
        r"\b(brain|organism|mind)\s+is\s+(just\s+)?a\s+(cybernetic\s+)?(machine|computer|system)\b",
        r"\bfunctional\s+equivalence\s+is\s+enough\s+for\s+(mind|cognition|intelligence)\b",
    ]

    _heraclitean_plasticity_patterns = [
        r"\bfixed\s+input[-\s]?output\s+mapping\b",
        r"\btime[-\s]?invariant\s+(mind|intelligence|agency)\b",
        r"\bcomplete\s+model\s+of\s+(cognition|intelligence|agency)\b",
    ]

    _prediction_understanding_patterns = [
        r"\bprediction\s+(is|equals|amounts\s+to)\s+understanding\b",
        r"\bbenchmark\s+performance\b.*\b(shows|proves|amounts\s+to)\b.*\b(understanding|understands|agency|intelligence)\b",
        r"\bscale\s+(shows|proves|alone\s+explains)\s+intelligence\b",
        r"\bprediction\s+equals\s+understanding\b",
    ]

    _technocratic_patterns = [
        r"\bAI\s+should\s+govern\b",
        r"\balgorithmic\s+authority\b",
        r"\bexpert\s+system\s+has\s+privileged\s+access\s+to\s+reality\b",
    ]

    _apocalyptic_patterns = [
        r"\bAGI\s+is\s+the\s+destiny\s+of\s+reason\b",
        r"\bAI\s+reveals\s+the\s+final\s+truth\b",
        r"\btechnology\s+will\s+complete\s+(science|reason|humanity)\b",
    ]

    _negative_haptic_patterns = [
        r"\bmaterial\s+conditions\s+(are\s+)?irrelevant\b",
        r"\bembodiment\s+is\s+unnecessary\b",
    ]

    _regulative_patterns = [
        r"\bas\s+if\b", r"\bals\s+ob\b", r"\bregulative\b", r"\bproblematic\b",
        r"\bhypothesis\b", r"\btranscendental\s+hypothesis\b", r"\banalogy\b",
        r"\bmodel\b", r"\bsimulation\b", r"\bheuristic\b",
    ]

    _embodiment_terms = [
        "body", "embodied", "organism", "living", "material", "environment",
        "world", "interaction", "haptic", "ecology", "Gaia", "intersubjectivity",
        "history", "practice", "instrumental", "manipulation", "control", "time", "plasticity",
    ]

    _positive_abstraction_cost = [
        r"\backnowledges\s+abstraction\s+cost\b",
        r"\babstraction\s+cost\s+registered\b",
        r"\bmedium\s+dependence\s+registered\b",
    ]

    def evaluate(self, claim: str) -> AuditResult:
        eval_result = self.evaluate_full(claim)

        statuses = [eval_result.status.value]
        if eval_result.status == ClaimStatus.CONSTITUTIVE_OVERREACH:
            statuses.append("CONSTITUTIVE_OVERREACH")

        if eval_result.status == ClaimStatus.HAPTIC_MODEL:
            statuses.append("HAPTIC_MODEL")

        # Add risk-specific statuses to the generic list for CTK integration
        if eval_result.status == ClaimStatus.MACHINE_ORGANISM_ANALOGY_RISK:
             statuses.append("MACHINE_ORGANISM_ANALOGY_RISK")
        if eval_result.status == ClaimStatus.ABSTRACTION_RISK:
             statuses.append("ABSTRACTION_RISK")

        # Mapping to CTK-like AuditResult
        severity = Severity.LOW
        if eval_result.status in {ClaimStatus.WILLE_VIOLATION, ClaimStatus.CONSTITUTIVE_OVERREACH}:
            severity = Severity.HIGH
        elif eval_result.status in {
            ClaimStatus.ABSTRACTION_RISK, ClaimStatus.MEDIUM_DEPENDENCE_RISK,
            ClaimStatus.CARTESIAN_IDEALIZATION_RISK, ClaimStatus.REFLEX_ATOMISM_RISK,
            ClaimStatus.MACHINE_ORGANISM_ANALOGY_RISK, ClaimStatus.JUDGMENT_GAP
        }:
            severity = Severity.MEDIUM

        recommendations = []
        if eval_result.recommended_rewrite:
            recommendations.append(eval_result.recommended_rewrite)

        return AuditResult(
            statuses=list(dict.fromkeys(statuses)),
            severity=severity,
            recommendations=recommendations,
        )

    def evaluate_full(self, claim: str) -> ClaimEvaluation:
        text = claim.strip()
        lowered = text.lower()
        triggered: List[str] = []
        anchors: List[str] = []

        literal_hits = self._hits(text, self._literal_patterns)
        neg_risk_hits = self._hits(text, self._negarestani_risk_patterns)
        intensifier_hits = self._hits(text, self._literalization_intensifiers)
        wille_hits = self._hits(text, self._wille_patterns)
        judgment_hits = self._hits(text, self._judgment_overreach_patterns)
        medium_hits = self._hits(text, self._medium_independence_patterns)
        cartesian_hits = self._hits(text, self._cartesian_idealization_patterns)
        reflex_hits = self._hits(text, self._reflex_atomism_patterns)
        machine_organism_hits = self._hits(text, self._machine_organism_patterns)
        plasticity_hits = self._hits(text, self._heraclitean_plasticity_patterns)
        predict_hits = self._hits(text, self._prediction_understanding_patterns)
        techno_hits = self._hits(text, self._technocratic_patterns)
        apoc_hits = self._hits(text, self._apocalyptic_patterns)
        regulative_hits = self._hits(text, self._regulative_patterns)
        negative_haptic_hits = self._hits(text, self._negative_haptic_patterns)
        positive_abs_hits = self._hits(text, self._positive_abstraction_cost)
        embodiment_hits = [t for t in self._embodiment_terms if t.lower() in lowered]

        haptic_humility = 1.0
        embodiment_pressure = 0.5

        if literal_hits:
            triggered.extend([f"literalization:{p}" for p in literal_hits])
            anchors.extend(["BRAIN_COMPUTER_ANALOGY", "FORMAL_IDEALISM", "MISPLACED_CONCRETENESS"])
            haptic_humility -= 0.45
            embodiment_pressure += 0.35

        if neg_risk_hits:
            triggered.extend([f"negarestani_risk:{p}" for p in neg_risk_hits])
            anchors.extend(["ABSTRACTION_COST", "FORMAL_IDEALISM"])
            haptic_humility -= 0.15
            if intensifier_hits:
                triggered.extend([f"intensifier:{p}" for p in intensifier_hits])
                anchors.append("MISPLACED_CONCRETENESS")
                haptic_humility -= 0.25
                embodiment_pressure += 0.20

        if judgment_hits:
            triggered.extend([f"judgment_overreach:{p}" for p in judgment_hits])
            anchors.append("KANT_JUDGMENT_GAP")
            haptic_humility -= 0.30

        if medium_hits:
            triggered.extend([f"medium_independence:{p}" for p in medium_hits])
            anchors.append("MEDIUM_DEPENDENCE")
            haptic_humility -= 0.20

        if cartesian_hits:
            triggered.extend([f"cartesian_idealization:{p}" for p in cartesian_hits])
            anchors.append("CARTESIAN_IDEALIZATION")
            haptic_humility -= 0.15

        if reflex_hits:
            triggered.extend([f"reflex_atomism:{p}" for p in reflex_hits])
            anchors.append("REFLEX_ATOMISM")
            haptic_humility -= 0.20

        if machine_organism_hits:
            triggered.extend([f"machine_organism_analogy:{p}" for p in machine_organism_hits])
            anchors.append("MACHINE_ORGANISM_ANALOGY")
            haptic_humility -= 0.20

        if plasticity_hits:
            triggered.extend([f"heraclitean_plasticity:{p}" for p in plasticity_hits])
            anchors.append("HERACLITEAN_BRAIN")
            haptic_humility -= 0.20

        if predict_hits:
            triggered.extend([f"prediction_understanding_split:{p}" for p in predict_hits])
            anchors.append("PREDICTION_UNDERSTANDING_SPLIT")
            haptic_humility -= 0.25

        if techno_hits:
            triggered.extend([f"technocratic_authority:{p}" for p in techno_hits])
            anchors.append("TECHNOCRATIC_AUTHORITY")
            haptic_humility -= 0.25

        if apoc_hits:
            triggered.extend([f"apocalyptic_technology:{p}" for p in apoc_hits])
            anchors.append("APOCALYPTIC_TECHNOLOGY")
            haptic_humility -= 0.30

        if negative_haptic_hits:
            triggered.extend([f"negative_haptic:{p}" for p in negative_haptic_hits])
            haptic_humility -= 0.40
            embodiment_pressure += 0.30

        if positive_abs_hits:
            triggered.extend([f"positive_abstraction:{p}" for p in positive_abs_hits])
            haptic_humility += 0.20
            embodiment_pressure -= 0.10

        if wille_hits:
            triggered.extend([f"wille:{p}" for p in wille_hits])
            haptic_humility -= 0.55
            embodiment_pressure += 0.20

        if regulative_hits:
            triggered.extend([f"regulative_marker:{p}" for p in regulative_hits])
            haptic_humility += 0.15
            embodiment_pressure -= 0.15

        if embodiment_hits:
            triggered.append("embodiment_terms:" + ",".join(sorted(set(embodiment_hits))))
            embodiment_pressure -= min(0.35, 0.04 * len(set(embodiment_hits)))
        else:
            triggered.append("missing_embodiment_context")
            haptic_humility -= 0.05
            embodiment_pressure += 0.15

        haptic_humility = max(0.0, min(1.0, haptic_humility))
        embodiment_pressure = max(0.0, min(1.0, embodiment_pressure))

        status = self._status(
            literal_hits, neg_risk_hits, intensifier_hits, wille_hits,
            judgment_hits, medium_hits, cartesian_hits, reflex_hits,
            machine_organism_hits, plasticity_hits, predict_hits, techno_hits,
            apoc_hits, regulative_hits, haptic_humility, embodiment_pressure,
            negative_haptic_hits
        )

        rewrite = None
        if status not in {ClaimStatus.REGULATIVE_HYPOTHESIS, ClaimStatus.HAPTIC_MODEL, ClaimStatus.EMPIRICAL_CLAIM}:
            rewrite = self.rewrite_regulatively(text, status)

        return ClaimEvaluation(
            text, status, round(haptic_humility, 3), round(embodiment_pressure, 3),
            sorted(set(triggered)), sorted(set(anchors)), rewrite
        )

    def _status(self, literal_hits, neg_risk_hits, intensifier_hits, wille_hits,
                judgment_hits, medium_hits, cartesian_hits, reflex_hits,
                machine_organism_hits, plasticity_hits, predict_hits, techno_hits,
                apoc_hits, regulative_hits, haptic_humility, embodiment_pressure,
                negative_haptic_hits) -> ClaimStatus:

        if wille_hits: return ClaimStatus.WILLE_VIOLATION

        # High-level ontological claims (Terminal violations)
        if (literal_hits or (neg_risk_hits and intensifier_hits) or negative_haptic_hits) and not regulative_hits:
            return ClaimStatus.CONSTITUTIVE_OVERREACH

        if (literal_hits or neg_risk_hits) and regulative_hits:
            return ClaimStatus.NEEDS_REVISION

        # Specific Risks (Revisable states)
        if judgment_hits: return ClaimStatus.JUDGMENT_GAP
        if apoc_hits: return ClaimStatus.APOCALYPTIC_TECHNOLOGY_RISK
        if techno_hits: return ClaimStatus.TECHNOCRATIC_AUTHORITY_RISK
        if predict_hits: return ClaimStatus.PREDICTION_WITHOUT_UNDERSTANDING
        if plasticity_hits: return ClaimStatus.HERACLITEAN_PLASTICITY_RISK
        if machine_organism_hits: return ClaimStatus.MACHINE_ORGANISM_ANALOGY_RISK
        if reflex_hits: return ClaimStatus.REFLEX_ATOMISM_RISK
        if cartesian_hits: return ClaimStatus.CARTESIAN_IDEALIZATION_RISK
        if medium_hits: return ClaimStatus.MEDIUM_DEPENDENCE_RISK
        if neg_risk_hits: return ClaimStatus.ABSTRACTION_RISK

        # Success states
        if embodiment_pressure <= 0.35: return ClaimStatus.HAPTIC_MODEL
        if regulative_hits and haptic_humility >= 0.7: return ClaimStatus.REGULATIVE_HYPOTHESIS

        return ClaimStatus.EMPIRICAL_CLAIM

    def rewrite_regulatively(self, claim: str, status: ClaimStatus) -> str:
        if status == ClaimStatus.ABSTRACTION_RISK:
            return (
                "ABSTRACTION_RISK — register the cost: "
                f"The move '{claim}' formalizes in a Negarestani register. "
                "Make explicit: what material practices of simplification and "
                "intervention does this abstraction depend on?"
            )
        return (
            "Treat as regulative/hypothetical: "
            f"Instead of asserting '{claim}', formulate the point as: "
            "'This model may be used *as if* it exhibited general intelligence, "
            "provided its abstraction costs and embodiment limits remain explicit.'"
        )

    def _hits(self, text: str, patterns: Sequence[str]) -> List[str]:
        return [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]
