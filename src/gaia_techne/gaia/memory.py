"""Planetary memory: the common world as a source.

Earlier claims re-enter later runs as premises, but only as what the record says
they are: a judgment of perception still holds only for its source, a claim
upheld by others holds before those it was tested by, and a refuted or revised
claim does not re-enter at all. The memory is a reading of the public record,
rebuilt by replay, so that nothing is remembered that the record does not
contain and nothing is remembered as more than the record allows.

Relevance is measured by shared words. That is deliberately modest: memory
proposes premises, it never decides what they are worth.
"""

from __future__ import annotations

import re
from typing import List

from ..ethos.premises import Premise
from ..koinos.common_world import CommonWorld
from ..metatheory.replay import replay

_WORD = re.compile(r"[\wÀ-ÿ]{4,}")


def _words(text: str) -> set:
    return {w.lower() for w in _WORD.findall(text)}


def recall(world: CommonWorld, query: str, k: int = 3) -> List[Premise]:
    """Earlier claims relevant to `query`, as premises whose source names their entry, stage and reach."""
    wanted = _words(query)
    if not wanted:
        return []
    scored = []
    for c in replay(world).claims:
        if c.refuted or c.revised_by:
            continue
        overlap = len(wanted & _words(c.content))
        if overlap:
            scored.append((overlap, c.exposed_at or 0, c))
    scored.sort(key=lambda t: (-t[0], -t[1]))
    return [
        Premise(c.content, f"common world entry {c.exposed_at}: {c.claim_id}, {c.stage.value}, reach {c.reach.name}")
        for _, _, c in scored[:k]
    ]
