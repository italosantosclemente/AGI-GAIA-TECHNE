"""
Compatibility wrapper for CTK.
The canonical Clemente Thesis Kernel now lives in agt.ctk.
"""

from __future__ import annotations

import warnings

from agt.ctk import *  # noqa: F401,F403
<<<<<<< HEAD
=======
from agt.types import ThesisStatus  # noqa: F401
>>>>>>> origin/main

warnings.warn(
    "src.clemente_thesis_kernel is deprecated. Use agt.ctk instead.",
    DeprecationWarning,
    stacklevel=2,
)
<<<<<<< HEAD
=======

# Re-export some internal logic that was in v4.2.2 but might be used by old tests
from agt.types import AuditResult as EvaluationResult  # noqa: F401
>>>>>>> origin/main
