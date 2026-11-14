"""The runtime: one run passes through the syntax, step by step.

    Ground -> Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger

It keeps the base of the v10 AGT syntax (Werk -> Trace -> Profile ->
Regression -> Horizon -> Descent -> Judgment -> Ledger) and changes its
centre: the unit is no longer a judgment issued by the runtime, but a claim
offered to others for correction.

- Ground: the geomorphic conditions the run depends on, who maintains them,
  and whether the run stays within the allowances people set (koinos.ground).
- Werk: a task, always under an acknowledged end (ethos).
- Trace: the premises used, each with its provenance (ethos.premises).
- Claim: the output, as a judgment of perception (canon).
- Ascent: the direction of the claim, tagged by the prism (koinos.prism).
- Horizon: the guards of the three ideas (canon.guards).
- Descent: the perception in which the claim can be tested (canon).
- Exposure: the claim is recorded in the common world (koinos.common_world).
- Correction: others measure it by public procedures (canon.judgment).
- Ledger: the record and its metatheoretical report (metatheory).

`Runtime.process` enters the first eight steps through a `RunTrace`, which
refuses any other order, and records the steps with the claim. Corrections
and verifications refer to the entry that exposed the claim.

The runtime is, by design, a practical automaton in Sellars's sense: purposes
come in from people, facts come in with provenance, procedures transform them,
claims come out (Sellars, 2007, p. 431). The premise of the form "any of us"
is never inside it; it stays with those who state and contest ends.

The model that generates text is an adapter. The architecture does not
depend on any particular model: what it fixes are the conditions under which
any model's output may count as a claim at all.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional

from ._version import __version__
from .adapters import as_adapter, declared_ground
from .boundaries import is_machine, refuse_ground_as_subject, require_author
from .canon.claims import Claim, CorrectionEvent, Procedure
from .canon.judgment import Canon
from .ethos.ends import AllowanceSetByMachine, End, EndsRegistry
from .ethos.imperatives import NoAcknowledgedEnd
from .ethos.premises import Premise, unattributed
from .koinos.common_world import CommonWorld
from .koinos.ground import Allowance, GroundBudget, GroundDependency, GroundFootprint, GroundKind
from .koinos.prism import Direction, SymbolicFunction
from .metatheory.indices import Report, report
from .metatheory.replay import replay
from .syntax import SYNTAX, RunTrace, Step, SyntaxViolation


@dataclass
class Werk:
    task: str
    end_id: str
    requested_by: str
    function: SymbolicFunction
    direction: Direction
    premises: List[Premise] = field(default_factory=list)
    procedures: List[Procedure] = field(default_factory=list)
    returns_to_perception: Optional[str] = None
    ground: List[GroundDependency] = field(default_factory=list)
    determines_object: bool = True


def _ground_record(d: GroundDependency) -> dict:
    return {
        "kind": d.kind.name,
        "description": d.description,
        "location": d.location,
        "maintained_by": d.maintained_by,
        "quantity": d.quantity,
        "unit": d.unit,
    }


class Runtime:
    def __init__(self, generator: Any, source_name: Optional[str] = None, world: Optional[CommonWorld] = None) -> None:
        name = source_name or getattr(generator, "name", None) or "model"
        self.adapter = as_adapter(generator, name)
        self.source_name = name
        self.machine_authors = {name, getattr(self.adapter, "name", name)}
        self.world = world if world is not None else CommonWorld()
        self.ends = EndsRegistry(record=self.world, machine_authors=self.machine_authors)
        self.canon = Canon(machine_authors=self.machine_authors)
        self.budget = GroundBudget()
        self.footprint = GroundFootprint()
        self.claims: List[Claim] = []
        self.world.record(
            author=self.source_name,
            kind="runtime",
            payload={
                "source": self.source_name,
                "names": sorted(self.machine_authors),
                "version": __version__,
                "syntax": [s.name for s in SYNTAX],
            },
        )

    @classmethod
    def resume(cls, world: CommonWorld, generator: Any, source_name: Optional[str] = None) -> "Runtime":
        """Continue from a record: replay it (which re-checks it), then act on what it says.

        The state of a runtime is a reading of its record. Nothing is carried over
        that the record does not contain.
        """
        projection = replay(world)
        rt = cls(generator, source_name=source_name, world=world)
        names = projection.machine_authors | rt.machine_authors
        rt.machine_authors = names
        rt.ends = projection.ends
        rt.ends.record = world
        rt.ends.machine_authors = names
        rt.canon.machine_authors = names
        rt.claims = projection.claims
        rt.footprint = projection.footprint
        rt.budget = projection.budget
        return rt

    # -- one run ---------------------------------------------------------------

    def process(self, werk: Werk) -> Claim:
        trace = RunTrace()
        pending: List[str] = []

        # Ground: what the run depends on, who maintains it, and whether it stays within the allowances.
        trace.enter(Step.GROUND)
        deps = list(werk.ground) + declared_ground(self.adapter)
        if not deps:
            pending.append("geomorphic: the ground this run depends on was not declared")
        for d in deps:
            if not d.maintained_by.strip():
                pending.append(f"geomorphic: no one declared as maintaining {d.kind.name}")
        pending.extend(self.budget.check(self.footprint, deps))  # LimitReached before anything is drawn

        # Werk: no action without an acknowledged end.
        trace.enter(Step.WERK)
        require_author(werk.requested_by)
        refuse_ground_as_subject(werk.requested_by)
        end = self.ends.find(werk.end_id)
        if end is None or not end.is_acknowledged:
            raise NoAcknowledgedEnd(f"{werk.end_id!r} has not been acknowledged by anyone")
        if is_machine(werk.requested_by, self.machine_authors):
            pending.append("werk: requested by the system itself; the end is acknowledged, but no person brought this task")

        # Trace: the automaton boundary.
        trace.enter(Step.TRACE)
        orphan = unattributed(werk.premises, self.machine_authors)
        if orphan:
            pending.append(f"automaton boundary: {len(orphan)} premise(s) without provenance")

        # Claim: the output as a judgment of perception.
        trace.enter(Step.CLAIM)
        content = self.adapter.generate(werk.task, list(werk.premises))
        if not isinstance(content, str):
            raise TypeError("a generator returns text; what the text may count as is decided by the canon and by others")
        claim = Claim(
            claim_id=f"c{len(self.claims) + 1}",
            content=content,
            source=self.source_name,
            end_id=werk.end_id,
            function=werk.function,
            direction=werk.direction,
            determines_object=werk.determines_object,
            grounds=[f"{p.text} [{p.source or 'no source'}]" for p in werk.premises],
            procedures=list(werk.procedures),
            returns_to_perception=werk.returns_to_perception,
            ground=[d.describe() for d in deps],
        )
        self.canon.perceive(claim)
        for d in deps:
            self.footprint.add(d)
        claim.flags.extend(pending)

        # Ascent, Horizon, Descent.
        trace.enter(Step.ASCENT)
        self.canon.ascent(claim)
        trace.enter(Step.HORIZON)
        self.canon.horizon(claim)
        trace.enter(Step.DESCENT)
        self.canon.descent(claim)

        # Exposure.
        trace.enter(Step.EXPOSURE)
        entry = self.world.record(
            author=self.source_name,
            kind="claim",
            payload=self._claim_record(claim, end, werk, deps, trace),
            refers_to=end.recorded_at,
        )
        claim.exposed_at = entry.index
        self.claims.append(claim)
        return claim

    @staticmethod
    def _claim_record(claim: Claim, end: End, werk: Werk, deps: List[GroundDependency], trace: RunTrace) -> dict:
        return {
            "claim_id": claim.claim_id,
            "content": claim.content,
            "source": claim.source,
            "end": end.end_id,
            "end_contested": end.is_contested,
            "requested_by": werk.requested_by,
            "function": claim.function.name,
            "direction": claim.direction.name,
            "determines_object": claim.determines_object,
            "grounds": claim.grounds,
            "procedures": [
                {"kind": p.kind.name, "description": p.description, "public": p.public, "restricted_to": p.restricted_to}
                for p in claim.procedures
            ],
            "returns_to_perception": claim.returns_to_perception,
            "flags": claim.flags,
            "ground": claim.ground,
            "ground_dependencies": [_ground_record(d) for d in deps],
            "syntax": trace.names(),
        }

    # -- the life of a claim after exposure --------------------------------------

    def _exposed(self, claim: Claim, act: str) -> int:
        if claim.exposed_at is None:
            raise SyntaxViolation(
                f"{act} cannot precede EXPOSURE: no one can measure or answer for a claim that was never offered to them"
            )
        return claim.exposed_at

    def correct(self, claim: Claim, event: CorrectionEvent) -> Claim:
        """Correction: only others can widen a claim's reach, and only once it has been exposed."""
        at = self._exposed(claim, "CORRECTION")
        self.canon.correct(claim, event)
        self.world.record(
            author=event.by,
            kind="correction",
            payload={
                "claim_id": claim.claim_id,
                "by": event.by,
                "procedure": event.procedure.name,
                "upheld": event.upheld,
                "community_reach": event.community_reach.name,
                "note": event.note,
            },
            refers_to=at,
        )
        return claim

    def verify(self, claim: Claim, person: str) -> Claim:
        """A person takes responsibility for using a result that cannot yet be tested."""
        at = self._exposed(claim, "a verification")
        self.canon.verify(claim, person)
        self.world.record(
            author=person,
            kind="verification",
            payload={"claim_id": claim.claim_id, "person": person},
            refers_to=at,
        )
        return claim

    # -- ends and allowances -----------------------------------------------------

    def propose_derived_end(self, parent_id: str, end_id: str, statement: str) -> End:
        """The system may propose an instrumental end; only people can make it usable."""
        return self.ends.derive(parent_id, end_id, statement, derived_by=self.source_name)

    def allow(self, kind: GroundKind, unit: str, limit: float, set_by: str, end_id: str, reason: str = "") -> Allowance:
        """People set how much of one kind of ground the runs may draw, under an acknowledged end."""
        require_author(set_by)
        refuse_ground_as_subject(set_by)
        if is_machine(set_by, self.machine_authors):
            raise AllowanceSetByMachine("The runtime cannot set or widen the allowance of the ground it draws on.")
        end = self.ends.find(end_id)
        if end is None or not end.is_acknowledged:
            raise NoAcknowledgedEnd(f"an allowance is set under an acknowledged end; {end_id!r} is not one")
        allowance = Allowance(kind, unit, limit, set_by, end_id, reason)
        self.budget.set(allowance)
        self.world.record(
            author=set_by,
            kind="allowance_set",
            payload={"kind": kind.name, "unit": unit, "limit": limit, "set_by": set_by, "end_id": end_id, "reason": reason},
            refers_to=end.recorded_at,
        )
        return allowance

    # -- ledger ------------------------------------------------------------------

    def ledger(self, claims: Optional[Iterable[Claim]] = None) -> Report:
        return report(self.claims if claims is None else claims)
