"""Manifest-last, atomic publication for streamed exact-state caches."""

from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from hdmatch.experiments.canonical import write_new_bytes, write_new_canonical_json
from hdmatch.provenance.swisseph_files import (
    EphemerisFileVerificationError,
    EphemerisManifestError,
    verify_ephemeris_directory,
)

from .chart_adapter import (
    ExactStateBatchError,
    VerifiedExactStateBatch,
    validate_verified_exact_state_batch,
)
from .evidence import (
    CenturyCacheEvidenceError,
    CenturyCacheEvidenceInputs,
    validate_external_cache_evidence,
)
from .models import (
    CenturyCacheBuildSpec,
    CenturyCacheManifest,
    CenturyCacheShard,
    CenturyCacheStreamIdentity,
    CenturyStateRecord,
    ExactStateUniverseProvenance,
    VerifiedCenturyCache,
)
from .parquet import (
    BoundedParquetShardWriter,
    BoundedShardWriteAudit,
    CenturyCacheDependencyError,
    CenturyCacheParquetError,
    validate_row_features,
)
from .streaming import (
    CenturyCacheStreamError,
    LogicalUniverseStreamAudit,
    LogicalUniverseStreamValidator,
)
from .trust_lock import century_cache_expectations_from_build_spec


class CenturyCachePublicationError(ValueError):
    """A streamed cache cannot be finalized as a canonical publication."""


@dataclass(frozen=True, slots=True)
class StagedCenturyCacheRows:
    """Final single-pass row audit available before boundary evidence exists."""

    staging_directory: Path
    logical_audit: LogicalUniverseStreamAudit
    shard_audit: BoundedShardWriteAudit
    shards: tuple[CenturyCacheShard, ...]


def _validate_row_metadata(
    row: CenturyStateRecord,
    identity: CenturyCacheStreamIdentity,
) -> None:
    expected = {
        "feature_vector_schema_version": identity.feature_vector_schema_version,
        "semantic_feature_registry_sha256": identity.semantic_feature_registry_sha256,
        "feature_registry_sha256": identity.feature_registry_sha256,
        "astronomy_engine_version": identity.engine.chart_engine_version,
        "ephemeris_file_set_sha256": (
            identity.engine.ephemeris_provenance.ephemeris_file_set_sha256
        ),
        "node_convention": identity.node_convention,
        "mandala_mapping_version": identity.mandala_mapping_version,
        "mandala_mapping_sha256": identity.mandala_mapping_sha256,
        "bodygraph_mapping_sha256": identity.bodygraph_mapping_sha256,
    }
    for field, required in expected.items():
        if getattr(row, field) != required:
            raise CenturyCacheStreamError(
                f"row {row.state_id} has mismatched {field}"
            )
    validate_row_features(row, identity.feature_registry)


