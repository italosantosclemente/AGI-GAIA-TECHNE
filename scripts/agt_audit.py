#!/usr/bin/env python3
"""
AGT Audit CLI - AGI-GAIA-TECHNE.

Functional audit tool for philosophical/technical claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.ctk import ClementeThesisKernel
from agt.types import AuditResult, Severity, ThesisStatus


def audit_claim(kernel: ClementeThesisKernel, claim: str) -> AuditResult:
    return kernel.evaluate(claim)


def audit_file(kernel: ClementeThesisKernel, filepath: str) -> List[AuditResult]:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File {filepath} not found.")
        sys.exit(2)

    content = path.read_text(encoding="utf-8")

    results: List[AuditResult] = []
    for sentence in re.split(r"(?<=[.!?])\s+", content):
        sentence = sentence.strip()
        if not sentence:
            continue

        result = kernel.evaluate(sentence)
        has_signal = (
            ThesisStatus.UNCLASSIFIED_CLAIM not in result.statuses
            or len(result.statuses) > 1
        )
        if has_signal:
            results.append(result)

    return results


def should_fail(results: Iterable[AuditResult], fail_on: str) -> bool:
    if fail_on == "none":
        return False

    # AGT currently exposes low/medium/high. Keep "critical" as a compatible
    # alias for high-risk canonical violations until a Critical enum exists.
    if fail_on in {"high", "critical"}:
        return any(result.severity == Severity.HIGH for result in results)

    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AGI-GAIA-TECHNE claims.")
    parser.add_argument("--claim", type=str, help="Single claim to audit.")
    parser.add_argument("--file", type=str, help="File to audit (scans sentences).")
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "markdown"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--fail-on",
        type=str,
        choices=["high", "critical", "none"],
        default="high",
        help=(
            "Exit code 1 on high severity. "
            "'critical' is kept as a compatibility alias for high."
        ),
    )

    args = parser.parse_args()

    if not args.claim and not args.file:
        parser.print_help()
        return 0

    kernel = ClementeThesisKernel()

    if args.claim:
        results = [audit_claim(kernel, args.claim)]
        title = "AGT Audit Report"
    else:
        results = audit_file(kernel, args.file)
        title = f"Audit Report for {args.file}"

    if args.format == "json":
        payload = results[0].to_dict() if args.claim else [r.to_dict() for r in results]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_markdown_report(results, title=title)

    return 1 if should_fail(results, args.fail_on) else 0


def print_markdown_report(
    results: List[AuditResult],
    title: str = "AGT Audit Report",
) -> None:
    print(f"# {title}\n")
    if not results:
        print("No significant architectonic patterns detected.")
        return

    for i, result in enumerate(results, 1):
        status_label = "OK" if result.ok else "BLOCK"
        print(f"## {i}. Claim Evaluation [{status_label}]")
        print(f"**Claim:** {result.claim}")
        print(f"**Status:** {', '.join(s.value for s in result.statuses)}")
        print(f"**Severity:** {result.severity.value}")
        if result.triggered_rules:
            print(f"**Rules:** {', '.join(result.triggered_rules)}")
        if result.recommendations:
            print("**Recommendations:**")
            for recommendation in result.recommendations:
                print(f"- {recommendation}")
        print("\n---")


if __name__ == "__main__":
    raise SystemExit(main())
