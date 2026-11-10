"""julia_bridge.py — Python calling Julia via juliacall."""

import juliacall
from .shared_types import InteropPacket

# Initialize Julia environment
jl = juliacall.new_module("InteropBridge")

def call_julia_function(module_name: str, func_name: str, *args):
    """Dynamically call a Julia function from a specific module."""
    # This is a simplified wrapper
    module = juliacall.Main.eval(f"using {module_name}; {module_name}")
    func = getattr(module, func_name)
    return func(*args)

def run_auseinandersetzung_on_julia_graph(graph_ptr, query):
    """Bridge call to trigger Julia-side graph negotiation."""
    return call_julia_function("MetateoriaIntersubjetiva", "auseinandersetzung!", graph_ptr, query)
