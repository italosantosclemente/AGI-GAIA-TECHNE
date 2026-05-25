"""
Compatibility wrapper for CHK.
The canonical Chirimuuta Haptic Kernel now lives in agt.chk.
"""

from __future__ import annotations

import warnings

from agt.chk import *  # noqa: F401,F403

warnings.warn(
    "src.chirimuuta_haptic_kernel is deprecated. Use agt.chk instead.",
    DeprecationWarning,
    stacklevel=2,
)
