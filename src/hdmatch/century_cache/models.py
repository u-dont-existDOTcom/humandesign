"""Typed, astronomy-agnostic contracts for the reusable century state cache."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Literal, Protocol, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json
from hdmatch.provenance.swisseph_files import VerifiedEphemerisProvenance

SHA256_PATTERN = r"^[a-f0-9]{64}$"
GIT_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
FEATURE_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$"
SHARD_NAME_PATTERN = r"^states-[A-Za-z0-9_.-]+\.parquet\.zst$"
LOGICAL_HASH_STRATEGY: Literal["sha256-canonical-json-lines-v1"] = (
    "sha256-canonical-json-lines-v1"
)
STORAGE_FORMAT: Literal["parquet-internal-zstd-v1"] = "parquet-internal-zstd-v1"
PARQUET_SHARD_TARGET_BYTES: Literal[67108864] = 67108864
PARQUET_SHARD_HARD_CAP_BYTES: Literal[83886080] = 83886080


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class FeatureStorageType(StrEnum):
    """Stable physical types accepted from the independent feature registry."""

    BOOLEAN = "boolean"
    INT64 = "int64"
    FLOAT64 = "float64"
    STRING = "string"
    STRING_LIST = "string_list"
    INT64_LIST = "int64_list"
    ACTIVATION_LIST = "activation_list"
    JSON = "json"


class FeatureColumnSpec(FrozenModel):
    """One registry field and its lossless Parquet representation."""

    feature_id: str = Field(pattern=FEATURE_ID_PATTERN)
    storage_type: FeatureStorageType
    nullable: bool = False

    @property
    def parquet_column_name(self) -> str:
        return f"feature::{self.feature_id}"


class FeatureValue(FrozenModel):
    """An explicitly present feature value; ``None`` means unknown, never false."""

    feature_id: str = Field(pattern=FEATURE_ID_PATTERN)
    value: JsonValue


class CacheableStateSource(Protocol):
    """Narrow adapter implemented by an independent feature-vector workstream."""

    def to_century_cache_mapping(self) -> Mapping[str, object]:
        """Return a canonical mapping accepted by :class:`CenturyStateRecord`."""


CacheRecordInput: TypeAlias = "CenturyStateRecord | CacheableStateSource | Mapping[str, object]"


class CenturyStateRecord(FrozenModel):
    """One exact interval plus a registry-defined, complete feature mapping.

    The cache contract intentionally does not define Human Design feature meaning.
    The independent registry supplies stable feature IDs and storage types.  Every
    row must contain every declared ID; missing fields cannot become false values.
    """

    schema_version: Literal["century-state-row-v1"] = "century-state-row-v1"
    state_id: str = Field(min_length=1)
    utc_start: datetime
    utc_end: datetime
    duration_seconds: float = Field(gt=0.0)
    representative_utc: datetime
    design_timestamp: datetime
    chart_features_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_vector_schema_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    astronomy_engine_version: str = Field(min_length=1)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_events: tuple[str, ...] = ()
    feature_values: tuple[FeatureValue, ...] = Field(min_length=1)

    @field_validator("utc_start", "utc_end", "representative_utc", "design_timestamp")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("century-cache timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("feature_values")
    @classmethod
    def require_canonical_feature_order(
        cls, values: tuple[FeatureValue, ...]
    ) -> tuple[FeatureValue, ...]:
        identifiers = tuple(item.feature_id for item in values)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("century-cache row contains duplicate feature IDs")
        if identifiers != tuple(sorted(identifiers)):
            raise ValueError("century-cache row feature IDs must be canonically sorted")
        return values

    @field_validator("boundary_events")
    @classmethod
    def require_canonical_boundary_events(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value for value in values):
            raise ValueError("boundary-event identifiers must not be empty")
        if values != tuple(sorted(set(values))):
            raise ValueError("boundary events must be sorted and unique")
        return values

    @model_validator(mode="after")
    def require_exact_interval(self) -> CenturyStateRecord:
        if self.utc_end <= self.utc_start:
            raise ValueError("century-cache interval must have positive duration")
        actual = (self.utc_end - self.utc_start).total_seconds()
        if abs(actual - self.duration_seconds) > 1e-6:
            raise ValueError("duration_seconds does not equal the exact interval duration")
        if not self.utc_start <= self.representative_utc < self.utc_end:
            raise ValueError("representative_utc must lie inside [utc_start, utc_end)")
        if self.design_timestamp >= self.utc_start:
            raise ValueError("Design timestamp must precede the Personality interval")
        return self

    def feature_mapping(self) -> dict[str, JsonValue]:
        return {item.feature_id: item.value for item in self.feature_values}


def coerce_century_state_record(value: CacheRecordInput) -> CenturyStateRecord:
    """Adapt a canonical mapping/protocol without importing feature internals."""

    if isinstance(value, CenturyStateRecord):
        return value
    payload = value if isinstance(value, Mapping) else value.to_century_cache_mapping()
    return CenturyStateRecord.model_validate(payload, strict=True)


class CenturyCacheEngineProvenance(FrozenModel):
    """SWIEPH proof bound into every canonical cache manifest."""

    schema_version: Literal["century-cache-engine-provenance-v1"] = (
        "century-cache-engine-provenance-v1"
    )
    provider: Literal["swiss_ephemeris_local_files"]
    chart_engine_version: str = Field(min_length=1)
    swiss_library_version: str = Field(min_length=1)
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_provenance: VerifiedEphemerisProvenance
    ephemeris_requested: Literal["SWIEPH"]
    ephemeris_returned: Literal["SWIEPH"]
    requested_flags: int = Field(gt=0)
    returned_flags_observed: tuple[int, ...] = Field(min_length=1)
    ephemeris_mask: int = Field(gt=0)
    swieph_flag: int = Field(gt=0)

    @field_validator("returned_flags_observed")
    @classmethod
    def require_canonical_returned_flags(cls, values: tuple[int, ...]) -> tuple[int, ...]:
        if values != tuple(sorted(set(values))):
            raise ValueError("returned flags must be sorted and unique")
        return values

    @model_validator(mode="after")
    def reject_fallback_flags(self) -> CenturyCacheEngineProvenance:
        if self.swieph_flag & self.ephemeris_mask != self.swieph_flag:
            raise ValueError("SWIEPH flag is not contained in the ephemeris mask")
        if self.requested_flags & self.ephemeris_mask != self.swieph_flag:
            raise ValueError("requested ephemeris flags do not select SWIEPH")
        if any(
            flags & self.ephemeris_mask != self.swieph_flag
            for flags in self.returned_flags_observed
        ):
            raise ValueError("returned ephemeris flags contain a non-SWIEPH mode")
        return self


def _validate_feature_registry(
    registry: tuple[FeatureColumnSpec, ...], registry_sha256: str
) -> None:
    identifiers = tuple(item.feature_id for item in registry)
    if not identifiers:
        raise ValueError("feature registry must not be empty")
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("feature registry contains duplicate IDs")
    if identifiers != tuple(sorted(identifiers)):
        raise ValueError("feature registry IDs must be canonically sorted")
    expected_hash = sha256_json([item.model_dump(mode="json") for item in registry])
    if registry_sha256 != expected_hash:
        raise ValueError("feature registry hash is inconsistent")


class CenturyCacheBuildSpec(FrozenModel):
    """Predeclared inputs to an explicit cache build; contains no generated rows."""

    schema_version: Literal["century-cache-build-spec-v1"] = "century-cache-build-spec-v1"
    cache_version: Literal["century-cache-v1"] = "century-cache-v1"
    feature_vector_schema_version: str = Field(min_length=1)
    utc_start: datetime
    utc_end_exclusive: datetime
    feature_registry: tuple[FeatureColumnSpec, ...] = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_coverage: float = Field(ge=0.0, le=1.0)
    calculation_tier: Literal["M2"]
    exact_intervals: Literal[True]
    canonical_row_hash_strategy: Literal["sha256-canonical-json-lines-v1"] = (
        LOGICAL_HASH_STRATEGY
    )
    storage_format: Literal["parquet-internal-zstd-v1"] = STORAGE_FORMAT
    parquet_shard_target_bytes: Literal[67108864] = PARQUET_SHARD_TARGET_BYTES
    parquet_shard_hard_cap_bytes: Literal[83886080] = PARQUET_SHARD_HARD_CAP_BYTES
    build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    engine: CenturyCacheEngineProvenance
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    parity_status: Literal["pass"]
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    parity_reference_source_locator: str = Field(min_length=1)
    parity_reference_source_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_audit_status: Literal["pass"]
    boundary_audit_report_sha256: str = Field(pattern=SHA256_PATTERN)
    reconciliation_aggregate_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    generation_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    created_at_utc: datetime

    @field_validator("utc_start", "utc_end_exclusive", "created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("cache contract timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_build_invariants(self) -> CenturyCacheBuildSpec:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("cache range must be positive")
        if self.required_feature_coverage != 1.0:
            raise ValueError("canonical cache requires complete feature coverage")
        _validate_feature_registry(self.feature_registry, self.feature_registry_sha256)
        if self.node_convention != "true":
            raise ValueError("cache node convention differs from the frozen convention")
        return self


class CenturyCacheStreamIdentity(FrozenModel):
    """Pre-stream identities that do not depend on the final boundary audit.

    The boundary-audit report binds the final row hash/count and therefore cannot
    exist before rows have streamed.  This contract freezes every identity needed
    to validate rows and storage while leaving evidence finalization for the
    manifest-last publication step.
    """

    schema_version: Literal["century-cache-stream-identity-v1"] = (
        "century-cache-stream-identity-v1"
    )
    cache_version: Literal["century-cache-v1"] = "century-cache-v1"
    feature_vector_schema_version: str = Field(min_length=1)
    utc_start: datetime
    utc_end_exclusive: datetime
    feature_registry: tuple[FeatureColumnSpec, ...] = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_coverage: float = Field(ge=0.0, le=1.0)
    calculation_tier: Literal["M2"]
    exact_intervals: Literal[True]
    canonical_row_hash_strategy: Literal["sha256-canonical-json-lines-v1"] = (
        LOGICAL_HASH_STRATEGY
    )
    storage_format: Literal["parquet-internal-zstd-v1"] = STORAGE_FORMAT
    parquet_shard_target_bytes: Literal[67108864] = PARQUET_SHARD_TARGET_BYTES
    parquet_shard_hard_cap_bytes: Literal[83886080] = PARQUET_SHARD_HARD_CAP_BYTES
    build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    engine: CenturyCacheEngineProvenance
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    generation_commit: str = Field(pattern=GIT_COMMIT_PATTERN)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("cache stream timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_stream_invariants(self) -> CenturyCacheStreamIdentity:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("cache stream range must be positive")
        if self.required_feature_coverage != 1.0:
            raise ValueError("canonical cache stream requires complete feature coverage")
        _validate_feature_registry(self.feature_registry, self.feature_registry_sha256)
        return self

    @classmethod
    def from_build_spec(cls, spec: CenturyCacheBuildSpec) -> CenturyCacheStreamIdentity:
        fields = set(cls.model_fields) - {"schema_version"}
        payload = {
            name: getattr(spec, name)
            for name in fields
        }
        return cls.model_validate(payload, strict=True)


class CenturyCacheShard(FrozenModel):
    filename: str = Field(pattern=SHARD_NAME_PATTERN)
    sha256: str = Field(pattern=SHA256_PATTERN)
    row_count: int = Field(gt=0)
    utc_start: datetime
    utc_end_exclusive: datetime
    canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    parquet_schema_sha256: str = Field(pattern=SHA256_PATTERN)
    byte_count: int = Field(gt=0, le=PARQUET_SHARD_HARD_CAP_BYTES)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("cache shard timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_positive_range(self) -> CenturyCacheShard:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("cache shard range must be positive")
        if Path(self.filename).name != self.filename:
            raise ValueError("cache shard filename must not contain a path")
        return self


class CenturyCacheEvidenceArtifact(FrozenModel):
    """One bundled proof artifact re-opened during every cache verification."""

    kind: Literal["engine_validation", "parity", "boundary_audit", "reconciliation"]
    filename: str = Field(pattern=r"^evidence/[a-z-]+\.json$")
    sha256: str = Field(pattern=SHA256_PATTERN)
    schema_version: str = Field(min_length=1)
    validation_status: Literal["pass"]


class ExactStateBatchProvenance(FrozenModel):
    """One bounded factory job's resumability receipt.

    The canonical hash binds persisted job output, but the receipt alone is not
    proof after a process restart.  Canonical assembly must re-hash/decode and
    production-replay the job before minting a new in-process verified token.
    """

    schema_version: Literal["exact-state-batch-provenance-v1"] = (
        "exact-state-batch-provenance-v1"
    )
    factory_version: Literal["production-exact-state-batch-v1"] = (
        "production-exact-state-batch-v1"
    )
    verification_status: Literal["pass"]
    utc_start: datetime
    utc_end_exclusive: datetime
    interval_count: int = Field(gt=0)
    boundary_event_count: int = Field(ge=0)
    boundary_policy_version: str = Field(min_length=1)
    stable_interval_partition_sha256: str = Field(pattern=SHA256_PATTERN)
    canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_vector_schema_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    chart_engine_version: str = Field(min_length=1)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("exact-state provenance timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_consistent_batch(self) -> ExactStateBatchProvenance:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("exact-state provenance range must be positive")
        if self.canonical_rows_sha256 != self.logical_universe_sha256:
            raise ValueError("exact-state canonical-row and logical-universe hashes differ")
        return self


class ExactStateUniverseProvenance(FrozenModel):
    """Aggregate provenance minted from ordered, in-process verified batches."""

    schema_version: Literal["exact-state-universe-provenance-v1"] = (
        "exact-state-universe-provenance-v1"
    )
    assembly_version: Literal["production-exact-state-assembly-v1"] = (
        "production-exact-state-assembly-v1"
    )
    verification_status: Literal["pass"]
    assembly_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    ordered_source_batch_provenance_sha256s: tuple[str, ...] = Field(min_length=1)
    reconciliation_report_sha256: str = Field(pattern=SHA256_PATTERN)
    utc_start: datetime
    utc_end_exclusive: datetime
    batch_count: int = Field(gt=0)
    interval_count: int = Field(gt=0)
    boundary_event_count: int = Field(ge=0)
    boundary_policy_version: str = Field(min_length=1)
    canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_vector_schema_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    chart_engine_version: str = Field(min_length=1)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("exact-state universe timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("ordered_source_batch_provenance_sha256s")
    @classmethod
    def require_source_hashes(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(re.fullmatch(SHA256_PATTERN, value) is None for value in values):
            raise ValueError("exact-state source batch hash is invalid")
        return values

    @model_validator(mode="after")
    def require_consistent_universe(self) -> ExactStateUniverseProvenance:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("exact-state universe range must be positive")
        if self.batch_count != len(self.ordered_source_batch_provenance_sha256s):
            raise ValueError("exact-state universe batch count is inconsistent")
        if self.canonical_rows_sha256 != self.logical_universe_sha256:
            raise ValueError("exact-state universe canonical and logical hashes differ")
        return self


class CenturyCacheManifest(FrozenModel):
    """Complete authoritative contract for a verified exact-state cache."""

    schema_version: Literal["century-cache-manifest-v1"] = "century-cache-manifest-v1"
    cache_version: Literal["century-cache-v1"] = "century-cache-v1"
    feature_vector_schema_version: str = Field(min_length=1)
    utc_start: datetime
    utc_end_exclusive: datetime
    interval_count: int = Field(gt=0)
    feature_registry: tuple[FeatureColumnSpec, ...] = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_coverage: float = Field(ge=0.0, le=1.0)
    calculation_tier: Literal["M2"]
    exact_intervals: Literal[True]
    canonical_row_hash_strategy: Literal["sha256-canonical-json-lines-v1"]
    storage_format: Literal["parquet-internal-zstd-v1"]
    parquet_shard_target_bytes: Literal[67108864]
    parquet_shard_hard_cap_bytes: Literal[83886080]
    build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    engine: CenturyCacheEngineProvenance
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    parity_status: Literal["pass"]
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    parity_reference_source_locator: str = Field(min_length=1)
    parity_reference_source_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_audit_status: Literal["pass"]
    boundary_audit_report_sha256: str = Field(pattern=SHA256_PATTERN)
    reconciliation_aggregate_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    generation_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    created_at_utc: datetime
    exact_state_provenance: ExactStateUniverseProvenance
    evidence_artifacts: tuple[CenturyCacheEvidenceArtifact, ...] = Field(min_length=3)
    shards: tuple[CenturyCacheShard, ...] = Field(min_length=1)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    verification_status: Literal["pass"]

    @field_validator("utc_start", "utc_end_exclusive", "created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("cache manifest timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_manifest_invariants(self) -> CenturyCacheManifest:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("cache range must be positive")
        if self.required_feature_coverage != 1.0:
            raise ValueError("canonical cache requires complete feature coverage")
        _validate_feature_registry(self.feature_registry, self.feature_registry_sha256)
        exact = self.exact_state_provenance
        exact_bindings = {
            "UTC start": (exact.utc_start, self.utc_start),
            "UTC end": (exact.utc_end_exclusive, self.utc_end_exclusive),
            "interval count": (exact.interval_count, self.interval_count),
            "logical-universe hash": (
                exact.logical_universe_sha256,
                self.logical_universe_sha256,
            ),
            "boundary policy": (
                exact.boundary_policy_version,
                self.boundary_policy_version,
            ),
            "feature-vector schema": (
                exact.feature_vector_schema_version,
                self.feature_vector_schema_version,
            ),
            "semantic feature registry": (
                exact.semantic_feature_registry_sha256,
                self.semantic_feature_registry_sha256,
            ),
            "physical feature registry": (
                exact.feature_registry_sha256,
                self.feature_registry_sha256,
            ),
            "chart engine": (exact.chart_engine_version, self.engine.chart_engine_version),
            "ephemeris file set": (
                exact.ephemeris_file_set_sha256,
                self.engine.ephemeris_provenance.ephemeris_file_set_sha256,
            ),
            "node convention": (exact.node_convention, self.node_convention),
            "Mandala version": (
                exact.mandala_mapping_version,
                self.mandala_mapping_version,
            ),
            "Mandala mapping": (
                exact.mandala_mapping_sha256,
                self.mandala_mapping_sha256,
            ),
            "Bodygraph mapping": (
                exact.bodygraph_mapping_sha256,
                self.bodygraph_mapping_sha256,
            ),
            "Design-root time tolerance": (
                exact.design_root_time_tolerance_seconds,
                self.design_root_time_tolerance_seconds,
            ),
            "Design-root arc tolerance": (
                exact.design_root_arc_tolerance_degrees,
                self.design_root_arc_tolerance_degrees,
            ),
        }
        for label, (actual, required) in exact_bindings.items():
            if actual != required:
                raise ValueError(f"cache exact-state {label} binding is inconsistent")
        expected_evidence: dict[str, tuple[str, str]] = {
            "engine_validation": (
                "evidence/engine-validation.json",
                self.engine.engine_validation_sha256,
            ),
            "parity": ("evidence/parity-report.json", self.parity_report_sha256),
            "boundary_audit": (
                "evidence/boundary-audit-report.json",
                self.boundary_audit_report_sha256,
            ),
        }
        if self.reconciliation_aggregate_sha256 is not None:
            expected_evidence["reconciliation"] = (
                "evidence/reconciliation-aggregate.json",
                self.reconciliation_aggregate_sha256,
            )
        if {item.kind for item in self.evidence_artifacts} != set(expected_evidence):
            raise ValueError("cache manifest proof-artifact set is inconsistent")
        if tuple(item.kind for item in self.evidence_artifacts) != tuple(
            sorted(expected_evidence)
        ):
            raise ValueError("cache evidence artifacts must be canonically ordered")
        for artifact in self.evidence_artifacts:
            filename, digest = expected_evidence[artifact.kind]
            if artifact.filename != filename or artifact.sha256 != digest:
                raise ValueError(f"cache {artifact.kind} evidence binding is inconsistent")
        if sum(shard.row_count for shard in self.shards) != self.interval_count:
            raise ValueError("cache shard row counts do not equal interval_count")
        if tuple(shard.filename for shard in self.shards) != tuple(
            sorted(shard.filename for shard in self.shards)
        ):
            raise ValueError("cache shards must be canonically ordered by filename")
        if self.shards[0].utc_start != self.utc_start:
            raise ValueError("first cache shard does not start at the declared universe start")
        if self.shards[-1].utc_end_exclusive != self.utc_end_exclusive:
            raise ValueError("last cache shard does not end at the declared universe end")
        for previous, current in zip(self.shards, self.shards[1:], strict=False):
            if previous.utc_end_exclusive != current.utc_start:
                raise ValueError("cache shard ranges contain a gap or overlap")
        expected_schema_hash = parquet_schema_sha256(self.feature_registry)
        if any(
            shard.parquet_schema_sha256 != expected_schema_hash for shard in self.shards
        ):
            raise ValueError("cache shard schema hash differs from the declared registry")
        return self


class CenturyCacheExpectations(FrozenModel):
    """Run-specific identities required before an ordinary recovery may read."""

    utc_start: datetime
    utc_end_exclusive: datetime
    feature_vector_schema_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_ids: tuple[str, ...] = Field(min_length=1)
    required_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_source_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    parity_reference_source_locator: str = Field(min_length=1)
    parity_reference_source_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_audit_report_sha256: str = Field(pattern=SHA256_PATTERN)
    reconciliation_aggregate_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("cache expectation timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("required_feature_ids")
    @classmethod
    def require_canonical_feature_ids(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if values != tuple(sorted(set(values))):
            raise ValueError("required feature IDs must be sorted and unique")
        if any(re.fullmatch(FEATURE_ID_PATTERN, item) is None for item in values):
            raise ValueError("required feature ID is invalid")
        return values

    @model_validator(mode="after")
    def require_expectation_hash(self) -> CenturyCacheExpectations:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("cache expectation range must be positive")
        if self.required_feature_registry_sha256 != sha256_json(
            list(self.required_feature_ids)
        ):
            raise ValueError("required feature ID hash is inconsistent")
        return self


@dataclass(frozen=True, slots=True)
class VerifiedCenturyCache:
    cache_directory: Path
    manifest_path: Path
    manifest_sha256: str
    manifest: CenturyCacheManifest
    required_feature_coverage: float


def canonical_rows_sha256(rows: tuple[CenturyStateRecord, ...]) -> str:
    """Hash canonical row content independently of Parquet layout/sharding."""

    digest = hashlib.sha256()
    for row in rows:
        digest.update(canonical_json_bytes(row.model_dump(mode="json")))
        digest.update(b"\n")
    return digest.hexdigest()


def discrete_chart_identity_sha256(row: CenturyStateRecord) -> str:
    """Hash only discrete chart content and the mappings that give it meaning.

    Interval identifiers, timestamps, declared chart hashes, and boundary-event
    labels are intentionally excluded.  Two adjacent rows with this same identity
    describe one stable state and must have been merged before cache serialization.
    """

    return sha256_json(
        {
            "feature_vector_schema_version": row.feature_vector_schema_version,
            "semantic_feature_registry_sha256": (
                row.semantic_feature_registry_sha256
            ),
            "feature_registry_sha256": row.feature_registry_sha256,
            "feature_values": [
                item.model_dump(mode="json") for item in row.feature_values
            ],
            "node_convention": row.node_convention,
            "mandala_mapping_version": row.mandala_mapping_version,
            "mandala_mapping_sha256": row.mandala_mapping_sha256,
            "bodygraph_mapping_sha256": row.bodygraph_mapping_sha256,
        }
    )


def feature_registry_sha256(registry: tuple[FeatureColumnSpec, ...]) -> str:
    return sha256_json([item.model_dump(mode="json") for item in registry])


def required_feature_ids_sha256(feature_ids: tuple[str, ...]) -> str:
    return sha256_json(list(feature_ids))


_FIXED_PARQUET_COLUMNS: tuple[tuple[str, str], ...] = (
    ("schema_version", "string"),
    ("state_id", "string"),
    ("utc_start", "timestamp_us_utc"),
    ("utc_end", "timestamp_us_utc"),
    ("duration_seconds", "float64"),
    ("representative_utc", "timestamp_us_utc"),
    ("design_timestamp", "timestamp_us_utc"),
    ("chart_features_sha256", "string"),
    ("feature_vector_schema_version", "string"),
    ("semantic_feature_registry_sha256", "string"),
    ("feature_registry_sha256", "string"),
    ("astronomy_engine_version", "string"),
    ("ephemeris_file_set_sha256", "string"),
    ("node_convention", "string"),
    ("mandala_mapping_version", "string"),
    ("mandala_mapping_sha256", "string"),
    ("bodygraph_mapping_sha256", "string"),
    ("boundary_events", "string_list"),
)


def parquet_schema_sha256(registry: tuple[FeatureColumnSpec, ...]) -> str:
    """Hash the logical Arrow schema without depending on a PyArrow version."""

    return sha256_json(
        {
            "fixed_columns": _FIXED_PARQUET_COLUMNS,
            "feature_columns": [
                {
                    "column_name": item.parquet_column_name,
                    "feature_id": item.feature_id,
                    "storage_type": item.storage_type.value,
                    "nullable": item.nullable,
                }
                for item in registry
            ],
        }
    )
