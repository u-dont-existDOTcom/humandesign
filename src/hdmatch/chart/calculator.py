"""End-to-end deterministic chart calculation from an ephemeris provider."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final

from .bodygraph import (
    ActivationSide,
    Bodygraph,
    GateActivation,
    bodygraph_constants_sha256,
    derive_bodygraph,
)
from .design_moment import DesignMomentResult, solve_design_moment
from .ephemeris import (
    DEFAULT_ACTIVATION_BODIES,
    CelestialBody,
    EphemerisMetadata,
    EphemerisProvider,
)
from .rave_mandala import longitude_to_gate_line, mandala_constants_sha256
from .validation import canonical_sha256

CHART_ENGINE_VERSION: Final[str] = "chart-engine-v1"


@dataclass(frozen=True, slots=True)
class ChartEngineMetadata:
    chart_engine_version: str
    ephemeris: EphemerisMetadata
    mandala_constants_sha256: str
    bodygraph_constants_sha256: str
    design_target_arc_degrees: float
    design_time_tolerance_seconds: float
    design_arc_tolerance_degrees: float
    advanced_substructure_status: str = "unavailable_unvalidated"


@dataclass(frozen=True, slots=True)
class ChartComputation:
    personality_utc: datetime
    design_utc: datetime
    activations: tuple[GateActivation, ...]
    bodygraph: Bodygraph
    design_root: DesignMomentResult
    metadata: ChartEngineMetadata
    stable_features: StableChartFeatures
    chart_features_sha256: str


@dataclass(frozen=True, slots=True)
class StableActivation:
    body: CelestialBody
    side: str
    gate: int
    line: int


@dataclass(frozen=True, slots=True)
class StableChartFeatures:
    """The complete discrete feature vector used to construct intervals."""

    activations: tuple[StableActivation, ...]
    bodygraph: Bodygraph
    chart_engine_version: str
    mandala_constants_sha256: str
    bodygraph_constants_sha256: str
    advanced_substructure_status: str = "unavailable_unvalidated"


def calculate_chart(
    provider: EphemerisProvider,
    birth_utc: datetime,
    *,
    bodies: tuple[CelestialBody, ...] = DEFAULT_ACTIVATION_BODIES,
    design_time_tolerance_seconds: float = 0.01,
    design_arc_tolerance_degrees: float = 1e-8,
) -> ChartComputation:
    """Calculate Personality/Design activations and all core architecture."""

    personality_utc = _require_utc(birth_utc)
    if CelestialBody.SUN not in bodies:
        raise ValueError("bodies must include the Sun for profile derivation")
    if len(set(bodies)) != len(bodies):
        raise ValueError("bodies must not contain duplicates")

    design_root = solve_design_moment(
        provider,
        personality_utc,
        time_tolerance_seconds=design_time_tolerance_seconds,
        arc_tolerance_degrees=design_arc_tolerance_degrees,
    )
    activations: list[GateActivation] = []
    activation_times: tuple[tuple[ActivationSide, datetime], ...] = (
        ("personality", personality_utc),
        ("design", design_root.design_utc),
    )
    for side, at_utc in activation_times:
        for body in bodies:
            position = provider.position(body, at_utc)
            mandala = longitude_to_gate_line(position.longitude)
            activations.append(
                GateActivation(
                    body=body,
                    side=side,
                    longitude=mandala.longitude,
                    gate=mandala.gate,
                    line=mandala.line,
                )
            )

    activation_tuple = tuple(activations)
    bodygraph = derive_bodygraph(activation_tuple)
    metadata = ChartEngineMetadata(
        chart_engine_version=CHART_ENGINE_VERSION,
        ephemeris=provider.metadata,
        mandala_constants_sha256=mandala_constants_sha256(),
        bodygraph_constants_sha256=bodygraph_constants_sha256(),
        design_target_arc_degrees=design_root.target_arc_degrees,
        design_time_tolerance_seconds=design_root.time_tolerance_seconds,
        design_arc_tolerance_degrees=design_root.arc_tolerance_degrees,
    )
    stable_features = StableChartFeatures(
        activations=tuple(
            StableActivation(
                body=item.body,
                side=item.side,
                gate=item.gate,
                line=item.line,
            )
            for item in activation_tuple
        ),
        bodygraph=bodygraph,
        chart_engine_version=metadata.chart_engine_version,
        mandala_constants_sha256=metadata.mandala_constants_sha256,
        bodygraph_constants_sha256=metadata.bodygraph_constants_sha256,
    )
    return ChartComputation(
        personality_utc=personality_utc,
        design_utc=design_root.design_utc,
        activations=activation_tuple,
        bodygraph=bodygraph,
        design_root=design_root,
        metadata=metadata,
        stable_features=stable_features,
        chart_features_sha256=canonical_sha256(stable_features),
    )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("birth timestamp must be timezone-aware")
    return value.astimezone(UTC)
