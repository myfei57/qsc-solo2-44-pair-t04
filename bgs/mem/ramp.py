"""Pressure ramp planning against the calibration band and the hard bound."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..errors import OverLimitError, ValidationError
from ..versioning.baseline import Baseline


@dataclass(frozen=True, slots=True)
class RampPlan:
    """The pressure a ramp settles on, pinned to one calibration baseline."""

    pressure_kpa: float
    baseline: float
    band_kpa: float
    generation: int

    def describe(self) -> dict[str, Any]:
        return {
            "pressure_kpa": self.pressure_kpa,
            "baseline_value": self.baseline,
            "band_kpa": self.band_kpa,
            "baseline_generation": self.generation,
        }


def plan_ramp(pressure_kpa: float, baseline: Baseline, *, band_kpa: float) -> RampPlan:
    """Validate a ramp target against the calibrated design value."""

    if band_kpa <= 0:
        raise ValidationError("ramp band must be positive", band=band_kpa)
    if abs(pressure_kpa - baseline.value) > band_kpa:
        raise OverLimitError(
            "pressure ramp is outside the calibrated band",
            pressure_kpa=pressure_kpa,
            baseline=baseline.value,
            band=band_kpa,
        )
    return RampPlan(
        pressure_kpa=pressure_kpa,
        baseline=baseline.value,
        band_kpa=band_kpa,
        generation=baseline.generation,
    )
