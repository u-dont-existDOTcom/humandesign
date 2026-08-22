"""Deterministic conversion from chart-engine records to public API records."""

from __future__ import annotations

from pathlib import Path

from hdmatch.api.models import (
    ActivationResponse,
    BoundaryEventResponse,
    ChartEngineMetadataResponse,
    ChartRecord,
    ChartStateInterval,
    EphemerisFileMetadata,
    EphemerisMetadataResponse,
)
from hdmatch.chart.boundaries import StableInterval
from hdmatch.chart.calculator import ChartComputation, calculate_chart
from hdmatch.chart.ephemeris import EphemerisMetadata, EphemerisProvider
from hdmatch.chart.validation import canonical_sha256


def ephemeris_metadata(metadata: EphemerisMetadata) -> EphemerisMetadataResponse:
    return EphemerisMetadataResponse(
        provider=metadata.provider,
        library_version=metadata.library_version,
        files=tuple(
            EphemerisFileMetadata(
                name=Path(item.path).name,
                sha256=item.sha256,
                size_bytes=item.size_bytes,
            )
            for item in metadata.files
        ),
        calculation_flags=metadata.calculation_flags,
        coordinate_frame=metadata.coordinate_frame,
        node_convention=metadata.node_convention.value,
    )


def engine_metadata(computation: ChartComputation) -> ChartEngineMetadataResponse:
    metadata = computation.metadata
    return ChartEngineMetadataResponse(
        chart_engine_version=metadata.chart_engine_version,
        ephemeris=ephemeris_metadata(metadata.ephemeris),
        mandala_constants_sha256=metadata.mandala_constants_sha256,
        bodygraph_constants_sha256=metadata.bodygraph_constants_sha256,
        design_target_arc_degrees=metadata.design_target_arc_degrees,
        design_time_tolerance_seconds=metadata.design_time_tolerance_seconds,
        design_arc_tolerance_degrees=metadata.design_arc_tolerance_degrees,
        advanced_substructure_status="unavailable_unvalidated",
    )


def _activation_records(
    computation: ChartComputation, side: str
) -> dict[str, ActivationResponse]:
    records: dict[str, ActivationResponse] = {}
    for activation in computation.activations:
        if activation.side != side:
            continue
        records[activation.body.value] = ActivationResponse(
            body=activation.body,
            side=activation.side,
            longitude=activation.longitude,
            gate=activation.gate,
            line=activation.line,
        )
    return records


def chart_record(computation: ChartComputation) -> ChartRecord:
    bodygraph = computation.bodygraph
    return ChartRecord(
        personality_utc=computation.personality_utc,
        design_utc=computation.design_utc,
        complete_feature_hash=computation.chart_features_sha256,
        personality_activations=_activation_records(computation, "personality"),
        design_activations=_activation_records(computation, "design"),
        type=bodygraph.type.value,
        strategy=bodygraph.strategy.value,
        authority=bodygraph.authority.value,
        profile=bodygraph.profile,
        definition=bodygraph.definition.value,
        defined_centers=tuple(center.value for center in bodygraph.defined_centers),
        channels=bodygraph.channels,
        engine_metadata=engine_metadata(computation),
    )


def state_interval_record(
    provider: EphemerisProvider,
    interval: StableInterval,
    *,
    root_tolerance_seconds: float,
) -> ChartStateInterval:
    computation = calculate_chart(
        provider,
        interval.representative_utc,
        design_time_tolerance_seconds=root_tolerance_seconds,
    )
    if computation.chart_features_sha256 != interval.feature_sha256:
        raise RuntimeError("interval representative does not match its complete feature hash")
    bodygraph = computation.bodygraph
    state_hash = canonical_sha256(
        {
            "start_utc": interval.start_utc,
            "end_utc": interval.end_utc,
            "complete_feature_hash": interval.feature_sha256,
        }
    )
    boundary_events = tuple(
        BoundaryEventResponse(
            at_utc=event.at_utc,
            ephemeris_utc=event.ephemeris_utc,
            side=event.side,
            body=event.body,
            resolution=event.resolution.value,
            boundary_longitude=event.boundary_longitude,
            before_gate=event.before_gate,
            before_line=event.before_line,
            after_gate=event.after_gate,
            after_line=event.after_line,
            root_tolerance_seconds=event.root_tolerance_seconds,
        )
        for event in interval.boundary_events
    )
    return ChartStateInterval(
        state_id=f"STATE-{state_hash[:24]}",
        start_utc=interval.start_utc,
        end_utc=interval.end_utc,
        representative_utc=interval.representative_utc,
        complete_feature_hash=interval.feature_sha256,
        personality_activations=_activation_records(computation, "personality"),
        design_utc=computation.design_utc,
        design_activations=_activation_records(computation, "design"),
        type=bodygraph.type.value,
        strategy=bodygraph.strategy.value,
        authority=bodygraph.authority.value,
        profile=bodygraph.profile,
        definition=bodygraph.definition.value,
        defined_centers=tuple(center.value for center in bodygraph.defined_centers),
        channels=bodygraph.channels,
        boundary_events=boundary_events,
    )
