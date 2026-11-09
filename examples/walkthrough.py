"""A claim from end to ledger.

Run from the repository root:

    python examples/walkthrough.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gaia_techne import Runtime, Werk  # noqa: E402
from gaia_techne.canon import CorrectionEvent, Procedure, ProcedureKind, Reach  # noqa: E402
from gaia_techne.ethos import Premise  # noqa: E402
from gaia_techne.koinos import Direction, SymbolicFunction  # noqa: E402


def generator(task, premises):
    # Any model can stand here: a local LLM, a statistical model, a human typist.
    return "Nitrate at station 4 exceeded 50 mg/L in 3 of the last 12 samples."


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

# Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure
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
    )
)
print("claim:", claim.content)
print("stage:", claim.stage.value, "| reach:", claim.reach.name, "| flags:", claim.flags)

# Correction: someone else repeats the procedure.
rt.correct(claim, CorrectionEvent("school lab", ProcedureKind.REPETITION, True, Reach.FORM_OF_LIFE))
rt.correct(claim, CorrectionEvent("university lab", ProcedureKind.REPETITION, True, Reach.EVERYONE))
print("after correction:", claim.stage.value, "| reach:", claim.reach.name)

# Ledger
print("record intact:", rt.world.verify())
print(rt.ledger())
