from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .types import MemoryKind


@dataclass(frozen=True)
class MemoryRecord:
    kind: MemoryKind
    key: str
    value: str
    tags: List[str]
    created_at: float
    version: int = 1


@dataclass(frozen=True)
class ObservationRecord:
    id: int
    source: str
    url: str
    title: str
    content_hash: str
    observed_at: float
    status: str
    metadata: Dict[str, Any]


class JsonlMemoryStore:
    """
    Backward-compatible JSONL memory.

    This remains available for tests, fixtures and simple local experiments.
    The production default for v10 is SQLiteMemoryStore.
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


class SQLiteMemoryStore:
    """
    Durable planetary memory for AGI-GAIA-TECHNE v10.

    It stores ordinary memories, web observations, learned symbolic terms,
    model document vectors, autonomy runs and public events in a single
    inspectable SQLite database.
    """

    def __init__(self, path: str = "memory/planetary_memory.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self._fts_enabled = False
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS memory_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                tags_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                version INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL UNIQUE,
                observed_at REAL NOT NULL,
                status TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS model_terms (
                term TEXT PRIMARY KEY,
                count INTEGER NOT NULL,
                weight REAL NOT NULL,
                updated_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS model_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER,
                content_hash TEXT NOT NULL,
                term_vector_json TEXT NOT NULL,
                learned_at REAL NOT NULL,
                FOREIGN KEY(observation_id) REFERENCES observations(id)
            );

            CREATE TABLE IF NOT EXISTS autonomy_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at REAL NOT NULL,
                completed_at REAL,
                status TEXT NOT NULL,
                cycles INTEGER NOT NULL,
                summary TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                key TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """
        )

        try:
            self.conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts
                USING fts5(record_id UNINDEXED, key, value, tags);
                """
            )
            self._fts_enabled = True
        except sqlite3.DatabaseError:
            self._fts_enabled = False

        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

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
        tags_json = json.dumps(record.tags, ensure_ascii=False)

        cur = self.conn.execute(
            """
            INSERT INTO memory_records(kind, key, value, tags_json, created_at, version)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record.kind.value,
                record.key,
                record.value,
                tags_json,
                record.created_at,
                record.version,
            ),
        )

        if self._fts_enabled:
            self.conn.execute(
                "INSERT INTO memory_fts(record_id, key, value, tags) VALUES (?, ?, ?, ?)",
                (cur.lastrowid, record.key, record.value, " ".join(record.tags)),
            )

        self.conn.commit()
        return record

    def search(
        self,
        query: str,
        kind: Optional[MemoryKind] = None,
        limit: int = 10,
    ) -> List[MemoryRecord]:
        rows: List[sqlite3.Row]

        if self._fts_enabled and self._fts_query(query):
            match = self._fts_query(query)
            sql = """
                SELECT mr.* FROM memory_records mr
                JOIN memory_fts fts ON fts.record_id = mr.id
                WHERE memory_fts MATCH ?
            """
            params: List[Any] = [match]
            if kind is not None:
                sql += " AND mr.kind = ?"
                params.append(kind.value)
            sql += " ORDER BY mr.created_at DESC LIMIT ?"
            params.append(limit)
            try:
                rows = list(self.conn.execute(sql, params))
            except sqlite3.DatabaseError:
                rows = self._like_search(query, kind, limit)
        else:
            rows = self._like_search(query, kind, limit)

        return [self._row_to_memory_record(row) for row in rows]

    def _like_search(
        self,
        query: str,
        kind: Optional[MemoryKind],
        limit: int,
    ) -> List[sqlite3.Row]:
        like = f"%{query.lower()}%"
        sql = """
            SELECT * FROM memory_records
            WHERE lower(key || ' ' || value || ' ' || tags_json) LIKE ?
        """
        params: List[Any] = [like]
        if kind is not None:
            sql += " AND kind = ?"
            params.append(kind.value)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        return list(self.conn.execute(sql, params))

    def _fts_query(self, query: str) -> str:
        tokens = [
            token
            for token in _tokenize(query)
            if len(token) >= 2
        ][:8]
        return " OR ".join(tokens)

    def _row_to_memory_record(self, row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            kind=MemoryKind(row["kind"]),
            key=row["key"],
            value=row["value"],
            tags=json.loads(row["tags_json"]),
            created_at=row["created_at"],
            version=row["version"],
        )

    def add_observation(
        self,
        source: str,
        url: str,
        title: str,
        content: str,
        status: str = "observed",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ObservationRecord:
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        observed_at = time.time()
        metadata_json = json.dumps(metadata or {}, ensure_ascii=False, sort_keys=True)

        self.conn.execute(
            """
            INSERT OR IGNORE INTO observations(
                source, url, title, content, content_hash, observed_at, status, metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (source, url, title, content, content_hash, observed_at, status, metadata_json),
        )
        self.conn.commit()

        row = self.conn.execute(
            "SELECT * FROM observations WHERE content_hash = ?",
            (content_hash,),
        ).fetchone()
        return self._row_to_observation(row)

    def get_observation_content(self, observation_id: int) -> str:
        row = self.conn.execute(
            "SELECT content FROM observations WHERE id = ?",
            (observation_id,),
        ).fetchone()
        return "" if row is None else row["content"]

    def list_observations(self, limit: int = 10) -> List[ObservationRecord]:
        rows = self.conn.execute(
            "SELECT * FROM observations ORDER BY observed_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [self._row_to_observation(row) for row in rows]

    def _row_to_observation(self, row: sqlite3.Row) -> ObservationRecord:
        return ObservationRecord(
            id=row["id"],
            source=row["source"],
            url=row["url"],
            title=row["title"],
            content_hash=row["content_hash"],
            observed_at=row["observed_at"],
            status=row["status"],
            metadata=json.loads(row["metadata_json"]),
        )

    def upsert_model_terms(self, term_counts: Dict[str, int]) -> None:
        now = time.time()
        total = max(sum(term_counts.values()), 1)
        for term, count in term_counts.items():
            weight = count / total
            self.conn.execute(
                """
                INSERT INTO model_terms(term, count, weight, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(term) DO UPDATE SET
                    count = count + excluded.count,
                    weight = ((weight + excluded.weight) / 2.0),
                    updated_at = excluded.updated_at
                """,
                (term, count, weight, now),
            )
        self.conn.commit()

    def add_model_document(
        self,
        observation_id: Optional[int],
        content_hash: str,
        term_vector: Dict[str, float],
    ) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO model_documents(observation_id, content_hash, term_vector_json, learned_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                observation_id,
                content_hash,
                json.dumps(term_vector, ensure_ascii=False, sort_keys=True),
                time.time(),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def top_model_terms(self, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT term, count, weight, updated_at
            FROM model_terms
            ORDER BY count DESC, weight DESC, term ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def record_event(self, kind: str, key: str, payload: Dict[str, Any]) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO events(kind, key, payload_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (kind, key, json.dumps(payload, ensure_ascii=False, sort_keys=True), time.time()),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def start_run(self, metadata: Optional[Dict[str, Any]] = None) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO autonomy_runs(started_at, completed_at, status, cycles, summary, metadata_json)
            VALUES (?, NULL, ?, 0, ?, ?)
            """,
            (
                time.time(),
                "running",
                "",
                json.dumps(metadata or {}, ensure_ascii=False, sort_keys=True),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def finish_run(self, run_id: int, status: str, cycles: int, summary: str) -> None:
        self.conn.execute(
            """
            UPDATE autonomy_runs
            SET completed_at = ?, status = ?, cycles = ?, summary = ?
            WHERE id = ?
            """,
            (time.time(), status, cycles, summary, run_id),
        )
        self.conn.commit()


class MemoryStore:
    """
    Compatibility facade.

    Paths ending in .jsonl keep the historical append-only store. Any other
    path uses SQLite planetary memory.
    """

    def __init__(self, path: str = "memory/planetary_memory.db") -> None:
        suffix = Path(path).suffix.lower()
        if suffix == ".jsonl":
            self.backend: Any = JsonlMemoryStore(path)
        else:
            self.backend = SQLiteMemoryStore(path)

    def add(
        self,
        kind: MemoryKind,
        key: str,
        value: str,
        tags: Optional[List[str]] = None,
    ) -> MemoryRecord:
        return self.backend.add(kind, key, value, tags)

    def search(
        self,
        query: str,
        kind: Optional[MemoryKind] = None,
        limit: int = 10,
    ) -> List[MemoryRecord]:
        return self.backend.search(query, kind, limit)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.backend, name)


def _tokenize(text: str) -> Iterable[str]:
    token = []
    for char in text.lower():
        if char.isalnum() or char == "_":
            token.append(char)
        elif token:
            yield "".join(token)
            token = []
    if token:
        yield "".join(token)
