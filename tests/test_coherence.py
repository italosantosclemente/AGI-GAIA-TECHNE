"""The README against the code.

Condition 0 asks that no technical layer be specified before the practical
question it serves is stated. These tests hold the documentation to the same
chain: the invariants table of README §8 lists exactly the tests that
`spec.py` names, every named test exists, the syntax, the guards and the
modules named in the README are the ones in the code.
"""

import ast
import re
from pathlib import Path

from gaia_techne import spec
from gaia_techne.canon.guards import GUARDS
from gaia_techne.syntax import SYNTAX, render

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
SRC = ROOT / "src" / "gaia_techne"


def section(number: int) -> str:
    start = re.search(rf"^## {number}\. .*$", README, flags=re.M)
    assert start, f"README has no section {number}"
    end = re.search(r"^## \d+\. ", README[start.end():], flags=re.M)
    return README[start.end(): start.end() + end.start()] if end else README[start.end():]


def _defined_tests():
    names = set()
    for path in (ROOT / "tests").glob("test_*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                names.add(node.name)
    return names


def test_spec_resolves():
    assert spec.check() == []


def test_readme_invariants_match_spec():
    table = [line for line in section(8).splitlines() if line.startswith("| ") and "`test_" in line]
    in_readme = {t for line in table for t in re.findall(r"`(test_\w+)`", line.split("|")[-2])}
    assert in_readme == set(spec.tests_named())
    assert set(spec.tests_named()) <= _defined_tests()
    assert len(table) == len(spec.INVARIANTS)


def test_readme_syntax_matches_code():
    assert render(SYNTAX) in section(5)
    assert render(SYNTAX) == "Ground -> Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger"


def test_readme_guards_match_code():
    mindmap = section(11)
    block = mindmap[mindmap.index("    Guards"):]
    block = block[: block.index("\n    Metatheory")]
    named = set(re.findall(r"^\s{6}(\w+):", block, flags=re.M))
    assert named == {g.name for g in GUARDS}


def test_readme_modules_exist():
    named = set(re.findall(r"`([\w/]+\.py)`", section(3)))
    assert named, "the isomorphism table names no module"
    for rel in named:
        assert (SRC / rel).exists(), rel
    tree = section(12)
    listed = set(re.findall(r"([\w]+\.py)", tree))
    on_disk = {p.name for p in SRC.rglob("*.py")} | {p.name for p in (ROOT / "tests").glob("*.py")}
    assert listed <= on_disk | {"walkthrough.py"}
    for path in SRC.rglob("*.py"):
        if path.name != "__init__.py":
            assert path.name in tree, f"{path.relative_to(SRC)} is missing from README §12"