def _require_aggregate_identity(
    provenance: ExactStateUniverseProvenance,
    identity: CenturyCacheStreamIdentity,
) -> None:
    expected = {
        "UTC start": (provenance.utc_start, identity.utc_start),
        "UTC end": (provenance.utc_end_exclusive, identity.utc_end_exclusive),
        "boundary policy": (
            provenance.boundary_policy_version,
            identity.boundary_policy_version,
        ),
        "feature-vector schema": (
            provenance.feature_vector_schema_version,
            identity.feature_vector_schema_version,
        ),
        "semantic feature registry": (
            provenance.semantic_feature_registry_sha256,
            identity.semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            provenance.feature_registry_sha256,
            identity.feature_registry_sha256,
        ),
        "chart engine": (
            provenance.chart_engine_version,
            identity.engine.chart_engine_version,
        ),
        "ephemeris file set": (
            provenance.ephemeris_file_set_sha256,
            identity.engine.ephemeris_provenance.ephemeris_file_set_sha256,
        ),
        "node convention": (provenance.node_convention, identity.node_convention),
        "Mandala version": (
            provenance.mandala_mapping_version,
            identity.mandala_mapping_version,
        ),
        "Mandala mapping": (
            provenance.mandala_mapping_sha256,
            identity.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            provenance.bodygraph_mapping_sha256,
            identity.bodygraph_mapping_sha256,
        ),
        "Design-root time tolerance": (
            provenance.design_root_time_tolerance_seconds,
            identity.design_root_time_tolerance_seconds,
        ),
        "Design-root arc tolerance": (
            provenance.design_root_arc_tolerance_degrees,
            identity.design_root_arc_tolerance_degrees,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise CenturyCachePublicationError(
                f"exact-state aggregate {label} mismatch"
            )


def _fsync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class Phase1CompatibilityCenturyCachePublisher:
    """Bounded publisher retained only for Phase-1 factory fixtures.

    The publisher intentionally has two finalization gates. ``finish_rows``
    exposes the final hash/count/event audit needed to construct the independent
    boundary report. ``finalize_and_publish`` then accepts the completed evidence
    and build spec, writes the manifest last, fully verifies the sibling staging
    directory, and only then renames it to the absent destination.
    """

    def __init__(
        self,
        cache_directory: str | Path,
        *,
        identity: CenturyCacheStreamIdentity,
        build_mode: Literal["explicit_rebuild"],
    ) -> None:
        if build_mode != "explicit_rebuild":
            raise CenturyCachePublicationError(
                "century cache publication requires the explicit_rebuild operation"
            )
        destination = Path(cache_directory)
        if destination.exists():
            raise FileExistsError(
                f"century-cache destination already exists: {destination}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(
            tempfile.mkdtemp(
                prefix=f".{destination.name}.staging-",
                dir=destination.parent,
            )
        )
        self._destination = destination
        self._staging = staging
        self._identity = identity
        self._logical_validator = LogicalUniverseStreamValidator(
            utc_start=identity.utc_start,
            utc_end_exclusive=identity.utc_end_exclusive,
            validate_row=lambda row: _validate_row_metadata(row, identity),
        )
        self._shard_writer = BoundedParquetShardWriter(
            staging,
            identity.feature_registry,
            target_bytes=identity.parquet_shard_target_bytes,
            hard_cap_bytes=identity.parquet_shard_hard_cap_bytes,
        )
        self._phase = "streaming"
        self._staged_rows: StagedCenturyCacheRows | None = None
        self._exact_provenance: ExactStateUniverseProvenance | None = None

    @property
    def staging_directory(self) -> Path:
        return self._staging

    def append_verified_batch(self, batch: VerifiedExactStateBatch) -> None:
        """Consume a Phase-1 batch; never use this as Phase-2 admission."""

        if self._phase != "streaming":
            raise CenturyCachePublicationError(
                "verified batches can only be appended during the streaming phase"
            )
        try:
            validate_verified_exact_state_batch(batch)
            for row in batch.rows:
                self._logical_validator.ingest(row)
                self._shard_writer.append(row)
        except (ExactStateBatchError, CenturyCacheParquetError, CenturyCacheStreamError) as exc:
            raise CenturyCachePublicationError(
                f"verified exact-state batch was rejected: {exc}"
            ) from exc

    def finish_rows(
        self,
        *,
        exact_state_provenance: ExactStateUniverseProvenance,
    ) -> StagedCenturyCacheRows:
        """Finish the row stream and expose inputs for final boundary evidence."""

        if self._phase != "streaming":
            raise CenturyCachePublicationError(
                "century-cache rows have already been finalized"
            )
        _require_aggregate_identity(exact_state_provenance, self._identity)
        try:
            logical_audit = self._logical_validator.finish(
                expected_interval_count=exact_state_provenance.interval_count,
                expected_boundary_event_count=(
                    exact_state_provenance.boundary_event_count
                ),
                expected_canonical_rows_sha256=(
                    exact_state_provenance.logical_universe_sha256
                ),
            )
            shards, shard_audit = self._shard_writer.finish()
        except (CenturyCacheParquetError, CenturyCacheStreamError) as exc:
            raise CenturyCachePublicationError(
                f"streamed exact-state universe was rejected: {exc}"
            ) from exc
        if shard_audit.row_count != logical_audit.interval_count:
            raise CenturyCachePublicationError(
                "logical and physical streamed row counts differ"
            )
        staged = StagedCenturyCacheRows(
            staging_directory=self._staging,
            logical_audit=logical_audit,
            shard_audit=shard_audit,
            shards=shards,
        )
        self._staged_rows = staged
        self._exact_provenance = exact_state_provenance
        self._phase = "rows_finished"
        return staged

    def finalize_and_publish(
        self,
        *,
        spec: CenturyCacheBuildSpec,
        evidence: CenturyCacheEvidenceInputs,
    ) -> VerifiedCenturyCache:
        """Bundle evidence, write manifest last, verify, and atomically publish."""

        if self._phase != "rows_finished":
            raise CenturyCachePublicationError(
                "finish_rows must pass before cache publication"
            )
        staged_rows = self._staged_rows
        exact_provenance = self._exact_provenance
        if staged_rows is None or exact_provenance is None:  # pragma: no cover
            raise RuntimeError("publisher state is inconsistent")
        if CenturyCacheStreamIdentity.from_build_spec(spec) != self._identity:
            raise CenturyCachePublicationError(
                "final build spec differs from the pre-stream identity contract"
            )

        try:
            observed_ephemeris = verify_ephemeris_directory(
                source_manifest_path=evidence.ephemeris_source_manifest_path,
                ephemeris_directory=evidence.ephemeris_directory,
            )
        except (EphemerisManifestError, EphemerisFileVerificationError) as exc:
            raise CenturyCachePublicationError(
                f"Swiss Ephemeris source verification failed: {exc}"
            ) from exc
        if observed_ephemeris != spec.engine.ephemeris_provenance:
            raise CenturyCachePublicationError(
                "actual Swiss Ephemeris source/files differ from cache provenance"
            )
        try:
            validated_evidence = validate_external_cache_evidence(
                evidence,
                spec=spec,
                logical_universe_sha256=(
                    staged_rows.logical_audit.canonical_rows_sha256
                ),
                interval_count=staged_rows.logical_audit.interval_count,
                boundary_event_count=(
                    staged_rows.logical_audit.boundary_event_count
                ),
                exact_state_provenance=exact_provenance,
            )
            for filename, raw in validated_evidence.bundled_bytes:
                write_new_bytes(self._staging / filename, raw)
        except (CenturyCacheEvidenceError, OSError, ValueError) as exc:
            raise CenturyCachePublicationError(
                f"cache proof evidence failed: {exc}"
            ) from exc

        manifest_payload = {
            **spec.model_dump(mode="python", exclude={"schema_version"}),
            "schema_version": "century-cache-manifest-v1",
            "interval_count": staged_rows.logical_audit.interval_count,
            "exact_state_provenance": exact_provenance,
            "evidence_artifacts": validated_evidence.artifacts,
            "shards": staged_rows.shards,
            "logical_universe_sha256": (
                staged_rows.logical_audit.canonical_rows_sha256
            ),
            "verification_status": "pass",
        }
        manifest_path = self._staging / "manifest.json"
        try:
            manifest = CenturyCacheManifest.model_validate(
                manifest_payload,
                strict=True,
            )
            write_new_canonical_json(manifest_path, manifest)
            _fsync_directory(self._staging)
        except (OSError, ValueError) as exc:
            raise CenturyCachePublicationError(
                f"could not finalize cache manifest: {exc}"
            ) from exc

        # Delayed import avoids coupling the storage verifier back into this
        # stateful publication helper.
        from .store import verify_century_cache

        try:
            verified_staging = verify_century_cache(
                self._staging,
                expectations=century_cache_expectations_from_build_spec(spec),
            )
        except (ValueError, CenturyCacheDependencyError) as exc:
            raise CenturyCachePublicationError(
                f"staged century cache failed complete verification: {exc}"
            ) from exc
        if self._destination.exists():
            raise FileExistsError(
                f"century-cache destination appeared before publish: {self._destination}"
            )
        os.rename(self._staging, self._destination)
        _fsync_directory(self._destination.parent)
        self._phase = "published"
        return VerifiedCenturyCache(
            cache_directory=self._destination,
            manifest_path=self._destination / "manifest.json",
            manifest_sha256=verified_staging.manifest_sha256,
            manifest=verified_staging.manifest,
            required_feature_coverage=verified_staging.required_feature_coverage,
        )

    def abort(self) -> None:
        """Delete only this publisher's private sibling staging directory."""

        if self._phase == "published":
            raise CenturyCachePublicationError(
                "a published cache cannot be aborted through its staging handle"
            )
        if self._staging.is_dir():
            shutil.rmtree(self._staging)
        self._logical_validator.close()
        self._phase = "aborted"


class StreamingCenturyCachePublisher(Phase1CompatibilityCenturyCachePublisher):
    """Phase-2 publisher reserved for the concrete reconciled capability.

    Direct Phase-1 batches are intentionally rejected.  The integration branch
    must wire ``append_reconciled_chunk`` to the concrete private-token validator
    in ``hdmatch.century_cache.reconcile`` before a canonical century build can
    begin.  Leaving this gate closed is safer than accepting a structural protocol
    that callers could implement to bypass overlap/core reconciliation.
    """

    def append_verified_batch(self, batch: VerifiedExactStateBatch) -> None:
        del batch
        raise CenturyCachePublicationError(
            "Phase-2 publication requires a concrete ReconciledExactStateChunk; "
            "direct Phase-1 exact batches are not admissible"
        )

    def append_reconciled_chunk(self, chunk: object) -> None:
        del chunk
        raise CenturyCachePublicationError(
            "concrete reconciled-chunk admission is not integrated; fail closed"
        )
