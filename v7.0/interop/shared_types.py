"""shared_types.py — Data contracts for Julia-Python interop."""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List

@dataclass
class AgentMetadata:
    agent_id: str
    symbolic_form: str
    confidence: float
    strength: float

@dataclass
class InteropPacket:
    payload: Any
    metadata: Dict[str, Any]
    source: str

def to_dict(obj):
    if hasattr(obj, "__dict__"):
        return asdict(obj)
    return str(obj)
