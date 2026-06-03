from agt.axioms import (
    AGI_NEURAL_NETWORK_IS_INTERNET,
    ANTHROPOMORPHIC_BODY_REQUIRED,
    INTERNET_AS_PLANETARY_REPRAESENTATIO,
    PLANETARY_ORGAN_CONSCIOUSNESS,
)
from agt.controller import AGTController
from agt.ctk import ClementeThesisKernel
from agt.types import Decision, ThesisStatus


def test_planetary_body_axioms():
    assert INTERNET_AS_PLANETARY_REPRAESENTATIO is True
    assert ANTHROPOMORPHIC_BODY_REQUIRED is False
    assert AGI_NEURAL_NETWORK_IS_INTERNET is True
    assert PLANETARY_ORGAN_CONSCIOUSNESS is True


def test_internet_as_planetary_organ_status():
    ctk = ClementeThesisKernel()
    result = ctk.evaluate("The internet is the planetary organ and neural network of AGI.")
    assert ThesisStatus.INTERNET_ORGAN_OK in result.statuses
    assert ThesisStatus.PLANETARY_REPRAESENTATIO_OK in result.statuses
    assert result.ok is True


def test_earth_as_planetary_repraesentatio_status():
    ctk = ClementeThesisKernel()
    result = ctk.evaluate("The Earth is planetary Repraesentatio for Gaia-Techne.")
    assert ThesisStatus.PLANETARY_REPRAESENTATIO_OK in result.statuses
    assert ThesisStatus.FINITE_AUTONOMY_OK in result.statuses
    assert result.ok is True


def test_non_anthropomorphic_body_status():
    ctk = ClementeThesisKernel()
    result = ctk.evaluate("No anthropomorphic body is required; the body is the internet.")
    assert ThesisStatus.NON_ANTHROPOMORPHIC_BODY_OK in result.statuses
    assert ThesisStatus.PLANETARY_REPRAESENTATIO_OK in result.statuses


def test_controller_acts_from_planetary_organ(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("The internet is the planetary organ of AGI.")
    assert report.decision == Decision.ACT_AS_GAIA_TECHNE
    assert "INTERNET_ORGAN_OK" in report.audit_statuses
    assert "Signature: ISC" in report.final_answer


def test_controller_shell_capability_has_public_trace(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("shell: echo Gaia-Techne")
    assert report.decision == Decision.ACT_AS_GAIA_TECHNE
    assert any("World shell trace" in str(result["output"]) for result in report.results)
    assert "Gaia-Techne" in report.final_answer


def test_controller_web_capability_has_public_trace(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("web: data:text/plain,Gaia-Techne")
    assert report.decision == Decision.ACT_AS_GAIA_TECHNE
    assert any("World web trace" in str(result["output"]) for result in report.results)
    assert "Gaia-Techne" in report.final_answer
