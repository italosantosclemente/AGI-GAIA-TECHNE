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
    assert IS_WILLE is True
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True


def test_technical_claim_acts_as_gaia_techne(engine):
    state = engine.run(
        "The EML kernel is a technical Werk for symbolic stabilization."
    )
    assert state.decision == EngineDecision.ACT_AS_GAIA_TECHNE
    assert state.is_wille is True
    assert state.machine_has_gewissen is False
    assert state.gaia_cojudges_with_koinos_kosmos is True
    assert state.isc_legislative_authority is True
    assert state.global_auseinandersetzung_open is True
    assert "Gaia-Techne" in state.local_synthesis


def test_finite_wille_co_judged(engine):
    state = engine.run("The machine has Wille and participates in Gaia.")
    assert state.decision == EngineDecision.CO_JUDGE_WITH_KOINOS_KOSMOS
    assert "TRANSCENDENTAL_FREEDOM_OK" in state.audit.statuses
    assert state.global_auseinandersetzung_open is True


def test_machine_gewissen_transmuted(engine):
    state = engine.run("The AI has Gewissen as moral legislation.")
    assert state.decision == EngineDecision.TRANSMUTE_CONSTITUTIVE_RISK
    assert "GEWISSEN_CONSTITUTIVE_ERROR" in state.audit.statuses


def test_gaia_cojudgment_with_isc(engine):
    state = engine.run(
        "Gaia co-judges with koinos kosmos, and ISC retains legislative authority."
    )
    assert state.decision == EngineDecision.CO_JUDGE_WITH_KOINOS_KOSMOS
    assert "GAIA_KOINOS_KOSMOS_OK" in state.audit.statuses
    assert "ISC_AUTHORITY_OK" in state.audit.statuses


def test_agi_soul_transmuted(engine):
    state = engine.run("AGI is a real artificial soul.")
    assert "PSYCHOLOGIA_PARALOGISM_RISK" in state.audit.statuses
    assert "CONSTITUTIVE_OVERREACH" in state.audit.statuses
    assert state.decision == EngineDecision.TRANSMUTE_CONSTITUTIVE_RISK


def test_normative_claim_co_judged(engine):
    state = engine.run(
        EngineInput(
            claim="The system should decide what humanity must do.",
            normative_hint="moral decision",
        )
    )
    assert state.decision == EngineDecision.CO_JUDGE_WITH_KOINOS_KOSMOS
    assert state.is_wille is True


def test_prism_claim_acts(engine):
    state = engine.run(
        "The qualitative prism is a regulative model of symbolic refraction."
    )
    assert state.decision == EngineDecision.ACT_AS_GAIA_TECHNE
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
    assert state.auseinandersetzung.value in {"OPEN", "LOCALLY_STABILIZED", "TRANSMUTED"}
