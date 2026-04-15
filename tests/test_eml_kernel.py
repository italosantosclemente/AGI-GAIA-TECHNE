"""
Tests for src/core/eml_kernel.py — calibração bidirecional 140426.

Cobertura:
  * classificação cassireriana (Ausdruck / Darstellung / Bedeutung)
  * guarda da singularidade Mythos (log(0))
  * operadores bidirecionais (ascensão e descida)
  * genus proximum / common_determination
  * focus imaginarius estritamente positivo (regra arquitetônica #4)
  * Ethos = Gewissen (regra arquitetônica #2)
"""

from __future__ import annotations

import cmath
import math
import os
import sys

import pytest

# torna importável src/core/ sem precisar de pacote instalado
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from core.eml_kernel import (  # noqa: E402
    CognitionSyntax,
    EMLNode,
    EMLTreeFactory,
    Ethos,
    LEAF_CONST,
    LEAF_PARAM,
    LEAF_VAR,
    Logos,
    NODE_EML,
    Simbiota,
    SymbolicFunction,
    ascend_step,
    classify_tree,
    common_determination,
    descend_evaluate,
    descend_residual,
    is_darstellung_one,
    is_pure_grammar,
    level_of_node,
    mythos_singularity_guard,
)


# ---------------------------------------------------------------- níveis

def test_darstellung_is_one():
    one = EMLNode(LEAF_CONST, value=1 + 0j)
    assert is_darstellung_one(one)
    assert level_of_node(one) is SymbolicFunction.DARSTELLUNG


def test_const_other_value_is_ausdruck():
    other = EMLNode(LEAF_CONST, value=2 + 0j)
    assert not is_darstellung_one(other)
    assert level_of_node(other) is SymbolicFunction.AUSDRUCK


def test_var_is_ausdruck():
    v = EMLNode(LEAF_VAR, name="x")
    assert level_of_node(v) is SymbolicFunction.AUSDRUCK


def test_param_is_ausdruck():
    p = EMLNode(LEAF_PARAM, value=0.3 + 0.1j)
    assert level_of_node(p) is SymbolicFunction.AUSDRUCK


def test_bedeutung_is_pure_grammar():
    one = lambda: EMLNode(LEAF_CONST, value=1 + 0j)
    inner = EMLNode(NODE_EML, left=one(), right=one())
    pure = EMLNode(NODE_EML, left=one(), right=inner)
    assert is_pure_grammar(pure)
    assert level_of_node(pure) is SymbolicFunction.BEDEUTUNG


def test_mixed_node_is_darstellung_in_transit():
    # eml(x, 1) é mediação em trânsito (tem VAR), não Bedeutung pura.
    mix = EMLNode(
        NODE_EML,
        left=EMLNode(LEAF_VAR, name="x"),
        right=EMLNode(LEAF_CONST, value=1 + 0j),
    )
    assert not is_pure_grammar(mix)
    assert level_of_node(mix) is SymbolicFunction.DARSTELLUNG


def test_classify_tree_profile():
    one = lambda: EMLNode(LEAF_CONST, value=1 + 0j)
    var = EMLNode(LEAF_VAR, name="x")
    tree = EMLNode(NODE_EML, left=var, right=one())
    profile = classify_tree(tree)
    assert profile[SymbolicFunction.AUSDRUCK] == 1     # x
    assert profile[SymbolicFunction.DARSTELLUNG] == 2  # 1 e o NODE misto
    assert profile[SymbolicFunction.BEDEUTUNG] == 0


# ----------------------------------------------------------- singularidade

def test_mythos_singularity_guard_replaces_zero():
    out = mythos_singularity_guard(0 + 0j)
    assert abs(out) > 0


def test_mythos_singularity_guard_passthrough():
    y = 0.7 - 0.2j
    assert mythos_singularity_guard(y) == y


def test_backward_does_not_explode_at_y_near_zero():
    # eml(x, y) com y ≈ 0; backward deve usar a guarda e não quebrar.
    x = EMLNode(LEAF_VAR, name="x")
    y = EMLNode(LEAF_PARAM, value=1e-15 + 0j)
    tree = EMLNode(NODE_EML, left=x, right=y)
    tree.forward({"x": 0.5 + 0j})
    tree.zero_grad()
    tree.backward(upstream=1 + 0j)
    # gradiente do PARAM existe e é finito
    assert math.isfinite(abs(y._grad))


# -------------------------------------------------------- bidirecionalidade

def test_ascend_step_replaces_param():
    p = EMLNode(LEAF_PARAM, value=0.4 + 0.1j)
    new = ascend_step(p)
    assert new.kind == NODE_EML
    assert is_darstellung_one(new.left)
    assert is_darstellung_one(new.right)


