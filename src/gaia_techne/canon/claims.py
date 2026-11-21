"""Claims: the unit of everything the runtime produces.

Chapter III ("What can I know?"). Every output is a claim, never a truth.
A claim begins as a judgment of perception, holding only "for me" (for the
source or model that produced it). It can become a judgment of experience,
holding "for everyone", only through public procedures of correction carried
out by others (Prolegomena, AA 4:298). Its degree of "objectivity" is the
reach and correctability of the claim, not the dignity of the form that
raised it.

No stage is final. The physical object is a limit-idea, and it can never be
asserted that the last "invariants of experience" have been reached (ECW
13:552-553): "We do not need the objectivity of absolute things, but we do need
the objective determinateness of the path of experience itself" (ECW 13:553).

"All of our judgments are at first mere judgments of perception" (AA 4:298):
every output starts at PERCEPTION. There is no general criterion of truth
(KrV A:58/B:82), and so no field here declares a claim true; the context of
experience "is the measure, not the measured" (ECN 1:117).

Reach. The reach of a claim is the extent of the community before which it
can be tested by its grounds, and its correctability the availability of a
public procedure by which others can measure it "and, if it fails, revise it"
(thesis, subsection 10.4). Three consequences are enforced here:

- only corrections made by others through public procedures count. A claim
  that refuses to be tested by those who do not already share it "has no more
  reach than the community that holds it" (thesis, 10.4), so a correction
  reserved to those who own the means widens nothing;
- the ascent and the return together give a claim its reach: a claim of
  signification that names no perception in which it can be tested cannot be
  communicated (thesis, 10.4; ECW 13:555-556), and its reach stays with its
  source;
- a claim about an object that anyone has refuted by a public procedure
  returns to perception with the reach of its source, and it is revised, not
  re-ascended: the revision is a new claim, which starts again as a judgment
  of perception.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from ..koinos.prism import Direction, SymbolicFunction


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Stage(Enum):
    """Not a ranking: SHARED is a universality of another kind, not a lower degree.

    "Objectivity" implies intersubjectivity, but intersubjectivity does not imply
    "objectivity". What claims to hold for everyone without determining an object
    of possible experience (as the judgment of taste does, whose "universal
    voice is thus only an idea", AA 5:216) is intersubjective without being
    "objective".
    """

    PERCEPTION = "holds for me"  # judgment of perception
    EXPERIENCE = "holds for everyone it has been tested before"  # judgment of experience: intersubjective and objective
    SHARED = "shared by others without determining an object"  # intersubjective, not objective

    def _refuse(self, other):
        raise TypeError("Stages are not ranked: SHARED is not a lower degree of EXPERIENCE.")

    __lt__ = __le__ = __gt__ = __ge__ = _refuse


class Reach(Enum):
    """Extent of the community before which a claim can be tested by its grounds."""

    SELF = 1  # the source in its present state
    FORM_OF_LIFE = 2  # a community sharing a form of life or of expression
    EVERYONE = 3  # anyone who has reason

    def widens(self, other: "Reach") -> bool:
        return self.value > other.value


class ProcedureKind(Enum):
    """Public procedures of correction. Each symbolic form has its own."""

    REPETITION = "repetition of an observation"
    EXPERIMENT = "experiment devised under the guidance of a law"
    SOURCE_CRITIQUE = "critique of a source"
    TRADITION = "comparison of a work with the works of a tradition"
    PROOF = "proof"
    REVIEW = "public review by those affected"


@dataclass(frozen=True)
class Procedure:
    kind: ProcedureKind
    description: str
    public: bool = True  # can anyone carry it out?
    restricted_to: str = ""  # who owns the means, if not public


@dataclass(frozen=True)
class CorrectionEvent:
    """Someone other than the source measured the claim by a procedure."""

    by: str
    procedure: ProcedureKind
    upheld: bool
    community_reach: Reach
    note: str = ""
    at: str = field(default_factory=_now)
    public: bool = True  # was the procedure carried out one that anyone could carry out?


@dataclass
class Claim:
    claim_id: str
    content: str
    source: str  # person, model or dataset that raised it
    end_id: str  # the acknowledged end under which it was produced
    function: SymbolicFunction
    direction: Direction
    determines_object: bool = True  # False: claims to hold for everyone without an object of possible experience
    grounds: List[str] = field(default_factory=list)
    procedures: List[Procedure] = field(default_factory=list)
    corrections: List[CorrectionEvent] = field(default_factory=list)
    stage: Stage = Stage.PERCEPTION
    returns_to_perception: Optional[str] = None  # the perception in which it can be tested
    flags: List[str] = field(default_factory=list)
    ground: List[str] = field(default_factory=list)  # geomorphic dependencies of the run
    verified_by: List[str] = field(default_factory=list)  # human verification where no test exists yet
    created_at: str = field(default_factory=_now)
    exposed_at: Optional[int] = None  # index of the entry that offered the claim to others (Exposure)
    revises: Optional[str] = None  # claim_id of the claim this one revises
    revised_by: Optional[str] = None  # claim_id of the claim that revised this one

    def counts(self, c: CorrectionEvent) -> bool:
        """A correction measures the claim only if someone else made it through a public procedure.

        A correction by the owner of a restricted procedure of the same kind is not
        public, whatever the event says of itself.
        """
        if c.by == self.source or not c.public:
            return False
        for p in self.procedures:
            if p.kind is c.procedure and not p.public and p.restricted_to and c.by == p.restricted_to:
                return False
        return True

    @property
    def has_descent(self) -> bool:
        """A claim of signification names the perception in which anyone can test it."""
        return self.direction is not Direction.AWAY_FROM_LIFE or bool(self.returns_to_perception)

    @property
    def refuted(self) -> bool:
        """Refuted by anyone, through a public procedure. Dissent does not refute a claim that determines no object."""
        return self.determines_object and any(not c.upheld for c in self.corrections if self.counts(c))

    @property
    def reach(self) -> Reach:
        """Widest community before which others upheld the claim through public procedures.

        Never the number of those who upheld it. A refuted claim about an object, or a
        claim of signification without descent, keeps the reach of its source.
        """
        if self.determines_object and (self.refuted or not self.has_descent):
            return Reach.SELF
        upheld = [c.community_reach for c in self.corrections if c.upheld and self.counts(c)]
        if not upheld:
            return Reach.SELF
        return max(upheld, key=lambda r: r.value)

    @property
    def correctable(self) -> bool:
        return any(p.public for p in self.procedures)
