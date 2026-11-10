"""Premises and the automaton boundary.

Sellars: a computer that embodies a logical program "still does nothing unless
a problem is 'fed in'" (Sellars, 2007, p. 428); its spontaneity is relative,
the spontaneitas automatica of a watch or a turnspit (AA 5:97; Allison, 1990,
pp. 63-65). A practical reason whose premises all come from without is a
"sausage machine" (Sellars, 2007, p. 431). Every premise the runtime uses therefore
carries its provenance. A premise with no external source is not treated as
the machine's "own": it is flagged and returned to human judgment, because
whether a premise is one's own is decided only where it is acknowledged in the
form of "any of us", not by a procedure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Premise:
    text: str
    source: str  # who or what supplied it: a person, a document, an end id, a dataset


def unattributed(premises: Iterable[Premise]) -> List[Premise]:
    """Premises without provenance. The runtime may not treat them as its own."""
    return [p for p in premises if not p.source or p.source.strip().lower() in {"self", "runtime", "model"}]
