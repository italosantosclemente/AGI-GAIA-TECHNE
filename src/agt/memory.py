from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from .types import MemoryKind


@dataclass(frozen=True)
class MemoryRecord:
    kind: MemoryKind
    key: str
    value: str
    tags: List[str]
    created_at: float
    version: int = 1


class MemoryStore:
    """
    Simple JSONL memory.

    This is intentionally minimal and auditable.

    Memory kinds:
    - episodic;
    - semantic;
    - procedural;
    - normative.
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
    ) -> MemoryRecord:
        record = MemoryRecord(
            kind=kind,
            key=key,
            value=value,
            tags=tags or [],
            created_at=time.time(),
            version=1,
        )

        with self.path.open("a", encoding="utf-8") as f:
            payload = asdict(record)
            payload["kind"] = record.kind.value
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

        return record

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
                data = json.loads(line)

                if kind is not None and data["kind"] != kind.value:
                    continue

                blob = " ".join(
                    [
                        data.get("key", ""),
                        data.get("value", ""),
                        " ".join(data.get("tags", [])),
                    ]
                ).lower()

                if q in blob:
                    out.append(
                        MemoryRecord(
                            kind=MemoryKind(data["kind"]),
                            key=data["key"],
                            value=data["value"],
                            tags=data.get("tags", []),
                            created_at=data["created_at"],
                            version=data.get("version", 1),
                        )
                    )

        return out[-limit:]
