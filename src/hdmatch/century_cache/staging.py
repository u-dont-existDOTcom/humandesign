"""Deterministic Phase-2 planning and replay-verified staged build jobs.

Staged receipts support resumability only.  They never recreate the private
factory capability carried by :class:`VerifiedExactStateBatch`; a new process
must re-hash, decode, and production-replay the exact scan range before the
persisted artifact may participate in canonical seam reconciliation.
"""

from __future__ import annotations

import math
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.chart.bodygraph import bodygraph_constants_sha256
from hdmatch.chart.boundaries import BOUNDARY_POLICY_VERSION
from hdmatch.chart.calculator import CHART_ENGINE_VERSION
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EphemerisMode,
    SwissCalculationAuditSnapshot,
    SwissEphemerisProvider,
)
from hdmatch.chart.feature_registry import CACHEABLE_M0_M2_REGISTRY
from hdmatch.chart.rave_mandala import (
    LINE_WIDTH_DEGREES,
    RAVE_MANDALA_VERSION,
    mandala_constants_sha256,
)
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.provenance.swisseph_files import (
    REQUIRED_EPHEMERIS_FILES,
    VerifiedEphemerisProvenance,
)

from .chart_adapter import (
    CACHEABLE_M0_M2_FEATURE_COLUMNS,
    CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256,
    CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256,
    VerifiedExactStateBatch,
    build_verified_exact_state_batch,
    validate_verified_exact_state_batch,
)
from .models import (
    ExactStateBatchProvenance,
    canonical_rows_sha256,
    parquet_schema_sha256,
)
from .parquet import read_parquet_shard, write_parquet_shard_new

SHA256_PATTERN = r"^[a-f0-9]{64}$"
GIT_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
JOB_ID_PATTERN = r"^utc-year-[0-9]{4}$"
ARTIFACT_FILENAME_PATTERN = r"^staged-utc-year-[0-9]{4}\.parquet\.zst$"
RECEIPT_FILENAME_PATTERN = r"^staged-utc-year-[0-9]{4}\.receipt\.json$"

CANONICAL_CENTURY_START_UTC = datetime(1926, 8, 22, tzinfo=UTC)
CANONICAL_CENTURY_END_EXCLUSIVE_UTC = datetime(2026, 8, 23, tzinfo=UTC)
DEFAULT_DESIGN_ROOT_TIME_TOLERANCE_SECONDS = 0.01
DEFAULT_DESIGN_ROOT_ARC_TOLERANCE_DEGREES = 1e-8


