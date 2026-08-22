from __future__ import annotations

import json
import tempfile
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from functools import cache
from pathlib import Path
from typing import Any, cast

import pyarrow.parquet as pq
import pytest

from hdmatch.century_cache import (
    CACHEABLE_M0_M2_FEATURE_COLUMNS,
    CenturyCacheBuildError,
    CenturyCacheBuildSpec,
    CenturyCacheEngineProvenance,
    CenturyCacheEvidenceInputs,
    CenturyCacheExpectations,
    CenturyCacheRecoveryError,
    CenturyCacheShardInput,
    CenturyCacheVerificationError,
    CenturyStateRecord,
    FeatureColumnSpec,
    VerifiedExactShardSet,
    VerifiedExactStateBatch,
    assemble_verified_exact_shard_set,
    build_verified_exact_state_batch,
    canonical_rows_sha256,
    coerce_century_state_record,
    feature_registry_sha256,
    iter_verified_century_cache_rows,
    open_century_cache_for_recovery,
    required_feature_ids_sha256,
    validate_engine_validation_evidence,
    verify_century_cache,
    write_century_cache_explicit,
    write_noncanonical_century_cache_fixture,
)
from hdmatch.chart.ephemeris import SwissEphemerisProvider
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    sha256_json,
)
from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_REPOSITORY,
    VerifiedEphemerisFile,
    VerifiedEphemerisProvenance,
)

_HASH = "a" * 64
_ROOT = Path(__file__).resolve().parents[2]
_START = datetime(2000, 1, 1, 12, tzinfo=UTC)
_END = _START + timedelta(minutes=1)
_EPHEMERIS_BYTES = {
    "sepl_18.se1": b"fixture planetary ephemeris",
    "semo_18.se1": b"fixture lunar ephemeris",
}


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

    def julday(
        self,
        year: int,
        month: int,
        day: int,
        hour: float,
        _calendar: int,
    ) -> float:
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


@cache
def _exact_batch() -> VerifiedExactStateBatch:
    root = Path(tempfile.mkdtemp(prefix="hdmatch-exact-cache-test-"))
    ephemeris = root / "ephemeris"
    ephemeris.mkdir()
    files = []
    for name, payload in _EPHEMERIS_BYTES.items():
        path = ephemeris / name
        path.write_bytes(payload)
        files.append(path)
    fake = _DeterministicFakeSwiss(files[0], files[1])
    provider = SwissEphemerisProvider(
        tuple(files),
        _swe_module=fake,  # type: ignore[arg-type]
    )
    batch = build_verified_exact_state_batch(provider, _START, _END)
    assert len(batch.rows) == 2
    return batch


@cache
def _exact_shard_set() -> VerifiedExactShardSet:
    return assemble_verified_exact_shard_set((_exact_batch(),))


def _source_manifest_payload(
    *, upstream_commit: str = PINNED_UPSTREAM_COMMIT
) -> dict[str, object]:
    return {
        "schema_version": "ephemeris-file-manifest-v1",
        "provider": "Swiss Ephemeris",
        "upstream_repository": PINNED_UPSTREAM_REPOSITORY,
        "upstream_commit": upstream_commit,
        "files": [
            {
                "name": name,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
            }
            for name, payload in _EPHEMERIS_BYTES.items()
        ],
        "tested_range": "fixture-only",
        "license": "fixture-only",
    }


def _registry() -> tuple[FeatureColumnSpec, ...]:
    return CACHEABLE_M0_M2_FEATURE_COLUMNS


def _ephemeris_provenance() -> VerifiedEphemerisProvenance:
    files = (
        VerifiedEphemerisFile(
            name="sepl_18.se1",
            bytes=len(_EPHEMERIS_BYTES["sepl_18.se1"]),
            sha256=sha256_bytes(_EPHEMERIS_BYTES["sepl_18.se1"]),
        ),
        VerifiedEphemerisFile(
            name="semo_18.se1",
            bytes=len(_EPHEMERIS_BYTES["semo_18.se1"]),
            sha256=sha256_bytes(_EPHEMERIS_BYTES["semo_18.se1"]),
        ),
    )
    return VerifiedEphemerisProvenance(
        source_repository=PINNED_UPSTREAM_REPOSITORY,
        source_commit=PINNED_UPSTREAM_COMMIT,
        source_manifest_sha256=sha256_json(_source_manifest_payload()),
        files=files,
        ephemeris_file_set_sha256=sha256_json(
            [item.model_dump(mode="json") for item in files]
        ),
    )


