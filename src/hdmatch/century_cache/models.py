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
    design_timestamp: datetime
    feature_vector_schema_version: str = Field(min_length=1)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    astronomy_engine_version: str = Field(min_length=1)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_values: tuple[FeatureValue, ...] = Field(min_length=1)

    @field_validator("utc_start", "utc_end", "design_timestamp")
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

    @model_validator(mode="after")
    def require_exact_interval(self) -> CenturyStateRecord:
        if self.utc_end <= self.utc_start:
            raise ValueError("century-cache interval must have positive duration")
        actual = (self.utc_end - self.utc_start).total_seconds()
        if abs(actual - self.duration_seconds) > 1e-6:
            raise ValueError("duration_seconds does not equal the exact interval duration")
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
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_coverage: float = Field(ge=0.0, le=1.0)
    calculation_tier: Literal["M2"]
    exact_intervals: Literal[True]
    canonical_row_hash_strategy: Literal["sha256-canonical-json-lines-v1"] = (
        LOGICAL_HASH_STRATEGY
    )
    storage_format: Literal["parquet-internal-zstd-v1"] = STORAGE_FORMAT
    engine: CenturyCacheEngineProvenance
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    parity_status: Literal["pass"]
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_audit_status: Literal["pass"]
    boundary_audit_report_sha256: str = Field(pattern=SHA256_PATTERN)
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


class CenturyCacheShard(FrozenModel):
    filename: str = Field(pattern=SHARD_NAME_PATTERN)
    sha256: str = Field(pattern=SHA256_PATTERN)
    row_count: int = Field(gt=0)
    utc_start: datetime
    utc_end_exclusive: datetime
    canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    parquet_schema_sha256: str = Field(pattern=SHA256_PATTERN)

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


class CenturyCacheManifest(FrozenModel):
    """Complete authoritative contract for a verified exact-state cache."""

    schema_version: Literal["century-cache-manifest-v1"] = "century-cache-manifest-v1"
    cache_version: Literal["century-cache-v1"] = "century-cache-v1"
    feature_vector_schema_version: str = Field(min_length=1)
    utc_start: datetime
    utc_end_exclusive: datetime
    interval_count: int = Field(gt=0)
    feature_registry: tuple[FeatureColumnSpec, ...] = Field(min_length=1)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_coverage: float = Field(ge=0.0, le=1.0)
    calculation_tier: Literal["M2"]
    exact_intervals: Literal[True]
    canonical_row_hash_strategy: Literal["sha256-canonical-json-lines-v1"]
    storage_format: Literal["parquet-internal-zstd-v1"]
    engine: CenturyCacheEngineProvenance
    node_convention: Literal["true"]
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    parity_status: Literal["pass"]
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_audit_status: Literal["pass"]
    boundary_audit_report_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    created_at_utc: datetime
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
    cache_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_ids: tuple[str, ...] = Field(min_length=1)
    required_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_source_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_audit_report_sha256: str = Field(pattern=SHA256_PATTERN)

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
    ("design_timestamp", "timestamp_us_utc"),
    ("feature_vector_schema_version", "string"),
    ("feature_registry_sha256", "string"),
    ("astronomy_engine_version", "string"),
    ("ephemeris_file_set_sha256", "string"),
    ("node_convention", "string"),
    ("mandala_mapping_version", "string"),
    ("mandala_mapping_sha256", "string"),
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
