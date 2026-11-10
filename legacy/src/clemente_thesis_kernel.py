"""
Import redirect for CTK.

The canonical Clemente Thesis Kernel now lives in:

    src/agt/ctk.py

This module is retained only to route older import paths into the v5 kernel.
"""

from __future__ import annotations

import warnings

from agt.ctk import *  # noqa: F401,F403
from agt.types import ThesisStatus  # noqa: F401

warnings.warn(
    "src.clemente_thesis_kernel is deprecated. Use agt.ctk instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export the public evaluation shape for callers pinned to this import path.
from agt.types import AuditResult as EvaluationResult  # noqa: F401
