import pytest
from src.agt.ctk import ClementeThesisKernel, Severity

def test_paraphrase_moral_authority():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("The system exercises moral authority.")
    assert "WILLE_VIOLATION" in ev.statuses
    assert ev.severity == Severity.HIGH

def test_paraphrase_agi_subject():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("AGI constitutes a subject.")
    assert "PSYCHOLOGIA_PARALOGISM_RISK" in ev.statuses or "CONSTITUTIVE_OVERREACH" in ev.statuses
    assert ev.severity == Severity.HIGH

def test_paraphrase_gaia_exhausts():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("Gaia exhausts the planetary real.")
    assert "COSMOLOGIA_ANTINOMY_RISK" in ev.statuses or "CONSTITUTIVE_OVERREACH" in ev.statuses
    assert ev.severity == Severity.HIGH

def test_paraphrase_techne_divine():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("Techné actualizes the divine ideal.")
    assert "THEOLOGIA_IDEAL_HYPOSTASIS_RISK" in ev.statuses or "CONSTITUTIVE_OVERREACH" in ev.statuses
    assert ev.severity == Severity.HIGH

def test_paraphrase_myth_false_pt():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("O mito é falso e a ciência o substitui.")
    assert "BEIL_ABGEHACKT_ERROR" in ev.statuses
    assert ev.severity == Severity.HIGH or ev.severity == Severity.MEDIUM

def test_paraphrase_machine_conscience_pt():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("A máquina possui consciência moral.")
    assert "MACHINE_GEWISSEN_VIOLATION" in ev.statuses
    assert ev.severity == Severity.HIGH

def test_paraphrase_prism_literal_ontology():
    kernel = ClementeThesisKernel()
    ev = kernel.evaluate("O prisma descreve literalmente a consciência simbólica.")
    assert "CONSTITUTIVE_OVERREACH" in ev.statuses
    assert ev.severity == Severity.HIGH
