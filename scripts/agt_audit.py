from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.ctk import ClementeThesisKernel
from agt.types import Severity


def audit_claim(claim: str) -> Dict[str, Any]:
    ctk = ClementeThesisKernel()
    result = ctk.evaluate(claim)
    return {
        "claim": claim,
        "statuses": result.statuses,
        "severity": result.severity.value,
        "recommendations": result.recommendations,
        "ok": result.ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AGI-GAIA-TECHNE claims.")
    parser.add_argument("--claim", action="append", help="Claim to evaluate.")
    parser.add_argument("--file", help="File to evaluate.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")

    args = parser.parse_args()

    results = []

    if args.claim:
        for c in args.claim:
            results.append(audit_claim(c))

    if args.file:
        path = Path(args.file)
        if path.exists():
            content = path.read_text(encoding="utf-8")
            results.append(audit_claim(content))

    if not results:
        print("No claims provided.")
        return 0

    if args.format == "json":
        if len(results) == 1:
             print(json.dumps(results[0], indent=2, ensure_ascii=False))
        else:
             print(json.dumps(results, indent=2, ensure_ascii=False))

    else:
        print("# AGT Audit Report\n")
        for r in results:
            print(f"## Claim: {r['claim'][:100]}...")
            print(f"**Severity:** {r['severity']}")
            print(f"**Statuses:** {', '.join(r['statuses'])}")
            if r["recommendations"]:
                print("\n**Recommendations:**")
                for rec in r["recommendations"]:
                    print(f"- {rec}")
            print("\n---\n")

    if any(r["severity"] == "high" for r in results):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
