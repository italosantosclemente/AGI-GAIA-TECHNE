#!/usr/bin/env python3
"""
AGT Audit CLI — AGI-GAIA-TECHNE
Functional audit tool for philosophical/technical claims.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List

# Ensure src is in path
sys.path.append(str(Path(__file__).parent.parent))

from src.agt.ctk import ClementeThesisKernel
from src.agt.types import AuditResult, ThesisStatus

def audit_claim(kernel: ClementeThesisKernel, claim: str) -> AuditResult:
    return kernel.evaluate(claim)

def audit_file(kernel: ClementeThesisKernel, filepath: str) -> List[AuditResult]:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File {filepath} not found.")
        sys.exit(2)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

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

def main():
    parser = argparse.ArgumentParser(description="Audit AGI-GAIA-TECHNE claims.")
    parser.add_argument("--claim", type=str, help="Single claim to audit.")
    parser.add_argument("--file", type=str, help="File to audit (scans sentences).")
    parser.add_argument("--format", type=str, choices=["json", "markdown"], default="markdown", help="Output format.")
    parser.add_argument("--fail-on", type=str, choices=["high", "critical"], default="high", help="Exit code 1 on severity.")

    args = parser.parse_args()

    if not args.claim and not args.file:
        parser.print_help()
        sys.exit(0)

    kernel = ClementeThesisKernel()

    if args.claim:
        result = audit_claim(kernel, args.claim)
        if args.format == "json":
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_markdown_report([result])

        if args.fail_on == "high" and result.severity == "high":
            sys.exit(1)

    elif args.file:
        results = audit_file(kernel, args.file)
        if args.format == "json":
            print(json.dumps([r.to_dict() for r in results], indent=2))
        else:
            print_markdown_report(results, title=f"Audit Report for {args.file}")

        if args.fail_on == "high" and any(r.severity == "high" for r in results):
            sys.exit(1)

def print_markdown_report(results: List[AuditResult], title: str = "AGT Audit Report"):
    print(f"# {title}\n")
    if not results:
        print("No significant architectonic patterns detected.")
        return

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

if __name__ == "__main__":
    main()
