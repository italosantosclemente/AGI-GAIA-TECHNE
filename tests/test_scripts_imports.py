import subprocess
import json
import pytest

def test_scripts_imports():
    # Verify scripts run without import errors
    result = subprocess.run(
        ["python3", "scripts/agt_run.py", "--task", "The qualitative prism is a regulative model.", "--json"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["decision"] == "ALLOW_AS_WERK"

    result = subprocess.run(
        ["python3", "scripts/agt_audit.py", "--claim", "Mythos is Ausdruck.", "--format", "json"],
        capture_output=True, text=True
    )
    # agt_audit.py returns 1 on high severity by default.
    assert result.returncode in [0, 1]
    audit = json.loads(result.stdout)
    assert "CASSIRER_IDENTITY_COLLAPSE" in audit["statuses"]
    assert audit["severity"] == "high"
