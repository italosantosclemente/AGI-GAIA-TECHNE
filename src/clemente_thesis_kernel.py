"""
Compatibility wrapper for CTK.
The canonical Clemente Thesis Kernel now lives in agt.ctk.
"""

from __future__ import annotations

import warnings

from agt.ctk import *  # noqa: F401,F403

warnings.warn(
    "src.clemente_thesis_kernel is deprecated. Use agt.ctk instead.",
    DeprecationWarning,
    stacklevel=2,
)
