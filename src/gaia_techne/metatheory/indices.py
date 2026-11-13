"""Metatheory: the conditions under which claims can be corrected by "any of us".

Final conclusion of the argument: a metatheory is not a metaphysics and not a
further theory; it is the reflection on the conditions under which the claims
of every theory can be corrected by anyone, and in this sense it is an
ethico-teleology: it orders the advance of every theory by an end that the
practical sets and that no theory can read off its own progress.
These indices measure those conditions over a set of claims. They are
reports for human judgment, not verdicts.

The report is a sign, not a forecast. Progress of a free being cannot be
predicted from its freedom (AA 7:81, 84-85), and critical philosophy "cannot
prophesy" where human doing is at stake (ECW 22:165). `widening` describes the
record as it stands; it predicts nothing.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List

from ..canon.claims import Claim, ProcedureKind, Reach, Stage


@dataclass(frozen=True)
class Report:
    claims: int
    correctable_share: float
    restricted_share: float
    experience_share: float
    shared_share: float
    reach_distribution: Dict[str, int]
    procedure_monoculture: float
    flagged_share: float

    @property
    def widening(self) -> bool:
        """True when the record keeps claims open to a wider community than their source."""
        return self.correctable_share >= 0.5 and self.restricted_share < 0.5


def _share(n: int, total: int) -> float:
    return round(n / total, 3) if total else 0.0


def report(claims: Iterable[Claim]) -> Report:
    cs: List[Claim] = list(claims)
    total = len(cs)
    objectual = [c for c in cs if c.determines_object]
    correctable = sum(1 for c in objectual if c.correctable)
    restricted = sum(1 for c in objectual if c.procedures and not c.correctable)
    experience = sum(1 for c in cs if c.stage is Stage.EXPERIENCE)
    shared = sum(1 for c in cs if c.stage is Stage.SHARED)
    flagged = sum(1 for c in cs if c.flags)
    reach = Counter(c.reach.name for c in cs)
    kinds = Counter(p.kind for c in cs for p in c.procedures)
    # Epistemicide is the substitution of one procedure of correction for all others.
    mono = round(max(kinds.values()) / sum(kinds.values()), 3) if kinds else 0.0
    return Report(
        claims=total,
        correctable_share=_share(correctable, len(objectual)),
        restricted_share=_share(restricted, len(objectual)),
        experience_share=_share(experience, total),
        shared_share=_share(shared, total),
        reach_distribution={r.name: reach.get(r.name, 0) for r in Reach},
        procedure_monoculture=mono,
        flagged_share=_share(flagged, total),
    )


def procedure_kinds_in_use(claims: Iterable[Claim]) -> List[ProcedureKind]:
    return sorted({p.kind for c in claims for p in c.procedures}, key=lambda k: k.name)
