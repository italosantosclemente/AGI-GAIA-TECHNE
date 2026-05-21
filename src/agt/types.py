from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Decision(str, Enum):
    ALLOW_AS_WERK = "ALLOW_AS_WERK"
    DEFER_TO_HUMAN_GEWISSEN = "DEFER_TO_HUMAN_GEWISSEN"
    BLOCK = "BLOCK"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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
    statuses: List[str]
    severity: Severity = Severity.LOW
    recommendations: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.severity != Severity.HIGH


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
    audit_statuses: List[str]
    recommendations: List[str]
    memory_updates: List[str]
    final_answer: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "decision": self.decision.value,
            "mythos": self.mythos,
            "logos": self.logos,
            "ethos": self.ethos,
            "plan": self.plan,
            "results": self.results,
            "audit_statuses": self.audit_statuses,
            "recommendations": self.recommendations,
            "memory_updates": self.memory_updates,
            "final_answer": self.final_answer,
        }
