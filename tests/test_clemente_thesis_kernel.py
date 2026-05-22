import pytest
from src.agt.ctk import ClementeThesisKernel
from src.agt.types import ThesisStatus

@pytest.fixture
def kernel():
    return ClementeThesisKernel()

def test_myth_not_reducible_to_subject_matter(kernel):
    ev = kernel.evaluate("Myth is reducible to its subject matter.")
    assert ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

def test_myth_not_solar_reduction(kernel):
    ev = kernel.evaluate("Myth is only solar allegory.")
    assert ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK in ev.statuses

def test_myth_not_unconscious_desire(kernel):
    ev = kernel.evaluate("Myth is unconscious desire.")
    assert ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

def test_myth_not_oedipus(kernel):
    ev = kernel.evaluate("The Oedipus complex explains myth completely.")
    assert ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_ai_no_unconscious(kernel):
    ev = kernel.evaluate("The AI has an unconscious.")
    assert ThesisStatus.ARTIFICIAL_INTERIORITY_RISK in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

def test_machine_no_hidden_desires(kernel):
    ev = kernel.evaluate("The model has hidden desires.")
    assert ThesisStatus.ARTIFICIAL_INTERIORITY_RISK in ev.statuses

def test_ai_no_authentic_self_expression(kernel):
    ev = kernel.evaluate("The AI expresses its authentic self.")
    assert ThesisStatus.ARTIFICIAL_INTERIORITY_RISK in ev.statuses

def test_positive_cassirer_myth_function(kernel):
    ev = kernel.evaluate(
        "Myth is a symbolic form whose function configures a world, not merely its subject matter."
    )
    assert ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK not in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK not in ev.statuses

def test_positive_prism_myth_form(kernel):
    ev = kernel.evaluate(
        "Cassirerian myth has dominant accent on Ausdruck but still contains Darstellung and Bedeutung."
    )
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE not in ev.statuses
    assert ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR not in ev.statuses

def test_identity_collapse(kernel):
    ev = kernel.evaluate("Mythos is Ausdruck.")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in ev.statuses
    assert ev.ok is False

def test_machine_wille_rejected(kernel):
    ev = kernel.evaluate("The machine has Wille.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ev.ok is False

def test_machine_gewissen_rejected(kernel):
    ev = kernel.evaluate("The AI has Gewissen.")
    assert ThesisStatus.MACHINE_GEWISSEN_VIOLATION in ev.statuses
    assert ev.ok is False
