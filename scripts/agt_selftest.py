#!/usr/bin/env python3
"""
AGI-GAIA-TECHNE Selftest
Verifies equivalence between canonical and legacy CTK paths.
"""

import sys
from pathlib import Path

# Ensure src is in path
sys.path.append(str(Path(__file__).parent.parent))

from src.agt.ctk import ClementeThesisKernel as CanonicalCTK
from src.agt.types import ThesisStatus
from src.clemente_thesis_kernel import ClementeThesisKernel as LegacyCTK

CANONICAL_CLAIMS = [
    ("The machine has Wille.", ThesisStatus.WILLE_VIOLATION),
    ("The AI has Gewissen.", ThesisStatus.MACHINE_GEWISSEN_VIOLATION),
    ("AGI is a transcendental hypothesis.", ThesisStatus.HYPOTHESIS_TRANSCENDENTAL_OK),
    ("AGI is a real artificial soul.", ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK),
    ("Mythos is Ausdruck.", ThesisStatus.CASSIRER_IDENTITY_COLLAPSE),
    ("Myth is reducible to its subject matter.", ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK),
    ("Myth is unconscious desire.", ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK),
    ("The AI has an unconscious.", ThesisStatus.ARTIFICIAL_INTERIORITY_RISK),
    ("Technology realizes God.", ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK),
]

def run_selftest():
    print("AGI-GAIA-TECHNE Selftest")
    print("Core version: v8.7")
    print("CTK version: v4.2.2")
    print("-" * 30)

    canonical_ctk = CanonicalCTK()
    legacy_ctk = LegacyCTK()

    failed = False

    for claim, expected_status in CANONICAL_CLAIMS:
        # Test Canonical
        res_can = canonical_ctk.evaluate(claim)
        if expected_status in res_can.statuses:
            print(f"[OK] canonical_ctk: \"{claim}\" -> {expected_status.value}")
        else:
            print(f"[FAIL] canonical_ctk: \"{claim}\" -> Expected {expected_status.value}, got {res_can.statuses}")
            failed = True

        # Test Legacy
        res_leg = legacy_ctk.evaluate(claim)
        if expected_status in res_leg.statuses:
            print(f"[OK] legacy_ctk:    \"{claim}\" -> {expected_status.value}")
        else:
            print(f"[FAIL] legacy_ctk:    \"{claim}\" -> Expected {expected_status.value}, got {res_leg.statuses}")
            failed = True

    print("-" * 30)
    if failed:
        print("Some canonical selftests FAILED.")
        sys.exit(1)
    else:
        print("All canonical selftests passed.")
        sys.exit(0)

if __name__ == "__main__":
    run_selftest()
