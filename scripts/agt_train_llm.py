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

from agt.llm_train import TrainingConfig, train_from_pack


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Train AGI-GAIA-TECHNE ManualGPT from random initialization."
    )
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--output", default="models/agt-gaia-manual-gpt")
    parser.add_argument(
        "--scale",
        choices=["micro", "debug", "seed", "small", "base", "large-plan"],
        default="debug",
    )
    parser.add_argument("--max-steps", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--grad-accum", type=int, default=1)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=0.1)
    parser.add_argument("--warmup-steps", type=int, default=10)
    parser.add_argument("--eval-interval", type=int, default=25)
    parser.add_argument("--eval-batches", type=int, default=10)
    parser.add_argument("--checkpoint-interval", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--no-amp", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    config = TrainingConfig(
        pack_dir=args.pack_dir,
        output_dir=args.output,
        scale=args.scale,
        max_steps=args.max_steps,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        warmup_steps=args.warmup_steps,
        eval_interval=args.eval_interval,
        eval_batches=args.eval_batches,
        checkpoint_interval=args.checkpoint_interval,
        seed=args.seed,
        device=args.device,
        amp=not args.no_amp,
    )
    report = train_from_pack(config)
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("# AGI-GAIA-TECHNE ManualGPT Training\n")
        for key, value in report.to_dict().items():
            print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
