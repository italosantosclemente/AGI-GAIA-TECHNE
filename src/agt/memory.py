from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .types import MemoryKind
from .version import MEMORY_SCHEMA_VERSION


@dataclass(frozen=True)
class MemoryRecord:
    record_id: str
    kind: MemoryKind
    key: str
    value: str
    content_hash: str
    tags: List[str]
    created_at: float
    schema_version: str = "1.0.0"
    source: str = "AGTController"


class MemoryStore:
    """
    Robust JSONL memory store with integrity checks.
    """

    def __init__(self, path: str = "memory/agt_memory.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(
        self,
        kind: MemoryKind,
        key: str,
        value: str,
        tags: Optional[List[str]] = None,
        source: str = "AGTController",
    ) -> MemoryRecord:
        content_hash = self._hash(kind, key, value)
        record = MemoryRecord(
            record_id=str(uuid.uuid4()),
            kind=kind,
            key=key,
            value=value,
            content_hash=content_hash,
            tags=tags or [],
            created_at=time.time(),
            schema_version=MEMORY_SCHEMA_VERSION,
            source=source,
        )

        self._write(record)
        return record

    def add_once(
        self,
        kind: MemoryKind,
        key: str,
        value: str,
        tags: Optional[List[str]] = None,
        source: str = "AGTController",
    ) -> Optional[MemoryRecord]:
        """
        Add a record only if it doesn't already exist (deduplicated by kind, key and content_hash).
        """
        content_hash = self._hash(kind, key, value)
        existing = self.search_exact(kind, key, content_hash)

        if existing:
            return None

        return self.add(kind, key, value, tags, source)

    def search(
        self,
        query: str,
        kind: Optional[MemoryKind] = None,
        limit: int = 10,
    ) -> List[MemoryRecord]:
        if not self.path.exists():
            return []

        q = query.lower()
        out = []

        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if kind is not None and data.get("kind") != kind.value:
                        continue

                    blob = " ".join(
                        [
                            data.get("key", ""),
                            data.get("value", ""),
                            " ".join(data.get("tags", [])),
                        ]
                    ).lower()

                    if q in blob:
                        out.append(self._to_record(data))
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        return out[-limit:]

    def search_exact(self, kind: MemoryKind, key: str, content_hash: str) -> Optional[MemoryRecord]:
        if not self.path.exists():
            return None

        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if (data.get("kind") == kind.value and
                        data.get("key") == key and
                        data.get("content_hash") == content_hash):
                        return self._to_record(data)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
        return None

    def _write(self, record: MemoryRecord) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            payload = asdict(record)
            payload["kind"] = record.kind.value
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _hash(self, kind: MemoryKind, key: str, value: str) -> str:
        blob = f"{kind.value}:{key}:{value}"
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def _to_record(self, data: Dict[str, Any]) -> MemoryRecord:
        return MemoryRecord(
            record_id=data.get("record_id", str(uuid.uuid4())),
            kind=MemoryKind(data["kind"]),
            key=data["key"],
            value=data["value"],
            content_hash=data.get("content_hash", ""),
            tags=data.get("tags", []),
            created_at=data["created_at"],
            schema_version=data.get("schema_version", MEMORY_SCHEMA_VERSION),
            source=data.get("source", "AGTController"),
        )
