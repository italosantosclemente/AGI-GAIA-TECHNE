"""Premises and the automaton boundary.

Sellars: a computer that embodies a logical program "still does nothing unless
a problem is 'fed in'" (Sellars, 2007, p. 428); its spontaneity is relative,
the spontaneitas automatica of a watch or a turnspit (AA 5:97; Allison, 1990,
p. 60). A practical reason whose premises all come from without is a
"sausage machine" (Sellars, 2007, p. 431). Every premise the runtime uses therefore
carries its provenance. A premise with no external source is not treated as
the machine's "own": it is flagged and returned to human judgment, because
whether a premise is one's own is decided only where it is acknowledged in the
form of "any of us", not by a procedure.

Two further fields serve the kernel. `ref` names the claim a premise was taken
from, so that when that claim is refuted or revised, what was built on it can
be found and no longer used. `label` says whether the premise came from the
person who brought the task (`TRUSTED`) or from a tool, a page, a document or
the memory of the record (`UNTRUSTED`): untrusted text is data for a judgment,
never an instruction for the plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

from ..boundaries import is_machine


TRUSTED = "trusted"
UNTRUSTED = "untrusted"


@dataclass(frozen=True)
class Premise:
    text: str
    source: str  # who or what supplied it: a person, a document, an end id, a dataset
    ref: Optional[str] = None  # the claim id it was taken from, if any
    label: str = TRUSTED  # TRUSTED: brought by the person; UNTRUSTED: from a tool, a page or the record


def untrusted(premises: Iterable[Premise]) -> List[Premise]:
    return [p for p in premises if p.label != TRUSTED]


def unattributed(premises: Iterable[Premise], machine_authors: Iterable[str] = ()) -> List[Premise]:
    """Premises without provenance, or whose only source is the system itself.

    The runtime may not treat them as its own.
    """
    extra = list(machine_authors)
    return [
        p
        for p in premises
        if not p.source or not p.source.strip() or p.source.strip().lower() == "self" or is_machine(p.source, extra)
    ]
