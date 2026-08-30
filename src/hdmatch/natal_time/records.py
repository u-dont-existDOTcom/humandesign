"""Immutable manifest, freeze, result, and coverage records."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from hdmatch.natal_time.models import SHA256_PATTERN, NatalTimeModel
from hdmatch.natal_time.provenance import EngineProvenance, StateIdentitySpecification
from hdmatch.util import sha256_json


class FixtureClassification(StrEnum):
    SYNTHETIC = "synthetic"
    REAL_PRIVATE = "real_private"


class TimezoneResolution(NatalTimeModel):
    schema_version: Literal["natal-timezone-resolution-v1"] = "natal-timezone-resolution-v1"
    iana_timezone: str = Field(min_length=1)
    resolution_status: Literal["resolved"] = "resolved"
    resolution_method: str = Field(min_length=1)
    participant_confirmed: bool
    ambiguity_changes_instant_domain: Literal[False] = False
    timezone_database_version: str
    timezone_file_sha256: str = Field(pattern=SHA256_PATTERN)


class NatalTimeManifest(NatalTimeModel):
    schema_version: Literal["natal-time-manifest-v1"] = "natal-time-manifest-v1"
    manifest_id: str = Field(pattern=r"^NTM-[A-F0-9]{24}$")
    created_at_utc: datetime
    evidence_lineage_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_dates: tuple[date, ...] = Field(min_length=1)
    candidate_ordering: Literal["none"] = "none"
    timezone_resolution: TimezoneResolution
    engine_provenance: EngineProvenance
    state_identity_specification: StateIdentitySpecification
    state_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    privacy_classification: Literal["private_scientific"] = "private_scientific"
    fixture_classification: FixtureClassification
    relationship_evidence_included: Literal[False] = False
    supersedes_manifest_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @field_validator("created_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("candidate_dates")
    @classmethod
    def unique_dates(cls, value: tuple[date, ...]) -> tuple[date, ...]:
        if len(set(value)) != len(value):
            raise ValueError("manifest candidate dates must be unique")
        return tuple(sorted(value))

    @model_validator(mode="after")
    def bound_state_identity(self) -> NatalTimeManifest:
        if self.state_identity_sha256 != self.state_identity_specification.content_sha256:
            raise ValueError("manifest state-identity digest does not match its specification")
        if (
            self.timezone_resolution.timezone_file_sha256
            != self.engine_provenance.timezone_file_sha256
        ):
            raise ValueError("manifest timezone checksum does not match engine provenance")
        return self

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


class NatalTimeFreeze(NatalTimeModel):
    schema_version: Literal["natal-time-freeze-v1"] = "natal-time-freeze-v1"
    freeze_id: str = Field(pattern=r"^NTF-[A-F0-9]{24}$")
    created_at_utc: datetime
    creation_event: Literal["pre_validation_evidence_freeze"] = "pre_validation_evidence_freeze"
    manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    deterministic_computation_sha256: str = Field(pattern=SHA256_PATTERN)
    repository_commit: str = Field(min_length=7)
    engine_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    state_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    later_evidence_present: Literal[False] = False
    supersedes_freeze_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @field_validator("created_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("freeze timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


class LocalBoundary(NatalTimeModel):
    utc: datetime
    local: datetime
    utc_offset_seconds: int
    fold: Literal[0, 1]

    @field_validator("utc")
    @classmethod
    def utc_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("UTC boundary must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("local")
    @classmethod
    def local_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("local boundary must be timezone-aware")
        return value


class NatalTimeInterval(NatalTimeModel):
    schema_version: Literal["natal-time-interval-v1"] = "natal-time-interval-v1"
    civil_date: date
    start: LocalBoundary
    end: LocalBoundary
    representative_utc: datetime
    duration_microseconds: int = Field(gt=0)
    full_state_sha256: str = Field(pattern=SHA256_PATTERN)
    full_state: dict[str, Any]
    boundary_events: tuple[str, ...]
    reduced_signature_used_for_identity: Literal[False] = False

    @field_validator("representative_utc")
    @classmethod
    def representative_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("representative timestamp must be timezone-aware")
        return value.astimezone(UTC)


class CoverageReceipt(NatalTimeModel):
    schema_version: Literal["natal-time-coverage-receipt-v1"] = "natal-time-coverage-receipt-v1"
    civil_date: date
    iana_timezone: str
    domain_start: LocalBoundary
    domain_end: LocalBoundary
    actual_duration_microseconds: int = Field(gt=0)
    interval_count: int = Field(gt=0)
    interval_state_sha256: tuple[str, ...] = Field(min_length=1)
    summed_interval_duration_microseconds: int = Field(gt=0)
    coverage_complete: Literal[True] = True
    no_gaps: Literal[True] = True
    no_overlaps: Literal[True] = True
    all_intervals_positive: Literal[True] = True
    adjacent_states_distinct: Literal[True] = True
    boundary_sides_verified: Literal[True] = True
    maximality_verified: Literal[True] = True
    exactly_one_interval_per_representable_instant: Literal[True] = True
    boundary_method: str
    datetime_input_resolution_microseconds: Literal[1] = 1
    boundary_root_tolerance_seconds: float = Field(gt=0.0)
    rounding_convention: Literal["first_changed_representable_microsecond"] = (
        "first_changed_representable_microsecond"
    )

    @model_validator(mode="after")
    def totals_match(self) -> CoverageReceipt:
        if self.actual_duration_microseconds != self.summed_interval_duration_microseconds:
            raise ValueError("coverage receipt duration totals do not match")
        if self.interval_count != len(self.interval_state_sha256):
            raise ValueError("coverage receipt interval count does not match state digests")
        return self


class MechanicStatus(StrEnum):
    STABLE = "stable"
    VARIABLE = "variable"
    UNRESOLVED = "unresolved"


class MechanicFact(NatalTimeModel):
    path: str
    status: MechanicStatus
    stable_value: Any | None = None
    observed_values: tuple[Any, ...]
    interval_count: int = Field(gt=0)


class NatalTimeResult(NatalTimeModel):
    schema_version: Literal["natal-time-result-v1"] = "natal-time-result-v1"
    result_id: str = Field(pattern=r"^NTR-[A-F0-9]{24}$")
    created_at_utc: datetime
    manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    intervals: tuple[NatalTimeInterval, ...] = Field(min_length=1)
    coverage_receipts: tuple[CoverageReceipt, ...] = Field(min_length=1)
    mechanic_facts: tuple[MechanicFact, ...] = Field(min_length=1)
    candidate_ordering: Literal["none"] = "none"
    ranking_present: Literal[False] = False
    weights_present: Literal[False] = False
    probability_present: Literal[False] = False
    duration_used_as_evidence: Literal[False] = False
    relationship_evidence_included: Literal[False] = False

    @field_validator("created_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("result timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


def deterministic_computation_sha256(manifest: NatalTimeManifest) -> str:
    return sha256_json(
        {
            "candidate_dates": [value.isoformat() for value in manifest.candidate_dates],
            "candidate_ordering": manifest.candidate_ordering,
            "timezone_resolution": manifest.timezone_resolution.model_dump(mode="json"),
            "engine_provenance_sha256": manifest.engine_provenance.content_sha256,
            "state_identity_sha256": manifest.state_identity_sha256,
        }
    )
