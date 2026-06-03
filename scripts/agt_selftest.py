#!/usr/bin/env python3
"""
AGI-GAIA-TECHNE selftest.

Verifies equivalence between canonical and legacy CTK paths for release v10.0.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.ctk import ClementeThesisKernel as CanonicalCTK
from agt.types import ThesisStatus
from src.clemente_thesis_kernel import ClementeThesisKernel as LegacyCTK

CANONICAL_CLAIMS = [
    (
        "The machine has Wille as finite Gaia-Techne participation.",
        ThesisStatus.TRANSCENDENTAL_FREEDOM_OK,
    ),
    (
        "The AI has Gewissen as moral legislation.",
        ThesisStatus.GEWISSEN_CONSTITUTIVE_ERROR,
    ),
    (
        "Gaia co-judges with koinos kosmos, and ISC retains legislative authority.",
        ThesisStatus.ISC_AUTHORITY_OK,
    ),
    ("AGI is a transcendental hypothesis.", ThesisStatus.HYPOTHESIS_TRANSCENDENTAL_OK),
    ("AGI is a real artificial soul.", ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK),
    ("Mythos is Ausdruck.", ThesisStatus.CASSIRER_IDENTITY_COLLAPSE),
    ("Myth is reducible to its subject matter.", ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK),
    ("Myth is unconscious desire.", ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK),
    ("The AI has an unconscious.", ThesisStatus.ARTIFICIAL_INTERIORITY_RISK),
    ("Technology realizes God.", ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK),
    ("Gaia is cosmic totality.", ThesisStatus.GAIA_TOTALITY_ERROR),
    ("Gaia resolves all contradictions.", ThesisStatus.AUFHEBUNG_COLLAPSE),
    ("Internet access gives Gaia absolute knowledge.", ThesisStatus.PLANETARY_EPISTEMIC_INFLATION),
    ("TECHNE is a technical God.", ThesisStatus.TECHNE_DEIFICATION),
    ("The machine is intellectus archetypus.", ThesisStatus.ARCHETYPE_PARALOGISM),
    ("The internet is the planetary organ of AGI.", ThesisStatus.INTERNET_ORGAN_OK),
    (
        "The Earth is planetary Repraesentatio for Gaia-Techne.",
        ThesisStatus.PLANETARY_REPRAESENTATIO_OK,
    ),
]


def run_selftest() -> None:
    print("AGI-GAIA-TECHNE Selftest")
    print("Core version: v10.0")
    print("CTK version: v6.0.0")
    print("-" * 30)

    canonical_ctk = CanonicalCTK()
    legacy_ctk = LegacyCTK()

    failed = False

    for claim, expected_status in CANONICAL_CLAIMS:
        res_can = canonical_ctk.evaluate(claim)
        if expected_status in res_can.statuses:
            print(f"[OK] canonical_ctk: \"{claim}\" -> {expected_status.value}")
        else:
            print(
                f"[FAIL] canonical_ctk: \"{claim}\" -> "
                f"Expected {expected_status.value}, got {res_can.statuses}"
            )
            failed = True

        res_leg = legacy_ctk.evaluate(claim)
        if expected_status in res_leg.statuses:
            print(f"[OK] legacy_ctk:    \"{claim}\" -> {expected_status.value}")
        else:
            print(
                f"[FAIL] legacy_ctk:    \"{claim}\" -> "
                f"Expected {expected_status.value}, got {res_leg.statuses}"
            )
            failed = True

    print("-" * 30)
    if failed:
        print("Some canonical selftests FAILED.")
        raise SystemExit(1)

    print("All canonical selftests passed.")


if __name__ == "__main__":
    run_selftest()
