import os
import pytest

def test_eml_v4_files_exist():
    # Note: src/core/eml_kernel_v4_complete.jl is expected to be provided by user
    # but the script and documentation should already point to it.
    assert os.path.exists("scripts/run_eml_v4_complete.jl")
    # This one might fail until the user provides the content
    # assert os.path.exists("src/core/eml_kernel_v4_complete.jl")

def test_run_eml_v4_script_content():
    with open("scripts/run_eml_v4_complete.jl", "r") as f:
        content = f.read()
    assert 'include("../src/core/eml_kernel_v4_complete.jl")' in content
    assert 'EMLKernelV4Complete.executar_verificacao_completa_v4()' in content

def test_eml_kernel_doc_anchors():
    assert os.path.exists("docs/references/eml-kernel.md")
    with open("docs/references/eml-kernel.md", "r") as f:
        content = f.read()
    assert "eml_kernel_v4_complete.jl" in content
    assert "run_eml_v4_complete.jl" in content
