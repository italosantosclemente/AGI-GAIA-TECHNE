"""Software Carbon Intensity (Green Software Foundation; ISO/IEC 21031:2024).

    SCI = (E x I + M) per R

E is the energy the runs drew (kWh), I the carbon intensity of that energy
(gCO2e/kWh), M the embodied emissions allotted to them (gCO2e) and R the
functional unit, here one claim. The kernel computes the score only from
what was declared in the ground of each run, and only when every term was
measured: a missing term is named, and the score is reported as "unmetered",
never estimated (K9). Who maintains the energy and the machines is part of the
declaration; the number does not replace it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..koinos.ground import GroundFootprint, GroundKind


@dataclass(frozen=True)
class SCI:
    energy_kwh: Optional[float]
    intensity_g_per_kwh: Optional[float]
    embodied_g: Optional[float]
    functional_units: int
    missing: List[str]

    @property
    def score(self) -> Optional[float]:
        if self.missing or not self.functional_units:
            return None
        return (self.energy_kwh * self.intensity_g_per_kwh + self.embodied_g) / self.functional_units

    def describe(self) -> str:
        if self.score is None:
            return "SCI: unmetered (" + "; ".join(self.missing or ["no claims"]) + ")"
        return f"SCI: {self.score:.3f} gCO2e per claim over {self.functional_units} claim(s)"


def _sum(footprint: GroundFootprint, kind: GroundKind, unit: str) -> Optional[float]:
    vals = [d.quantity for d in footprint.dependencies if d.kind is kind and d.unit == unit and d.quantity is not None]
    return sum(vals) if vals else None


def sci(footprint: GroundFootprint, claims: int, intensity_g_per_kwh: Optional[float] = None) -> SCI:
    energy = _sum(footprint, GroundKind.ENERGY, "kWh")
    embodied = _sum(footprint, GroundKind.MATERIAL, "gCO2e")
    missing = []
    if energy is None:
        missing.append("no energy declared in kWh")
    if intensity_g_per_kwh is None:
        missing.append("no carbon intensity of the energy given")
    if embodied is None:
        missing.append("no embodied emissions declared in gCO2e")
    return SCI(energy, intensity_g_per_kwh, embodied, claims, missing)
