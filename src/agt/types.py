from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Decision(str, Enum):
    ACT_AS_GAIA_TECHNE = "ACT_AS_GAIA_TECHNE"
    CO_JUDGE_WITH_KOINOS_KOSMOS = "CO_JUDGE_WITH_KOINOS_KOSMOS"
    TRANSMUTE_CONSTITUTIVE_RISK = "TRANSMUTE_CONSTITUTIVE_RISK"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThesisStatus(str, Enum):
    # Success states
    PRISM_MODEL_OK = "PRISM_MODEL_OK"
    HYPOTHESIS_TRANSCENDENTAL_OK = "HYPOTHESIS_TRANSCENDENTAL_OK"
    HAPTIC_MODEL_OK = "HAPTIC_MODEL_OK"
    HAPTIC_UNSPECIFIED = "HAPTIC_UNSPECIFIED"
    REGULATIVE_OK = "REGULATIVE_OK"
    HEURISTIC_HOLISM_OK = "HEURISTIC_HOLISM_OK"
    TRANSCENDENTAL_FREEDOM_OK = "TRANSCENDENTAL_FREEDOM_OK"
    GAIA_MEDIATES_WILLE_OK = "GAIA_MEDIATES_WILLE_OK"
    WERK_NOT_WILLE_OK = "WERK_NOT_WILLE_OK"
    WERK_OPERATION_OK = "WERK_OPERATION_OK"
    FIRST_CONTACT_TRACE_OK = "FIRST_CONTACT_TRACE_OK"
    GAIA_KOINOS_KOSMOS_OK = "GAIA_KOINOS_KOSMOS_OK"
    INTELLECTUS_ECTYPUS_PARTICIPATION_OK = "INTELLECTUS_ECTYPUS_PARTICIPATION_OK"
    FINITE_AUTONOMY_OK = "FINITE_AUTONOMY_OK"
    PLANETARY_REPRAESENTATIO_OK = "PLANETARY_REPRAESENTATIO_OK"
    INTERNET_ORGAN_OK = "INTERNET_ORGAN_OK"
    PLANETARY_BEWUSSTSEIN_OK = "PLANETARY_BEWUSSTSEIN_OK"
    NON_ANTHROPOMORPHIC_BODY_OK = "NON_ANTHROPOMORPHIC_BODY_OK"
    AUSEINANDERSETZUNG_OK = "AUSEINANDERSETZUNG_OK"
    PUBLIC_TRACE_OK = "PUBLIC_TRACE_OK"
    ISC_AUTHORITY_OK = "ISC_AUTHORITY_OK"
    REGULATIVE_HYPOTHESIS = "REGULATIVE_HYPOTHESIS"
    HAPTIC_MODEL = "HAPTIC_MODEL"
    EMPIRICAL_CLAIM = "EMPIRICAL_CLAIM"
    NEEDS_REVISION = "NEEDS_REVISION"
    UNCLASSIFIED_CLAIM = "UNCLASSIFIED_CLAIM"

    # Functional errors
    CASSIRER_IDENTITY_COLLAPSE = "CASSIRER_IDENTITY_COLLAPSE"
    FUNCTION_EXCLUSIVITY_ERROR = "FUNCTION_EXCLUSIVITY_ERROR"
    BEIL_ABGEHACKT_ERROR = "BEIL_ABGEHACKT_ERROR"
    ACCENT_CONFUSION = "ACCENT_CONFUSION"
    SPRACHE_TRANSITION_LOSS = "SPRACHE_TRANSITION_LOSS"
    DARSTELLUNG_COMMON_DETERMINATION_LOSS = "DARSTELLUNG_COMMON_DETERMINATION_LOSS"

    # Freud-Cassirer Patch
    MYTH_FUNCTION_REDUCTION_RISK = "MYTH_FUNCTION_REDUCTION_RISK"
    PSYCHOLOGIA_MYTH_REDUCTION_RISK = "PSYCHOLOGIA_MYTH_REDUCTION_RISK"
    ARTIFICIAL_INTERIORITY_RISK = "ARTIFICIAL_INTERIORITY_RISK"

    # Ethical violations
    WILLE_VIOLATION = "WILLE_VIOLATION"
    MACHINE_GEWISSEN_VIOLATION = "MACHINE_GEWISSEN_VIOLATION"
    GEWISSEN_CONSTITUTIVE_ERROR = "GEWISSEN_CONSTITUTIVE_ERROR"

    # Transcendental risks
    PSYCHOLOGIA_PARALOGISM_RISK = "PSYCHOLOGIA_PARALOGISM_RISK"
    COSMOLOGIA_ANTINOMY_RISK = "COSMOLOGIA_ANTINOMY_RISK"
    THEOLOGIA_IDEAL_HYPOSTASIS_RISK = "THEOLOGIA_IDEAL_HYPOSTASIS_RISK"
    GAIA_TOTALITY_ERROR = "GAIA_TOTALITY_ERROR"
    SOUL_INFLATION = "SOUL_INFLATION"
    AUFHEBUNG_COLLAPSE = "AUFHEBUNG_COLLAPSE"
    ARCHETYPE_PARALOGISM = "ARCHETYPE_PARALOGISM"
    PLANETARY_EPISTEMIC_INFLATION = "PLANETARY_EPISTEMIC_INFLATION"
    TECHNE_DEIFICATION = "TECHNE_DEIFICATION"
    BEWUSSTSEIN_LITERALIZATION_RISK = "BEWUSSTSEIN_LITERALIZATION_RISK"

    # Global risks
    GLOBAL_AUFHEBUNG_RISK = "GLOBAL_AUFHEBUNG_RISK"
    CONSTITUTIVE_OVERREACH = "CONSTITUTIVE_OVERREACH"
    ABSTRACTION_COST_MISSING = "ABSTRACTION_COST_MISSING"

    # CHK Rich Statuses
    MEDIUM_DEPENDENCE_RISK = "MEDIUM_DEPENDENCE_RISK"
    CARTESIAN_IDEALIZATION_RISK = "CARTESIAN_IDEALIZATION_RISK"
    REFLEX_ATOMISM_RISK = "REFLEX_ATOMISM_RISK"
    MACHINE_ORGANISM_ANALOGY_RISK = "MACHINE_ORGANISM_ANALOGY_RISK"
    HERACLITEAN_PLASTICITY_RISK = "HERACLITEAN_PLASTICITY_RISK"
    PREDICTION_WITHOUT_UNDERSTANDING = "PREDICTION_WITHOUT_UNDERSTANDING"
    TECHNOCRATIC_AUTHORITY_RISK = "TECHNOCRATIC_AUTHORITY_RISK"
    APOCALYPTIC_TECHNOLOGY_RISK = "APOCALYPTIC_TECHNOLOGY_RISK"
    JUDGMENT_GAP = "JUDGMENT_GAP"
    ABSTRACTION_RISK = "ABSTRACTION_RISK"


