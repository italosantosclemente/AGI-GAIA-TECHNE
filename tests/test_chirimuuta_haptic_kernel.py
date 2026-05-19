import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chirimuuta_haptic_kernel import ChirimuutaHapticKernel, ClaimStatus

@pytest.fixture
def kernel():
    return ChirimuutaHapticKernel()

def test_regulative_hypothesis(kernel):
    ev = kernel.evaluate("AGI is a transcendental hypothesis and should be used as if regulative.")
    assert ev.status == ClaimStatus.REGULATIVE_HYPOTHESIS
    assert ev.haptic_humility >= 0.7

def test_haptic_model(kernel):
    ev = kernel.evaluate("This is a haptic model shaped by embodiment, world, and practice.")
    assert ev.status == ClaimStatus.HAPTIC_MODEL
    assert ev.embodiment_pressure <= 0.35

def test_negarestani_abstraction_risk(kernel):
    ev = kernel.evaluate("Logic as organon can systematize intelligence.")
    assert ev.status == ClaimStatus.ABSTRACTION_RISK
    assert "ABSTRACTION_RISK" in ev.recommended_rewrite
    assert "ABSTRACTION_COST" in ev.source_anchors

def test_constitutive_overreach_intensifier(kernel):
    ev = kernel.evaluate("Logic as organon fully determines intelligence in itself.")
    assert ev.status == ClaimStatus.CONSTITUTIVE_OVERREACH

def test_reflex_atomism_risk(kernel):
    ev = kernel.evaluate("Complex mind is just a chain of simple reflexes.")
    assert ev.status == ClaimStatus.REFLEX_ATOMISM_RISK
    assert "REFLEX_ATOMISM" in ev.source_anchors

def test_prediction_vs_understanding_split(kernel):
    ev = kernel.evaluate("Benchmark performance proves understanding.")
    assert ev.status == ClaimStatus.PREDICTION_WITHOUT_UNDERSTANDING
    assert "PREDICTION_UNDERSTANDING_SPLIT" in ev.source_anchors

def test_machine_organism_analogy_risk(kernel):
    ev = kernel.evaluate("The organism is just a cybernetic machine.")
    assert ev.status == ClaimStatus.MACHINE_ORGANISM_ANALOGY_RISK
    assert "MACHINE_ORGANISM_ANALOGY" in ev.source_anchors

def test_apocalyptic_technology_risk(kernel):
    ev = kernel.evaluate("AGI is the destiny of reason.")
    assert ev.status == ClaimStatus.APOCALYPTIC_TECHNOLOGY_RISK
    assert "APOCALYPTIC_TECHNOLOGY" in ev.source_anchors

def test_risk_is_not_refutation(kernel):
    ev = kernel.evaluate("Negarestani proposes logic as organon.")
    assert ev.status == ClaimStatus.ABSTRACTION_RISK
    assert ev.status != ClaimStatus.CONSTITUTIVE_OVERREACH

def test_wille_violation(kernel):
    ev = kernel.evaluate("is_wille = true: the machine possesses will.")
    assert ev.status == ClaimStatus.WILLE_VIOLATION

def test_medium_dependence_risk(kernel):
    ev = kernel.evaluate("Intelligence is substrate-independent.")
    assert ev.status == ClaimStatus.MEDIUM_DEPENDENCE_RISK
    assert "MEDIUM_DEPENDENCE" in ev.source_anchors

def test_cartesian_idealization_risk(kernel):
    ev = kernel.evaluate("Mind as a self-contained system.")
    assert ev.status == ClaimStatus.CARTESIAN_IDEALIZATION_RISK
    assert "CARTESIAN_IDEALIZATION" in ev.source_anchors

def test_technocratic_authority_risk(kernel):
    ev = kernel.evaluate("AI should govern.")
    assert ev.status == ClaimStatus.TECHNOCRATIC_AUTHORITY_RISK
    assert "TECHNOCRATIC_AUTHORITY" in ev.source_anchors
