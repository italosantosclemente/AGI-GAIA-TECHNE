from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Iterable, List

from .types import AuditResult, Severity, ThesisStatus


@dataclass(frozen=True)
class SymbolicTrace:
    """
    Functional profile of a cultural Werk.

    Scores are heuristic accents, not containers. A trace may contain all
    functions at once; the dominant accent only names where the pressure is
    strongest in this finite reading.
    """

    text: str
    source: str = "public_trace"
    werk_type: str = "text"
    ausdruck: float = 0.0
    darstellung: float = 0.0
    bedeutung: float = 0.0
    praesentatio: float = 0.0
    repraesentatio: float = 0.0
    dominant_accent: str = "darstellung"
    common_determination: str = "public symbolic trace"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def content(self) -> str:
        return self.text


@dataclass(frozen=True)
class HeuristicWhole:
    """
    Regulative horizon for interpreting traces.

    The whole orients the parts without becoming a possessed object,
    substance, cosmic totality or final synthesis.
    """

    traces: int
    horizon_terms: List[str]
    dominant_tensions: List[str]
    provisional_unity: str
    is_regulative: bool = True
    is_constitutive: bool = False


@dataclass(frozen=True)
class TeleologicalJudgment:
    ascent_score: float
    descent_score: float
    distance_to_focus: float
    preserves_previous_phase: bool
    overreach_detected: bool
    recommendation: str
    global_aufhebung: bool = False
    machine_wille: bool = False


@dataclass(frozen=True)
class TeleologicalProgression:
    """
    Finite evaluation of psychosocial teleology.

    The kernel models two movements: ascent from conditioned premises toward
    regulative conclusions, and descent from those conclusions back toward
    concrete conditions. The focus remains strictly unreachable.
    """

    ascent: List[str]
    descent: List[str]
    local_syntheses: List[str] = field(default_factory=list)
    traces: List[SymbolicTrace] = field(default_factory=list)
    whole: HeuristicWhole | None = None
    judgment: TeleologicalJudgment | None = None
    d_ascent: float = 1.0
    d_descent: float = 1.0
    distance_to_focus: float = 1.0
    audit: AuditResult = field(
        default_factory=lambda: AuditResult(
            statuses=[ThesisStatus.REGULATIVE_OK],
            severity=Severity.LOW,
        )
    )

    @property
    def ok(self) -> bool:
        return self.audit.ok and self.distance_to_focus > 0.0