class StagedCenturyBuildError(ValueError):
    """A plan, staged artifact, receipt, or replay binding failed closed."""


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class CenturyBuildJobV1(_FrozenModel):
    """One UTC-calendar-year core plus its explicitly derived scan overlap."""

    schema_version: Literal["century-build-job-v1"] = "century-build-job-v1"
    job_id: str = Field(pattern=JOB_ID_PATTERN)
    ordinal: int = Field(ge=0)
    core_utc_start: datetime
    core_utc_end_exclusive: datetime
    scan_utc_start: datetime
    scan_utc_end_exclusive: datetime

    @field_validator(
        "core_utc_start",
        "core_utc_end_exclusive",
        "scan_utc_start",
        "scan_utc_end_exclusive",
    )
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("century build job timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_valid_ranges(self) -> CenturyBuildJobV1:
        if self.core_utc_end_exclusive <= self.core_utc_start:
            raise ValueError("century build job core range must be positive")
        if self.scan_utc_end_exclusive <= self.scan_utc_start:
            raise ValueError("century build job scan range must be positive")
        if not (
            self.scan_utc_start
            <= self.core_utc_start
            < self.core_utc_end_exclusive
            <= self.scan_utc_end_exclusive
        ):
            raise ValueError("century build job scan range must contain its core range")
        expected_id = f"utc-year-{self.core_utc_start.year:04d}"
        if self.job_id != expected_id:
            raise ValueError("century build job ID differs from its UTC core year")
        next_year = datetime(self.core_utc_start.year + 1, 1, 1, tzinfo=UTC)
        if self.core_utc_end_exclusive > next_year:
            raise ValueError("century build job core crosses a UTC calendar-year boundary")
        return self


class SwissEngineBuildIdentityV1(_FrozenModel):
    """Path-free engine identity shared by the plan and every job receipt."""

    schema_version: Literal["swiss-engine-build-identity-v1"] = (
        "swiss-engine-build-identity-v1"
    )
    provider: Literal["swiss_ephemeris_local_files"]
    swiss_library_version: str = Field(min_length=1)
    requested_ephemeris: Literal[EphemerisMode.SWIEPH] = EphemerisMode.SWIEPH
    requested_flags: int = Field(gt=0)
    ephemeris_mask: int = Field(gt=0)
    swieph_flag: int = Field(gt=0)
    node_convention: Literal["true"]
    provider_configuration_sha256: str = Field(pattern=SHA256_PATTERN)
    canonical_ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_provenance: VerifiedEphemerisProvenance

    @model_validator(mode="after")
    def require_swieph(self) -> SwissEngineBuildIdentityV1:
        if self.requested_flags & self.ephemeris_mask != self.swieph_flag:
            raise ValueError("build engine request is not exactly SWIEPH")
        if self.swieph_flag & self.ephemeris_mask != self.swieph_flag:
            raise ValueError("build engine SWIEPH flag is outside the ephemeris mask")
        if self.canonical_ephemeris_file_set_sha256 != (
            self.ephemeris_provenance.ephemeris_file_set_sha256
        ):
            raise ValueError("build engine file-set identity is inconsistent")
        return self


class CenturyBuildPlanV1(_FrozenModel):
    """Frozen deterministic plan for the canonical or a bounded test horizon."""

    schema_version: Literal["century-build-plan-v1"] = "century-build-plan-v1"
    planning_policy_version: Literal["utc-calendar-year-overlap-v1"] = (
        "utc-calendar-year-overlap-v1"
    )
    utc_start: datetime
    utc_end_exclusive: datetime
    source_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    source_tree_dirty: Literal[False]
    engine_validation_status: Literal["pass"] = "pass"
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    parity_status: Literal["pass"] = "pass"
    parity_report_sha256: str = Field(pattern=SHA256_PATTERN)
    parity_reference_source_locator: str = Field(min_length=1)
    parity_reference_source_sha256: str = Field(pattern=SHA256_PATTERN)
    engine: SwissEngineBuildIdentityV1
    calculation_tier: Literal["M2"] = "M2"
    exact_intervals: Literal[True] = True
    chart_engine_version: Literal["chart-engine-v1"] = "chart-engine-v1"
    boundary_policy_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    physical_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    mandala_mapping_version: str = Field(min_length=1)
    mandala_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    design_root_time_tolerance_seconds: float = Field(gt=0.0)
    design_root_arc_tolerance_degrees: float = Field(gt=0.0)
    overlap_derivation: Literal["one-solar-line-at-frozen-minimum-speed-v1"] = (
        "one-solar-line-at-frozen-minimum-speed-v1"
    )
    solar_line_width_degrees: float = Field(gt=0.0)
    minimum_solar_speed_degrees_per_day: float = Field(gt=0.0)
    overlap_scan_seconds: int = Field(gt=0)
    jobs: tuple[CenturyBuildJobV1, ...] = Field(min_length=1)

    @field_validator("utc_start", "utc_end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("century build plan timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_deterministic_plan(self) -> CenturyBuildPlanV1:
        if self.utc_end_exclusive <= self.utc_start:
            raise ValueError("century build plan range must be positive")
        if self.boundary_policy_version != BOUNDARY_POLICY_VERSION:
            raise ValueError("century build plan boundary policy is stale")
        if self.chart_engine_version != CHART_ENGINE_VERSION:
            raise ValueError("century build plan chart engine is stale")
        if self.semantic_feature_registry_sha256 != (
            CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256
        ):
            raise ValueError("century build plan semantic registry is stale")
        if self.physical_feature_registry_sha256 != (
            CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256
        ):
            raise ValueError("century build plan physical registry is stale")
        if self.mandala_mapping_version != RAVE_MANDALA_VERSION or (
            self.mandala_mapping_sha256 != mandala_constants_sha256()
        ):
            raise ValueError("century build plan Mandala identity is stale")
        if self.bodygraph_mapping_sha256 != bodygraph_constants_sha256():
            raise ValueError("century build plan Bodygraph identity is stale")
        if self.design_root_arc_tolerance_degrees != (
            DEFAULT_DESIGN_ROOT_ARC_TOLERANCE_DEGREES
        ):
            raise ValueError("century build plan Design arc tolerance is not frozen")
        expected_overlap = _derive_overlap_scan_seconds(
            solar_line_width_degrees=self.solar_line_width_degrees,
            minimum_solar_speed_degrees_per_day=(
                self.minimum_solar_speed_degrees_per_day
            ),
            root_tolerance_seconds=self.design_root_time_tolerance_seconds,
        )
        if self.overlap_scan_seconds != expected_overlap:
            raise ValueError("century build plan overlap is not deterministically derived")
        expected_jobs = _derive_jobs(
            self.utc_start,
            self.utc_end_exclusive,
            overlap_scan_seconds=self.overlap_scan_seconds,
        )
        if self.jobs != expected_jobs:
            raise ValueError("century build plan jobs differ from the canonical derivation")
        return self


class SwissCalculationAuditV1(_FrozenModel):
    """Path-free all-call SWIEPH evidence for one exact-state build/replay."""

    schema_version: Literal["swiss-calculation-audit-v1"] = (
        "swiss-calculation-audit-v1"
    )
    verification_status: Literal["pass"]
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    canonical_ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    requested_flags: int = Field(gt=0)
    ephemeris_mask: int = Field(gt=0)
    swieph_flag: int = Field(gt=0)
    calculation_call_count: int = Field(gt=0)
    requested_flags_counts: tuple[tuple[int, int], ...] = Field(min_length=1)
    returned_flags_counts: tuple[tuple[int, int], ...] = Field(min_length=1)
    returned_mode_bits_counts: tuple[tuple[int, int], ...] = Field(min_length=1)
    calculated_body_counts: tuple[tuple[str, int], ...] = Field(min_length=1)
    used_file_counts: tuple[tuple[str, str, int, int], ...] = Field(min_length=1)
    calculation_trace_sha256: str = Field(pattern=SHA256_PATTERN)
    first_calculation_sha256: str = Field(pattern=SHA256_PATTERN)
    final_calculation_sha256: str = Field(pattern=SHA256_PATTERN)
    entry_provider_configuration_sha256: str = Field(pattern=SHA256_PATTERN)
    exit_provider_configuration_sha256: str = Field(pattern=SHA256_PATTERN)
    entry_ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    exit_ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_complete_swieph_trace(self) -> SwissCalculationAuditV1:
        count = self.calculation_call_count
        for label, entries in (
            ("requested flags", self.requested_flags_counts),
            ("returned flags", self.returned_flags_counts),
            ("returned mode bits", self.returned_mode_bits_counts),
            ("calculated bodies", self.calculated_body_counts),
        ):
            if entries != tuple(sorted(entries)) or len({item[0] for item in entries}) != len(
                entries
            ):
                raise ValueError(f"Swiss audit {label} counts are not canonical")
            if any(item[1] <= 0 for item in entries) or sum(
                item[1] for item in entries
            ) != count:
                raise ValueError(f"Swiss audit {label} counts are incomplete")
        if self.requested_flags_counts != ((self.requested_flags, count),):
            raise ValueError("Swiss audit did not use one frozen request flag set")
        if self.requested_flags & self.ephemeris_mask != self.swieph_flag:
            raise ValueError("Swiss audit request is not SWIEPH")
        if self.returned_mode_bits_counts != ((self.swieph_flag, count),):
            raise ValueError("Swiss audit contains a non-SWIEPH returned mode")
        if any(
            flags & self.ephemeris_mask != self.swieph_flag
            for flags, _flag_count in self.returned_flags_counts
        ):
            raise ValueError("Swiss audit returned flags contain fallback")
        if self.used_file_counts != tuple(sorted(self.used_file_counts)):
            raise ValueError("Swiss audit used-file counts are not canonical")
        if any(item[3] <= 0 for item in self.used_file_counts) or sum(
            item[3] for item in self.used_file_counts
        ) != count:
            raise ValueError("Swiss audit used-file identities do not cover every call")
        if self.entry_provider_configuration_sha256 != (
            self.exit_provider_configuration_sha256
        ):
            raise ValueError("Swiss provider configuration changed during the build")
        if self.entry_ephemeris_file_set_sha256 != (
            self.exit_ephemeris_file_set_sha256
        ):
            raise ValueError("Swiss ephemeris file set changed during the build")
        if self.entry_ephemeris_file_set_sha256 != (
            self.canonical_ephemeris_file_set_sha256
        ):
            raise ValueError("Swiss audit file set differs from canonical provenance")
        return self


class StagedExactStateBatchReceiptV1(_FrozenModel):
    """Receipt-last resumability claim for one atomic staged Parquet artifact."""

    schema_version: Literal["staged-exact-state-batch-receipt-v1"] = (
        "staged-exact-state-batch-receipt-v1"
    )
    verification_status: Literal["pass"]
    plan_sha256: str = Field(pattern=SHA256_PATTERN)
    job_sha256: str = Field(pattern=SHA256_PATTERN)
    job_id: str = Field(pattern=JOB_ID_PATTERN)
    source_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    source_tree_dirty: Literal[False]
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    physical_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    core_utc_start: datetime
    core_utc_end_exclusive: datetime
    scan_utc_start: datetime
    scan_utc_end_exclusive: datetime
    artifact_filename: str = Field(pattern=ARTIFACT_FILENAME_PATTERN)
    artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    artifact_size_bytes: int = Field(gt=0)
    parquet_schema_sha256: str = Field(pattern=SHA256_PATTERN)
    interval_count: int = Field(gt=0)
    boundary_event_count: int = Field(ge=0)
    canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    exact_state_batch_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    exact_state_batch_provenance: ExactStateBatchProvenance
    swiss_calculation_audit: SwissCalculationAuditV1
    created_at_utc: datetime

    @field_validator(
        "core_utc_start",
        "core_utc_end_exclusive",
        "scan_utc_start",
        "scan_utc_end_exclusive",
        "created_at_utc",
    )
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("staged receipt timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_internal_bindings(self) -> StagedExactStateBatchReceiptV1:
        provenance = self.exact_state_batch_provenance
        if self.exact_state_batch_provenance_sha256 != sha256_json(
            provenance.model_dump(mode="json")
        ):
            raise ValueError("staged receipt exact-state provenance hash is inconsistent")
        if self.scan_utc_start != provenance.utc_start or (
            self.scan_utc_end_exclusive != provenance.utc_end_exclusive
        ):
            raise ValueError("staged receipt scan range differs from exact provenance")
        if self.interval_count != provenance.interval_count:
            raise ValueError("staged receipt interval count differs from exact provenance")
        if self.boundary_event_count != provenance.boundary_event_count:
            raise ValueError("staged receipt event count differs from exact provenance")
        if self.canonical_rows_sha256 != provenance.canonical_rows_sha256:
            raise ValueError("staged receipt row hash differs from exact provenance")
        if self.boundary_policy_version != provenance.boundary_policy_version:
            raise ValueError("staged receipt boundary policy differs from exact provenance")
        if self.semantic_feature_registry_sha256 != (
            provenance.semantic_feature_registry_sha256
        ):
            raise ValueError("staged receipt semantic registry differs from exact provenance")
        if self.physical_feature_registry_sha256 != provenance.feature_registry_sha256:
            raise ValueError("staged receipt physical registry differs from exact provenance")
        if self.engine_identity_sha256 != (
            self.swiss_calculation_audit.engine_identity_sha256
        ):
            raise ValueError("staged receipt engine identity differs from its audit")
        return self


class StagedExactStateReplayVerificationV1(_FrozenModel):
    """Independent deterministic replay evidence for one producer receipt."""

    schema_version: Literal["staged-exact-state-replay-verification-v1"] = (
        "staged-exact-state-replay-verification-v1"
    )
    verification_status: Literal["pass"]
    plan_sha256: str = Field(pattern=SHA256_PATTERN)
    job_sha256: str = Field(pattern=SHA256_PATTERN)
    job_id: str = Field(pattern=JOB_ID_PATTERN)
    source_commit: str = Field(pattern=GIT_COMMIT_PATTERN)
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    producer_receipt_sha256: str = Field(pattern=SHA256_PATTERN)
    artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    artifact_size_bytes: int = Field(gt=0)
    persisted_canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    replay_canonical_rows_sha256: str = Field(pattern=SHA256_PATTERN)
    interval_count: int = Field(gt=0)
    boundary_event_count: int = Field(ge=0)
    producer_exact_state_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    replay_exact_state_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    producer_swiss_calculation_audit_sha256: str = Field(pattern=SHA256_PATTERN)
    replay_swiss_calculation_audit_sha256: str = Field(pattern=SHA256_PATTERN)
    artifact_bytes_match: Literal[True]
    logical_rows_match: Literal[True]
    partition_and_events_match: Literal[True]
    all_call_swieph_audit_match: Literal[True]

    @model_validator(mode="after")
    def require_equal_replay_bindings(self) -> StagedExactStateReplayVerificationV1:
        if self.persisted_canonical_rows_sha256 != self.replay_canonical_rows_sha256:
            raise ValueError("replay verification row hashes differ")
        if self.producer_exact_state_provenance_sha256 != (
            self.replay_exact_state_provenance_sha256
        ):
            raise ValueError("replay verification exact-state provenances differ")
        if self.producer_swiss_calculation_audit_sha256 != (
            self.replay_swiss_calculation_audit_sha256
        ):
            raise ValueError("replay verification Swiss audits differ")
        return self


class VerifiedStagedExactStateBatch:
    """In-process replay-minted batch plus canonical producer/replay evidence."""

    __slots__ = (
        "_batch",
        "_factory_token",
        "_producer_receipt",
        "_producer_receipt_sha256",
        "_replay_verification",
        "_replay_verification_sha256",
    )
    _batch: VerifiedExactStateBatch
    _factory_token: object
    _producer_receipt: StagedExactStateBatchReceiptV1
    _producer_receipt_sha256: str
    _replay_verification: StagedExactStateReplayVerificationV1
    _replay_verification_sha256: str

    def __init__(
        self,
        *,
        batch: VerifiedExactStateBatch,
        producer_receipt: StagedExactStateBatchReceiptV1,
        producer_receipt_sha256: str,
        replay_verification: StagedExactStateReplayVerificationV1,
        replay_verification_sha256: str,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _VERIFIED_STAGED_EXACT_STATE_BATCH_FACTORY_TOKEN:
            raise StagedCenturyBuildError(
                "verified staged batches must be minted by deterministic replay"
            )
        object.__setattr__(self, "_batch", batch)
        object.__setattr__(self, "_producer_receipt", producer_receipt)
        object.__setattr__(
            self, "_producer_receipt_sha256", producer_receipt_sha256
        )
        object.__setattr__(self, "_replay_verification", replay_verification)
        object.__setattr__(
            self, "_replay_verification_sha256", replay_verification_sha256
        )
        object.__setattr__(self, "_factory_token", _factory_token)

    def __setattr__(self, name: str, value: object) -> None:
        del name, value
        raise AttributeError("VerifiedStagedExactStateBatch is immutable")

    @property
    def batch(self) -> VerifiedExactStateBatch:
        return self._batch

    @property
    def producer_receipt(self) -> StagedExactStateBatchReceiptV1:
        return self._producer_receipt

    @property
    def producer_receipt_sha256(self) -> str:
        return self._producer_receipt_sha256

    @property
    def replay_verification(self) -> StagedExactStateReplayVerificationV1:
        return self._replay_verification

    @property
    def replay_verification_sha256(self) -> str:
        return self._replay_verification_sha256


_VERIFIED_STAGED_EXACT_STATE_BATCH_FACTORY_TOKEN: Final[object] = object()


def staged_replay_verification_sha256(
    verification: StagedExactStateReplayVerificationV1,
) -> str:
    return sha256_json(verification.model_dump(mode="json"))


def validate_verified_staged_exact_state_batch(
    source: VerifiedStagedExactStateBatch,
) -> StagedExactStateReplayVerificationV1:
    """Recheck the replay-factory capability and all in-memory evidence bindings."""

    if not isinstance(source, VerifiedStagedExactStateBatch) or (
        source._factory_token is not _VERIFIED_STAGED_EXACT_STATE_BATCH_FACTORY_TOKEN
    ):
        raise StagedCenturyBuildError(
            "staged exact-state batch lacks deterministic-replay factory capability"
        )
    try:
        provenance = validate_verified_exact_state_batch(source.batch)
        receipt = StagedExactStateBatchReceiptV1.model_validate(
            source.producer_receipt.model_dump(mode="python")
        )
        replay = StagedExactStateReplayVerificationV1.model_validate(
            source.replay_verification.model_dump(mode="python")
        )
    except (TypeError, ValueError) as exc:
        raise StagedCenturyBuildError(
            "verified staged batch contains invalid replay evidence"
        ) from exc
    receipt_sha256 = sha256_json(receipt.model_dump(mode="json"))
    replay_sha256 = staged_replay_verification_sha256(replay)
    provenance_sha256 = sha256_json(provenance.model_dump(mode="json"))
    audit_sha256 = sha256_json(
        receipt.swiss_calculation_audit.model_dump(mode="json")
    )
    expected: dict[str, tuple[object, object]] = {
        "producer receipt hash": (source.producer_receipt_sha256, receipt_sha256),
        "replay verification hash": (
            source.replay_verification_sha256,
            replay_sha256,
        ),
        "replay producer receipt": (replay.producer_receipt_sha256, receipt_sha256),
        "build plan": (replay.plan_sha256, receipt.plan_sha256),
        "build job": (replay.job_sha256, receipt.job_sha256),
        "job ID": (replay.job_id, receipt.job_id),
        "source commit": (replay.source_commit, receipt.source_commit),
        "engine identity": (
            replay.engine_identity_sha256,
            receipt.engine_identity_sha256,
        ),
        "artifact": (replay.artifact_sha256, receipt.artifact_sha256),
        "artifact size": (replay.artifact_size_bytes, receipt.artifact_size_bytes),
        "row hash": (replay.replay_canonical_rows_sha256, canonical_rows_sha256(source.batch.rows)),
        "interval count": (replay.interval_count, len(source.batch.rows)),
        "event count": (
            replay.boundary_event_count,
            sum(len(row.boundary_events) for row in source.batch.rows),
        ),
        "exact-state provenance": (
            replay.replay_exact_state_provenance_sha256,
            provenance_sha256,
        ),
        "producer exact-state provenance": (
            receipt.exact_state_batch_provenance_sha256,
            provenance_sha256,
        ),
        "producer Swiss audit": (
            replay.producer_swiss_calculation_audit_sha256,
            audit_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise StagedCenturyBuildError(
                f"verified staged batch {label} binding changed"
            )
    return replay


def _derive_overlap_scan_seconds(
    *,
    solar_line_width_degrees: float,
    minimum_solar_speed_degrees_per_day: float,
    root_tolerance_seconds: float,
) -> int:
    return math.ceil(
        solar_line_width_degrees
        / minimum_solar_speed_degrees_per_day
        * 86_400.0
        + 2.0 * root_tolerance_seconds
    )


def _require_utc_datetime(value: datetime, *, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise StagedCenturyBuildError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _derive_jobs(
    start_utc: datetime,
    end_utc: datetime,
    *,
    overlap_scan_seconds: int,
) -> tuple[CenturyBuildJobV1, ...]:
    jobs: list[CenturyBuildJobV1] = []
    overlap = timedelta(seconds=overlap_scan_seconds)
    year = start_utc.year
    while True:
        year_start = datetime(year, 1, 1, tzinfo=UTC)
        next_year = datetime(year + 1, 1, 1, tzinfo=UTC)
        core_start = max(start_utc, year_start)
        core_end = min(end_utc, next_year)
        if core_start < core_end:
            jobs.append(
                CenturyBuildJobV1(
                    job_id=f"utc-year-{year:04d}",
                    ordinal=len(jobs),
                    core_utc_start=core_start,
                    core_utc_end_exclusive=core_end,
                    scan_utc_start=max(start_utc, core_start - overlap),
                    scan_utc_end_exclusive=min(end_utc, core_end + overlap),
                )
            )
        if next_year >= end_utc:
            break
        year += 1
    return tuple(jobs)


def _provider_path_free_file_set(
    provider: SwissEphemerisProvider,
) -> tuple[dict[str, object], ...]:
    by_name = {Path(item.path).name: item for item in provider.metadata.files}
    try:
        return tuple(
            {
                "bytes": by_name[name].size_bytes,
                "name": name,
                "sha256": by_name[name].sha256,
            }
            for name in REQUIRED_EPHEMERIS_FILES
        )
    except KeyError as exc:
        raise StagedCenturyBuildError(
            "Swiss provider does not expose the canonical pinned file set"
        ) from exc


def _engine_identity_from_provider(
    provider: SwissEphemerisProvider,
    ephemeris_provenance: VerifiedEphemerisProvenance,
) -> SwissEngineBuildIdentityV1:
    provider.verify_production_configuration()
    metadata = provider.metadata
    if (
        metadata.requested_ephemeris is not EphemerisMode.SWIEPH
        or metadata.requested_flags is None
        or metadata.ephemeris_mask is None
        or metadata.node_convention.value != "true"
    ):
        raise StagedCenturyBuildError("provider is not a frozen true-Node SWIEPH engine")
    observed_files = _provider_path_free_file_set(provider)
    expected_files = tuple(
        {
            "bytes": item.bytes,
            "name": item.name,
            "sha256": item.sha256,
        }
        for item in ephemeris_provenance.files
    )
    if observed_files != expected_files:
        raise StagedCenturyBuildError(
            "provider file bytes differ from verified ephemeris provenance"
        )
    observed_file_set_sha256 = sha256_json(list(observed_files))
    if observed_file_set_sha256 != ephemeris_provenance.ephemeris_file_set_sha256:
        raise StagedCenturyBuildError("provider ephemeris file-set hash is inconsistent")
    swieph_flag = metadata.requested_flags & metadata.ephemeris_mask
    provider_configuration_sha256, audit_file_set_sha256 = (
        provider.calculation_audit_identity_hashes()
    )
    if audit_file_set_sha256 != observed_file_set_sha256:
        raise StagedCenturyBuildError("provider audit file-set hash is inconsistent")
    return SwissEngineBuildIdentityV1(
        provider="swiss_ephemeris_local_files",
        swiss_library_version=metadata.library_version,
        requested_ephemeris=EphemerisMode.SWIEPH,
        requested_flags=metadata.requested_flags,
        ephemeris_mask=metadata.ephemeris_mask,
        swieph_flag=swieph_flag,
        node_convention="true",
        provider_configuration_sha256=provider_configuration_sha256,
        canonical_ephemeris_file_set_sha256=audit_file_set_sha256,
        ephemeris_provenance=ephemeris_provenance,
    )


def create_century_build_plan(
    provider: SwissEphemerisProvider,
    ephemeris_provenance: VerifiedEphemerisProvenance,
    *,
    utc_start: datetime,
    utc_end_exclusive: datetime,
    source_commit: str,
    source_tree_dirty: Literal[False],
    engine_validation_sha256: str,
    parity_report_sha256: str,
    parity_reference_source_locator: str,
    parity_reference_source_sha256: str,
    design_root_time_tolerance_seconds: float = (
        DEFAULT_DESIGN_ROOT_TIME_TOLERANCE_SECONDS
    ),
) -> CenturyBuildPlanV1:
    """Create a deterministic calendar-year build plan with derived overlaps."""

    start = _require_utc_datetime(utc_start, label="build-plan UTC start")
    end = _require_utc_datetime(
        utc_end_exclusive,
        label="build-plan UTC end",
    )
    minimum_solar_speed = provider.min_solar_speed_degrees_per_day()
    overlap_seconds = _derive_overlap_scan_seconds(
        solar_line_width_degrees=LINE_WIDTH_DEGREES,
        minimum_solar_speed_degrees_per_day=minimum_solar_speed,
        root_tolerance_seconds=design_root_time_tolerance_seconds,
    )
    return CenturyBuildPlanV1(
        utc_start=start,
        utc_end_exclusive=end,
        source_commit=source_commit,
        source_tree_dirty=source_tree_dirty,
        engine_validation_sha256=engine_validation_sha256,
        parity_report_sha256=parity_report_sha256,
        parity_reference_source_locator=parity_reference_source_locator,
        parity_reference_source_sha256=parity_reference_source_sha256,
        engine=_engine_identity_from_provider(provider, ephemeris_provenance),
        boundary_policy_version=BOUNDARY_POLICY_VERSION,
        semantic_feature_registry_sha256=(
            CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256
        ),
        physical_feature_registry_sha256=CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256,
        mandala_mapping_version=RAVE_MANDALA_VERSION,
        mandala_mapping_sha256=mandala_constants_sha256(),
        bodygraph_mapping_sha256=bodygraph_constants_sha256(),
        design_root_time_tolerance_seconds=design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=(
            DEFAULT_DESIGN_ROOT_ARC_TOLERANCE_DEGREES
        ),
        solar_line_width_degrees=LINE_WIDTH_DEGREES,
        minimum_solar_speed_degrees_per_day=minimum_solar_speed,
        overlap_scan_seconds=overlap_seconds,
        jobs=_derive_jobs(start, end, overlap_scan_seconds=overlap_seconds),
    )


def create_canonical_century_build_plan(
    provider: SwissEphemerisProvider,
    ephemeris_provenance: VerifiedEphemerisProvenance,
    *,
    source_commit: str,
    source_tree_dirty: Literal[False],
    engine_validation_sha256: str,
    parity_report_sha256: str,
    parity_reference_source_locator: str,
    parity_reference_source_sha256: str,
    design_root_time_tolerance_seconds: float = (
        DEFAULT_DESIGN_ROOT_TIME_TOLERANCE_SECONDS
    ),
) -> CenturyBuildPlanV1:
    """Create the frozen 1926-08-22 through 2026-08-23 production plan."""

    return create_century_build_plan(
        provider,
        ephemeris_provenance,
        utc_start=CANONICAL_CENTURY_START_UTC,
        utc_end_exclusive=CANONICAL_CENTURY_END_EXCLUSIVE_UTC,
        source_commit=source_commit,
        source_tree_dirty=source_tree_dirty,
        engine_validation_sha256=engine_validation_sha256,
        parity_report_sha256=parity_report_sha256,
        parity_reference_source_locator=parity_reference_source_locator,
        parity_reference_source_sha256=parity_reference_source_sha256,
        design_root_time_tolerance_seconds=design_root_time_tolerance_seconds,
    )


def century_build_plan_sha256(plan: CenturyBuildPlanV1) -> str:
    checked = CenturyBuildPlanV1.model_validate(plan.model_dump(mode="python"), strict=True)
    return sha256_json(checked.model_dump(mode="json"))


def century_build_job_sha256(job: CenturyBuildJobV1) -> str:
    checked = CenturyBuildJobV1.model_validate(job.model_dump(mode="python"), strict=True)
    return sha256_json(checked.model_dump(mode="json"))


def staged_job_artifact_path(
    staging_directory: str | Path,
    job: CenturyBuildJobV1,
) -> Path:
    return Path(staging_directory) / f"staged-{job.job_id}.parquet.zst"


def staged_job_receipt_path(
    staging_directory: str | Path,
    job: CenturyBuildJobV1,
) -> Path:
    return Path(staging_directory) / f"staged-{job.job_id}.receipt.json"


def _require_plan_job(plan: CenturyBuildPlanV1, job: CenturyBuildJobV1) -> None:
    checked_plan = CenturyBuildPlanV1.model_validate(
        plan.model_dump(mode="python"), strict=True
    )
    checked_job = CenturyBuildJobV1.model_validate(job.model_dump(mode="python"), strict=True)
    if checked_job.ordinal >= len(checked_plan.jobs) or (
        checked_plan.jobs[checked_job.ordinal] != checked_job
    ):
        raise StagedCenturyBuildError("job is not the declared member of this build plan")


def _require_provider_matches_plan(
    provider: SwissEphemerisProvider,
    plan: CenturyBuildPlanV1,
) -> None:
    actual = _engine_identity_from_provider(provider, plan.engine.ephemeris_provenance)
    if actual != plan.engine:
        raise StagedCenturyBuildError("current Swiss engine differs from the build plan")
    if provider.min_solar_speed_degrees_per_day() != (
        plan.minimum_solar_speed_degrees_per_day
    ):
        raise StagedCenturyBuildError("current solar speed bound differs from the build plan")


def certify_swiss_calculation_audit(
    snapshot: SwissCalculationAuditSnapshot,
    *,
    engine_identity: SwissEngineBuildIdentityV1,
) -> SwissCalculationAuditV1:
    """Mint a passing typed audit only from a complete all-SWIEPH snapshot."""

    if snapshot.first_calculation_sha256 is None or (
        snapshot.final_calculation_sha256 is None
    ):
        raise StagedCenturyBuildError("Swiss calculation audit contains no direct calls")
    expected_engine_fields = (
        (snapshot.requested_flags, engine_identity.requested_flags),
        (snapshot.ephemeris_mask, engine_identity.ephemeris_mask),
        (snapshot.swieph_flag, engine_identity.swieph_flag),
        (
            snapshot.entry_provider_configuration_sha256,
            engine_identity.provider_configuration_sha256,
        ),
        (
            snapshot.exit_provider_configuration_sha256,
            engine_identity.provider_configuration_sha256,
        ),
        (
            snapshot.entry_ephemeris_file_set_sha256,
            engine_identity.canonical_ephemeris_file_set_sha256,
        ),
        (
            snapshot.exit_ephemeris_file_set_sha256,
            engine_identity.canonical_ephemeris_file_set_sha256,
        ),
    )
    if any(actual != required for actual, required in expected_engine_fields):
        raise StagedCenturyBuildError(
            "Swiss calculation audit differs from the frozen engine identity"
        )
    valid_body_names = {body.value for body in CelestialBody}
    if any(name not in valid_body_names for name, _count in snapshot.calculated_body_counts):
        raise StagedCenturyBuildError("Swiss calculation audit contains an unknown body")
    expected_files = {
        (item.name, item.sha256, item.bytes)
        for item in engine_identity.ephemeris_provenance.files
    }
    if any(
        (name, digest, size) not in expected_files
        for name, digest, size, _count in snapshot.used_file_counts
    ):
        raise StagedCenturyBuildError(
            "Swiss calculation audit contains an undeclared used file"
        )
    return SwissCalculationAuditV1(
        verification_status="pass",
        engine_identity_sha256=sha256_json(engine_identity.model_dump(mode="json")),
        canonical_ephemeris_file_set_sha256=(
            engine_identity.canonical_ephemeris_file_set_sha256
        ),
        requested_flags=snapshot.requested_flags,
        ephemeris_mask=snapshot.ephemeris_mask,
        swieph_flag=snapshot.swieph_flag,
        calculation_call_count=snapshot.calculation_call_count,
        requested_flags_counts=snapshot.requested_flags_counts,
        returned_flags_counts=snapshot.returned_flags_counts,
        returned_mode_bits_counts=snapshot.returned_mode_bits_counts,
        calculated_body_counts=snapshot.calculated_body_counts,
        used_file_counts=snapshot.used_file_counts,
        calculation_trace_sha256=snapshot.calculation_trace_sha256,
        first_calculation_sha256=snapshot.first_calculation_sha256,
        final_calculation_sha256=snapshot.final_calculation_sha256,
        entry_provider_configuration_sha256=(
            snapshot.entry_provider_configuration_sha256
        ),
        exit_provider_configuration_sha256=snapshot.exit_provider_configuration_sha256,
        entry_ephemeris_file_set_sha256=(
            snapshot.entry_ephemeris_file_set_sha256
        ),
        exit_ephemeris_file_set_sha256=snapshot.exit_ephemeris_file_set_sha256,
    )


def _build_audited_batch(
    provider: SwissEphemerisProvider,
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
) -> tuple[VerifiedExactStateBatch, SwissCalculationAuditV1]:
    with provider.capture_calculation_audit() as capture:
        batch = build_verified_exact_state_batch(
            provider,
            job.scan_utc_start,
            job.scan_utc_end_exclusive,
            root_tolerance_seconds=plan.design_root_time_tolerance_seconds,
            required_registry=CACHEABLE_M0_M2_REGISTRY,
        )
    audit = certify_swiss_calculation_audit(
        capture.snapshot(),
        engine_identity=plan.engine,
    )
    return batch, audit


def _require_batch_matches_plan_job(
    batch: VerifiedExactStateBatch,
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
) -> ExactStateBatchProvenance:
    provenance = validate_verified_exact_state_batch(batch)
    expected = {
        "scan start": (provenance.utc_start, job.scan_utc_start),
        "scan end": (provenance.utc_end_exclusive, job.scan_utc_end_exclusive),
        "boundary policy": (
            provenance.boundary_policy_version,
            plan.boundary_policy_version,
        ),
        "semantic registry": (
            provenance.semantic_feature_registry_sha256,
            plan.semantic_feature_registry_sha256,
        ),
        "physical registry": (
            provenance.feature_registry_sha256,
            plan.physical_feature_registry_sha256,
        ),
        "chart engine": (provenance.chart_engine_version, plan.chart_engine_version),
        "ephemeris file set": (
            provenance.ephemeris_file_set_sha256,
            plan.engine.ephemeris_provenance.ephemeris_file_set_sha256,
        ),
        "Mandala version": (
            provenance.mandala_mapping_version,
            plan.mandala_mapping_version,
        ),
        "Mandala mapping": (
            provenance.mandala_mapping_sha256,
            plan.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            provenance.bodygraph_mapping_sha256,
            plan.bodygraph_mapping_sha256,
        ),
        "Design time tolerance": (
            provenance.design_root_time_tolerance_seconds,
            plan.design_root_time_tolerance_seconds,
        ),
        "Design arc tolerance": (
            provenance.design_root_arc_tolerance_degrees,
            plan.design_root_arc_tolerance_degrees,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise StagedCenturyBuildError(
                f"exact-state batch {label} differs from its build plan"
            )
    return provenance


def write_staged_exact_state_batch(
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
    provider: SwissEphemerisProvider,
    staging_directory: str | Path,
    *,
    created_at_utc: datetime | None = None,
) -> StagedExactStateBatchReceiptV1:
    """Atomically write the job artifact, then write its passing receipt last."""

    _require_plan_job(plan, job)
    _require_provider_matches_plan(provider, plan)
    artifact_path = staged_job_artifact_path(staging_directory, job)
    receipt_path = staged_job_receipt_path(staging_directory, job)
    if artifact_path.exists() or receipt_path.exists():
        raise FileExistsError("staged job artifact or receipt already exists")

    batch, audit = _build_audited_batch(provider, plan, job)
    provenance = _require_batch_matches_plan_job(batch, plan, job)
    write_parquet_shard_new(
        artifact_path,
        batch.rows,
        CACHEABLE_M0_M2_FEATURE_COLUMNS,
    )
    persisted_rows = read_parquet_shard(
        artifact_path,
        CACHEABLE_M0_M2_FEATURE_COLUMNS,
    )
    if persisted_rows != batch.rows:
        raise StagedCenturyBuildError("new staged artifact changed logical rows")

    created_at = (
        datetime.now(UTC)
        if created_at_utc is None
        else _require_utc_datetime(created_at_utc, label="staged receipt creation time")
    )
    receipt = StagedExactStateBatchReceiptV1(
        verification_status="pass",
        plan_sha256=century_build_plan_sha256(plan),
        job_sha256=century_build_job_sha256(job),
        job_id=job.job_id,
        source_commit=plan.source_commit,
        source_tree_dirty=plan.source_tree_dirty,
        engine_identity_sha256=sha256_json(plan.engine.model_dump(mode="json")),
        boundary_policy_version=plan.boundary_policy_version,
        semantic_feature_registry_sha256=plan.semantic_feature_registry_sha256,
        physical_feature_registry_sha256=plan.physical_feature_registry_sha256,
        core_utc_start=job.core_utc_start,
        core_utc_end_exclusive=job.core_utc_end_exclusive,
        scan_utc_start=job.scan_utc_start,
        scan_utc_end_exclusive=job.scan_utc_end_exclusive,
        artifact_filename=artifact_path.name,
        artifact_sha256=sha256_file(artifact_path),
        artifact_size_bytes=artifact_path.stat().st_size,
        parquet_schema_sha256=parquet_schema_sha256(
            CACHEABLE_M0_M2_FEATURE_COLUMNS
        ),
        interval_count=len(batch.rows),
        boundary_event_count=sum(len(row.boundary_events) for row in batch.rows),
        canonical_rows_sha256=canonical_rows_sha256(batch.rows),
        exact_state_batch_provenance_sha256=sha256_json(
            provenance.model_dump(mode="json")
        ),
        exact_state_batch_provenance=provenance,
        swiss_calculation_audit=audit,
        created_at_utc=created_at,
    )
    write_new_canonical_json(receipt_path, receipt)
    return receipt


def load_staged_exact_state_batch_receipt(
    path: str | Path,
) -> StagedExactStateBatchReceiptV1:
    """Load a resumability claim without minting a verified batch capability."""

    receipt_path = Path(path)
    try:
        raw = receipt_path.read_bytes()
        receipt = StagedExactStateBatchReceiptV1.model_validate_json(raw, strict=True)
    except (OSError, ValueError) as exc:
        raise StagedCenturyBuildError("invalid staged exact-state receipt") from exc
    if canonical_json_bytes(receipt.model_dump(mode="json")) != raw:
        raise StagedCenturyBuildError("staged exact-state receipt is not canonical JSON")
    if receipt_path.name != f"staged-{receipt.job_id}.receipt.json" or (
        re.fullmatch(RECEIPT_FILENAME_PATTERN, receipt_path.name) is None
    ):
        raise StagedCenturyBuildError("staged exact-state receipt filename is inconsistent")
    return receipt


def _require_receipt_matches_plan_job(
    receipt: StagedExactStateBatchReceiptV1,
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
) -> None:
    expected: dict[str, tuple[object, object]] = {
        "plan hash": (receipt.plan_sha256, century_build_plan_sha256(plan)),
        "job hash": (receipt.job_sha256, century_build_job_sha256(job)),
        "job ID": (receipt.job_id, job.job_id),
        "source commit": (receipt.source_commit, plan.source_commit),
        "source tree": (receipt.source_tree_dirty, plan.source_tree_dirty),
        "engine": (
            receipt.engine_identity_sha256,
            sha256_json(plan.engine.model_dump(mode="json")),
        ),
        "boundary policy": (
            receipt.boundary_policy_version,
            plan.boundary_policy_version,
        ),
        "semantic registry": (
            receipt.semantic_feature_registry_sha256,
            plan.semantic_feature_registry_sha256,
        ),
        "physical registry": (
            receipt.physical_feature_registry_sha256,
            plan.physical_feature_registry_sha256,
        ),
        "core start": (receipt.core_utc_start, job.core_utc_start),
        "core end": (receipt.core_utc_end_exclusive, job.core_utc_end_exclusive),
        "scan start": (receipt.scan_utc_start, job.scan_utc_start),
        "scan end": (receipt.scan_utc_end_exclusive, job.scan_utc_end_exclusive),
        "Parquet schema": (
            receipt.parquet_schema_sha256,
            parquet_schema_sha256(CACHEABLE_M0_M2_FEATURE_COLUMNS),
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise StagedCenturyBuildError(f"staged receipt {label} binding changed")


def verify_staged_exact_state_batch(
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
    provider: SwissEphemerisProvider,
    staging_directory: str | Path,
) -> VerifiedStagedExactStateBatch:
    """Re-hash/decode and production-replay a staged job before minting proof."""

    _require_plan_job(plan, job)
    _require_provider_matches_plan(provider, plan)
    receipt_path = staged_job_receipt_path(staging_directory, job)
    receipt = load_staged_exact_state_batch_receipt(receipt_path)
    _require_receipt_matches_plan_job(receipt, plan, job)
    artifact_path = receipt_path.parent / receipt.artifact_filename
    if artifact_path != staged_job_artifact_path(staging_directory, job):
        raise StagedCenturyBuildError("staged artifact locator changed")
    if not artifact_path.is_file():
        raise StagedCenturyBuildError("staged exact-state artifact is missing")
    if artifact_path.stat().st_size != receipt.artifact_size_bytes or (
        sha256_file(artifact_path) != receipt.artifact_sha256
    ):
        raise StagedCenturyBuildError("staged exact-state artifact bytes changed")
    try:
        persisted_rows = read_parquet_shard(
            artifact_path,
            CACHEABLE_M0_M2_FEATURE_COLUMNS,
        )
    except (TypeError, ValueError, RuntimeError) as exc:
        raise StagedCenturyBuildError("staged exact-state artifact cannot be decoded") from exc
    if len(persisted_rows) != receipt.interval_count or (
        canonical_rows_sha256(persisted_rows) != receipt.canonical_rows_sha256
    ):
        raise StagedCenturyBuildError("staged exact-state logical rows changed")
    if sum(len(row.boundary_events) for row in persisted_rows) != (
        receipt.boundary_event_count
    ):
        raise StagedCenturyBuildError("staged exact-state boundary events changed")

    replay_batch, replay_audit = _build_audited_batch(provider, plan, job)
    replay_provenance = _require_batch_matches_plan_job(replay_batch, plan, job)
    if replay_batch.rows != persisted_rows:
        raise StagedCenturyBuildError(
            "deterministic exact-state replay differs from persisted logical rows"
        )
    if replay_provenance != receipt.exact_state_batch_provenance:
        raise StagedCenturyBuildError(
            "deterministic replay partition/provenance differs from staged receipt"
        )
    if replay_audit != receipt.swiss_calculation_audit:
        raise StagedCenturyBuildError(
            "deterministic all-call SWIEPH audit differs from staged receipt"
        )
    producer_receipt_sha256 = sha256_file(receipt_path)
    replay_provenance_sha256 = sha256_json(replay_provenance.model_dump(mode="json"))
    replay_audit_sha256 = sha256_json(replay_audit.model_dump(mode="json"))
    replay_verification = StagedExactStateReplayVerificationV1(
        verification_status="pass",
        plan_sha256=receipt.plan_sha256,
        job_sha256=receipt.job_sha256,
        job_id=receipt.job_id,
        source_commit=receipt.source_commit,
        engine_identity_sha256=receipt.engine_identity_sha256,
        producer_receipt_sha256=producer_receipt_sha256,
        artifact_sha256=receipt.artifact_sha256,
        artifact_size_bytes=receipt.artifact_size_bytes,
        persisted_canonical_rows_sha256=receipt.canonical_rows_sha256,
        replay_canonical_rows_sha256=canonical_rows_sha256(replay_batch.rows),
        interval_count=receipt.interval_count,
        boundary_event_count=receipt.boundary_event_count,
        producer_exact_state_provenance_sha256=(
            receipt.exact_state_batch_provenance_sha256
        ),
        replay_exact_state_provenance_sha256=replay_provenance_sha256,
        producer_swiss_calculation_audit_sha256=sha256_json(
            receipt.swiss_calculation_audit.model_dump(mode="json")
        ),
        replay_swiss_calculation_audit_sha256=replay_audit_sha256,
        artifact_bytes_match=True,
        logical_rows_match=True,
        partition_and_events_match=True,
        all_call_swieph_audit_match=True,
    )
    verified = VerifiedStagedExactStateBatch(
        batch=replay_batch,
        producer_receipt=receipt,
        producer_receipt_sha256=producer_receipt_sha256,
        replay_verification=replay_verification,
        replay_verification_sha256=staged_replay_verification_sha256(
            replay_verification
        ),
        _factory_token=_VERIFIED_STAGED_EXACT_STATE_BATCH_FACTORY_TOKEN,
    )
    validate_verified_staged_exact_state_batch(verified)
    return verified
