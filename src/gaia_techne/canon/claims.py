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

    @property
    def reach(self) -> Reach:
        """Widest community whose members upheld the claim, by others than its source."""
        upheld = [c.community_reach for c in self.corrections if c.upheld and c.by != self.source]
        if not upheld:
            return Reach.SELF
        return max(upheld, key=lambda r: r.value)

    @property
    def correctable(self) -> bool:
        return any(p.public for p in self.procedures)

    @property
    def refuted(self) -> bool:
        return any(not c.upheld for c in self.corrections)
