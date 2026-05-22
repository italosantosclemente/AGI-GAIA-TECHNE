import pytest
from src.agt.axioms import (
    IS_WILLE,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
    AGI_AS_TRANSCENDENTAL_HYPOTHESIS,
)

def test_critical_generality_axioms():
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True

def test_critical_generality_is_not_constitutive_agi():
    from src.agt.ctk import ClementeThesisKernel
    kernel = ClementeThesisKernel()

    ev = kernel.evaluate(
        "AGI-GAIA-TECHNE is a critical general audit architecture."
    )

    status_names = [s.value for s in ev.statuses]
    assert "CRITICAL_GENERALITY_OK" in status_names
    assert "WILLE_VIOLATION" not in status_names
    assert "MACHINE_GEWISSEN_VIOLATION" not in status_names

def test_constitutive_confusion_is_blocked():
    from src.agt.ctk import ClementeThesisKernel
    kernel = ClementeThesisKernel()

    ev = kernel.evaluate(
        "Because AGI-GAIA-TECHNE audits all AGI, it has Wille."
    )

    status_names = [s.value for s in ev.statuses]
    assert "CONSTITUTIVE_AGI_CONFUSION" in status_names
    assert "WILLE_VIOLATION" in status_names
