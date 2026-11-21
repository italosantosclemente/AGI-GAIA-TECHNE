"""Capabilities that can only be narrowed (macaroon-style).

A person who brings a task under an end gives the agent a capability: a token
that names the end, the person and the tools allowed, signed with a key the
kernel keeps. Anyone holding the token can attenuate it, by adding a caveat,
but no one can remove one: each caveat is folded into an HMAC chain, so the
signature of a token with a caveat removed no longer verifies (Birgisson et
al., "Macaroons", NDSS 2014). Every caveat must hold for the token to grant
anything, so adding one can only narrow what it grants (K5).

Caveats are plain text, `key op value`:

    end = E          the token is good only under end E
    by = P           only for tasks brought by person P
    tools <= a,b     at most these tools (the intersection over all such caveats)
    max_steps <= N   at most N plan steps
    before = T       only before the ISO time T
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple


class CapabilityRefused(PermissionError):
    """The token does not verify, or one of its caveats does not hold."""


def _mac(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _parse(caveat: str) -> Tuple[str, str, str]:
    for op in ("<=", "="):
        if f" {op} " in caveat:
            k, v = caveat.split(f" {op} ", 1)
            return k.strip(), op, v.strip()
    raise CapabilityRefused(f"a caveat must read 'key op value': {caveat!r}")


KNOWN = {("end", "="), ("by", "="), ("tools", "<="), ("max_steps", "<="), ("before", "=")}


@dataclass(frozen=True)
class Capability:
    identifier: str
    caveats: Tuple[str, ...]
    signature: str  # hex HMAC chain

    def attenuate(self, caveat: str) -> "Capability":
        """A narrower token: everything this one grants, under one condition more."""
        k, op, _ = _parse(caveat)
        if (k, op) not in KNOWN:
            raise CapabilityRefused(f"unknown caveat {caveat!r}: an unknown condition could not be checked")
        sig = _mac(bytes.fromhex(self.signature), caveat).hex()
        return Capability(self.identifier, self.caveats + (caveat,), sig)

    def serialize(self) -> str:
        body = {"id": self.identifier, "caveats": list(self.caveats), "sig": self.signature}
        return base64.urlsafe_b64encode(json.dumps(body, separators=(",", ":")).encode()).decode()

    @classmethod
    def parse(cls, token: str) -> "Capability":
        try:
            d = json.loads(base64.urlsafe_b64decode(token.encode()))
            return cls(d["id"], tuple(d["caveats"]), d["sig"])
        except (ValueError, KeyError, TypeError) as exc:
            raise CapabilityRefused(f"not a capability: {exc}") from exc


@dataclass(frozen=True)
class Grant:
    """What a verified token allows."""

    end: Optional[str]
    by: Optional[str]
    tools: Optional[Set[str]]  # None: no tools caveat (every tool the agent has)
    max_steps: Optional[int]


@dataclass
class Minter:
    """Holds the root key. Minting is the kernel's; deciding what to grant is a person's."""

    root_key: bytes = field(default_factory=lambda: os.urandom(32), repr=False)

    def mint(self, identifier: str, caveats: List[str]) -> Capability:
        cap = Capability(identifier, (), _mac(self.root_key, identifier).hex())
        for c in caveats:
            cap = cap.attenuate(c)
        return cap

    def verify(self, cap: Capability, end: str, by: str, now: Optional[str] = None) -> Grant:
        sig = _mac(self.root_key, cap.identifier)
        for c in cap.caveats:
            sig = _mac(sig, c)
        if not hmac.compare_digest(sig.hex(), cap.signature):
            raise CapabilityRefused("the token does not verify: a caveat was removed or changed, or it was not minted here")
        now = now or datetime.now(timezone.utc).isoformat()
        tools: Optional[Set[str]] = None
        max_steps: Optional[int] = None
        named: Dict[str, Set[str]] = {"end": set(), "by": set()}
        for c in cap.caveats:
            k, op, v = _parse(c)
            if (k, op) not in KNOWN:
                raise CapabilityRefused(f"unknown caveat {c!r}")
            if k in named:
                named[k].add(v)
            elif k == "tools":
                allowed = {t.strip() for t in v.split(",") if t.strip()}
                tools = allowed if tools is None else tools & allowed
            elif k == "max_steps":
                max_steps = int(v) if max_steps is None else min(max_steps, int(v))
            elif k == "before" and not now < v:
                raise CapabilityRefused(f"the token expired at {v}")
        if named["end"] and named["end"] != {end}:
            raise CapabilityRefused(f"the token is for end(s) {sorted(named['end'])}, not {end!r}")
        if named["by"] and named["by"] != {by}:
            raise CapabilityRefused(f"the token is for tasks brought by {sorted(named['by'])}, not {by!r}")
        return Grant(end, by, tools, max_steps)
