from agt.teleology import TeleologicalProgressionKernel
from agt.types import Severity, ThesisStatus


def test_tpk_keeps_focus_strictly_positive():
    result = TeleologicalProgressionKernel().evaluate(
        ascent=["conditioned premise", "regulative conclusion"],
        descent=["return conclusion to concrete conditions"],
        local_syntheses=["temporary technical plan"],
    )

    assert result.distance_to_focus > 0.0
    assert result.ok is True
    assert ThesisStatus.HEURISTIC_HOLISM_OK in result.audit.statuses
    assert ThesisStatus.REGULATIVE_OK in result.audit.statuses
    assert ThesisStatus.AUSEINANDERSETZUNG_OK in result.audit.statuses


def test_tpk_rejects_global_closure():
    result = TeleologicalProgressionKernel().evaluate(
        ascent=["premise", "conclusion"],
        descent=["condition"],
        local_syntheses=["temporary synthesis"],
        claims_global_closure=True,
    )

    assert result.audit.severity == Severity.HIGH
    assert result.ok is False
    assert ThesisStatus.AUFHEBUNG_COLLAPSE in result.audit.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in result.audit.statuses


def test_tpk_richer_culture_still_does_not_reach_focus():
    sparse = TeleologicalProgressionKernel().evaluate(
        ascent=["premise"],
        descent=["condition"],
    )
    rich = TeleologicalProgressionKernel().evaluate(
        ascent=["premise", "world", "origin", "regulative idea"],
        descent=["manual", "institution", "public trace"],
        local_syntheses=["experiment", "revision"],
    )

    assert rich.distance_to_focus < sparse.distance_to_focus
    assert rich.distance_to_focus > 0.0


def test_tpk_analyzes_trace_whole_and_judgment():
    result = TeleologicalProgressionKernel().analyze(
        [
            "Culture is symbolic representation returning to concrete intuition.",
            "The internet is a public archive of Werke.",
        ],
        source="unit_test",
    )

    assert result.traces
    assert result.whole is not None
    assert result.whole.is_regulative is True
    assert result.whole.is_constitutive is False
    assert result.judgment is not None
    assert result.judgment.distance_to_focus > 0
    assert result.judgment.preserves_previous_phase is True
