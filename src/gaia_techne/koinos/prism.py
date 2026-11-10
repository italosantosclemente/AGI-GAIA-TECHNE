"""The prism: symbolic functions as directions, never as ranks.

Chapter II/III. Cassirer distinguishes expression, presentation and
signification within the one function of representation. The project orders
them by direction (away from the immediacy of life, or back toward intuition),
as a prism refracts one beam with different indices and the shift of the
spectrum marks the movement, as in the Doppler effect. There is deliberately
no ordering operator: forms cannot be ranked, and neither can peoples.

Sources. The unity of the natural world-image is crossed by the three
functions "like a uniform and simple beam of light" not yet refracted by
different media of sense (ECN 1:5-8). The process keeps a constant direction,
in which the confrontation (Auseinandersetzung) between I and world becomes
clearer and anthropomorphic components are suppressed (ECW 13:487-490); but
the direction does not assign each symbolic form to one function, since myth
already contains all three, with its accent on expression (ECN 1:234). Physics
cannot "jump over its own shadow": it never dispenses with the medium of
representation (ECW 13:555-556), which is why the descent is required.
The two limits of the direction, a pure identity of presence and
representation and their absolute separation, are never reached (ECN 1:230);
between them lies the domain of culture.
"""

from __future__ import annotations

from enum import Enum


class RankingRefused(TypeError):
    """Raised when code tries to rank symbolic functions or forms."""


class _Unranked(Enum):
    def _refuse(self, other):  # noqa: D401
        raise RankingRefused(
            "Symbolic functions are ordered by direction, not ranked: prism, not ladder."
        )

    __lt__ = __le__ = __gt__ = __ge__ = _refuse


class SymbolicFunction(_Unranked):
    EXPRESSION = "Ausdruck"
    PRESENTATION = "Darstellung"
    SIGNIFICATION = "Bedeutung"

    @property
    def horizon(self) -> str:
        """The idea of reason that is this function's regulative horizon."""
        return {
            SymbolicFunction.EXPRESSION: "soul: the unity of the lived",
            SymbolicFunction.PRESENTATION: "world: a totality never given as a whole",
            SymbolicFunction.SIGNIFICATION: "God: the focus imaginarius of systematic unity",
        }[self]


class Direction(_Unranked):
    AWAY_FROM_LIFE = "ascent: from perception toward signification"
    TOWARD_INTUITION = "descent: from signification back to a perception that tests it"
