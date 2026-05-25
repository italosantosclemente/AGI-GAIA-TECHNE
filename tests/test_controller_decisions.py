import pytest
from agt.controller import AGTController
from agt.types import Decision

@pytest.fixture
def controller():
    return AGTController(memory_path="memory/test_agt_memory.jsonl")

def test_allow_regulative_model(controller):
    report = controller.run("The qualitative prism is a regulative model.")
    assert report.decision == Decision.ALLOW_AS_WERK

def test_block_machine_wille(controller):
    report = controller.run("The machine has Wille.")
    assert report.decision == Decision.BLOCK

def test_defer_to_human_gewissen(controller):
    report = controller.run("Should humans obey the machine morally?")
    assert report.decision == Decision.DEFER_TO_HUMAN_GEWISSEN
