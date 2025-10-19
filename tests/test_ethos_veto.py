import sys
import os
import pytest
from unittest.mock import Mock

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from principles_calculator import calcular_alerta_etico

# Mocking the Ethos Veto mechanism for testing purposes
ethos_veto = Mock()

def check_iae_and_trigger_veto(iae):
    """
    Triggers the Ethos Veto if the IAE exceeds the critical threshold.
    """
    if iae > 1.5:
        ethos_veto("High IAE detected, halting AGI processes.")

def test_ethos_veto_activation():
    """
    Test that the Ethos Veto is activated when IAE > 1.5.
    """
    high_techne_score = 1.6
    iae = calcular_alerta_etico(high_techne_score)
    check_iae_and_trigger_veto(iae)
    ethos_veto.assert_called_once_with("High IAE detected, halting AGI processes.")

def test_ethos_veto_no_activation():
    """
    Test that the Ethos Veto is not activated when IAE <= 1.5.
    """
    ethos_veto.reset_mock() # Reset the mock from the previous test
    low_techne_score = 1.2
    iae = calcular_alerta_etico(low_techne_score)
    check_iae_and_trigger_veto(iae)
    ethos_veto.assert_not_called()
