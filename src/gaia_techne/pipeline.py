"""The v2.0 syntax.

    Ground -> Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger

It keeps the base of the v10 AGT syntax (Werk -> Trace -> Profile ->
Regression -> Horizon -> Descent -> Judgment -> Ledger) and changes its
centre: the unit is no longer a judgment issued by the runtime, but a claim
offered to others for correction.

- Ground: the geomorphic conditions the run depends on: compute, energy,
  network, material and archive, and who maintains them (koinos.ground).
- Werk: a task, always under an acknowledged end (ethos).
- Trace: the premises used, each with its provenance (ethos.premises).
- Claim: the output, as a judgment of perception (canon.claims).
- Ascent: the direction toward signification (koinos.prism).
- Horizon: the guards of the three ideas (canon.guards).
- Descent: the perception in which the claim can be tested.
- Exposure: the claim is recorded in the common world (koinos.common_world).
- Correction: others measure it by public procedures (canon.judgment).
- Ledger: the record and its metatheoretical report (metatheory).

The model that generates text is an adapter. The architecture does not
depend on any particular model: what it fixes are the conditions under which
any model's output may count as a claim at all.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional

from .canon.claims import Claim, CorrectionEvent, Procedure
from .canon.judgment import Canon
from .ethos.ends import EndsRegistry
from .ethos.imperatives import NoAcknowledgedEnd
from .ethos.premises import Premise, unattributed
from .koinos.common_world import CommonWorld
from .koinos.ground import GroundDependency, GroundFootprint
from .koinos.prism import Direction, SymbolicFunction
from .metatheory.indices import Report, report

Generator = Callable[[str, List[Premise]], str]


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


class Runtime:
    def __init__(self, generator: Generator, source_name: str = "model") -> None:
        self.ends = EndsRegistry()
        self.world = CommonWorld()
        self.canon = Canon()
        self.generator = generator
        self.source_name = source_name
        self.claims: List[Claim] = []
        self.footprint = GroundFootprint()

    def process(self, werk: Werk) -> Claim:
        # Werk: no action without an acknowledged end.
        end = self.ends.find(werk.end_id)
        if end is None or not end.is_acknowledged:
            raise NoAcknowledgedEnd(f"{werk.end_id!r} has not been acknowledged by anyone")
        # Trace: the automaton boundary.
        orphan = unattributed(werk.premises)
        content = self.generator(werk.task, werk.premises)
        claim = Claim(
            claim_id=f"c{len(self.claims) + 1}",
            content=content,
            source=self.source_name,
            end_id=werk.end_id,
            function=werk.function,
            direction=werk.direction,
            grounds=[f"{p.text} [{p.source or 'no source'}]" for p in werk.premises],
            procedures=list(werk.procedures),
            returns_to_perception=werk.returns_to_perception,
            ground=[f"{d.kind.name}: {d.description} @ {d.location} (maintained by {d.maintained_by or 'unknown'})" for d in werk.ground],
        )
        # Ascent, Horizon, Descent.
        self.canon.admit(claim)
        if orphan:
            claim.flags.append(f"automaton boundary: {len(orphan)} premise(s) without provenance")
        # Ground: the formative power the run seems to have is borrowed.
        if not werk.ground:
            claim.flags.append("geomorphic: the ground this run depends on was not declared")
        for d in werk.ground:
            self.footprint.add(d)
            if not d.maintained_by.strip():
                claim.flags.append(f"geomorphic: no one declared as maintaining {d.kind.name}")
        # Exposure.
        self.world.record(
            author=self.source_name,
            kind="claim",
            payload={
                "claim_id": claim.claim_id,
                "content": claim.content,
                "end": end.end_id,
                "end_contested": end.is_contested,
                "requested_by": werk.requested_by,
                "flags": claim.flags,
                "ground": claim.ground,
            },
        )
        self.claims.append(claim)
        return claim

    def propose_derived_end(self, parent_id: str, end_id: str, statement: str):
        """The system may propose an instrumental end; only people can make it usable."""
        end = self.ends.derive(parent_id, end_id, statement, derived_by=self.source_name)
        end.derived_by_machine = True
        self.world.record(
            author=self.source_name,
            kind="derived_end",
            payload={"end_id": end_id, "parent": parent_id, "statement": statement, "acknowledged": False},
        )
        return end

    def correct(self, claim: Claim, event: CorrectionEvent) -> Claim:
        # Correction: only others can widen a claim's reach.
        self.canon.correct(claim, event)
        self.world.record(
            author=event.by,
            kind="correction",
            payload={"claim_id": claim.claim_id, "upheld": event.upheld, "procedure": event.procedure.name},
        )
        return claim

    def ledger(self, claims: Optional[Iterable[Claim]] = None) -> Report:
        return report(self.claims if claims is None else claims)
