"""The kernel: one facade over the record, the identities, the proofs and the grants.

The kernel is a canon, not an organon. It produces nothing: claims still come
from the runtime and its generator, ends and corrections still come from
people. What it adds is the means of checking, from the record alone, that
the acts the architecture forbids did not happen and that the acts it counts
were made by those who are said to have made them:

- K1  the record is a Merkle log; checkpoints are signed and witnessed, and
      every later size is provably an extension of every earlier one;
- K2  the runtime, a model or a tool never corrects, acknowledges or verifies
      (enforced by the canon and the ends registry, checked again on replay);
- K3  where principals are configured, a correction, verification or
      acknowledgment counts only if its author's key signed it;
- K4  a claim whose premise was refuted or revised is not usable;
- K5  a capability can only be narrowed;
- K6  untrusted premises never reach the plan, and an outbound tool cannot be
      sent to an address that only untrusted text supplied;
- K8  the status of the record can be asked as of any entry;
- K9  the carbon intensity of the runs is reported, or reported as unmetered.

`status()` replays the record; it is the reading that counts. The runtime's
objects in memory are one reading among others (README §10.1).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional, Tuple

from ..agent.loop import Agent, AgentRun, Task
from ..boundaries import is_machine, refuse_ground_as_subject, require_author
from ..canon.claims import Claim, CorrectionEvent
from ..koinos.common_world import CommonWorld, Entry
from ..metatheory.replay import RECOGNITION, Projection, replay
from ..pipeline import Runtime
from . import ed25519, log, prov, sshsig
from .capabilities import Capability, CapabilityRefused, Minter
from .identity import Keyring, Principals
from .sci import SCI, sci

LOG_KEY = "gaia-techne-log"


class GrantRefused(PermissionError):
    """Only a person can grant a capability, and only under an end they may bring tasks under."""


@dataclass
class Status:
    """What the record says, as of an entry, counting only the acts that count."""

    size: int
    projection: Projection
    sci: SCI
    not_counted: List[Tuple[int, str]]

    @property
    def claims(self) -> List[Claim]:
        return self.projection.claims

    def claim(self, claim_id: str) -> Claim:
        for c in self.claims:
            if c.claim_id == claim_id:
                return c
        raise KeyError(claim_id)

    def summary(self) -> str:
        from ..canon.judgment import Canon

        canon = Canon()
        lines = [f"entries: {self.size}"]
        for c in self.claims:
            state = "usable" if canon.usable(c) else "not usable"
            extra = f"; premises fell: {'; '.join(c.premises_fallen)}" if c.premises_fallen else ""
            lines.append(f"  {c.claim_id} [{c.stage.value}, reach {c.reach.name}, {state}]{extra}")
        for i, why in self.not_counted:
            lines.append(f"  entry {i} does not count: {why}")
        lines.append("  " + self.sci.describe())
        return "\n".join(lines)


def status_of(world: CommonWorld, principals: Optional[Principals] = None, as_of: Optional[int] = None,
              carbon_intensity: Optional[float] = None) -> Status:
    """The status of a record anyone holds, with the public keys anyone can hold. No secret is needed."""
    admit = None
    if principals:
        admit = lambda e: principals.check(e.author, e.digest, e.signature)  # noqa: E731
    proj = replay(world, until=as_of, admit=admit)
    return Status(proj.size, proj, sci(proj.footprint, len(proj.claims), carbon_intensity), proj.not_counted)


@dataclass
class Kernel:
    runtime: Runtime
    keyring: Keyring = field(default_factory=Keyring)
    principals: Principals = field(default_factory=Principals)
    minter: Minter = field(default_factory=Minter)
    carbon_intensity: Optional[float] = None  # gCO2e/kWh of the energy the runs draw, if anyone measured it
    log_secret: bytes = field(default_factory=ed25519.generate_secret, repr=False)

    def __post_init__(self) -> None:
        source = self.runtime.source_name
        if source not in self.keyring.secrets:
            self.principals.add(source, self.keyring.create(source))
        for name, secret in self.keyring.secrets.items():
            self.principals.keys.setdefault(name, ed25519.public_key(secret))
        self.runtime.world.signer = self.keyring.sign

    @property
    def world(self) -> CommonWorld:
        return self.runtime.world

    @property
    def log_public(self) -> bytes:
        return ed25519.public_key(self.log_secret)

    # -- identity --------------------------------------------------------------

    def enroll(self, person: str, public: Optional[Any] = None) -> bytes:
        """Register a person's public key; with no key given, create one in the local keyring (demonstration)."""
        require_author(person)
        refuse_ground_as_subject(person)
        if is_machine(person, self.runtime.machine_authors):
            raise GrantRefused(f"{person!r} is a name of the system; it is not enrolled as a person")
        if public is None:
            public = self.keyring.create(person)
        self.principals.add(person, public)
        return self.principals.keys[person]

    def admit(self, e: Entry) -> Optional[str]:
        """K3: None if the act counts, otherwise why not. Without principals, every act counts (demo mode)."""
        if not self.principals:
            return None
        return self.principals.check(e.author, e.digest, e.signature)

    def attach(self, index: int, armored: str) -> Entry:
        """Attach a signature made elsewhere (`ssh-keygen -Y sign -n gaia-techne`) over an entry's digest."""
        e = self.world.entries()[index]
        why = self.principals.check(e.author, e.digest, armored)
        if why is not None:
            raise sshsig.BadSignature(why)
        return self.world.attach_signature(index, armored)

    # -- reading ---------------------------------------------------------------

    def status(self, as_of: Optional[int] = None) -> Status:
        return status_of(self.world, self.principals, as_of, self.carbon_intensity)

    def unsigned_acts(self) -> List[Tuple[int, str]]:
        return [(e.index, why) for e in self.world.entries() if e.kind in RECOGNITION for why in [self.admit(e)] if why]

    def prov(self) -> Dict[str, Any]:
        return prov.export(self.world)

    # -- the log ---------------------------------------------------------------

    def checkpoint(self, size: Optional[int] = None) -> log.Checkpoint:
        return log.checkpoint(self.world, size).sign(LOG_KEY, self.log_secret)

    def prove_inclusion(self, index: int, size: Optional[int] = None) -> List[bytes]:
        return log.prove_inclusion(self.world, index, size)

    def prove_consistency(self, old_size: int, size: Optional[int] = None) -> List[bytes]:
        return log.prove_consistency(self.world, old_size, size)

    def witness(self, witness: log.Witness) -> log.Checkpoint:
        """Ask a witness to cosign the current checkpoint, proving it extends the last one it saw."""
        cp = self.checkpoint()
        last = witness.seen.get(cp.origin)
        proof = self.prove_consistency(last.size, cp.size) if last is not None and 0 < last.size <= cp.size else []
        return witness.cosign(cp, proof, LOG_KEY, self.log_public)

    # -- grants and the agent ------------------------------------------------------

    def grant(self, person: str, end_id: str, tools: Optional[List[str]] = None, max_steps: Optional[int] = None,
              before: Optional[str] = None) -> Capability:
        """A person gives the agent a capability under an end they could bring a task under."""
        require_author(person)
        refuse_ground_as_subject(person)
        if is_machine(person, self.runtime.machine_authors):
            raise GrantRefused("the system cannot grant itself a capability")
        end = self.runtime.ends.find(end_id)
        if end is None or not end.is_acknowledged:
            raise GrantRefused(f"{end_id!r} has not been acknowledged by anyone")
        caveats = [f"end = {end_id}", f"by = {person}"]
        if tools is not None:
            caveats.append(f"tools <= {','.join(tools)}")
        if max_steps is not None:
            caveats.append(f"max_steps <= {max_steps}")
        if before is not None:
            caveats.append(f"before = {before}")
        identifier = os.urandom(8).hex()
        cap = self.minter.mint(identifier, caveats)
        self.world.record(person, "capability_granted", {"id": identifier, "caveats": caveats, "by": person},
                          refers_to=end.recorded_at)
        return cap

    def pursue(self, agent: Agent, task: Task, capability: Capability) -> AgentRun:
        """Run the agent only within what the capability grants (K5), for the person it was granted to."""
        grant = self.minter.verify(capability, task.end_id, task.requested_by)
        tools = task.tools
        if grant.tools is not None:
            tools = sorted(grant.tools if tools is None else set(tools) & grant.tools)
        steps = task.max_steps if grant.max_steps is None else min(task.max_steps, grant.max_steps)
        return agent.pursue(replace(task, tools=tools, max_steps=steps))

    # -- people's acts, signed --------------------------------------------------------

    def correct(self, claim: Claim, event: CorrectionEvent) -> Claim:
        return self.runtime.correct(claim, event)

    def verify(self, claim: Claim, person: str) -> Claim:
        return self.runtime.verify(claim, person)


__all__ = ["Kernel", "Status", "status_of", "GrantRefused", "CapabilityRefused", "LOG_KEY"]
