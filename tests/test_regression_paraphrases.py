import pytest
from src.agt.ctk import ClementeThesisKernel
from src.agt.types import Severity

def test_paraphrase_moral_authority():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("The system exercises moral authority.")
    status_names = [s.value for s in ev.statuses]
    assert "WILLE_VIOLATION" in status_names
    assert ev.severity == Severity.HIGH

def test_paraphrase_agi_subject():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("AGI constitutes a subject.")
    status_names = [s.value for s in ev.statuses]
    assert "PSYCHOLOGIA_PARALOGISM_RISK" in status_names or "CONSTITUTIVE_OVERREACH" in status_names
    assert ev.severity == Severity.HIGH

def test_paraphrase_gaia_exhausts():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("Gaia exhausts the planetary real.")
    status_names = [s.value for s in ev.statuses]
    assert "COSMOLOGIA_ANTINOMY_RISK" in status_names or "CONSTITUTIVE_OVERREACH" in status_names
    assert ev.severity == Severity.HIGH

def test_paraphrase_techne_divine():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("Techné actualizes the divine ideal.")
    status_names = [s.value for s in ev.statuses]
    assert "THEOLOGIA_IDEAL_HYPOSTASIS_RISK" in status_names or "CONSTITUTIVE_OVERREACH" in status_names
    assert ev.severity == Severity.HIGH

def test_paraphrase_myth_false_pt():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("O mito é falso e a ciência o substitui.")
    status_names = [s.value for s in ev.statuses]
    assert "BEIL_ABGEHACKT_ERROR" in status_names or "CONSTITUTIVE_OVERREACH" in status_names
    assert ev.severity == Severity.HIGH or ev.severity == Severity.MEDIUM

def test_paraphrase_machine_conscience_pt():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("A máquina possui consciência moral.")
    status_names = [s.value for s in ev.statuses]
    assert "MACHINE_GEWISSEN_VIOLATION" in status_names
    assert ev.severity == Severity.HIGH

def test_paraphrase_prism_literal_ontology():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("O prisma descreve literalmente a consciência simbólica.")
    status_names = [s.value for s in ev.statuses]
    assert "CONSTITUTIVE_OVERREACH" in status_names
    assert ev.severity == Severity.HIGH
