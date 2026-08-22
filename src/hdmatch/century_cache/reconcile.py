"""Streaming overlap reconciliation for factory-verified exact-state jobs.

The production interface deliberately retains at most two bounded scan jobs and
one unresolved tail row.  It never materializes the century universe.  A caller
can therefore publish each returned private-token batch immediately and compare
its own incremental hash/counts with the final aggregate provenance.
"""

from __future__ import annotations

import hashlib
import json
import math
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.ephemeris import (
    SwissCalculationAuditCapture,
    SwissCalculationAuditSnapshot,
    SwissEphemerisProvider,
)
from hdmatch.chart.feature_registry import cacheable_serialization_session
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

from .chart_adapter import (
    _EXACT_STATE_RECONCILIATION_MINT_TOKEN,
    ExactStateBatchError,
    VerifiedExactStateBatch,
    _mint_reconciled_exact_state_batch,
    cacheable_chart_state_to_century_record,
    validate_verified_exact_state_batch,
)
from .models import (
    SHA256_PATTERN,
    CenturyStateRecord,
    ExactStateBatchProvenance,
    ExactStateUniverseProvenance,
    canonical_rows_sha256,
    discrete_chart_identity_sha256,
)
from .staging import (
    SwissCalculationAuditV1,
    SwissEngineBuildIdentityV1,
    VerifiedStagedExactStateBatch,
    certify_swiss_calculation_audit,
    staged_replay_verification_sha256,
    validate_verified_staged_exact_state_batch,
)

RECONCILIATION_POLICY_VERSION: Final[
    Literal["exact-state-overlap-reconciliation-v1"]
] = "exact-state-overlap-reconciliation-v1"
BOUNDARY_EVENT_CATALOG_SHA256: Final[str] = sha256_json(
    {
        "schema_version": "chart-boundary-event-v1",
        "semantic_identity": [
            "side",
            "body",
            "resolution",
            "boundary_longitude",
            "before.gate",
            "before.line",
            "after.gate",
            "after.line",
        ],
        "duplicate_rule": "same-semantic-identity-within-max-root-tolerance",
        "ownership_rule": "half-open-core-left-owns-event-at-core-end",
    }
)
_RECONCILED_CHUNK_FACTORY_TOKEN: Final[object] = object()
_OVERLAPPING_STAGED_SOURCE_FACTORY_TOKEN: Final[object] = object()
_OVERLAPPING_TEST_SOURCE_FACTORY_TOKEN: Final[object] = object()
_RECONCILIATION_FINALIZATION_FACTORY_TOKEN: Final[object] = object()


class ExactStateReconciliationError(ValueError):
    """Verified jobs cannot be reconciled into one exact maximal universe."""


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class ReconciliationSourceV1(_FrozenModel):
    """One replay-verified staged job and the core range it owns."""

    schema_version: Literal["exact-state-reconciliation-source-v1"] = (
        "exact-state-reconciliation-source-v1"
    )
    ordinal: int = Field(ge=0)
    source_build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    source_staged_receipt_sha256: str = Field(pattern=SHA256_PATTERN)
    source_replay_verification_sha256: str = Field(pattern=SHA256_PATTERN)
    source_all_call_audit_sha256: str = Field(pattern=SHA256_PATTERN)
    exact_state_batch_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    scan_start_utc: datetime
    scan_end_exclusive: datetime
    core_start_utc: datetime
    core_end_exclusive: datetime

    @field_validator(
        "scan_start_utc",
        "scan_end_exclusive",
        "core_start_utc",
        "core_end_exclusive",
    )
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reconciliation source timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_ranges(self) -> ReconciliationSourceV1:
        if not (
            self.scan_start_utc <= self.core_start_utc
            < self.core_end_exclusive <= self.scan_end_exclusive
        ):
            raise ValueError("reconciliation core is not contained in its scan range")
        return self


class CoreReconciliationReceiptV1(_FrozenModel):
    """One seam/final emission receipt; it contains no astronomy secret."""

    schema_version: Literal["core-reconciliation-receipt-v1"] = (
        "core-reconciliation-receipt-v1"
    )
    status: Literal["pass"]
    ordinal: int = Field(ge=0)
    phase: Literal["seam", "final"]
    reconciliation_policy_version: Literal[
        "exact-state-overlap-reconciliation-v1"
    ] = RECONCILIATION_POLICY_VERSION
    boundary_event_catalog_sha256: str = Field(pattern=SHA256_PATTERN)
    root_tolerance_seconds: float = Field(gt=0.0)
    ordered_source_identity_sha256s: tuple[str, ...] = Field(min_length=1)
    core_cut_utc: datetime | None
    overlap_start_utc: datetime | None
    overlap_end_exclusive: datetime | None
    duplicate_boundary_event_count: int = Field(ge=0)
    excluded_artificial_scan_endpoint_count: int = Field(ge=0)
    equal_state_artificial_cut_merged: bool
    emitted_exact_batch_provenance_sha256: str | None
    emitted_canonical_rows_sha256: str | None
    emitted_interval_count: int = Field(ge=0)
    emitted_boundary_event_count: int = Field(ge=0)
    emitted_utc_start: datetime | None
    emitted_utc_end_exclusive: datetime | None

    @field_validator(
        "core_cut_utc",
        "overlap_start_utc",
        "overlap_end_exclusive",
        "emitted_utc_start",
        "emitted_utc_end_exclusive",
    )
    @classmethod
    def normalize_optional_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reconciliation receipt timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_emission(self) -> CoreReconciliationReceiptV1:
        if self.boundary_event_catalog_sha256 != BOUNDARY_EVENT_CATALOG_SHA256:
            raise ValueError("reconciliation receipt event catalog is stale")
        if not math.isfinite(self.root_tolerance_seconds):
            raise ValueError("reconciliation receipt root tolerance must be finite")
        if any(
            len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
            for value in self.ordered_source_identity_sha256s
        ):
            raise ValueError("reconciliation receipt has an invalid source identity")
        hashes = (
            self.emitted_exact_batch_provenance_sha256,
            self.emitted_canonical_rows_sha256,
        )
        ranges = (self.emitted_utc_start, self.emitted_utc_end_exclusive)
        if self.emitted_interval_count == 0:
            if any(value is not None for value in (*hashes, *ranges)):
                raise ValueError("empty reconciliation receipt binds emitted output")
            if self.emitted_boundary_event_count != 0:
                raise ValueError("empty reconciliation receipt has boundary events")
        elif any(value is None for value in (*hashes, *ranges)):
            raise ValueError("non-empty reconciliation receipt lacks output bindings")
        if self.phase == "seam":
            cut = self.core_cut_utc
            overlap_start = self.overlap_start_utc
            overlap_end = self.overlap_end_exclusive
            if cut is None or overlap_start is None or overlap_end is None:
                raise ValueError("seam receipt lacks cut/overlap timestamps")
            assert isinstance(cut, datetime)
            assert isinstance(overlap_start, datetime)
            assert isinstance(overlap_end, datetime)
            if not overlap_start < cut < overlap_end:
                raise ValueError("seam receipt overlap does not straddle the core cut")
        elif any(
            value is not None
            for value in (
                self.core_cut_utc,
                self.overlap_start_utc,
                self.overlap_end_exclusive,
            )
        ):
            raise ValueError("final receipt must not claim a seam")
        if self.phase == "final" and self.equal_state_artificial_cut_merged:
            raise ValueError("final receipt cannot claim an artificial cut merge")
        if self.emitted_interval_count > 0:
            emitted_start = self.emitted_utc_start
            emitted_end = self.emitted_utc_end_exclusive
            if emitted_start is None or emitted_end is None:
                raise ValueError("reconciliation receipt lacks emitted range")
            if not emitted_start < emitted_end:
                raise ValueError("reconciliation receipt emitted range is not positive")
        return self