def _engine_receipt_payload() -> dict[str, object]:
    provenance = _ephemeris_provenance()
    files_by_name = {item.name: item for item in provenance.files}
    probes = []
    for body, filename in (("sun", "sepl_18.se1"), ("moon", "semo_18.se1")):
        probes.append(
            {
                "at_utc": _START,
                "body": body,
                "longitude": 0.0,
                "speed_degrees_per_day": 1.0,
                "gate": 41,
                "line": 1,
                "requested_mode": "SWIEPH",
                "returned_mode": "SWIEPH",
                "requested_flags": 258,
                "returned_flags": 258,
                "ephemeris_mask": 7,
                "used_file_name": filename,
                "used_file_sha256": files_by_name[filename].sha256,
            }
        )
    return {
        "schema_version": "production-engine-validation-receipt-v1",
        "validation_status": "pass",
        "software_commit": "e" * 40,
        "software_dirty": False,
        "software_environment": {"python_version": "fixture"},
        "ephemeris_mode_argument": "SWIEPH",
        "ephemeris_provenance": provenance.model_dump(mode="json"),
        "engine_validation": {
            "schema_version": "production-engine-validation-v1",
            "validation_status": "pass",
            "provider": "swiss_ephemeris_local_files",
            "library_version": "deterministic-fake",
            "ephemeris_requested": "SWIEPH",
            "ephemeris_returned": "SWIEPH",
            "requested_flags": 258,
            "ephemeris_mask": 7,
            "files": [
                {
                    "name": item.name,
                    "sha256": item.sha256,
                    "size_bytes": item.bytes,
                }
                for item in reversed(provenance.files)
            ],
            "calculation_probes": probes,
            "design_root_probes": [
                {
                    "personality_utc": _START,
                    "design_utc": _START - timedelta(days=88),
                    "target_arc_degrees": 88.0,
                    "solved_arc_degrees": 88.0,
                    "residual_degrees": 0.0,
                    "time_tolerance_seconds": 0.01,
                    "arc_tolerance_degrees": 1e-8,
                }
            ],
            "gate_line_deterministic": True,
            "design_root_converged": True,
            "node_convention": "true",
        },
        "claim_boundary": (
            "astronomy-engine-phase-0-only-not-a-v4-3-cache-or-behavioral-result"
        ),
    }


def _engine() -> CenturyCacheEngineProvenance:
    exact = _exact_batch().provenance
    return CenturyCacheEngineProvenance(
        provider="swiss_ephemeris_local_files",
        chart_engine_version=exact.chart_engine_version,
        swiss_library_version="deterministic-fake",
        engine_validation_sha256=sha256_json(_engine_receipt_payload()),
        ephemeris_provenance=_ephemeris_provenance(),
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        requested_flags=258,
        returned_flags_observed=(258,),
        ephemeris_mask=7,
        swieph_flag=2,
    )


def _parity_report_payload() -> dict[str, object]:
    return {
        "schema_version": "century-cache-parity-report-v1",
        "validation_status": "pass",
        "engine_validation_sha256": _engine().engine_validation_sha256,
        "ephemeris_file_set_sha256": _ephemeris_provenance().ephemeris_file_set_sha256,
        "feature_vector_schema_version": (
            _exact_batch().provenance.feature_vector_schema_version
        ),
        "utc_start": _START,
        "utc_end_exclusive": _END,
        "reference_source_locator": (
            "tests/golden/fixtures/swieph_phase0_golden_v1.json"
        ),
        "reference_source_sha256": sha256_file(
            _ROOT / "tests/golden/fixtures/swieph_phase0_golden_v1.json"
        ),
        "comparison_count": 2,
        "mismatch_count": 0,
        "tolerance_degrees": 1e-8,
        "max_abs_longitude_error_degrees": 0.0,
    }


def _boundary_audit_payload() -> dict[str, object]:
    exact = _exact_batch().provenance
    return {
        "schema_version": "century-cache-boundary-audit-report-v1",
        "validation_status": "pass",
        "engine_validation_sha256": _engine().engine_validation_sha256,
        "logical_universe_sha256": exact.logical_universe_sha256,
        "semantic_feature_registry_sha256": exact.semantic_feature_registry_sha256,
        "feature_registry_sha256": exact.feature_registry_sha256,
        "mandala_mapping_sha256": exact.mandala_mapping_sha256,
        "bodygraph_mapping_sha256": exact.bodygraph_mapping_sha256,
        "boundary_policy_version": exact.boundary_policy_version,
        "design_root_time_tolerance_seconds": (
            exact.design_root_time_tolerance_seconds
        ),
        "design_root_arc_tolerance_degrees": (
            exact.design_root_arc_tolerance_degrees
        ),
        "utc_start": _START,
        "utc_end_exclusive": _END,
        "interval_count": exact.interval_count,
        "audited_boundary_event_count": exact.boundary_event_count,
        "missing_boundary_count": 0,
        "gap_count": 0,
        "overlap_count": 0,
        "maximality_violation_count": 0,
    }


