from __future__ import annotations

import json
import os
import platform
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from .memory import MemoryStore, SQLiteMemoryStore
from .planetary_model import PlanetarySymbolicModel
from .world_ingestion import IngestionResult, InternetIngestor


DEFAULT_HEARTBEAT_URL = "data:text/plain,AGI-GAIA-TECHNE planetary heartbeat"


@dataclass(frozen=True)
class AutonomyCycleReport:
    cycle_index: int
    observations: int
    learned_terms: int
    ok: bool
    errors: List[str]
    model_summary: str


@dataclass(frozen=True)
class AutonomyRunReport:
    run_id: int
    cycles: List[AutonomyCycleReport]
    status: str
    summary: str

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "summary": self.summary,
            "cycles": [asdict(cycle) for cycle in self.cycles],
        }


class PlanetaryAutonomyRuntime:
    """
    Persistent autonomy loop for AGI-GAIA-TECHNE.

    It does not claim full AGI. It implements the missing operational loop:
    perception -> ingestion -> memory -> local model training -> run ledger.
    """

    def __init__(
        self,
        db_path: str = "memory/planetary_memory.db",
        urls: Optional[Iterable[str]] = None,
        interval_seconds: float = 60.0,
        lock_path: Optional[str] = None,
    ) -> None:
        self.memory = _ensure_sqlite_memory(db_path)
        self.model = PlanetarySymbolicModel(self.memory)
        self.ingestor = InternetIngestor(self.memory, self.model)
        self.urls = list(urls or [DEFAULT_HEARTBEAT_URL])
        self.interval_seconds = interval_seconds
        self.lock_path = Path(lock_path or str(Path(db_path).with_suffix(".lock")))

    def run_once(self) -> AutonomyRunReport:
        return self.run(max_cycles=1)

    def run(self, max_cycles: int = 1) -> AutonomyRunReport:
        with _FileLock(self.lock_path):
            run_id = self.memory.start_run(
                {
                    "urls": self.urls,
                    "interval_seconds": self.interval_seconds,
                    "max_cycles": max_cycles,
                }
            )
            cycles: List[AutonomyCycleReport] = []
            status = "completed"

            try:
                for index in range(max_cycles):
                    cycles.append(self._cycle(index + 1))
                    if index + 1 < max_cycles:
                        time.sleep(self.interval_seconds)
            except Exception as exc:
                status = "error"
                cycles.append(
                    AutonomyCycleReport(
                        cycle_index=len(cycles) + 1,
                        observations=0,
                        learned_terms=0,
                        ok=False,
                        errors=[str(exc)],
                        model_summary=self.model.summarize(),
                    )
                )

            summary = self._summary(cycles)
            self.memory.finish_run(run_id, status, len(cycles), summary)
            return AutonomyRunReport(run_id=run_id, cycles=cycles, status=status, summary=summary)

    def _cycle(self, cycle_index: int) -> AutonomyCycleReport:
        heartbeat = self._system_heartbeat()
        heartbeat_observation = self.memory.add_observation(
            source="system",
            url="system://heartbeat",
            title="Planetary autonomy heartbeat",
            content=heartbeat,
            status="observed",
            metadata={"cycle_index": cycle_index},
        )
        heartbeat_learning = self.model.train_text(
            heartbeat,
            observation_id=heartbeat_observation.id,
        )

        results = self.ingestor.ingest_many(self.urls)
        errors = [result.error or "unknown ingestion error" for result in results if not result.ok]
        learned_terms = heartbeat_learning.term_count + sum(
            result.learning.term_count
            for result in results
            if result.learning is not None
        )
        observations = 1 + sum(1 for result in results if result.observation is not None)

        self.memory.record_event(
            "autonomy_cycle",
            f"cycle:{cycle_index}",
            {
                "cycle_index": cycle_index,
                "urls": self.urls,
                "observations": observations,
                "errors": errors,
                "ingestion": [_result_payload(result) for result in results],
            },
        )

        return AutonomyCycleReport(
            cycle_index=cycle_index,
            observations=observations,
            learned_terms=learned_terms,
            ok=not errors,
            errors=errors,
            model_summary=self.model.summarize(),
        )

    def _system_heartbeat(self) -> str:
        return json.dumps(
            {
                "runtime": "AGI-GAIA-TECHNE PlanetaryAutonomyRuntime",
                "time": time.time(),
                "platform": platform.platform(),
                "urls": self.urls,
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    def _summary(self, cycles: List[AutonomyCycleReport]) -> str:
        observations = sum(cycle.observations for cycle in cycles)
        learned_terms = sum(cycle.learned_terms for cycle in cycles)
        errors = sum(len(cycle.errors) for cycle in cycles)
        return (
            f"cycles={len(cycles)}; observations={observations}; "
            f"learned_terms={learned_terms}; errors={errors}"
        )


class _FileLock:
    def __init__(self, path: Path) -> None:
        self.path = path

    def __enter__(self) -> "_FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode("utf-8"))
            os.close(fd)
        except FileExistsError as exc:
            raise RuntimeError(f"Autonomy lock already exists: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def _ensure_sqlite_memory(path: str) -> SQLiteMemoryStore:
    store = MemoryStore(path)
    backend = getattr(store, "backend", store)
    if not isinstance(backend, SQLiteMemoryStore):
        raise ValueError("Planetary autonomy requires a SQLite memory path, not JSONL.")
    return backend


def _result_payload(result: IngestionResult) -> dict:
    return {
        "ok": result.ok,
        "url": result.url,
        "bytes_read": result.bytes_read,
        "error": result.error,
        "observation_id": result.observation.id if result.observation else None,
        "top_terms": result.learning.top_terms if result.learning else [],
    }
