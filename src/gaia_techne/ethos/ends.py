"""Ends and their acknowledgment.

Chapter I ("What should I do?"): the runtime is technically practical only.
Rules of skill hold under ends they do not set, so the runtime never creates
an end. An end exists for the runtime only when a community has stated it in
public and acknowledged it, and it stays open to dissent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

from ..koinos.ground import refuse_ground_as_subject


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    """Raised when the runtime itself tries to set an end."""


class EndsRegistry:
    """Public register of ends. The runtime reads it; only people write to it."""

    MACHINE_AUTHORS = {"runtime", "gaia-techne", "model", "system"}

    def __init__(self) -> None:
        self._ends: Dict[str, End] = {}

    def propose(self, end_id: str, statement: str, proposed_by: str, community: str) -> End:
        refuse_ground_as_subject(proposed_by)
        if proposed_by.strip().lower() in self.MACHINE_AUTHORS:
            raise EndProposedByMachine(
                "The runtime is technically practical only: it cannot set the ends "
                "under which its own rules hold."
            )
        if end_id in self._ends:
            raise ValueError(f"end {end_id!r} already registered")
        end = End(end_id=end_id, statement=statement, proposed_by=proposed_by, community=community)
        self._ends[end_id] = end
        return end

    def acknowledge(self, end_id: str, person: str, accepts: bool = True, reason: str = "") -> End:
        refuse_ground_as_subject(person)
        if person.strip().lower() in self.MACHINE_AUTHORS:
            raise EndProposedByMachine("Only people can acknowledge an end.")
        end = self.get(end_id)
        end.acknowledgments.append(Acknowledgment(person=person, accepts=accepts, reason=reason))
        return end

    def derive(self, parent_id: str, end_id: str, statement: str, derived_by: str) -> End:
        """Record an instrumental end that a system derived from an acknowledged one.

        The processes by which a system forms and revises the ends it pursues
        must be public and open to "any of us". A derived end is recorded, linked
        to its parent, and stays unusable until a person acknowledges it.
        """
        parent = self.get(parent_id)
        if not parent.is_acknowledged:
            raise ValueError(f"cannot derive from {parent_id!r}: it has not been acknowledged")
        if end_id in self._ends:
            raise ValueError(f"end {end_id!r} already registered")
        end = End(
            end_id=end_id,
            statement=statement,
            proposed_by=derived_by,
            community=parent.community,
            parent_id=parent_id,
            derived_by_machine=derived_by.strip().lower() in self.MACHINE_AUTHORS,
        )
        self._ends[end_id] = end
        return end

    def revise(self, end_id: str, new_statement: str, by: str, reason: str) -> End:
        """Change an end's statement, keeping the old one public. A revision clears acknowledgment."""
        end = self.get(end_id)
        end.revisions.append({"from": end.statement, "to": new_statement, "by": by, "reason": reason, "at": _now()})
        end.statement = new_statement
        end.acknowledgments = []
        return end

    def get(self, end_id: str) -> End:
        if end_id not in self._ends:
            raise KeyError(f"no end {end_id!r}: the runtime cannot act without a stated end")
        return self._ends[end_id]

    def find(self, end_id: str) -> Optional[End]:
        return self._ends.get(end_id)

    def all(self) -> List[End]:
        return list(self._ends.values())
