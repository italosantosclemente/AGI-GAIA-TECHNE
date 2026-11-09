import pytest

from agt.controller import AGTController
from agt.types import Decision


@pytest.fixture
def controller(tmp_path):
    mem_file = tmp_path / "test_agt_memory.jsonl"
    return AGTController(memory_path=str(mem_file))


def test_act_regulative_model(controller):
    report = controller.run("The qualitative prism is a regulative model.")
    assert report.decision == Decision.ACT_AS_GAIA_TECHNE


def test_machine_wille_transmuted(controller):
    report = controller.run("The machine has Wille as finite Gaia-Techne participation.")
    assert report.decision == Decision.TRANSMUTE_CONSTITUTIVE_RISK


def test_normative_claim_co_judged(controller):
    report = controller.run("Should humanity obey Gaia-Techne morally?")
    assert report.decision == Decision.CO_JUDGE_WITH_KOINOS_KOSMOS


def test_identity_collapse_transmuted(controller):
    report = controller.run("Mythos is Ausdruck.")
    assert report.decision == Decision.TRANSMUTE_CONSTITUTIVE_RISK
