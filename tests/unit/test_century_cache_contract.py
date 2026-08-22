from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pyarrow.parquet as pq
import pytest

from hdmatch.century_cache import (
    CenturyCacheBuildError,
    CenturyCacheBuildSpec,
    CenturyCacheEngineProvenance,
    CenturyCacheExpectations,
    CenturyCacheRecoveryError,
    CenturyCacheShardInput,
    CenturyCacheVerificationError,
    CenturyStateRecord,
    FeatureColumnSpec,
    FeatureStorageType,
    FeatureValue,
    canonical_rows_sha256,
    coerce_century_state_record,
    feature_registry_sha256,
    iter_verified_century_cache_rows,
    open_century_cache_for_recovery,
    required_feature_ids_sha256,
    verify_century_cache,
    write_century_cache_explicit,
)
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_file, sha256_json
from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_REPOSITORY,
    VerifiedEphemerisFile,
    VerifiedEphemerisProvenance,
)

_HASH = "a" * 64
_START = datetime(2000, 1, 1, tzinfo=UTC)
_END = _START + timedelta(hours=2)


def _registry() -> tuple[FeatureColumnSpec, ...]:
    return (
        FeatureColumnSpec(
            feature_id="activation.design",
            storage_type=FeatureStorageType.ACTIVATION_LIST,
        ),
        FeatureColumnSpec(
            feature_id="architecture.type",
            storage_type=FeatureStorageType.STRING,
        ),
        FeatureColumnSpec(
            feature_id="centers.defined",
            storage_type=FeatureStorageType.STRING_LIST,
        ),
        FeatureColumnSpec(
            feature_id="predicate.contextual",
            storage_type=FeatureStorageType.BOOLEAN,
            nullable=True,
        ),
    )


def _ephemeris_provenance() -> VerifiedEphemerisProvenance:
    files = (
        VerifiedEphemerisFile(name="sepl_18.se1", bytes=484061, sha256="1" * 64),
        VerifiedEphemerisFile(name="semo_18.se1", bytes=1304771, sha256="2" * 64),
    )
    return VerifiedEphemerisProvenance(
        source_repository=PINNED_UPSTREAM_REPOSITORY,
        source_commit=PINNED_UPSTREAM_COMMIT,
        source_manifest_sha256="3" * 64,
        files=files,
        ephemeris_file_set_sha256=sha256_json(
            [item.model_dump(mode="json") for item in files]
        ),
    )


def _engine() -> CenturyCacheEngineProvenance:
    return CenturyCacheEngineProvenance(
        provider="swiss_ephemeris_local_files",
        chart_engine_version="chart-engine-v4.3-test",
        swiss_library_version="2.10.03",
        engine_validation_sha256="4" * 64,
        ephemeris_provenance=_ephemeris_provenance(),
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        requested_flags=258,
        returned_flags_observed=(258,),
        ephemeris_mask=7,
        swieph_flag=2,
    )


def _spec() -> CenturyCacheBuildSpec:
    registry = _registry()
    return CenturyCacheBuildSpec(
        feature_vector_schema_version="v4.3-m2-fixture-v1",
        utc_start=_START,
        utc_end_exclusive=_END,
        feature_registry=registry,
        feature_registry_sha256=feature_registry_sha256(registry),
        required_feature_coverage=1.0,
        calculation_tier="M2",
        exact_intervals=True,
        engine=_engine(),
        node_convention="true",
        mandala_mapping_version="rave-mandala-v1",
        mandala_mapping_sha256="5" * 64,
        bodygraph_mapping_sha256="b" * 64,
        boundary_policy_version="exact-boundaries-v4.3-test",
        design_root_time_tolerance_seconds=0.01,
        design_root_arc_tolerance_degrees=1e-8,
        parity_status="pass",
        parity_report_sha256="6" * 64,
        boundary_audit_status="pass",
        boundary_audit_report_sha256="7" * 64,
        generation_commit="8" * 40,
        created_at_utc=datetime(2026, 8, 22, tzinfo=UTC),
    )


def _activation(gate: int) -> dict[str, object]:
    return {
        "body": "sun",
        "side": "design",
        "gate": gate,
        "line": 1,
        "color": None,
        "tone": None,
        "base": None,
    }


