from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.agt.ctk import ClementeThesisKernel
from src.agt.types import AuditResult, ThesisStatus, Severity

def audit_claim(kernel: ClementeThesisKernel, claim: str) -> AuditResult:
    return kernel.evaluate(claim)

def audit_file(kernel: ClementeThesisKernel, filepath: str) -> List[AuditResult]:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File {filepath} not found.")
        sys.exit(2)

    content = path.read_text(encoding="utf-8")
    # Simple sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', content)
    results = []
    for sentence in sentences:
        if sentence.strip():
            res = kernel.evaluate(sentence.strip())
            # Only add if it's not unclassified or it's a success state
            if ThesisStatus.UNCLASSIFIED_CLAIM not in res.statuses or len(res.statuses) > 1:
                results.append(res)
    return results

def print_markdown_report(results: List[AuditResult], title: str = "AGT Audit Report"):
    print(f"# {title}\n")
    for i, res in enumerate(results, 1):
        status_color = "🟢" if res.ok else "🔴"
        print(f"## {i}. Claim Evaluation {status_color}")
        print(f"**Claim:** {res.claim}")
        print(f"**Status:** {', '.join([s.value for s in res.statuses])}")
        print(f"**Severity:** {res.severity.value}")
        if res.triggered_rules:
            print(f"**Rules:** {', '.join(res.triggered_rules)}")
        if res.recommendations:
            print("**Recommendations:**")
            for rec in res.recommendations:
                print(f"- {rec}")
        print("\n---")

def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AGI-GAIA-TECHNE claims.")
    parser.add_argument("--claim", action="append", help="Claim to evaluate.")
    parser.add_argument("--file", help="File to evaluate.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--fail-on", choices=["high", "none"], default="high")

    args = parser.parse_args()
    kernel = ClementeThesisKernel()
    results = []

    if args.claim:
        for c in args.claim:
            results.append(audit_claim(kernel, c))

    elif args.file:
        results = audit_file(kernel, args.file)

    if not results:
        print("No claims provided.")
        return 0

    if args.format == "json":
        if len(results) == 1:
             print(json.dumps(results[0].to_dict(), indent=2, ensure_ascii=False))
        else:
             print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))

    else:
        print_markdown_report(results)

    if args.fail_on == "high" and any(r.severity == Severity.HIGH for r in results):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
