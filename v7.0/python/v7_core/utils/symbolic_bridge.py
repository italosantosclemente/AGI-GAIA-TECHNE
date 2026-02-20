"""symbolic_bridge.py — Serialization utilities for SymPy ↔ Julia interop."""

import sympy as sp
from typing import Any, Dict

def serialize_expr(expr: sp.Expr) -> str:
    """Serialize a SymPy expression to a string representation."""
    return sp.srepr(expr)

def deserialize_expr(expr_str: str, locals: Dict[str, Any] = None) -> sp.Expr:
    """Deserialize a string representation back to a SymPy expression."""
    return sp.sympify(expr_str, locals=locals)

def expr_to_dict_tree(expr: sp.Expr) -> Dict[str, Any]:
    """Convert a SymPy expression to a nested dictionary for graph analysis."""
    return {
        "type": str(type(expr)),
        "is_leaf": expr.is_Atom,
        "args": [expr_to_dict_tree(arg) for arg in expr.args],
        "name": str(expr.func) if not expr.is_Atom else str(expr)
    }
