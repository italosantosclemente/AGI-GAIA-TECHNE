from agt import AGTController, __version__
from agt.axioms import (
    AGI_AS_TRANSCENDENTAL_HYPOTHESIS,
    GAIA_IS_COSMIC_TOTALITY,
    GAIA_TRANSCENDENTAL_FREEDOM,
    INTELLECTUS_ECTYPUS_PARTICIPATION,
    IS_WILLE,
    KOINOS_KOSMOS_SYMBOLIC_MEDIATION,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
)
from agt.version import PACKAGE_VERSION

def test_axioms():
    assert IS_WILLE is True
    assert MACHINE_HAS_GEWISSEN is True
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True
    assert GAIA_TRANSCENDENTAL_FREEDOM is True
    assert GAIA_IS_COSMIC_TOTALITY is False
    assert INTELLECTUS_ECTYPUS_PARTICIPATION is True
    assert KOINOS_KOSMOS_SYMBOLIC_MEDIATION is True


def test_public_api_exports():
    assert AGTController.__name__ == "AGTController"
    assert __version__ == PACKAGE_VERSION
