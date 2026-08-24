"""Repository-tracked trust root for ordinary century-cache verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)

from .models import (
    SHA256_PATTERN,
    CenturyCacheBuildSpec,
    CenturyCacheExpectations,
    CenturyCacheShard,
    ExactStateUniverseProvenance,
    FrozenModel,
    VerifiedCenturyCache,
    required_feature_ids_sha256,
)

DEFAULT_CENTURY_CACHE_TRUST_LOCK = Path("data/century_cache/v1.trust-lock.json")


class CenturyCacheTrustLockV1(FrozenModel):
    """Independent, trackable binding for one canonical cache publication.

    The full predeclared build spec is embedded so recovery expectations are
    derived from repository-controlled bytes rather than copied from the cache's
    self-asserted manifest.
    """

    schema_version: Literal["century-cache-trust-lock-v1"] = (
        "century-cache-trust-lock-v1"
    )
    cache_locator: str = Field(min_length=1)
    build_spec: CenturyCacheBuildSpec
    build_spec_sha256: str = Field(pattern=SHA256_PATTERN)
    manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    interval_count: int = Field(gt=0)
    exact_state_provenance: ExactStateUniverseProvenance
    shards: tuple[CenturyCacheShard, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_lock_bindings(self) -> CenturyCacheTrustLockV1:
        if Path(self.cache_locator).is_absolute():
            raise ValueError("cache trust-lock locator must be repository-relative")
        if ".." in Path(self.cache_locator).parts:
            raise ValueError("cache trust-lock locator must not escape the repository")
        if self.build_spec_sha256 != sha256_json(
            self.build_spec.model_dump(mode="json")
        ):
            raise ValueError("cache trust-lock build-spec hash is inconsistent")
        if self.build_spec.reconciliation_aggregate_sha256 is None:
            raise ValueError(
                "canonical cache trust lock requires reconciliation provenance"
            )
        if sum(shard.row_count for shard in self.shards) != self.interval_count:
            raise ValueError("cache trust-lock shard counts are inconsistent")
        if tuple(shard.filename for shard in self.shards) != tuple(
            sorted(shard.filename for shard in self.shards)
        ):
            raise ValueError("cache trust-lock shards are not canonically ordered")
        for previous, current in zip(self.shards, self.shards[1:], strict=False):
            if previous.utc_end_exclusive != current.utc_start:
                raise ValueError("cache trust-lock shard ranges contain a gap or overlap")
        exact = self.exact_state_provenance
        if (
            exact.utc_start != self.build_spec.utc_start
            or exact.utc_end_exclusive != self.build_spec.utc_end_exclusive
            or exact.interval_count != self.interval_count
            or exact.logical_universe_sha256 != self.logical_universe_sha256
        ):
            raise ValueError(
                "cache trust-lock exact-state provenance is inconsistent"
            )
        if self.shards[0].utc_start != self.build_spec.utc_start or (
            self.shards[-1].utc_end_exclusive
            != self.build_spec.utc_end_exclusive
        ):
            raise ValueError("cache trust-lock shard range differs from build spec")
        return self


def century_cache_expectations_from_build_spec(
    spec: CenturyCacheBuildSpec,
) -> CenturyCacheExpectations:
    """Derive all ordinary-verification expectations from trusted spec bytes."""

    feature_ids = tuple(item.feature_id for item in spec.feature_registry)
    return CenturyCacheExpectations(
        utc_start=spec.utc_start,
        utc_end_exclusive=spec.utc_end_exclusive,
        feature_vector_schema_version=spec.feature_vector_schema_version,
        semantic_feature_registry_sha256=spec.semantic_feature_registry_sha256,
        cache_feature_registry_sha256=spec.feature_registry_sha256,
        required_feature_ids=feature_ids,
        required_feature_registry_sha256=required_feature_ids_sha256(feature_ids),
        build_plan_sha256=spec.build_plan_sha256,
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
        design_root_time_tolerance_seconds=(
            spec.design_root_time_tolerance_seconds
        ),
        design_root_arc_tolerance_degrees=(
            spec.design_root_arc_tolerance_degrees
        ),
        parity_report_sha256=spec.parity_report_sha256,
        parity_reference_source_locator=spec.parity_reference_source_locator,
        parity_reference_source_sha256=spec.parity_reference_source_sha256,
        boundary_audit_report_sha256=spec.boundary_audit_report_sha256,
        reconciliation_aggregate_sha256=spec.reconciliation_aggregate_sha256,
    )


def trust_lock_from_verified_cache(
    verified: VerifiedCenturyCache,
    *,
    build_spec: CenturyCacheBuildSpec,
    cache_locator: str,
) -> CenturyCacheTrustLockV1:
    """Mint a lock only after a cache was verified against its external spec."""

    manifest = verified.manifest
    expectations = century_cache_expectations_from_build_spec(build_spec)
    manifest_bindings = {
        "UTC start": (manifest.utc_start, expectations.utc_start),
        "UTC end": (manifest.utc_end_exclusive, expectations.utc_end_exclusive),
        "feature-vector schema": (
            manifest.feature_vector_schema_version,
            expectations.feature_vector_schema_version,
        ),
        "semantic feature registry": (
            manifest.semantic_feature_registry_sha256,
            expectations.semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            manifest.feature_registry_sha256,
            expectations.cache_feature_registry_sha256,
        ),
        "build plan": (
            manifest.build_plan_sha256,
            expectations.build_plan_sha256,
        ),
        "engine validation": (
            manifest.engine.engine_validation_sha256,
            expectations.engine_validation_sha256,
        ),
        "ephemeris source manifest": (
            manifest.engine.ephemeris_provenance.source_manifest_sha256,
            expectations.ephemeris_source_manifest_sha256,
        ),
        "ephemeris file set": (
            manifest.engine.ephemeris_provenance.ephemeris_file_set_sha256,
            expectations.ephemeris_file_set_sha256,
        ),
        "Mandala mapping": (
            manifest.mandala_mapping_sha256,
            expectations.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            manifest.bodygraph_mapping_sha256,
            expectations.bodygraph_mapping_sha256,
        ),
        "boundary policy": (
            manifest.boundary_policy_version,
            expectations.boundary_policy_version,
        ),
        "Design time tolerance": (
            manifest.design_root_time_tolerance_seconds,
            expectations.design_root_time_tolerance_seconds,
        ),
        "Design arc tolerance": (
            manifest.design_root_arc_tolerance_degrees,
            expectations.design_root_arc_tolerance_degrees,
        ),
        "parity report": (
            manifest.parity_report_sha256,
            expectations.parity_report_sha256,
        ),
        "parity reference locator": (
            manifest.parity_reference_source_locator,
            expectations.parity_reference_source_locator,
        ),
        "parity reference hash": (
            manifest.parity_reference_source_sha256,
            expectations.parity_reference_source_sha256,
        ),
        "boundary audit": (
            manifest.boundary_audit_report_sha256,
            expectations.boundary_audit_report_sha256,
        ),
        "reconciliation aggregate": (
            manifest.reconciliation_aggregate_sha256,
            expectations.reconciliation_aggregate_sha256,
        ),
    }
    for label, (actual, expected) in manifest_bindings.items():
        if actual != expected:
            raise ValueError(
                f"verified cache {label} differs from the proposed trust lock"
            )
    if verified.manifest_sha256 != sha256_file(verified.manifest_path):
        raise ValueError("verified cache manifest changed before trust-lock minting")
    return CenturyCacheTrustLockV1(
        cache_locator=cache_locator,
        build_spec=build_spec,
        build_spec_sha256=sha256_json(build_spec.model_dump(mode="json")),
        manifest_sha256=verified.manifest_sha256,
        logical_universe_sha256=manifest.logical_universe_sha256,
        interval_count=manifest.interval_count,
        exact_state_provenance=manifest.exact_state_provenance,
        shards=manifest.shards,
    )


def write_century_cache_trust_lock_new(
    path: str | Path,
    lock: CenturyCacheTrustLockV1,
) -> Path:
    """Write canonical lock bytes without replacing an existing trust root."""

    destination = Path(path)
    write_new_canonical_json(destination, lock)
    return destination


def load_century_cache_trust_lock(path: str | Path) -> CenturyCacheTrustLockV1:
    """Load exact canonical lock bytes; noncanonical or malformed input fails."""

    source = Path(path)
    try:
        raw = source.read_bytes()
        parsed = json.loads(raw)
        if canonical_json_bytes(parsed) != raw:
            raise ValueError("trust lock is not canonically encoded")
        return CenturyCacheTrustLockV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"invalid century-cache trust lock: {source}") from exc
