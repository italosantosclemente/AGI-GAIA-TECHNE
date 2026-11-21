"""The agent scenario: one task, from end to answer, without a network.

A school in the basin asks how many water samples a year its pupils would take
if each of the 4 classes sampled the river twice a month, and whether that
covers the stations the archive lists. The model is scripted, so that the
scenario runs anywhere; `python -m gaia_techne agent --model ollama:MODEL` runs
the same loop with a real model.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Callable, Optional

from ..canon import CorrectionEvent, Procedure, ProcedureKind, Reach
from ..gaia.archive import Archive
from ..koinos import Direction, GroundKind, SymbolicFunction
from ..models import ScriptedAdapter
from ..pipeline import Runtime
from .loop import Agent, Task

PLAN = json.dumps([
    {"step": "tool", "tool": "arithmetic", "input": "4 * 2 * 12"},
    {"step": "tool", "tool": "archive_search", "input": "stations sampling"},
    {"step": "claim", "task": "Say which stations the archive lists and whether 96 samples a year cover them"},
    {"step": "end", "statement": "Share the pupils' samples with the state water agency"},
])
ANSWERS = [
    PLAN,
    "The archive lists stations 2, 4 and 7. 96 samples a year are 32 per station, about one every eleven days.",
    "The 4 classes would take 4 * 2 * 12 = 96 samples a year, 32 for each of the stations 2, 4 and 7 that the "
    "archive lists. Anyone can test this by counting the samples logged at the school at the end of the year.",
]


def run(ledger: Optional[str] = None, out: Callable[..., None] = print):
    folder = Path(tempfile.mkdtemp(prefix="gaia-archive-"))
    (folder / "stations.md").write_text(
        "Basin monitoring plan. Sampling stations: 2 (upper river), 4 (near the school), 7 (estuary).\n",
        encoding="utf-8",
    )
    model = ScriptedAdapter(answers=list(ANSWERS), maintained_by="the school's teacher who wrote the script")
    rt = Runtime(generator=model, source_name="scripted-model")
    rt.ends.propose("school-water", "Let the pupils take part in checking the river water of the basin",
                    proposed_by="school council", community="school and basin residents")
    rt.ends.acknowledge("school-water", "Carla")
    rt.allow(GroundKind.COMPUTE, "calls", 5, set_by="Carla", end_id="school-water", reason="one afternoon of the lab laptop")

    agent = Agent(rt, archive=Archive(str(folder), maintained_by="the school's teacher"))
    result = agent.pursue(Task(
        goal="How many samples a year would the 4 classes take at twice a month each, and do they cover the stations?",
        end_id="school-water",
        requested_by="Carla",
        function=SymbolicFunction.SIGNIFICATION,
        direction=Direction.AWAY_FROM_LIFE,
        procedures=[Procedure(ProcedureKind.REPETITION, "count the samples logged at the school")],
        returns_to_perception="the sample log kept at the school",
        tools=["arithmetic", "archive_search", "memory"],
    ))
    out(result.summary())

    # Others measure the answer; the agent cannot.
    rt.correct(result.answer, CorrectionEvent("Daniel", ProcedureKind.REPETITION, True, Reach.FORM_OF_LIFE,
                                              note="counted the log at the end of the year"))
    out(f"after correction by Daniel: {result.answer.stage.value}, reach {result.answer.reach.name}, "
        f"usable: {rt.canon.usable(result.answer)}")
    out(f"record intact: {rt.world.verify()} ({len(rt.world)} entries); allowance left: {rt.budget.remaining(rt.footprint)}")
    if ledger:
        path = rt.world.dump(ledger)
        out(f"public record written to {path}; check it with: python -m gaia_techne verify {path}")
    return result
