"""Ends and their acknowledgment.

Chapter I ("What should I do?"): the runtime is technically practical only.
Rules of skill hold under ends they do not set, so the runtime never creates
an end. An end exists for the runtime only when a community has stated it in
public and acknowledged it, and it stays open to dissent.

"In public" is enforced, not declared: when the registry is given a record
(any object with the `record(author, kind, payload, refers_to)` method of
`koinos.CommonWorld`), every proposal, acknowledgment, dissent, derivation and
revision is written to it. The ethos layer does not import the koinos layer;
the runtime hands the record to it, so the order of the layers is kept.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Protocol

from ..boundaries import is_machine, refuse_ground_as_subject, require_author


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class PublicRecord(Protocol):
    def record(self, author: str, kind: str, payload: Dict[str, Any], refers_to: Optional[int] = None) -> Any: ...


@dataclass(frozen=True)
class Acknowledgment:
    """A person's public acknowledgment of (or dissent from) an end."""

    person: str
    accepts: bool
    reason: str = ""
    at: str = field(default_factory=_now)


@dataclass
class End:
    """An end stated by human beings, never by the runtime.

    `statement` must be phrased so that it could be addressed to "any of us":
    the registry does not test universality (no machine can), it only keeps the
    statement public, attributable and contestable.
    """

    end_id: str
    statement: str
    proposed_by: str
    community: str
    acknowledgments: List[Acknowledgment] = field(default_factory=list)
    parent_id: Optional[str] = None  # set when the end was derived from another
    derived_by_machine: bool = False
    revisions: List[Dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    recorded_at: Optional[int] = None  # index of the entry that made the end public

    @property
    def accepted_by(self) -> List[str]:
        return [a.person for a in self.acknowledgments if a.accepts]

    @property
    def contested_by(self) -> List[str]:
        return [a.person for a in self.acknowledgments if not a.accepts]

    @property
    def is_acknowledged(self) -> bool:
        return len(self.accepted_by) > 0

    @property
    def is_contested(self) -> bool:
        return len(self.contested_by) > 0


class EndProposedByMachine(ValueError):
    """Raised when the runtime itself tries to set, acknowledge or revise an end."""


class AllowanceSetByMachine(EndProposedByMachine):
    """Raised when the runtime tries to set or widen the allowance of the ground it draws on.

    How much of a planet a task may draw is decided under ends, by people.
    """


class EndsRegistry:
    """Public register of ends. The runtime reads it; only people write to it.

    `machine_authors` adds the names under which a runtime presents itself to the
    default names of `gaia_techne.boundaries`, so that no alias of the system can
    set, acknowledge or revise an end.
    """

    def __init__(self, record: Optional[PublicRecord] = None, machine_authors: Iterable[str] = ()) -> None:
        self._ends: Dict[str, End] = {}
        self.record = record
        self.machine_authors = set(machine_authors)

    # -- who may write -------------------------------------------------------

    def _person(self, who: str, act: str) -> None:
        require_author(who)
        refuse_ground_as_subject(who)
        if is_machine(who, self.machine_authors):
            raise EndProposedByMachine(
                f"The runtime is technically practical only: it cannot {act} "
                "the ends under which its own rules hold."
            )

    def _publish(self, author: str, kind: str, payload: Dict[str, Any], refers_to: Optional[int] = None) -> Optional[int]:
        if self.record is None:
            return None
        entry = self.record.record(author=author, kind=kind, payload=payload, refers_to=refers_to)
        return getattr(entry, "index", None)

    # -- acts ----------------------------------------------------------------

    def propose(self, end_id: str, statement: str, proposed_by: str, community: str) -> End:
        self._person(proposed_by, "set")
        if end_id in self._ends:
            raise ValueError(f"end {end_id!r} already registered")
        end = End(end_id=end_id, statement=statement, proposed_by=proposed_by, community=community)
        end.recorded_at = self._publish(
            proposed_by,
            "end_proposed",
            {"end_id": end_id, "statement": statement, "proposed_by": proposed_by, "community": community},
        )
        self._ends[end_id] = end
        return end

    def acknowledge(self, end_id: str, person: str, accepts: bool = True, reason: str = "") -> End:
        self._person(person, "acknowledge")
        end = self.get(end_id)
        end.acknowledgments.append(Acknowledgment(person=person, accepts=accepts, reason=reason))
        self._publish(
            person,
            "end_acknowledged",
            {"end_id": end_id, "person": person, "accepts": accepts, "reason": reason},
            refers_to=end.recorded_at,
        )
        return end

    def derive(self, parent_id: str, end_id: str, statement: str, derived_by: str) -> End:
        """Record an instrumental end that a system derived from an acknowledged one.

        The processes by which a system forms and revises the ends it pursues
        must be public and open to "any of us". A derived end is recorded, linked
        to its parent, and stays unusable until a person acknowledges it.
        """
        require_author(derived_by)
        refuse_ground_as_subject(derived_by)
        parent = self.get(parent_id)
        if not parent.is_acknowledged:
            raise ValueError(f"cannot derive from {parent_id!r}: it has not been acknowledged")
        if end_id in self._ends:
            raise ValueError(f"end {end_id!r} already registered")
        by_machine = is_machine(derived_by, self.machine_authors)
        end = End(
            end_id=end_id,
            statement=statement,
            proposed_by=derived_by,
            community=parent.community,
            parent_id=parent_id,
            derived_by_machine=by_machine,
        )
        end.recorded_at = self._publish(
            derived_by,
            "end_derived",
            {"end_id": end_id, "parent": parent_id, "statement": statement, "derived_by": derived_by, "derived_by_machine": by_machine},
            refers_to=parent.recorded_at,
        )
        self._ends[end_id] = end
        return end

    def revise(self, end_id: str, new_statement: str, by: str, reason: str) -> End:
        """Change an end's statement, keeping the old one public. A revision clears acknowledgment.

        The runtime cannot revise an end: it may derive a new one, which then waits for people.
        """
        self._person(by, "revise")
        end = self.get(end_id)
        end.revisions.append({"from": end.statement, "to": new_statement, "by": by, "reason": reason, "at": _now()})
        self._publish(
            by,
            "end_revised",
            {"end_id": end_id, "from": end.statement, "to": new_statement, "by": by, "reason": reason},
            refers_to=end.recorded_at,
        )
        end.statement = new_statement
        end.acknowledgments = []
        return end

    # -- reading -------------------------------------------------------------

    def get(self, end_id: str) -> End:
        if end_id not in self._ends:
            raise KeyError(f"no end {end_id!r}: the runtime cannot act without a stated end")
        return self._ends[end_id]

    def find(self, end_id: str) -> Optional[End]:
        return self._ends.get(end_id)

    def all(self) -> List[End]:
        return list(self._ends.values())
