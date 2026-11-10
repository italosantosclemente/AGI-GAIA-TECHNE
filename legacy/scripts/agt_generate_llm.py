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

from agt.llm_train import generate_text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate text from an AGI-GAIA-TECHNE ManualGPT checkpoint."
    )
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.85)
    parser.add_argument("--top-k", type=int, default=80)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    output = generate_text(
        checkpoint_path=args.checkpoint,
        prompt=args.prompt,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
        device=args.device,
    )
    if args.json:
        print(json.dumps({"prompt": args.prompt, "completion": output}, ensure_ascii=False, indent=2))
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
