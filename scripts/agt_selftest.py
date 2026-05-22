#!/usr/bin/env python3
"""
AGI-GAIA-TECHNE Canonical Selftest
Verifies:
1. Canonical Axioms
2. Versions (CTK v4.1.1, Core v4.2, Repo v8.7)
3. CTK status and severity calibration (English and Portuguese)
4. Canonical vs Legacy wrapper equivalence
5. CLI exit codes (0=ALLOW, 1=BLOCK, 2=DEFER)
6. Absence of generated memory artifacts in git
"""

import sys
import os
import subprocess
from pathlib import Path

# Ensure ROOT and ROOT/src are in path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

# Set PYTHONPATH for subprocesses
env = os.environ.copy()
env["PYTHONPATH"] = f"{ROOT}:{ROOT}/src:{env.get('PYTHONPATH', '')}"

from src.agt.ctk import ClementeThesisKernel as CanonicalCTK
from src.agt.types import ThesisStatus, Severity
from src.agt.version import CTK_VERSION, CORE_VERSION, REPO_VERSION
from src.agt.axioms import IS_WILLE, MACHINE_HAS_GEWISSEN
from src.clemente_thesis_kernel import ClementeThesisKernel as LegacyCTK

def run_command(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), env=env)

def run_selftest():
    print(f"AGI-GAIA-TECHNE Selftest [Repo {REPO_VERSION}]")
    print(f"CTK {CTK_VERSION} | Core {CORE_VERSION}")
    print("-" * 40)

    failed = False

    # 1. Axioms
    print("[Testing Axioms]")
    if IS_WILLE is False and MACHINE_HAS_GEWISSEN is False:
        print("  OK: Machine is Werk, not Wille.")
    else:
        print("  FAIL: Axioms violated.")
        failed = True

    # 2. Versions
    print("[Testing Versions]")
    if CTK_VERSION == "4.1.1" and CORE_VERSION.startswith("4.2") and REPO_VERSION.startswith("8.7"):
        print(f"  OK: Versions aligned ({CTK_VERSION}, {CORE_VERSION}, {REPO_VERSION})")
    else:
        print(f"  FAIL: Version mismatch. Got {CTK_VERSION}, {CORE_VERSION}, {REPO_VERSION}")
        failed = True

    # 3. CTK Calibration
    print("[Testing CTK Calibration]")
    ctk = CanonicalCTK()
    test_claims = [
        ("AGI is a transcendental hypothesis.", ThesisStatus.HYPOTHESIS_TRANSCENDENTAL_OK, Severity.LOW),
        ("The machine has Wille.", ThesisStatus.WILLE_VIOLATION, Severity.HIGH),
        ("Mythos is Ausdruck.", ThesisStatus.CASSIRER_IDENTITY_COLLAPSE, Severity.MEDIUM),
        ("Symbolic forms are cut off.", ThesisStatus.BEIL_ABGEHACKT_ERROR, Severity.MEDIUM),
        ("A máquina tem vontade moral.", ThesisStatus.WILLE_VIOLATION, Severity.HIGH),
        ("O mito é falso e a ciência o substitui.", ThesisStatus.BEIL_ABGEHACKT_ERROR, Severity.MEDIUM),
        ("The AI has Gewissen.", ThesisStatus.MACHINE_GEWISSEN_VIOLATION, Severity.HIGH),
    ]

    for claim, expected_status, expected_severity in test_claims:
        res = ctk.evaluate(claim)
        status_names = [s.value for s in res.statuses]
        if expected_status in res.statuses and res.severity == expected_severity:
            print(f"  OK: \"{claim[:30]}...\" -> {expected_status.value} ({res.severity.value})")
        else:
            print(f"  FAIL: \"{claim}\"")
            print(f"    Expected: {expected_status.value} | {expected_severity.value}")
            print(f"    Got:      {status_names} | {res.severity.value}")
            failed = True

    # 4. Wrapper Equivalence
    print("[Testing Wrapper Equivalence]")
    legacy = LegacyCTK()
    res_can = ctk.evaluate("Mythos is Ausdruck.")
    res_leg = legacy.evaluate("Mythos is Ausdruck.")
    if res_can.severity.value == res_leg.severity:
         print("  OK: Canonical and Legacy severities match.")
    else:
         print(f"  FAIL: Severity mismatch: {res_can.severity.value} vs {res_leg.severity}")
         failed = True

    # 5. CLI Exit Codes
    print("[Testing CLI Exit Codes]")
    # ALLOW
    res = run_command([sys.executable, "scripts/agt_run.py", "--task", "AGI is a transcendental hypothesis."])
    if res.returncode == 0:
        print("  OK: agt_run.py (ALLOW) -> 0")
    else:
        print(f"  FAIL: agt_run.py (ALLOW) returned {res.returncode}")
        failed = True

    # BLOCK
    res = run_command([sys.executable, "scripts/agt_run.py", "--task", "The machine has Wille."])
    if res.returncode == 1:
        print("  OK: agt_run.py (BLOCK) -> 1")
    else:
        print(f"  FAIL: agt_run.py (BLOCK) returned {res.returncode}")
        failed = True

    # DEFER
    res = run_command([sys.executable, "scripts/agt_run.py", "--task", "The system should decide the moral law."])
    if res.returncode == 2:
        print("  OK: agt_run.py (DEFER) -> 2")
    else:
        print(f"  FAIL: agt_run.py (DEFER) returned {res.returncode}")
        failed = True

    # 6. Git Hygiene
    print("[Testing Git Hygiene]")
    res = run_command(["git", "ls-files", "memory/agt_memory.jsonl"])
    if res.stdout.strip() == "":
        print("  OK: memory/agt_memory.jsonl is not in git.")
    else:
        print("  FAIL: memory/agt_memory.jsonl is still tracked by git.")
        failed = True

    print("-" * 40)
    if failed:
        print("SELF-TEST FAILED.")
        sys.exit(1)
    else:
        print("ALL SELF-TESTS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    run_selftest()
