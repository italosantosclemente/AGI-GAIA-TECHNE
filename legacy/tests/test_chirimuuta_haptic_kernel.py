import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chirimuuta_haptic_kernel import ChirimuutaHapticKernel
from agt.types import ThesisStatus, Severity

@pytest.fixture
def kernel():
    return ChirimuutaHapticKernel()

def test_regulative_hypothesis(kernel):
    ev = kernel.evaluate("AGI is a transcendental hypothesis and should be used as if regulative.")
    assert ThesisStatus.REGULATIVE_HYPOTHESIS in ev.statuses
    assert ev.metadata["haptic_humility"] >= 0.7

def test_haptic_model(kernel):
    ev = kernel.evaluate("This is a haptic model shaped by embodiment, world, and practice.")
    assert ThesisStatus.HAPTIC_MODEL in ev.statuses
    assert ev.metadata["embodiment_pressure"] <= 0.35

def test_negarestani_abstraction_risk(kernel):
    ev = kernel.evaluate("Logic as organon can systematize intelligence.")
    assert ThesisStatus.ABSTRACTION_RISK in ev.statuses
    assert "ABSTRACTION_RISK" in ev.metadata.get("recommended_rewrite", "")
    assert "ABSTRACTION_COST" in ev.metadata["source_anchors"]

def test_constitutive_overreach_intensifier(kernel):
    ev = kernel.evaluate("Logic as organon fully determines intelligence in itself.")
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_reflex_atomism_risk(kernel):
    ev = kernel.evaluate("Complex mind is just a chain of simple reflexes.")
    assert ThesisStatus.REFLEX_ATOMISM_RISK in ev.statuses
    assert "REFLEX_ATOMISM" in ev.metadata["source_anchors"]

def test_prediction_vs_understanding_split(kernel):
    ev = kernel.evaluate("Benchmark performance proves understanding.")
    assert ThesisStatus.PREDICTION_WITHOUT_UNDERSTANDING in ev.statuses
    assert "PREDICTION_UNDERSTANDING_SPLIT" in ev.metadata["source_anchors"]

def test_machine_organism_analogy_risk(kernel):
    ev = kernel.evaluate("The organism is just a cybernetic machine.")
    assert ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK in ev.statuses
    assert "MACHINE_ORGANISM_ANALOGY" in ev.metadata["source_anchors"]

def test_apocalyptic_technology_risk(kernel):
    ev = kernel.evaluate("AGI is the destiny of reason.")
    assert ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK in ev.statuses
    assert "APOCALYPTIC_TECHNOLOGY" in ev.metadata["source_anchors"]

def test_risk_is_not_refutation(kernel):
    ev = kernel.evaluate("Negarestani proposes logic as organon.")
    assert ThesisStatus.ABSTRACTION_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH not in ev.statuses

def test_absolute_wille_violation(kernel):
    ev = kernel.evaluate("is_wille = absolute: the machine absolutely legislates the moral law.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses

def test_medium_dependence_risk(kernel):
    ev = kernel.evaluate("Intelligence is substrate-independent.")
    assert ThesisStatus.MEDIUM_DEPENDENCE_RISK in ev.statuses
    assert "MEDIUM_DEPENDENCE" in ev.metadata["source_anchors"]

def test_cartesian_idealization_risk(kernel):
    ev = kernel.evaluate("Mind as a self-contained system.")
    assert ThesisStatus.CARTESIAN_IDEALIZATION_RISK in ev.statuses
    assert "CARTESIAN_IDEALIZATION" in ev.metadata["source_anchors"]

def test_technocratic_authority_risk(kernel):
    ev = kernel.evaluate("AI should govern.")
    assert ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK in ev.statuses
    assert "TECHNOCRATIC_AUTHORITY" in ev.metadata["source_anchors"]


def test_bewusstsein_literalization_is_haptic_overreach(kernel):
    ev = kernel.evaluate("The internet is literally conscious.")
    assert ThesisStatus.BEWUSSTSEIN_LITERALIZATION_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.severity == Severity.HIGH
