#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.memory import MemoryStore, SQLiteMemoryStore
from agt.planetary_model import PlanetarySymbolicModel
from agt.world_ingestion import InternetIngestor


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ingest live symbolic sources into AGI-GAIA-TECHNE planetary memory."
    )
    parser.add_argument("--db", default="memory/planetary_memory.db")
    parser.add_argument("--url", action="append", required=True)
    parser.add_argument("--allow-private-hosts", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    store = MemoryStore(args.db)
    memory = getattr(store, "backend", store)
    if not isinstance(memory, SQLiteMemoryStore):
        raise SystemExit("Live ingestion requires a SQLite memory path, not JSONL.")

    model = PlanetarySymbolicModel(memory)
    ingestor = InternetIngestor(
        memory,
        model=model,
        allow_private_hosts=args.allow_private_hosts,
    )
    results = ingestor.ingest_many(args.url)

    if args.json:
        payload = [
            {
                "ok": result.ok,
                "url": result.url,
                "bytes_read": result.bytes_read,
                "error": result.error,
                "observation": asdict(result.observation) if result.observation else None,
                "learning": asdict(result.learning) if result.learning else None,
            }
            for result in results
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("# AGI-GAIA-TECHNE Ingestion Report\n")
        for result in results:
            status = "OK" if result.ok else "TRANSMUTE"
            print(f"- [{status}] {result.url}")
            if result.learning:
                print(f"  learned_terms={result.learning.term_count}")
                print(f"  top_terms={', '.join(result.learning.top_terms)}")
            if result.error:
                print(f"  error={result.error}")
        print("\n" + model.summarize())

    return 1 if any(not result.ok for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
