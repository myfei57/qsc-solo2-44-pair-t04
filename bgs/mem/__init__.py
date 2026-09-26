"""Gas valve, pressure ramp and methane analysis."""

from __future__ import annotations

from .analyzer import QUALITY_KIND, AnalyzerSnapshot, evaluate_methane, rebuild_window
from .ramp import BASELINE_NAME, RAMP_BAND_KPA, RampGate, check_ramp
from .service import MemService
from .status import compose_status
from .valve import ValveState, valve_payload

__all__ = [
    "BASELINE_NAME",
    "QUALITY_KIND",
    "AnalyzerSnapshot",
    "MemService",
    "RAMP_BAND_KPA",
    "RampGate",
    "ValveState",
    "check_ramp",
    "compose_status",
    "evaluate_methane",
    "rebuild_window",
    "valve_payload",
]
