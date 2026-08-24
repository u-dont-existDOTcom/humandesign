"""Deterministic Human Design chart calculation primitives.

The package deliberately separates astronomical calculation from symbolic
interpretation.  Advanced Color/Tone/Base values are not emitted because the
repository has not frozen independently validated rules for those layers.
"""

from .bodygraph import Authority, Bodygraph, Center, Definition, HDType, Strategy
from .boundaries import canonical_boundary_event_string
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
from .feature_registry import (
    CACHEABLE_M0_M2_REGISTRY,
    AdvancedField,
    AdvancedSubstructure,
    CacheableChartStateV2,
    CapabilityStatus,
    ChannelCircuitry,
    ChartFeatureVectorV2,
    CircuitryFeatures,
    FeatureCoverage,
    FeatureCoverageError,
    FeatureId,
    FeatureTier,
    RequiredFeatureRegistry,
    assess_required_feature_coverage,
    cacheable_serialization_session,
    compile_required_feature_registry,
    require_complete_feature_coverage,
    serialize_cacheable_chart_state,
    serialize_chart_feature_vector,
)
from .rave_mandala import RAVE_MANDALA_VERSION, MandalaPosition, longitude_to_gate_line
from .timezone import LocalTimeResolution, LocalTimeStatus, resolve_local_datetime

__all__ = [
    "Authority",
    "Bodygraph",
    "CACHEABLE_M0_M2_REGISTRY",
    "CelestialBody",
    "Center",
    "AdvancedField",
    "AdvancedSubstructure",
    "CacheableChartStateV2",
    "CapabilityStatus",
    "ChannelCircuitry",
    "ChartComputation",
    "ChartFeatureVectorV2",
    "CircuitryFeatures",
    "Definition",
    "DesignMomentResult",
    "EphemerisProvider",
    "EphemerisMode",
    "FeatureCoverage",
    "FeatureCoverageError",
    "FeatureId",
    "FeatureTier",
    "HDType",
    "LocalTimeResolution",
    "LocalTimeStatus",
    "MandalaPosition",
    "ProductionEngineValidation",
    "RAVE_MANDALA_VERSION",
    "RequiredFeatureRegistry",
    "Strategy",
    "SwissEphemerisProvider",
    "assess_required_feature_coverage",
    "cacheable_serialization_session",
    "canonical_boundary_event_string",
    "calculate_chart",
    "compile_required_feature_registry",
    "longitude_to_gate_line",
    "require_complete_feature_coverage",
    "resolve_local_datetime",
    "serialize_cacheable_chart_state",
    "serialize_chart_feature_vector",
    "solve_design_moment",
    "solve_personality_moment_from_design",
    "validate_production_engine",
]
