"""Ed25519 (RFC 8032), with the `cryptography` package when it is installed.

Identity in the kernel is a key, not a name: an act counts as a person's only
when it carries a signature that their public key verifies. The project keeps
no hard dependency, so this module falls back to a small pure-Python
implementation of RFC 8032, section 5.1. It is slow and not constant-time:
good enough to verify a record and to sign in a demonstration, not to guard
keys on a shared machine. With `cryptography` installed, that library signs
and verifies, and the tests check the two against each other and against the
test vectors of RFC 8032, section 7.1.
"""

from __future__ import annotations

import hashlib
import os
from typing import Tuple

try:  # pragma: no cover - depends on the environment
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

    HAVE_CRYPTOGRAPHY = True
except ImportError:  # pragma: no cover
    HAVE_CRYPTOGRAPHY = False

# -- pure Python, RFC 8032 section 5.1 -------------------------------------------

_p = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_d = -121665 * pow(121666, _p - 2, _p) % _p
_I = pow(2, (_p - 1) // 4, _p)


def _H(m: bytes) -> bytes:
    return hashlib.sha512(m).digest()


def _add(P, Q):
    x1, y1, z1, t1 = P
    x2, y2, z2, t2 = Q
    a = (y1 - x1) * (y2 - x2) % _p
    b = (y1 + x1) * (y2 + x2) % _p
    c = 2 * t1 * t2 * _d % _p
    dd = 2 * z1 * z2 % _p
    e, f, g, h = b - a, dd - c, dd + c, b + a
    return (e * f % _p, g * h % _p, f * g % _p, e * h % _p)


def _mul(s: int, P):
    Q = (0, 1, 1, 0)
    while s:
        if s & 1:
            Q = _add(Q, P)
        P = _add(P, P)
        s >>= 1
    return Q


def _equal(P, Q) -> bool:
    return (P[0] * Q[2] - Q[0] * P[2]) % _p == 0 and (P[1] * Q[2] - Q[1] * P[2]) % _p == 0


def _recover_x(y: int, sign: int):
    if y >= _p:
        return None
    x2 = (y * y - 1) * pow(_d * y * y + 1, _p - 2, _p)
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_p + 3) // 8, _p)
    if (x * x - x2) % _p:
        x = x * _I % _p
    if (x * x - x2) % _p:
        return None
    if x & 1 != sign:
        x = _p - x
    return x


_gy = 4 * pow(5, _p - 2, _p) % _p
_gx = _recover_x(_gy, 0)
_G = (_gx, _gy, 1, _gx * _gy % _p)


def _compress(P) -> bytes:
    zinv = pow(P[2], _p - 2, _p)
    x, y = P[0] * zinv % _p, P[1] * zinv % _p
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _decompress(s: bytes):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % _p)


def _expand(secret: bytes) -> Tuple[int, bytes]:
    h = _H(secret)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def _py_public(secret: bytes) -> bytes:
    a, _ = _expand(secret)
    return _compress(_mul(a, _G))


def _py_sign(secret: bytes, msg: bytes) -> bytes:
    a, prefix = _expand(secret)
    A = _compress(_mul(a, _G))
    r = int.from_bytes(_H(prefix + msg), "little") % _L
    R = _compress(_mul(r, _G))
    k = int.from_bytes(_H(R + A + msg), "little") % _L
    return R + int.to_bytes((r + k * a) % _L, 32, "little")


def _py_verify(public: bytes, msg: bytes, sig: bytes) -> bool:
    if len(public) != 32 or len(sig) != 64:
        return False
    A = _decompress(public)
    R = _decompress(sig[:32])
    if A is None or R is None:
        return False
    s = int.from_bytes(sig[32:], "little")
    if s >= _L:
        return False
    k = int.from_bytes(_H(sig[:32] + public + msg), "little") % _L
    return _equal(_mul(s, _G), _add(R, _mul(k, A)))


# -- public interface --------------------------------------------------------------


def generate_secret() -> bytes:
    return os.urandom(32)


def public_key(secret: bytes) -> bytes:
    if HAVE_CRYPTOGRAPHY:
        from cryptography.hazmat.primitives import serialization

        k = Ed25519PrivateKey.from_private_bytes(secret).public_key()
        return k.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return _py_public(secret)


def sign(secret: bytes, msg: bytes) -> bytes:
    if HAVE_CRYPTOGRAPHY:
        return Ed25519PrivateKey.from_private_bytes(secret).sign(msg)
    return _py_sign(secret, msg)


def verify(public: bytes, msg: bytes, sig: bytes) -> bool:
    if HAVE_CRYPTOGRAPHY:
        try:
            Ed25519PublicKey.from_public_bytes(public).verify(sig, msg)
            return True
        except (InvalidSignature, ValueError):
            return False
    return _py_verify(public, msg, sig)
