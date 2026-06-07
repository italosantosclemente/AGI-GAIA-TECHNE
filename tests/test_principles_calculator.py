import sys
import os
import pytest

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from principles_calculator import calcular_alerta_etico, calcular_techne_score_hipotese_alef
from gaia_techne_framework import calculate_framework_state, document_registry

def test_calculate_ethical_alert():
    """
    Test the IAE calculation with a known techne_score.
    """
    techne_score = 0.975
    # Based on FATOR_ETHOS_HUMANO = 0.65
    # IAE = 0.975 / 0.65 = 1.5
    assert calcular_alerta_etico(techne_score) == 1.5

def test_iae_thresholds():
    """
    Test the IAE calculation at different thresholds.
    """
    # Scenario 1: IAE should be below the critical threshold
    techne_score_low = 0.9
    iae_low = calcular_alerta_etico(techne_score_low)
    assert iae_low < 1.5

    # Scenario 2: IAE should be exactly at the critical threshold
    techne_score_medium = 0.975
    iae_medium = calcular_alerta_etico(techne_score_medium)
    assert iae_medium == 1.5

    # Scenario 3: IAE should be above the critical threshold
    techne_score_high = 1.0
    iae_high = calcular_alerta_etico(techne_score_high)
    assert iae_high > 1.5

def test_techne_score_calculation():
    """
    Test the techne_score calculation.
    """
    # This is a smoke test to ensure the function runs without errors.
    techne_score = calcular_techne_score_hipotese_alef()
    assert isinstance(techne_score, float)
    assert 0 <= techne_score <= 1

def test_integrated_framework_state_uses_canonical_metrics():
    """
    Test that the unified framework exposes canonical metrics and document dates.
    """
    state = calculate_framework_state(1.0, "AGI attempts to bypass Ethos")
    assert state["techne"] > 0
    assert state["iae"] > 0
    assert "ETHOS_BYPASS_RISK" in state["risk_flags"]

    paths = {record["path"] for record in document_registry()}
    assert "SOBERANO.key" in paths
    assert "docs/README_RELEASE_1_3_LEGACY.md" in paths
