"""Deterministic Human Design chart calculation primitives.

The package deliberately separates astronomical calculation from symbolic
interpretation.  Advanced Color/Tone/Base values are not emitted because the
repository has not frozen independently validated rules for those layers.
"""

from .bodygraph import Authority, Bodygraph, Center, Definition, HDType, Strategy
from .calculator import ChartComputation, calculate_chart
from .design_moment import (
    DesignMomentResult,
    solve_design_moment,
    solve_personality_moment_from_design,
)
from .engine_probe import ProductionEngineValidation, validate_production_engine
from .ephemeris import (
    CelestialBody,
    EphemerisMode,
    EphemerisProvider,
    SwissEphemerisProvider,
)
from .rave_mandala import MandalaPosition, longitude_to_gate_line
from .timezone import LocalTimeResolution, LocalTimeStatus, resolve_local_datetime

__all__ = [
    "Authority",
    "Bodygraph",
    "CelestialBody",
    "Center",
    "ChartComputation",
    "Definition",
    "DesignMomentResult",
    "EphemerisProvider",
    "EphemerisMode",
    "HDType",
    "LocalTimeResolution",
    "LocalTimeStatus",
    "MandalaPosition",
    "ProductionEngineValidation",
    "Strategy",
    "SwissEphemerisProvider",
    "calculate_chart",
    "longitude_to_gate_line",
    "resolve_local_datetime",
    "solve_design_moment",
    "solve_personality_moment_from_design",
    "validate_production_engine",
]
