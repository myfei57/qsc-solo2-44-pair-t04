"""Pressure ramp gate.

A ramp target has to satisfy two independent bounds:

* the calibrated design value of the generation currently in force, inside a
  narrow tolerance band, and
* the hard pressure bound the equipment is rated for.

Passing the equipment bound is not enough when the reading no longer matches
the calibration in force.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..decision.thresholds import ThresholdSet
from ..errors import OverLimitError
from ..versioning.baseline import Baseline
from ..versioning.facade import VersionedArtifacts

BASELINE_NAME = "membrane_pressure"
RAMP_BAND_KPA = 2.0


@dataclass(frozen=True, slots=True)
class RampGate:
    """The calibration a ramp was checked against."""

    pressure_kpa: float
    baseline: float
    band_kpa: float
    generation: int

    def describe(self) -> dict[str, Any]:
        return {
            "pressure_kpa": self.pressure_kpa,
            "baseline_value": self.baseline,
            "baseline_generation": self.generation,
            "band_kpa": self.band_kpa,
            "unit": "kPa",
        }


def check_ramp(
    versions: VersionedArtifacts,
    thresholds: ThresholdSet,
    pressure_kpa: float,
    *,
    baseline_generation: int,
    now: int,
    band_kpa: float = RAMP_BAND_KPA,
) -> RampGate:
    """Check a ramp target against the calibration band and the hard bound."""

    baseline: Baseline = versions.require_baseline(
        BASELINE_NAME, generation=baseline_generation, now=now
    )
    deviation = abs(pressure_kpa - baseline.value)
    if deviation > band_kpa:
        raise OverLimitError(
            "pressure ramp target sits outside the calibrated band",
            pressure_kpa=pressure_kpa,
            baseline=baseline.value,
            band=band_kpa,
            baseline_generation=baseline.generation,
        )
    thresholds.require("membrane_pressure", pressure_kpa)
    return RampGate(
        pressure_kpa=pressure_kpa,
        baseline=baseline.value,
        band_kpa=band_kpa,
        generation=baseline.generation,
    )
