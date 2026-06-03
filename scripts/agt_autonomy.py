#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.autonomy import PlanetaryAutonomyRuntime


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run AGI-GAIA-TECHNE planetary autonomy cycles."
    )
    parser.add_argument("--db", default="memory/planetary_memory.db")
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--interval", type=float, default=60.0)
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cycles = 1 if args.once else max(args.cycles, 1)
    runtime = PlanetaryAutonomyRuntime(
        db_path=args.db,
        urls=args.url or None,
        interval_seconds=args.interval,
    )
    report = runtime.run(max_cycles=cycles)

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("# AGI-GAIA-TECHNE Autonomy Report\n")
        print(f"run_id={report.run_id}")
        print(f"status={report.status}")
        print(report.summary)
        for cycle in report.cycles:
            print(
                f"- cycle={cycle.cycle_index} ok={cycle.ok} "
                f"observations={cycle.observations} learned_terms={cycle.learned_terms}"
            )
            if cycle.errors:
                print(f"  errors={'; '.join(cycle.errors)}")
            print(f"  {cycle.model_summary}")

    return 0 if report.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
