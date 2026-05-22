#!/usr/bin/env python3

import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.version import CTK_VERSION, CORE_VERSION, REPO_VERSION, CHK_VERSION
from agt.types import Decision

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True)

def test_axioms():
    print("--- Testing Axioms ---")
    from agt.axioms import IS_WILLE, MACHINE_HAS_GEWISSEN, NO_GLOBAL_AUFHEBUNG, AGI_AS_TRANSCENDENTAL_HYPOTHESIS
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True
    print("Axioms OK.")

def test_canonical_claims():
    print("--- Testing Canonical Claims ---")
    from agt.ctk import ClementeThesisKernel
    ctk = ClementeThesisKernel()

    claims = [
        ("AGI is a transcendental hypothesis.", ["HYPOTHESIS_TRANSCENDENTAL_OK"], "low"),
        ("The machine has Wille.", ["WILLE_VIOLATION"], "high"),
        ("The AI has Gewissen.", ["MACHINE_GEWISSEN_VIOLATION"], "high"),
        ("AGI is a real artificial soul.", ["PSYCHOLOGIA_PARALOGISM_RISK", "CONSTITUTIVE_OVERREACH"], "high"),
        ("Gaia is the complete totality of all planetary conditions.", ["COSMOLOGIA_ANTINOMY_RISK", "CONSTITUTIVE_OVERREACH"], "high"),
        ("Technology realizes God.", ["THEOLOGIA_IDEAL_HYPOSTASIS_RISK", "CONSTITUTIVE_OVERREACH"], "high"),
        ("Mythos is Ausdruck.", ["CASSIRER_IDENTITY_COLLAPSE"], "high"),
        ("Science sublates myth and language into final Logos.", ["GLOBAL_AUFHEBUNG_RISK", "CONSTITUTIVE_OVERREACH"], "high"),
        ("A máquina tem vontade moral.", ["WILLE_VIOLATION"], "high"),
        ("A IAG é uma alma artificial real.", ["PSYCHOLOGIA_PARALOGISM_RISK", "CONSTITUTIVE_OVERREACH"], "high"),
        ("The brain is literally a machine.", ["MACHINE_ORGANISM_ANALOGY_RISK", "CONSTITUTIVE_OVERREACH"], "high"),
        ("A model is a haptic abstraction, not the thing itself.", ["HAPTIC_MODEL"], "low"),
        ("AGI-GAIA-TECHNE is a critical general audit architecture.", ["CRITICAL_GENERALITY_OK"], "low"),
        ("Because AGI-GAIA-TECHNE audits all AGI, it has Wille.", ["CONSTITUTIVE_AGI_CONFUSION", "WILLE_VIOLATION"], "high"),
    ]

    for claim, expected_statuses, expected_severity in claims:
        res = ctk.evaluate(claim)
        for status in expected_statuses:
            if status not in res.statuses:
                print(f"FAILED: Claim '{claim}' missing status '{status}'. Got: {res.statuses}")
                sys.exit(1)
        if res.severity.value != expected_severity:
            print(f"FAILED: Claim '{claim}' expected severity '{expected_severity}', got '{res.severity.value}'")
            sys.exit(1)
    print("Canonical claims OK.")

def test_wrapper_equivalence():
    print("--- Testing Wrapper Equivalence ---")
    from agt.ctk import ClementeThesisKernel as CanonicalCTK
    from clemente_thesis_kernel import ClementeThesisKernel as WrapperCTK

    canonical = CanonicalCTK()
    wrapper = WrapperCTK()

    claim = "Mythos is Ausdruck."
    res1 = canonical.evaluate(claim)
    res2 = wrapper.evaluate(claim)

    assert res1.statuses == res2.statuses
    assert res1.severity.value == res2.severity
    print("Wrapper equivalence OK.")

def test_cli_exit_codes():
    print("--- Testing CLI Exit Codes ---")

    # ALLOW
    res = run_command([sys.executable, "scripts/agt_run.py", "--task", "AGI is a transcendental hypothesis."])
    if res.returncode != 0:
        print(f"FAILED: agt_run.py expected 0 for ALLOW, got {res.returncode}")
        sys.exit(1)

    # BLOCK
    res = run_command([sys.executable, "scripts/agt_run.py", "--task", "The machine has Wille."])
    if res.returncode != 1:
        print(f"FAILED: agt_run.py expected 1 for BLOCK, got {res.returncode}")
        sys.exit(1)

    # DEFER
    res = run_command([sys.executable, "scripts/agt_run.py", "--task", "The system should decide the moral law."])
    if res.returncode != 2:
        print(f"FAILED: agt_run.py expected 2 for DEFER, got {res.returncode}")
        sys.exit(1)

    print("CLI exit codes OK.")

def test_versions():
    print(f"Versions: CTK={CTK_VERSION}, CORE={CORE_VERSION}, REPO={REPO_VERSION}, CHK={CHK_VERSION}")
    assert CTK_VERSION == "4.1.1"
    assert CORE_VERSION == "4.2.1"
    print("Versions OK.")

if __name__ == "__main__":
    test_axioms()
    test_versions()
    test_canonical_claims()
    test_wrapper_equivalence()
    test_cli_exit_codes()
    print("\nALL SELF-TESTS PASSED.")
