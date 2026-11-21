"""SSH signatures (OpenSSH PROTOCOL.sshsig) for ed25519 keys.

People already hold SSH keys, and `ssh-keygen -Y sign -n gaia-techne` makes
signatures that this module verifies; signatures made here verify with
`ssh-keygen -Y verify`. That is why the kernel uses this format rather than a
format of its own: a correction counts when a person signs it with a key they
use elsewhere, and anyone can check it with standard tools.

A signature covers the namespace and the SHA-512 hash of the message:

    "SSHSIG" || string(namespace) || string("") || string("sha512") || string(H(message))

and is stored as

    "SSHSIG" || uint32(1) || string(publickey) || string(namespace) || string("")
             || string("sha512") || string(signature)

with `string` the SSH wire encoding (uint32 length, then the bytes).
Only ed25519 keys are supported.
"""

from __future__ import annotations

import base64
import hashlib
import struct
from dataclasses import dataclass
from typing import Tuple

from . import ed25519

MAGIC = b"SSHSIG"
VERSION = 1
NAMESPACE = "gaia-techne"
KEY_TYPE = b"ssh-ed25519"
BEGIN = "-----BEGIN SSH SIGNATURE-----"
END = "-----END SSH SIGNATURE-----"


class BadSignature(ValueError):
    """The signature cannot be read, or it was not made over this message by this key."""


def _string(b: bytes) -> bytes:
    return struct.pack(">I", len(b)) + b


def _read(buf: bytes, at: int) -> Tuple[bytes, int]:
    if at + 4 > len(buf):
        raise BadSignature("truncated")
    (n,) = struct.unpack(">I", buf[at:at + 4])
    at += 4
    if at + n > len(buf):
        raise BadSignature("truncated")
    return buf[at:at + n], at + n


def public_blob(public: bytes) -> bytes:
    return _string(KEY_TYPE) + _string(public)


def format_public_key(public: bytes, comment: str = "") -> str:
    """The key as it appears in authorized_keys and allowed_signers files."""
    line = "ssh-ed25519 " + base64.b64encode(public_blob(public)).decode()
    return f"{line} {comment}".strip()


def parse_public_key(text: str) -> bytes:
    """Raw 32-byte ed25519 key from "ssh-ed25519 AAAA... [comment]"."""
    parts = text.split()
    if len(parts) < 2 or parts[0] != "ssh-ed25519":
        raise BadSignature(f"not an ssh-ed25519 public key: {text[:40]!r}")
    blob = base64.b64decode(parts[1])
    kind, at = _read(blob, 0)
    key, at = _read(blob, at)
    if kind != KEY_TYPE or len(key) != 32 or at != len(blob):
        raise BadSignature("not an ssh-ed25519 public key")
    return key


def _signed_data(message: bytes, namespace: str) -> bytes:
    return (MAGIC + _string(namespace.encode()) + _string(b"") + _string(b"sha512")
            + _string(hashlib.sha512(message).digest()))


@dataclass(frozen=True)
class Signature:
    public: bytes
    namespace: str
    raw: bytes  # the 64-byte ed25519 signature

    def blob(self) -> bytes:
        sig = _string(KEY_TYPE) + _string(self.raw)
        return (MAGIC + struct.pack(">I", VERSION) + _string(public_blob(self.public)) + _string(self.namespace.encode())
                + _string(b"") + _string(b"sha512") + _string(sig))

    def armor(self) -> str:
        b64 = base64.b64encode(self.blob()).decode()
        lines = [b64[i:i + 70] for i in range(0, len(b64), 70)]
        return "\n".join([BEGIN, *lines, END])


def sign(secret: bytes, message: bytes, namespace: str = NAMESPACE) -> Signature:
    return Signature(ed25519.public_key(secret), namespace, ed25519.sign(secret, _signed_data(message, namespace)))


def unarmor(text: str) -> Signature:
    body = text.strip()
    if not body.startswith(BEGIN) or not body.endswith(END):
        raise BadSignature("not an armored SSH signature")
    blob = base64.b64decode("".join(body[len(BEGIN):-len(END)].split()))
    if not blob.startswith(MAGIC):
        raise BadSignature("no SSHSIG magic")
    at = len(MAGIC)
    (version,) = struct.unpack(">I", blob[at:at + 4])
    at += 4
    if version != VERSION:
        raise BadSignature(f"unsupported version {version}")
    pub, at = _read(blob, at)
    namespace, at = _read(blob, at)
    _reserved, at = _read(blob, at)
    hash_alg, at = _read(blob, at)
    sig, at = _read(blob, at)
    if hash_alg != b"sha512":
        raise BadSignature(f"unsupported hash {hash_alg!r}")
    kind, k = _read(pub, 0)
    key, _ = _read(pub, k)
    skind, s = _read(sig, 0)
    raw, _ = _read(sig, s)
    if kind != KEY_TYPE or skind != KEY_TYPE:
        raise BadSignature("only ssh-ed25519 signatures are supported")
    return Signature(key, namespace.decode(), raw)


def verify(text: str, message: bytes, public: bytes, namespace: str = NAMESPACE) -> bool:
    """True if `text` is a signature over `message` by `public` in `namespace`."""
    try:
        sig = unarmor(text)
    except (BadSignature, ValueError, struct.error):
        return False
    if sig.public != public or sig.namespace != namespace:
        return False
    return ed25519.verify(public, _signed_data(message, namespace), sig.raw)
