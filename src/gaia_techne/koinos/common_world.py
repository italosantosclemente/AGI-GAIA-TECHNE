"""The common world (koinos kosmos).

Chapter II ("What may I hope?"). A common world that no one possesses and that
each participant reconstructs by their own efforts. In engineering terms: an
append-only, public, attributable record. Nobody, including the operator,
can rewrite an entry unnoticed; corrections are new entries that point to old
ones. Technology first creates a community of fate among those who work in it;
the record lets that community see and contest the ends it serves, which is the
only way it can be hoped to become a community of wills.

Integrity. Each entry keeps a canonical JSON snapshot of its payload, taken at
the moment of recording, and a SHA-256 digest of everything it says, chained to
the digest of the entry before it. `verify()` recomputes every digest and every
link, so that changing a payload, an author, a time or the order of entries is
detected, not only a forged digest. An entry can refer only to an earlier one.

Persistence. `dump()` writes the record as JSON Lines, one entry per line;
`load()` reads it back and refuses a record that does not verify. Anyone with
the file can check it without trusting whoever kept it.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

from ..boundaries import refuse_ground_as_subject, require_author

GENESIS = "genesis"


def canonical(obj: Any) -> str:
    """The one serialization from which digests are computed."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _digest(index: int, author: str, kind: str, payload_json: str, refers_to: Optional[int], previous: str, at: str) -> str:
    body = canonical(
        {"index": index, "author": author, "kind": kind, "payload": payload_json, "refers_to": refers_to, "prev": previous, "at": at}
    )
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class TamperedRecord(ValueError):
    """Raised when a stored record does not verify."""


@dataclass(frozen=True)
class Entry:
    index: int
    author: str
    kind: str
    payload_json: str  # canonical snapshot taken when the entry was recorded
    refers_to: Optional[int]
    previous_hash: str
    at: str
    digest: str

    @property
    def payload(self) -> Dict[str, Any]:
        """A fresh copy: changing it cannot change the record."""
        return json.loads(self.payload_json)

    def expected_digest(self) -> str:
        return _digest(self.index, self.author, self.kind, self.payload_json, self.refers_to, self.previous_hash, self.at)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "author": self.author,
            "kind": self.kind,
            "payload": self.payload,
            "refers_to": self.refers_to,
            "previous_hash": self.previous_hash,
            "at": self.at,
            "digest": self.digest,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Entry":
        return cls(
            index=d["index"],
            author=d["author"],
            kind=d["kind"],
            payload_json=canonical(d["payload"]),
            refers_to=d.get("refers_to"),
            previous_hash=d["previous_hash"],
            at=d["at"],
            digest=d["digest"],
        )


@dataclass
class CommonWorld:
    participants: Set[str] = field(default_factory=set)
    _entries: List[Entry] = field(default_factory=list)
    clock: Callable[[], str] = field(default=_utc_now, repr=False)

    def join(self, person: str) -> None:
        refuse_ground_as_subject(person)
        self.participants.add(person)

    def record(self, author: str, kind: str, payload: Dict[str, Any], refers_to: Optional[int] = None) -> Entry:
        require_author(author)
        refuse_ground_as_subject(author)
        if refers_to is not None and not 0 <= refers_to < len(self._entries):
            raise ValueError(f"entry {refers_to} does not exist yet: an entry can refer only to an earlier one")
        index = len(self._entries)
        previous = self.head
        at = self.clock()
        payload_json = canonical(payload)
        entry = Entry(
            index=index,
            author=author,
            kind=kind,
            payload_json=payload_json,
            refers_to=refers_to,
            previous_hash=previous,
            at=at,
            digest=_digest(index, author, kind, payload_json, refers_to, previous, at),
        )
        self._entries.append(entry)
        return entry

    @property
    def head(self) -> str:
        return self._entries[-1].digest if self._entries else GENESIS

    def __len__(self) -> int:
        return len(self._entries)

    def entries(self) -> List[Entry]:
        return list(self._entries)

    def find(self, kind: Optional[str] = None, refers_to: Optional[int] = None) -> List[Entry]:
        return [
            e
            for e in self._entries
            if (kind is None or e.kind == kind) and (refers_to is None or e.refers_to == refers_to)
        ]

    def first_invalid(self) -> Optional[int]:
        """Index of the first entry that does not verify, or None if the whole record does."""
        previous = GENESIS
        for i, e in enumerate(self._entries):
            if e.index != i or e.previous_hash != previous or e.digest != e.expected_digest():
                return i
            if e.refers_to is not None and not 0 <= e.refers_to < i:
                return i
            previous = e.digest
        return None

    def verify(self) -> bool:
        """Anyone can check that no entry was rewritten, removed or reordered."""
        return self.first_invalid() is None

    def dump(self, path: Union[str, Path]) -> Path:
        path = Path(path)
        with path.open("w", encoding="utf-8") as f:
            for e in self._entries:
                f.write(canonical(e.to_dict()) + "\n")
        return path

    @classmethod
    def load(cls, path: Union[str, Path]) -> "CommonWorld":
        world = cls()
        with Path(path).open(encoding="utf-8") as f:
            for n, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    world._entries.append(Entry.from_dict(json.loads(line)))
                except (KeyError, TypeError, json.JSONDecodeError) as exc:
                    raise TamperedRecord(f"line {n} is not an entry of the common world: {exc}") from exc
        bad = world.first_invalid()
        if bad is not None:
            raise TamperedRecord(f"entry {bad} does not verify: the record was changed after it was written")
        return world
