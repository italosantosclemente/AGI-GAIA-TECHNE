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

Two guards follow from Cassirer's map of metaphysics, in which every
metaphysics singles out one "moment" of experience and declares it the being
in itself (ECN 1:150-152):

- immediacy guard (horizon of expression): presence claimed without
  representation. There is no naked sensation, no materia nuda, to which a
  form would be added (ECW 13:16-17); the paradise of pure immediacy is closed
  (ECW 11:48-49);
- bearer guard (horizon of presentation, at the level of history): works
  explained through a super-empirical bearer, such as the spirit of a people
  or the world spirit (ECN 1:152-158). A work arises from reciprocal action
  and is a social phenomenon (ECN 1:136-137, 155-156). Before the world spirit, the
  finite individual becomes a mere marionette (ECW 22:149-152).

Two further guards follow from the practical chapter:

- technique guard: the technical norm posited as absolute and imposed on the
  other spheres (ECW 17:173); rules of skill hold only under ends they do not
  set, and the culture of skill prepares the culture of discipline without
  becoming it (AA 5:431-432);
- humanity guard: speaking in the name of humanity, or stratifying its title.
  The humanity in the person is holy (AA 5:87); its title is neither granted
  nor produced, but acknowledged in the form of "any of us", and it cannot be
  stratified, since the law holds for every rational will or for none.

The technique guard also flags technology posited as a new creed: the modern
politician acts "as both a homo magus and a homo faber" (ECW 25:277), and the
programs of convergence expect "a dynamic new creed to replace religion"
(Weiss, 2012, p. 240). The ideal guard flags the demand "that we become gods"
(Negarestani, 2018, p. 506): the holiness of the will is an archetype that no
finite will occupies (AA 5:122, 5:127n).

The guards also keep the AGI hypothesis defensive: hypotheses are allowed in
pure reason only "as weapons of war", to defend, never to ground a right
(KrV A:777/B:805).

Keyword matching is a deliberately modest first detector. It flags; it never
decides. Every flag returns to human judgment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple

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
    r"\b(?:we |it |they |humans |machines )?(?:will |shall |must )?become (?:a )?gods?\b",
]

_IMMEDIACY = [
    r"\bthe data speak(?:s)? for (?:themselves|itself)\b",
    r"\bunmediated (?:access to )?(?:reality|the world|experience)\b",
    r"\b(?:pure|brute|naked) (?:facts?|reality|givens?) (?:without|free of|prior to) (?:any )?(?:interpretation|theory|form)\b",
    r"\bwithout any (?:interpretation|model|symbols?|representation) at all\b",
]
_BEARER = [
    r"\b(?:the )?(?:world[- ]spirit|weltgeist|zeitgeist) (?:decides|wills|wants|speaks|produces|writes)\b",
    r"\bthe (?:spirit|soul|mind) of (?:the|a|this) (?:people|nation|race|civili[sz]ation)\b",
    r"\b(?:the )?(?:collective|global|planetary|hive) (?:mind|consciousness|brain) (?:of (?:the )?(?:internet|network|planet|archive) )?(?:decides|wills|wants|knows|wrote|produces)\b",
    r"\bthe (?:archive|corpus|internet) (?:itself )?(?:knows|wants|wills|decides)\b",
]

_TECHNIQUE = [
    r"\b(?:the )?most efficient (?:option |solution )?is (?:the )?(?:right|good|just|best for everyone)\b",
    r"\boptimi[sz]ation (?:decides|determines|settles) (?:what|which|the) (?:ought|ends?|goals?|values?)\b",
    r"\bwhat can be (?:done|made|built) (?:should|must) be (?:done|made|built)\b",
    r"\befficiency (?:is|as) the (?:only|highest|final) (?:value|end|measure)\b",
    r"\b(?:technology|ai|agi|science|the machine) (?:is|as|will be) (?:a|the|our) new (?:religion|creed|god|faith)\b",
    r"\b(?:a )?(?:new )?creed to replace religion\b",
]
_HUMANITY = [
    r"\bin the name of (?:all )?humanity\b",
    r"\bhumanity (?:wants|demands|has decided|needs|requires)\b",
    r"\b(?:more|less) human than\b",
    r"\b(?:superior|inferior|primitive|advanced) (?:races?|peoples?)\b",
]


@dataclass(frozen=True)
class Guard:
    """One guard: the idea whose horizon it keeps, the error it names, the patterns that flag it."""

    name: str
    idea: str
    error: str
    patterns: Tuple[str, ...]


GUARDS: Tuple[Guard, ...] = (
    Guard("soul", "soul", "paralogism: inner life ascribed to the system", tuple(_SOUL)),
    Guard("world", "world", "antinomy: the world taken as a given whole", tuple(_WORLD)),
    Guard("ideal", "God", "ideal: a standpoint no one occupies taken as available", tuple(_IDEAL)),
    Guard("immediacy", "soul", "presence claimed without representation: no materia nuda", tuple(_IMMEDIACY)),
    Guard("bearer", "world", "works ascribed to a super-empirical bearer: a work arises from reciprocal action", tuple(_BEARER)),
    Guard("technique", "-", "technical norm posited as absolute: rules of skill do not set ends", tuple(_TECHNIQUE)),
    Guard("humanity", "-", "the title of humanity is acknowledged by any of us, not spoken for or stratified", tuple(_HUMANITY)),
)


@dataclass(frozen=True)
class Flag:
    guard: str
    idea: str
    error: str
    match: str


def _scan(text: str, patterns: Iterable[str]) -> List[str]:
    hits = []
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            hits.append(m.group(0))
    return hits


def check(claim: Claim) -> List[Flag]:
    flags: List[Flag] = []
    for g in GUARDS:
        for m in _scan(claim.content, g.patterns):
            flags.append(Flag(g.name, g.idea, g.error, m))
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