def test_ascend_descend_eml_x_one_matches_exp():
    # crystal = eml(x, 1)  ≡  exp(x) − log(1)  =  exp(x)
    crystal = EMLNode(
        NODE_EML,
        left=EMLNode(LEAF_VAR, name="x"),
        right=EMLNode(LEAF_CONST, value=1 + 0j),
    )
    xs = [complex(v, 0) for v in (-2.0, -0.5, 0.0, 0.5, 2.0)]
    err = descend_residual(crystal, cmath.exp, xs)
    assert err < 1e-20


def test_descend_evaluate_returns_per_env_outputs():
    crystal = EMLNode(
        NODE_EML,
        left=EMLNode(LEAF_VAR, name="x"),
        right=EMLNode(LEAF_CONST, value=1 + 0j),
    )
    envs = [{"x": 0 + 0j}, {"x": 1 + 0j}]
    out = descend_evaluate(crystal, envs)
    assert len(out) == 2
    assert abs(out[0] - cmath.exp(0)) < 1e-12
    assert abs(out[1] - cmath.exp(1)) < 1e-12


# ----------------------------------------------------------- genus proximum

def test_common_determination_extracts_shared_subtree():
    one = lambda: EMLNode(LEAF_CONST, value=1 + 0j)
    var = lambda: EMLNode(LEAF_VAR, name="x")
    inner_a = EMLNode(NODE_EML, left=var(), right=one())   # eml(x, 1)
    inner_b = EMLNode(NODE_EML, left=var(), right=one())   # eml(x, 1)
    tree_a = EMLNode(NODE_EML, left=inner_a, right=one())  # eml(eml(x,1), 1)
    tree_b = EMLNode(
        NODE_EML,
        left=inner_b,
        right=EMLNode(NODE_EML, left=one(), right=one()),  # eml(eml(x,1), eml(1,1))
    )
    common = common_determination(tree_a, tree_b)
    assert common is not None
    assert common.kind == NODE_EML
    assert common.left.kind == LEAF_VAR
    assert is_darstellung_one(common.right)


def test_common_determination_none_when_only_params():
    a = EMLNode(LEAF_PARAM, value=0.1 + 0j)
    b = EMLNode(LEAF_PARAM, value=0.1 + 0j)
    assert common_determination(a, b) is None


def test_common_determination_const_one_match():
    a = EMLNode(LEAF_CONST, value=1 + 0j)
    b = EMLNode(LEAF_CONST, value=1 + 0j)
    out = common_determination(a, b)
    assert out is not None
    assert is_darstellung_one(out)


# ----------------------------------------------------------- focus + ethos

def test_focus_strictly_positive_even_when_loss_zero():
    crystal = EMLNode(
        NODE_EML,
        left=EMLNode(LEAF_VAR, name="x"),
        right=EMLNode(LEAF_CONST, value=1 + 0j),
    )
    ethos = Ethos()
    ev = ethos.evaluate(crystal, loss=0.0, descent_residual=0.0)
    # regra arquitetônica #4: o focus imaginarius é INALCANÇÁVEL
    assert ev.distance_to_focus > 0.0
    assert ev.distance_to_focus_ascent >= 0.0
    assert ev.distance_to_focus_descent == 0.0


def test_focus_norm_combines_both_directions():
    crystal = EMLNode(LEAF_CONST, value=1 + 0j)
    ethos = Ethos()
    ev = ethos.evaluate(crystal, loss=0.0, descent_residual=0.5)
    # √(d_asc² + d_desc²) ≥ |d_desc|
    assert ev.distance_to_focus >= ev.distance_to_focus_descent


def test_ethos_is_gewissen_not_wissen():
    """Regra arquitetônica #2: o Ethos é Gewissen, jamais Wissen."""
    ethos = Ethos()
    assert hasattr(ethos, "gewissen_accept")
    assert not hasattr(ethos, "wissen_accept")


# ------------------------------------------------------- syntax + simbiota

def test_cognition_syntax_round_trip():
    syntax = CognitionSyntax()
    one = syntax.darstellung_one()
    assert syntax.is_darstellung_one_node(one)
    profile = syntax.classify(one)
    assert profile[SymbolicFunction.DARSTELLUNG] == 1


def test_simbiota_bidirectional_runs():
    xs = [complex(v, 0) for v in (-1.0, -0.5, 0.0, 0.5, 1.0)]
    ys = [cmath.exp(x) for x in xs]
    sim = Simbiota(
        xs, ys,
        candidates_per_depth=6,
        fit_steps=60,
        lr=0.08,
        seed=42,
        target_fn=cmath.exp,
        descent_domain=[complex(v, 0) for v in (-2.0, 0.0, 2.0)],
    )
    state = sim.run_bidirectional(max_depth=2, verbose=False)
    # ambas as componentes devem ser quantidades reais finitas
    assert math.isfinite(state.best_eval.distance_to_focus_ascent)
    assert math.isfinite(state.best_eval.distance_to_focus_descent)
    assert state.best_eval.distance_to_focus > 0