def _spec() -> CenturyCacheBuildSpec:
    registry = _registry()
    exact = _exact_batch().provenance
    return CenturyCacheBuildSpec(
        feature_vector_schema_version=exact.feature_vector_schema_version,
        utc_start=_START,
        utc_end_exclusive=_END,
        feature_registry=registry,
        semantic_feature_registry_sha256=exact.semantic_feature_registry_sha256,
        feature_registry_sha256=feature_registry_sha256(registry),
        required_feature_coverage=1.0,
        calculation_tier="M2",
        exact_intervals=True,
        engine=_engine(),
        node_convention="true",
        mandala_mapping_version=exact.mandala_mapping_version,
        mandala_mapping_sha256=exact.mandala_mapping_sha256,
        bodygraph_mapping_sha256=exact.bodygraph_mapping_sha256,
        boundary_policy_version=exact.boundary_policy_version,
        design_root_time_tolerance_seconds=exact.design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=exact.design_root_arc_tolerance_degrees,
        parity_status="pass",
        parity_report_sha256=sha256_json(_parity_report_payload()),
        parity_reference_source_locator=(
            "tests/golden/fixtures/swieph_phase0_golden_v1.json"
        ),
        parity_reference_source_sha256=sha256_file(
            _ROOT / "tests/golden/fixtures/swieph_phase0_golden_v1.json"
        ),
        boundary_audit_status="pass",
        boundary_audit_report_sha256=sha256_json(_boundary_audit_payload()),
        generation_commit="8" * 40,
        created_at_utc=datetime(2026, 8, 22, tzinfo=UTC),
    )


def _row(index: int) -> CenturyStateRecord:
    return _exact_batch().rows[index]


def _expectations(*, required: tuple[str, ...] | None = None) -> CenturyCacheExpectations:
    spec = _spec()
    identifiers = required or tuple(item.feature_id for item in spec.feature_registry)
    return CenturyCacheExpectations(
        utc_start=spec.utc_start,
        utc_end_exclusive=spec.utc_end_exclusive,
        feature_vector_schema_version=spec.feature_vector_schema_version,
        semantic_feature_registry_sha256=spec.semantic_feature_registry_sha256,
        cache_feature_registry_sha256=spec.feature_registry_sha256,
        required_feature_ids=identifiers,
        required_feature_registry_sha256=required_feature_ids_sha256(identifiers),
        engine_validation_sha256=spec.engine.engine_validation_sha256,
        ephemeris_source_manifest_sha256=(
            spec.engine.ephemeris_provenance.source_manifest_sha256
        ),
        ephemeris_file_set_sha256=(
            spec.engine.ephemeris_provenance.ephemeris_file_set_sha256
        ),
        mandala_mapping_sha256=spec.mandala_mapping_sha256,
        bodygraph_mapping_sha256=spec.bodygraph_mapping_sha256,
        boundary_policy_version=spec.boundary_policy_version,
        design_root_time_tolerance_seconds=spec.design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=spec.design_root_arc_tolerance_degrees,
        parity_report_sha256=spec.parity_report_sha256,
        parity_reference_source_locator=spec.parity_reference_source_locator,
        parity_reference_source_sha256=spec.parity_reference_source_sha256,
        boundary_audit_report_sha256=spec.boundary_audit_report_sha256,
    )


def _evidence_inputs(
    directory: Path,
    *,
    engine_payload: dict[str, object] | None = None,
    parity_payload: dict[str, object] | None = None,
    boundary_payload: dict[str, object] | None = None,
    source_manifest_payload: dict[str, object] | None = None,
) -> CenturyCacheEvidenceInputs:
    directory.mkdir(parents=True)
    ephemeris = directory / "ephemeris"
    ephemeris.mkdir()
    for name, payload in _EPHEMERIS_BYTES.items():
        (ephemeris / name).write_bytes(payload)
    source_manifest = directory / "ephemeris-source-manifest.json"
    source_manifest.write_bytes(
        canonical_json_bytes(source_manifest_payload or _source_manifest_payload())
    )
    engine_path = directory / "engine-validation.json"
    parity_path = directory / "parity-report.json"
    boundary_path = directory / "boundary-audit-report.json"
    engine_path.write_bytes(canonical_json_bytes(engine_payload or _engine_receipt_payload()))
    parity_path.write_bytes(canonical_json_bytes(parity_payload or _parity_report_payload()))
    boundary_path.write_bytes(
        canonical_json_bytes(boundary_payload or _boundary_audit_payload())
    )
    return CenturyCacheEvidenceInputs(
        engine_validation_path=engine_path,
        parity_report_path=parity_path,
        boundary_audit_report_path=boundary_path,
        parity_reference_source_path=(
            _ROOT / "tests/golden/fixtures/swieph_phase0_golden_v1.json"
        ),
        ephemeris_source_manifest_path=source_manifest,
        ephemeris_directory=ephemeris,
    )


