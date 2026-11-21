"""The kernel scenario: signed acts, a capability, a fallen premise, a witnessed log.

Runs offline with a scripted model. Ana and Bia have keys; Caio has none.
Ana grants the agent a capability under the end she brought; the agent's
answer rests on an earlier claim; Bia, who signs, refutes that claim; Caio,
who does not sign, upholds the answer. The status read from the record shows
that the answer is not usable (its premise fell) and that Caio's act does not
count, and a witness cosigns checkpoints before and after.
"""

from __future__ import annotations

import json
from typing import Callable, Optional

from ..agent.loop import Agent, Task
from ..canon import CorrectionEvent, Procedure, ProcedureKind, Reach
from ..ethos.premises import Premise
from ..koinos import Direction, GroundDependency, GroundKind, SymbolicFunction
from ..models import ScriptedAdapter
from ..pipeline import Runtime, Werk
from .core import Kernel
from .log import Witness

ANSWERS = [
    "Station 4 was sampled 30 times last year.",
    json.dumps([{"step": "tool", "tool": "arithmetic", "input": "30 / 12"}]),
    "Station 4 was sampled about 2.5 times a month, which meets the twice-a-month target.",
]


def run(ledger: Optional[str] = None, out: Callable[..., None] = print) -> Kernel:
    rt = Runtime(generator=ScriptedAdapter(answers=list(ANSWERS)), source_name="scripted-model")
    k = Kernel(rt)
    for person in ("ana", "bia"):
        k.enroll(person)
    rt.ends.propose("e1", "Let anyone in the basin check its water", "ana", "basin")
    rt.ends.acknowledge("e1", "ana")
    test = [Procedure(ProcedureKind.REPETITION, "count the samples in the station log")]
    ground = [GroundDependency(GroundKind.COMPUTE, "one model call", "this machine", "ana", 1.0, "calls")]
    first = rt.process(Werk("How often was station 4 sampled?", "e1", "ana", SymbolicFunction.SIGNIFICATION,
                            Direction.AWAY_FROM_LIFE, procedures=test, returns_to_perception="the station log",
                            ground=ground))
    w = Witness("witness-basin")
    out("checkpoint before the task, cosigned:\n" + k.witness(w).text())

    cap = k.grant("ana", "e1", tools=["arithmetic"], max_steps=2)
    task = Task("Does station 4 meet the twice-a-month target?", "e1", "ana",
                function=SymbolicFunction.SIGNIFICATION, direction=Direction.AWAY_FROM_LIFE,
                procedures=test, returns_to_perception="the station log",
                premises=[Premise(first.content, f"claim {first.claim_id}", ref=first.claim_id)], use_memory=False)
    result = k.pursue(Agent(rt), task, cap)
    out(result.summary())

    rt.correct(first, CorrectionEvent("bia", ProcedureKind.REPETITION, False, Reach.FORM_OF_LIFE,
                                      "the log shows 18 samples, not 30"))
    rt.correct(result.answer, CorrectionEvent("caio", ProcedureKind.REPETITION, True, Reach.FORM_OF_LIFE,
                                              "looks right to me"))
    out("\nstatus, read from the record:")
    out(k.status().summary())
    out("\ncheckpoint after, cosigned (the witness checked it extends the first):\n" + k.witness(w).text())
    if ledger:
        out(f"public record written to {rt.world.dump(ledger)}")
    return k
