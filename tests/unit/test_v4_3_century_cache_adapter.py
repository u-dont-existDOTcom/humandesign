from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.century_cache import (
    CACHEABLE_M0_M2_FEATURE_COLUMNS,
    CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256,
    CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256,
    cacheable_chart_state_to_century_record,
    feature_registry_sha256,
)
from hdmatch.century_cache.parquet import (
    CenturyCacheParquetError,
    read_parquet_shard,
    validate_row_features,
    write_parquet_shard_new,
)
from hdmatch.chart.boundaries import (
    build_production_chart_state_intervals,
    canonical_boundary_event_string,
)
from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.ephemeris import NodeConvention, SwissEphemerisProvider
from hdmatch.chart.feature_registry import (
    CACHEABLE_M0_M2_REGISTRY,
    FeatureCoverageError,
    FeatureId,
    compile_required_feature_registry,
    serialize_cacheable_chart_state,
)
from hdmatch.experiments.canonical import canonical_json_bytes
from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_REPOSITORY,
    EphemerisFilePin,
    EphemerisSourceManifest,
    VerifiedEphemerisProvenance,
    verify_ephemeris_directory,
)


class _DeterministicFakeSwiss:
    FLG_JPLEPH = 1
    FLG_SWIEPH = 2
    FLG_MOSEPH = 4
    FLG_EPHMASK = 7
    FLG_SPEED = 256
    GREG_CAL = 1
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
    MEAN_NODE = 10
    TRUE_NODE = 11
    version = "deterministic-fake"

    def __init__(self, planetary_file: Path, lunar_file: Path) -> None:
        self.files = (planetary_file, lunar_file)

    def set_ephe_path(self, _path: str) -> None:
        pass

    def julday(self, year: int, month: int, day: int, hour: float, _calendar: int) -> float:
        midnight = datetime(year, month, day, tzinfo=UTC)
        return float(midnight.toordinal()) + hour / 24.0

    def calc_ut(
        self,
        julian_day: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        if body == self.SUN:
            longitude, speed = (julian_day + 261.4998) % 360.0, 1.0
        else:
            longitude, speed = (body * 17.0 + 0.01 * julian_day) % 360.0, 0.01
        return (longitude, 0.0, 1.0, speed, 0.0, 0.0), flags

    def get_current_file_data(self, index: int) -> tuple[str, float, float, int]:
        return str(self.files[index]), 0.0, 0.0, 441


def _verified_fixture(
    root: Path,
    *,
    node_convention: NodeConvention = NodeConvention.TRUE,
) -> tuple[SwissEphemerisProvider, VerifiedEphemerisProvenance]:
    ephemeris_directory = root / "ephemeris"
    ephemeris_directory.mkdir()
    planetary = ephemeris_directory / "sepl_18.se1"
    lunar = ephemeris_directory / "semo_18.se1"
    planetary.write_bytes(b"deterministic-planetary-test-file")
    lunar.write_bytes(b"deterministic-lunar-test-file")
    pins = (
        EphemerisFilePin(
            name=planetary.name,
            bytes=planetary.stat().st_size,
            sha256=_sha256_file(planetary),
        ),
        EphemerisFilePin(
            name=lunar.name,
            bytes=lunar.stat().st_size,
            sha256=_sha256_file(lunar),
        ),
    )
    manifest = EphemerisSourceManifest(
        schema_version="ephemeris-file-manifest-v1",
        provider="Swiss Ephemeris",
        upstream_repository=PINNED_UPSTREAM_REPOSITORY,
        upstream_commit=PINNED_UPSTREAM_COMMIT,
        files=pins,
        tested_range="unit fixture only",
        license="test fixture",
    )
    manifest_path = root / "manifest.json"
    manifest_path.write_bytes(canonical_json_bytes(manifest.model_dump(mode="json")))
    verified = verify_ephemeris_directory(
        source_manifest_path=manifest_path,
        ephemeris_directory=ephemeris_directory,
    )
    fake = _DeterministicFakeSwiss(planetary, lunar)
    provider = SwissEphemerisProvider(
        (planetary, lunar),
        node_convention=node_convention,
        _swe_module=fake,  # type: ignore[arg-type]
    )
    return provider, verified


def _sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_exact_m2_state_round_trips_through_zstd_parquet(tmp_path: Path) -> None:
    provider, verified_ephemeris = _verified_fixture(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    end = start + timedelta(minutes=1)
    intervals = build_production_chart_state_intervals(provider, start, end)
    interval = next(item for item in intervals if item.boundary_events)
    computation = calculate_chart(provider, interval.representative_utc)
    boundary_events = tuple(
        sorted(canonical_boundary_event_string(event) for event in interval.boundary_events)
    )
    cacheable = serialize_cacheable_chart_state(
        computation,
        provider=provider,
        utc_start=interval.start_utc,
        utc_end=interval.end_utc,
        boundary_events=boundary_events,
    )
    row = cacheable_chart_state_to_century_record(cacheable)
    provenance = cacheable.chart_features.provenance

    assert provenance.ephemeris_file_set_sha256 == (verified_ephemeris.ephemeris_file_set_sha256)
    assert [item.model_dump(mode="json") for item in provenance.ephemeris_files] == [
        item.model_dump(mode="json") for item in verified_ephemeris.files
    ]
    assert row.semantic_feature_registry_sha256 == CACHEABLE_M0_M2_REGISTRY.sha256()
    assert row.feature_registry_sha256 == feature_registry_sha256(CACHEABLE_M0_M2_FEATURE_COLUMNS)
    assert row.representative_utc == interval.representative_utc
    assert row.chart_features_sha256 == cacheable.chart_features_sha256
    assert row.boundary_events == cacheable.boundary_events
    serialized = json.loads(row.boundary_events[0])
    source_event = next(
        event
        for event in interval.boundary_events
        if canonical_boundary_event_string(event) == row.boundary_events[0]
    )
    assert serialized == {
        "after": {"gate": source_event.after_gate, "line": source_event.after_line},
        "at_utc": source_event.at_utc.isoformat(),
        "before": {"gate": source_event.before_gate, "line": source_event.before_line},
        "body": source_event.body.value,
        "boundary_longitude": source_event.boundary_longitude,
        "ephemeris_utc": source_event.ephemeris_utc.isoformat(),
        "resolution": source_event.resolution.value,
        "root_tolerance_seconds": source_event.root_tolerance_seconds,
        "schema_version": "chart-boundary-event-v1",
        "side": source_event.side,
    }

    shard = write_parquet_shard_new(
        tmp_path / "states-fixture.parquet.zst",
        (row,),
        CACHEABLE_M0_M2_FEATURE_COLUMNS,
    )

    assert read_parquet_shard(shard, CACHEABLE_M0_M2_FEATURE_COLUMNS) == (row,)


def test_adapter_emits_every_physical_feature_without_unknown_boolean_coercion(
    tmp_path: Path,
) -> None:
    assert CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256 == (
        "6a081572beec6053fb0af94c70ec47c1389b57da65b08a96603e331992eb23e9"
    )
    assert CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256 == (
        "b24791ea04702d87df32be5c8821115f6b0f14819f61cd3b83ad30cca721d3ac"
    )
    provider, _ = _verified_fixture(tmp_path)
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    computation = calculate_chart(provider, birth)
    cacheable = serialize_cacheable_chart_state(
        computation,
        provider=provider,
        utc_start=birth,
        utc_end=birth + timedelta(minutes=1),
    )
    row = cacheable_chart_state_to_century_record(cacheable)

    assert tuple(row.feature_mapping()) == tuple(
        item.feature_id for item in CACHEABLE_M0_M2_FEATURE_COLUMNS
    )
    assert all(value is not None for value in row.feature_mapping().values())
    assert row.feature_mapping()[FeatureId.CIRCUITRY_STATUS.value] == ("unavailable_unvalidated")
    assert row.feature_mapping()[FeatureId.ADVANCED_STATUS.value] == ("unavailable_unvalidated")

    malformed = cacheable.model_dump(mode="python")
    malformed["boundary_events"] = ("z-event", "a-event")
    with pytest.raises(ValidationError, match="sorted and unique"):
        type(cacheable).model_validate(malformed, strict=True)


def test_missing_physical_or_conditional_capability_fails_closed(tmp_path: Path) -> None:
    provider, verified_ephemeris = _verified_fixture(tmp_path)
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    computation = calculate_chart(provider, birth)
    cacheable = serialize_cacheable_chart_state(
        computation,
        provider=provider,
        utc_start=birth,
        utc_end=birth + timedelta(minutes=1),
    )
    conditional = compile_required_feature_registry(
        (*CACHEABLE_M0_M2_REGISTRY.feature_ids, FeatureId.CIRCUITRY_CHANNEL_METADATA)
    )
    with pytest.raises(FeatureCoverageError, match="coverage is below 1.0"):
        cacheable_chart_state_to_century_record(
            cacheable,
            required_registry=conditional,
        )

    complete = cacheable_chart_state_to_century_record(cacheable)
    missing_payload = complete.model_dump(mode="python")
    missing_payload["feature_values"] = tuple(complete.feature_values[:-1])
    missing_row = type(complete).model_validate(missing_payload, strict=True)
    with pytest.raises(
        CenturyCacheParquetError,
        match="missing=.*incarnation_cross.cardinal_components",
    ):
        validate_row_features(missing_row, CACHEABLE_M0_M2_FEATURE_COLUMNS)


def test_m2_serialization_rejects_mean_node_provider_before_vector_creation(
    tmp_path: Path,
) -> None:
    provider, _ = _verified_fixture(
        tmp_path,
        node_convention=NodeConvention.MEAN,
    )
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    computation = calculate_chart(provider, birth)

    with pytest.raises(FeatureCoverageError, match="true-Node convention"):
        serialize_cacheable_chart_state(
            computation,
            provider=provider,
            utc_start=birth,
            utc_end=birth + timedelta(minutes=1),
        )