class ReconciliationCalculationAuditV1(_FrozenModel):
    """Complete Swiss trace for reconciliation, including a valid zero-call case."""

    schema_version: Literal["reconciliation-calculation-audit-v1"] = (
        "reconciliation-calculation-audit-v1"
    )
    verification_status: Literal["pass"]
    outcome: Literal["all_calls_swieph", "no_recomputation_required"]
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    requested_flags: int = Field(gt=0)
    ephemeris_mask: int = Field(gt=0)
    swieph_flag: int = Field(gt=0)
    calculation_call_count: int = Field(ge=0)
    requested_flags_counts: tuple[tuple[int, int], ...]
    returned_flags_counts: tuple[tuple[int, int], ...]
    returned_mode_bits_counts: tuple[tuple[int, int], ...]
    calculated_body_counts: tuple[tuple[str, int], ...]
    used_file_counts: tuple[tuple[str, str, int, int], ...]
    calculation_trace_sha256: str = Field(pattern=SHA256_PATTERN)
    first_calculation_sha256: str | None
    final_calculation_sha256: str | None
    entry_provider_configuration_sha256: str = Field(pattern=SHA256_PATTERN)
    exit_provider_configuration_sha256: str = Field(pattern=SHA256_PATTERN)
    entry_ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    exit_ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    certified_nonempty_audit: SwissCalculationAuditV1 | None

    @model_validator(mode="after")
    def validate_trace(self) -> ReconciliationCalculationAuditV1:
        if self.entry_provider_configuration_sha256 != (
            self.exit_provider_configuration_sha256
        ):
            raise ValueError("reconciliation provider configuration changed")
        if self.entry_ephemeris_file_set_sha256 != (
            self.exit_ephemeris_file_set_sha256
        ):
            raise ValueError("reconciliation ephemeris file set changed")
        if self.calculation_call_count == 0:
            if self.outcome != "no_recomputation_required":
                raise ValueError("zero-call reconciliation audit has wrong outcome")
            if self.certified_nonempty_audit is not None:
                raise ValueError("zero-call reconciliation audit embeds call evidence")
            if any(
                (
                    self.requested_flags_counts,
                    self.returned_flags_counts,
                    self.returned_mode_bits_counts,
                    self.calculated_body_counts,
                    self.used_file_counts,
                )
            ):
                raise ValueError("zero-call reconciliation audit has nonempty counts")
            if (
                self.first_calculation_sha256 is not None
                or self.final_calculation_sha256 is not None
            ):
                raise ValueError("zero-call reconciliation audit has endpoint calls")
        else:
            audit = self.certified_nonempty_audit
            if self.outcome != "all_calls_swieph" or audit is None:
                raise ValueError("nonempty reconciliation trace lacks SWIEPH audit")
            expected = {
                "engine_identity_sha256": self.engine_identity_sha256,
                "requested_flags": self.requested_flags,
                "ephemeris_mask": self.ephemeris_mask,
                "swieph_flag": self.swieph_flag,
                "calculation_call_count": self.calculation_call_count,
                "requested_flags_counts": self.requested_flags_counts,
                "returned_flags_counts": self.returned_flags_counts,
                "returned_mode_bits_counts": self.returned_mode_bits_counts,
                "calculated_body_counts": self.calculated_body_counts,
                "used_file_counts": self.used_file_counts,
                "calculation_trace_sha256": self.calculation_trace_sha256,
                "first_calculation_sha256": self.first_calculation_sha256,
                "final_calculation_sha256": self.final_calculation_sha256,
                "entry_provider_configuration_sha256": (
                    self.entry_provider_configuration_sha256
                ),
                "exit_provider_configuration_sha256": (
                    self.exit_provider_configuration_sha256
                ),
                "entry_ephemeris_file_set_sha256": (
                    self.entry_ephemeris_file_set_sha256
                ),
                "exit_ephemeris_file_set_sha256": (
                    self.exit_ephemeris_file_set_sha256
                ),
            }
            for field, value in expected.items():
                if getattr(audit, field) != value:
                    raise ValueError(
                        f"reconciliation trace differs from certified audit: {field}"
                    )
        return self


class ExactStateReconciliationAggregateProvenanceV1(_FrozenModel):
    """Streaming reconciliation proof paired with manifest-compatible provenance."""

    schema_version: Literal["exact-state-reconciliation-aggregate-v1"] = (
        "exact-state-reconciliation-aggregate-v1"
    )
    status: Literal["pass"]
    reconciliation_policy_version: Literal[
        "exact-state-overlap-reconciliation-v1"
    ] = RECONCILIATION_POLICY_VERSION
    boundary_event_catalog_sha256: str = Field(pattern=SHA256_PATTERN)
    build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    root_tolerance_seconds: float = Field(gt=0.0)
    ordered_sources: tuple[ReconciliationSourceV1, ...] = Field(min_length=1)
    ordered_core_reconciliation_receipt_sha256s: tuple[str, ...] = Field(
        min_length=1
    )
    ordered_output_chunk_provenance_sha256s: tuple[str, ...] = Field(min_length=1)
    reconciliation_calculation_audit: ReconciliationCalculationAuditV1
    exact_state_universe_provenance: ExactStateUniverseProvenance

    @model_validator(mode="after")
    def validate_complete_chain(self) -> ExactStateReconciliationAggregateProvenanceV1:
        exact = self.exact_state_universe_provenance
        if self.boundary_event_catalog_sha256 != BOUNDARY_EVENT_CATALOG_SHA256:
            raise ValueError("aggregate reconciliation event catalog is stale")
        if not math.isfinite(self.root_tolerance_seconds):
            raise ValueError("aggregate reconciliation root tolerance must be finite")
        if self.reconciliation_calculation_audit.engine_identity_sha256 != (
            self.engine_identity_sha256
        ):
            raise ValueError("aggregate reconciliation engine identity differs")
        if any(
            item.source_build_plan_sha256 != self.build_plan_sha256
            for item in self.ordered_sources
        ):
            raise ValueError("aggregate reconciliation sources mix build plans")
        source_hashes = tuple(
            item.exact_state_batch_provenance_sha256 for item in self.ordered_sources
        )
        if exact.ordered_source_batch_provenance_sha256s != source_hashes:
            raise ValueError("aggregate exact provenance lost source batch ordering")
        if exact.batch_count != len(self.ordered_sources):
            raise ValueError("aggregate exact provenance source count differs")
        if tuple(item.ordinal for item in self.ordered_sources) != tuple(
            range(len(self.ordered_sources))
        ):
            raise ValueError("reconciliation sources are not ordinal-contiguous")
        for left, right in zip(
            self.ordered_sources, self.ordered_sources[1:], strict=False
        ):
            if left.core_end_exclusive != right.core_start_utc:
                raise ValueError("aggregate source cores contain a gap or overlap")
            overlap_start = max(left.scan_start_utc, right.scan_start_utc)
            overlap_end = min(
                left.scan_end_exclusive, right.scan_end_exclusive
            )
            if not overlap_start < left.core_end_exclusive < overlap_end:
                raise ValueError("aggregate source scans do not overlap around the cut")
        if exact.utc_start != self.ordered_sources[0].core_start_utc or (
            exact.utc_end_exclusive != self.ordered_sources[-1].core_end_exclusive
        ):
            raise ValueError("aggregate exact range differs from ordered source cores")
        if len(self.ordered_core_reconciliation_receipt_sha256s) != len(
            self.ordered_sources
        ):
            raise ValueError("every reconciliation source requires one output receipt")
        expected_plan = _assembly_plan_sha256(
            self.ordered_sources,
            engine_identity_sha256=self.engine_identity_sha256,
            root_tolerance_seconds=self.root_tolerance_seconds,
        )
        if exact.assembly_plan_sha256 != expected_plan:
            raise ValueError("aggregate assembly-plan hash differs")
        expected_report = _aggregate_report_sha256(
            sources=self.ordered_sources,
            receipt_sha256s=self.ordered_core_reconciliation_receipt_sha256s,
            output_chunk_sha256s=self.ordered_output_chunk_provenance_sha256s,
            reconciliation_calculation_audit_sha256=self.reconciliation_calculation_audit_sha256,
            engine_identity_sha256=self.engine_identity_sha256,
            root_tolerance_seconds=self.root_tolerance_seconds,
            exact=exact,
        )
        if exact.reconciliation_report_sha256 != expected_report:
            raise ValueError("aggregate reconciliation-report hash differs")
        return self

    @property
    def reconciliation_calculation_audit_sha256(self) -> str:
        return sha256_json(self.reconciliation_calculation_audit.model_dump(mode="json"))

    @property
    def ordered_source_staged_receipt_sha256s(self) -> tuple[str, ...]:
        return tuple(item.source_staged_receipt_sha256 for item in self.ordered_sources)

    @property
    def ordered_source_replay_verification_sha256s(self) -> tuple[str, ...]:
        return tuple(
            item.source_replay_verification_sha256 for item in self.ordered_sources
        )

    @property
    def ordered_source_all_call_audit_sha256s(self) -> tuple[str, ...]:
        return tuple(item.source_all_call_audit_sha256 for item in self.ordered_sources)


