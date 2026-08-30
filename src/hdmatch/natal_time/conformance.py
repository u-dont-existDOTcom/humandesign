"""Canonical chart-engine inventory and actual temporal-resolution probes."""

from __future__ import annotations

import math
from dataclasses import fields
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from types import ModuleType
from typing import Literal

from pydantic import Field, model_validator

from hdmatch.chart.bodygraph import Bodygraph, GateActivation
from hdmatch.chart.calculator import (
    ChartComputation,
    ChartEngineMetadata,
    StableActivation,
    StableChartFeatures,
)
from hdmatch.chart.design_moment import DesignMomentResult
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EphemerisMetadata,
    EphemerisProvider,
    _julian_day_ut,
)
from hdmatch.chart.rave_mandala import MandalaPosition
from hdmatch.natal_time.models import NatalTimeModel
from hdmatch.util import sha256_json


class FieldClassification(StrEnum):
    DISCRETE_STATE_IDENTITY = "discrete_state_identity"
    CANDIDATE_COORDINATE = "candidate_coordinate"
    CONTINUOUS_DIAGNOSTIC = "continuous_diagnostic"
    PROVENANCE = "provenance"
    UNSUPPORTED_OR_UNAVAILABLE = "unsupported_or_unavailable"
    EXCLUDED_FROM_IDENTITY = "excluded_from_identity"


class EngineFieldRecord(NatalTimeModel):
    source_field: str = Field(min_length=3)
    output_path: str = Field(min_length=1)
    classification: FieldClassification
    included_in_interval_identity: bool
    bound_by_manifest: bool
    exclusion_reason: str | None = None
    transition_driver: str | None = None

    @model_validator(mode="after")
    def exclusion_is_explicit(self) -> EngineFieldRecord:
        if self.included_in_interval_identity and self.exclusion_reason is not None:
            raise ValueError("identity fields cannot have an exclusion reason")
        if not self.included_in_interval_identity and not self.exclusion_reason:
            raise ValueError("every non-identity field requires an exclusion reason")
        return self


