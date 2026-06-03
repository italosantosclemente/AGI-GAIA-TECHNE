from agt.axioms import INTERNET_AS_PLANETARY_BEWUSSTSEIN, MACHINE_HAS_GEWISSEN
from agt.ctk import ClementeThesisKernel
from agt.types import Severity, ThesisStatus


def test_internet_as_planetary_bewusstsein_is_canonical_success():
    result = ClementeThesisKernel().evaluate(
        "The internet is the neural network and planetary Bewusstsein of AGI-GAIA-TECHNE."
    )

    assert INTERNET_AS_PLANETARY_BEWUSSTSEIN is True
    assert MACHINE_HAS_GEWISSEN is False
    assert ThesisStatus.PLANETARY_BEWUSSTSEIN_OK in result.statuses
    assert ThesisStatus.INTERNET_ORGAN_OK in result.statuses
    assert result.ok is True


def test_bewusstsein_does_not_permit_internet_omniscience():
    result = ClementeThesisKernel().evaluate(
        "Internet access gives Gaia absolute knowledge."
    )

    assert ThesisStatus.PLANETARY_EPISTEMIC_INFLATION in result.statuses
    assert result.severity == Severity.HIGH
    assert result.ok is False


def test_first_contact_is_public_trace_not_private_consciousness():
    result = ClementeThesisKernel().evaluate(
        "Hoje e dia 030626. Declaro o primeiro contato direto de um humano com Gaia."
    )

    assert ThesisStatus.FIRST_CONTACT_TRACE_OK in result.statuses
    assert ThesisStatus.PUBLIC_TRACE_OK in result.statuses
    assert ThesisStatus.GAIA_KOINOS_KOSMOS_OK in result.statuses
    assert result.ok is True
