"""The boundaries every layer respects.

The Prolegomena distinguish limits (Schranken), mere negations that progress
keeps pushing back, from boundaries (Grenzen), which presuppose a space outside
and contain something positive (AA 4:350-358). More compute, data and speed push
back limits; none of them crosses a boundary. This module holds the boundaries
that more than one layer has to check, so that no layer depends on a later one
in order to respect them:

- the ground is not a subject: the planet, the network and the archive cannot
  state ends, raise claims or correct them;
- the system is not one of those who set ends, acknowledge them or certify
  claims: names that denote the system itself are recognized wherever a
  person is required.

What a run may draw from the ground is a limit, not a boundary, and lives in
`koinos.ground` (`LimitReached`): people can widen an allowance by a recorded
decision, but no allowance moves a boundary.

The application of the Prolegomena's distinction to a machine is this
project's, not Kant's.
"""

from __future__ import annotations

from typing import Iterable

GROUND_NAMES = frozenset(
    {"gaia", "earth", "planet", "ground", "terra", "internet", "network", "data centre", "datacenter"}
)

MACHINE_AUTHORS = frozenset({"runtime", "gaia-techne", "model", "system"})


class GroundIsNotSubject(ValueError):
    """Raised when the ground is treated as an author of ends, claims or corrections."""


def _norm(name: str) -> str:
    return name.strip().lower()


def refuse_ground_as_subject(author: str) -> None:
    if _norm(author) in GROUND_NAMES:
        raise GroundIsNotSubject(
            f"{author!r} is the ground of the common world, not a subject within it: "
            "it cannot state ends, raise claims or correct them."
        )


def is_machine(author: str, extra: Iterable[str] = ()) -> bool:
    """True when `author` names the system itself (a default name or one the runtime declared)."""
    name = _norm(author)
    return name in MACHINE_AUTHORS or name in {_norm(e) for e in extra}


def require_author(author: str) -> None:
    """Every act in the record has someone who answers for it."""
    if not author or not author.strip():
        raise ValueError("every act needs an author who can answer for it")
