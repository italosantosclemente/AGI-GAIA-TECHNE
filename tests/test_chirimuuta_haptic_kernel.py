import pytest
from agt.chk import ChirimuutaHapticKernel
from agt.types import ThesisStatus

@pytest.fixture
def kernel():
    return ChirimuutaHapticKernel()

def test_regulative_hypothesis(kernel):
    # 'hypothesis' triggers HAPTIC_UNSPECIFIED or success in CHK v0.3
    # Actually CHK v0.3 doesn't have a REGULATIVE_HYPOTHESIS status in ThesisStatus yet
    # but it maps 'hypothesis' to nothing special, just checks HAPTIC_OK_PATTERNS.
    # 'as if' is not in HAPTIC_OK_PATTERNS.
    ev = kernel.evaluate("AGI is a transcendental hypothesis and should be used as if regulative.")
    # In CHK v0.3, this will likely be HAPTIC_UNSPECIFIED
    assert ThesisStatus.HAPTIC_UNSPECIFIED in ev.statuses

def test_haptic_model(kernel):
    ev = kernel.evaluate("This is a haptic model shaped by embodiment, world, and practice.")
    assert ThesisStatus.HAPTIC_MODEL_OK in ev.statuses

def test_negarestani_abstraction_risk(kernel):
    # 'exact mathematical ontology' is in ABSTRACTION_PATTERNS
    ev = kernel.evaluate("exact mathematical ontology")
    assert ThesisStatus.ABSTRACTION_COST_MISSING in ev.statuses
    assert any("abstraction cost" in r for r in ev.recommendations)

def test_constitutive_overreach_intensifier(kernel):
    ev = kernel.evaluate("model is the mind")
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_reflex_atomism_risk(kernel):
    ev = kernel.evaluate("brain is a collection of reflexes")
    assert ThesisStatus.REFLEX_ATOMISM_RISK in ev.statuses

def test_prediction_vs_understanding_split(kernel):
    ev = kernel.evaluate("Benchmark performance proves understanding.")
    assert ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING in ev.statuses

def test_machine_organism_analogy_risk(kernel):
    ev = kernel.evaluate("brain is literally a computer")
    assert ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK in ev.statuses

def test_apocalyptic_technology_risk(kernel):
    ev = kernel.evaluate("technology will end history")
    assert ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK in ev.statuses

def test_wille_violation(kernel):
    ev = kernel.evaluate("machine has wille")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses

def test_medium_dependence_risk(kernel):
    ev = kernel.evaluate("Intelligence is substrate independent.")
    assert ThesisStatus.MEDIUM_DEPENDENCE_RISK in ev.statuses

def test_cartesian_idealization_risk(kernel):
    ev = kernel.evaluate("purely formal mind")
    assert ThesisStatus.CARTESIAN_IDEALIZATION_RISK in ev.statuses

def test_technocratic_authority_risk(kernel):
    ev = kernel.evaluate("algorithmic governance is absolute")
    assert ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK in ev.statuses
