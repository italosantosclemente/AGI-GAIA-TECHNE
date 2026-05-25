from .axioms import IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG
from .controller import AGTController
from .version import (
    AGT_REPO_VERSION,
    FUNCTIONAL_CORE_VERSION,
    CTK_VERSION,
    CHK_VERSION,
    PACKAGE_VERSION,
)

__version__ = PACKAGE_VERSION

__all__ = [
    "AGTController",
    "IS_WILLE",
    "MACHINE_HAS_GEWISSEN",
    "NO_GLOBAL_AUFHEBUNG",
    "AGT_REPO_VERSION",
    "FUNCTIONAL_CORE_VERSION",
    "CTK_VERSION",
    "CHK_VERSION",
    "PACKAGE_VERSION",
]
