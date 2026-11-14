"""A claim from end to ledger: the walkthrough scenario.

People of a river basin state an end, set how much energy the runs under it
may draw, and bring a task. A model produces a claim; the canon admits it as a
judgment of perception; others correct it; the system proposes a derived end
that waits for people; and the record is verified and read.

Run it with `python -m gaia_techne demo` or `python examples/walkthrough.py`.
"""

from __future__ import annotations

from typing import Callable, Optional

from .canon import CorrectionEvent, Procedure, ProcedureKind, Reach
from .ethos import Premise
from .koinos import Direction, GroundDependency, GroundKind, SymbolicFunction
from .pipeline import Runtime, Werk


def generator(task, premises):
    # Any model can stand here: a local LLM, a statistical model, a human typist.
    return "Nitrate at station 4 exceeded 50 mg/L in 3 of the last 12 samples."


def run(ledger: Optional[str] = None, out: Callable[..., None] = print) -> Runtime:
    rt = Runtime(generator=generator, source_name="model-v0")

    # I. What should I do? People state and acknowledge the end; the runtime cannot.
    rt.ends.propose(
        "basin-water",
        "Make the water quality of the basin checkable by anyone who lives on it",
        proposed_by="river committee",
        community="basin residents",
    )
    rt.ends.acknowledge("basin-water", "Ana")
    rt.ends.acknowledge("basin-water", "Bruno", accepts=False, reason="fishing data matters more")

    # II. The ground is finite: people set how much energy the runs under this end may draw.
    rt.allow(GroundKind.ENERGY, "kWh", 1.0, set_by="river committee", end_id="basin-water",
             reason="what the school's solar panel spares in a day")

    # Ground -> Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure
    claim = rt.process(
        Werk(
            task="Summarize nitrate measurements at station 4",
            end_id="basin-water",
            requested_by="Ana",
            function=SymbolicFunction.SIGNIFICATION,
            direction=Direction.AWAY_FROM_LIFE,
            premises=[Premise("2026 sensor series, station 4", "state water agency open data")],
            procedures=[Procedure(ProcedureKind.REPETITION, "take a new water sample at station 4")],
            returns_to_perception="a water sample anyone can take at station 4",
            ground=[
                GroundDependency(GroundKind.COMPUTE, "one laptop CPU", "Luz, MG", "its owner"),
                GroundDependency(GroundKind.ENERGY, "grid power", "Luz, MG", "local utility workers", 0.02, "kWh"),
                GroundDependency(GroundKind.ARCHIVE, "agency sensor archive", "state servers", "agency technicians"),
            ],
        )
    )
    out("claim:", claim.content)
    out("stage:", claim.stage.value, "| reach:", claim.reach.name, "| flags:", claim.flags)

    # III. Correction: someone else repeats the procedure.
    rt.correct(claim, CorrectionEvent("school lab", ProcedureKind.REPETITION, True, Reach.FORM_OF_LIFE))
    rt.correct(claim, CorrectionEvent("university lab", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    out("after correction:", claim.stage.value, "| reach:", claim.reach.name)

    # The system may propose a derived end; it stays unusable until a person acknowledges it.
    rt.propose_derived_end("basin-water", "basin-water.schools", "Sample first the stations near schools")
    out("derived end acknowledged?", rt.ends.get("basin-water.schools").is_acknowledged)

    # Ledger
    out("record intact:", rt.world.verify(), f"({len(rt.world)} entries)")
    out("ground borrowed:", rt.footprint.totals(), "| allowance left:", rt.budget.remaining(rt.footprint))
    out(rt.ledger())
    if ledger:
        path = rt.world.dump(ledger)
        out(f"public record written to {path}; check it with: python -m gaia_techne verify {path}")
    return rt
