"""A Merkle tree over the common world, in the manner of RFC 6962/9162.

The hash chain of `koinos.CommonWorld` already lets anyone holding the whole
file check that nothing was rewritten. A transparency log adds two things a
chain cannot give cheaply: a short commitment to the whole record at a given
size (the root, published in a checkpoint), and short proofs against it.

- an inclusion proof shows that one entry is in the record at that size,
  without handing over the rest;
- a consistency proof shows that the record at a later size extends the
  record at an earlier size, so that no one who saw the earlier checkpoint
  can be shown a rewritten past.

Hashing follows RFC 6962, section 2.1: leaves are SHA-256(0x00 || data),
interior nodes SHA-256(0x01 || left || right), and the tree over n leaves splits
at the largest power of two smaller than n. The proofs are the audit paths of
section 2.1.1 and the consistency proofs of section 2.1.2; the verification
algorithms are those of RFC 9162, sections 2.1.3.2 and 2.1.4.2.
"""

from __future__ import annotations

import hashlib
from typing import List, Sequence


def leaf_hash(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()


def node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


EMPTY_ROOT = hashlib.sha256(b"").digest()


def _split(n: int) -> int:
    """The largest power of two strictly smaller than n (n > 1)."""
    k = 1
    while k << 1 < n:
        k <<= 1
    return k


def root(leaves: Sequence[bytes]) -> bytes:
    """Merkle Tree Hash of the given leaf hashes."""
    n = len(leaves)
    if n == 0:
        return EMPTY_ROOT
    if n == 1:
        return leaves[0]
    k = _split(n)
    return node_hash(root(leaves[:k]), root(leaves[k:]))


def inclusion_proof(leaves: Sequence[bytes], index: int) -> List[bytes]:
    """Audit path for leaf `index` in the tree over `leaves` (RFC 6962, 2.1.1)."""
    n = len(leaves)
    if not 0 <= index < n:
        raise IndexError(f"leaf {index} is not in a tree of size {n}")
    if n == 1:
        return []
    k = _split(n)
    if index < k:
        return inclusion_proof(leaves[:k], index) + [root(leaves[k:])]
    return inclusion_proof(leaves[k:], index - k) + [root(leaves[:k])]


def verify_inclusion(leaf: bytes, index: int, size: int, proof: Sequence[bytes], expected_root: bytes) -> bool:
    """RFC 9162, 2.1.3.2."""
    if not 0 <= index < size:
        return False
    fn, sn = index, size - 1
    r = leaf
    for p in proof:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            r = node_hash(p, r)
            if not fn & 1:
                while fn and not fn & 1:
                    fn >>= 1
                    sn >>= 1
        else:
            r = node_hash(r, p)
        fn >>= 1
        sn >>= 1
    return sn == 0 and r == expected_root


def _subproof(m: int, leaves: Sequence[bytes], complete: bool) -> List[bytes]:
    n = len(leaves)
    if m == n:
        return [] if complete else [root(leaves)]
    k = _split(n)
    if m <= k:
        return _subproof(m, leaves[:k], complete) + [root(leaves[k:])]
    return _subproof(m - k, leaves[k:], False) + [root(leaves[:k])]


def consistency_proof(leaves: Sequence[bytes], old_size: int) -> List[bytes]:
    """Proof that the first `old_size` leaves are a prefix of `leaves` (RFC 6962, 2.1.2)."""
    n = len(leaves)
    if not 0 < old_size <= n:
        raise ValueError(f"no consistency proof from size {old_size} to size {n}")
    if old_size == n:
        return []
    return _subproof(old_size, leaves, True)


def verify_consistency(old_size: int, new_size: int, old_root: bytes, new_root: bytes, proof: Sequence[bytes]) -> bool:
    """RFC 9162, 2.1.4.2."""
    if old_size == new_size:
        return not proof and old_root == new_root
    if not 0 < old_size < new_size or not proof:
        return False
    proof = list(proof)
    if old_size & (old_size - 1) == 0:  # a power of two: the old root is the first node
        proof = [old_root] + proof
    fn, sn = old_size - 1, new_size - 1
    while fn & 1:
        fn >>= 1
        sn >>= 1
    fr = sr = proof[0]
    for c in proof[1:]:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            fr = node_hash(c, fr)
            sr = node_hash(c, sr)
            if not fn & 1:
                while fn and not fn & 1:
                    fn >>= 1
                    sn >>= 1
        else:
            sr = node_hash(sr, c)
        fn >>= 1
        sn >>= 1
    return sn == 0 and fr == old_root and sr == new_root
