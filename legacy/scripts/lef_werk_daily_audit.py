from __future__ import annotations

import argparse
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

from agt.lef_werk_auditor import (  # noqa: E402
    audit_trace,
    daily_ledger_entry,
    explain_alphabet,
    format_audit_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run 🌊 LEF/WERK daily audit.")
    parser.add_argument("--text", help="Text to audit.")
    parser.add_argument("--file", help="UTF-8 text file to audit.")
    parser.add_argument("--source", default="manual", help="Source label for the trace.")
    parser.add_argument("--ledger-dir", default="telemetrias/lef-werk", help="Ledger output directory.")
    parser.add_argument("--write-ledger", action="store_true", help="Write a dated ledger entry.")
    parser.add_argument("--explain-alphabet", action="store_true", help="Explain LEF/WERK and 🌊.")
    args = parser.parse_args()

    if args.explain_alphabet:
        print(explain_alphabet(include_gl25=True))
        return 0

    if not args.text and not args.file:
        parser.error("Provide --text, --file or --explain-alphabet.")

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = args.text or ""

    audit = audit_trace(text, source=args.source)
    markdown = format_audit_markdown(audit)
    print(markdown)

    if args.write_ledger:
        ledger_dir = ROOT / args.ledger_dir
        ledger_dir.mkdir(parents=True, exist_ok=True)
        today = __import__("datetime").date.today().isoformat()
        ledger_path = ledger_dir / f"{today}-wave-audit.md"
        entry = daily_ledger_entry(audit, date=today)
        if ledger_path.exists():
            ledger_path.write_text(
                ledger_path.read_text(encoding="utf-8").rstrip()
                + "\n\n---\n\n"
                + entry
                + "\n",
                encoding="utf-8",
            )
        else:
            ledger_path.write_text(entry + "\n", encoding="utf-8")
        print(f"\nLedger written: {ledger_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
