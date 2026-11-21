"""The common world as a transparency log: checkpoints, proofs, witnesses.

Leaves are the canonical JSON of each entry, signature included, so that a
checkpoint commits to who signed as well as to what was said. A checkpoint
is a signed note in the C2SP formats (c2sp.org/tlog-checkpoint, c2sp.org/signed-note):

    <origin>
    <size>
    <base64 root>

    — <name> <base64(key id || ed25519 signature)>

The kernel signs it; witnesses, who keep the last checkpoint they saw, cosign
it only after checking that it is consistent with that one. A record keeper who
shows different histories to different people is then caught as soon as two
of them compare checkpoints, or a witness compares them for everyone (K1).
"""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from ..koinos.common_world import CommonWorld, Entry, canonical
from . import ed25519, merkle

ORIGIN = "gaia-techne/common-world"


class InconsistentLog(ValueError):
    """A checkpoint does not extend the one seen before it, or a proof does not verify."""


def leaf_data(e: Entry) -> bytes:
    return canonical(e.to_dict()).encode("utf-8")


def leaves(world: CommonWorld, size: Optional[int] = None) -> List[bytes]:
    entries = world.entries() if size is None else world.entries()[:size]
    return [merkle.leaf_hash(leaf_data(e)) for e in entries]


def key_id(name: str, public: bytes) -> bytes:
    return hashlib.sha256(name.encode() + b"\n" + b"\x01" + public).digest()[:4]


@dataclass
class Checkpoint:
    origin: str
    size: int
    root: bytes
    signatures: List[Tuple[str, bytes]] = field(default_factory=list)  # (name, key id || signature)

    def body(self) -> str:
        return f"{self.origin}\n{self.size}\n{base64.b64encode(self.root).decode()}\n"

    def sign(self, name: str, secret: bytes) -> "Checkpoint":
        pub = ed25519.public_key(secret)
        sig = ed25519.sign(secret, self.body().encode())
        self.signatures.append((name, key_id(name, pub) + sig))
        return self

    def signed_by(self, name: str, public: bytes) -> bool:
        kid = key_id(name, public)
        for n, blob in self.signatures:
            if n == name and blob[:4] == kid and ed25519.verify(public, self.body().encode(), blob[4:]):
                return True
        return False

    def text(self) -> str:
        sigs = "".join(f"— {n} {base64.b64encode(b).decode()}\n" for n, b in self.signatures)
        return self.body() + "\n" + sigs

    @classmethod
    def parse(cls, text: str) -> "Checkpoint":
        head, _, tail = text.partition("\n\n")
        lines = head.split("\n")
        if len(lines) < 3:
            raise InconsistentLog("not a checkpoint")
        cp = cls(lines[0], int(lines[1]), base64.b64decode(lines[2]))
        for line in tail.splitlines():
            if line.startswith("— "):
                _, name, b64 = line.split(" ", 2)
                cp.signatures.append((name, base64.b64decode(b64)))
        return cp


def checkpoint(world: CommonWorld, size: Optional[int] = None, origin: str = ORIGIN) -> Checkpoint:
    ls = leaves(world, size)
    return Checkpoint(origin, len(ls), merkle.root(ls))


def prove_inclusion(world: CommonWorld, index: int, size: Optional[int] = None) -> List[bytes]:
    return merkle.inclusion_proof(leaves(world, size), index)


def prove_consistency(world: CommonWorld, old_size: int, size: Optional[int] = None) -> List[bytes]:
    return merkle.consistency_proof(leaves(world, size), old_size)


def check_inclusion(entry: Entry, cp: Checkpoint, proof: Sequence[bytes]) -> bool:
    return merkle.verify_inclusion(merkle.leaf_hash(leaf_data(entry)), entry.index, cp.size, proof, cp.root)


@dataclass
class Witness:
    """Keeps the last checkpoint it cosigned and cosigns only what extends it."""

    name: str
    secret: bytes = field(default_factory=ed25519.generate_secret, repr=False)
    seen: Dict[str, Checkpoint] = field(default_factory=dict)

    @property
    def public(self) -> bytes:
        return ed25519.public_key(self.secret)

    def cosign(self, cp: Checkpoint, proof: Sequence[bytes], log_name: str, log_key: bytes) -> Checkpoint:
        if not cp.signed_by(log_name, log_key):
            raise InconsistentLog(f"the checkpoint is not signed by the log {log_name!r}")
        last = self.seen.get(cp.origin)
        if last is not None:
            if cp.size < last.size:
                raise InconsistentLog(f"the log went back from size {last.size} to {cp.size}")
            if not merkle.verify_consistency(last.size, cp.size, last.root, cp.root, proof):
                raise InconsistentLog(f"size {cp.size} does not extend the size {last.size} this witness saw")
        cp.sign(self.name, self.secret)
        self.seen[cp.origin] = Checkpoint(cp.origin, cp.size, cp.root)
        return cp
