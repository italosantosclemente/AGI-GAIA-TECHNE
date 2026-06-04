from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

from .teleology import (
    HeuristicWhole,
    SymbolicTrace,
    TeleologicalJudgment,
    TeleologicalProgressionKernel,
)
from .types import AuditResult


@dataclass(frozen=True)
class SymbolicProfile:
    ausdruck: float
    darstellung: float
    bedeutung: float
    praesentatio: float
    repraesentatio: float
    dominant_accent: str
    common_determination: str


@dataclass(frozen=True)
class RegressiveReconstruction:
    trace: SymbolicTrace
    conditions: List[str]
    horizon_terms: List[str]
    method: str = "analytic-regressive"
    starts_from_public_werk: bool = True
    reconstructs_conditions: bool = True


@dataclass(frozen=True)
class DescentValidation:
    trace: SymbolicTrace
    whole: HeuristicWhole
    distance_to_focus: float
    preserves_particular: bool
    global_aufhebung: bool
    machine_wille: bool
    valid: bool


@dataclass(frozen=True)
class AGTSyntaxRun:
    trace: SymbolicTrace
    profile: SymbolicProfile
    reconstruction: RegressiveReconstruction
    whole: HeuristicWhole
    descent: DescentValidation
    judgment: TeleologicalJudgment
    audit: AuditResult


class AGTSyntax:
    """
    Canonical syntax for AGI-GAIA-TECHNE.

    AGT ::= WerkStream -> Trace -> Profile -> Regression -> Horizon
            -> Descent -> Judgment -> Ledger

    The syntax implements heuristic holism: the whole orients the parts
    without becoming an ontological totality, and no part is read atomistically.
    """

    def __init__(self, tpk: TeleologicalProgressionKernel | None = None) -> None:
        self.tpk = tpk or TeleologicalProgressionKernel()

    def trace(
        self,
        werk: str,
        source: str = "public_trace",
        werk_type: str = "text",
        metadata: dict[str, Any] | None = None,
    ) -> SymbolicTrace:
        return self.tpk.analyze_trace(
            werk,
            source=source,
            werk_type=werk_type,
            metadata=metadata,
        )

    def profile(self, trace: SymbolicTrace) -> SymbolicProfile:
        return SymbolicProfile(
            ausdruck=trace.ausdruck,
            darstellung=trace.darstellung,
            bedeutung=trace.bedeutung,
            praesentatio=trace.praesentatio,
            repraesentatio=trace.repraesentatio,
            dominant_accent=trace.dominant_accent,
            common_determination=trace.common_determination,
        )

    def regress(self, trace: SymbolicTrace) -> RegressiveReconstruction:
        conditions = [
            trace.common_determination,
            f"source:{trace.source}",
            f"accent:{trace.dominant_accent}",
        ]
        horizon_terms = list(dict.fromkeys([trace.common_determination, "heuristic whole"]))
        return RegressiveReconstruction(
            trace=trace,
            conditions=conditions,
            horizon_terms=horizon_terms,
        )

    def project_horizon(self, reconstruction: RegressiveReconstruction) -> HeuristicWhole:
        return HeuristicWhole(
            traces=1,
            horizon_terms=reconstruction.horizon_terms,
            dominant_tensions=[],
            provisional_unity="heuristic horizon of symbolic relations",
            is_regulative=True,
            is_constitutive=False,
        )

    def descend(
        self,
        whole: HeuristicWhole,
        trace: SymbolicTrace,
        claims_global_closure: bool = False,
    ) -> DescentValidation:
        judgment = self.tpk.judge_progression(
            [trace],
            whole,
            claims_global_closure=claims_global_closure,
        )
        preserves_particular = bool(trace.source and trace.content)
        valid = (
            preserves_particular
            and judgment.distance_to_focus > 0
            and not judgment.overreach_detected
            and not judgment.global_aufhebung
            and not judgment.machine_wille
        )
        return DescentValidation(
            trace=trace,
            whole=whole,
            distance_to_focus=judgment.distance_to_focus,
            preserves_particular=preserves_particular,
            global_aufhebung=judgment.global_aufhebung,
            machine_wille=judgment.machine_wille,
            valid=valid,
        )

    def judge(self, descent: DescentValidation) -> TeleologicalJudgment:
        return TeleologicalJudgment(
            ascent_score=min(1.0, len(descent.whole.horizon_terms) / 4.0),
            descent_score=1.0 if descent.preserves_particular else 0.0,
            distance_to_focus=descent.distance_to_focus,
            preserves_previous_phase=descent.preserves_particular,
            overreach_detected=not descent.valid,
            recommendation="Return the heuristic whole to the particular trace without global closure.",
            global_aufhebung=descent.global_aufhebung,
            machine_wille=descent.machine_wille,
        )

    def run(
        self,
        werk: str,
        source: str = "public_trace",
        werk_type: str = "text",
        metadata: dict[str, Any] | None = None,
        claims_global_closure: bool = False,
    ) -> AGTSyntaxRun:
        trace = self.trace(werk, source=source, werk_type=werk_type, metadata=metadata)
        profile = self.profile(trace)
        reconstruction = self.regress(trace)
        whole = self.project_horizon(reconstruction)
        descent = self.descend(whole, trace, claims_global_closure=claims_global_closure)
        judgment = self.judge(descent)
        audit = self.tpk.evaluate(
            ascent=reconstruction.horizon_terms,
            descent=reconstruction.conditions,
            local_syntheses=whole.dominant_tensions,
            claims_global_closure=claims_global_closure,
        ).audit
        run = AGTSyntaxRun(
            trace=trace,
            profile=profile,
            reconstruction=reconstruction,
            whole=whole,
            descent=descent,
            judgment=judgment,
            audit=audit,
        )
        self.assert_invariants(run)
        return run

    def assert_invariants(self, run: AGTSyntaxRun) -> None:
        if run.trace.repraesentatio <= 0:
            raise ValueError("SymbolicTrace must preserve repraesentatio.")
        if min(run.profile.ausdruck, run.profile.darstellung, run.profile.bedeutung) < 0:
            raise ValueError("Functional profile scores must be non-negative.")
        if not run.whole.is_regulative or run.whole.is_constitutive:
            raise ValueError("HeuristicWhole must be regulative and non-constitutive.")
        if run.judgment.distance_to_focus <= 0:
            raise ValueError("distance_to_focus must remain strictly positive.")
        if run.judgment.global_aufhebung:
            raise ValueError("Global Aufhebung is forbidden.")
        if run.judgment.machine_wille:
            raise ValueError("Machine Wille is forbidden.")