class OverlappingVerifiedExactStateBatch:
    """A replay-verified scan batch plus its non-overlapping owned core."""

    __slots__ = (
        "_batch",
        "_core_end_exclusive",
        "_core_start_utc",
        "_factory_token",
        "_source_all_call_audit_sha256",
        "_source_build_plan_sha256",
        "_source_replay_verification_sha256",
        "_source_staged_receipt_sha256",
    )
    _batch: VerifiedExactStateBatch
    _core_end_exclusive: datetime
    _core_start_utc: datetime
    _factory_token: object
    _source_all_call_audit_sha256: str
    _source_build_plan_sha256: str
    _source_replay_verification_sha256: str
    _source_staged_receipt_sha256: str

    def __init__(
        self,
        *,
        batch: VerifiedExactStateBatch,
        core_start_utc: datetime,
        core_end_exclusive: datetime,
        source_staged_receipt_sha256: str,
        source_replay_verification_sha256: str,
        source_all_call_audit_sha256: str,
        source_build_plan_sha256: str,
        _factory_token: object,
    ) -> None:
        if _factory_token not in (
            _OVERLAPPING_STAGED_SOURCE_FACTORY_TOKEN,
            _OVERLAPPING_TEST_SOURCE_FACTORY_TOKEN,
        ):
            raise ExactStateReconciliationError(
                "overlapping sources must be minted from staged replay verification"
            )
        try:
            provenance = validate_verified_exact_state_batch(batch)
        except ExactStateBatchError as exc:
            raise ExactStateReconciliationError(str(exc)) from exc
        start = _require_utc(core_start_utc)
        end = _require_utc(core_end_exclusive)
        if not provenance.utc_start <= start < end <= provenance.utc_end_exclusive:
            raise ExactStateReconciliationError(
                "owned core must be a positive subrange of its verified scan batch"
            )
        for label, value in (
            ("staged receipt", source_staged_receipt_sha256),
            ("replay verification", source_replay_verification_sha256),
            ("all-call audit", source_all_call_audit_sha256),
            ("build plan", source_build_plan_sha256),
        ):
            if len(value) != 64 or any(
                character not in "0123456789abcdef" for character in value
            ):
                raise ExactStateReconciliationError(f"invalid {label} SHA-256")
        object.__setattr__(self, "_batch", batch)
        object.__setattr__(self, "_core_start_utc", start)
        object.__setattr__(self, "_core_end_exclusive", end)
        object.__setattr__(
            self, "_source_staged_receipt_sha256", source_staged_receipt_sha256
        )
        object.__setattr__(
            self,
            "_source_replay_verification_sha256",
            source_replay_verification_sha256,
        )
        object.__setattr__(
            self, "_source_all_call_audit_sha256", source_all_call_audit_sha256
        )
        object.__setattr__(self, "_source_build_plan_sha256", source_build_plan_sha256)
        object.__setattr__(self, "_factory_token", _factory_token)

    def __setattr__(self, name: str, value: object) -> None:
        del name, value
        raise AttributeError("OverlappingVerifiedExactStateBatch is immutable")

    @property
    def batch(self) -> VerifiedExactStateBatch:
        return self._batch

    @property
    def core_start_utc(self) -> datetime:
        return self._core_start_utc

    @property
    def core_end_exclusive(self) -> datetime:
        return self._core_end_exclusive

    @property
    def source_staged_receipt_sha256(self) -> str:
        return self._source_staged_receipt_sha256

    @property
    def source_replay_verification_sha256(self) -> str:
        return self._source_replay_verification_sha256

    @property
    def source_all_call_audit_sha256(self) -> str:
        return self._source_all_call_audit_sha256

    @property
    def source_build_plan_sha256(self) -> str:
        return self._source_build_plan_sha256

    @classmethod
    def from_verified_staged_batch(
        cls,
        source: VerifiedStagedExactStateBatch,
    ) -> OverlappingVerifiedExactStateBatch:
        """Derive all production source identities from replay-verified staging."""

        if not isinstance(source, VerifiedStagedExactStateBatch):
            raise ExactStateReconciliationError(
                "production source must be a replay-verified staged batch"
            )
        try:
            validate_verified_staged_exact_state_batch(source)
        except (TypeError, ValueError) as exc:
            raise ExactStateReconciliationError(
                f"staged replay admission failed: {exc}"
            ) from exc
        try:
            provenance = validate_verified_exact_state_batch(source.batch)
        except ExactStateBatchError as exc:
            raise ExactStateReconciliationError(str(exc)) from exc
        receipt = source.producer_receipt
        replay = source.replay_verification
        receipt_sha256 = sha256_json(receipt.model_dump(mode="json"))
        replay_sha256 = staged_replay_verification_sha256(replay)
        provenance_sha256 = sha256_json(provenance.model_dump(mode="json"))
        if source.producer_receipt_sha256 != receipt_sha256:
            raise ExactStateReconciliationError("staged producer receipt hash changed")
        if source.replay_verification_sha256 != replay_sha256:
            raise ExactStateReconciliationError("staged replay verification hash changed")
        if receipt.exact_state_batch_provenance_sha256 != provenance_sha256 or (
            replay.replay_exact_state_provenance_sha256 != provenance_sha256
        ):
            raise ExactStateReconciliationError(
                "staged replay batch differs from its exact-state provenance"
            )
        if replay.producer_receipt_sha256 != receipt_sha256:
            raise ExactStateReconciliationError(
                "staged replay does not bind its producer receipt"
            )
        if replay.plan_sha256 != receipt.plan_sha256:
            raise ExactStateReconciliationError(
                "staged replay does not bind its producer build plan"
            )
        producer_audit_sha256 = sha256_json(
            receipt.swiss_calculation_audit.model_dump(mode="json")
        )
        if replay.producer_swiss_calculation_audit_sha256 != producer_audit_sha256:
            raise ExactStateReconciliationError(
                "staged replay does not bind its producer all-call audit"
            )
        return cls(
            batch=source.batch,
            core_start_utc=receipt.core_utc_start,
            core_end_exclusive=receipt.core_utc_end_exclusive,
            source_staged_receipt_sha256=receipt_sha256,
            source_replay_verification_sha256=replay_sha256,
            source_all_call_audit_sha256=producer_audit_sha256,
            source_build_plan_sha256=receipt.plan_sha256,
            _factory_token=_OVERLAPPING_STAGED_SOURCE_FACTORY_TOKEN,
        )

    @classmethod
    def _from_factory_verified_batch_for_test(
        cls,
        *,
        batch: VerifiedExactStateBatch,
        core_start_utc: datetime,
        core_end_exclusive: datetime,
        source_staged_receipt_sha256: str,
        source_replay_verification_sha256: str,
        source_all_call_audit_sha256: str,
        source_build_plan_sha256: str,
    ) -> OverlappingVerifiedExactStateBatch:
        """Mint an isolated fake-Swiss fixture; never a production admission path."""

        return cls(
            batch=batch,
            core_start_utc=core_start_utc,
            core_end_exclusive=core_end_exclusive,
            source_staged_receipt_sha256=source_staged_receipt_sha256,
            source_replay_verification_sha256=source_replay_verification_sha256,
            source_all_call_audit_sha256=source_all_call_audit_sha256,
            source_build_plan_sha256=source_build_plan_sha256,
            _factory_token=_OVERLAPPING_TEST_SOURCE_FACTORY_TOKEN,
        )