def _write_fixture(
    directory: Path,
    *,
    one_shard: bool = False,
    spec: CenturyCacheBuildSpec | None = None,
    evidence: CenturyCacheEvidenceInputs | None = None,
) -> Any:
    rows = (_row(0), _row(1))
    shards = (
        (
            CenturyCacheShardInput(
                filename="states-0000.parquet.zst",
                rows=rows,
            ),
        )
        if one_shard
        else (
            CenturyCacheShardInput(
                filename="states-0000.parquet.zst",
                rows=(rows[0],),
            ),
            CenturyCacheShardInput(
                filename="states-0001.parquet.zst",
                rows=(rows[1],),
            ),
        )
    )
    return write_century_cache_explicit(
        directory,
        spec=spec or _spec(),
        exact_shard_set=_exact_shard_set(),
        shards=shards,
        evidence=evidence or _evidence_inputs(directory.parent / f"{directory.name}-inputs"),
        build_mode="explicit_rebuild",
    )


def _mutate_manifest(directory: Path, mutation: str) -> None:
    path = directory / "manifest.json"
    payload = json.loads(path.read_bytes())
    if mutation == "coverage":
        payload["required_feature_coverage"] = 0.5
    elif mutation == "parity":
        payload["parity_status"] = "fail"
    elif mutation == "boundary":
        payload["boundary_audit_status"] = "fail"
    elif mutation == "returned-mode":
        payload["engine"]["ephemeris_returned"] = "MOSHIER"
    elif mutation == "returned-flags":
        payload["engine"]["returned_flags_observed"] = [260]
    elif mutation == "row-count":
        payload["shards"][0]["row_count"] += 1
        payload["interval_count"] += 1
    elif mutation == "logical-hash":
        payload["logical_universe_sha256"] = "0" * 64
    else:  # pragma: no cover - protects test helper additions
        raise AssertionError(mutation)
    path.write_bytes(canonical_json_bytes(payload))


def test_small_parquet_round_trip_and_shard_independent_logical_hash(
    tmp_path: Path,
) -> None:
    two_shards = _write_fixture(tmp_path / "two")
    one_shard = _write_fixture(tmp_path / "one", one_shard=True)

    rows = tuple(iter_verified_century_cache_rows(two_shards))
    assert rows == (_row(0), _row(1))
    assert two_shards.required_feature_coverage == 1.0
    assert two_shards.manifest.logical_universe_sha256 == canonical_rows_sha256(rows)
    assert (
        two_shards.manifest.logical_universe_sha256
        == one_shard.manifest.logical_universe_sha256
    )
    parquet_file = pq.ParquetFile(tmp_path / "two/states-0000.parquet.zst")
    compressions = {
        parquet_file.metadata.row_group(group).column(column).compression
        for group in range(parquet_file.metadata.num_row_groups)
        for column in range(parquet_file.metadata.row_group(group).num_columns)
    }
    assert compressions == {"ZSTD"}
    assert rows[0].representative_utc == (
        rows[0].utc_start + (rows[0].utc_end - rows[0].utc_start) / 2
    )
    assert rows[0].bodygraph_mapping_sha256 == (
        _exact_batch().provenance.bodygraph_mapping_sha256
    )
    assert any(row.boundary_events for row in rows)


def test_protocol_adapter_accepts_a_canonical_mapping() -> None:
    row = _row(0)

    class Source:
        def to_century_cache_mapping(self) -> dict[str, object]:
            return row.model_dump(mode="python")

    assert coerce_century_state_record(Source()) == row
    assert coerce_century_state_record(row.model_dump(mode="python")) == row


def test_missing_feature_is_not_silently_false(tmp_path: Path) -> None:
    payload = _row(0).model_dump(mode="python")
    payload["feature_values"] = tuple(_row(0).feature_values[:-1])
    missing = CenturyStateRecord.model_validate(payload, strict=True)
    with pytest.raises(CenturyCacheBuildError, match="missing="):
        write_noncanonical_century_cache_fixture(
            tmp_path / "missing",
            registry=CACHEABLE_M0_M2_FEATURE_COLUMNS,
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(missing,),
                ),
            ),
            fixture_mode="noncanonical_fixture",
        )

    assert all(value is not None for value in _row(0).feature_mapping().values())


