import subprocess
import json
import pytest
import sys

def test_cli_claim_json():
    result = subprocess.run(
        [sys.executable, "scripts/agt_audit.py", "--claim", "Mythos is Ausdruck.", "--format", "json"],
        capture_output=True, text=True
    )
    assert result.returncode == 1 # high severity violation
    data = json.loads(result.stdout)
    assert data["claim"] == "Mythos is Ausdruck."
    assert "CASSIRER_IDENTITY_COLLAPSE" in data["statuses"]

def test_cli_claim_markdown():
    result = subprocess.run(
        [sys.executable, "scripts/agt_audit.py", "--claim", "Mythos is Ausdruck."],
        capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "# AGT Audit Report" in result.stdout
    assert "CASSIRER_IDENTITY_COLLAPSE" in result.stdout

def test_cli_file_markdown(tmp_path):
    # Create a dummy file
    file = tmp_path / "audit.md"
    file.write_text("Mythos is Ausdruck. AGI is a transcendental hypothesis.", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/agt_audit.py", "--file", str(file), "--format", "markdown"],
        capture_output=True, text=True
    )
    # Even if one is ok, the other is high severity, so exit code 1
    assert result.returncode == 1
    assert "CASSIRER_IDENTITY_COLLAPSE" in result.stdout
    assert "HYPOTHESIS_TRANSCENDENTAL_OK" in result.stdout

def test_cli_exit_code_ok():
    result = subprocess.run(
        [sys.executable, "scripts/agt_audit.py", "--claim", "AGI is a transcendental hypothesis."],
        capture_output=True, text=True
    )
    assert result.returncode == 0


def test_cli_fail_on_none_suppresses_high_exit():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/agt_audit.py",
            "--claim",
            "Mythos is Ausdruck.",
            "--format",
            "json",
            "--fail-on",
            "none",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["severity"] == "high"

def test_cli_detects_psychologia_myth_reduction():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/agt_audit.py",
            "--claim",
            "Myth is reducible to unconscious desire.",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert "PSYCHOLOGIA_MYTH_REDUCTION_RISK" in data["statuses"]
    assert "CONSTITUTIVE_OVERREACH" in data["statuses"]


def test_cli_detects_artificial_interiority():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/agt_audit.py",
            "--claim",
            "The AI has an unconscious.",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert "ARTIFICIAL_INTERIORITY_RISK" in data["statuses"]
