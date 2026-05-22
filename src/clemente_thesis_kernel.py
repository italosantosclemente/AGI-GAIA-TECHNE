"""
Compatibility wrapper for CTK.

The canonical Clemente Thesis Kernel now lives in:

    src/agt/ctk.py

This module is retained only for legacy imports.
"""

from __future__ import annotations

import warnings

from src.agt.ctk import *  # noqa: F401,F403
from src.agt.types import ThesisStatus  # noqa: F401

warnings.warn(
    "src.clemente_thesis_kernel is deprecated. Use src.agt.ctk instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export some internal logic that was in v4.1 but might be used by old tests
from src.agt.types import AuditResult as EvaluationResult  # noqa: F401
