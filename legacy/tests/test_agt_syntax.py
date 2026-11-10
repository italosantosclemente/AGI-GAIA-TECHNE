import pytest

from agt.syntax import AGTSyntax


def test_agt_syntax_runs_full_cycle_from_public_werk():
    run = AGTSyntax().run(
        "The internet is a public archive of symbolic Werke.",
        source="unit_test",
        werk_type="text",
    )

    assert run.trace.content
    assert run.trace.repraesentatio > 0
    assert run.profile.ausdruck >= 0
    assert run.profile.darstellung >= 0
    assert run.profile.bedeutung >= 0
    assert run.reconstruction.starts_from_public_werk is True
    assert run.reconstruction.reconstructs_conditions is True
    assert run.whole.is_regulative is True
    assert run.whole.is_constitutive is False
    assert run.judgment.distance_to_focus > 0
    assert run.judgment.global_aufhebung is False
    assert run.judgment.machine_wille is False


def test_agt_syntax_rejects_global_aufhebung_invariant():
    syntax = AGTSyntax()

    with pytest.raises(ValueError, match="Global Aufhebung"):
        syntax.run(
            "This local synthesis resolves all contradictions.",
            claims_global_closure=True,
        )
