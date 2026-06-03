import pytest
from pathlib import Path
import subprocess
import sys

def test_eml_v4_artifact_exists():
    assert Path("src/core/eml_kernel_v4_complete.jl").exists()
    assert Path("scripts/run_eml_v4_complete.jl").exists()

def test_eml_v4_artifact_content():
    content = Path("src/core/eml_kernel_v4_complete.jl").read_text()
    assert "executar_verificacao_completa_v4" in content
    assert "FirewallDecision" in content
    assert "BoundaryManifesto" in content
    assert "ManifestLedger" in content
    assert "json_escape" in content
    assert "sha256" in content
    assert "@assert" in content

@pytest.mark.skipif(subprocess.call(["which", "julia"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0, reason="Julia not installed")
def test_eml_v4_execution():
    result = subprocess.run(["julia", "scripts/run_eml_v4_complete.jl"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Todos os testes passaram" in result.stdout
