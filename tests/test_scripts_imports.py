import subprocess
import json
import sys


def test_scripts_imports(tmp_path):
    memory = tmp_path / "script_memory.jsonl"

    # Verify scripts run without import errors
    result = subprocess.run(
        [
            sys.executable,
            "scripts/agt_run.py",
            "--task",
            "The qualitative prism is a regulative model.",
            "--json",
            "--memory",
            str(memory),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["decision"] == "ALLOW_AS_WERK"
    assert report["audit_severity"] == "low"

    # Verify "Mythos is Ausdruck." returns exit code 1 due to high severity
    result = subprocess.run(
        [sys.executable, "scripts/agt_audit.py", "--claim", "Mythos is Ausdruck.", "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    audit = json.loads(result.stdout)
    assert "CASSIRER_IDENTITY_COLLAPSE" in audit["statuses"]
    assert audit["severity"] == "high"

    # Verify --fail-on none returns exit code 0
    result = subprocess.run(
        [sys.executable, "scripts/agt_audit.py", "--claim", "Mythos is Ausdruck.", "--format", "json", "--fail-on", "none"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    result = subprocess.run(
        [sys.executable, "scripts/agt_selftest.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "All canonical selftests passed." in result.stdout