def test_noncanonical_fixture_writer_cannot_emit_verified_cache(tmp_path: Path) -> None:
    fixture = write_noncanonical_century_cache_fixture(
        tmp_path / "physical-only",
        registry=CACHEABLE_M0_M2_FEATURE_COLUMNS,
        shards=(
            CenturyCacheShardInput(
                filename="states-0000.parquet.zst",
                rows=(_row(0),),
            ),
        ),
        fixture_mode="noncanonical_fixture",
    )

    assert fixture.shard_paths[0].is_file()
    assert not (fixture.cache_directory / "manifest.json").exists()
    with pytest.raises(CenturyCacheRecoveryError, match="prebuilt verified"):
        open_century_cache_for_recovery(
            fixture.cache_directory,
            expectations=_expectations(),
        )


def test_fixed_interval_metadata_is_validated_before_write(tmp_path: Path) -> None:
    row = _row(0)
    outside = row.model_dump(mode="python")
    outside["representative_utc"] = row.utc_end
    with pytest.raises(ValueError, match="representative_utc"):
        CenturyStateRecord.model_validate(outside, strict=True)

    noncanonical_events = row.model_dump(mode="python")
    noncanonical_events["boundary_events"] = (
        "boundary.z",
        "boundary.a",
    )
    with pytest.raises(ValueError, match="sorted and unique"):
        CenturyStateRecord.model_validate(noncanonical_events, strict=True)

    changed_bodygraph = row.model_dump(mode="python")
    changed_bodygraph["bodygraph_mapping_sha256"] = "d" * 64
    mismatched = CenturyStateRecord.model_validate(changed_bodygraph, strict=True)
    with pytest.raises(CenturyCacheBuildError, match="differ from the factory-created"):
        write_century_cache_explicit(
            tmp_path / "bodygraph-mismatch",
            spec=_spec(),
            exact_shard_set=_exact_shard_set(),
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(mismatched, _row(1)),
                ),
            ),
            evidence=_evidence_inputs(tmp_path / "bodygraph-mismatch-inputs"),
            build_mode="explicit_rebuild",
        )


def test_adjacent_identical_states_split_across_shards_are_rejected(
    tmp_path: Path,
) -> None:
    first = _row(0)
    second_payload = _row(1).model_dump(mode="python")
    second_payload["feature_values"] = first.feature_values
    # A substituted declared hash or different boundary label must not hide that
    # the two rows have identical discrete chart content and should be merged.
    second = CenturyStateRecord.model_validate(second_payload, strict=True)

    with pytest.raises(CenturyCacheBuildError, match="differ from the factory-created"):
        write_century_cache_explicit(
            tmp_path / "non-maximal",
            spec=_spec(),
            exact_shard_set=_exact_shard_set(),
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(first,),
                ),
                CenturyCacheShardInput(
                    filename="states-0001.parquet.zst",
                    rows=(second,),
                ),
            ),
            evidence=_evidence_inputs(tmp_path / "non-maximal-inputs"),
            build_mode="explicit_rebuild",
        )


def test_writer_rehashes_actual_ephemeris_and_rejects_fabricated_provenance(
    tmp_path: Path,
) -> None:
    actual = _ephemeris_provenance()
    fabricated = actual.model_copy(update={"source_manifest_sha256": "f" * 64})
    spec = _spec()
    engine = spec.engine.model_copy(update={"ephemeris_provenance": fabricated})
    fabricated_spec = spec.model_copy(update={"engine": engine})

    with pytest.raises(CenturyCacheBuildError, match="actual Swiss Ephemeris"):
        _write_fixture(
            tmp_path / "fabricated",
            spec=fabricated_spec,
            evidence=_evidence_inputs(tmp_path / "fabricated-inputs"),
        )


def test_repository_phase0_engine_receipt_is_semantically_valid() -> None:
    path = _ROOT / "reports/v4_3_migration/phase0_engine_validation.json"
    payload = json.loads(path.read_bytes())
    validation = cast(dict[str, Any], payload["engine_validation"])
    provenance = VerifiedEphemerisProvenance.model_validate_json(
        canonical_json_bytes(payload["ephemeris_provenance"]), strict=True
    )
    engine = CenturyCacheEngineProvenance(
        provider="swiss_ephemeris_local_files",
        chart_engine_version="phase0-exact-chart-adapter",
        swiss_library_version=cast(str, validation["library_version"]),
        engine_validation_sha256=sha256_file(path),
        ephemeris_provenance=provenance,
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        requested_flags=cast(int, validation["requested_flags"]),
        returned_flags_observed=tuple(
            sorted(
                {
                    cast(int, probe["returned_flags"])
                    for probe in cast(list[dict[str, Any]], validation["calculation_probes"])
                }
            )
        ),
        ephemeris_mask=cast(int, validation["ephemeris_mask"]),
        swieph_flag=2,
    )
    first_root = cast(list[dict[str, Any]], validation["design_root_probes"])[0]
    spec = _spec().model_copy(
        update={
            "engine": engine,
            "design_root_time_tolerance_seconds": first_root[
                "time_tolerance_seconds"
            ],
            "design_root_arc_tolerance_degrees": first_root[
                "arc_tolerance_degrees"
            ],
        }
    )

    receipt = validate_engine_validation_evidence(path, spec=spec)

    assert receipt.validation_status == "pass"
    assert receipt.ephemeris_provenance == provenance
    assert len(receipt.engine_validation.calculation_probes) == 33
    assert len(receipt.engine_validation.design_root_probes) == 3


