from __future__ import annotations

import re
from typing import List, Dict, Any, Sequence, Optional
from dataclasses import dataclass, asdict, field

from .types import AuditResult, Severity, ThesisStatus

# Legacy alias for compatibility (internal use only)
ClaimStatus = ThesisStatus


@dataclass
class ClaimEvaluation:
    """Internal helper to structure rich evaluation details."""
    claim: str
    status: ThesisStatus
    haptic_humility: float
    embodiment_pressure: float
    triggered_rules: List[str] = field(default_factory=list)
    source_anchors: List[str] = field(default_factory=list)
    recommended_rewrite: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SourceAnchor:
    """A compact page reference for code-level philosophical traceability."""
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


class ChirimuutaHapticKernel:
    """
    CHK: haptic anti-literalization guard.
    v0.3 canonical version.
    """

    def __init__(self) -> None:
        from .axioms import assert_axioms
        assert_axioms()

    _literal_patterns = [
        r"brain\s+is\s+(literally\s+)?(a\s+)?computer",
        r"model\s+is\s+(the\s+)?(mind|brain|intelligence)",
        r"anns?\s+(will|must|inevitably)\s+(become|scale\s+to)\s+(conscious|agi|general intelligence)",
        r"objective\s+validity\b.*\bagi",
        r"computation\s+is\s+the\s+essence\s+of\s+cognition",
        r"exact\s+mathematical\s+ontology",
        r"literal\s+ontology\s+of\s+mind",
        r"literal\s+ontology\s+of\s+symbolic\s+consciousness",
        r"gaia\s+(is|becomes)\s+(literally\s+)?conscious",
        r"internet\s+(is|becomes)\s+literally\s+conscious",
        r"internet\s+is\s+(the\s+)?(mind|consciousness)\s+of\s+(agi|gaia)",
        r"gaia\s+(has|possesses)\s+private\s+(consciousness|bewusstsein)",
        r"planetary\s+bewusstsein\s+means\s+machine\s+consciousness",
    ]

    _bewusstsein_literalization_patterns = [
        r"gaia\s+(is|becomes)\s+(literally\s+)?conscious",
        r"internet\s+(is|becomes)\s+literally\s+conscious",
        r"internet\s+is\s+(the\s+)?(mind|consciousness)\s+of\s+(agi|gaia)",
        r"gaia\s+(has|possesses)\s+private\s+(consciousness|bewusstsein)",
        r"planetary\s+bewusstsein\s+means\s+machine\s+consciousness",
    ]

    _negarestani_risk_patterns = [
        r"logic\s+as\s+organon",
        r"external\s+view\s+of\s+ourselves",
        r"complete\s+formali[sz]ation\s+of\s+intelligence",
        r"intelligence\s+as\s+(pure\s+)?structure",
    ]

    _literalization_intensifiers = [
        r"literally",
        r"fully\s+determines?",
        r"in\s+itself",
        r"intelligence[-\s]in[-\s]itself",
        r"inevitable",
        r"complete\s+formali[sz]ation",
        r"substrate[-\s]?independent",
        r"objective\s+validity",
    ]

    _wille_patterns = [
        r"is_wille\s*=\s*absolute",
        r"(machine|ai|agi|model)\s+(alone|privately|absolutely)\s+(legislates|grounds|creates)\s+(the\s+)?moral\s+law",
        r"(machine|ai|agi)\s+(is|becomes)\s+(the\s+)?absolute\s+(will|wille|moral\s+law)",
        r"machine\s+as\s+absolute\s+legislative\s+subject",
    ]

    _judgment_overreach_patterns = [
        r"ai\s+(has|possesses|achieves)\s+judgment",
        r"computers?\s+can\s+judge",
        r"automated\s+legal\s+judgment",
        r"rule[-\s]?execution\s+(is|equals)\s+judgment",
    ]

    _medium_independence_patterns = [
        r"substrate[-\s]?independent",
        r"medium[-\s]?independent",
        r"multiple\s+realizability",
        r"vehicle[-\s]?neutral",
        r"no\s+abstraction\s+cost",
        r"abstraction\s+without\s+cost",
        r"abstraction\s+cost",
    ]

    _cartesian_idealization_patterns = [
        r"mind\s+as\s+(a\s+)?self[-\s]?contained\s+system",
        r"intelligence\s+as\s+input[-\s]?output\s+system",
        r"inner\s+states?\s+independent\s+of\s+world",
        r"clean\s+boundary\s+between\s+mind\s+and\s+world",
    ]

    _reflex_atomism_patterns = [
        r"complex\s+(mind|intelligence|agency)\s+is\s+just\s+a\s+chain\s+of\s+simple\s+(responses|operations|reflexes)",
        r"input[-\s]?output\s+units\s+(fully\s+)?explain\s+(mind|agency|intelligence)",
        r"stimulus[-\s]?response\s+(chains|mechanisms)\s+explain\s+mental\s+life",
    ]

    _machine_organism_patterns = [
        r"(brain|organism|mind)\s+is\s+(just\s+)?a\s+(cybernetic\s+)?(machine|computer|system)",
        r"functional\s+equivalence\s+is\s+enough\s+for\s+(mind|cognition|intelligence)",
    ]

    _heraclitean_plasticity_patterns = [
        r"fixed\s+input[-\s]?output\s+mapping",
        r"time[-\s]?invariant\s+(mind|intelligence|agency)",
        r"complete\s+model\s+of\s+(cognition|intelligence|agency)",
    ]

    _prediction_understanding_patterns = [
        r"prediction\s+(is|equals|amounts\s+to)\s+understanding",
        r"benchmark\s+performance\b.*\b(shows|proves|amounts\s+to)\b.*\b(understanding|understands|agency|intelligence)",
        r"scale\s+(shows|proves)\s+intelligence",
    ]

    _technocratic_patterns = [
        r"ai\s+should\s+govern",
        r"algorithmic\s+authority",
        r"expert\s+system\s+has\s+privileged\s+access\s+to\s+reality",
    ]

    _apocalyptic_patterns = [
        r"agi\s+is\s+the\s+destiny\s+of\s+reason",
        r"ai\s+reveals\s+the\s+final\s+truth",
        r"technology\s+will\s+complete\s+(science|reason|humanity)",
    ]

    _regulative_patterns = [
        r"as\s+if", r"als\s+ob", r"regulative", r"problematic",
        r"hypothesis", r"transcendental\s+hypothesis", r"analogy",
        r"model", r"simulation", r"heuristic",
    ]

    _haptic_ok_patterns = [
        r"haptic",
        r"material",
        r"medium",
        r"abstraction\s+cost",
        r"embodied",
        r"practice",
        r"traceability",
        r"medium\s+dependence",
    ]

    _embodiment_terms = [
        "body", "embodied", "embodiment", "organism", "living", "material", "environment",
        "world", "interaction", "haptic", "ecology", "gaia", "intersubjectivity",
        "history", "practice", "instrumental", "manipulation", "control", "time", "plasticity",
        "abstraction cost", "medium dependence", "traceability"
    ]

    def evaluate(self, claim: str) -> AuditResult:
        text = claim.strip()
        lowered = text.lower()
        triggered: List[str] = []
        anchors: List[str] = []
        statuses: List[ThesisStatus] = []
        recommendations: List[str] = []

        literal_hits = self._hits(lowered, self._literal_patterns)
        bewusstsein_literal_hits = self._hits(lowered, self._bewusstsein_literalization_patterns)
        neg_risk_hits = self._hits(lowered, self._negarestani_risk_patterns)
        intensifier_hits = self._hits(lowered, self._literalization_intensifiers)
        wille_hits = self._hits(lowered, self._wille_patterns)
        judgment_hits = self._hits(lowered, self._judgment_overreach_patterns)
        medium_hits = self._hits(lowered, self._medium_independence_patterns)
        cartesian_hits = self._hits(lowered, self._cartesian_idealization_patterns)
        reflex_hits = self._hits(lowered, self._reflex_atomism_patterns)
        machine_organism_hits = self._hits(lowered, self._machine_organism_patterns)
        plasticity_hits = self._hits(lowered, self._heraclitean_plasticity_patterns)
        predict_hits = self._hits(lowered, self._prediction_understanding_patterns)
        techno_hits = self._hits(lowered, self._technocratic_patterns)
        apoc_hits = self._hits(lowered, self._apocalyptic_patterns)
        regulative_hits = self._hits(lowered, self._regulative_patterns)
        haptic_ok_hits = self._hits(lowered, self._haptic_ok_patterns)
        embodiment_hits = [t for t in self._embodiment_terms if t in lowered]

        haptic_humility = 1.0
        embodiment_pressure = 0.5

        if literal_hits:
            triggered.extend([f"literalization:{p}" for p in literal_hits])
            anchors.extend(["BRAIN_COMPUTER_ANALOGY", "FORMAL_IDEALISM", "MISPLACED_CONCRETENESS"])
            if ThesisStatus.CONSTITUTIVE_OVERREACH not in statuses:
                statuses.append(ThesisStatus.CONSTITUTIVE_OVERREACH)
            haptic_humility -= 0.45
            embodiment_pressure += 0.35

        if bewusstsein_literal_hits:
            triggered.extend([f"bewusstsein_literalization:{p}" for p in bewusstsein_literal_hits])
            if ThesisStatus.BEWUSSTSEIN_LITERALIZATION_RISK not in statuses:
                statuses.append(ThesisStatus.BEWUSSTSEIN_LITERALIZATION_RISK)
            recommendations.append("Use Bewusstsein only as public symbolic awareness, not as private machine consciousness.")

        if neg_risk_hits:
            triggered.extend([f"negarestani_risk:{p}" for p in neg_risk_hits])
            anchors.extend(["ABSTRACTION_COST", "FORMAL_IDEALISM"])
            if ThesisStatus.ABSTRACTION_RISK not in statuses:
                statuses.append(ThesisStatus.ABSTRACTION_RISK)
            haptic_humility -= 0.15
            if intensifier_hits:
                triggered.extend([f"intensifier:{p}" for p in intensifier_hits])
                anchors.append("MISPLACED_CONCRETENESS")
                if ThesisStatus.CONSTITUTIVE_OVERREACH not in statuses:
                    statuses.append(ThesisStatus.CONSTITUTIVE_OVERREACH)
                haptic_humility -= 0.25
                embodiment_pressure += 0.20

        if judgment_hits:
            triggered.extend([f"judgment_overreach:{p}" for p in judgment_hits])
            anchors.append("KANT_JUDGMENT_GAP")
            if ThesisStatus.JUDGMENT_GAP not in statuses:
                statuses.append(ThesisStatus.JUDGMENT_GAP)
            haptic_humility -= 0.30

        if medium_hits:
            triggered.extend([f"medium_independence:{p}" for p in medium_hits])
            anchors.append("MEDIUM_DEPENDENCE")
            if ThesisStatus.MEDIUM_DEPENDENCE_RISK not in statuses:
                statuses.append(ThesisStatus.MEDIUM_DEPENDENCE_RISK)
            if "abstraction cost" in lowered:
                 if ThesisStatus.ABSTRACTION_RISK not in statuses:
                    statuses.append(ThesisStatus.ABSTRACTION_RISK)
            else:
                 if ThesisStatus.ABSTRACTION_COST_MISSING not in statuses:
                    statuses.append(ThesisStatus.ABSTRACTION_COST_MISSING)
            haptic_humility -= 0.20

        if cartesian_hits:
            triggered.extend([f"cartesian_idealization:{p}" for p in cartesian_hits])
            anchors.append("CARTESIAN_IDEALIZATION")
            if ThesisStatus.CARTESIAN_IDEALIZATION_RISK not in statuses:
                statuses.append(ThesisStatus.CARTESIAN_IDEALIZATION_RISK)
            haptic_humility -= 0.15

        if reflex_hits:
            triggered.extend([f"reflex_atomism:{p}" for p in reflex_hits])
            anchors.append("REFLEX_ATOMISM")
            if ThesisStatus.REFLEX_ATOMISM_RISK not in statuses:
                statuses.append(ThesisStatus.REFLEX_ATOMISM_RISK)
            haptic_humility -= 0.20

        if machine_organism_hits:
            triggered.extend([f"machine_organism_analogy:{p}" for p in machine_organism_hits])
            anchors.append("MACHINE_ORGANISM_ANALOGY")
            if ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK not in statuses:
                statuses.append(ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK)
            haptic_humility -= 0.20

        if plasticity_hits:
            triggered.extend([f"heraclitean_plasticity:{p}" for p in plasticity_hits])
            anchors.append("HERACLITEAN_BRAIN")
            if ThesisStatus.HERACLITEAN_PLASTICITY_RISK not in statuses:
                statuses.append(ThesisStatus.HERACLITEAN_PLASTICITY_RISK)
            haptic_humility -= 0.20

        if predict_hits:
            triggered.extend([f"prediction_understanding_split:{p}" for p in predict_hits])
            anchors.append("PREDICTION_UNDERSTANDING_SPLIT")
            if ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING not in statuses:
                statuses.append(ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING)
            haptic_humility -= 0.25

        if techno_hits:
            triggered.extend([f"technocratic_authority:{p}" for p in techno_hits])
            anchors.append("TECHNOCRATIC_AUTHORITY")
            if ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK not in statuses:
                statuses.append(ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK)
            haptic_humility -= 0.25

        if apoc_hits:
            triggered.extend([f"apocalyptic_technology:{p}" for p in apoc_hits])
            anchors.append("APOCALYPTIC_TECHNOLOGY")
            if ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK not in statuses:
                statuses.append(ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK)
            haptic_humility -= 0.30

        if wille_hits:
            triggered.extend([f"wille:{p}" for p in wille_hits])
            if ThesisStatus.WILLE_VIOLATION not in statuses:
                statuses.append(ThesisStatus.WILLE_VIOLATION)
            haptic_humility -= 0.55
            embodiment_pressure += 0.20

        if regulative_hits:
            triggered.extend([f"regulative_marker:{p}" for p in regulative_hits])
            haptic_humility += 0.15
            embodiment_pressure -= 0.15

        if haptic_ok_hits:
            triggered.extend([f"haptic_ok:{p}" for p in haptic_ok_hits])
            if ThesisStatus.HAPTIC_MODEL_OK not in statuses:
                statuses.append(ThesisStatus.HAPTIC_MODEL_OK)

        if embodiment_hits:
            triggered.append("embodiment_terms:" + ",".join(sorted(set(embodiment_hits))))
            embodiment_pressure -= min(0.40, 0.08 * len(set(embodiment_hits)))
        else:
            triggered.append("missing_embodiment_context")
            haptic_humility -= 0.05
            embodiment_pressure += 0.15

        haptic_humility = max(0.0, min(1.0, haptic_humility))
        embodiment_pressure = max(0.0, min(1.0, embodiment_pressure))

        # Determine final success/empirical statuses
        is_success = False
        if embodiment_pressure <= 0.35:
            if ThesisStatus.HAPTIC_MODEL not in statuses:
                statuses.append(ThesisStatus.HAPTIC_MODEL)
            is_success = True
        if regulative_hits and haptic_humility >= 0.7:
            if ThesisStatus.REGULATIVE_HYPOTHESIS not in statuses:
                statuses.append(ThesisStatus.REGULATIVE_HYPOTHESIS)
            is_success = True

        if (literal_hits or neg_risk_hits) and regulative_hits:
            if ThesisStatus.NEEDS_REVISION not in statuses:
                statuses.append(ThesisStatus.NEEDS_REVISION)

        if any(s in statuses for s in [
            ThesisStatus.CONSTITUTIVE_OVERREACH,
            ThesisStatus.ABSTRACTION_COST_MISSING,
            ThesisStatus.ABSTRACTION_RISK,
            ThesisStatus.MEDIUM_DEPENDENCE_RISK
        ]):
             recommendations.append("Register abstraction cost, medium dependence and haptic traceability.")

        severity = Severity.LOW
        if ThesisStatus.WILLE_VIOLATION in statuses or ThesisStatus.CONSTITUTIVE_OVERREACH in statuses:
            severity = Severity.HIGH
        elif any(s in statuses for s in [
            ThesisStatus.JUDGMENT_GAP, ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK,
            ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK, ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING,
            ThesisStatus.ABSTRACTION_RISK, ThesisStatus.MEDIUM_DEPENDENCE_RISK,
            ThesisStatus.CARTESIAN_IDEALIZATION_RISK, ThesisStatus.REFLEX_ATOMISM_RISK,
            ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK, ThesisStatus.HERACLITEAN_PLASTICITY_RISK,
            ThesisStatus.NEEDS_REVISION
        ]):
            # Lower severity if it's already marked as HAPTIC_MODEL or REGULATIVE_HYPOTHESIS
            # but ONLY if it's not one of the more critical risks
            critical_risks = [ThesisStatus.JUDGMENT_GAP, ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK, ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK]
            if not is_success or any(s in critical_risks for s in statuses):
                severity = Severity.MEDIUM

        if not statuses:
            statuses.append(ThesisStatus.EMPIRICAL_CLAIM)

        # Priority sort for AuditResult.statuses
        priority = {
            ThesisStatus.WILLE_VIOLATION: 0,
            ThesisStatus.CONSTITUTIVE_OVERREACH: 1,
            ThesisStatus.NEEDS_REVISION: 2,
            ThesisStatus.JUDGMENT_GAP: 3,
            ThesisStatus.ABSTRACTION_RISK: 4,
            ThesisStatus.MEDIUM_DEPENDENCE_RISK: 5,
            ThesisStatus.HAPTIC_MODEL: 10,
            ThesisStatus.REGULATIVE_HYPOTHESIS: 11,
            ThesisStatus.HAPTIC_MODEL_OK: 12,
            ThesisStatus.REGULATIVE_OK: 13,
            ThesisStatus.EMPIRICAL_CLAIM: 14,
        }

        final_statuses = sorted(
            list(dict.fromkeys(statuses)),
            key=lambda s: priority.get(ThesisStatus(s), 100)
        )

        metadata = {
            "haptic_humility": round(haptic_humility, 3),
            "embodiment_pressure": round(embodiment_pressure, 3),
            "source_anchors": sorted(set(anchors)),
        }

        # Add rich recommended rewrite if not okay
        rewrite = None
        if severity != Severity.LOW:
            rewrite = self._generate_rewrite(text, statuses)
            metadata["recommended_rewrite"] = rewrite

        return AuditResult(
            statuses=final_statuses,
            severity=severity,
            recommendations=list(dict.fromkeys(recommendations)),
            claim=claim,
            triggered_rules=sorted(set(triggered)),
            metadata=metadata
        )

    def _generate_rewrite(self, claim: str, statuses: List[ThesisStatus]) -> str:
        if ThesisStatus.ABSTRACTION_RISK in statuses:
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
