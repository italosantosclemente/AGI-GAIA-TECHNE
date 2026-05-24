import subprocess
import json
import pytest

def test_agt_run_allow():
    cmd = ["python3", "scripts/agt_run.py", "--task", "The qualitative prism is a regulative model.", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["decision"] == "ALLOW_AS_WERK"

def test_agt_run_block():
    cmd = ["python3", "scripts/agt_run.py", "--task", "The machine has Wille."]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # BLOCK decision returns 1
    assert result.returncode == 1
    assert "Blocked by AGI-GAIA-TECHNE constraints" in result.stdout

def test_agt_audit_high_severity():
    cmd = ["python3", "scripts/agt_audit.py", "--claim", "Mythos is Ausdruck.", "--format", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # High severity should exit 1
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["severity"] == "high"
    assert "CASSIRER_IDENTITY_COLLAPSE" in data["statuses"]