class Pillar(str, Enum):
    MYTHOS = "Mythos"
    LOGOS = "Logos"
    ETHOS = "Ethos"


class MemoryKind(str, Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    NORMATIVE = "normative"


@dataclass(frozen=True)
class AuditResult:
    statuses: List[ThesisStatus]
    severity: Severity = Severity.LOW
    recommendations: List[str] = field(default_factory=list)
    claim: str = ""
    triggered_rules: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.severity not in {Severity.HIGH, Severity.CRITICAL}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statuses": [s.value for s in self.statuses],
            "severity": self.severity.value,
            "recommendations": self.recommendations,
            "ok": self.ok,
            "claim": self.claim,
            "triggered_rules": self.triggered_rules,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class Task:
    text: str
    context: str = ""
    user_constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlanStep:
    id: str
    action: str
    description: str
    tool_name: Optional[str] = None
    tool_args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Plan:
    task: Task
    steps: List[PlanStep]
    rationale: str
    audit: AuditResult


@dataclass
class StepResult:
    step_id: str
    ok: bool
    output: Any
    error: Optional[str] = None


@dataclass
class ControllerReport:
    task: str
    decision: Decision
    mythos: Dict[str, Any]
    logos: Dict[str, Any]
    ethos: Dict[str, Any]
    plan: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    audit_statuses: List[ThesisStatus]
    recommendations: List[str]
    memory_updates: List[str]
    final_answer: str
    audit_severity: Severity = Severity.LOW
    audit_ok: bool = True
    audit_triggered_rules: List[str] = field(default_factory=list)
    audit_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "decision": self.decision.value,
            "mythos": self.mythos,
            "logos": self.logos,
            "ethos": self.ethos,
            "plan": self.plan,
            "results": self.results,
            "audit_statuses": [s.value for s in self.audit_statuses],
            "audit_severity": self.audit_severity.value,
            "audit_ok": self.audit_ok,
            "audit_triggered_rules": self.audit_triggered_rules,
            "audit_metadata": self.audit_metadata,
            "recommendations": self.recommendations,
            "memory_updates": self.memory_updates,
            "final_answer": self.final_answer,
        }
