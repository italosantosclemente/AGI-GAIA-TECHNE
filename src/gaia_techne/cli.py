"""Command line: anyone with a record can check it without trusting whoever kept it.

    python -m gaia_techne demo [--ledger PATH]   run the walkthrough; optionally write the public record
    python -m gaia_techne verify PATH            check the hash chain, then replay the record against the invariants
    python -m gaia_techne report PATH            recompute the metatheoretical report from the record alone
    python -m gaia_techne spec                   print the chain question -> condition -> invariant -> code -> test
    python -m gaia_techne syntax                 print the syntax of a run
    python -m gaia_techne agent [GOAL] [options]  pursue a task under an end you state and acknowledge

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


def _agent(args) -> int:
    from .agent import Agent, Task
    from .agent.demo import run as scenario
    from .canon import Procedure, ProcedureKind
    from .gaia import Archive
    from .koinos import Direction, GroundKind, SymbolicFunction
    from .models import from_spec
    from .pipeline import Runtime

    if not args.goal:
        scenario(ledger=args.ledger)
        return 0
    if not args.end or not args.by:
        print("an agent acts only under an end that a person states and acknowledges: give --end and --by")
        return 2
    model = from_spec(args.model)
    rt = Runtime(generator=model, source_name=model.name)
    rt.ends.propose("e1", args.end, proposed_by=args.by, community=args.community)
    rt.ends.acknowledge("e1", args.by)
    rt.allow(GroundKind.COMPUTE, "calls", args.calls, set_by=args.by, end_id="e1", reason="set on the command line")
    agent = Agent(rt, archive=Archive(args.archive, allow_network=args.web))
    test = args.test or f"review of the answer by {args.by}"
    result = agent.pursue(Task(
        goal=args.goal, end_id="e1", requested_by=args.by,
        function=SymbolicFunction.PRESENTATION, direction=Direction.TOWARD_INTUITION,
        procedures=[Procedure(ProcedureKind.REVIEW, test)], returns_to_perception=test,
    ))
    print(result.summary())
    if args.ledger:
        print(f"public record written to {rt.world.dump(args.ledger)}")
    return 0 if result.answer is not None else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gaia_techne", description=f"AGI-GAIA-TECHNE {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="run the walkthrough scenario")
    demo.add_argument("--ledger", help="write the public record to this JSON Lines file")
    sub.add_parser("verify", help="verify a record and replay it against the invariants").add_argument("path")
    sub.add_parser("report", help="recompute the metatheoretical report from a record").add_argument("path")
    sub.add_parser("spec", help="print the chain from questions to tests")
    sub.add_parser("syntax", help="print the syntax of a run")
    ag = sub.add_parser("agent", help="pursue a task under an end you state and acknowledge (without GOAL: the offline scenario)")
    ag.add_argument("goal", nargs="?")
    ag.add_argument("--end", help="the end, stated so that anyone could be asked to share it")
    ag.add_argument("--by", help="your name: you propose and acknowledge the end and bring the task")
    ag.add_argument("--community", default="those the end concerns")
    ag.add_argument("--model", default="ollama:llama3.1", help="ollama:MODEL, openai:URL|MODEL or anthropic:MODEL")
    ag.add_argument("--archive", help="a folder of documents you put at the system's disposal")
    ag.add_argument("--web", action="store_true", help="also allow reading public web addresses")
    ag.add_argument("--calls", type=float, default=10, help="allowance of model calls under the end")
    ag.add_argument("--test", help="the perception in which anyone can test the answer")
    ag.add_argument("--ledger", help="write the public record to this JSON Lines file")
    args = parser.parse_args(argv)

    if args.command == "demo":
        from .demo import run

        run(ledger=args.ledger)
        return 0
    if args.command == "agent":
        return _agent(args)
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
