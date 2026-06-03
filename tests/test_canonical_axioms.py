from agt import AGTController, __version__
from agt.axioms import IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG, AGI_AS_TRANSCENDENTAL_HYPOTHESIS
from agt.version import PACKAGE_VERSION

def test_axioms():
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True


def test_public_api_exports():
    assert AGTController.__name__ == "AGTController"
    assert __version__ == PACKAGE_VERSION