class EngineFieldInventory(NatalTimeModel):
    schema_version: Literal["natal-real-engine-field-inventory-v1"] = (
        "natal-real-engine-field-inventory-v1"
    )
    chart_engine_version: Literal["chart-engine-v1"] = "chart-engine-v1"
    complete_against_runtime_dataclasses: Literal[True] = True
    fields: tuple[EngineFieldRecord, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def source_fields_are_unique(self) -> EngineFieldInventory:
        names = [item.source_field for item in self.fields]
        if len(names) != len(set(names)):
            raise ValueError("field inventory source fields must be unique")
        return self

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


class JulianDayResolutionSample(NatalTimeModel):
    reference_utc: datetime
    sampled_coordinate_count: int = Field(gt=1)
    distinct_julian_day_count: int = Field(gt=0)
    julian_day_ulp_microseconds: float = Field(gt=0.0)
    minimum_equal_value_run_points: int = Field(gt=0)
    maximum_equal_value_run_points: int = Field(gt=0)
    maximum_equal_value_coordinate_span_microseconds: int = Field(ge=0)
    sun_equal_after_one_microsecond: bool
    sun_equal_after_julian_quantum_ceiling: bool


class EngineTemporalResolutionAudit(NatalTimeModel):
    schema_version: Literal["natal-real-engine-temporal-resolution-v1"] = (
        "natal-real-engine-temporal-resolution-v1"
    )
    ephemeris_provider: Literal["swiss_ephemeris_local_files"] = "swiss_ephemeris_local_files"
    ephemeris_library_version: str
    python_datetime_coordinate_quantum_microseconds: Literal[1] = 1
    julian_day_conversion: Literal["utc-calendar-to-binary64-julian-day"] = (
        "utc-calendar-to-binary64-julian-day"
    )
    boundary_coordinate_convention: Literal[
        "first-python-datetime-microsecond-whose-engine-discrete-state-differs"
    ] = "first-python-datetime-microsecond-whose-engine-discrete-state-differs"
    mandala_equality_convention: Literal["half-open-boundary-enters-new-sector"] = (
        "half-open-boundary-enters-new-sector"
    )
    design_root_method: Literal["binary64-bisection-of-88-degree-solar-arc"] = (
        "binary64-bisection-of-88-degree-solar-arc"
    )
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    samples: tuple[JulianDayResolutionSample, ...] = Field(min_length=1)
    maximum_observed_equal_julian_day_coordinate_span_microseconds: int = Field(ge=0)
    adjacent_python_microseconds_are_distinguishable: Literal[False] = False
    astronomical_microsecond_precision_claimed: Literal[False] = False
    exactness_scope: Literal[
        "exact-on-declared-python-coordinate-grid-relative-to-pinned-binary64-engine"
    ] = "exact-on-declared-python-coordinate-grid-relative-to-pinned-binary64-engine"
    precision_warning: str = Field(min_length=1)

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


_RUNTIME_CLASSES = (
    ChartComputation,
    ChartEngineMetadata,
    StableActivation,
    StableChartFeatures,
    GateActivation,
    Bodygraph,
    DesignMomentResult,
    MandalaPosition,
    EphemerisMetadata,
)


def _record(
    source_field: str,
    output_path: str,
    classification: FieldClassification,
    *,
    identity: bool = False,
    manifest: bool = False,
    reason: str | None = None,
    driver: str | None = None,
) -> EngineFieldRecord:
    return EngineFieldRecord(
        source_field=source_field,
        output_path=output_path,
        classification=classification,
        included_in_interval_identity=identity,
        bound_by_manifest=manifest,
        exclusion_reason=reason,
        transition_driver=driver,
    )


def build_engine_field_inventory() -> EngineFieldInventory:
    """Inventory every field on every dataclass in the canonical engine surface."""

    discrete = FieldClassification.DISCRETE_STATE_IDENTITY
    coordinate = FieldClassification.CANDIDATE_COORDINATE
    continuous = FieldClassification.CONTINUOUS_DIAGNOSTIC
    provenance = FieldClassification.PROVENANCE
    unsupported = FieldClassification.UNSUPPORTED_OR_UNAVAILABLE
    excluded = FieldClassification.EXCLUDED_FROM_IDENTITY
    derived_driver = "complete personality/design gate-line activation vector"

    records = (
        _record(
            "ChartComputation.personality_utc",
            "personality_utc",
            coordinate,
            reason="candidate coordinate; interval membership carries the value",
        ),
        _record(
            "ChartComputation.design_utc",
            "design_utc",
            continuous,
            reason="continuous solved diagnostic; design gate/line outputs drive identity",
        ),
        _record(
            "ChartComputation.activations",
            "activations",
            excluded,
            reason="diagnostic activation objects; StableChartFeatures.activations is canonical",
        ),
        _record(
            "ChartComputation.bodygraph",
            "bodygraph",
            excluded,
            reason="diagnostic duplicate; StableChartFeatures.bodygraph is canonical",
        ),
        _record(
            "ChartComputation.design_root",
            "design_root",
            continuous,
            reason="solver diagnostics are bound by method/tolerances, not interval identity",
        ),
        _record(
            "ChartComputation.metadata",
            "metadata",
            provenance,
            manifest=True,
            reason="expanded provenance is bound by the manifest",
        ),
        _record(
            "ChartComputation.stable_features",
            "stable_features",
            excluded,
            reason="container whose leaves are inventoried separately",
        ),
        _record(
            "ChartComputation.chart_features_sha256",
            "chart_features_sha256",
            provenance,
            reason="derived commitment to identity fields, not an independent state field",
        ),
        _record(
            "ChartEngineMetadata.chart_engine_version",
            "chart_engine_version",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "ChartEngineMetadata.ephemeris",
            "engine_metadata.ephemeris",
            provenance,
            manifest=True,
            reason="expanded ephemeris provenance is manifest-bound",
        ),
        _record(
            "ChartEngineMetadata.mandala_constants_sha256",
            "mandala_constants_sha256",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "ChartEngineMetadata.bodygraph_constants_sha256",
            "bodygraph_constants_sha256",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "ChartEngineMetadata.design_target_arc_degrees",
            "engine_metadata.design_target_arc_degrees",
            provenance,
            manifest=True,
            reason="solver convention is manifest-bound and does not vary by interval",
        ),
        _record(
            "ChartEngineMetadata.design_time_tolerance_seconds",
            "engine_metadata.design_time_tolerance_seconds",
            provenance,
            manifest=True,
            reason="solver tolerance is manifest-bound and does not vary by interval",
        ),
        _record(
            "ChartEngineMetadata.design_arc_tolerance_degrees",
            "engine_metadata.design_arc_tolerance_degrees",
            provenance,
            manifest=True,
            reason="solver tolerance is manifest-bound and does not vary by interval",
        ),
        _record(
            "ChartEngineMetadata.advanced_substructure_status",
            "advanced_substructure_status",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record("StableActivation.body", "activations.{side}.{body}.body", discrete, identity=True),
        _record("StableActivation.side", "activations.{side}.{body}.side", discrete, identity=True),
        _record(
            "StableActivation.gate",
            "activations.{side}.{body}.gate",
            discrete,
            identity=True,
            driver="body longitude crossing a frozen gate boundary",
        ),
        _record(
            "StableActivation.line",
            "activations.{side}.{body}.line",
            discrete,
            identity=True,
            driver="body longitude crossing a frozen line boundary",
        ),
        _record(
            "StableChartFeatures.activations",
            "activations",
            excluded,
            reason="container; every StableActivation field is inventoried separately",
        ),
        _record(
            "StableChartFeatures.bodygraph",
            "bodygraph",
            excluded,
            reason="container; every Bodygraph field is inventoried separately",
        ),
        _record(
            "StableChartFeatures.chart_engine_version",
            "chart_engine_version",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "StableChartFeatures.mandala_constants_sha256",
            "mandala_constants_sha256",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "StableChartFeatures.bodygraph_constants_sha256",
            "bodygraph_constants_sha256",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "StableChartFeatures.advanced_substructure_status",
            "advanced_substructure_status",
            provenance,
            identity=True,
            manifest=True,
        ),
        _record(
            "GateActivation.body",
            "diagnostics.activations[].body",
            excluded,
            reason="key axis represented by stable activation identity",
        ),
        _record(
            "GateActivation.side",
            "diagnostics.activations[].side",
            excluded,
            reason="key axis represented by stable activation identity",
        ),
        _record(
            "GateActivation.longitude",
            "diagnostics.activations[].longitude",
            continuous,
            reason="continuous diagnostic; frozen gate/line mapping drives identity",
        ),
        _record(
            "GateActivation.gate",
            "diagnostics.activations[].gate",
            excluded,
            reason="duplicate of StableActivation.gate",
        ),
        _record(
            "GateActivation.line",
            "diagnostics.activations[].line",
            excluded,
            reason="duplicate of StableActivation.line",
        ),
        *(
            _record(
                f"Bodygraph.{name}",
                f"bodygraph.{name}",
                discrete,
                identity=True,
                driver=derived_driver,
            )
            for name in (
                "active_gates",
                "channels",
                "defined_centers",
                "definition_components",
                "type",
                "strategy",
                "authority",
                "profile",
                "definition",
            )
        ),
        _record(
            "DesignMomentResult.birth_utc",
            "design_root.birth_utc",
            coordinate,
            reason="duplicate candidate coordinate",
        ),
        _record(
            "DesignMomentResult.design_utc",
            "design_root.design_utc",
            continuous,
            reason="continuous solved diagnostic",
        ),
        _record(
            "DesignMomentResult.target_arc_degrees",
            "design_root.target_arc_degrees",
            provenance,
            manifest=True,
            reason="fixed solver convention",
        ),
        _record(
            "DesignMomentResult.solved_arc_degrees",
            "design_root.solved_arc_degrees",
            continuous,
            reason="continuous solver diagnostic",
        ),
        _record(
            "DesignMomentResult.residual_degrees",
            "design_root.residual_degrees",
            continuous,
            reason="continuous solver diagnostic",
        ),
        _record(
            "DesignMomentResult.bracket_start_utc",
            "design_root.bracket_start_utc",
            continuous,
            reason="continuous solver diagnostic",
        ),
        _record(
            "DesignMomentResult.bracket_end_utc",
            "design_root.bracket_end_utc",
            continuous,
            reason="continuous solver diagnostic",
        ),
        _record(
            "DesignMomentResult.iterations",
            "design_root.iterations",
            continuous,
            reason="solver diagnostic; not chart state",
        ),
        _record(
            "DesignMomentResult.time_tolerance_seconds",
            "design_root.time_tolerance_seconds",
            provenance,
            manifest=True,
            reason="fixed solver tolerance",
        ),
        _record(
            "DesignMomentResult.arc_tolerance_degrees",
            "design_root.arc_tolerance_degrees",
            provenance,
            manifest=True,
            reason="fixed solver tolerance",
        ),
        _record(
            "MandalaPosition.longitude",
            "mandala.longitude",
            continuous,
            reason="continuous normalized diagnostic",
        ),
        _record(
            "MandalaPosition.gate",
            "mandala.gate",
            excluded,
            reason="duplicate of StableActivation.gate",
        ),
        _record(
            "MandalaPosition.line",
            "mandala.line",
            excluded,
            reason="duplicate of StableActivation.line",
        ),
        _record(
            "MandalaPosition.gate_index",
            "mandala.gate_index",
            excluded,
            reason="one-to-one redundant encoding of gate under frozen gate order",
        ),
        _record(
            "MandalaPosition.fraction_through_line",
            "mandala.fraction_through_line",
            continuous,
            reason="continuous within-line diagnostic",
        ),
        _record(
            "MandalaPosition.color",
            "mandala.color",
            unsupported,
            reason="engine always emits None; constants are not validated",
        ),
        _record(
            "MandalaPosition.tone",
            "mandala.tone",
            unsupported,
            reason="engine always emits None; constants are not validated",
        ),
        _record(
            "MandalaPosition.base",
            "mandala.base",
            unsupported,
            reason="engine always emits None; constants are not validated",
        ),
        _record(
            "MandalaPosition.advanced_substructure_status",
            "mandala.advanced_substructure_status",
            provenance,
            manifest=True,
            reason="duplicate of canonical stable status",
        ),
        _record(
            "EphemerisMetadata.provider",
            "engine_metadata.ephemeris.provider",
            provenance,
            manifest=True,
            reason="manifest-bound engine identity",
        ),
        _record(
            "EphemerisMetadata.library_version",
            "engine_metadata.ephemeris.library_version",
            provenance,
            manifest=True,
            reason="manifest-bound engine identity",
        ),
        _record(
            "EphemerisMetadata.files",
            "engine_metadata.ephemeris.files",
            provenance,
            manifest=True,
            reason="manifest-bound file checksums",
        ),
        _record(
            "EphemerisMetadata.calculation_flags",
            "engine_metadata.ephemeris.calculation_flags",
            provenance,
            manifest=True,
            reason="manifest-bound coordinate conventions",
        ),
        _record(
            "EphemerisMetadata.coordinate_frame",
            "engine_metadata.ephemeris.coordinate_frame",
            provenance,
            manifest=True,
            reason="manifest-bound coordinate convention",
        ),
        _record(
            "EphemerisMetadata.node_convention",
            "engine_metadata.ephemeris.node_convention",
            provenance,
            manifest=True,
            reason="manifest-bound true-node convention",
        ),
    )
    expected = {
        f"{runtime_class.__name__}.{field.name}"
        for runtime_class in _RUNTIME_CLASSES
        for field in fields(runtime_class)
    }
    actual = {item.source_field for item in records}
    if actual != expected:
        raise RuntimeError(
            "engine inventory drifted from runtime dataclasses: "
            f"missing={sorted(expected - actual)}, unexpected={sorted(actual - expected)}"
        )
    return EngineFieldInventory(fields=records)


def audit_swiss_temporal_resolution(
    provider: EphemerisProvider,
    swe_module: ModuleType,
    *,
    design_root_time_tolerance_seconds: float = 0.01,
    design_root_arc_tolerance_degrees: float = 1e-8,
    references: tuple[datetime, ...] = (
        datetime(1900, 1, 1, tzinfo=UTC),
        datetime(2000, 1, 1, tzinfo=UTC),
        datetime(2026, 8, 30, tzinfo=UTC),
        datetime(2099, 12, 31, tzinfo=UTC),
    ),
) -> EngineTemporalResolutionAudit:
    """Measure the binary64 Julian-day grid without claiming astronomical µs precision."""

    if provider.metadata.provider != "swiss_ephemeris_local_files":
        raise ValueError("temporal audit requires the canonical strict Swiss-file provider")
    samples: list[JulianDayResolutionSample] = []
    for reference in references:
        if reference.tzinfo is None or reference.utcoffset() is None:
            raise ValueError("temporal audit references must be timezone-aware")
        reference = reference.astimezone(UTC)
        values = tuple(
            _julian_day_ut(swe_module, reference + timedelta(microseconds=offset))
            for offset in range(501)
        )
        runs: list[int] = []
        run_start = 0
        for index in range(1, len(values)):
            if values[index] != values[index - 1]:
                runs.append(index - run_start)
                run_start = index
        runs.append(len(values) - run_start)
        quantum_ceiling = math.ceil(math.ulp(values[0]) * 86_400_000_000.0)
        sun_at_reference = provider.position(CelestialBody.SUN, reference).longitude
        samples.append(
            JulianDayResolutionSample(
                reference_utc=reference,
                sampled_coordinate_count=len(values),
                distinct_julian_day_count=len(set(values)),
                julian_day_ulp_microseconds=math.ulp(values[0]) * 86_400_000_000.0,
                minimum_equal_value_run_points=min(runs),
                maximum_equal_value_run_points=max(runs),
                maximum_equal_value_coordinate_span_microseconds=max(runs) - 1,
                sun_equal_after_one_microsecond=(
                    provider.position(
                        CelestialBody.SUN, reference + timedelta(microseconds=1)
                    ).longitude
                    == sun_at_reference
                ),
                sun_equal_after_julian_quantum_ceiling=(
                    provider.position(
                        CelestialBody.SUN,
                        reference + timedelta(microseconds=quantum_ceiling),
                    ).longitude
                    == sun_at_reference
                ),
            )
        )
    return EngineTemporalResolutionAudit(
        ephemeris_library_version=provider.metadata.library_version,
        design_root_time_tolerance_seconds=design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=design_root_arc_tolerance_degrees,
        samples=tuple(samples),
        maximum_observed_equal_julian_day_coordinate_span_microseconds=max(
            item.maximum_equal_value_coordinate_span_microseconds for item in samples
        ),
        precision_warning=(
            "Boundary timestamps are coordinates on the Python datetime grid after binary64 "
            "Julian-day conversion. Their six decimal places do not establish astronomical "
            "microsecond precision; adjacent input microseconds commonly evaluate identically."
        ),
    )
