"""The syntax of a run, as an enforced order.

    Ground -> Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger

Cassirer's critical idealism hopes "to come to a sort of grammar and syntax of
the human mind" (Cassirer, 1979a, p. 90). The word is borrowed here in a
narrower sense: the order in which one run of the system passes from its
ground to its record.

The first eight steps are one call of `Runtime.process` and must occur in
this order, each once. The last two belong to the life of the claim after it
has been exposed: corrections come later, from others, any number of times,
and the ledger can be read at any moment. A correction of a claim that was
never exposed is a syntax violation, because no one could have measured what
was never offered to them.

The order of a run is not the order of the layers. The ground comes first in
every run, because every run is conditioned by it; but what a run may draw
from the ground is decided by people under acknowledged ends, so the layer of
ends is specified before the layer of the ground (Condition 0).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


class Step(Enum):
    GROUND = "the declared geomorphic conditions of the run and who maintains them"
    WERK = "a task under an acknowledged end"
    TRACE = "the premises, each with provenance"
    CLAIM = "the output as a judgment of perception"
    ASCENT = "the direction of the claim, tagged by the prism"
    HORIZON = "the guards of the three ideas"
    DESCENT = "the perception in which the claim can be tested"
    EXPOSURE = "entry in the common world"
    CORRECTION = "measurement by others through public procedures"
    LEDGER = "the record and its metatheoretical report"


SYNTAX: Tuple[Step, ...] = tuple(Step)
RUN_STEPS: Tuple[Step, ...] = SYNTAX[: SYNTAX.index(Step.EXPOSURE) + 1]
LIFE_STEPS: Tuple[Step, ...] = SYNTAX[len(RUN_STEPS):]


def render(steps=SYNTAX) -> str:
    return " -> ".join(s.name.title() for s in steps)


class SyntaxViolation(RuntimeError):
    """Raised when a run skips, repeats or reorders a step of the syntax."""


@dataclass
class RunTrace:
    """The steps one run has passed through, in order."""

    steps: List[Step] = field(default_factory=list)

    def enter(self, step: Step) -> None:
        done = len(self.steps)
        expected = RUN_STEPS[done] if done < len(RUN_STEPS) else None
        if step is not expected:
            after = self.steps[-1].name if self.steps else "the start of the run"
            raise SyntaxViolation(
                f"{step.name} cannot follow {after}; a run passes through {render(RUN_STEPS)}, each step once"
            )
        self.steps.append(step)

    @property
    def complete(self) -> bool:
        return tuple(self.steps) == RUN_STEPS

    def names(self) -> List[str]:
        return [s.name for s in self.steps]