def _row(index: int, *, include_contextual: bool = True) -> CenturyStateRecord:
    spec = _spec()
    start = _START + timedelta(hours=index)
    values = [
        FeatureValue(feature_id="activation.design", value=[_activation(index + 1)]),
        FeatureValue(feature_id="architecture.type", value="projector"),
        FeatureValue(feature_id="centers.defined", value=["Ajna", "Throat"]),
    ]
    if include_contextual:
        values.append(FeatureValue(feature_id="predicate.contextual", value=None))
    return CenturyStateRecord(
        state_id=f"state-{index}",
        utc_start=start,
        utc_end=start + timedelta(hours=1),
        duration_seconds=3600.0,
        representative_utc=start + timedelta(minutes=30),
        design_timestamp=start - timedelta(days=88),
        chart_features_sha256=("c" * 63) + str(index),
        feature_vector_schema_version=spec.feature_vector_schema_version,
        feature_registry_sha256=spec.feature_registry_sha256,
        astronomy_engine_version=spec.engine.chart_engine_version,
        ephemeris_file_set_sha256=(
            spec.engine.ephemeris_provenance.ephemeris_file_set_sha256
        ),
        node_convention="true",
        mandala_mapping_version=spec.mandala_mapping_version,
        mandala_mapping_sha256=spec.mandala_mapping_sha256,
        bodygraph_mapping_sha256=spec.bodygraph_mapping_sha256,
        boundary_events=(f"boundary.event.{index}",),
        feature_values=tuple(values),
    )


def _expectations(*, required: tuple[str, ...] | None = None) -> CenturyCacheExpectations:
    spec = _spec()
    identifiers = required or tuple(item.feature_id for item in spec.feature_registry)
    return CenturyCacheExpectations(
        utc_start=spec.utc_start,
        utc_end_exclusive=spec.utc_end_exclusive,
        feature_vector_schema_version=spec.feature_vector_schema_version,
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
        boundary_audit_report_sha256=spec.boundary_audit_report_sha256,
    )


def _write_fixture(directory: Path, *, one_shard: bool = False) -> Any:
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
        spec=_spec(),
        shards=shards,
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
    assert rows[0].representative_utc == _START + timedelta(minutes=30)
    assert rows[0].chart_features_sha256 == ("c" * 63) + "0"
    assert rows[0].bodygraph_mapping_sha256 == "b" * 64
    assert rows[0].boundary_events == ("boundary.event.0",)


def test_protocol_adapter_accepts_a_canonical_mapping() -> None:
    row = _row(0)

    class Source:
        def to_century_cache_mapping(self) -> dict[str, object]:
            return row.model_dump(mode="python")

    assert coerce_century_state_record(Source()) == row
    assert coerce_century_state_record(row.model_dump(mode="python")) == row


def test_missing_nullable_feature_is_not_silently_false(tmp_path: Path) -> None:
    missing = _row(0, include_contextual=False)
    complete = _row(1)
    with pytest.raises(CenturyCacheBuildError, match="missing=.*predicate.contextual"):
        write_century_cache_explicit(
            tmp_path / "missing",
            spec=_spec(),
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(missing, complete),
                ),
            ),
            build_mode="explicit_rebuild",
        )

    verified = _write_fixture(tmp_path / "complete")
    first = next(iter_verified_century_cache_rows(verified))
    assert first.feature_mapping()["predicate.contextual"] is None


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
    with pytest.raises(CenturyCacheBuildError, match="bodygraph_mapping_sha256"):
        write_century_cache_explicit(
            tmp_path / "bodygraph-mismatch",
            spec=_spec(),
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(mismatched, _row(1)),
                ),
            ),
            build_mode="explicit_rebuild",
        )


def test_shard_byte_tampering_fails_closed(tmp_path: Path) -> None:
    verified = _write_fixture(tmp_path / "cache")
    shard = verified.cache_directory / verified.manifest.shards[0].filename
    shard.write_bytes(shard.read_bytes() + b"tamper")

    with pytest.raises(CenturyCacheVerificationError, match="SHA-256 mismatch"):
        verify_century_cache(verified.cache_directory, expectations=_expectations())


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
            shards=(
                CenturyCacheShardInput(
                    filename="states-0000.parquet.zst",
                    rows=(_row(0), _row(1)),
                ),
            ),
            build_mode=cast(Any, "ordinary_recovery"),
        )
    assert not (tmp_path / "wrong-mode").exists()


def test_verified_handle_detects_manifest_change_before_yield(tmp_path: Path) -> None:
    verified = _write_fixture(tmp_path / "cache")
    verified.manifest_path.write_bytes(verified.manifest_path.read_bytes() + b"\n")

    with pytest.raises(CenturyCacheVerificationError, match="changed after verification"):
        tuple(iter_verified_century_cache_rows(verified))
