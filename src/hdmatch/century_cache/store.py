"""Explicit cache writer and fail-closed reader/verifier contracts."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_file,
    write_new_bytes,
    write_new_canonical_json,
)
from hdmatch.provenance.swisseph_files import (
    EphemerisFileVerificationError,
    EphemerisManifestError,
    verify_ephemeris_directory,
)

from .evidence import (
    CenturyCacheEvidenceError,
    CenturyCacheEvidenceInputs,
    validate_bundled_cache_evidence,
    validate_external_cache_evidence,
)
from .models import (
    SHARD_NAME_PATTERN,
    CenturyCacheBuildSpec,
    CenturyCacheExpectations,
    CenturyCacheManifest,
    CenturyCacheShard,
    CenturyStateRecord,
    VerifiedCenturyCache,
    canonical_rows_sha256,
    discrete_chart_identity_sha256,
    parquet_schema_sha256,
    required_feature_ids_sha256,
)
from .parquet import (
    CenturyCacheDependencyError,
    CenturyCacheParquetError,
    read_parquet_shard,
    validate_row_features,
    write_parquet_shard_new,
)


class CenturyCacheBuildError(ValueError):
    """An explicit cache build violates the frozen storage contract."""


class CenturyCacheVerificationError(ValueError):
    """A cache cannot be trusted for ordinary recovery."""


class CenturyCacheRecoveryError(RuntimeError):
    """Ordinary recovery was denied because no verified cache is available."""


@dataclass(frozen=True, slots=True)
class CenturyCacheShardInput:
    """One precomputed shard supplied by the independent boundary workstream."""

    filename: str
    rows: tuple[CenturyStateRecord, ...]

    def __post_init__(self) -> None:
        if re.fullmatch(SHARD_NAME_PATTERN, self.filename) is None:
            raise ValueError("invalid century-cache shard filename")
        if Path(self.filename).name != self.filename:
            raise ValueError("century-cache shard filename must not contain a path")
        if not self.rows:
            raise ValueError("century-cache shard must not be empty")


def _validate_record_metadata(
    row: CenturyStateRecord,
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
) -> None:
    expected = {
        "feature_vector_schema_version": spec.feature_vector_schema_version,
        "semantic_feature_registry_sha256": spec.semantic_feature_registry_sha256,
        "feature_registry_sha256": spec.feature_registry_sha256,
        "astronomy_engine_version": spec.engine.chart_engine_version,
        "ephemeris_file_set_sha256": (
            spec.engine.ephemeris_provenance.ephemeris_file_set_sha256
        ),
        "node_convention": spec.node_convention,
        "mandala_mapping_version": spec.mandala_mapping_version,
        "mandala_mapping_sha256": spec.mandala_mapping_sha256,
        "bodygraph_mapping_sha256": spec.bodygraph_mapping_sha256,
    }
    for field, value in expected.items():
        if getattr(row, field) != value:
            raise ValueError(f"row {row.state_id} has mismatched {field}")
    validate_row_features(row, spec.feature_registry)


def _validate_logical_universe(
    rows: tuple[CenturyStateRecord, ...],
    spec: CenturyCacheBuildSpec | CenturyCacheManifest,
) -> None:
    if not rows:
        raise ValueError("century cache must contain at least one interval")
    if rows[0].utc_start != spec.utc_start:
        raise ValueError("first cache interval does not start at the declared universe start")
    if rows[-1].utc_end != spec.utc_end_exclusive:
        raise ValueError("last cache interval does not end at the declared universe end")
    identities = tuple(row.state_id for row in rows)
    if len(set(identities)) != len(identities):
        raise ValueError("century cache contains duplicate state IDs")
    ordering = tuple((row.utc_start, row.state_id) for row in rows)
    if ordering != tuple(sorted(ordering)):
        raise ValueError("century-cache rows are not in canonical UTC/state order")
    for row in rows:
        _validate_record_metadata(row, spec)
    for previous, current in zip(rows, rows[1:], strict=False):
        if previous.utc_end != current.utc_start:
            raise ValueError("century-cache intervals contain a gap or overlap")
        if discrete_chart_identity_sha256(previous) == discrete_chart_identity_sha256(
            current
        ):
            raise ValueError(
                "century-cache intervals are not maximal: adjacent rows have the "
                "same discrete chart identity"
            )


def _expectations_for_spec(spec: CenturyCacheBuildSpec) -> CenturyCacheExpectations:
    feature_ids = tuple(item.feature_id for item in spec.feature_registry)
    return CenturyCacheExpectations(
        utc_start=spec.utc_start,
        utc_end_exclusive=spec.utc_end_exclusive,
        feature_vector_schema_version=spec.feature_vector_schema_version,
        semantic_feature_registry_sha256=spec.semantic_feature_registry_sha256,
        cache_feature_registry_sha256=spec.feature_registry_sha256,
        required_feature_ids=feature_ids,
        required_feature_registry_sha256=required_feature_ids_sha256(feature_ids),
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


def write_century_cache_explicit(
    cache_directory: str | Path,
    *,
    spec: CenturyCacheBuildSpec,
    shards: tuple[CenturyCacheShardInput, ...],
    evidence: CenturyCacheEvidenceInputs,
    build_mode: Literal["explicit_rebuild"],
) -> VerifiedCenturyCache:
    """Write supplied exact states; this function never computes astronomy.

    The mandatory ``build_mode`` token makes cache construction an explicit
    operation.  Ordinary recovery has a separate read-only entry point below.
    """

    if build_mode != "explicit_rebuild":
        raise CenturyCacheBuildError(
            "century cache creation requires the explicit_rebuild operation"
        )
    if not shards:
        raise CenturyCacheBuildError("century cache requires at least one shard")
    if tuple(item.filename for item in shards) != tuple(
        sorted(item.filename for item in shards)
    ):
        raise CenturyCacheBuildError("century-cache shard inputs must be filename-sorted")

    rows = tuple(row for shard in shards for row in shard.rows)
    try:
        _validate_logical_universe(rows, spec)
    except (ValueError, CenturyCacheParquetError) as exc:
        raise CenturyCacheBuildError(str(exc)) from exc

    try:
        observed_ephemeris = verify_ephemeris_directory(
            source_manifest_path=evidence.ephemeris_source_manifest_path,
            ephemeris_directory=evidence.ephemeris_directory,
        )
    except (EphemerisManifestError, EphemerisFileVerificationError) as exc:
        raise CenturyCacheBuildError(
            f"Swiss Ephemeris source verification failed: {exc}"
        ) from exc
    if observed_ephemeris != spec.engine.ephemeris_provenance:
        raise CenturyCacheBuildError(
            "actual Swiss Ephemeris source/files differ from the cache engine provenance"
        )

    logical_universe_sha256 = canonical_rows_sha256(rows)
    try:
        validated_evidence = validate_external_cache_evidence(
            evidence,
            spec=spec,
            logical_universe_sha256=logical_universe_sha256,
            interval_count=len(rows),
        )
    except CenturyCacheEvidenceError as exc:
        raise CenturyCacheBuildError(f"cache proof evidence failed: {exc}") from exc

    output = Path(cache_directory)
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.json"
    if manifest_path.exists():
        raise FileExistsError(f"century-cache manifest already exists: {manifest_path}")

    try:
        for filename, raw in validated_evidence.bundled_bytes:
            write_new_bytes(output / filename, raw)
    except (OSError, ValueError) as exc:
        raise CenturyCacheBuildError(f"could not bundle cache proof evidence: {exc}") from exc

    shard_records: list[CenturyCacheShard] = []
    decoded_rows: list[CenturyStateRecord] = []
    schema_sha256 = parquet_schema_sha256(spec.feature_registry)
    try:
        for shard in shards:
            destination = output / shard.filename
            write_parquet_shard_new(destination, shard.rows, spec.feature_registry)
            round_trip = read_parquet_shard(destination, spec.feature_registry)
            if round_trip != shard.rows:
                raise CenturyCacheBuildError(
                    f"Parquet round-trip changed logical rows in {shard.filename}"
                )
            decoded_rows.extend(round_trip)
            shard_records.append(
                CenturyCacheShard(
                    filename=shard.filename,
                    sha256=sha256_file(destination),
                    row_count=len(round_trip),
                    utc_start=round_trip[0].utc_start,
                    utc_end_exclusive=round_trip[-1].utc_end,
                    canonical_rows_sha256=canonical_rows_sha256(round_trip),
                    parquet_schema_sha256=schema_sha256,
                )
            )
    except (OSError, ValueError, CenturyCacheDependencyError, CenturyCacheParquetError) as exc:
        raise CenturyCacheBuildError(f"could not write verified cache shards: {exc}") from exc

    manifest_payload = {
        **spec.model_dump(mode="python", exclude={"schema_version"}),
        "schema_version": "century-cache-manifest-v1",
        "interval_count": len(decoded_rows),
        "evidence_artifacts": validated_evidence.artifacts,
        "shards": tuple(shard_records),
        "logical_universe_sha256": logical_universe_sha256,
        "verification_status": "pass",
    }
    try:
        manifest = CenturyCacheManifest.model_validate(manifest_payload, strict=True)
        write_new_canonical_json(manifest_path, manifest)
    except (OSError, ValueError) as exc:
        raise CenturyCacheBuildError(f"could not finalize cache manifest: {exc}") from exc
    return verify_century_cache(output, expectations=_expectations_for_spec(spec))


def _load_manifest(path: Path) -> CenturyCacheManifest:
    try:
        raw = path.read_bytes()
        parsed = json.loads(raw)
        if canonical_json_bytes(parsed) != raw:
            raise ValueError("manifest is not canonically encoded")
        return CenturyCacheManifest.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise CenturyCacheVerificationError(
            f"invalid century-cache manifest: {path}"
        ) from exc


def _verify_expectations(
    manifest: CenturyCacheManifest, expectations: CenturyCacheExpectations
) -> float:
    if not (
        manifest.utc_start <= expectations.utc_start
        and manifest.utc_end_exclusive >= expectations.utc_end_exclusive
    ):
        raise CenturyCacheVerificationError("cache does not cover the requested UTC range")
    expected_fields = {
        "feature_vector_schema_version": expectations.feature_vector_schema_version,
        "semantic feature registry": expectations.semantic_feature_registry_sha256,
        "cache feature registry": expectations.cache_feature_registry_sha256,
        "engine validation": expectations.engine_validation_sha256,
        "ephemeris source manifest": expectations.ephemeris_source_manifest_sha256,
        "ephemeris file set": expectations.ephemeris_file_set_sha256,
        "Mandala mapping": expectations.mandala_mapping_sha256,
        "Bodygraph mapping": expectations.bodygraph_mapping_sha256,
        "boundary policy": expectations.boundary_policy_version,
        "Design-root time tolerance": expectations.design_root_time_tolerance_seconds,
        "Design-root arc tolerance": expectations.design_root_arc_tolerance_degrees,
        "parity report": expectations.parity_report_sha256,
        "parity reference-source locator": (
            expectations.parity_reference_source_locator
        ),
        "parity reference-source hash": expectations.parity_reference_source_sha256,
        "boundary-audit report": expectations.boundary_audit_report_sha256,
    }
    actual_fields = {
        "feature_vector_schema_version": manifest.feature_vector_schema_version,
        "semantic feature registry": manifest.semantic_feature_registry_sha256,
        "cache feature registry": manifest.feature_registry_sha256,
        "engine validation": manifest.engine.engine_validation_sha256,
        "ephemeris source manifest": (
            manifest.engine.ephemeris_provenance.source_manifest_sha256
        ),
        "ephemeris file set": (
            manifest.engine.ephemeris_provenance.ephemeris_file_set_sha256
        ),
        "Mandala mapping": manifest.mandala_mapping_sha256,
        "Bodygraph mapping": manifest.bodygraph_mapping_sha256,
        "boundary policy": manifest.boundary_policy_version,
        "Design-root time tolerance": manifest.design_root_time_tolerance_seconds,
        "Design-root arc tolerance": manifest.design_root_arc_tolerance_degrees,
        "parity report": manifest.parity_report_sha256,
        "parity reference-source locator": manifest.parity_reference_source_locator,
        "parity reference-source hash": manifest.parity_reference_source_sha256,
        "boundary-audit report": manifest.boundary_audit_report_sha256,
    }
    for name, expected in expected_fields.items():
        if actual_fields[name] != expected:
            raise CenturyCacheVerificationError(f"cache {name} mismatch")

    available = {item.feature_id for item in manifest.feature_registry}
    required = set(expectations.required_feature_ids)
    coverage = len(required & available) / len(required)
    if coverage != 1.0:
        missing = sorted(required - available)
        raise CenturyCacheVerificationError(
            f"cache required feature coverage is {coverage:.6f}; missing={missing}"
        )
    if expectations.required_feature_registry_sha256 != required_feature_ids_sha256(
        expectations.required_feature_ids
    ):
        raise CenturyCacheVerificationError("required feature registry identity changed")
    return coverage


def verify_century_cache(
    cache_directory: str | Path,
    *,
    expectations: CenturyCacheExpectations,
) -> VerifiedCenturyCache:
    """Re-hash, decode, and validate the complete declared exact-state universe."""

    directory = Path(cache_directory)
    manifest_path = directory / "manifest.json"
    manifest = _load_manifest(manifest_path)
    coverage = _verify_expectations(manifest, expectations)
    try:
        validate_bundled_cache_evidence(directory, manifest=manifest)
    except CenturyCacheEvidenceError as exc:
        raise CenturyCacheVerificationError(
            f"cache proof evidence verification failed: {exc}"
        ) from exc
    decoded_rows: list[CenturyStateRecord] = []
    try:
        for shard in manifest.shards:
            shard_path = directory / shard.filename
            if not shard_path.is_file():
                raise CenturyCacheVerificationError(
                    f"cache shard is missing: {shard.filename}"
                )
            if sha256_file(shard_path) != shard.sha256:
                raise CenturyCacheVerificationError(
                    f"cache shard SHA-256 mismatch: {shard.filename}"
                )
            rows = read_parquet_shard(shard_path, manifest.feature_registry)
            if len(rows) != shard.row_count:
                raise CenturyCacheVerificationError(
                    f"cache shard row-count mismatch: {shard.filename}"
                )
            if canonical_rows_sha256(rows) != shard.canonical_rows_sha256:
                raise CenturyCacheVerificationError(
                    f"cache shard logical-row hash mismatch: {shard.filename}"
                )
            if rows[0].utc_start != shard.utc_start or rows[-1].utc_end != (
                shard.utc_end_exclusive
            ):
                raise CenturyCacheVerificationError(
                    f"cache shard UTC bounds mismatch: {shard.filename}"
                )
            decoded_rows.extend(rows)
        logical_rows = tuple(decoded_rows)
        _validate_logical_universe(logical_rows, manifest)
    except (OSError, ValueError, CenturyCacheDependencyError, CenturyCacheParquetError) as exc:
        if isinstance(exc, CenturyCacheVerificationError):
            raise
        raise CenturyCacheVerificationError(f"cache shard verification failed: {exc}") from exc

    if len(decoded_rows) != manifest.interval_count:
        raise CenturyCacheVerificationError("cache interval count mismatch")
    if canonical_rows_sha256(tuple(decoded_rows)) != manifest.logical_universe_sha256:
        raise CenturyCacheVerificationError("cache logical-universe hash mismatch")
    return VerifiedCenturyCache(
        cache_directory=directory,
        manifest_path=manifest_path,
        manifest_sha256=sha256_file(manifest_path),
        manifest=manifest,
        required_feature_coverage=coverage,
    )


def iter_verified_century_cache_rows(
    verified: VerifiedCenturyCache,
) -> Iterator[CenturyStateRecord]:
    """Yield only after each current shard still matches its verified binding."""

    if sha256_file(verified.manifest_path) != verified.manifest_sha256:
        raise CenturyCacheVerificationError("cache manifest changed after verification")
    try:
        validate_bundled_cache_evidence(
            verified.cache_directory,
            manifest=verified.manifest,
        )
    except CenturyCacheEvidenceError as exc:
        raise CenturyCacheVerificationError(
            f"cache proof evidence changed after verification: {exc}"
        ) from exc
    for shard in verified.manifest.shards:
        shard_path = verified.cache_directory / shard.filename
        if sha256_file(shard_path) != shard.sha256:
            raise CenturyCacheVerificationError(
                f"cache shard changed after verification: {shard.filename}"
            )
        rows = read_parquet_shard(shard_path, verified.manifest.feature_registry)
        if len(rows) != shard.row_count:
            raise CenturyCacheVerificationError(
                f"cache shard row count changed after verification: {shard.filename}"
            )
        if canonical_rows_sha256(rows) != shard.canonical_rows_sha256:
            raise CenturyCacheVerificationError(
                f"cache shard logical content changed after verification: {shard.filename}"
            )
        yield from rows


def open_century_cache_for_recovery(
    cache_directory: str | Path,
    *,
    expectations: CenturyCacheExpectations,
) -> VerifiedCenturyCache:
    """Read-only recovery gate; missing/invalid caches require an external rebuild.

    This entry point has no chart engine, builder callback, or regeneration option.
    It therefore cannot turn an ordinary global recovery into a century scan.
    """

    directory = Path(cache_directory)
    if not (directory / "manifest.json").is_file():
        raise CenturyCacheRecoveryError(
            "ordinary recovery requires a prebuilt verified century cache; "
            "run the explicit cache-build workflow first"
        )
    try:
        return verify_century_cache(directory, expectations=expectations)
    except CenturyCacheVerificationError as exc:
        raise CenturyCacheRecoveryError(
            f"ordinary recovery rejected the century cache: {exc}"
        ) from exc
