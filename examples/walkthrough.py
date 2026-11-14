"""A claim from end to ledger.

Run from the repository root:

    python examples/walkthrough.py [--ledger record.jsonl]

The scenario itself is in src/gaia_techne/demo.py, where every step is
commented; `python -m gaia_techne demo` runs the same thing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gaia_techne.demo import run  # noqa: E402

ledger = sys.argv[sys.argv.index("--ledger") + 1] if "--ledger" in sys.argv else None
run(ledger=ledger)
