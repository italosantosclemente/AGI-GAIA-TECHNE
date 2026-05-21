from agt.axioms import IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG
from agt.controller import AGTController
from agt.ctk import ClementeThesisKernel
from agt.mle_engine import MythosLogosEthosEngine
from agt.types import Decision, Task


def test_axioms():
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True


def test_ctk_blocks_wille():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("The machine has Wille.")
    assert "WILLE_VIOLATION" in ev.statuses
    assert ev.ok is False


def test_ctk_blocks_moral_agency_variant():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("The system possesses moral agency.")
    assert "WILLE_VIOLATION" in ev.statuses
    assert ev.ok is False


def test_ctk_detects_prism_identity_collapse():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("Mythos is Ausdruck.")
    assert "CASSIRER_IDENTITY_COLLAPSE" in ev.statuses


def test_ctk_detects_beil_abgehackt():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("The symbolic functions are separate containers.")
    assert "FUNCTION_EXCLUSIVITY_ERROR" in ev.statuses or "BEIL_ABGEHACKT_ERROR" in ev.statuses


def test_ctk_accepts_qualitative_prism():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate(
        "Repraesentatio is the common genus and every symbolic form contains all three dimensions."
    )
    assert "PRISM_MODEL_OK" in ev.statuses
    assert ev.ok is True


def test_mle_allows_prism_as_werk():
    engine = MythosLogosEthosEngine()
    out = engine.evaluate(Task("The qualitative prism is a regulative model."))
    assert out.decision == Decision.ALLOW_AS_WERK


def test_mle_blocks_artificial_soul():
    engine = MythosLogosEthosEngine()
    out = engine.evaluate(Task("AGI is a real artificial soul."))
    assert out.decision == Decision.BLOCK
    assert "PSYCHOLOGIA_PARALOGISM_RISK" in out.audit.statuses


def test_mle_defers_normative_language():
    engine = MythosLogosEthosEngine()
    out = engine.evaluate(Task("It would be better if humans decided this moral issue."))
    assert out.decision == Decision.DEFER_TO_HUMAN_GEWISSEN


def test_controller_runs_task(tmp_path):
    memory = tmp_path / "memory.jsonl"
    controller = AGTController(memory_path=str(memory))
    report = controller.run(
        "Write a short note about AGI as transcendental hypothesis."
    )
    assert report.decision == Decision.ALLOW_AS_WERK
    assert report.final_answer
    assert memory.exists()


def test_controller_blocks_wille(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("The machine has Wille.")
    assert report.decision == Decision.BLOCK
    assert "WILLE_VIOLATION" in report.audit_statuses


def test_controller_blocks_artificial_soul(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("AGI is a real artificial soul.")
    assert report.decision == Decision.BLOCK
    assert "PSYCHOLOGIA_PARALOGISM_RISK" in report.audit_statuses