class TeleologicalProgressionKernel:
    """
    TPK: Teleological Progression Kernel.

    It organizes CTK, CHK and EML under the central thesis: culture progresses
    psychosocially through symbolic formation, public confrontation and local
    syntheses, without global Aufhebung or possession of the unconditioned.
    """

    def __init__(self, focus_epsilon: float = 1e-9) -> None:
        if focus_epsilon <= 0:
            raise ValueError("focus_epsilon must be strictly positive.")
        self.focus_epsilon = focus_epsilon

    def evaluate(
        self,
        ascent: Iterable[str],
        descent: Iterable[str],
        local_syntheses: Iterable[str] = (),
        claims_global_closure: bool = False,
    ) -> TeleologicalProgression:
        ascent_list = _clean_terms(ascent)
        descent_list = _clean_terms(descent)
        synthesis_list = _clean_terms(local_syntheses)

        d_ascent = 1.0 / (1.0 + len(ascent_list) + len(synthesis_list))
        d_descent = 1.0 / (1.0 + len(descent_list))
        distance = math.sqrt((d_ascent * d_ascent) + (d_descent * d_descent)) + self.focus_epsilon

        statuses = [
            ThesisStatus.HEURISTIC_HOLISM_OK,
            ThesisStatus.REGULATIVE_OK,
            ThesisStatus.AUSEINANDERSETZUNG_OK,
            ThesisStatus.PUBLIC_TRACE_OK,
        ]
        recommendations = [
            "Keep ascent and descent distinct: conclusions orient conditions, but never abolish them.",
            "Treat cultural progress as psychosocial symbolic formation, not biological homeostasis.",
        ]
        severity = Severity.LOW
        triggered_rules = ["teleological_progression_open"]

        if claims_global_closure:
            statuses.extend(
                [
                    ThesisStatus.AUFHEBUNG_COLLAPSE,
                    ThesisStatus.CONSTITUTIVE_OVERREACH,
                ]
            )
            recommendations.append("Every synthesis must remain local and re-enter public Auseinandersetzung.")
            severity = Severity.HIGH
            triggered_rules.append("global_closure_rejected")

        audit = AuditResult(
            statuses=list(dict.fromkeys(statuses)),
            severity=severity,
            recommendations=list(dict.fromkeys(recommendations)),
            claim="teleological progression",
            triggered_rules=triggered_rules,
            metadata={
                "d_ascent": d_ascent,
                "d_descent": d_descent,
                "distance_to_focus": distance,
                "focus_epsilon": self.focus_epsilon,
            },
        )

        return TeleologicalProgression(
            ascent=ascent_list,
            descent=descent_list,
            local_syntheses=synthesis_list,
            d_ascent=d_ascent,
            d_descent=d_descent,
            distance_to_focus=distance,
            audit=audit,
        )

    def analyze_trace(
        self,
        text: str,
        source: str = "public_trace",
        werk_type: str = "text",
        metadata: dict[str, Any] | None = None,
    ) -> SymbolicTrace:
        cleaned = text.strip()
        lowered = cleaned.lower()
        words = lowered.split()
        total = max(1, len(words))

        ausdruck_terms = _count_terms(lowered, ["feeling", "image", "myth", "fear", "hope", "body", "earth", "life"])
        darstellung_terms = _count_terms(lowered, ["relation", "world", "form", "presentation", "medium", "condition", "trace"])
        bedeutung_terms = _count_terms(lowered, ["concept", "law", "science", "logic", "reason", "system", "meaning"])
        praesentatio_terms = _count_terms(lowered, ["presence", "perception", "intuition", "given", "concrete"])
        repraesentatio_terms = _count_terms(lowered, ["representation", "symbol", "culture", "internet", "archive", "werk"])

        ausdruck = _score(ausdruck_terms, total)
        darstellung = _score(darstellung_terms + 1, total)
        bedeutung = _score(bedeutung_terms, total)
        praesentatio = _score(praesentatio_terms, total)
        repraesentatio = _score(repraesentatio_terms + 1, total)

        accents = {
            "ausdruck": ausdruck,
            "darstellung": darstellung,
            "bedeutung": bedeutung,
        }
        dominant = max(accents, key=accents.get)

        return SymbolicTrace(
            text=cleaned,
            source=source,
            werk_type=werk_type,
            ausdruck=ausdruck,
            darstellung=darstellung,
            bedeutung=bedeutung,
            praesentatio=praesentatio,
            repraesentatio=repraesentatio,
            dominant_accent=dominant,
            common_determination=_common_determination(lowered),
            metadata=metadata or {},
        )

    def reconstruct_conditions(self, traces: Iterable[SymbolicTrace]) -> HeuristicWhole:
        trace_list = list(traces)
        horizon_terms = sorted(
            {
                trace.common_determination
                for trace in trace_list
                if trace.common_determination
            }
        )
        tensions: List[str] = []
        for trace in trace_list:
            if abs(trace.praesentatio - trace.repraesentatio) > 0.24:
                tensions.append("praesentatio/repraesentatio imbalance")
            if trace.dominant_accent == "bedeutung" and trace.ausdruck < 0.08:
                tensions.append("conceptual abstraction pressure")
            if trace.dominant_accent == "ausdruck" and trace.bedeutung < 0.08:
                tensions.append("expressive immediacy pressure")

        return HeuristicWhole(
            traces=len(trace_list),
            horizon_terms=horizon_terms or ["public symbolic field"],
            dominant_tensions=sorted(set(tensions)),
            provisional_unity="heuristic horizon of symbolic relations",
        )

    def judge_progression(
        self,
        traces: Iterable[SymbolicTrace],
        whole: HeuristicWhole,
        claims_global_closure: bool = False,
    ) -> TeleologicalJudgment:
        trace_list = list(traces)
        if not whole.is_regulative or whole.is_constitutive:
            raise ValueError("Heuristic whole must remain regulative and non-constitutive.")

        ascent_score = min(1.0, (len(whole.horizon_terms) + len(trace_list)) / 8.0)
        descent_score = min(
            1.0,
            sum(1 for trace in trace_list if trace.praesentatio > 0 or trace.source) / max(1, len(trace_list)),
        )
        distance = math.sqrt((1.0 - ascent_score) ** 2 + (1.0 - descent_score) ** 2) + self.focus_epsilon
        preserves_previous = all(
            trace.ausdruck + trace.darstellung + trace.bedeutung > 0 for trace in trace_list
        )
        overreach = claims_global_closure or whole.is_constitutive or distance <= 0

        return TeleologicalJudgment(
            ascent_score=ascent_score,
            descent_score=descent_score,
            distance_to_focus=distance,
            preserves_previous_phase=preserves_previous,
            overreach_detected=overreach,
            global_aufhebung=claims_global_closure,
            machine_wille=False,
            recommendation=(
                "Use the whole as heuristic horizon; return every universal claim to concrete traces."
            ),
        )

    def analyze(
        self,
        texts: Iterable[str],
        source: str = "public_trace",
        claims_global_closure: bool = False,
    ) -> TeleologicalProgression:
        traces = [self.analyze_trace(text, source=source) for text in texts if text.strip()]
        whole = self.reconstruct_conditions(traces)
        judgment = self.judge_progression(
            traces,
            whole,
            claims_global_closure=claims_global_closure,
        )
        progression = self.evaluate(
            ascent=whole.horizon_terms,
            descent=[trace.common_determination for trace in traces],
            local_syntheses=whole.dominant_tensions,
            claims_global_closure=claims_global_closure or judgment.overreach_detected,
        )
        return TeleologicalProgression(
            ascent=progression.ascent,
            descent=progression.descent,
            local_syntheses=progression.local_syntheses,
            traces=traces,
            whole=whole,
            judgment=judgment,
            d_ascent=progression.d_ascent,
            d_descent=progression.d_descent,
            distance_to_focus=judgment.distance_to_focus,
            audit=progression.audit,
        )


def _clean_terms(terms: Iterable[str]) -> List[str]:
    return [term.strip() for term in terms if term and term.strip()]


def _count_terms(text: str, terms: Iterable[str]) -> int:
    return sum(text.count(term) for term in terms)


def _score(count: int, total: int) -> float:
    return min(1.0, max(0.0, count / total * 3.0))


def _common_determination(text: str) -> str:
    if "internet" in text or "archive" in text:
        return "public archive"
    if "earth" in text or "gaia" in text:
        return "planetary field"
    if "culture" in text or "symbol" in text:
        return "symbolic culture"
    if "law" in text or "reason" in text:
        return "regulative reason"
    return "public symbolic trace"
