"""Candidate-complete civil-day interval enumeration with coverage receipts."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from hdmatch.chart.boundaries import build_chart_state_intervals
from hdmatch.chart.calculator import StableChartFeatures, calculate_chart
from hdmatch.chart.ephemeris import EphemerisProvider
from hdmatch.chart.validation import canonical_sha256
from hdmatch.natal_time.provenance import timezone_file_sha256
from hdmatch.natal_time.records import (
    CoverageReceipt,
    LocalBoundary,
    MechanicFact,
    MechanicStatus,
    NatalTimeFreeze,
    NatalTimeInterval,
    NatalTimeManifest,
    NatalTimeResult,
    deterministic_computation_sha256,
)
from hdmatch.util import sha256_json

_QUANTUM = timedelta(microseconds=1)


def enumerate_manifest(
    provider: EphemerisProvider,
    manifest: NatalTimeManifest,
    freeze: NatalTimeFreeze,
) -> NatalTimeResult:
    """Enumerate every accepted civil date without ranks, weights, or priors."""

    _verify_bindings(provider, manifest, freeze)
    zone = ZoneInfo(manifest.timezone_resolution.iana_timezone)
    all_intervals: list[NatalTimeInterval] = []
    receipts: list[CoverageReceipt] = []
    tolerance = manifest.engine_provenance.boundary_root_tolerance_seconds
    for civil_date in manifest.candidate_dates:
        start_utc, end_utc = _validated_civil_date_domain(civil_date, zone)
        stable = build_chart_state_intervals(
            provider,
            start_utc,
            end_utc,
            root_tolerance_seconds=tolerance,
        )
        converted = tuple(_convert_interval(civil_date, interval, zone) for interval in stable)
        _verify_boundary_sides(provider, converted, tolerance)
        receipt = _coverage_receipt(
            civil_date,
            manifest.timezone_resolution.iana_timezone,
            start_utc,
            end_utc,
            converted,
            zone,
            tolerance,
            manifest.engine_provenance.boundary_method,
            manifest.engine_provenance.ephemeris_julian_day_quantum_microseconds,
            manifest.engine_provenance.maximum_equal_ephemeris_time_span_microseconds,
        )
        all_intervals.extend(converted)
        receipts.append(receipt)

    facts = derive_mechanic_facts(tuple(item.full_state for item in all_intervals))
    return NatalTimeResult(
        result_id=(
            "NTR-"
            + sha256_json(
                {
                    "freeze_sha256": freeze.content_sha256,
                    "manifest_sha256": manifest.content_sha256,
                    "enumerator_version": manifest.engine_provenance.enumerator_version,
                }
            )[:24].upper()
        ),
        created_at_utc=freeze.created_at_utc,
        manifest_sha256=manifest.content_sha256,
        freeze_sha256=freeze.content_sha256,
        intervals=tuple(all_intervals),
        coverage_receipts=tuple(receipts),
        mechanic_facts=facts,
    )


def derive_mechanic_facts(states: tuple[dict[str, Any], ...]) -> tuple[MechanicFact, ...]:
    """Return set-theoretic stable/variable facts over complete state leaves."""

    if not states:
        raise ValueError("mechanic facts require at least one complete state")
    flattened = tuple(_flatten_state(state) for state in states)
    paths = sorted(set().union(*(set(item) for item in flattened)))
    facts: list[MechanicFact] = []
    for path in paths:
        values = [item.get(path, _MISSING) for item in flattened]
        if _MISSING in values:
            facts.append(
                MechanicFact(
                    path=path,
                    status=MechanicStatus.UNRESOLVED,
                    observed_values=tuple(
                        _canonical_unique(v for v in values if v is not _MISSING)
                    ),
                    interval_count=len(states),
                )
            )
            continue
        unique = tuple(_canonical_unique(values))
        if len(unique) == 1:
            facts.append(
                MechanicFact(
                    path=path,
                    status=MechanicStatus.STABLE,
                    stable_value=unique[0],
                    observed_values=unique,
                    interval_count=len(states),
                )
            )
        else:
            facts.append(
                MechanicFact(
                    path=path,
                    status=MechanicStatus.VARIABLE,
                    observed_values=unique,
                    interval_count=len(states),
                )
            )
    return tuple(facts)


def _verify_bindings(
    provider: EphemerisProvider,
    manifest: NatalTimeManifest,
    freeze: NatalTimeFreeze,
) -> None:
    if freeze.manifest_sha256 != manifest.content_sha256:
        raise ValueError("freeze does not bind the supplied manifest")
    if freeze.deterministic_computation_sha256 != deterministic_computation_sha256(manifest):
        raise ValueError("freeze computation digest does not match manifest")
    if freeze.engine_provenance_sha256 != manifest.engine_provenance.content_sha256:
        raise ValueError("freeze engine provenance does not match manifest")
    if freeze.state_identity_sha256 != manifest.state_identity_sha256:
        raise ValueError("freeze state identity does not match manifest")
    if (
        sha256_json(asdict(provider.metadata))
        != manifest.engine_provenance.ephemeris_metadata_sha256
    ):
        raise ValueError("runtime ephemeris metadata does not match frozen provenance")
    current_tz_sha = timezone_file_sha256(manifest.timezone_resolution.iana_timezone)
    if current_tz_sha != manifest.timezone_resolution.timezone_file_sha256:
        raise ValueError("runtime timezone data does not match frozen provenance")


def _validated_civil_date_domain(civil_date: date, zone: ZoneInfo) -> tuple[datetime, datetime]:
    start_local = datetime.combine(civil_date, datetime.min.time(), tzinfo=zone).replace(fold=0)
    end_local = datetime.combine(
        civil_date + timedelta(days=1), datetime.min.time(), tzinfo=zone
    ).replace(fold=0)
    start = start_local.astimezone(UTC)
    end = end_local.astimezone(UTC)
    if end <= start:
        raise ValueError(f"civil date has no positive instant domain: {civil_date}")
    if start.astimezone(zone).date() != civil_date:
        raise ValueError(f"civil-date start is ambiguous or nonexistent: {civil_date}")
    if (end - _QUANTUM).astimezone(zone).date() != civil_date:
        raise ValueError(f"civil-date end is ambiguous or nonexistent: {civil_date}")
    if (start - _QUANTUM).astimezone(zone).date() == civil_date:
        raise ValueError(f"civil-date domain starts too late: {civil_date}")
    if end.astimezone(zone).date() == civil_date:
        raise ValueError(f"civil-date domain ends too early: {civil_date}")
    return start, end


def _convert_interval(civil_date: date, interval: Any, zone: ZoneInfo) -> NatalTimeInterval:
    if canonical_sha256(interval.features) != interval.feature_sha256:
        raise ValueError("internal interval feature digest changed before canonical conversion")
    state = _canonical_full_state(interval.features)
    state_sha = sha256_json(state)
    return NatalTimeInterval(
        civil_date=civil_date,
        start=_local_boundary(interval.start_utc, zone),
        end=_local_boundary(interval.end_utc, zone),
        representative_utc=interval.representative_utc,
        duration_microseconds=_duration_microseconds(interval.start_utc, interval.end_utc),
        full_state_sha256=state_sha,
        full_state=state,
        boundary_events=tuple(
            (
                f"{event.at_utc.isoformat()}|{event.side}|{event.body.value}|"
                f"{event.before_gate}.{event.before_line}->"
                f"{event.after_gate}.{event.after_line}"
            )
            for event in interval.boundary_events
        ),
    )


def _verify_boundary_sides(
    provider: EphemerisProvider,
    intervals: tuple[NatalTimeInterval, ...],
    design_time_tolerance_seconds: float,
) -> None:
    for previous, current in zip(intervals, intervals[1:], strict=False):
        boundary = current.start.utc
        before_hash = sha256_json(
            _canonical_full_state(
                calculate_chart(
                    provider,
                    boundary - _QUANTUM,
                    design_time_tolerance_seconds=design_time_tolerance_seconds,
                ).stable_features
            )
        )
        at_hash = sha256_json(
            _canonical_full_state(
                calculate_chart(
                    provider,
                    boundary,
                    design_time_tolerance_seconds=design_time_tolerance_seconds,
                ).stable_features
            )
        )
        if before_hash != previous.full_state_sha256 or at_hash != current.full_state_sha256:
            raise ValueError("interval boundary sides do not match adjacent complete states")


def _coverage_receipt(
    civil_date: date,
    iana_timezone: str,
    start: datetime,
    end: datetime,
    intervals: tuple[NatalTimeInterval, ...],
    zone: ZoneInfo,
    tolerance: float,
    boundary_method: str,
    ephemeris_julian_day_quantum_microseconds: float | None,
    maximum_equal_ephemeris_time_span_microseconds: int,
) -> CoverageReceipt:
    if not intervals or intervals[0].start.utc != start or intervals[-1].end.utc != end:
        raise ValueError("intervals do not cover the complete civil-date domain")
    for previous, current in zip(intervals, intervals[1:], strict=False):
        if previous.end.utc != current.start.utc:
            raise ValueError("interval partition contains a gap or overlap")
        if previous.full_state_sha256 == current.full_state_sha256:
            raise ValueError("interval partition is not maximal")
    total = sum(item.duration_microseconds for item in intervals)
    return CoverageReceipt(
        civil_date=civil_date,
        iana_timezone=iana_timezone,
        domain_start=_local_boundary(start, zone),
        domain_end=_local_boundary(end, zone),
        actual_duration_microseconds=_duration_microseconds(start, end),
        interval_count=len(intervals),
        interval_state_sha256=tuple(item.full_state_sha256 for item in intervals),
        summed_interval_duration_microseconds=total,
        boundary_method=boundary_method,
        ephemeris_julian_day_quantum_microseconds=(ephemeris_julian_day_quantum_microseconds),
        maximum_equal_ephemeris_time_span_microseconds=(
            maximum_equal_ephemeris_time_span_microseconds
        ),
        boundary_root_tolerance_seconds=tolerance,
    )


def _local_boundary(value: datetime, zone: ZoneInfo) -> LocalBoundary:
    utc = value.astimezone(UTC)
    local = utc.astimezone(zone)
    offset = local.utcoffset()
    if offset is None:
        raise ValueError("local boundary has no UTC offset")
    return LocalBoundary(
        utc=utc,
        local=local,
        utc_offset_seconds=int(offset.total_seconds()),
        fold=0 if local.fold == 0 else 1,
    )


def _duration_microseconds(start: datetime, end: datetime) -> int:
    delta = end - start
    return (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds


def _canonical_full_state(features: StableChartFeatures) -> dict[str, Any]:
    activations: dict[str, dict[str, dict[str, int]]] = {
        "personality": {},
        "design": {},
    }
    for activation in features.activations:
        activations[activation.side][activation.body.value] = {
            "gate": activation.gate,
            "line": activation.line,
        }
    bodygraph = features.bodygraph
    return {
        "activations": activations,
        "bodygraph": {
            "active_gates": list(bodygraph.active_gates),
            "channels": list(bodygraph.channels),
            "defined_centers": [item.value for item in bodygraph.defined_centers],
            "definition_components": [
                [center.value for center in component]
                for component in bodygraph.definition_components
            ],
            "type": bodygraph.type.value,
            "strategy": bodygraph.strategy.value,
            "authority": bodygraph.authority.value,
            "profile": bodygraph.profile,
            "definition": bodygraph.definition.value,
        },
        "chart_engine_version": features.chart_engine_version,
        "mandala_constants_sha256": features.mandala_constants_sha256,
        "bodygraph_constants_sha256": features.bodygraph_constants_sha256,
        "advanced_substructure_status": features.advanced_substructure_status,
    }


class _Missing:
    pass


_MISSING = _Missing()


def _flatten_state(value: Any, path: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            child = f"{path}.{key}" if path else str(key)
            result.update(_flatten_state(value[key], child))
        return result
    if isinstance(value, (list, tuple)):
        result = {}
        for index, item in enumerate(value):
            result.update(_flatten_state(item, f"{path}[{index}]"))
        return result
    return {path: value}


def _canonical_unique(values: Any) -> list[Any]:
    by_json: dict[str, Any] = {}
    for value in values:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        by_json.setdefault(encoded, value)
    return [by_json[key] for key in sorted(by_json)]
