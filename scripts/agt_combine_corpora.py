#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Combine AGT corpus JSONL files with chunk-level deduplication."
    )
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    written = 0
    read = 0

    with output.open("w", encoding="utf-8") as out:
        for input_path in args.input:
            with Path(input_path).open("r", encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    read += 1
                    payload = json.loads(line)
                    text = str(payload.get("text", ""))
                    digest = payload.get("content_sha256") or hashlib.sha256(text.encode("utf-8")).hexdigest()
                    if digest in seen:
                        continue
                    seen.add(digest)
                    out.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
                    written += 1

    report = {
        "output": str(output),
        "input_files": args.input,
        "read_records": read,
        "written_records": written,
        "duplicates": read - written,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("# Combined Corpus\n")
        for key, value in report.items():
            print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
