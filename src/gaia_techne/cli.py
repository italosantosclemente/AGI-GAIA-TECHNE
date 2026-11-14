"""Command line: anyone with a record can check it without trusting whoever kept it.

    python -m gaia_techne demo [--ledger PATH]   run the walkthrough; optionally write the public record
    python -m gaia_techne verify PATH            check the hash chain, then replay the record against the invariants
    python -m gaia_techne report PATH            recompute the metatheoretical report from the record alone
    python -m gaia_techne spec                   print the chain question -> condition -> invariant -> code -> test
    python -m gaia_techne syntax                 print the syntax of a run

Exit status: 0 when the record verifies and no invariant is broken, 1 when the
record was changed after it was written, 2 when it verifies but an act in it
breaks an invariant.
"""

from __future__ import annotations

import argparse
from typing import List, Optional

from . import spec
from ._version import __version__
from .koinos.common_world import CommonWorld, TamperedRecord
from .metatheory.indices import report
from .metatheory.replay import InvariantViolation, replay
from .syntax import SYNTAX


def _load(path: str):
    try:
        world = CommonWorld.load(path)
    except TamperedRecord as exc:
        print(f"TAMPERED: {exc}")
        return None, 1
    try:
        projection = replay(world)
    except InvariantViolation as exc:
        print(f"INVALID: the record verifies, but {exc}")
        return None, 2
    return (world, projection), 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gaia_techne", description=f"AGI-GAIA-TECHNE {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="run the walkthrough scenario")
    demo.add_argument("--ledger", help="write the public record to this JSON Lines file")
    sub.add_parser("verify", help="verify a record and replay it against the invariants").add_argument("path")
    sub.add_parser("report", help="recompute the metatheoretical report from a record").add_argument("path")
    sub.add_parser("spec", help="print the chain from questions to tests")
    sub.add_parser("syntax", help="print the syntax of a run")
    args = parser.parse_args(argv)

    if args.command == "demo":
        from .demo import run

        run(ledger=args.ledger)
        return 0
    if args.command == "syntax":
        for step in SYNTAX:
            print(f"{step.name.title():<11} {step.value}")
        return 0
    if args.command == "spec":
        problems = spec.check()
        print(spec.tree())
        for p in problems:
            print(f"PROBLEM: {p}")
        return 1 if problems else 0
    loaded, status = _load(args.path)
    if loaded is None:
        return status
    world, projection = loaded
    if args.command == "verify":
        print(
            f"record verifies: {len(world)} entries, head {world.head[:16]}...; replay re-checked "
            f"{len(projection.ends.all())} ends, {len(projection.claims)} claims and their corrections: no invariant broken"
        )
        return 0
    r = report(projection.claims)
    print(r)
    print(f"widening: {r.widening}")
    print(f"ground borrowed: {projection.footprint.totals()}")
    if projection.budget.allowances():
        print(f"allowance left: {projection.budget.remaining(projection.footprint)}")
    return 0
