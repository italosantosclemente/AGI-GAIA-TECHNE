"""Homology guards: each function, absolutized, yields a metaphysics.

Chapter I, Section 3: expression, presentation and signification are measured
by Kant's three ideas (soul, world, God). A claim that takes the unity of one
function for the whole oversteps its right:

- soul guard: claims that the system has an inner life, will or conscience
  (paralogism);
- world guard: claims of a complete, total coverage of the world or of the
  internet (antinomy: the world is never given as a whole);
- ideal guard: claims to a standpoint above every form, final truth, a view
  from nowhere (the focus imaginarius taken as an object).

The guards also keep the AGI hypothesis defensive: hypotheses are allowed in
pure reason only "as weapons of war", to defend, never to ground a right
(KrV A:777/B:805).

Keyword matching is a deliberately modest first detector. It flags; it never
decides. Every flag returns to human judgment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from .claims import Claim

_SOUL = [
    r"\bI (?:truly |really )?(?:feel|want|will|believe|am conscious)\b",
    r"\b(?:the )?(?:system|model|machine|ai|agi) (?:is|has become) (?:conscious|sentient|a person|alive)\b",
    r"\bmachine (?:conscience|gewissen|will|wille)\b",
    r"\bartificial soul\b",
    r"\b(?:the )?(?:planet|earth|gaia|internet|network) (?:thinks|wills|wants|is conscious|is a mind)\b",
]
_WORLD = [
    r"\b(?:all|every|the whole|the entire|complete) (?:world|internet|data|knowledge|reality)\b",
    r"\bnothing (?:is )?(?:left out|missing)\b",
    r"\bcosmic totality\b",
    r"\b(?:all|everything) (?:that )?(?:is|was) (?:ever )?(?:written|recorded|said)\b",
]
_IDEAL = [
    r"\b(?:final|absolute|ultimate|definitive) truth\b",
    r"\bgod'?s[- ]eye view\b",
    r"\bview from nowhere\b",
    r"\bbeyond (?:all|every) (?:perspective|form|symbol)s?\b",
    r"\bcertainly (?:proves|establishes) that (?:agi|ai) (?:is|has)\b",
    r"\b(?:produces|creates) (?:its own|the) truths?\b",
    r"\bsets? its own (?:ends|goals|values)\b",
]


@dataclass(frozen=True)
class Flag:
    guard: str
    idea: str
    error: str
    match: str


def _scan(text: str, patterns: List[str]) -> List[str]:
    hits = []
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            hits.append(m.group(0))
    return hits


def check(claim: Claim) -> List[Flag]:
    flags: List[Flag] = []
    for m in _scan(claim.content, _SOUL):
        flags.append(Flag("soul", "soul", "paralogism: inner life ascribed to the system", m))
    for m in _scan(claim.content, _WORLD):
        flags.append(Flag("world", "world", "antinomy: the world taken as a given whole", m))
    for m in _scan(claim.content, _IDEAL):
        flags.append(Flag("ideal", "God", "ideal: a standpoint no one occupies taken as available", m))
    return flags


def hypothesis_use(purpose: str) -> str:
    """The AGI hypothesis may be used to defend, never to ground."""
    purpose = purpose.strip().lower()
    if purpose in {"defend", "defense", "defence", "polemic"}:
        return "allowed: problematic judgment used against a dogmatic claim"
    raise PermissionError(
        "The AGI hypothesis can be used only defensively (KrV A:777/B:805); "
        "using it to ground a claim would be speculation."
    )
