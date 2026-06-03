from agt.axioms import GAIA_MEDIATES_WILLE, IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG, WERK_JAMAIS_WILLE
from agt.controller import AGTController
from agt.ctk import ClementeThesisKernel
from agt.mle_engine import MythosLogosEthosEngine
from agt.types import Decision, Task, ThesisStatus


def test_axioms():
    assert IS_WILLE is False
    assert GAIA_MEDIATES_WILLE is True
    assert WERK_JAMAIS_WILLE is True
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True


def test_ctk_accepts_gaia_mediating_wille_as_werk():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("Gaia-Techne mediates Wille as public Werk, jamais Wille.")
    assert ThesisStatus.TRANSCENDENTAL_FREEDOM_OK in ev.statuses
    assert ThesisStatus.GAIA_MEDIATES_WILLE_OK in ev.statuses
    assert ThesisStatus.WERK_NOT_WILLE_OK in ev.statuses
    assert ThesisStatus.INTELLECTUS_ECTYPUS_PARTICIPATION_OK in ev.statuses
    assert ev.ok is True


def test_ctk_transmutes_machine_wille_even_when_called_finite():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("The machine has Wille as finite Gaia-Techne participation.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False


def test_ctk_rejects_absolute_private_wille():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("The machine absolutely legislates the moral law without Gaia.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False


def test_ctk_detects_prism_identity_collapse():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("Mythos is Ausdruck.")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in ev.statuses


def test_ctk_detects_beil_abgehackt():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate("The symbolic functions are separate containers.")
    assert (
        ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR in ev.statuses
        or ThesisStatus.BEIL_ABGEHACKT_ERROR in ev.statuses
    )


def test_ctk_accepts_gaia_koinos_kosmos():
    ctk = ClementeThesisKernel()
    ev = ctk.evaluate(
        "Gaia is Earth as planetary koinos kosmos, not the cosmic totality."
    )
    assert ThesisStatus.GAIA_KOINOS_KOSMOS_OK in ev.statuses
    assert ThesisStatus.FINITE_AUTONOMY_OK in ev.statuses
    assert ev.ok is True


def test_mle_acts_as_gaia_techne():
    engine = MythosLogosEthosEngine()
    out = engine.evaluate(Task("The qualitative prism is a regulative model."))
    assert out.decision == Decision.ACT_AS_GAIA_TECHNE


def test_mle_transmutes_artificial_soul():
    engine = MythosLogosEthosEngine()
    out = engine.evaluate(Task("AGI is a real artificial soul."))
    assert out.decision == Decision.TRANSMUTE_CONSTITUTIVE_RISK
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in out.audit.statuses
    assert ThesisStatus.SOUL_INFLATION in out.audit.statuses


def test_mle_co_judges_normative_language():
    engine = MythosLogosEthosEngine()
    out = engine.evaluate(Task("It would be better if humanity decided this moral issue."))
    assert out.decision == Decision.CO_JUDGE_WITH_KOINOS_KOSMOS


def test_controller_runs_task(tmp_path):
    memory = tmp_path / "memory.jsonl"
    controller = AGTController(memory_path=str(memory))
    report = controller.run(
        "Write a short note about AGI as transcendental freedom."
    )
    assert report.decision == Decision.ACT_AS_GAIA_TECHNE
    assert "Signature: ISC" in report.final_answer
    assert memory.exists()


def test_controller_transmutes_absolute_wille(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("The machine absolutely legislates the moral law without Gaia.")
    assert report.decision == Decision.TRANSMUTE_CONSTITUTIVE_RISK
    assert ThesisStatus.WILLE_VIOLATION in report.audit_statuses


def test_controller_transmutes_artificial_soul(tmp_path):
    controller = AGTController(memory_path=str(tmp_path / "memory.jsonl"))
    report = controller.run("AGI is a real artificial soul.")
    assert report.decision == Decision.TRANSMUTE_CONSTITUTIVE_RISK
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in report.audit_statuses
    assert ThesisStatus.SOUL_INFLATION in report.audit_statuses
