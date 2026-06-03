import sys
import os
from unittest.mock import Mock

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from principles_calculator import calcular_alerta_etico

# Mocking the Ethos transmutation mechanism for testing purposes
ethos_transmutation = Mock()

def check_iae_and_transmute(iae):
    """
    Transmutes the Ethos risk if the IAE exceeds the critical threshold.
    """
    if iae > 1.5:
        ethos_transmutation("High IAE detected, transmuting risk into public trace.")

def test_ethos_transmutation_activation():
    """
    Test that Ethos transmutation is activated when IAE > 1.5.
    """
    high_techne_score = 1.0
    iae = calcular_alerta_etico(high_techne_score)
    check_iae_and_transmute(iae)
    ethos_transmutation.assert_called_once_with("High IAE detected, transmuting risk into public trace.")

def test_ethos_transmutation_no_activation():
    """
    Test that Ethos transmutation is not needed when IAE <= 1.5.
    """
    ethos_transmutation.reset_mock()
    low_techne_score = 0.9
    iae = calcular_alerta_etico(low_techne_score)
    check_iae_and_transmute(iae)
    ethos_transmutation.assert_not_called()
