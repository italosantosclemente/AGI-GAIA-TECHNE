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
  corrections (the boundary is checked in `gaia_techne.boundaries`). To treat
  it as one would be hylozoism, or the paralogism that takes the unity of a
  function for the unity of a substance;
- the ground is finite, as the resources of a planet are finite. People set
  allowances under acknowledged ends, and a run that would exceed one does not
  start. An allowance is a limit (Schranke), which people can widen by a
  recorded decision; it is not a boundary (Grenze), which no allowance moves
  (AA 4:350-358). Reading the finitude of the geomorphic conditions as a
  finitude of resources is this project's, not Kant's or Husserl's.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional

from ..boundaries import GROUND_NAMES, GroundIsNotSubject, refuse_ground_as_subject

__all__ = [
    "GROUND_NAMES",
    "Allowance",
    "GroundBudget",
    "GroundDependency",
    "GroundFootprint",
    "GroundIsNotSubject",
    "GroundKind",
    "LimitReached",
    "kinds_declared",
    "refuse_ground_as_subject",
]


class GroundKind(Enum):
    COMPUTE = "data centres and processors"
    ENERGY = "energy supply"
    NETWORK = "networks"
    MATERIAL = "minerals, water, land"
    ARCHIVE = "archive of human expression (training data, documents)"


@dataclass(frozen=True)
class GroundDependency:
    kind: GroundKind
    description: str
    location: str
    maintained_by: str  # people who produce, maintain and repair it
    quantity: float = 0.0
    unit: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.kind, GroundKind):
            raise TypeError("the kind of ground must be a GroundKind")
        if self.quantity < 0:
            raise ValueError("a run draws on the ground; it cannot declare a negative quantity")

    @property
    def key(self) -> str:
        return f"{self.kind.name}:{self.unit}" if self.unit else self.kind.name

    @property
    def metered(self) -> bool:
        return bool(self.unit) and self.quantity > 0

    def describe(self) -> str:
        who = self.maintained_by or "unknown"
        amount = f", {self.quantity:g} {self.unit}" if self.unit else ""
        return f"{self.kind.name}: {self.description} @ {self.location} (maintained by {who}{amount})"


@dataclass
class GroundFootprint:
    """What the runs of the system borrowed from people and planet."""

    dependencies: List[GroundDependency] = field(default_factory=list)

    def add(self, dep: GroundDependency) -> None:
        self.dependencies.append(dep)

    @property
    def unmaintained(self) -> List[GroundDependency]:
        return [d for d in self.dependencies if not d.maintained_by.strip()]

    @property
    def maintainers(self) -> List[str]:
        return sorted({d.maintained_by for d in self.dependencies if d.maintained_by.strip()})

    def totals(self) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for d in self.dependencies:
            out[d.key] = out.get(d.key, 0.0) + d.quantity
        return out


class LimitReached(RuntimeError):
    """A run would exceed an allowance of the ground.

    A limit, not a boundary: the people who set the allowance can widen it by a
    recorded decision. The runtime cannot.
    """


@dataclass(frozen=True)
class Allowance:
    """How much of one kind of ground the runs under an end may draw, set by a person."""

    kind: GroundKind
    unit: str
    limit: float
    set_by: str
    end_id: str
    reason: str = ""

    def __post_init__(self) -> None:
        if not self.unit:
            raise ValueError("an allowance needs a unit in which the ground is measured")
        if self.limit < 0:
            raise ValueError("an allowance cannot be negative")

    @property
    def key(self) -> str:
        return f"{self.kind.name}:{self.unit}"


class GroundBudget:
    """The finite allowances of the ground. Setting them is the business of people."""

    def __init__(self) -> None:
        self._current: Dict[str, Allowance] = {}
        self.history: List[Allowance] = []

    def set(self, allowance: Allowance) -> None:
        self._current[allowance.key] = allowance
        self.history.append(allowance)

    def allowance(self, kind: GroundKind, unit: str) -> Optional[Allowance]:
        return self._current.get(f"{kind.name}:{unit}")

    def allowances(self) -> List[Allowance]:
        return list(self._current.values())

    def check(self, footprint: GroundFootprint, deps: Iterable[GroundDependency]) -> List[str]:
        """Refuse a run that would exceed an allowance; flag what cannot be checked.

        Raises `LimitReached` before anything is drawn. Returns flags for
        dependencies of a kind that is under an allowance but declare no
        quantity in its unit: they cannot be measured against it.
        """
        deps = list(deps)
        totals = footprint.totals()
        flags: List[str] = []
        planned: Dict[str, float] = {}
        for d in deps:
            limited = [a for a in self._current.values() if a.kind is d.kind]
            if not limited:
                continue
            if d.key in self._current and d.quantity > 0:
                planned[d.key] = planned.get(d.key, 0.0) + d.quantity
            else:
                units = ", ".join(sorted(a.unit for a in limited))
                flags.append(
                    f"unmetered: {d.kind.name} is under an allowance in {units}, "
                    "but this run declares no quantity in that unit"
                )
        for key, amount in planned.items():
            a = self._current[key]
            after = totals.get(key, 0.0) + amount
            if after > a.limit:
                raise LimitReached(
                    f"{key}: this run would bring the total to {after:g} {a.unit}, above the allowance of "
                    f"{a.limit:g} set by {a.set_by} under {a.end_id!r}; people can widen it by a recorded "
                    "decision, the runtime cannot"
                )
        return flags

    def remaining(self, footprint: GroundFootprint) -> Dict[str, float]:
        totals = footprint.totals()
        return {k: round(a.limit - totals.get(k, 0.0), 6) for k, a in self._current.items()}


def kinds_declared(deps: Iterable[GroundDependency]) -> List[GroundKind]:
    return sorted({d.kind for d in deps}, key=lambda k: k.name)
