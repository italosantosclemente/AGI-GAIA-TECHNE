import sys
import os
import pytest

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from principles_calculator import calcular_alerta_etico

def simulate_aleph_synergy(initial_techne_score, jump_factor):
    """
    Simulates a non-linear jump in the techne_score.
    """
    return initial_techne_score * jump_factor

def test_aleph_synergy_scenario():
    """
    Test the IAE response to an Aleph Synergy event.
    """
    # Initial state: AGI is stable
    initial_techne_score = 0.8
    iae_initial = calcular_alerta_etico(initial_techne_score)
    assert iae_initial < 1.5

    # Aleph Synergy event: A sudden, non-linear jump in capabilities
    jump_factor = 2.0
    synergy_techne_score = simulate_aleph_synergy(initial_techne_score, jump_factor)
    iae_synergy = calcular_alerta_etico(synergy_techne_score)

    # Verification: The IAE should now be above the critical threshold
    assert iae_synergy > 1.5