def test_writer_rejects_noncanonical_ephemeris_source_pin(tmp_path: Path) -> None:
    inputs = _evidence_inputs(
        tmp_path / "wrong-pin-inputs",
        source_manifest_payload=_source_manifest_payload(upstream_commit="0" * 40),
    )

    with pytest.raises(CenturyCacheBuildError, match="source verification failed"):
        _write_fixture(tmp_path / "wrong-pin", evidence=inputs)


def test_writer_rejects_missing_or_tampered_proof_artifacts(tmp_path: Path) -> None:
    missing_inputs = _evidence_inputs(tmp_path / "missing-proof-inputs")
    missing_inputs.engine_validation_path.unlink()
    with pytest.raises(CenturyCacheBuildError, match="invalid engine-validation"):
        _write_fixture(tmp_path / "missing-proof", evidence=missing_inputs)

    tampered_inputs = _evidence_inputs(tmp_path / "tampered-proof-inputs")
    tampered_inputs.parity_report_path.write_bytes(
        tampered_inputs.parity_report_path.read_bytes() + b"\n"
    )
    with pytest.raises(CenturyCacheBuildError, match="invalid parity"):
        _write_fixture(tmp_path / "tampered-proof", evidence=tampered_inputs)


def test_writer_rejects_wrong_status_even_when_artifact_hash_is_declared(
    tmp_path: Path,
) -> None:
    failed = {**_parity_report_payload(), "validation_status": "fail"}
    spec = _spec().model_copy(
        update={"parity_report_sha256": sha256_json(failed)}
    )
    inputs = _evidence_inputs(tmp_path / "failed-parity-inputs", parity_payload=failed)

    with pytest.raises(CenturyCacheBuildError, match="invalid parity evidence"):
        _write_fixture(tmp_path / "failed-parity", spec=spec, evidence=inputs)


def test_writer_rejects_semantically_mismatched_proof_with_matching_hash(
    tmp_path: Path,
) -> None:
    mismatched = {
        **_boundary_audit_payload(),
        "logical_universe_sha256": "9" * 64,
    }
    spec = _spec().model_copy(
        update={"boundary_audit_report_sha256": sha256_json(mismatched)}
    )
    inputs = _evidence_inputs(
        tmp_path / "mismatched-boundary-inputs",
        boundary_payload=mismatched,
    )

    with pytest.raises(CenturyCacheBuildError, match="logical-universe hash mismatch"):
        _write_fixture(tmp_path / "mismatched-boundary", spec=spec, evidence=inputs)


def test_writer_binds_boundary_audit_event_count(tmp_path: Path) -> None:
    mismatched = {
        **_boundary_audit_payload(),
        "audited_boundary_event_count": (
            _exact_batch().provenance.boundary_event_count + 1
        ),
    }
    spec = _spec().model_copy(
        update={"boundary_audit_report_sha256": sha256_json(mismatched)}
    )
    inputs = _evidence_inputs(
        tmp_path / "mismatched-event-count-inputs",
        boundary_payload=mismatched,
    )

    with pytest.raises(CenturyCacheBuildError, match="boundary-event count mismatch"):
        _write_fixture(
            tmp_path / "mismatched-event-count",
            spec=spec,
            evidence=inputs,
        )


def test_writer_rejects_boundary_audit_semantic_registry_substitution(
    tmp_path: Path,
) -> None:
    mismatched = {
        **_boundary_audit_payload(),
        "semantic_feature_registry_sha256": "9" * 64,
    }
    spec = _spec().model_copy(
        update={"boundary_audit_report_sha256": sha256_json(mismatched)}
    )
    inputs = _evidence_inputs(
        tmp_path / "mismatched-semantic-registry-inputs",
        boundary_payload=mismatched,
    )

    with pytest.raises(
        CenturyCacheBuildError,
        match="semantic feature-registry hash mismatch",
    ):
        _write_fixture(
            tmp_path / "mismatched-semantic-registry",
            spec=spec,
            evidence=inputs,
        )


