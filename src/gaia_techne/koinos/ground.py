"""The ground: geomorphic conditions of possibility.

Chapter II, Section 5. The machine expected to become a general intelligence
stays on the side of the watch: it has motive power, not formative power
(AA 5:374). Its conditions of possibility are not those of a body among
bodies but those of a planet: the material and energetic layer of data
centres, networks and resources, together with an archive of human
expression that no single consciousness has lived through. Husserl describes
the Earth as the ground (Boden) on which every experience of bodies rests,
a whole that is not itself a body (Husserl, 2024, pp. 182, 185, 187). These
conditions are called geomorphic rather than anthropomorphic.

Tools such as a lever are machines, not works of art: they can be used for
ends but are not possible solely in relation to them (AA 20:219). A causality
according to ends, made constitutive, would be one "which, however, we merely
borrow from ourselves and ascribe to other beings" (AA 5:361).

Engineering consequences:

- every run declares the ground it depends on (compute, energy, network,
  material, archive) and who produces, maintains and repairs it, because the
  formative power the system seems to have is borrowed from the people and the
  planet it depends on;
- the ground is never a "subject": it cannot author ends, claims or
  corrections. To treat it as one would be hylozoism, or the paralogism that
  takes the unity of a function for the unity of a substance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List


class GroundKind(Enum):
    COMPUTE = "data centres and processors"
    ENERGY = "energy supply"
    NETWORK = "networks"
    MATERIAL = "minerals, water, land"
    ARCHIVE = "archive of human expression (training data, documents)"


GROUND_NAMES = {"gaia", "earth", "planet", "ground", "terra", "internet", "network", "data centre", "datacenter"}


class GroundIsNotSubject(ValueError):
    """Raised when the ground is treated as an author of ends, claims or corrections."""


def refuse_ground_as_subject(author: str) -> None:
    if author.strip().lower() in GROUND_NAMES:
        raise GroundIsNotSubject(
            f"{author!r} is the ground of the common world, not a subject within it: "
            "it cannot state ends, raise claims or correct them."
        )


@dataclass(frozen=True)
class GroundDependency:
    kind: GroundKind
    description: str
    location: str
    maintained_by: str  # people who produce, maintain and repair it
    quantity: float = 0.0
    unit: str = ""


@dataclass
class GroundFootprint:
    """What one run of the system borrowed from people and planet."""

    dependencies: List[GroundDependency] = field(default_factory=list)

    def add(self, dep: GroundDependency) -> None:
        self.dependencies.append(dep)

    @property
    def unmaintained(self) -> List[GroundDependency]:
        return [d for d in self.dependencies if not d.maintained_by.strip()]

    def totals(self) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for d in self.dependencies:
            key = f"{d.kind.name}:{d.unit}" if d.unit else d.kind.name
            out[key] = out.get(key, 0.0) + d.quantity
        return out


def kinds_declared(deps: Iterable[GroundDependency]) -> List[GroundKind]:
    return sorted({d.kind for d in deps}, key=lambda k: k.name)
