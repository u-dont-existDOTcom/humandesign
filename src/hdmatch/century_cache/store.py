"""Explicit cache writer and fail-closed reader/verifier contracts."""

from __future__ import annotations

import hashlib
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

from .chart_adapter import (
    ExactStateBatchError,
    VerifiedExactShardSet,
    validate_verified_exact_shard_set,
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
    ExactStateUniverseProvenance,
    FeatureColumnSpec,
    VerifiedCenturyCache,
    canonical_rows_sha256,
    discrete_chart_identity_sha256,
    parquet_schema_sha256,
    required_feature_ids_sha256,
)
from .parquet import (
    CenturyCacheDependencyError,
    CenturyCacheParquetError,
    iter_parquet_shard_rows,
    read_parquet_shard,
    validate_row_features,
    write_parquet_shard_new,
)
from .streaming import (
    CenturyCacheStreamError,
    LogicalUniverseStreamValidator,
    canonical_row_json_line,
)
from .trust_lock import (
    century_cache_expectations_from_build_spec,
    load_century_cache_trust_lock,
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


@dataclass(frozen=True, slots=True)
class NoncanonicalCenturyCacheFixture:
    """Physical fixture output that can never be treated as a verified cache."""

    cache_directory: Path
    shard_paths: tuple[Path, ...]


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
    return century_cache_expectations_from_build_spec(spec)


def _validate_exact_universe_spec(
    provenance: ExactStateUniverseProvenance,
    spec: CenturyCacheBuildSpec,
) -> None:
    expected = {
        "UTC start": (provenance.utc_start, spec.utc_start),
        "UTC end": (provenance.utc_end_exclusive, spec.utc_end_exclusive),
        "boundary policy": (
            provenance.boundary_policy_version,
            spec.boundary_policy_version,
        ),
        "feature-vector schema": (
            provenance.feature_vector_schema_version,
            spec.feature_vector_schema_version,
        ),
        "semantic feature registry": (
            provenance.semantic_feature_registry_sha256,
            spec.semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            provenance.feature_registry_sha256,
            spec.feature_registry_sha256,
        ),
        "chart engine": (
            provenance.chart_engine_version,
            spec.engine.chart_engine_version,
        ),
        "ephemeris file set": (
            provenance.ephemeris_file_set_sha256,
            spec.engine.ephemeris_provenance.ephemeris_file_set_sha256,
        ),
        "node convention": (provenance.node_convention, spec.node_convention),
        "Mandala version": (
            provenance.mandala_mapping_version,
            spec.mandala_mapping_version,
        ),
        "Mandala mapping": (
            provenance.mandala_mapping_sha256,
            spec.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            provenance.bodygraph_mapping_sha256,
            spec.bodygraph_mapping_sha256,
        ),
        "Design-root time tolerance": (
            provenance.design_root_time_tolerance_seconds,
            spec.design_root_time_tolerance_seconds,
        ),
        "Design-root arc tolerance": (
            provenance.design_root_arc_tolerance_degrees,
            spec.design_root_arc_tolerance_degrees,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise CenturyCacheBuildError(f"exact-state batch {label} mismatch")


def write_noncanonical_century_cache_fixture(
    cache_directory: str | Path,
    *,
    registry: tuple[FeatureColumnSpec, ...],
    shards: tuple[CenturyCacheShardInput, ...],
    fixture_mode: Literal["noncanonical_fixture"],
) -> NoncanonicalCenturyCacheFixture:
    """Write physical Parquet fixtures without creating a trusted manifest.

    This deliberately cannot return :class:`VerifiedCenturyCache`, bundle proof
    evidence, or create ``manifest.json``.  It exists only for isolated storage
    contract tests and cannot be opened by the production recovery gate.
    """

    if fixture_mode != "noncanonical_fixture":
        raise CenturyCacheBuildError(
            "noncanonical fixture writing requires the noncanonical_fixture token"
        )
    if not shards:
        raise CenturyCacheBuildError("noncanonical fixture requires at least one shard")
    output = Path(cache_directory)
    if (output / "manifest.json").exists():
        raise CenturyCacheBuildError(
            "noncanonical fixture writer refuses a canonical cache directory"
        )
    output.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    try:
        for shard in shards:
            destination = output / shard.filename
            write_parquet_shard_new(destination, shard.rows, registry)
            paths.append(destination)
    except (OSError, ValueError, CenturyCacheDependencyError, CenturyCacheParquetError) as exc:
        raise CenturyCacheBuildError(
            f"could not write noncanonical cache fixture: {exc}"
        ) from exc
    return NoncanonicalCenturyCacheFixture(
        cache_directory=output,
        shard_paths=tuple(paths),
    )


def write_century_cache_explicit(
    cache_directory: str | Path,
    *,
    spec: CenturyCacheBuildSpec,
    exact_shard_set: VerifiedExactShardSet,
    shards: tuple[CenturyCacheShardInput, ...],
    evidence: CenturyCacheEvidenceInputs,
    build_mode: Literal["explicit_rebuild"],
) -> VerifiedCenturyCache:
    """Write a bounded Phase-1 compatibility fixture.

    The mandatory ``build_mode`` token makes cache construction an explicit
    operation.  This tuple-based compatibility path is deliberately capped at
    31 days and is not the Phase-2 century publisher.  The separate factory owns
    all astronomy and boundary selection; arbitrary caller-selected rows fail.
    """

    if build_mode != "explicit_rebuild":
        raise CenturyCacheBuildError(
            "century cache creation requires the explicit_rebuild operation"
        )
    if not shards:
        raise CenturyCacheBuildError("century cache requires at least one shard")
    if (spec.utc_end_exclusive - spec.utc_start).total_seconds() > 31 * 86400:
        raise CenturyCacheBuildError(
            "tuple-based Phase-1 compatibility writer is limited to 31 days; "
            "use the reconciled streaming Phase-2 publisher"
        )
    if tuple(item.filename for item in shards) != tuple(
        sorted(item.filename for item in shards)
    ):
        raise CenturyCacheBuildError("century-cache shard inputs must be filename-sorted")

    try:
        exact_provenance = validate_verified_exact_shard_set(exact_shard_set)
    except ExactStateBatchError as exc:
        raise CenturyCacheBuildError(f"invalid exact-state batch: {exc}") from exc
    _validate_exact_universe_spec(exact_provenance, spec)

    rows = tuple(row for shard in shards for row in shard.rows)
    if rows != tuple(exact_shard_set.iter_rows()):
        raise CenturyCacheBuildError(
            "canonical shard rows differ from the factory-created exact-state batch"
        )
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
            boundary_event_count=exact_provenance.boundary_event_count,
            exact_state_provenance=exact_provenance,
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
                    byte_count=destination.stat().st_size,
                )
            )
    except (OSError, ValueError, CenturyCacheDependencyError, CenturyCacheParquetError) as exc:
        raise CenturyCacheBuildError(f"could not write verified cache shards: {exc}") from exc

    manifest_payload = {
        **spec.model_dump(mode="python", exclude={"schema_version"}),
        "schema_version": "century-cache-manifest-v1",
        "interval_count": len(decoded_rows),
        "exact_state_provenance": exact_provenance,
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
        "build plan": expectations.build_plan_sha256,
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
        "reconciliation aggregate": expectations.reconciliation_aggregate_sha256,
    }
    actual_fields = {
        "feature_vector_schema_version": manifest.feature_vector_schema_version,
        "semantic feature registry": manifest.semantic_feature_registry_sha256,
        "cache feature registry": manifest.feature_registry_sha256,
        "build plan": manifest.build_plan_sha256,
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
        "reconciliation aggregate": manifest.reconciliation_aggregate_sha256,
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
    validator = LogicalUniverseStreamValidator(
        utc_start=manifest.utc_start,
        utc_end_exclusive=manifest.utc_end_exclusive,
        validate_row=lambda row: _validate_record_metadata(row, manifest),
    )
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
            if shard_path.stat().st_size != shard.byte_count:
                raise CenturyCacheVerificationError(
                    f"cache shard byte-count mismatch: {shard.filename}"
                )
            shard_digest = hashlib.sha256()
            shard_count = 0
            shard_start = None
            shard_end = None
            for row in iter_parquet_shard_rows(
                shard_path,
                manifest.feature_registry,
            ):
                if shard_start is None:
                    shard_start = row.utc_start
                shard_end = row.utc_end
                shard_digest.update(canonical_row_json_line(row))
                shard_count += 1
                validator.ingest(row)
            if shard_count != shard.row_count:
                raise CenturyCacheVerificationError(
                    f"cache shard row-count mismatch: {shard.filename}"
                )
            if shard_digest.hexdigest() != shard.canonical_rows_sha256:
                raise CenturyCacheVerificationError(
                    f"cache shard logical-row hash mismatch: {shard.filename}"
                )
            if shard_start != shard.utc_start or shard_end != shard.utc_end_exclusive:
                raise CenturyCacheVerificationError(
                    f"cache shard UTC bounds mismatch: {shard.filename}"
                )
        validator.finish(
            expected_interval_count=manifest.interval_count,
            expected_boundary_event_count=(
                manifest.exact_state_provenance.boundary_event_count
            ),
            expected_canonical_rows_sha256=manifest.logical_universe_sha256,
        )
    except (
        OSError,
        ValueError,
        CenturyCacheDependencyError,
        CenturyCacheParquetError,
        CenturyCacheStreamError,
    ) as exc:
        if isinstance(exc, CenturyCacheVerificationError):
            raise
        raise CenturyCacheVerificationError(f"cache shard verification failed: {exc}") from exc
    finally:
        validator.close()
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
        if shard_path.stat().st_size != shard.byte_count:
            raise CenturyCacheVerificationError(
                f"cache shard byte count changed after verification: {shard.filename}"
            )
        digest = hashlib.sha256()
        row_count = 0
        for row in iter_parquet_shard_rows(
            shard_path,
            verified.manifest.feature_registry,
        ):
            digest.update(canonical_row_json_line(row))
            row_count += 1
            yield row
        if row_count != shard.row_count:
            raise CenturyCacheVerificationError(
                f"cache shard row count changed after verification: {shard.filename}"
            )
        if digest.hexdigest() != shard.canonical_rows_sha256:
            raise CenturyCacheVerificationError(
                f"cache shard logical content changed after verification: {shard.filename}"
            )


def verify_century_cache_against_trust_lock(
    cache_directory: str | Path,
    *,
    trust_lock_path: str | Path,
) -> VerifiedCenturyCache:
    """Verify a cache only from independent repository-controlled lock bytes."""

    try:
        lock = load_century_cache_trust_lock(trust_lock_path)
    except ValueError as exc:
        raise CenturyCacheVerificationError(str(exc)) from exc
    verified = verify_century_cache(
        cache_directory,
        expectations=century_cache_expectations_from_build_spec(lock.build_spec),
    )
    manifest = verified.manifest
    lock_bindings = {
        "manifest SHA-256": (verified.manifest_sha256, lock.manifest_sha256),
        "logical-universe hash": (
            manifest.logical_universe_sha256,
            lock.logical_universe_sha256,
        ),
        "interval count": (manifest.interval_count, lock.interval_count),
        "exact-state provenance": (
            manifest.exact_state_provenance,
            lock.exact_state_provenance,
        ),
        "ordered shard bindings": (manifest.shards, lock.shards),
    }
    for label, (actual, expected) in lock_bindings.items():
        if actual != expected:
            raise CenturyCacheVerificationError(
                f"cache {label} differs from tracked trust lock"
            )
    return verified


def open_century_cache_for_recovery(
    cache_directory: str | Path,
    *,
    trust_lock_path: str | Path,
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
        return verify_century_cache_against_trust_lock(
            directory,
            trust_lock_path=trust_lock_path,
        )
    except CenturyCacheVerificationError as exc:
        raise CenturyCacheRecoveryError(
            f"ordinary recovery rejected the century cache: {exc}"
        ) from exc
