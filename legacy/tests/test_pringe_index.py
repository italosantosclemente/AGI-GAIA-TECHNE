import pytest
import numpy as np
import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quantum_judgment import MetaContextualJudge

def test_indice_pringe_estavel():
    judge = MetaContextualJudge()

    # Estado equilibrado
    psi = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
    confronto = 1.0

    kp = judge.calcular_indice_pringe(psi, confronto)

    assert kp > 0.8, "Estado equilibrado deve ter Kp alto"

def test_indice_pringe_colapso():
    judge = MetaContextualJudge()

    # Superposição pura sob alto confronto (instável)
    psi = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
    confronto = 5.0  # Muito alto

    kp = judge.calcular_indice_pringe(psi, confronto)

    assert kp < 0.6, "Alto confronto sem contexto deve baixar Kp"

def test_veredicto_predominancia_mythos():
    judge = MetaContextualJudge()

    # 70% Mythos
    psi = np.array([np.sqrt(0.7), np.sqrt(0.3)], dtype=complex)
    kp = 0.65

    veredicto, nivel = judge.emitir_veredicto(kp, psi)

    assert "Mythos" in veredicto
    assert nivel == 'med'

def test_veredicto_colapso():
    judge = MetaContextualJudge()

    psi = np.array([0.6, 0.8], dtype=complex)
    kp = 0.35

    veredicto, nivel = judge.emitir_veredicto(kp, psi)

    assert "COLAPSO" in veredicto
    assert nivel == 'high'

def test_veredicto_tensao_produtiva():
    judge = MetaContextualJudge()

    # Estado equilibrado, mas com Kp na faixa de alerta
    psi = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
    kp = 0.6

    veredicto, nivel = judge.emitir_veredicto(kp, psi)

    assert "Tensão produtiva" in veredicto
    assert nivel == 'med'