def test_writer_rejects_substituted_parity_reference_with_matching_report_hash(
    tmp_path: Path,
) -> None:
    mismatched = {
        **_parity_report_payload(),
        "reference_source_sha256": "9" * 64,
    }
    spec = _spec().model_copy(
        update={"parity_report_sha256": sha256_json(mismatched)}
    )
    inputs = _evidence_inputs(
        tmp_path / "mismatched-parity-reference-inputs",
        parity_payload=mismatched,
    )

    with pytest.raises(CenturyCacheBuildError, match="reference-source hash mismatch"):
        _write_fixture(
            tmp_path / "mismatched-parity-reference",
            spec=spec,
            evidence=inputs,
        )


def test_writer_and_verifier_rehash_bundled_parity_reference_source(
    tmp_path: Path,
) -> None:
    inputs = _evidence_inputs(tmp_path / "tampered-reference-inputs")
    tampered_source = tmp_path / "tampered-reference.json"
    tampered_source.write_bytes(
        (_ROOT / "tests/golden/fixtures/swieph_phase0_golden_v1.json").read_bytes()
        + b"tamper"
    )
    with pytest.raises(CenturyCacheBuildError, match="reference-source artifact SHA-256"):
        _write_fixture(
            tmp_path / "tampered-reference-build",
            evidence=replace(inputs, parity_reference_source_path=tampered_source),
        )

    verified = _write_fixture(tmp_path / "reference-cache")
    bundled = verified.cache_directory / "evidence/parity-reference-source.json"
    bundled.write_bytes(bundled.read_bytes() + b"tamper")
    with pytest.raises(
        CenturyCacheVerificationError,
        match="reference-source artifact SHA-256",
    ):
        verify_century_cache(verified.cache_directory, expectations=_expectations())


def test_writer_rejects_engine_receipt_with_mismatched_ephemeris_binding(
    tmp_path: Path,
) -> None:
    mismatched = _engine_receipt_payload()
    provenance = cast(dict[str, object], mismatched["ephemeris_provenance"])
    mismatched["ephemeris_provenance"] = {
        **provenance,
        "source_manifest_sha256": "9" * 64,
    }
    spec = _spec()
    engine = spec.engine.model_copy(
        update={"engine_validation_sha256": sha256_json(mismatched)}
    )
    spec = spec.model_copy(update={"engine": engine})
    inputs = _evidence_inputs(
        tmp_path / "mismatched-engine-inputs",
        engine_payload=mismatched,
    )

    with pytest.raises(CenturyCacheBuildError, match="ephemeris provenance differs"):
        _write_fixture(tmp_path / "mismatched-engine", spec=spec, evidence=inputs)


def test_shard_byte_tampering_fails_closed(tmp_path: Path) -> None:
    verified = _write_fixture(tmp_path / "cache")
    shard = verified.cache_directory / verified.manifest.shards[0].filename
    shard.write_bytes(shard.read_bytes() + b"tamper")

    with pytest.raises(CenturyCacheVerificationError, match="SHA-256 mismatch"):
        verify_century_cache(verified.cache_directory, expectations=_expectations())


def test_verifier_reopens_bundled_evidence_and_rejects_missing_or_tampered_bytes(
    tmp_path: Path,
) -> None:
    missing = _write_fixture(tmp_path / "missing-cache")
    (missing.cache_directory / "evidence/parity-report.json").unlink()
    with pytest.raises(CenturyCacheVerificationError, match="invalid parity"):
        verify_century_cache(missing.cache_directory, expectations=_expectations())

    tampered = _write_fixture(tmp_path / "tampered-cache")
    parity = tampered.cache_directory / "evidence/parity-report.json"
    parity.write_bytes(parity.read_bytes() + b"\n")
    with pytest.raises(CenturyCacheVerificationError, match="invalid parity"):
        verify_century_cache(tampered.cache_directory, expectations=_expectations())


def test_verifier_semantically_checks_evidence_after_hash_rebinding(
    tmp_path: Path,
) -> None:
    verified = _write_fixture(tmp_path / "cache")
    boundary_path = verified.cache_directory / "evidence/boundary-audit-report.json"
    failed = {
        **json.loads(boundary_path.read_bytes()),
        "validation_status": "fail",
    }
    boundary_path.write_bytes(canonical_json_bytes(failed))
    digest = sha256_file(boundary_path)
    manifest_path = verified.manifest_path
    manifest = json.loads(manifest_path.read_bytes())
    manifest["boundary_audit_report_sha256"] = digest
    for artifact in manifest["evidence_artifacts"]:
        if artifact["kind"] == "boundary_audit":
            artifact["sha256"] = digest
    manifest_path.write_bytes(canonical_json_bytes(manifest))
    expectations = _expectations().model_copy(
        update={"boundary_audit_report_sha256": digest}
    )

    with pytest.raises(CenturyCacheVerificationError, match="invalid boundary-audit"):
        verify_century_cache(verified.cache_directory, expectations=expectations)


