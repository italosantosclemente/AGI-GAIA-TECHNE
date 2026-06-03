from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.planetary_telemetry import PlanetaryTelemetry, format_telemetry_markdown


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Gaia-Techne planetary telemetry: the command behind 'fazer telemetria'."
    )
    parser.add_argument("--json", action="store_true", help="Emit the sourced telemetry report as JSON.")
    parser.add_argument("--timeout", type=int, default=6, help="Network timeout per public source.")
    args = parser.parse_args()

    report = PlanetaryTelemetry(timeout=args.timeout).collect()
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_telemetry_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
