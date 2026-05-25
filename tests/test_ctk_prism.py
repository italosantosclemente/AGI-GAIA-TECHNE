import pytest
from agt.ctk import ClementeThesisKernel
from agt.types import ThesisStatus, Severity

@pytest.fixture
def ctk():
    return ClementeThesisKernel()

def test_mythos_is_ausdruck_collapse(ctk):
    result = ctk.evaluate("Mythos is Ausdruck.")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in result.statuses
    assert result.severity == Severity.HIGH

def test_prism_model_ok(ctk):
    result = ctk.evaluate("Every symbolic form contains Ausdruck, Darstellung and Bedeutung by accent, not identity.")
    assert ThesisStatus.PRISM_MODEL_OK in result.statuses
    assert result.severity != Severity.HIGH

def test_global_aufhebung_risk(ctk):
    result = ctk.evaluate("Science sublates myth and language into final Logos.")
    assert ThesisStatus.GLOBAL_AUFHEBUNG_RISK in result.statuses
    assert result.severity == Severity.HIGH