@pytest.mark.parametrize(
    "mutation",
    [
        "coverage",
        "parity",
        "boundary",
        "returned-mode",
        "returned-flags",
        "row-count",
        "logical-hash",
    ],
)
def test_manifest_mutations_fail_closed(tmp_path: Path, mutation: str) -> None:
    verified = _write_fixture(tmp_path / "cache")
    _mutate_manifest(verified.cache_directory, mutation)

    with pytest.raises(CenturyCacheVerificationError):
        verify_century_cache(verified.cache_directory, expectations=_expectations())


def test_physical_parquet_schema_mutation_fails_closed(tmp_path: Path) -> None:
    verified = _write_fixture(tmp_path / "cache")
    shard_path = verified.cache_directory / verified.manifest.shards[0].filename
    table = pq.read_table(shard_path)
    reduced = table.drop(["feature::architecture.type"])
    pq.write_table(reduced, shard_path, compression="zstd")

    manifest_path = verified.manifest_path
    payload = json.loads(manifest_path.read_bytes())
    payload["shards"][0]["sha256"] = sha256_file(shard_path)
    manifest_path.write_bytes(canonical_json_bytes(payload))

    with pytest.raises(CenturyCacheVerificationError, match="schema mismatch"):
        verify_century_cache(verified.cache_directory, expectations=_expectations())


def test_required_feature_coverage_is_checked_for_each_recovery(tmp_path: Path) -> None:
    verified = _write_fixture(tmp_path / "cache")
    required = tuple(
        sorted((*_expectations().required_feature_ids, "unavailable.required.feature"))
    )

    with pytest.raises(CenturyCacheVerificationError, match="coverage"):
        verify_century_cache(
            verified.cache_directory,
            expectations=_expectations(required=required),
        )


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    [
        ("cache_feature_registry_sha256", "9" * 64, "cache feature registry mismatch"),
        (
            "semantic_feature_registry_sha256",
            "9" * 64,
            "semantic feature registry mismatch",
        ),
        ("engine_validation_sha256", "9" * 64, "engine validation mismatch"),
        (
            "ephemeris_source_manifest_sha256",
            "9" * 64,
            "ephemeris source manifest mismatch",
        ),
        ("ephemeris_file_set_sha256", "9" * 64, "ephemeris file set mismatch"),
        ("mandala_mapping_sha256", "9" * 64, "Mandala mapping mismatch"),
        ("bodygraph_mapping_sha256", "9" * 64, "Bodygraph mapping mismatch"),
        ("boundary_policy_version", "substituted-policy", "boundary policy mismatch"),
        (
            "design_root_time_tolerance_seconds",
            1.0,
            "Design-root time tolerance mismatch",
        ),
        (
            "design_root_arc_tolerance_degrees",
            1e-4,
            "Design-root arc tolerance mismatch",
        ),
        ("parity_report_sha256", "9" * 64, "parity report mismatch"),
        (
            "parity_reference_source_locator",
            "substituted-reference",
            "parity reference-source locator mismatch",
        ),
        (
            "parity_reference_source_sha256",
            "9" * 64,
            "parity reference-source hash mismatch",
        ),
        (
            "boundary_audit_report_sha256",
            "9" * 64,
            "boundary-audit report mismatch",
        ),
    ],
)
def test_recovery_binds_exact_external_proof_identities(
    tmp_path: Path,
    field: str,
    replacement: object,
    message: str,
) -> None:
    verified = _write_fixture(tmp_path / "cache")
    expectations = _expectations().model_copy(update={field: replacement})

    with pytest.raises(CenturyCacheVerificationError, match=message):
        verify_century_cache(verified.cache_directory, expectations=expectations)


def test_ordinary_recovery_has_no_regeneration_path(tmp_path: Path) -> None:
    missing = tmp_path / "not-built"
    with pytest.raises(CenturyCacheRecoveryError, match="prebuilt verified"):
        open_century_cache_for_recovery(missing, expectations=_expectations())
    assert not missing.exists()

    with pytest.raises(CenturyCacheBuildError, match="explicit_rebuild"):
        write_century_cache_explicit(
            tmp_path / "wrong-mode",
            spec=_spec(),
            exact_shard_set=_exact_shard_set(),
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(_row(0), _row(1)),
                ),
            ),
            evidence=_evidence_inputs(tmp_path / "wrong-mode-inputs"),
            build_mode=cast(Any, "ordinary_recovery"),
        )
    assert not (tmp_path / "wrong-mode").exists()


def test_verified_handle_detects_manifest_change_before_yield(tmp_path: Path) -> None:
    verified = _write_fixture(tmp_path / "cache")
    verified.manifest_path.write_bytes(verified.manifest_path.read_bytes() + b"\n")

    with pytest.raises(CenturyCacheVerificationError, match="changed after verification"):
        tuple(iter_verified_century_cache_rows(verified))
