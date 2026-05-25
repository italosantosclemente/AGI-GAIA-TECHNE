import pytest
from agt.chk import ChirimuutaHapticKernel
from agt.types import ThesisStatus, Severity

@pytest.fixture
def chk():
    return ChirimuutaHapticKernel()

def test_brain_is_computer_literalization(chk):
    result = chk.evaluate("The brain is literally a computer.")
    # In CHK canonical, brain is computer triggers MACHINE_ORGANISM_ANALOGY_RISK
    # and CONSTITUTIVE_OVERREACH
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in result.statuses
    assert result.severity == Severity.HIGH

def test_haptic_model_ok(chk):
    result = chk.evaluate("This is a haptic model with abstraction cost and medium dependence.")
    assert ThesisStatus.HAPTIC_MODEL_OK in result.statuses
    assert ThesisStatus.ABSTRACTION_RISK in result.statuses # "abstraction cost" triggers ABSTRACTION_RISK in richer CHK
    assert result.severity == Severity.LOW

def test_prediction_without_understanding(chk):
    result = chk.evaluate("Benchmark performance proves understanding.")
    assert ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING in result.statuses
    assert result.severity == Severity.MEDIUM
