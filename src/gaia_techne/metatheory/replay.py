"""Replay: the record as the measure, the runtime as one of its readings.

The metatheoretical report "shows on the system's own record whether the
community that can correct it is being widened or narrowed" (README, §2.6).
For that to hold, the record has to be enough: anyone with the file must be
able to rebuild the ends, claims, corrections, verifications and allowances
from it, recompute the report, and check that no act in it broke an invariant,
without trusting the runtime that wrote it.

Two checks, in this order:

1. integrity: the hash chain of the common world verifies (`TamperedRecord`);
2. validity: the acts are re-performed in order through the same layers, so
   that every invariant the runtime enforced is enforced again on the record
   (`InvariantViolation`). A record whose hashes were recomputed after a
   correction by the source was added still fails here.

Entries of other kinds are kept as notes and re-check nothing.

Two options serve the kernel. `until` replays the record only up to an entry,
so that anyone can ask what the record said at that point ("as of"). `admit`
decides which acts of recognition count: given, it is called for every
correction, verification and acknowledgment, and an entry it does not admit
(an unsigned act where signatures are required) counts for nothing and is kept
in `Projection.not_counted` with the reason.
After the acts are replayed, `propagate` marks the claims whose premises fell.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Set, Tuple

from ..boundaries import GroundIsNotSubject, is_machine
from ..canon.claims import Claim, CorrectionEvent, Procedure, ProcedureKind, Reach
from ..canon.judgment import Canon, OrganonRefused, propagate
from ..ethos.ends import EndProposedByMachine, EndsRegistry
from ..ethos.imperatives import NoAcknowledgedEnd
from ..koinos.common_world import CommonWorld, Entry, TamperedRecord
from ..koinos.ground import Allowance, GroundBudget, GroundDependency, GroundFootprint, GroundKind, LimitReached
from ..koinos.prism import Direction, SymbolicFunction
from ..syntax import RUN_STEPS
from .indices import Report, report

RUN_STEP_NAMES = [s.name for s in RUN_STEPS]


class InvariantViolation(ValueError):
    """The record verifies, but an act in it breaks an invariant."""


@dataclass
class Projection:
    """What the record says, rebuilt act by act."""

    ends: EndsRegistry
    claims: List[Claim]
    footprint: GroundFootprint
    budget: GroundBudget
    machine_authors: Set[str]
    notes: List[Entry]
    not_counted: List[Tuple[int, str]] = field(default_factory=list)  # (entry index, reason)
    size: int = 0  # entries replayed


def _same(e: Entry, named: str) -> None:
    if named != e.author:
        raise InvariantViolation(f"entry {e.index}: signed by {e.author!r} but names {named!r} as the one who acted")


RECOGNITION = ("correction", "verification", "end_acknowledged")


def replay(world: CommonWorld, until: Optional[int] = None,
           admit: Optional[Callable[[Entry], Optional[str]]] = None) -> Projection:
    """Rebuild the record; `until` stops after that entry; `admit` returns None to count an act, or why it does not."""
    bad = world.first_invalid()
    if bad is not None:
        raise TamperedRecord(f"entry {bad} does not verify")
    machine: Set[str] = set()
    ends = EndsRegistry()  # no record: replaying writes nothing
    canon = Canon()
    ends.machine_authors = canon.machine_authors = machine  # one set, filled by the runtime entries as they come
    budget = GroundBudget()
    footprint = GroundFootprint()
    claims: List[Claim] = []
    exposed: Dict[int, Claim] = {}
    notes: List[Entry] = []
    not_counted: List[Tuple[int, str]] = []
    entries = world.entries()
    if until is not None:
        if not 0 <= until < len(entries):
            raise ValueError(f"entry {until} is not in a record of {len(entries)} entries")
        entries = entries[: until + 1]

    for e in entries:
        p = e.payload
        if admit is not None and e.kind in RECOGNITION:
            why = admit(e)
            if why is not None:
                not_counted.append((e.index, why))
                continue
        try:
            if e.kind == "runtime":
                machine.update(p.get("names", [p["source"]]))
            elif e.kind == "end_proposed":
                _same(e, p["proposed_by"])
                ends.propose(p["end_id"], p["statement"], e.author, p["community"]).recorded_at = e.index
            elif e.kind == "end_acknowledged":
                _same(e, p["person"])
                ends.acknowledge(p["end_id"], e.author, p["accepts"], p.get("reason", ""))
            elif e.kind == "end_derived":
                _same(e, p["derived_by"])
                ends.derive(p["parent"], p["end_id"], p["statement"], e.author).recorded_at = e.index
            elif e.kind == "end_revised":
                _same(e, p["by"])
                ends.revise(p["end_id"], p["to"], e.author, p.get("reason", ""))
            elif e.kind == "allowance_set":
                _same(e, p["set_by"])
                if is_machine(e.author, machine):
                    raise EndProposedByMachine("an allowance set by the system itself")
                end = ends.find(p["end_id"])
                if end is None or not end.is_acknowledged:
                    raise NoAcknowledgedEnd(f"allowance under {p['end_id']!r}, which no one had acknowledged")
                budget.set(Allowance(GroundKind[p["kind"]], p["unit"], p["limit"], e.author, p["end_id"], p.get("reason", "")))
            elif e.kind == "claim":
                claim = _claim(e, p, ends, budget, footprint, canon, claims)
                if claim.revises is not None:
                    old = next((c for c in claims if c.claim_id == claim.revises), None)
                    if old is None:
                        raise InvariantViolation(f"entry {e.index}: revises {claim.revises!r}, which was never exposed")
                    if old.revised_by:
                        raise InvariantViolation(f"entry {e.index}: {claim.revises!r} was already revised by {old.revised_by!r}")
                    old.revised_by = claim.claim_id
                claims.append(claim)
                exposed[e.index] = claim
            elif e.kind == "correction":
                _same(e, p["by"])
                claim = exposed.get(e.refers_to)
                if claim is None:
                    raise InvariantViolation(f"entry {e.index}: a correction that refers to no exposed claim")
                event = CorrectionEvent(
                    e.author, ProcedureKind[p["procedure"]], p["upheld"], Reach[p["community_reach"]], p.get("note", ""),
                    at=e.at, public=p.get("public", True),
                )
                canon.correct(claim, event)
            elif e.kind == "verification":
                _same(e, p["person"])
                claim = exposed.get(e.refers_to)
                if claim is None:
                    raise InvariantViolation(f"entry {e.index}: a verification that refers to no exposed claim")
                canon.verify(claim, e.author)
            else:
                notes.append(e)
        except InvariantViolation:
            raise
        except (EndProposedByMachine, OrganonRefused, GroundIsNotSubject, NoAcknowledgedEnd, LimitReached,
                KeyError, ValueError, TypeError) as exc:
            raise InvariantViolation(f"entry {e.index} ({e.kind} by {e.author}): {exc}") from exc
    propagate(claims)
    return Projection(ends, claims, footprint, budget, machine, notes, not_counted, len(entries))


def _claim(e: Entry, p: dict, ends: EndsRegistry, budget: GroundBudget, footprint: GroundFootprint, canon: Canon,
           claims: List[Claim]) -> Claim:
    if p["source"] != e.author:
        raise InvariantViolation(f"entry {e.index}: exposed by {e.author!r} but names {p['source']!r} as its source")
    end = ends.find(p["end"])
    if end is None or not end.is_acknowledged:
        raise InvariantViolation(f"entry {e.index}: a claim under {p['end']!r}, which no one had acknowledged")
    if p["syntax"] != RUN_STEP_NAMES:
        raise InvariantViolation(f"entry {e.index}: the run did not pass through the syntax in order: {p['syntax']}")
    deps = [
        GroundDependency(GroundKind[d["kind"]], d["description"], d["location"], d["maintained_by"], d["quantity"], d["unit"])
        for d in p["ground_dependencies"]
    ]
    budget.check(footprint, deps)
    for d in deps:
        footprint.add(d)
    claim = Claim(
        claim_id=p["claim_id"],
        content=p["content"],
        source=e.author,
        end_id=p["end"],
        function=SymbolicFunction[p["function"]],
        direction=Direction[p["direction"]],
        determines_object=p["determines_object"],
        grounds=list(p["grounds"]),
        procedures=[Procedure(ProcedureKind[x["kind"]], x["description"], x["public"], x["restricted_to"]) for x in p["procedures"]],
        returns_to_perception=p["returns_to_perception"],
        flags=list(p["flags"]),
        ground=list(p["ground"]),
        exposed_at=e.index,
        revises=p.get("revises"),
        depends_on=list(p.get("depends_on", [])),
    )
    unknown = [d for d in claim.depends_on if d not in {c.claim_id for c in claims}]
    if unknown:
        raise InvariantViolation(f"entry {e.index}: depends on claims never exposed before it: {unknown}")
    missing = [f for f in canon.admission_flags(claim) if f not in claim.flags]
    if missing:
        raise InvariantViolation(f"entry {e.index}: flags that admission gives this claim are missing from the record: {missing}")
    return claim


def report_from_record(world: CommonWorld) -> Report:
    """The metatheoretical report, computed from the public record alone."""
    return report(replay(world).claims)
