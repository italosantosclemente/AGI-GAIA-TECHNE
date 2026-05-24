import pytest
from agt.axioms import IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG, AGI_AS_TRANSCENDENTAL_HYPOTHESIS, assert_axioms

def test_axioms_values():
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True

def test_assert_axioms_passes():
    # Should not raise AssertionError
    assert_axioms()
