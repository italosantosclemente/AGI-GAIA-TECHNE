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

Intuition is that "at which all thought as a means is directed as an end"
(KrV A:19/B:33); the genuine concept turns away from intuition only to lead
back to it the more surely (ECW 13:356), and the transition to symbols
"demands their conservation", not the abandonment of schemata (Pringe, 2007,
p. 188). The canon questions what it is given as an appointed judge who
compels the witnesses to answer (KrV B:XIII; ECW 10:6).
"""

from __future__ import annotations

from typing import List

from ..koinos.ground import refuse_ground_as_subject
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
        if not claim.determines_object:
            # Shared, not corrected: no procedure of correction is required.
            return claim
        if not claim.procedures:
            claim.flags.append("untestable: no public procedure yet; requires human verification before use")
        elif not claim.correctable:
            claim.flags.append("restricted: correction reserved to those who own the means")
        if claim.direction is Direction.AWAY_FROM_LIFE and not claim.returns_to_perception:
            claim.flags.append("no descent: names no perception in which it can be tested")
        return claim

    def correct(self, claim: Claim, event: CorrectionEvent) -> Claim:
        refuse_ground_as_subject(event.by)
        if event.by == claim.source:
            raise OrganonRefused(
                "A source cannot certify its own claim: that would be logic as an organon."
            )
        claim.corrections.append(event)
        claim.stage = self._stage(claim)
        return claim

    def verify(self, claim: Claim, person: str) -> Claim:
        """Human verification of a claim that cannot yet be tested by a public procedure.

        Verification does not widen reach: it records who takes responsibility for
        using an untested result, which is the form that responsibility for the
        system's ends takes when no autonomy is ascribed to it.
        """
        refuse_ground_as_subject(person)
        if person == claim.source:
            raise OrganonRefused("A source cannot verify its own claim.")
        claim.verified_by.append(person)
        return claim

    def usable(self, claim: Claim) -> bool:
        """A claim may be acted on if it has been upheld by others or verified by a person."""
        return claim.stage in (Stage.EXPERIENCE, Stage.SHARED) or bool(claim.verified_by)

    @staticmethod
    def _stage(claim: Claim) -> Stage:
        if not claim.determines_object:
            # Dissent does not refute a claim of this kind: it only shows that agreement
            # is ascribed, not postulated (AA 5:216).
            return Stage.SHARED if claim.reach.widens(Reach.SELF) else Stage.PERCEPTION
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
