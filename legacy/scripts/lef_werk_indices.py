from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from agt.werk_indices import (  # noqa: E402
    calculate_werk_indices,
    format_werk_indices_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate 🌊 WERK indices.")
    parser.add_argument("--leap", default=1.0, help="Leap factor for framework state.")
    parser.add_argument("--conjecture", default="", help="Conjecture or event text to audit.")
    parser.add_argument("--live-telemetry", action="store_true", help="Collect live planetary telemetry.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()

    indices = calculate_werk_indices(
        leap_factor=args.leap,
        conjecture=args.conjecture,
        collect_live_telemetry=args.live_telemetry,
    )
    if args.json:
        print(json.dumps(indices, ensure_ascii=False, indent=2))
    else:
        print(format_werk_indices_markdown(indices))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
