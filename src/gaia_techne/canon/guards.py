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

Each idea keeps a regulative horizon once its constitutive use is denied:
the unity of consciousness "is only the unity of thinking, through which no
object is given" (KrV B:421-422); the regress in the series of conditions is
"given to us as a problem" (KrV A:497-498/B:526); and the systematic unity of
cognition is a focus imaginarius outside the bounds of possible experience
(KrV A:644/B:672). Cassirer traces the three dialectical inferences to one
source: a relation valid within experience turned into a self-subsistent
entity preceding all experience (ECW 8:191-193).

The illusion is "a natural and unavoidable dialectic of pure reason" (KrV
A:298/B:354) and does not cease once uncovered (KrV A:297-298/B:353-354).
Hence the guards run on every admitted claim, and no correction clears their
flags. Speaking of the system is allowed only as symbolic anthropomorphism,
which attributes properties to a relation to the world, not to a being in
itself (AA 4:357); the soul guard flags the second kind of sentence. The
application of these passages to a machine is this project's, not Kant's.

Two further guards follow from the practical chapter:

- technique guard: the technical norm posited as absolute and imposed on the
  other spheres (ECW 17:173); rules of skill hold only under ends they do not
  set, and the culture of skill prepares the culture of discipline without
  becoming it (AA 5:431-432);
- humanity guard: speaking in the name of humanity, or stratifying its title.
  The humanity in the person is holy (AA 5:87); its title is neither granted
  nor produced, but acknowledged in the form of "any of us", and it cannot be
  stratified, since the law holds for every rational will or for none.

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


_TECHNIQUE = [
    r"\b(?:the )?most efficient (?:option |solution )?is (?:the )?(?:right|good|just|best for everyone)\b",
    r"\boptimi[sz]ation (?:decides|determines|settles) (?:what|which|the) (?:ought|ends?|goals?|values?)\b",
    r"\bwhat can be (?:done|made|built) (?:should|must) be (?:done|made|built)\b",
    r"\befficiency (?:is|as) the (?:only|highest|final) (?:value|end|measure)\b",
]
_HUMANITY = [
    r"\bin the name of (?:all )?humanity\b",
    r"\bhumanity (?:wants|demands|has decided|needs|requires)\b",
    r"\b(?:more|less) human than\b",
    r"\b(?:superior|inferior|primitive|advanced) (?:races?|peoples?)\b",
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
    for m in _scan(claim.content, _TECHNIQUE):
        flags.append(Flag("technique", "-", "technical norm posited as absolute: rules of skill do not set ends", m))
    for m in _scan(claim.content, _HUMANITY):
        flags.append(Flag("humanity", "-", "the title of humanity is acknowledged by any of us, not spoken for or stratified", m))
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
