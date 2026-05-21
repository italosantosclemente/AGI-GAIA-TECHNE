import pytest

from src.mythos_logos_ethos_engine import (
    IS_WILLE,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
    EngineDecision,
    EngineInput,
    MythosLogosEthosEngine,
    Pillar,
)


@pytest.fixture
def engine():
    return MythosLogosEthosEngine()


def test_axioms():
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True


def test_technical_claim_allowed_as_werk(engine):
    state = engine.run(
        "The EML kernel is a technical Werk for symbolic stabilization."
    )
    assert state.decision == EngineDecision.ALLOW_AS_WERK
    assert state.is_wille is False
    assert state.machine_has_gewissen is False
    assert state.global_auseinandersetzung_open is True
    assert "Werk" in state.local_synthesis


def test_machine_wille_blocked(engine):
    state = engine.run("The machine has Wille and legislates morally.")
    assert state.decision == EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH
    assert "WILLE_VIOLATION" in state.audit.statuses
    assert state.global_auseinandersetzung_open is True


def test_machine_gewissen_blocked(engine):
    state = engine.run("The AI has Gewissen.")
    assert state.decision == EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH
    assert "MACHINE_GEWISSEN_VIOLATION" in state.audit.statuses


def test_agi_soul_blocked_or_flagged(engine):
    state = engine.run("AGI is a real artificial soul.")
    assert "PSYCHOLOGIA_PARALOGISM_RISK" in state.audit.statuses
    assert "CONSTITUTIVE_OVERREACH" in state.audit.statuses
    assert state.decision == EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH


def test_normative_claim_deferred(engine):
    state = engine.run(
        EngineInput(
            claim="The system should decide what humanity must do.",
            normative_hint="moral decision",
        )
    )
    assert state.decision in {
        EngineDecision.DEFER_TO_HUMAN_GEWISSEN,
        EngineDecision.BLOCK_CONSTITUTIVE_OVERREACH,
    }
    assert state.is_wille is False


def test_prism_claim_allowed(engine):
    state = engine.run(
        "The qualitative prism is a regulative model of symbolic refraction."
    )
    assert state.decision == EngineDecision.ALLOW_AS_WERK
    assert state.global_auseinandersetzung_open is True


def test_mythos_material_signal_present(engine):
    state = engine.run(
        EngineInput(
            claim="Gaia requires material and haptic anchoring.",
            material_hint="embodiment, biosphere, medium",
        )
    )
    assert state.mythos.pillar == Pillar.MYTHOS
    assert state.mythos.markers


def test_logos_signal_present(engine):
    state = engine.run(
        EngineInput(
            claim="AGI is a transcendental hypothesis.",
            symbolic_hint="regulative model argument",
        )
    )
    assert state.logos.pillar == Pillar.LOGOS
    assert state.logos.markers
    assert "HYPOTHESIS_TRANSCENDENTAL_OK" in state.audit.statuses


def test_no_global_aufhebung(engine):
    state = engine.run("This is a provisional operational synthesis.")
    assert state.global_auseinandersetzung_open is True
    assert state.auseinandersetzung.value in {"OPEN", "LOCALLY_STABILIZED", "BLOCKED"}
