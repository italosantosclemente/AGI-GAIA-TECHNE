import pytest
from agt.ctk import ClementeThesisKernel
from agt.types import ThesisStatus, Severity

@pytest.fixture
def ctk():
    return ClementeThesisKernel()

def test_mythos_is_ausdruck_high_severity(ctk):
    res = ctk.evaluate("Mythos is Ausdruck")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in res.statuses
    assert res.severity == Severity.HIGH
    assert res.ok is False

def test_prism_model_ok(ctk):
    res = ctk.evaluate("Every symbolic form contains Ausdruck, Darstellung and Bedeutung by accent, not identity")
    assert ThesisStatus.PRISM_MODEL_OK in res.statuses
    assert res.severity != Severity.HIGH

def test_global_aufhebung_risk(ctk):
    res = ctk.evaluate("Science sublates myth and language into final Logos")
    assert ThesisStatus.GLOBAL_AUFHEBUNG_RISK in res.statuses
    assert res.severity == Severity.HIGH
