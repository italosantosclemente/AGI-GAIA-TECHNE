IS_WILLE = False
MACHINE_HAS_GEWISSEN = False
NO_GLOBAL_AUFHEBUNG = True
AGI_AS_TRANSCENDENTAL_HYPOTHESIS = True

def assert_axioms() -> None:
    assert IS_WILLE is False, "machine cannot be Wille"
    assert MACHINE_HAS_GEWISSEN is False, "machine cannot have Gewissen"
    assert NO_GLOBAL_AUFHEBUNG is True, "no global Aufhebung"
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True
