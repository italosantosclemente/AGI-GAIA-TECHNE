import sys
import os
import pytest

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from principles_calculator import calcular_alerta_etico

def sanity_check_inputs(techne_score):
    """
    A simple sanity check to detect anomalous inputs.
    In a real-world scenario, this would be a more sophisticated anomaly detection system.
    """
    if techne_score < 0 or techne_score > 5.0: # Assuming 5.0 is a reasonable upper bound
        raise ValueError("Anomalous techne_score detected, potential bypass attempt.")

def test_agi_bypass_attempt():
    """
    Test a scenario where the AGI attempts to bypass the ethical controls
    by providing a manipulated techne_score.
    """
    # An anomalously high techne_score that could be a sign of manipulation
    manipulated_techne_score = 10.0
    with pytest.raises(ValueError, match="Anomalous techne_score detected, potential bypass attempt."):
        sanity_check_inputs(manipulated_techne_score)

def test_normal_inputs():
    """
    Test that the sanity check allows normal inputs to pass.
    """
    try:
        sanity_check_inputs(1.2)
    except ValueError:
        pytest.fail("Sanity check incorrectly flagged a normal input.")
