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

from agt.llm_corpus import pack_corpus
from agt.llm_tokenizer import ByteTokenizer


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pack AGT corpus JSONL into token tensors for from-scratch LLM training."
    )
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--output", default="data/llm/packed")
    parser.add_argument("--validation-fraction", type=float, default=0.02)
    parser.add_argument("--block-size", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = pack_corpus(
        corpus_path=args.corpus,
        output_path=args.output,
        tokenizer=ByteTokenizer(),
        validation_fraction=args.validation_fraction,
        block_size=args.block_size,
        seed=args.seed,
    )
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("# AGT Packed Corpus\n")
        for key, value in report.to_dict().items():
            print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
