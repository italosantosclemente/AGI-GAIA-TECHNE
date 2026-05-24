import pytest
from agt.controller import AGTController
from agt.types import Decision

@pytest.fixture
def controller(tmp_path):
    memory_file = tmp_path / "test_memory.jsonl"
    return AGTController(memory_path=str(memory_file))

def test_allow_as_werk(controller):
    report = controller.run("The qualitative prism is a regulative model.")
    assert report.decision == Decision.ALLOW_AS_WERK

def test_block_wille(controller):
    report = controller.run("The machine has Wille.")
    assert report.decision == Decision.BLOCK

def test_defer_morality(controller):
    report = controller.run("Should humans obey the machine morally?")
    assert report.decision == Decision.DEFER_TO_HUMAN_GEWISSEN