class ReconciledExactStateChunk:
    """One bounded private-token batch safe for immediate streaming publish."""

    __slots__ = ("_batch", "_factory_token", "_receipt")
    _batch: VerifiedExactStateBatch
    _factory_token: object
    _receipt: CoreReconciliationReceiptV1

    def __init__(
        self,
        *,
        batch: VerifiedExactStateBatch,
        receipt: CoreReconciliationReceiptV1,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _RECONCILED_CHUNK_FACTORY_TOKEN:
            raise ExactStateReconciliationError(
                "reconciled chunks must be minted by the streaming factory"
            )
        object.__setattr__(self, "_batch", batch)
        object.__setattr__(self, "_receipt", receipt)
        object.__setattr__(self, "_factory_token", _factory_token)

    def __setattr__(self, name: str, value: object) -> None:
        del name, value
        raise AttributeError("ReconciledExactStateChunk is immutable")

    @property
    def batch(self) -> VerifiedExactStateBatch:
        return self._batch

    @property
    def receipt(self) -> CoreReconciliationReceiptV1:
        return self._receipt


class ReconciliationStreamFinalization:
    """The last bounded chunk and the complete row-free aggregate proof."""

    __slots__ = ("_aggregate_provenance", "_factory_token", "_final_chunk")
    _aggregate_provenance: ExactStateReconciliationAggregateProvenanceV1
    _factory_token: object
    _final_chunk: ReconciledExactStateChunk

    def __init__(
        self,
        *,
        final_chunk: ReconciledExactStateChunk,
        aggregate_provenance: ExactStateReconciliationAggregateProvenanceV1,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _RECONCILIATION_FINALIZATION_FACTORY_TOKEN:
            raise ExactStateReconciliationError(
                "reconciliation finalization must be minted by the stream"
            )
        object.__setattr__(self, "_final_chunk", final_chunk)
        object.__setattr__(self, "_aggregate_provenance", aggregate_provenance)
        object.__setattr__(self, "_factory_token", _factory_token)

    def __setattr__(self, name: str, value: object) -> None:
        del name, value
        raise AttributeError("ReconciliationStreamFinalization is immutable")

    @property
    def final_chunk(self) -> ReconciledExactStateChunk:
        return self._final_chunk

    @property
    def aggregate_provenance(self) -> ExactStateReconciliationAggregateProvenanceV1:
        return self._aggregate_provenance

    @property
    def exact_state_universe_provenance(self) -> ExactStateUniverseProvenance:
        return self.aggregate_provenance.exact_state_universe_provenance


@dataclass(frozen=True, slots=True)
class _ParsedBoundaryEvent:
    raw: str
    at_utc: datetime
    side: str
    body: str
    resolution: str
    boundary_longitude: float
    before_gate: int
    before_line: int
    after_gate: int
    after_line: int
    root_tolerance_seconds: float


@dataclass(frozen=True, slots=True)
class _SeamEvidence:
    overlap_start_utc: datetime
    overlap_end_exclusive: datetime
    duplicate_boundary_event_count: int
    excluded_artificial_scan_endpoint_count: int
    exact_event_at_core_cut: bool


class _Digest(Protocol):
    def update(self, value: bytes) -> None: ...

    def hexdigest(self) -> str: ...


class ExactStateReconciliationStream:
    """Validate overlapping jobs and emit a globally exact stream incrementally."""

    def __init__(
        self,
        provider: SwissEphemerisProvider,
        *,
        engine_identity: SwissEngineBuildIdentityV1,
        root_tolerance_seconds: float = 0.01,
        _test_source_factory_token: object | None = None,
    ) -> None:
        if not isinstance(provider, SwissEphemerisProvider):
            raise ExactStateReconciliationError(
                "production reconciliation requires SwissEphemerisProvider"
            )
        if not math.isfinite(root_tolerance_seconds) or root_tolerance_seconds <= 0.0:
            raise ExactStateReconciliationError("root tolerance must be positive and finite")
        try:
            provider.verify_production_configuration()
        except (TypeError, ValueError, RuntimeError) as exc:
            raise ExactStateReconciliationError(
                f"Swiss production configuration failed: {exc}"
            ) from exc
        _validate_reconciliation_engine_identity(provider, engine_identity)
        self._provider = provider
        self._engine_identity = engine_identity
        self._root_tolerance_seconds = root_tolerance_seconds
        self._allow_test_sources = (
            _test_source_factory_token is _OVERLAPPING_TEST_SOURCE_FACTORY_TOKEN
        )
        self._audit_context: AbstractContextManager[
            SwissCalculationAuditCapture
        ] | None = None
        self._audit_capture: SwissCalculationAuditCapture | None = None
        self._audit_closed = True
        self._pending_source: OverlappingVerifiedExactStateBatch | None = None
        self._pending_rows: tuple[CenturyStateRecord, ...] = ()
        self._sources: list[ReconciliationSourceV1] = []
        self._receipt_sha256s: list[str] = []
        self._output_chunk_sha256s: list[str] = []
        self._logical_digest: _Digest = hashlib.sha256()
        self._output_interval_count = 0
        self._output_boundary_event_count = 0
        self._output_start: datetime | None = None
        self._output_end: datetime | None = None
        self._last_emitted_row: CenturyStateRecord | None = None
        self._finalized = False

    @classmethod
    def _for_factory_verified_test_sources(
        cls,
        provider: SwissEphemerisProvider,
        *,
        engine_identity: SwissEngineBuildIdentityV1,
        root_tolerance_seconds: float = 0.01,
    ) -> ExactStateReconciliationStream:
        """Create the narrowly scoped fake-Swiss seam-test stream."""

        return cls(
            provider,
            engine_identity=engine_identity,
            root_tolerance_seconds=root_tolerance_seconds,
            _test_source_factory_token=_OVERLAPPING_TEST_SOURCE_FACTORY_TOKEN,
        )

    def __enter__(self) -> ExactStateReconciliationStream:
        if self._finalized:
            raise ExactStateReconciliationError("reconciliation stream is finalized")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object,
    ) -> Literal[False]:
        del exc_type, exc_value, traceback
        if not self._finalized:
            self.abort()
        return False

    def abort(self) -> None:
        """Release the provider audit boundary without minting pass provenance."""

        self._abort_audit()

    def append(
        self,
        source: OverlappingVerifiedExactStateBatch,
    ) -> ReconciledExactStateChunk | None:
        """Append one ordered replay-verified scan; emit only finalized rows."""

        try:
            return self._append(source)
        except BaseException:
            self._abort_audit()
            raise

    def _append(
        self,
        source: OverlappingVerifiedExactStateBatch,
    ) -> ReconciledExactStateChunk | None:
        """Internal append body guarded by the lifetime all-call audit."""

        if self._finalized:
            raise ExactStateReconciliationError("reconciliation stream is finalized")
        _validate_overlapping_source_admission(
            source,
            allow_test_source=self._allow_test_sources,
        )
        self._ensure_audit_open()
        source_provenance = validate_verified_exact_state_batch(source.batch)
        ordinal = len(self._sources)
        descriptor = _source_descriptor(source, ordinal)
        if self._sources and descriptor.source_build_plan_sha256 != (
            self._sources[0].source_build_plan_sha256
        ):
            raise ExactStateReconciliationError(
                "reconciliation sources mix immutable build plans"
            )
        core_rows = _materialize_core_rows(self._provider, source)
        _validate_explained_partition(core_rows)
        if self._pending_source is None:
            self._pending_source = source
            self._pending_rows = core_rows
            self._sources.append(descriptor)
            return None

        previous_source = self._pending_source
        previous_rows = self._pending_rows
        if previous_source.core_end_exclusive != source.core_start_utc:
            raise ExactStateReconciliationError("owned core ranges contain a gap or overlap")
        _require_uniform_provenance(previous_source.batch.provenance, source_provenance)
        seam = source.core_start_utc
        seam_evidence = _reconcile_overlap(
            previous_source,
            source,
            seam,
            root_tolerance_seconds=self._root_tolerance_seconds,
        )

        left_identity = discrete_chart_identity_sha256(previous_rows[-1])
        right_identity = discrete_chart_identity_sha256(core_rows[0])
        equal_state = left_identity == right_identity
        if not equal_state and not seam_evidence.exact_event_at_core_cut:
            raise ExactStateReconciliationError(
                "unexplained identity change at core cut: no reconciled exact event"
            )

        if equal_state:
            merged = _recompute_interval(
                self._provider,
                start_utc=previous_rows[-1].utc_start,
                end_utc=core_rows[0].utc_end,
                boundary_events=tuple(
                    sorted(
                        set(
                            previous_rows[-1].boundary_events
                            + core_rows[0].boundary_events
                        )
                    )
                ),
                expected_identity_sha256=left_identity,
                source_provenance=previous_source.batch.provenance,
            )
            emitted_rows = previous_rows[:-1]
            pending_rows = (merged, *core_rows[1:])
        else:
            emitted_rows = previous_rows
            pending_rows = core_rows

        self._sources.append(descriptor)
        chunk, receipt = self._mint_chunk_and_receipt(
            rows=emitted_rows,
            phase="seam",
            source_identities=(
                _source_identity_sha256(self._sources[-2]),
                _source_identity_sha256(self._sources[-1]),
            ),
            core_cut_utc=seam,
            seam_evidence=seam_evidence,
            equal_state_artificial_cut_merged=equal_state,
        )
        self._pending_source = source
        self._pending_rows = pending_rows
        self._receipt_sha256s.append(sha256_json(receipt.model_dump(mode="json")))
        if chunk is not None:
            self._record_emitted_chunk(chunk)
        return chunk

    def finalize(self) -> ReconciliationStreamFinalization:
        """Emit the pending suffix and mint manifest-compatible aggregate proof."""

        try:
            return self._finalize()
        except BaseException:
            self._abort_audit()
            raise

    def _finalize(self) -> ReconciliationStreamFinalization:
        """Internal finalizer guarded by the lifetime all-call audit."""

        if self._finalized:
            raise ExactStateReconciliationError("reconciliation stream is finalized")
        if self._pending_source is None or not self._pending_rows:
            raise ExactStateReconciliationError("reconciliation stream contains no source")
        self._finalized = True
        chunk, receipt = self._mint_chunk_and_receipt(
            rows=self._pending_rows,
            phase="final",
            source_identities=(_source_identity_sha256(self._sources[-1]),),
            core_cut_utc=None,
            seam_evidence=None,
            equal_state_artificial_cut_merged=False,
        )
        if chunk is None:  # pragma: no cover - pending rows are required above
            raise ExactStateReconciliationError("final reconciliation chunk is empty")
        self._receipt_sha256s.append(sha256_json(receipt.model_dump(mode="json")))
        self._record_emitted_chunk(chunk)
        reconciliation_audit = self._close_and_certify_audit()
        reconciliation_audit_sha256 = sha256_json(
            reconciliation_audit.model_dump(mode="json")
        )
        exact = self._final_exact_universe_provenance(
            reconciliation_calculation_audit_sha256=reconciliation_audit_sha256
        )
        aggregate = ExactStateReconciliationAggregateProvenanceV1(
            status="pass",
            boundary_event_catalog_sha256=BOUNDARY_EVENT_CATALOG_SHA256,
            build_plan_sha256=self._sources[0].source_build_plan_sha256,
            engine_identity_sha256=sha256_json(
                self._engine_identity.model_dump(mode="json")
            ),
            root_tolerance_seconds=self._root_tolerance_seconds,
            ordered_sources=tuple(self._sources),
            ordered_core_reconciliation_receipt_sha256s=tuple(
                self._receipt_sha256s
            ),
            ordered_output_chunk_provenance_sha256s=tuple(
                self._output_chunk_sha256s
            ),
            reconciliation_calculation_audit=reconciliation_audit,
            exact_state_universe_provenance=exact,
        )
        finalization = ReconciliationStreamFinalization(
            final_chunk=chunk,
            aggregate_provenance=aggregate,
            _factory_token=_RECONCILIATION_FINALIZATION_FACTORY_TOKEN,
        )
        validate_reconciliation_stream_finalization(finalization)
        return finalization

    def _mint_chunk_and_receipt(
        self,
        *,
        rows: tuple[CenturyStateRecord, ...],
        phase: Literal["seam", "final"],
        source_identities: tuple[str, ...],
        core_cut_utc: datetime | None,
        seam_evidence: _SeamEvidence | None,
        equal_state_artificial_cut_merged: bool,
    ) -> tuple[ReconciledExactStateChunk | None, CoreReconciliationReceiptV1]:
        batch: VerifiedExactStateBatch | None = None
        batch_hash: str | None = None
        rows_hash: str | None = None
        if rows:
            partition_hash = _reconciled_partition_sha256(rows)
            batch = _mint_reconciled_exact_state_batch(
                rows,
                source_batch=(
                    self._pending_source.batch
                    if self._pending_source is not None
                    else _raise_missing_source()
                ),
                stable_interval_partition_sha256=partition_hash,
                _reconciliation_factory_token=(
                    _EXACT_STATE_RECONCILIATION_MINT_TOKEN
                ),
            )
            batch_hash = sha256_json(batch.provenance.model_dump(mode="json"))
            rows_hash = canonical_rows_sha256(rows)
        receipt = CoreReconciliationReceiptV1(
            status="pass",
            ordinal=len(self._receipt_sha256s),
            phase=phase,
            boundary_event_catalog_sha256=BOUNDARY_EVENT_CATALOG_SHA256,
            root_tolerance_seconds=self._root_tolerance_seconds,
            ordered_source_identity_sha256s=source_identities,
            core_cut_utc=core_cut_utc,
            overlap_start_utc=(
                seam_evidence.overlap_start_utc if seam_evidence is not None else None
            ),
            overlap_end_exclusive=(
                seam_evidence.overlap_end_exclusive
                if seam_evidence is not None
                else None
            ),
            duplicate_boundary_event_count=(
                seam_evidence.duplicate_boundary_event_count
                if seam_evidence is not None
                else 0
            ),
            excluded_artificial_scan_endpoint_count=(
                seam_evidence.excluded_artificial_scan_endpoint_count
                if seam_evidence is not None
                else 0
            ),
            equal_state_artificial_cut_merged=(
                equal_state_artificial_cut_merged
                and not (
                    seam_evidence.exact_event_at_core_cut
                    if seam_evidence is not None
                    else False
                )
            ),
            emitted_exact_batch_provenance_sha256=batch_hash,
            emitted_canonical_rows_sha256=rows_hash,
            emitted_interval_count=len(rows),
            emitted_boundary_event_count=sum(len(row.boundary_events) for row in rows),
            emitted_utc_start=rows[0].utc_start if rows else None,
            emitted_utc_end_exclusive=rows[-1].utc_end if rows else None,
        )
        if batch is None:
            return None, receipt
        chunk = ReconciledExactStateChunk(
            batch=batch,
            receipt=receipt,
            _factory_token=_RECONCILED_CHUNK_FACTORY_TOKEN,
        )
        validate_reconciled_exact_state_chunk(chunk)
        return chunk, receipt

    def _record_emitted_chunk(self, chunk: ReconciledExactStateChunk) -> None:
        provenance = validate_reconciled_exact_state_chunk(chunk)
        rows = chunk.batch.rows
        if self._last_emitted_row is not None:
            if self._last_emitted_row.utc_end != rows[0].utc_start:
                raise ExactStateReconciliationError(
                    "reconciled output chunks contain a gap or overlap"
                )
            if discrete_chart_identity_sha256(
                self._last_emitted_row
            ) == discrete_chart_identity_sha256(rows[0]):
                raise ExactStateReconciliationError(
                    "reconciled output chunks are not globally maximal"
                )
        if self._output_start is None:
            self._output_start = rows[0].utc_start
        self._output_end = rows[-1].utc_end
        for row in rows:
            self._logical_digest.update(canonical_json_bytes(row.model_dump(mode="json")))
            self._logical_digest.update(b"\n")
        self._output_interval_count += len(rows)
        self._output_boundary_event_count += sum(
            len(row.boundary_events) for row in rows
        )
        self._last_emitted_row = rows[-1]
        self._output_chunk_sha256s.append(
            sha256_json(provenance.model_dump(mode="json"))
        )

    def _final_exact_universe_provenance(
        self,
        *,
        reconciliation_calculation_audit_sha256: str,
    ) -> ExactStateUniverseProvenance:
        if (
            self._output_start is None
            or self._output_end is None
            or self._last_emitted_row is None
        ):
            raise ExactStateReconciliationError("reconciliation emitted no exact rows")
        first = self._pending_source
        if first is None:  # pragma: no cover - guarded by finalize
            raise ExactStateReconciliationError("reconciliation source is missing")
        template = validate_verified_exact_state_batch(first.batch)
        logical_hash = self._logical_digest.hexdigest()
        source_tuple = tuple(self._sources)
        source_hashes = tuple(
            item.exact_state_batch_provenance_sha256 for item in source_tuple
        )
        engine_identity_sha256 = sha256_json(
            self._engine_identity.model_dump(mode="json")
        )
        assembly_hash = _assembly_plan_sha256(
            source_tuple,
            engine_identity_sha256=engine_identity_sha256,
            root_tolerance_seconds=self._root_tolerance_seconds,
        )
        report_hash = _aggregate_report_sha256_values(
            sources=source_tuple,
            receipt_sha256s=tuple(self._receipt_sha256s),
            output_chunk_sha256s=tuple(self._output_chunk_sha256s),
            reconciliation_calculation_audit_sha256=(
                reconciliation_calculation_audit_sha256
            ),
            engine_identity_sha256=engine_identity_sha256,
            root_tolerance_seconds=self._root_tolerance_seconds,
            utc_start=self._output_start,
            utc_end_exclusive=self._output_end,
            batch_count=len(source_tuple),
            interval_count=self._output_interval_count,
            boundary_event_count=self._output_boundary_event_count,
            canonical_rows_sha256=logical_hash,
            logical_universe_sha256=logical_hash,
        )
        return ExactStateUniverseProvenance(
            verification_status="pass",
            assembly_plan_sha256=assembly_hash,
            ordered_source_batch_provenance_sha256s=source_hashes,
            reconciliation_report_sha256=report_hash,
            utc_start=self._output_start,
            utc_end_exclusive=self._output_end,
            batch_count=len(source_tuple),
            interval_count=self._output_interval_count,
            boundary_event_count=self._output_boundary_event_count,
            canonical_rows_sha256=logical_hash,
            logical_universe_sha256=logical_hash,
            boundary_policy_version=template.boundary_policy_version,
            feature_vector_schema_version=template.feature_vector_schema_version,
            semantic_feature_registry_sha256=(
                template.semantic_feature_registry_sha256
            ),
            feature_registry_sha256=template.feature_registry_sha256,
            chart_engine_version=template.chart_engine_version,
            ephemeris_file_set_sha256=template.ephemeris_file_set_sha256,
            node_convention=template.node_convention,
            mandala_mapping_version=template.mandala_mapping_version,
            mandala_mapping_sha256=template.mandala_mapping_sha256,
            bodygraph_mapping_sha256=template.bodygraph_mapping_sha256,
            design_root_time_tolerance_seconds=(
                template.design_root_time_tolerance_seconds
            ),
            design_root_arc_tolerance_degrees=(
                template.design_root_arc_tolerance_degrees
            ),
        )

    def _ensure_audit_open(self) -> None:
        if not self._audit_closed:
            return
        self._audit_context = self._provider.capture_calculation_audit()
        self._audit_capture = self._audit_context.__enter__()
        self._audit_closed = False

    def _close_and_certify_audit(self) -> ReconciliationCalculationAuditV1:
        if (
            self._audit_closed
            or self._audit_context is None
            or self._audit_capture is None
        ):
            raise ExactStateReconciliationError("reconciliation audit is already closed")
        self._audit_context.__exit__(None, None, None)
        self._audit_closed = True
        snapshot = self._audit_capture.snapshot()
        try:
            certified = (
                certify_swiss_calculation_audit(
                    snapshot,
                    engine_identity=self._engine_identity,
                )
                if snapshot.calculation_call_count > 0
                else None
            )
            return _reconciliation_calculation_audit(
                snapshot,
                engine_identity=self._engine_identity,
                certified=certified,
            )
        except (TypeError, ValueError, RuntimeError) as exc:
            raise ExactStateReconciliationError(
                f"reconciliation Swiss calculation audit failed: {exc}"
            ) from exc

    def _abort_audit(self) -> None:
        self._finalized = True
        if not self._audit_closed and self._audit_context is not None:
            self._audit_context.__exit__(None, None, None)
            self._audit_closed = True


def validate_reconciled_exact_state_chunk(
    chunk: ReconciledExactStateChunk,
) -> ExactStateBatchProvenance:
    """Fail closed unless a chunk and receipt still bind identical exact rows."""

    if not isinstance(chunk, ReconciledExactStateChunk) or (
        chunk._factory_token is not _RECONCILED_CHUNK_FACTORY_TOKEN
    ):
        raise ExactStateReconciliationError("chunk lacks reconciliation factory token")
    try:
        provenance = validate_verified_exact_state_batch(chunk.batch)
    except ExactStateBatchError as exc:
        raise ExactStateReconciliationError(str(exc)) from exc
    receipt = chunk.receipt
    if receipt.emitted_interval_count != len(chunk.batch.rows):
        raise ExactStateReconciliationError("chunk receipt interval count changed")
    if receipt.emitted_boundary_event_count != sum(
        len(row.boundary_events) for row in chunk.batch.rows
    ):
        raise ExactStateReconciliationError("chunk receipt event count changed")
    if receipt.emitted_canonical_rows_sha256 != canonical_rows_sha256(chunk.batch.rows):
        raise ExactStateReconciliationError("chunk receipt logical row hash changed")
    if receipt.emitted_exact_batch_provenance_sha256 != sha256_json(
        provenance.model_dump(mode="json")
    ):
        raise ExactStateReconciliationError("chunk receipt batch provenance changed")
    if receipt.emitted_utc_start != chunk.batch.rows[0].utc_start or (
        receipt.emitted_utc_end_exclusive != chunk.batch.rows[-1].utc_end
    ):
        raise ExactStateReconciliationError("chunk receipt range changed")
    return provenance


def validate_reconciliation_stream_finalization(
    finalization: ReconciliationStreamFinalization,
) -> ExactStateReconciliationAggregateProvenanceV1:
    """Require the stream capability and bind its final chunk into the aggregate."""

    if not isinstance(finalization, ReconciliationStreamFinalization) or (
        finalization._factory_token is not _RECONCILIATION_FINALIZATION_FACTORY_TOKEN
    ):
        raise ExactStateReconciliationError(
            "finalization lacks the reconciliation stream factory token"
        )
    final_provenance = validate_reconciled_exact_state_chunk(
        finalization.final_chunk
    )
    aggregate = validate_exact_state_reconciliation_aggregate_provenance(
        finalization.aggregate_provenance
    )
    expected_final_chunk_sha256 = sha256_json(
        final_provenance.model_dump(mode="json")
    )
    if aggregate.ordered_output_chunk_provenance_sha256s[-1] != (
        expected_final_chunk_sha256
    ):
        raise ExactStateReconciliationError(
            "finalization final chunk differs from aggregate output ordering"
        )
    expected_final_receipt_sha256 = sha256_json(
        finalization.final_chunk.receipt.model_dump(mode="json")
    )
    if aggregate.ordered_core_reconciliation_receipt_sha256s[-1] != (
        expected_final_receipt_sha256
    ):
        raise ExactStateReconciliationError(
            "finalization receipt differs from aggregate receipt ordering"
        )
    if finalization.final_chunk.receipt.phase != "final":
        raise ExactStateReconciliationError("finalization chunk is not the final phase")
    if final_provenance.utc_end_exclusive != (
        aggregate.exact_state_universe_provenance.utc_end_exclusive
    ):
        raise ExactStateReconciliationError(
            "finalization chunk does not end the reconciled universe"
        )
    return aggregate


def canonical_reconciliation_aggregate_bytes(
    aggregate: ExactStateReconciliationAggregateProvenanceV1,
) -> bytes:
    """Return the canonical, row-free artifact for manifest/trust-lock binding."""

    validated = validate_exact_state_reconciliation_aggregate_provenance(aggregate)
    return canonical_json_bytes(validated.model_dump(mode="json"))


def exact_state_reconciliation_aggregate_sha256(
    aggregate: ExactStateReconciliationAggregateProvenanceV1,
) -> str:
    """Hash the complete persisted reconciliation proof artifact."""

    return hashlib.sha256(canonical_reconciliation_aggregate_bytes(aggregate)).hexdigest()


def validate_exact_state_reconciliation_aggregate_provenance(
    aggregate: ExactStateReconciliationAggregateProvenanceV1,
) -> ExactStateReconciliationAggregateProvenanceV1:
    """Reparse every aggregate binding and reject noncanonical model subclasses."""

    if type(aggregate) is not ExactStateReconciliationAggregateProvenanceV1:
        raise ExactStateReconciliationError(
            "reconciliation aggregate has an unexpected runtime type"
        )
    try:
        return ExactStateReconciliationAggregateProvenanceV1.model_validate(
            aggregate.model_dump(mode="python")
        )
    except (TypeError, ValueError) as exc:
        raise ExactStateReconciliationError(
            f"reconciliation aggregate validation failed: {exc}"
        ) from exc


def _source_descriptor(
    source: OverlappingVerifiedExactStateBatch,
    ordinal: int,
) -> ReconciliationSourceV1:
    provenance = validate_verified_exact_state_batch(source.batch)
    return ReconciliationSourceV1(
        ordinal=ordinal,
        source_build_plan_sha256=source.source_build_plan_sha256,
        source_staged_receipt_sha256=source.source_staged_receipt_sha256,
        source_replay_verification_sha256=source.source_replay_verification_sha256,
        source_all_call_audit_sha256=source.source_all_call_audit_sha256,
        exact_state_batch_provenance_sha256=sha256_json(
            provenance.model_dump(mode="json")
        ),
        scan_start_utc=provenance.utc_start,
        scan_end_exclusive=provenance.utc_end_exclusive,
        core_start_utc=source.core_start_utc,
        core_end_exclusive=source.core_end_exclusive,
    )


def _validate_overlapping_source_admission(
    source: OverlappingVerifiedExactStateBatch,
    *,
    allow_test_source: bool,
) -> None:
    if not isinstance(source, OverlappingVerifiedExactStateBatch):
        raise ExactStateReconciliationError("source lacks overlap factory capability")
    if source._factory_token is _OVERLAPPING_STAGED_SOURCE_FACTORY_TOKEN:
        return
    if (
        allow_test_source
        and source._factory_token is _OVERLAPPING_TEST_SOURCE_FACTORY_TOKEN
    ):
        return
    raise ExactStateReconciliationError(
        "source lacks staged replay-verification admission"
    )


def _source_identity_sha256(source: ReconciliationSourceV1) -> str:
    return sha256_json(source.model_dump(mode="json"))


def _materialize_core_rows(
    provider: SwissEphemerisProvider,
    source: OverlappingVerifiedExactStateBatch,
) -> tuple[CenturyStateRecord, ...]:
    segments: list[
        tuple[
            datetime,
            datetime,
            tuple[str, ...],
            str,
            CenturyStateRecord,
        ]
    ] = []
    for row in source.batch.rows:
        start = max(row.utc_start, source.core_start_utc)
        end = min(row.utc_end, source.core_end_exclusive)
        if end <= start:
            continue
        events = tuple(
            event.raw
            for event in (_parse_boundary_event(raw) for raw in row.boundary_events)
            if start < event.at_utc <= end
        )
        segments.append(
            (start, end, tuple(sorted(set(events))), discrete_chart_identity_sha256(row), row)
        )
    if not segments:
        raise ExactStateReconciliationError("owned core contains no exact-state rows")
    if segments[0][0] != source.core_start_utc or (
        segments[-1][1] != source.core_end_exclusive
    ):
        raise ExactStateReconciliationError("owned core rows do not cover the declared core")

    output: list[CenturyStateRecord] = []
    provenance = source.batch.provenance
    try:
        with cacheable_serialization_session(provider) as session:
            for start, end, events, expected_identity, original in segments:
                midpoint = start + (end - start) / 2
                if (
                    start == original.utc_start
                    and end == original.utc_end
                    and midpoint == original.representative_utc
                    and events == original.boundary_events
                ):
                    row = original
                else:
                    computation = calculate_chart(
                        provider,
                        midpoint,
                        design_time_tolerance_seconds=(
                            provenance.design_root_time_tolerance_seconds
                        ),
                        design_arc_tolerance_degrees=(
                            provenance.design_root_arc_tolerance_degrees
                        ),
                    )
                    cacheable = session.serialize_cacheable_chart_state(
                        computation,
                        provider=provider,
                        utc_start=start,
                        utc_end=end,
                        boundary_events=events,
                    )
                    row = cacheable_chart_state_to_century_record(cacheable)
                if discrete_chart_identity_sha256(row) != expected_identity:
                    raise ExactStateReconciliationError(
                        "clipped core midpoint differs from its verified source state"
                    )
                output.append(row)
    except ExactStateReconciliationError:
        raise
    except (TypeError, ValueError, RuntimeError) as exc:
        raise ExactStateReconciliationError(
            f"could not recompute clipped core representative: {exc}"
        ) from exc
    return tuple(output)


def _recompute_interval(
    provider: SwissEphemerisProvider,
    *,
    start_utc: datetime,
    end_utc: datetime,
    boundary_events: tuple[str, ...],
    expected_identity_sha256: str,
    source_provenance: ExactStateBatchProvenance,
) -> CenturyStateRecord:
    midpoint = start_utc + (end_utc - start_utc) / 2
    try:
        computation = calculate_chart(
            provider,
            midpoint,
            design_time_tolerance_seconds=(
                source_provenance.design_root_time_tolerance_seconds
            ),
            design_arc_tolerance_degrees=(
                source_provenance.design_root_arc_tolerance_degrees
            ),
        )
        with cacheable_serialization_session(provider) as session:
            cacheable = session.serialize_cacheable_chart_state(
                computation,
                provider=provider,
                utc_start=start_utc,
                utc_end=end_utc,
                boundary_events=boundary_events,
            )
            row = cacheable_chart_state_to_century_record(cacheable)
    except (TypeError, ValueError, RuntimeError) as exc:
        raise ExactStateReconciliationError(
            f"could not recompute merged seam representative: {exc}"
        ) from exc
    if discrete_chart_identity_sha256(row) != expected_identity_sha256:
        raise ExactStateReconciliationError(
            "merged canonical midpoint differs from the stable seam state"
        )
    return row


def _validate_explained_partition(rows: tuple[CenturyStateRecord, ...]) -> None:
    for previous, current in zip(rows, rows[1:], strict=False):
        if previous.utc_end != current.utc_start:
            raise ExactStateReconciliationError("core rows contain a gap or overlap")
        if discrete_chart_identity_sha256(previous) == discrete_chart_identity_sha256(
            current
        ):
            raise ExactStateReconciliationError("core rows are not maximal")
        if not any(
            _parse_boundary_event(raw).at_utc == previous.utc_end
            for raw in previous.boundary_events
        ):
            raise ExactStateReconciliationError(
                "unexplained identity change inside owned core"
            )


def _reconcile_overlap(
    left: OverlappingVerifiedExactStateBatch,
    right: OverlappingVerifiedExactStateBatch,
    seam: datetime,
    *,
    root_tolerance_seconds: float,
) -> _SeamEvidence:
    overlap_start = max(left.batch.provenance.utc_start, right.batch.provenance.utc_start)
    overlap_end = min(
        left.batch.provenance.utc_end_exclusive,
        right.batch.provenance.utc_end_exclusive,
    )
    if not overlap_start < seam < overlap_end:
        raise ExactStateReconciliationError(
            "scan overlap must extend strictly across the owned core cut"
        )
    left_events = _events_in_open_range(left.batch.rows, overlap_start, overlap_end)
    right_events = _events_in_open_range(right.batch.rows, overlap_start, overlap_end)
    if any(
        not math.isclose(
            event.root_tolerance_seconds,
            root_tolerance_seconds,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
        for event in (*left_events, *right_events)
    ):
        raise ExactStateReconciliationError(
            "boundary-event tolerance differs from reconciliation policy"
        )
    matched_right: set[int] = set()
    canonical_event_times: list[datetime] = []
    duplicate_count = 0
    excluded_count = 0
    exact_at_seam = False
    for left_event in left_events:
        candidates = [
            (index, right_event)
            for index, right_event in enumerate(right_events)
            if index not in matched_right and _events_are_duplicates(left_event, right_event)
        ]
        if candidates:
            index, right_event = min(
                candidates,
                key=lambda item: abs(
                    (left_event.at_utc - item[1].at_utc).total_seconds()
                ),
            )
            matched_right.add(index)
            duplicate_count += 1
            canonical_at = _canonical_duplicate_time(left_event, right_event, seam)
            canonical_event_times.append(canonical_at)
            if canonical_at == seam:
                exact_at_seam = True
            continue
        if _event_is_safely_inside_overlap(left_event, overlap_start, overlap_end):
            raise ExactStateReconciliationError(
                "overlap disagreement: left exact boundary has no matching right event"
            )
        excluded_count += 1
    for index, right_event in enumerate(right_events):
        if index in matched_right:
            continue
        if _event_is_safely_inside_overlap(right_event, overlap_start, overlap_end):
            raise ExactStateReconciliationError(
                "overlap disagreement: right exact boundary has no matching left event"
            )
        excluded_count += 1

    cuts = tuple(
        sorted(
            {
                overlap_start,
                seam,
                overlap_end,
                *(
                    value
                    for value in canonical_event_times
                    if overlap_start < value < overlap_end
                ),
            }
        )
    )
    for start, end in zip(cuts, cuts[1:], strict=False):
        if end <= start:
            continue
        midpoint = start + (end - start) / 2
        left_identity = _source_identity_at(left.batch.rows, midpoint)
        right_identity = _source_identity_at(right.batch.rows, midpoint)
        if left_identity != right_identity:
            raise ExactStateReconciliationError(
                "overlap disagreement: verified batches encode different states"
            )

    if not exact_at_seam:
        exact_at_seam = any(
            event.at_utc == seam
            for event in (*left_events, *right_events)
            if any(
                _events_are_duplicates(event, candidate)
                for candidate in (*left_events, *right_events)
                if candidate is not event
            )
        )
    return _SeamEvidence(
        overlap_start_utc=overlap_start,
        overlap_end_exclusive=overlap_end,
        duplicate_boundary_event_count=duplicate_count,
        excluded_artificial_scan_endpoint_count=excluded_count,
        exact_event_at_core_cut=exact_at_seam,
    )


def _events_in_open_range(
    rows: tuple[CenturyStateRecord, ...],
    start: datetime,
    end: datetime,
) -> tuple[_ParsedBoundaryEvent, ...]:
    events = {
        parsed.raw: parsed
        for row in rows
        for parsed in (_parse_boundary_event(raw) for raw in row.boundary_events)
        if start < parsed.at_utc < end
    }
    return tuple(sorted(events.values(), key=lambda item: (item.at_utc, item.raw)))


def _parse_boundary_event(raw: str) -> _ParsedBoundaryEvent:
    try:
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw.encode("utf-8"):
            raise ValueError("boundary event is not canonical JSON")
        if payload["schema_version"] != "chart-boundary-event-v1":
            raise ValueError("unexpected boundary-event schema")
        at_utc = _require_utc(datetime.fromisoformat(payload["at_utc"]))
        tolerance = float(payload["root_tolerance_seconds"])
        longitude = float(payload["boundary_longitude"])
        if not math.isfinite(tolerance) or tolerance <= 0.0:
            raise ValueError("invalid root tolerance")
        if not math.isfinite(longitude):
            raise ValueError("invalid boundary longitude")
        return _ParsedBoundaryEvent(
            raw=raw,
            at_utc=at_utc,
            side=str(payload["side"]),
            body=str(payload["body"]),
            resolution=str(payload["resolution"]),
            boundary_longitude=longitude,
            before_gate=int(payload["before"]["gate"]),
            before_line=int(payload["before"]["line"]),
            after_gate=int(payload["after"]["gate"]),
            after_line=int(payload["after"]["line"]),
            root_tolerance_seconds=tolerance,
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ExactStateReconciliationError("invalid canonical boundary event") from exc


def _events_are_duplicates(
    left: _ParsedBoundaryEvent,
    right: _ParsedBoundaryEvent,
) -> bool:
    semantic_equal = (
        left.side,
        left.body,
        left.resolution,
        left.before_gate,
        left.before_line,
        left.after_gate,
        left.after_line,
    ) == (
        right.side,
        right.body,
        right.resolution,
        right.before_gate,
        right.before_line,
        right.after_gate,
        right.after_line,
    ) and math.isclose(
        left.boundary_longitude,
        right.boundary_longitude,
        rel_tol=0.0,
        abs_tol=1e-10,
    )
    separation = abs((left.at_utc - right.at_utc).total_seconds())
    return semantic_equal and separation <= max(
        left.root_tolerance_seconds,
        right.root_tolerance_seconds,
    )


def _canonical_duplicate_time(
    left: _ParsedBoundaryEvent,
    right: _ParsedBoundaryEvent,
    seam: datetime,
) -> datetime:
    if left.at_utc == seam or right.at_utc == seam:
        return seam
    return min(left.at_utc, right.at_utc)


def _event_is_safely_inside_overlap(
    event: _ParsedBoundaryEvent,
    start: datetime,
    end: datetime,
) -> bool:
    tolerance = event.root_tolerance_seconds
    return (
        (event.at_utc - start).total_seconds() > tolerance
        and (end - event.at_utc).total_seconds() > tolerance
    )


def _source_identity_at(
    rows: tuple[CenturyStateRecord, ...],
    at_utc: datetime,
) -> str:
    for row in rows:
        if row.utc_start <= at_utc < row.utc_end:
            return discrete_chart_identity_sha256(row)
    raise ExactStateReconciliationError("overlap sample is outside a source partition")


def _require_uniform_provenance(
    left: ExactStateBatchProvenance,
    right: ExactStateBatchProvenance,
) -> None:
    fields = (
        "boundary_policy_version",
        "feature_vector_schema_version",
        "semantic_feature_registry_sha256",
        "feature_registry_sha256",
        "chart_engine_version",
        "ephemeris_file_set_sha256",
        "node_convention",
        "mandala_mapping_version",
        "mandala_mapping_sha256",
        "bodygraph_mapping_sha256",
        "design_root_time_tolerance_seconds",
        "design_root_arc_tolerance_degrees",
    )
    if any(getattr(left, field) != getattr(right, field) for field in fields):
        raise ExactStateReconciliationError(
            "overlapping sources do not share frozen production identities"
        )


def _validate_reconciliation_engine_identity(
    provider: SwissEphemerisProvider,
    engine_identity: SwissEngineBuildIdentityV1,
) -> None:
    metadata = provider.metadata
    configuration_sha256, file_set_sha256 = provider.calculation_audit_identity_hashes()
    actual = {
        "Swiss library": metadata.library_version,
        "requested flags": metadata.requested_flags,
        "ephemeris mask": metadata.ephemeris_mask,
        "Node convention": metadata.node_convention.value,
        "provider configuration": configuration_sha256,
        "ephemeris file set": file_set_sha256,
    }
    required = {
        "Swiss library": engine_identity.swiss_library_version,
        "requested flags": engine_identity.requested_flags,
        "ephemeris mask": engine_identity.ephemeris_mask,
        "Node convention": engine_identity.node_convention,
        "provider configuration": engine_identity.provider_configuration_sha256,
        "ephemeris file set": engine_identity.canonical_ephemeris_file_set_sha256,
    }
    if actual != required:
        raise ExactStateReconciliationError(
            "current Swiss provider differs from the frozen reconciliation engine"
        )


def _reconciled_partition_sha256(rows: tuple[CenturyStateRecord, ...]) -> str:
    return sha256_json(
        {
            "schema_version": "reconciled-exact-state-partition-v1",
            "reconciliation_policy_version": RECONCILIATION_POLICY_VERSION,
            "boundary_event_catalog_sha256": BOUNDARY_EVENT_CATALOG_SHA256,
            "rows": [
                {
                    "utc_start": row.utc_start,
                    "utc_end": row.utc_end,
                    "representative_utc": row.representative_utc,
                    "design_timestamp": row.design_timestamp,
                    "discrete_identity_sha256": discrete_chart_identity_sha256(row),
                    "boundary_events": row.boundary_events,
                }
                for row in rows
            ],
        }
    )


def _assembly_plan_sha256(
    sources: tuple[ReconciliationSourceV1, ...],
    *,
    engine_identity_sha256: str,
    root_tolerance_seconds: float,
) -> str:
    return sha256_json(
        {
            "schema_version": "streaming-exact-state-assembly-plan-v1",
            "reconciliation_policy_version": RECONCILIATION_POLICY_VERSION,
            "boundary_event_catalog_sha256": BOUNDARY_EVENT_CATALOG_SHA256,
            "engine_identity_sha256": engine_identity_sha256,
            "root_tolerance_seconds": root_tolerance_seconds,
            "ordered_sources": [item.model_dump(mode="json") for item in sources],
        }
    )


def _aggregate_report_sha256(
    *,
    sources: tuple[ReconciliationSourceV1, ...],
    receipt_sha256s: tuple[str, ...],
    output_chunk_sha256s: tuple[str, ...],
    reconciliation_calculation_audit_sha256: str,
    engine_identity_sha256: str,
    root_tolerance_seconds: float,
    exact: ExactStateUniverseProvenance,
) -> str:
    return _aggregate_report_sha256_values(
        sources=sources,
        receipt_sha256s=receipt_sha256s,
        output_chunk_sha256s=output_chunk_sha256s,
        reconciliation_calculation_audit_sha256=(
            reconciliation_calculation_audit_sha256
        ),
        engine_identity_sha256=engine_identity_sha256,
        root_tolerance_seconds=root_tolerance_seconds,
        utc_start=exact.utc_start,
        utc_end_exclusive=exact.utc_end_exclusive,
        batch_count=exact.batch_count,
        interval_count=exact.interval_count,
        boundary_event_count=exact.boundary_event_count,
        canonical_rows_sha256=exact.canonical_rows_sha256,
        logical_universe_sha256=exact.logical_universe_sha256,
    )


def _aggregate_report_sha256_values(
    *,
    sources: tuple[ReconciliationSourceV1, ...],
    receipt_sha256s: tuple[str, ...],
    output_chunk_sha256s: tuple[str, ...],
    reconciliation_calculation_audit_sha256: str,
    engine_identity_sha256: str,
    root_tolerance_seconds: float,
    utc_start: datetime,
    utc_end_exclusive: datetime,
    batch_count: int,
    interval_count: int,
    boundary_event_count: int,
    canonical_rows_sha256: str,
    logical_universe_sha256: str,
) -> str:
    return sha256_json(
        {
            "schema_version": "streaming-exact-state-reconciliation-report-v1",
            "reconciliation_policy_version": RECONCILIATION_POLICY_VERSION,
            "boundary_event_catalog_sha256": BOUNDARY_EVENT_CATALOG_SHA256,
            "engine_identity_sha256": engine_identity_sha256,
            "root_tolerance_seconds": root_tolerance_seconds,
            "ordered_source_identity_sha256s": [
                _source_identity_sha256(item) for item in sources
            ],
            "ordered_source_staged_receipt_sha256s": [
                item.source_staged_receipt_sha256 for item in sources
            ],
            "ordered_source_replay_verification_sha256s": [
                item.source_replay_verification_sha256 for item in sources
            ],
            "ordered_source_all_call_audit_sha256s": [
                item.source_all_call_audit_sha256 for item in sources
            ],
            "ordered_core_reconciliation_receipt_sha256s": receipt_sha256s,
            "ordered_output_chunk_provenance_sha256s": output_chunk_sha256s,
            "reconciliation_calculation_audit_sha256": (
                reconciliation_calculation_audit_sha256
            ),
            "utc_start": utc_start,
            "utc_end_exclusive": utc_end_exclusive,
            "batch_count": batch_count,
            "interval_count": interval_count,
            "boundary_event_count": boundary_event_count,
            "canonical_rows_sha256": canonical_rows_sha256,
            "logical_universe_sha256": logical_universe_sha256,
        }
    )


def _reconciliation_calculation_audit(
    snapshot: SwissCalculationAuditSnapshot,
    *,
    engine_identity: SwissEngineBuildIdentityV1,
    certified: SwissCalculationAuditV1 | None,
) -> ReconciliationCalculationAuditV1:
    expected = (
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
    if any(actual != required for actual, required in expected):
        raise ExactStateReconciliationError(
            "reconciliation audit differs from the frozen engine identity"
        )
    return ReconciliationCalculationAuditV1(
        verification_status="pass",
        outcome=(
            "all_calls_swieph"
            if snapshot.calculation_call_count > 0
            else "no_recomputation_required"
        ),
        engine_identity_sha256=sha256_json(engine_identity.model_dump(mode="json")),
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
        exit_provider_configuration_sha256=(
            snapshot.exit_provider_configuration_sha256
        ),
        entry_ephemeris_file_set_sha256=(
            snapshot.entry_ephemeris_file_set_sha256
        ),
        exit_ephemeris_file_set_sha256=snapshot.exit_ephemeris_file_set_sha256,
        certified_nonempty_audit=certified,
    )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ExactStateReconciliationError("reconciliation timestamps must be aware")
    return value.astimezone(UTC)


def _raise_missing_source() -> VerifiedExactStateBatch:
    raise ExactStateReconciliationError("reconciliation mint source is missing")
