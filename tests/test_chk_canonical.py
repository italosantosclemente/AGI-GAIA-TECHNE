import pytest
from agt.chk import ChirimuutaHapticKernel
from agt.types import ThesisStatus, Severity

@pytest.fixture
def chk():
    return ChirimuutaHapticKernel()

def test_machine_organism_analogy(chk):
    res = chk.evaluate("The brain is literally a computer")
    assert ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK in res.statuses

def test_haptic_model_ok(chk):
    res = chk.evaluate("This is a haptic model with abstraction cost and medium dependence")
    assert ThesisStatus.HAPTIC_MODEL_OK in res.statuses
    assert res.severity != Severity.HIGH

def test_prediction_without_understanding(chk):
    res = chk.evaluate("Benchmark performance proves understanding")
    assert ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING in res.statuses
