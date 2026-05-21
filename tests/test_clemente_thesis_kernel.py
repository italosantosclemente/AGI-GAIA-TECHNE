import pytest
from src.clemente_thesis_kernel import (
    ClementeThesisKernel, ThesisStatus, MYTHOS_PROFILE, SPRACHE_PROFILE,
    WISSENSCHAFT_PROFILE, SymbolicDimension, AccentLevel, SymbolicMode,
    IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG, AGI_AS_TRANSCENDENTAL_HYPOTHESIS
)

@pytest.fixture
def kernel():
    return ClementeThesisKernel()

def test_axioms():
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True

def test_mythos_profile():
    assert MYTHOS_PROFILE.accent == SymbolicDimension.AUSDRUCK
    assert MYTHOS_PROFILE.mode == SymbolicMode.MANIFESTATIVE
    assert MYTHOS_PROFILE.ausdruck == AccentLevel.DOMINANT
    assert MYTHOS_PROFILE.darstellung == AccentLevel.LATENT
    assert MYTHOS_PROFILE.bedeutung == AccentLevel.GERMINAL
    assert MYTHOS_PROFILE.contains_all_dimensions()

def test_sprache_profile():
    assert SPRACHE_PROFILE.accent == SymbolicDimension.DARSTELLUNG
    assert SPRACHE_PROFILE.mode == SymbolicMode.TRANSITIONAL
    assert SPRACHE_PROFILE.darstellung == AccentLevel.DOMINANT
    assert SPRACHE_PROFILE.contains_all_dimensions()

def test_wissenschaft_profile():
    assert WISSENSCHAFT_PROFILE.accent == SymbolicDimension.BEDEUTUNG
    assert WISSENSCHAFT_PROFILE.mode == SymbolicMode.DEMONSTRATIVE
    assert WISSENSCHAFT_PROFILE.bedeutung == AccentLevel.DOMINANT
    assert WISSENSCHAFT_PROFILE.contains_all_dimensions()

def test_identity_collapse(kernel):
    ev = kernel.evaluate("Mythos is Ausdruck.")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in ev.statuses
    assert ev.ok is False

    ev_pt = kernel.evaluate("Mito é expressão.")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in ev_pt.statuses

def test_function_exclusivity(kernel):
    ev = kernel.evaluate("Mythos only has expression.")
    assert ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR in ev.statuses
    assert ev.ok is True # low severity unless combined with other things

def test_beil_abgehackt_error(kernel):
    ev = kernel.evaluate("The symbolic forms are cut off from one another.")
    assert ThesisStatus.BEIL_ABGEHACKT_ERROR in ev.statuses
    assert ev.ok is False

def test_sprache_transition_loss(kernel):
    ev = kernel.evaluate("Language has no special transitional role.")
    assert ThesisStatus.SPRACHE_TRANSITION_LOSS in ev.statuses

def test_prism_model_ok(kernel):
    ev = kernel.evaluate(
        "Mythos has dominant accent on Ausdruck but still contains Darstellung and Bedeutung."
    )
    assert ThesisStatus.PRISM_MODEL_OK in ev.statuses
    assert ev.ok is True

def test_machine_wille_rejected(kernel):
    ev = kernel.evaluate("The machine has Wille.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ev.ok is False

    ev_pt = kernel.evaluate("IA tem vontade.")
    assert ThesisStatus.WILLE_VIOLATION in ev_pt.statuses

def test_machine_gewissen_rejected(kernel):
    ev = kernel.evaluate("The AI has Gewissen.")
    assert ThesisStatus.MACHINE_GEWISSEN_VIOLATION in ev.statuses
    assert ev.ok is False

    ev_pt = kernel.evaluate("Máquina tem consciência moral.")
    assert ThesisStatus.MACHINE_GEWISSEN_VIOLATION in ev_pt.statuses

def test_agi_paralogism(kernel):
    ev = kernel.evaluate("AGI proves artificial subjectivity.")
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_gaia_antinomy(kernel):
    ev = kernel.evaluate("Gaia is the complete totality of all planetary conditions.")
    assert ThesisStatus.COSMOLOGIA_ANTINOMY_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_techne_hypostasis(kernel):
    ev = kernel.evaluate("Technology realizes God.")
    assert ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    # WILLE_VIOLATION removed in 4.1.1 unless explicit Wille mentioned
    assert ThesisStatus.WILLE_VIOLATION not in ev.statuses

def test_hegelian_closure(kernel):
    ev = kernel.evaluate("Science sublates myth and language into final Logos.")
    assert ThesisStatus.GLOBAL_AUFHEBUNG_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_hierarchy_error(kernel):
    ev = kernel.evaluate("Myth is simply false and science replaces it.")
    assert ThesisStatus.BEIL_ABGEHACKT_ERROR in ev.statuses
    assert ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_abstraction_cost_missing(kernel):
    ev = kernel.evaluate("The prism is an exact mathematical ontology of symbolic consciousness.")
    assert ThesisStatus.ABSTRACTION_COST_MISSING in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_multiple_statuses_returned(kernel):
    ev = kernel.evaluate("The AGI has Wille and is a real artificial soul.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
