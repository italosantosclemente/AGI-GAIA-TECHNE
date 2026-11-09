"""The canon: judging the form of claims, never producing them.

Kant distinguishes logic as a canon, which judges cognitions given to it,
from logic as an organon, which would produce them (KrV A:61/B:85). The
runtime is a canon in preparation:

- it never marks its own claim as holding for everyone;
- a claim moves from perception to experience only by corrections made by
  others, through public procedures;
- every claim of signification must name a perception in which it can be
  tested (descent), because our understanding is discursive and cannot
  produce the particular from the whole (AA 5:406-408).
"""

from __future__ import annotations

from typing import List

from ..koinos.prism import Direction
from . import guards
from .claims import Claim, CorrectionEvent, Reach, Stage


class OrganonRefused(PermissionError):
    """Raised when the runtime tries to certify its own claim."""


class Canon:
    def admit(self, claim: Claim) -> Claim:
        """Admit a claim as a judgment of perception, with its guard flags."""
        claim.stage = Stage.PERCEPTION
        claim.flags = [f"{f.guard}: {f.error} ({f.match!r})" for f in guards.check(claim)]
        if not claim.procedures:
            claim.flags.append("uncorrectable: no procedure by which others can test it")
        elif not claim.correctable:
            claim.flags.append("restricted: correction reserved to those who own the means")
        if claim.direction is Direction.AWAY_FROM_LIFE and not claim.returns_to_perception:
            claim.flags.append("no descent: names no perception in which it can be tested")
        return claim

    def correct(self, claim: Claim, event: CorrectionEvent) -> Claim:
        if event.by == claim.source:
            raise OrganonRefused(
                "A source cannot certify its own claim: that would be logic as an organon."
            )
        claim.corrections.append(event)
        claim.stage = self._stage(claim)
        return claim

    @staticmethod
    def _stage(claim: Claim) -> Stage:
        if claim.refuted:
            return Stage.PERCEPTION
        if claim.reach.widens(Reach.SELF) and claim.correctable:
            return Stage.EXPERIENCE
        return Stage.PERCEPTION

    def open_questions(self, claim: Claim) -> List[str]:
        """What a human being still has to judge before acting on the claim."""
        qs = list(claim.flags)
        if claim.stage is Stage.PERCEPTION:
            qs.append("holds only for its source so far")
        return qs
