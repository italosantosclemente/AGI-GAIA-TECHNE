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

from agt.controller import AGTController


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run AGI-GAIA-TECHNE functional controller."
    )

    parser.add_argument("--task", required=True)
    parser.add_argument("--context", default="")
    parser.add_argument("--memory", default="memory/planetary_memory.db")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    controller = AGTController(memory_path=args.memory)
    report = controller.run(args.task, context=args.context)

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))

    else:
        print("# AGI-GAIA-TECHNE Functional Report\n")
        print(f"**Decision:** {report.decision.value}")
        print(f"**Audit:** {', '.join(report.audit_statuses)}")
        print("\n## Final answer\n")
        print(report.final_answer)

        if report.recommendations:
            print("\n## Recommendations")
            for rec in report.recommendations:
                print(f"- {rec}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
