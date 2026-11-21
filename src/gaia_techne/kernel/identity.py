"""Who acted: principals (public keys) and a local keyring (secret keys).

`Principals` is the public side and may be shared: a map from the names that
appear as authors in the common world to SSH ed25519 public keys. It reads and
writes the `allowed_signers` format of `ssh-keygen -Y verify`:

    ana@example.org namespaces="gaia-techne" ssh-ed25519 AAAA...

`Keyring` is the private side, for demonstrations and for people who sign on
their own machine. The kernel never needs a person's secret key: it accepts a
signature made elsewhere (`ssh-keygen -Y sign -n gaia-techne`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Union

from . import ed25519, sshsig


@dataclass
class Principals:
    keys: Dict[str, bytes] = field(default_factory=dict)

    def add(self, name: str, public: Union[bytes, str]) -> None:
        self.keys[name] = sshsig.parse_public_key(public) if isinstance(public, str) else public

    def __contains__(self, name: str) -> bool:
        return name in self.keys

    def __bool__(self) -> bool:
        return bool(self.keys)

    def check(self, author: str, digest: str, signature: Optional[str]) -> Optional[str]:
        """None if `signature` is `author`'s over `digest`; otherwise the reason it is not."""
        if signature is None:
            return "unsigned"
        key = self.keys.get(author)
        if key is None:
            return f"{author!r} has no key among the principals"
        if not sshsig.verify(signature, digest.encode(), key):
            return f"the signature is not {author!r}'s over this entry"
        return None

    def dumps(self) -> str:
        return "".join(
            f'{name} namespaces="{sshsig.NAMESPACE}" {sshsig.format_public_key(key)}\n' for name, key in sorted(self.keys.items())
        )

    @classmethod
    def loads(cls, text: str) -> "Principals":
        out = cls()
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r'(\S+)\s+(?:(\S*namespaces="[^"]*"\S*)\s+)?(ssh-ed25519\s+\S+)', line)
            if not m:
                continue
            opts = m.group(2) or ""
            ns = re.search(r'namespaces="([^"]*)"', opts)
            if ns and sshsig.NAMESPACE not in ns.group(1).split(","):
                continue
            for name in m.group(1).split(","):
                out.add(name, m.group(3))
        return out

    @classmethod
    def load(cls, path: Union[str, Path]) -> "Principals":
        return cls.loads(Path(path).read_text(encoding="utf-8"))


@dataclass
class Keyring:
    secrets: Dict[str, bytes] = field(default_factory=dict, repr=False)

    def create(self, name: str) -> bytes:
        """A new key for `name`; returns the public key."""
        self.secrets[name] = ed25519.generate_secret()
        return ed25519.public_key(self.secrets[name])

    def sign(self, name: str, digest: str) -> Optional[str]:
        secret = self.secrets.get(name)
        return None if secret is None else sshsig.sign(secret, digest.encode()).armor()

    def principals(self) -> Principals:
        return Principals({n: ed25519.public_key(s) for n, s in self.secrets.items()})
