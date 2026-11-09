"""The common world (koinos kosmos).

Chapter II ("What may I hope?"). A common world that no one possesses and that
each participant reconstructs by their own efforts. In engineering terms: an
append-only, public, attributable record. Nobody, including the operator,
can rewrite an entry; corrections are new entries that point to old ones.
Technology first creates a community of fate among those who work in it; the
record lets that community see and contest the ends it serves, which is the
only way it can be hoped to become a community of wills.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from .ground import refuse_ground_as_subject


@dataclass(frozen=True)
class Entry:
    index: int
    author: str
    kind: str
    payload: Dict[str, Any]
    refers_to: Optional[int]
    previous_hash: str
    at: str
    digest: str


@dataclass
class CommonWorld:
    participants: Set[str] = field(default_factory=set)
    _entries: List[Entry] = field(default_factory=list)

    def join(self, person: str) -> None:
        self.participants.add(person)

    def record(self, author: str, kind: str, payload: Dict[str, Any], refers_to: Optional[int] = None) -> Entry:
        refuse_ground_as_subject(author)
        previous = self._entries[-1].digest if self._entries else "genesis"
        at = datetime.now(timezone.utc).isoformat()
        body = json.dumps(
            {"author": author, "kind": kind, "payload": payload, "refers_to": refers_to, "prev": previous, "at": at},
            sort_keys=True,
            default=str,
        )
        entry = Entry(
            index=len(self._entries),
            author=author,
            kind=kind,
            payload=payload,
            refers_to=refers_to,
            previous_hash=previous,
            at=at,
            digest=hashlib.sha256(body.encode()).hexdigest(),
        )
        self._entries.append(entry)
        return entry

    def entries(self) -> List[Entry]:
        return list(self._entries)

    def verify(self) -> bool:
        """Anyone can check that no entry was rewritten."""
        previous = "genesis"
        for e in self._entries:
            if e.previous_hash != previous:
                return False
            previous = e.digest
        return True
