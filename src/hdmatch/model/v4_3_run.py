"""Memory-bounded, cache-only canonical V4.3 universe runs.

The run API exposes no chart-engine object, ephemeris path, or cache-rebuild
callback. It consumes only exact artifacts that have already passed cache,
mapping, response, and prevalence verification. Ranking uses the five frozen
fields directly in an on-disk SQLite sort; no scalar score is introduced.
"""

from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import math
import os
import platform
import shutil
import sqlite3
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import suppress
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from importlib import import_module, metadata
from itertools import zip_longest
from pathlib import Path
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.century_cache.plan_lock import (
    VerifiedCenturyBuildPlanTrust,
    verify_century_build_plan_against_trust_lock,
)
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.model.v4_3.compliance import V43Compliance
from hdmatch.model.v4_3.contracts import V43_RANKING_POLICY_VERSION
from hdmatch.model.v4_3.integration import (
    CanonicalV43Bindings,
    CanonicalV43CandidateEvaluation,
    CanonicalV43ScoringSession,
    V43UniverseStreamError,
)
from hdmatch.model.v4_3_compiler import compile_verified_mapping_library_v2
from hdmatch.model.v4_3_mapping import MappingLibrarySourceV2, MappingLibraryV2
from hdmatch.model.v4_3_prevalence import (
    VerifiedV43ConditionalPrevalence,
    verify_v4_3_prevalence_artifact,
)
from hdmatch.model.v4_3_responses import (
    VerifiedV43DirectTargetResponses,
    verify_v4_3_direct_target_responses,
)

SHA256_PATTERN: Final[str] = r"^[a-f0-9]{64}$"
V43_RUNNER_VERSION: Final[str] = "v4.3-cache-stream-run-v4"
SCORE_HASH_STRATEGY: Final[str] = "sha256-canonical-json-lines-input-order-v1"
RANKED_HASH_STRATEGY: Final[str] = "sha256-canonical-json-lines-rank-order-v1"
RANKED_FILENAME: Final[str] = "ranked-scores.parquet.zst"
DETAIL_FILENAME: Final[str] = "bounded-detail.json"
FAILURE_FILENAME: Final[str] = "failure.json"
PRODUCER_FAILURE_DIAGNOSTICS_FILENAME: Final[str] = (
    "producer-failure-diagnostics.json"
)
PARTIAL_SCORES_FILENAME: Final[str] = "partial-scores.jsonl"
MANIFEST_FILENAME: Final[str] = "manifest.json"
PARQUET_BATCH_ROWS: Final[int] = 1024
MAX_DETAIL_ROWS: Final[int] = 10_000
_RUNTIME_DEPENDENCY_DISTRIBUTIONS: Final[tuple[str, ...]] = (
    "hdmatch",
    "pyarrow",
    "pydantic",
)


class V43RunError(RuntimeError):
    """A Phase-4 run or its immutable output violates the cache-only contract."""


class V43FailureStage(StrEnum):
    SCORE_STORE_OPEN = "score-store-open"
    EVALUATION = "evaluation"
    PARTIAL_SCORE_JOURNAL = "partial-score-journal"
    SCORE_STORE_APPEND = "score-store-append"
    SCORE_STORE_COMMIT = "score-store-commit"
    SCORE_STORE_FINALIZE = "score-store-finalize"
    RANKED_ARTIFACT = "ranked-artifact"
    BOUNDED_DETAIL = "bounded-detail"
    COMPLIANCE = "compliance"
    MANIFEST = "manifest"
    STAGED_VERIFICATION = "staged-verification"


_FAILURE_SEMANTICS: Final[dict[V43FailureStage, tuple[str, str]]] = {
    stage: (
        f"v4_3_{stage.value.replace('-', '_')}_failure",
        f"V4.3 cache run failed during {stage.value}.",
    )
    for stage in V43FailureStage
}


class V43RunFailedError(V43RunError):
    """Scoring/storage failed after preflight and a failure package was published."""

    def __init__(
        self,
        run_directory: Path,
        failure: V43RunFailureV1,
        *,
        publication_error: Exception | None = None,
    ) -> None:
        self.run_directory = run_directory
        self.failure = failure
        self.publication_error = publication_error
        suffix = (
            "; failure-package publication or durability is incomplete"
            if publication_error is not None
            else ""
        )
        super().__init__(
            "V4.3 run failed at producer-reported stage "
            f"{failure.producer_reported_stage}; failure package: {run_directory}"
            f"{suffix}"
        )


class V43RunPublicationPendingError(V43RunError):
    """A verified success was renamed but its parent fsync did not complete."""

    def __init__(self, run_directory: Path, cause: OSError) -> None:
        self.run_directory = run_directory
        self.cause = cause
        super().__init__(
            "V4.3 run is verified and visible but publication durability is "
            f"pending finalization: {run_directory}"
        )


class V43RunPublicationConflictError(V43RunError):
    """Another publisher claimed the destination before this run could."""

    def __init__(
        self,
        run_directory: Path,
        *,
        preserved_staging_directory: Path | None = None,
    ) -> None:
        self.run_directory = run_directory
        self.preserved_staging_directory = preserved_staging_directory
        super().__init__(
            "V4.3 run destination was claimed concurrently and was not overwritten: "
            f"{run_directory}"
        )


class V43ScoreStoreAppendError(V43RunError):
    """SQLite rejected one exact score-row insert."""


class V43ScoreStoreCommitError(V43RunError):
    """SQLite could not durably commit the current score-row transaction."""


class _V43FailurePackagePublicationError(RuntimeError):
    """A complete failure package remains staged after publication failed."""

    def __init__(self, staging_directory: Path, cause: Exception) -> None:
        self.staging_directory = staging_directory
        self.cause = cause
        super().__init__(
            f"failure package remains staged at {staging_directory}: {cause}"
        )


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class V43MinimalScoreRecordV1(_FrozenModel):
    """Minimal score facts required to reproduce the exact rank tuple."""

    schema_version: Literal["v4-3-minimal-score-record-v1"] = (
        "v4-3-minimal-score-record-v1"
    )
    input_ordinal: int = Field(ge=0)
    state_id: str = Field(min_length=1)
    candidate_record_sha256: str = Field(pattern=SHA256_PATTERN)
    utc_start: datetime
    utc_end_exclusive: datetime
    stable_duration_microseconds: int = Field(gt=0)
    evidence_rubric_bits: float
    contradiction_rubric_bits: float
    net_information: float
    meaningful_contradictions: int = Field(ge=0)
    detailed_support: float = Field(ge=0.0, le=100.0)
    core_fit: float = Field(ge=0.0, le=100.0)
    unresolved_observation_count: int = Field(ge=0)

    @model_validator(mode="after")
    def require_exact_finite_score(self) -> V43MinimalScoreRecordV1:
        if self.utc_start.tzinfo is None or self.utc_start.utcoffset() is None:
            raise ValueError("score UTC start must be timezone-aware")
        if self.utc_end_exclusive.tzinfo is None or self.utc_end_exclusive.utcoffset() is None:
            raise ValueError("score UTC end must be timezone-aware")
        if self.utc_start.utcoffset() != timedelta(0) or (
            self.utc_end_exclusive.utcoffset() != timedelta(0)
        ):
            raise ValueError("score timestamps must use zero UTC offset")
        exact_duration = _duration_microseconds(
            self.utc_end_exclusive - self.utc_start
        )
        if exact_duration != self.stable_duration_microseconds:
            raise ValueError("score duration differs from its exact stable interval")
        numeric = (
            self.evidence_rubric_bits,
            self.contradiction_rubric_bits,
            self.net_information,
            self.detailed_support,
            self.core_fit,
        )
        if not all(math.isfinite(item) for item in numeric):
            raise ValueError("minimal score fields must be finite")
        if not math.isclose(
            self.net_information,
            self.evidence_rubric_bits - self.contradiction_rubric_bits,
            rel_tol=1e-15,
            abs_tol=1e-15,
        ):
            raise ValueError("NetInformation contains a hidden scalar contribution")
        return self

    @property
    def substantive_rank_key(self) -> tuple[float, int, float, float, int]:
        return (
            -self.net_information,
            self.meaningful_contradictions,
            -self.detailed_support,
            -self.core_fit,
            -self.stable_duration_microseconds,
        )

    @property
    def display_key(self) -> tuple[datetime, str]:
        return (self.utc_start, self.state_id)


class V43RankedScoreRecordV1(_FrozenModel):
    score: V43MinimalScoreRecordV1
    rank_start: int = Field(gt=0)
    rank_end: int = Field(gt=0)
    midrank_numerator: int = Field(gt=0)
    midrank_denominator: Literal[2] = 2
    substantively_tied: bool

    @model_validator(mode="after")
    def require_exact_rank_interval(self) -> V43RankedScoreRecordV1:
        if self.rank_end < self.rank_start:
            raise ValueError("rank interval is reversed")
        if self.midrank_numerator != self.rank_start + self.rank_end:
            raise ValueError("midrank numerator differs from exact rank interval")
        if self.substantively_tied != (self.rank_start != self.rank_end):
            raise ValueError("tie flag differs from exact rank interval")
        return self


class V43RunArtifactV1(_FrozenModel):
    filename: str = Field(min_length=1)
    sha256: str = Field(pattern=SHA256_PATTERN)
    byte_count: int = Field(ge=0)
    row_count: int = Field(ge=0)
    logical_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_hash_strategy: str = Field(min_length=1)
    storage_format: str = Field(min_length=1)


class V43RuntimeSourceFileV1(_FrozenModel):
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=SHA256_PATTERN)


class V43RuntimeSourceProvenanceV1(_FrozenModel):
    """Clean committed source tree and executable runtime identity."""

    schema_version: Literal["v4-3-runtime-source-provenance-v1"] = (
        "v4-3-runtime-source-provenance-v1"
    )
    source_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    source_tree_git_oid: str = Field(pattern=r"^[a-f0-9]{40,64}$")
    source_files: tuple[V43RuntimeSourceFileV1, ...] = Field(min_length=1)
    source_code_fingerprint_sha256: str = Field(pattern=SHA256_PATTERN)
    python_version: str = Field(min_length=1)
    python_implementation: str = Field(min_length=1)
    sqlite_version: str = Field(min_length=1)
    dependency_versions: dict[str, str] = Field(min_length=1)

    @model_validator(mode="after")
    def require_canonical_source_inventory(self) -> V43RuntimeSourceProvenanceV1:
        paths = tuple(item.path for item in self.source_files)
        if paths != tuple(sorted(set(paths))):
            raise ValueError("runtime source-file inventory must be sorted and unique")
        expected_fingerprint = sha256_json(
            [item.model_dump(mode="json") for item in self.source_files]
        )
        if self.source_code_fingerprint_sha256 != expected_fingerprint:
            raise ValueError("runtime source-code fingerprint differs from its files")
        if tuple(self.dependency_versions) != tuple(
            sorted(self.dependency_versions)
        ):
            raise ValueError("runtime dependency versions must be sorted")
        return self


class V43ProducerFailureDiagnosticsV1(_FrozenModel):
    """Unauthenticated producer report retained for failure diagnosis only."""

    schema_version: Literal["v4-3-producer-failure-diagnostics-v1"] = (
        "v4-3-producer-failure-diagnostics-v1"
    )
    scope: Literal["producer-reported-internal-consistency-only"] = (
        "producer-reported-internal-consistency-only"
    )
    historically_authenticated: Literal[False] = False
    producer_reported_stage: V43FailureStage
    attempted_input_ordinal: int | None = Field(default=None, ge=0)
    attempted_record_is_in_partial_scores: bool
    successfully_evaluated_count: int = Field(ge=0)
    producer_reported_sqlite_inserted_count: int = Field(ge=0)
    producer_reported_sqlite_persisted_count: int = Field(ge=0)
    sqlite_commit_batch_rows: Literal[1024] = 1024
    partial_score_records_sha256: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_reproducible_operation_frontier(
        self,
    ) -> V43ProducerFailureDiagnosticsV1:
        expected_inserted = _expected_failure_inserted_count(
            stage=self.producer_reported_stage,
            evaluated_count=self.successfully_evaluated_count,
            attempted_record_is_in_partial_scores=(
                self.attempted_record_is_in_partial_scores
            ),
        )
        if self.producer_reported_sqlite_inserted_count != expected_inserted:
            raise ValueError(
                "producer-reported stage disagrees with producer operation counters"
            )
        if (
            self.producer_reported_sqlite_persisted_count
            > self.producer_reported_sqlite_inserted_count
        ):
            raise ValueError(
                "producer-reported persistence exceeds producer insertion count"
            )
        return self


class V43RunFailureV1(_FrozenModel):
    schema_version: Literal["v4-3-run-failure-v4"] = "v4-3-run-failure-v4"
    diagnostics_scope: Literal["producer-reported-internal-consistency-only"] = (
        "producer-reported-internal-consistency-only"
    )
    diagnostics_historically_authenticated: Literal[False] = False
    producer_reported_stage: V43FailureStage
    failure_code: str = Field(min_length=1)
    error_type: str = Field(min_length=1)
    error_message: str = Field(min_length=1)
    producer_reported_cause_type: str = Field(min_length=1)
    producer_reported_cause_message: str = Field(min_length=1)
    attempted_input_ordinal: int | None = Field(default=None, ge=0)
    attempted_state_id: str | None = None
    attempted_candidate_record_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    attempted_record_is_in_partial_scores: bool
    successfully_evaluated_count: int = Field(ge=0)
    persisted_scored_count: int = Field(ge=0)
    partial_score_records_sha256: str = Field(pattern=SHA256_PATTERN)
    producer_diagnostics_sha256: str = Field(pattern=SHA256_PATTERN)
    score_hash_strategy: Literal[
        "sha256-canonical-json-lines-input-order-v1"
    ] = "sha256-canonical-json-lines-input-order-v1"

    @model_validator(mode="after")
    def require_deterministic_failure_semantics(self) -> V43RunFailureV1:
        expected_type, expected_message = _FAILURE_SEMANTICS[
            self.producer_reported_stage
        ]
        if self.failure_code != expected_type:
            raise ValueError("failure code differs from its deterministic stage")
        if self.error_type != expected_type or self.error_message != expected_message:
            raise ValueError("failure semantic type/message differs from its stage")
        if self.persisted_scored_count > self.successfully_evaluated_count:
            raise ValueError("persisted score count exceeds evaluated score count")
        row_fields = (
            self.attempted_input_ordinal,
            self.attempted_state_id,
            self.attempted_candidate_record_sha256,
        )
        if any(value is None for value in row_fields) != all(
            value is None for value in row_fields
        ):
            raise ValueError("attempted failure-row binding is incomplete")
        if self.attempted_input_ordinal is None:
            if self.attempted_record_is_in_partial_scores:
                raise ValueError("unbound failure row cannot be in partial scores")
        elif self.attempted_record_is_in_partial_scores:
            if self.attempted_input_ordinal != self.successfully_evaluated_count - 1:
                raise ValueError("evaluated failure row has the wrong ordinal")
        elif self.attempted_input_ordinal != self.successfully_evaluated_count:
            raise ValueError("unevaluated failure row has the wrong ordinal")
        if self.producer_reported_stage is V43FailureStage.SCORE_STORE_OPEN and (
            self.successfully_evaluated_count != 0
            or self.persisted_scored_count != 0
            or self.attempted_input_ordinal is not None
        ):
            raise ValueError("score-store-open failure cannot contain score rows")
        if self.producer_reported_stage is V43FailureStage.EVALUATION and (
            self.attempted_input_ordinal is None
            or self.attempted_record_is_in_partial_scores
        ):
            raise ValueError("evaluation failure must bind its unevaluated cache row")
        if self.producer_reported_stage in {
            V43FailureStage.SCORE_STORE_APPEND,
            V43FailureStage.SCORE_STORE_COMMIT,
        } and (
            self.attempted_input_ordinal is None
            or not self.attempted_record_is_in_partial_scores
        ):
            raise ValueError(
                "score-store append/commit failure must bind its evaluated row"
            )
        if self.producer_reported_stage in {
            V43FailureStage.SCORE_STORE_FINALIZE,
            V43FailureStage.RANKED_ARTIFACT,
            V43FailureStage.BOUNDED_DETAIL,
            V43FailureStage.COMPLIANCE,
            V43FailureStage.MANIFEST,
            V43FailureStage.STAGED_VERIFICATION,
        } and self.attempted_input_ordinal is not None:
            raise ValueError("post-stream failure cannot bind one attempted row")
        return self


class V43RunComplianceV1(_FrozenModel):
    protocol_version: Literal["V4.3"]
    reported_model_version: Literal["V4.3"]
    status: Literal["compliant"]
    calculation_tier: Literal["M2"]
    scoring_tier: Literal["M2"]
    required_feature_count: int = Field(gt=0)
    available_required_feature_count: int = Field(gt=0)
    required_feature_coverage: float
    missing_required_feature_ids: tuple[str, ...] = ()
    simplified: Literal[False]
    cache_verified: Literal[True]
    ephemeris_requested: Literal["SWIEPH"]
    ephemeris_returned: Literal["SWIEPH"]
    flexibility_penalty_enabled: Literal[True]
    conditional_prevalence_enabled: Literal[True]
    v4_3_compliant: Literal[True]
    failure_reasons: tuple[str, ...] = ()

    @model_validator(mode="after")
    def require_complete_feature_claim(self) -> V43RunComplianceV1:
        if self.required_feature_coverage != 1.0:
            raise ValueError("claim-grade feature coverage must equal 1.0")
        if self.missing_required_feature_ids or self.failure_reasons:
            raise ValueError("claim-grade compliance cannot retain failures")
        if self.available_required_feature_count != self.required_feature_count:
            raise ValueError("claim-grade available feature count is incomplete")
        return self


class V43RunBindingsV1(_FrozenModel):
    mapping_library_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_source_library_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_prevalence_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    response_source_mode: Literal["direct_behavioral_target"]
    response_source_id: str = Field(min_length=1)
    response_source_sha256: str = Field(pattern=SHA256_PATTERN)
    behavioral_target_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: None = None
    direct_target_response_artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    response_set_sha256: str = Field(pattern=SHA256_PATTERN)
    prevalence_artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    prevalence_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    prevalence_parent_hierarchy_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_trust_lock_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_plan_trust_lock_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_generation_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    cache_engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_plan_engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)


class V43RunManifestV1(_FrozenModel):
    schema_version: Literal["v4-3-cache-run-manifest-v4"] = (
        "v4-3-cache-run-manifest-v4"
    )
    runner_version: Literal["v4.3-cache-stream-run-v4"] = (
        "v4.3-cache-stream-run-v4"
    )
    runner_source_sha256: str = Field(pattern=SHA256_PATTERN)
    runtime_source_provenance: V43RuntimeSourceProvenanceV1
    run_status: Literal["complete", "failed"]
    ranking_policy_version: Literal["v4.3-lexicographic-rank-v1"] = (
        "v4.3-lexicographic-rank-v1"
    )
    bindings: V43RunBindingsV1
    declared_interval_count: int = Field(gt=0)
    successfully_scored_count: int = Field(ge=0)
    score_records_sha256: str = Field(pattern=SHA256_PATTERN)
    score_hash_strategy: Literal[
        "sha256-canonical-json-lines-input-order-v1"
    ] = "sha256-canonical-json-lines-input-order-v1"
    ranked_artifact: V43RunArtifactV1 | None = None
    bounded_detail_artifact: V43RunArtifactV1 | None = None
    failure_artifact: V43RunArtifactV1 | None = None
    producer_failure_diagnostics_artifact: V43RunArtifactV1 | None = None
    failure_diagnostics_scope: (
        Literal["producer-reported-internal-consistency-only"] | None
    ) = None
    partial_score_artifact: V43RunArtifactV1 | None = None
    successfully_evaluated_count: int = Field(ge=0)
    persisted_scored_count: int = Field(ge=0)
    substantive_tie_group_count: int = Field(ge=0)
    tied_candidate_count: int = Field(ge=0)
    unresolved_observation_count_per_candidate: int = Field(ge=0)
    unresolved_mapping_ids: tuple[str, ...]
    compliance: V43RunComplianceV1 | None = None

    @model_validator(mode="after")
    def require_status_specific_artifacts(self) -> V43RunManifestV1:
        if self.unresolved_mapping_ids != tuple(sorted(set(self.unresolved_mapping_ids))):
            raise ValueError("unresolved mapping IDs must be sorted and unique")
        if self.run_status == "complete":
            if self.successfully_scored_count != self.declared_interval_count:
                raise ValueError("complete run did not score the full declared universe")
            if (
                self.ranked_artifact is None
                or self.bounded_detail_artifact is None
                or self.failure_artifact is not None
                or self.producer_failure_diagnostics_artifact is not None
                or self.failure_diagnostics_scope is not None
                or self.partial_score_artifact is not None
                or self.compliance is None
            ):
                raise ValueError("complete run artifact inventory is inconsistent")
        elif (
            self.failure_artifact is None
            or self.producer_failure_diagnostics_artifact is None
            or self.failure_diagnostics_scope
            != "producer-reported-internal-consistency-only"
            or self.partial_score_artifact is None
            or self.ranked_artifact is not None
            or self.bounded_detail_artifact is not None
            or self.compliance is not None
        ):
            raise ValueError(
                "failed run must contain failure and partial-score artifacts only"
            )
        if self.run_status == "complete" and (
            self.successfully_evaluated_count != self.declared_interval_count
            or self.persisted_scored_count != self.declared_interval_count
        ):
            raise ValueError("complete run score accounting is incomplete")
        if self.run_status == "failed" and (
            self.successfully_scored_count != self.persisted_scored_count
        ):
            raise ValueError("failed manifest legacy/persisted counts differ")
        return self


@dataclass(frozen=True, slots=True)
class VerifiedV43Run:
    run_directory: Path
    manifest_path: Path
    manifest_sha256: str
    manifest: V43RunManifestV1


@dataclass(frozen=True, slots=True)
class _RankedWriteSummary:
    artifact: V43RunArtifactV1
    substantive_tie_group_count: int
    tied_candidate_count: int
    bounded_top_records: tuple[V43RankedScoreRecordV1, ...]
    bounded_tie_groups: tuple[dict[str, object], ...]
    detail_truncated: bool


class V43PartialScoreJournal:
    """Bounded-memory canonical JSON-lines journal of every evaluated score."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._handle = self._path.open("xb")
        self._batch: list[bytes] = []
        self._count = 0
        self._durable_count = 0
        self._durable_byte_count = 0
        self._digest = hashlib.sha256()
        self._closed = False

    @property
    def count(self) -> int:
        return self._count

    @property
    def sha256(self) -> str:
        return self._digest.hexdigest()

    def append(self, record: V43MinimalScoreRecordV1) -> None:
        if self._closed:
            raise V43RunError("partial-score journal is closed")
        if record.input_ordinal != self._count:
            raise V43RunError("partial-score journal order differs from cache order")
        line = canonical_json_bytes(record) + b"\n"
        self._batch.append(line)
        self._digest.update(line)
        self._count += 1
        if len(self._batch) == PARQUET_BATCH_ROWS:
            self._flush_batch()

    def _flush_batch(self) -> None:
        if not self._batch:
            return
        payload = b"".join(self._batch)
        try:
            self._handle.write(payload)
            self._handle.flush()
            os.fsync(self._handle.fileno())
        except OSError:
            with suppress(OSError):
                self._handle.seek(self._durable_byte_count)
                self._handle.truncate()
                self._handle.flush()
            raise
        self._durable_byte_count += len(payload)
        self._durable_count += len(self._batch)
        self._batch.clear()

    def finalize(self) -> None:
        if self._closed:
            raise V43RunError("partial-score journal was already closed")
        self._flush_batch()
        self._handle.close()
        self._closed = True
        if self._durable_count != self._count:
            raise V43RunError("partial-score journal did not persist every evaluation")

    def discard(self) -> None:
        if not self._closed:
            self._handle.close()
            self._closed = True
        self._path.unlink(missing_ok=True)

    def move_finalized(self, destination: Path) -> Path:
        if not self._closed:
            self.finalize()
        if not self._path.is_file() or self._path.is_symlink():
            raise V43RunError("partial-score journal is unavailable for publication")
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"partial-score destination exists: {destination}")
        os.rename(self._path, destination)
        return destination


class V43ExternalRankStore:
    """Disk-backed exact five-field ranking with bounded process memory."""

    def __init__(self, database_path: str | Path) -> None:
        self._path = Path(database_path)
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(self._path)
            connection.execute("PRAGMA journal_mode=OFF")
            connection.execute("PRAGMA synchronous=OFF")
            connection.execute("PRAGMA temp_store=FILE")
            connection.execute(
                """
                CREATE TABLE score_records (
                    input_ordinal INTEGER PRIMARY KEY,
                    state_id TEXT NOT NULL UNIQUE,
                    utc_start_microseconds INTEGER NOT NULL,
                    net_information REAL NOT NULL,
                    meaningful_contradictions INTEGER NOT NULL,
                    detailed_support REAL NOT NULL,
                    core_fit REAL NOT NULL,
                    stable_duration_microseconds INTEGER NOT NULL,
                    payload BLOB NOT NULL
                )
                """
            )
        except (OSError, sqlite3.Error):
            if connection is not None:
                with suppress(sqlite3.Error):
                    connection.close()
            raise
        self._connection = connection
        self._digest = hashlib.sha256()
        self._count = 0
        self._persisted_count = 0
        self._finished = False
        self._append_mode: Literal["ordered", "verification-unordered"] | None = None

    @property
    def count(self) -> int:
        return self._count

    @property
    def persisted_count(self) -> int:
        return self._persisted_count

    @property
    def score_records_sha256(self) -> str:
        if not self._finished:
            raise V43RunError("external rank store has not been finalized")
        return self._digest.hexdigest()

    @property
    def partial_score_records_sha256(self) -> str:
        if self._append_mode == "verification-unordered":
            raise V43RunError(
                "unordered verification records have no partial input-order hash"
            )
        return self._digest.hexdigest()

    def append(self, record: V43MinimalScoreRecordV1) -> None:
        if self._finished:
            raise V43RunError("cannot append after external ranking finalization")
        if self._append_mode == "verification-unordered":
            raise V43RunError("cannot mix ordered and unordered score-store appends")
        if record.input_ordinal != self._count:
            raise V43RunError("score records must be appended in exact cache order")
        payload = canonical_json_bytes(record)
        self._insert_record(record, payload)
        self._append_mode = "ordered"
        self._digest.update(payload)
        self._digest.update(b"\n")
        self._count += 1
        if self._count % PARQUET_BATCH_ROWS == 0:
            self._commit_pending()

    def append_unordered_for_verification(
        self,
        record: V43MinimalScoreRecordV1,
    ) -> None:
        """Load rank-ordered persisted rows before rebuilding input-order evidence."""

        if self._finished:
            raise V43RunError("cannot append after external ranking finalization")
        if self._append_mode == "ordered":
            raise V43RunError("cannot mix unordered and ordered score-store appends")
        self._insert_record(record, canonical_json_bytes(record))
        self._append_mode = "verification-unordered"
        self._count += 1
        if self._count % PARQUET_BATCH_ROWS == 0:
            self._commit_pending()

    def _insert_record(
        self,
        record: V43MinimalScoreRecordV1,
        payload: bytes,
    ) -> None:
        try:
            self._connection.execute(
                """
                INSERT INTO score_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.input_ordinal,
                    record.state_id,
                    _utc_epoch_microseconds(record.utc_start),
                    record.net_information,
                    record.meaningful_contradictions,
                    record.detailed_support,
                    record.core_fit,
                    record.stable_duration_microseconds,
                    payload,
                ),
            )
        except (OSError, sqlite3.Error) as exc:
            raise V43ScoreStoreAppendError(
                "SQLite rejected an exact score row"
            ) from exc

    def finish(self) -> None:
        if self._finished:
            raise V43RunError("external rank store was already finalized")
        self._commit_pending()
        self._finished = True

    def _commit_pending(self) -> None:
        try:
            self._commit_database()
        except (OSError, sqlite3.Error) as exc:
            raise V43ScoreStoreCommitError(
                "SQLite could not commit exact score rows"
            ) from exc
        self._persisted_count = self._count

    def _commit_database(self) -> None:
        self._connection.commit()

    def finish_unordered_for_verification(self) -> None:
        """Prove a contiguous input ordinal set and rebuild its exact line hash."""

        if self._finished:
            raise V43RunError("external rank store was already finalized")
        if self._append_mode not in (None, "verification-unordered"):
            raise V43RunError("ordered score store needs ordinary finalization")
        count, minimum, maximum, distinct_count = self._connection.execute(
            """
            SELECT COUNT(*), MIN(input_ordinal), MAX(input_ordinal),
                   COUNT(DISTINCT input_ordinal)
            FROM score_records
            """
        ).fetchone()
        if int(count) != self._count or int(distinct_count) != self._count:
            raise V43RunError("verification store contains duplicate score ordinals")
        if self._count and (int(minimum) != 0 or int(maximum) != self._count - 1):
            raise V43RunError(
                "verification store score ordinals are not a contiguous universe"
            )
        digest = hashlib.sha256()
        for (payload,) in self._connection.execute(
            "SELECT payload FROM score_records ORDER BY input_ordinal ASC"
        ):
            digest.update(payload)
            digest.update(b"\n")
        self._digest = digest
        self._commit_pending()
        self._finished = True

    def iter_input_order(self) -> Iterator[V43MinimalScoreRecordV1]:
        if not self._finished:
            raise V43RunError("external rank store has not been finalized")
        cursor = self._connection.execute(
            "SELECT payload FROM score_records ORDER BY input_ordinal ASC"
        )
        for (payload,) in cursor:
            yield V43MinimalScoreRecordV1.model_validate_json(payload, strict=True)

    def iter_ranked(self) -> Iterator[V43RankedScoreRecordV1]:
        if not self._finished:
            raise V43RunError("external rank store has not been finalized")
        cursor = self._connection.execute(_RANK_QUERY)
        for payload, rank_start, tie_count in cursor:
            score = V43MinimalScoreRecordV1.model_validate_json(payload, strict=True)
            start = int(rank_start)
            end = start + int(tie_count) - 1
            yield V43RankedScoreRecordV1(
                score=score,
                rank_start=start,
                rank_end=end,
                midrank_numerator=start + end,
                substantively_tied=start != end,
            )

    def close(self) -> None:
        self._connection.close()


_RANK_QUERY: Final[str] = """
WITH ranked AS (
    SELECT
        payload,
        state_id,
        utc_start_microseconds,
        net_information,
        meaningful_contradictions,
        detailed_support,
        core_fit,
        stable_duration_microseconds,
        RANK() OVER (
            ORDER BY
                net_information DESC,
                meaningful_contradictions ASC,
                detailed_support DESC,
                core_fit DESC,
                stable_duration_microseconds DESC
        ) AS rank_start,
        COUNT(*) OVER (
            PARTITION BY
                net_information,
                meaningful_contradictions,
                detailed_support,
                core_fit,
                stable_duration_microseconds
        ) AS tie_count
    FROM score_records
)
SELECT payload, rank_start, tie_count
FROM ranked
ORDER BY
    net_information DESC,
    meaningful_contradictions ASC,
    detailed_support DESC,
    core_fit DESC,
    stable_duration_microseconds DESC,
    utc_start_microseconds ASC,
    state_id ASC
"""


def run_verified_v4_3_cache(
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    cache_build_plan_path: str | Path,
    cache_plan_trust_lock_path: str | Path,
    expected_cache_plan_trust_lock_sha256: str,
    cache_plan_repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    prevalence_plan_path: str | Path,
    prevalence_artifact_path: str | Path,
    response_artifact_path: str | Path,
    output_directory: str | Path,
    detail_limit: int = 100,
) -> VerifiedV43Run:
    """Run one complete cache-only universe score after exact input preflight."""

    if detail_limit <= 0 or detail_limit > MAX_DETAIL_ROWS:
        raise V43RunError(
            f"bounded detail limit must be between 1 and {MAX_DETAIL_ROWS}"
        )
    runtime_source = _require_clean_runtime_source(Path(repository_root))
    library, responses, prevalence, session, plan_trust = _preflight(
        repository_root=repository_root,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        cache_build_plan_path=cache_build_plan_path,
        cache_plan_trust_lock_path=cache_plan_trust_lock_path,
        expected_cache_plan_trust_lock_sha256=(
            expected_cache_plan_trust_lock_sha256
        ),
        cache_plan_repository_root=cache_plan_repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        prevalence_plan_path=prevalence_plan_path,
        prevalence_artifact_path=prevalence_artifact_path,
        response_artifact_path=response_artifact_path,
    )
    bindings = _run_bindings(session.bindings, responses, prevalence, plan_trust)
    destination = Path(output_directory)
    if _path_is_present(destination):
        return _finalize_existing_v4_3_run(
            destination,
            repository_root=repository_root,
            cache_directory=cache_directory,
            trust_lock_path=trust_lock_path,
            cache_build_plan_path=cache_build_plan_path,
            cache_plan_trust_lock_path=cache_plan_trust_lock_path,
            expected_cache_plan_trust_lock_sha256=(
                expected_cache_plan_trust_lock_sha256
            ),
            cache_plan_repository_root=cache_plan_repository_root,
            mapping_library_path=mapping_library_path,
            mapping_source_library_path=mapping_source_library_path,
            prevalence_plan_path=prevalence_plan_path,
            prevalence_artifact_path=prevalence_artifact_path,
            response_artifact_path=response_artifact_path,
        )
    declared_count = prevalence.artifact.source.interval_count
    unresolved_ids = tuple(
        sorted(item.rule_id for item in library.unresolved_mappings)
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-",
            dir=destination.parent,
        )
    )
    store: V43ExternalRankStore | None = None
    journal: V43PartialScoreJournal | None = None
    journal_directory: Path | None = None
    current: V43MinimalScoreRecordV1 | None = None
    unresolved_count: int | None = None
    stage = V43FailureStage.PARTIAL_SCORE_JOURNAL
    renamed = False
    try:
        journal_directory = Path(
            tempfile.mkdtemp(
                prefix=f".{destination.name}.journal-",
                dir=destination.parent,
            )
        )
        journal = V43PartialScoreJournal(
            journal_directory / ".partial-scores.jsonl"
        )
        stage = V43FailureStage.SCORE_STORE_OPEN
        store = V43ExternalRankStore(staging / ".rank.sqlite3")
        for ordinal, evaluation in enumerate(
            session.stream_verified_universe(responses.artifact.observed_responses())
        ):
            current = _minimal_score_record(ordinal, evaluation)
            if unresolved_count is None:
                unresolved_count = current.unresolved_observation_count
            elif unresolved_count != current.unresolved_observation_count:
                raise V43RunError(
                    "unresolved-observation count changed across one response set"
                )
            stage = V43FailureStage.PARTIAL_SCORE_JOURNAL
            journal.append(current)
            stage = V43FailureStage.SCORE_STORE_APPEND
            store.append(current)
        stage = V43FailureStage.SCORE_STORE_FINALIZE
        store.finish()
        if store.count != declared_count:
            raise V43RunError("score store count differs from declared cache universe")
        if store.persisted_count != store.count:
            raise V43RunError("score store did not commit the complete universe")
        if store.score_records_sha256 != journal.sha256:
            raise V43RunError("score store differs from the evaluated-score journal")
        stage = V43FailureStage.RANKED_ARTIFACT
        ranked_summary = _write_and_verify_ranked_artifact(
            staging / RANKED_FILENAME,
            store,
            detail_limit=detail_limit,
        )
        stage = V43FailureStage.BOUNDED_DETAIL
        detail_payload = {
            "schema_version": "v4-3-bounded-run-detail-v1",
            "detail_limit": detail_limit,
            "detail_truncated": ranked_summary.detail_truncated,
            "top_records": [
                item.model_dump(mode="json")
                for item in ranked_summary.bounded_top_records
            ],
            "tie_groups": list(ranked_summary.bounded_tie_groups),
            "all_ties_are_preserved_in": RANKED_FILENAME,
            "unresolved_mapping_ids": list(unresolved_ids),
        }
        detail_path = write_new_canonical_json(staging / DETAIL_FILENAME, detail_payload)
        detail_artifact = V43RunArtifactV1(
            filename=DETAIL_FILENAME,
            sha256=sha256_file(detail_path),
            byte_count=detail_path.stat().st_size,
            row_count=len(ranked_summary.bounded_top_records),
            logical_sha256=sha256_json(detail_payload),
            logical_hash_strategy="sha256-canonical-json-v1",
            storage_format="canonical-json-v1",
        )
        stage = V43FailureStage.COMPLIANCE
        complete = session.require_streamed_universe_compliance()
        if complete.response_set_sha256 != responses.artifact.response_set_sha256:
            raise V43RunError("streamed response-set identity mismatch")
        compliance = _compliance_model(complete.compliance)
        score_records_sha256 = store.score_records_sha256
        scored_count = store.count
        persisted_count = store.persisted_count
        store.close()
        (staging / ".rank.sqlite3").unlink(missing_ok=True)
        manifest = V43RunManifestV1(
            runner_source_sha256=sha256_file(__file__),
            runtime_source_provenance=runtime_source,
            run_status="complete",
            bindings=bindings,
            declared_interval_count=declared_count,
            successfully_scored_count=scored_count,
            successfully_evaluated_count=scored_count,
            persisted_scored_count=persisted_count,
            score_records_sha256=score_records_sha256,
            ranked_artifact=ranked_summary.artifact,
            bounded_detail_artifact=detail_artifact,
            substantive_tie_group_count=(
                ranked_summary.substantive_tie_group_count
            ),
            tied_candidate_count=ranked_summary.tied_candidate_count,
            unresolved_observation_count_per_candidate=(
                unresolved_count if unresolved_count is not None else 0
            ),
            unresolved_mapping_ids=unresolved_ids,
            compliance=compliance,
        )
        stage = V43FailureStage.MANIFEST
        write_new_canonical_json(staging / MANIFEST_FILENAME, manifest)
        _fsync_directory(staging)
        stage = V43FailureStage.STAGED_VERIFICATION
        verify_v4_3_run(
            staging,
            repository_root=repository_root,
            cache_directory=cache_directory,
            trust_lock_path=trust_lock_path,
            cache_build_plan_path=cache_build_plan_path,
            cache_plan_trust_lock_path=cache_plan_trust_lock_path,
            expected_cache_plan_trust_lock_sha256=(
                expected_cache_plan_trust_lock_sha256
            ),
            cache_plan_repository_root=cache_plan_repository_root,
            mapping_library_path=mapping_library_path,
            mapping_source_library_path=mapping_source_library_path,
            prevalence_plan_path=prevalence_plan_path,
            prevalence_artifact_path=prevalence_artifact_path,
            response_artifact_path=response_artifact_path,
        )
        try:
            _atomic_publish_directory_noreplace(staging, destination)
        except FileExistsError as exc:
            raise V43RunPublicationConflictError(destination) from exc
        renamed = True
        try:
            _fsync_directory(destination.parent)
        except OSError as exc:
            raise V43RunPublicationPendingError(destination, exc) from exc
        journal.discard()
        with suppress(OSError):
            if journal_directory is not None:
                journal_directory.rmdir()
        return _verified_run(destination, manifest)
    except (V43RunPublicationPendingError, V43RunPublicationConflictError):
        raise
    except Exception as exc:
        if renamed:
            raise V43RunError(
                "published V4.3 destination must be finalized, not replaced"
            ) from exc
        actual_stage = (
            V43FailureStage.EVALUATION
            if isinstance(exc, V43UniverseStreamError)
            else V43FailureStage.SCORE_STORE_COMMIT
            if isinstance(exc, V43ScoreStoreCommitError)
            else stage
        )
        failure, producer_diagnostics = _failure_from_exception(
            stage=actual_stage,
            exception=exc,
            current=current,
            journal=journal,
            store=store,
        )
        with suppress(sqlite3.Error):
            if store is not None:
                store.close()
        try:
            published_failure, publication_error = _publish_failure_package(
                destination=destination,
                previous_staging=staging,
                journal=journal,
                journal_directory=journal_directory,
                failure=failure,
                producer_diagnostics=producer_diagnostics,
                runtime_source=runtime_source,
                bindings=bindings,
                declared_count=declared_count,
                unresolved_mapping_ids=unresolved_ids,
            )
        except _V43FailurePackagePublicationError as publish_exc:
            raise V43RunFailedError(
                publish_exc.staging_directory,
                failure,
                publication_error=publish_exc.cause,
            ) from exc
        raise V43RunFailedError(
            published_failure,
            failure,
            publication_error=publication_error,
        ) from exc


def verify_v4_3_run(
    run_directory: str | Path,
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    cache_build_plan_path: str | Path,
    cache_plan_trust_lock_path: str | Path,
    expected_cache_plan_trust_lock_sha256: str,
    cache_plan_repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    prevalence_plan_path: str | Path,
    prevalence_artifact_path: str | Path,
    response_artifact_path: str | Path,
) -> VerifiedV43Run:
    """Re-hash ranks, ties, order, and bindings without invoking astronomy."""

    directory = Path(run_directory)
    if directory.is_symlink() or not directory.is_dir():
        raise V43RunError("V4.3 run must be an existing regular directory")
    manifest = _load_manifest(directory / MANIFEST_FILENAME)
    runtime_source = _require_clean_runtime_source(Path(repository_root))
    library, responses, prevalence, session, plan_trust = _preflight(
        repository_root=repository_root,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        cache_build_plan_path=cache_build_plan_path,
        cache_plan_trust_lock_path=cache_plan_trust_lock_path,
        expected_cache_plan_trust_lock_sha256=(
            expected_cache_plan_trust_lock_sha256
        ),
        cache_plan_repository_root=cache_plan_repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        prevalence_plan_path=prevalence_plan_path,
        prevalence_artifact_path=prevalence_artifact_path,
        response_artifact_path=response_artifact_path,
    )
    _verify_v4_3_run_preverified(
        directory,
        manifest=manifest,
        library=library,
        responses=responses,
        prevalence=prevalence,
        session=session,
        plan_trust=plan_trust,
        runtime_source=runtime_source,
    )
    return _verified_run(directory, manifest)


def finalize_v4_3_run_publication(
    run_directory: str | Path,
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    cache_build_plan_path: str | Path,
    cache_plan_trust_lock_path: str | Path,
    expected_cache_plan_trust_lock_sha256: str,
    cache_plan_repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    prevalence_plan_path: str | Path,
    prevalence_artifact_path: str | Path,
    response_artifact_path: str | Path,
) -> VerifiedV43Run:
    """Verify a visible run and retry only its parent-directory durability barrier."""

    verified = verify_v4_3_run(
        run_directory,
        repository_root=repository_root,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        cache_build_plan_path=cache_build_plan_path,
        cache_plan_trust_lock_path=cache_plan_trust_lock_path,
        expected_cache_plan_trust_lock_sha256=(
            expected_cache_plan_trust_lock_sha256
        ),
        cache_plan_repository_root=cache_plan_repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        prevalence_plan_path=prevalence_plan_path,
        prevalence_artifact_path=prevalence_artifact_path,
        response_artifact_path=response_artifact_path,
    )
    try:
        _fsync_directory(verified.run_directory.parent)
    except OSError as exc:
        raise V43RunPublicationPendingError(verified.run_directory, exc) from exc
    return verified


def publish_verified_v4_3_run_staging(
    staging_directory: str | Path,
    output_directory: str | Path,
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    cache_build_plan_path: str | Path,
    cache_plan_trust_lock_path: str | Path,
    expected_cache_plan_trust_lock_sha256: str,
    cache_plan_repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    prevalence_plan_path: str | Path,
    prevalence_artifact_path: str | Path,
    response_artifact_path: str | Path,
) -> VerifiedV43Run:
    """Verify and atomically publish a preserved complete staging package."""

    staging = Path(staging_directory)
    destination = Path(output_directory)
    if staging.parent.resolve() != destination.parent.resolve():
        raise V43RunError("V4.3 staging recovery requires sibling directories")
    verified = verify_v4_3_run(
        staging,
        repository_root=repository_root,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        cache_build_plan_path=cache_build_plan_path,
        cache_plan_trust_lock_path=cache_plan_trust_lock_path,
        expected_cache_plan_trust_lock_sha256=(
            expected_cache_plan_trust_lock_sha256
        ),
        cache_plan_repository_root=cache_plan_repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        prevalence_plan_path=prevalence_plan_path,
        prevalence_artifact_path=prevalence_artifact_path,
        response_artifact_path=response_artifact_path,
    )
    try:
        _atomic_publish_directory_noreplace(staging, destination)
    except FileExistsError as exc:
        raise V43RunPublicationConflictError(
            destination,
            preserved_staging_directory=staging,
        ) from exc
    try:
        _fsync_directory(destination.parent)
    except OSError as exc:
        raise V43RunPublicationPendingError(destination, exc) from exc
    return _verified_run(destination, verified.manifest)


def _finalize_existing_v4_3_run(
    run_directory: Path,
    **inputs: Any,
) -> VerifiedV43Run:
    verified = finalize_v4_3_run_publication(run_directory, **inputs)
    if verified.manifest.run_status == "failed":
        failure = _load_failure(verified.run_directory / FAILURE_FILENAME)
        raise V43RunFailedError(verified.run_directory, failure)
    return verified


def _preflight(
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    cache_build_plan_path: str | Path,
    cache_plan_trust_lock_path: str | Path,
    expected_cache_plan_trust_lock_sha256: str,
    cache_plan_repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    prevalence_plan_path: str | Path,
    prevalence_artifact_path: str | Path,
    response_artifact_path: str | Path,
) -> tuple[
    MappingLibraryV2,
    VerifiedV43DirectTargetResponses,
    VerifiedV43ConditionalPrevalence,
    CanonicalV43ScoringSession,
    VerifiedCenturyBuildPlanTrust,
]:
    library = _load_verified_mapping(
        repository_root=repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
    )
    responses = verify_v4_3_direct_target_responses(
        response_artifact_path,
        repository_root=repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
    )
    prevalence = verify_v4_3_prevalence_artifact(
        prevalence_artifact_path,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        mapping_repository_root=repository_root,
        prevalence_plan_path=prevalence_plan_path,
    )
    plan_trust = verify_century_build_plan_against_trust_lock(
        cache_build_plan_path,
        trust_lock_path=cache_plan_trust_lock_path,
        expected_trust_lock_sha256=expected_cache_plan_trust_lock_sha256,
        repository_root=cache_plan_repository_root,
    )
    _require_cache_plan_binding(prevalence, plan_trust)
    session = CanonicalV43ScoringSession.open(
        mapping_library=library,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        prevalence=prevalence,
    )
    expected = _run_bindings(
        session.bindings,
        responses,
        prevalence,
        plan_trust,
    )
    if responses.artifact.mapping_library_sha256 != expected.mapping_library_sha256:
        raise V43RunError("response/mapping library identity mismatch")
    if responses.artifact.mapping_source_library_sha256 != (
        expected.mapping_source_library_sha256
    ):
        raise V43RunError("response/mapping source-library identity mismatch")
    return library, responses, prevalence, session, plan_trust


def _load_verified_mapping(
    *,
    repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
) -> MappingLibraryV2:
    root = Path(repository_root).resolve()
    compiled_path = Path(mapping_library_path).resolve()
    source_path = Path(mapping_source_library_path).resolve()
    for path in (compiled_path, source_path):
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise V43RunError(f"mapping artifact escapes repository root: {path}") from exc
    try:
        compiled_raw = compiled_path.read_bytes()
        source_raw = source_path.read_bytes()
        if canonical_json_bytes(json.loads(compiled_raw)) != compiled_raw:
            raise V43RunError("compiled mapping library is not canonical")
        if canonical_json_bytes(json.loads(source_raw)) != source_raw:
            raise V43RunError("mapping source library is not canonical")
        compiled = MappingLibraryV2.model_validate_json(compiled_raw, strict=True)
        source = MappingLibrarySourceV2.model_validate_json(source_raw, strict=True)
        replayed = compile_verified_mapping_library_v2(source, repository_root=root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43RunError):
            raise
        raise V43RunError("mapping library verification failed") from exc
    if compiled != replayed:
        raise V43RunError("compiled mapping differs from exact source replay")
    return compiled


def _run_bindings(
    bindings: CanonicalV43Bindings,
    responses: VerifiedV43DirectTargetResponses,
    prevalence: VerifiedV43ConditionalPrevalence,
    plan_trust: VerifiedCenturyBuildPlanTrust,
) -> V43RunBindingsV1:
    artifact = responses.artifact
    expected = {
        "response source mode": (
            bindings.response_source_mode.value,
            artifact.response_source_mode,
        ),
        "response source ID": (
            bindings.response_source_id,
            artifact.behavioral_target_source_id,
        ),
        "response source hash": (
            bindings.response_source_sha256,
            artifact.behavioral_target_sha256,
        ),
        "behavioral target hash": (
            bindings.behavioral_target_sha256,
            artifact.behavioral_target_sha256,
        ),
        "question bank hash": (
            bindings.question_bank_sha256,
            artifact.question_bank_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43RunError(f"{label} differs between response and score artifacts")
    return V43RunBindingsV1(
        mapping_library_sha256=bindings.mapping_library_sha256,
        mapping_source_library_sha256=bindings.mapping_source_library_sha256,
        required_feature_registry_sha256=(
            bindings.required_feature_registry_sha256
        ),
        mapping_prevalence_plan_sha256=(
            bindings.mapping_prevalence_plan_sha256
        ),
        response_source_mode="direct_behavioral_target",
        response_source_id=bindings.response_source_id,
        response_source_sha256=bindings.response_source_sha256,
        behavioral_target_sha256=bindings.behavioral_target_sha256,
        direct_target_response_artifact_sha256=responses.artifact_sha256,
        response_set_sha256=artifact.response_set_sha256,
        prevalence_artifact_sha256=bindings.prevalence_artifact_sha256,
        prevalence_plan_sha256=bindings.prevalence_plan_sha256,
        prevalence_parent_hierarchy_sha256=(
            bindings.prevalence_parent_hierarchy_sha256
        ),
        cache_manifest_sha256=bindings.cache_manifest_sha256,
        cache_trust_lock_sha256=bindings.cache_trust_lock_sha256,
        cache_build_plan_sha256=plan_trust.plan_sha256,
        cache_plan_trust_lock_sha256=plan_trust.trust_lock_sha256,
        cache_generation_commit=plan_trust.plan.source_commit,
        cache_engine_identity_sha256=(
            prevalence.artifact.source.engine_identity_sha256
        ),
        cache_plan_engine_identity_sha256=(
            plan_trust.trust_lock.engine_identity_sha256
        ),
        logical_universe_sha256=bindings.logical_universe_sha256,
    )


def _require_cache_plan_binding(
    prevalence: VerifiedV43ConditionalPrevalence,
    plan_trust: VerifiedCenturyBuildPlanTrust,
) -> None:
    source = prevalence.artifact.source
    plan = plan_trust.plan
    expected = {
        "build-plan SHA-256": (
            source.cache_build_plan_sha256,
            plan_trust.plan_sha256,
        ),
        "generation commit": (source.generation_commit, plan.source_commit),
        "engine validation": (
            source.engine_validation_sha256,
            plan.engine_validation_sha256,
        ),
        "ephemeris file set": (
            source.ephemeris_file_set_sha256,
            plan.engine.canonical_ephemeris_file_set_sha256,
        ),
        "boundary policy": (
            source.boundary_policy_version,
            plan.boundary_policy_version,
        ),
        "semantic feature registry": (
            source.semantic_feature_registry_sha256,
            plan.semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            source.feature_registry_sha256,
            plan.physical_feature_registry_sha256,
        ),
        "UTC start": (source.utc_start, _utc_identity_text(plan.utc_start)),
        "UTC end": (
            source.utc_end_exclusive,
            _utc_identity_text(plan.utc_end_exclusive),
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43RunError(
                f"verified cache {label} differs from the reviewed build plan"
            )


def _minimal_score_record(
    ordinal: int,
    evaluation: CanonicalV43CandidateEvaluation,
) -> V43MinimalScoreRecordV1:
    interval = evaluation.ranked_interval
    score = evaluation.score
    duration = interval.stable_duration_microseconds
    return V43MinimalScoreRecordV1(
        input_ordinal=ordinal,
        state_id=evaluation.state_id,
        candidate_record_sha256=evaluation.candidate_record_sha256,
        utc_start=interval.utc_start.astimezone(UTC),
        utc_end_exclusive=(
            interval.utc_start + timedelta(microseconds=duration)
        ).astimezone(UTC),
        stable_duration_microseconds=duration,
        evidence_rubric_bits=score.evidence_rubric_bits,
        contradiction_rubric_bits=score.contradiction_rubric_bits,
        net_information=score.net_information,
        meaningful_contradictions=score.meaningful_contradictions,
        detailed_support=score.detailed_support,
        core_fit=score.core_fit,
        unresolved_observation_count=sum(
            not item.confidence.disposition.is_scorable
            for item in evaluation.scoring_input.observations
        ),
    )


def _write_and_verify_ranked_artifact(
    path: Path,
    store: V43ExternalRankStore,
    *,
    detail_limit: int,
) -> _RankedWriteSummary:
    pa, pq = _pyarrow_modules()
    schema = _ranked_arrow_schema(pa)
    writer = pq.ParquetWriter(
        path,
        schema,
        compression="zstd",
        version="2.6",
        data_page_version="2.0",
        use_dictionary=False,
        write_statistics=True,
    )
    batch: list[dict[str, object]] = []
    top: list[V43RankedScoreRecordV1] = []
    tie_details: list[dict[str, object]] = []
    tie_group_count = 0
    tied_candidate_count = 0
    last_tie_rank_start: int | None = None
    try:
        for ranked in store.iter_ranked():
            batch.append(_ranked_physical_row(ranked))
            if len(top) < detail_limit:
                top.append(ranked)
            if ranked.substantively_tied:
                tied_candidate_count += 1
                if ranked.rank_start != last_tie_rank_start:
                    last_tie_rank_start = ranked.rank_start
                    tie_group_count += 1
                    if len(tie_details) < detail_limit:
                        tie_details.append(
                            {
                                "rank_start": ranked.rank_start,
                                "rank_end": ranked.rank_end,
                                "substantive_rank_key": list(
                                    ranked.score.substantive_rank_key
                                ),
                            }
                        )
            if len(batch) == PARQUET_BATCH_ROWS:
                writer.write_table(pa.Table.from_pylist(batch, schema=schema))
                batch.clear()
        if batch:
            writer.write_table(pa.Table.from_pylist(batch, schema=schema))
    finally:
        writer.close()
    with path.open("rb") as handle:
        os.fsync(handle.fileno())
    ranked_digest = hashlib.sha256()
    row_count = 0
    expected = store.iter_ranked()
    observed = _iter_ranked_parquet(path)
    sentinel = object()
    for expected_row, observed_row in zip_longest(
        expected,
        observed,
        fillvalue=sentinel,
    ):
        if expected_row is sentinel or observed_row is sentinel:
            raise V43RunError("ranked Parquet row count differs from external sort")
        if expected_row != observed_row:
            raise V43RunError("ranked Parquet changed an exact rank or score record")
        assert isinstance(observed_row, V43RankedScoreRecordV1)
        ranked_digest.update(canonical_json_bytes(observed_row))
        ranked_digest.update(b"\n")
        row_count += 1
    artifact = V43RunArtifactV1(
        filename=path.name,
        sha256=sha256_file(path),
        byte_count=path.stat().st_size,
        row_count=row_count,
        logical_sha256=ranked_digest.hexdigest(),
        logical_hash_strategy=RANKED_HASH_STRATEGY,
        storage_format="parquet-internal-zstd-v1",
    )
    return _RankedWriteSummary(
        artifact=artifact,
        substantive_tie_group_count=tie_group_count,
        tied_candidate_count=tied_candidate_count,
        bounded_top_records=tuple(top),
        bounded_tie_groups=tuple(tie_details),
        detail_truncated=(row_count > detail_limit or tie_group_count > detail_limit),
    )


def _verify_v4_3_run_preverified(
    directory: Path,
    *,
    manifest: V43RunManifestV1,
    library: MappingLibraryV2,
    responses: VerifiedV43DirectTargetResponses,
    prevalence: VerifiedV43ConditionalPrevalence,
    session: CanonicalV43ScoringSession,
    plan_trust: VerifiedCenturyBuildPlanTrust,
    runtime_source: V43RuntimeSourceProvenanceV1,
) -> None:
    manifest_path = directory / MANIFEST_FILENAME
    _require_exact_run_inventory(directory, manifest)
    if sha256_file(__file__) != manifest.runner_source_sha256:
        raise V43RunError("run was produced by different runner source bytes")
    if manifest.runtime_source_provenance != runtime_source:
        raise V43RunError(
            "run source commit/tree/code/runtime differs from the clean current tree"
        )
    if (
        _run_bindings(session.bindings, responses, prevalence, plan_trust)
        != manifest.bindings
    ):
        raise V43RunError("run input bindings differ from verified artifacts")
    if manifest.declared_interval_count != prevalence.artifact.source.interval_count:
        raise V43RunError("run declared count differs from prevalence/cache universe")
    expected_unresolved = tuple(
        sorted(item.rule_id for item in library.unresolved_mappings)
    )
    if manifest.unresolved_mapping_ids != expected_unresolved:
        raise V43RunError("run unresolved mapping inventory changed")
    if manifest.run_status == "failed":
        assert manifest.failure_artifact is not None
        assert manifest.producer_failure_diagnostics_artifact is not None
        assert manifest.partial_score_artifact is not None
        _require_artifact_contract(
            manifest.failure_artifact,
            filename=FAILURE_FILENAME,
            logical_hash_strategy="sha256-canonical-json-v1",
            storage_format="canonical-json-v1",
        )
        _verify_artifact_file(directory, manifest.failure_artifact)
        _require_artifact_contract(
            manifest.producer_failure_diagnostics_artifact,
            filename=PRODUCER_FAILURE_DIAGNOSTICS_FILENAME,
            logical_hash_strategy="sha256-canonical-json-v1",
            storage_format="canonical-json-v1",
        )
        _verify_artifact_file(
            directory,
            manifest.producer_failure_diagnostics_artifact,
        )
        _require_artifact_contract(
            manifest.partial_score_artifact,
            filename=PARTIAL_SCORES_FILENAME,
            logical_hash_strategy=SCORE_HASH_STRATEGY,
            storage_format="canonical-json-lines-v1",
        )
        _verify_artifact_file(directory, manifest.partial_score_artifact)
        if manifest.failure_artifact.row_count != 1:
            raise V43RunError("failure artifact row count must equal one")
        if manifest.producer_failure_diagnostics_artifact.row_count != 1:
            raise V43RunError(
                "producer failure-diagnostics row count must equal one"
            )
        failure_path = directory / manifest.failure_artifact.filename
        failure = _load_failure(failure_path)
        failure_bytes = canonical_json_bytes(failure)
        producer_diagnostics_path = (
            directory / manifest.producer_failure_diagnostics_artifact.filename
        )
        producer_diagnostics = _load_producer_failure_diagnostics(
            producer_diagnostics_path
        )
        producer_diagnostics_bytes = canonical_json_bytes(producer_diagnostics)
        if failure.producer_diagnostics_sha256 != sha256_json(
            producer_diagnostics
        ):
            raise V43RunError(
                "producer failure-diagnostics hash differs from failure"
            )
        _verify_producer_failure_diagnostics_internal_consistency(
            failure,
            producer_diagnostics,
        )
        if (
            failure.persisted_scored_count != manifest.persisted_scored_count
            or failure.successfully_evaluated_count
            != manifest.successfully_evaluated_count
            or manifest.successfully_scored_count != manifest.persisted_scored_count
        ):
            raise V43RunError("failure score accounting differs from manifest")
        if failure.partial_score_records_sha256 != manifest.score_records_sha256:
            raise V43RunError("failure partial score hash differs from manifest")
        recomputed_partial = _partial_score_artifact(
            directory / PARTIAL_SCORES_FILENAME
        )
        if recomputed_partial != manifest.partial_score_artifact:
            raise V43RunError("failure partial-score artifact metadata changed")
        _verify_failure_partial_scores(
            failure,
            partial_path=directory / PARTIAL_SCORES_FILENAME,
            partial_artifact=recomputed_partial,
            manifest_unresolved_count=(
                manifest.unresolved_observation_count_per_candidate
            ),
            declared_count=manifest.declared_interval_count,
            responses=responses,
            session=session,
        )
        _verify_artifact_file(directory, manifest.failure_artifact)
        _verify_artifact_file(
            directory,
            manifest.producer_failure_diagnostics_artifact,
        )
        _verify_artifact_file(directory, manifest.partial_score_artifact)
        if failure_path.read_bytes() != failure_bytes:
            raise V43RunError("failure artifact bytes changed during verification")
        if (
            producer_diagnostics_path.read_bytes()
            != producer_diagnostics_bytes
        ):
            raise V43RunError(
                "producer failure-diagnostics bytes changed during verification"
            )
        _require_exact_run_inventory(directory, manifest)
        if manifest_path.read_bytes() != canonical_json_bytes(manifest):
            raise V43RunError("run manifest bytes changed after canonical load")
        return
    assert manifest.ranked_artifact is not None
    assert manifest.bounded_detail_artifact is not None
    _require_artifact_contract(
        manifest.ranked_artifact,
        filename=RANKED_FILENAME,
        logical_hash_strategy=RANKED_HASH_STRATEGY,
        storage_format="parquet-internal-zstd-v1",
    )
    _require_artifact_contract(
        manifest.bounded_detail_artifact,
        filename=DETAIL_FILENAME,
        logical_hash_strategy="sha256-canonical-json-v1",
        storage_format="canonical-json-v1",
    )
    _verify_artifact_file(directory, manifest.ranked_artifact)
    _verify_artifact_file(directory, manifest.bounded_detail_artifact)
    scratch_context = tempfile.TemporaryDirectory(prefix="hdmatch-v43-verify-")
    database_path = Path(scratch_context.name) / "rank.sqlite3"
    store = V43ExternalRankStore(database_path)
    try:
        for ranked in _iter_ranked_parquet(directory / RANKED_FILENAME):
            store.append_unordered_for_verification(ranked.score)
        store.finish_unordered_for_verification()
        if store.count != manifest.declared_interval_count:
            raise V43RunError("ranked artifact does not cover the declared universe")
        if manifest.ranked_artifact.row_count != store.count:
            raise V43RunError("ranked artifact row count differs from its rows")
        if store.score_records_sha256 != manifest.score_records_sha256:
            raise V43RunError("ranked artifact input-order score hash mismatch")
        expected_ranked = store.iter_ranked()
        observed_ranked = _iter_ranked_parquet(directory / RANKED_FILENAME)
        sentinel = object()
        tie_group_count = 0
        tied_candidate_count = 0
        last_tie_start: int | None = None
        ranked_digest = hashlib.sha256()
        for expected, observed in zip_longest(
            expected_ranked,
            observed_ranked,
            fillvalue=sentinel,
        ):
            if expected is sentinel or observed is sentinel or expected != observed:
                raise V43RunError("ranked artifact differs from exact external rerank")
            assert isinstance(observed, V43RankedScoreRecordV1)
            ranked_digest.update(canonical_json_bytes(observed))
            ranked_digest.update(b"\n")
            if observed.substantively_tied:
                tied_candidate_count += 1
                if observed.rank_start != last_tie_start:
                    tie_group_count += 1
                    last_tie_start = observed.rank_start
        if ranked_digest.hexdigest() != manifest.ranked_artifact.logical_sha256:
            raise V43RunError("ranked artifact logical hash mismatch")
        if tie_group_count != manifest.substantive_tie_group_count:
            raise V43RunError("run tie-group count mismatch")
        if tied_candidate_count != manifest.tied_candidate_count:
            raise V43RunError("run tied-candidate count mismatch")
        _verify_bounded_detail(
            directory / DETAIL_FILENAME,
            artifact=manifest.bounded_detail_artifact,
            store=store,
            ranked_row_count=manifest.declared_interval_count,
            tie_group_count=tie_group_count,
            unresolved_mapping_ids=manifest.unresolved_mapping_ids,
        )
        input_records = store.iter_input_order()
        rescored_count = 0
        rescored_unresolved_count: int | None = None
        for evaluation, score_record in zip_longest(
            session.stream_verified_universe(responses.artifact.observed_responses()),
            input_records,
            fillvalue=sentinel,
        ):
            if evaluation is sentinel or score_record is sentinel:
                raise V43RunError(
                    "ranked input order differs from verified cache scoring length"
                )
            assert isinstance(evaluation, CanonicalV43CandidateEvaluation)
            assert isinstance(score_record, V43MinimalScoreRecordV1)
            if _minimal_score_record(rescored_count, evaluation) != score_record:
                raise V43RunError(
                    "ranked score differs from cache-only canonical rescore"
                )
            if rescored_unresolved_count is None:
                rescored_unresolved_count = score_record.unresolved_observation_count
            elif (
                rescored_unresolved_count
                != score_record.unresolved_observation_count
            ):
                raise V43RunError(
                    "ranked rows contain inconsistent unresolved counts"
                )
            rescored_count += 1
        if rescored_count != manifest.declared_interval_count:
            raise V43RunError("cache-only rescore count mismatch")
        if (
            manifest.successfully_evaluated_count != rescored_count
            or manifest.persisted_scored_count != rescored_count
            or manifest.successfully_scored_count != rescored_count
        ):
            raise V43RunError("complete run score accounting mismatch")
        if (rescored_unresolved_count or 0) != (
            manifest.unresolved_observation_count_per_candidate
        ):
            raise V43RunError("complete run unresolved-observation count mismatch")
        complete = session.require_streamed_universe_compliance()
        if complete.response_set_sha256 != manifest.bindings.response_set_sha256:
            raise V43RunError("verified response-set identity mismatch")
    finally:
        store.close()
        scratch_context.cleanup()
    _verify_complete_compliance(manifest, library, complete.compliance)
    if manifest_path.read_bytes() != canonical_json_bytes(manifest):
        raise V43RunError("run manifest bytes changed after canonical load")


def _require_exact_run_inventory(
    directory: Path,
    manifest: V43RunManifestV1,
) -> None:
    expected = (
        {MANIFEST_FILENAME, RANKED_FILENAME, DETAIL_FILENAME}
        if manifest.run_status == "complete"
        else {
            MANIFEST_FILENAME,
            FAILURE_FILENAME,
            PRODUCER_FAILURE_DIAGNOSTICS_FILENAME,
            PARTIAL_SCORES_FILENAME,
        }
    )
    observed: set[str] = set()
    for path in directory.iterdir():
        if path.is_symlink() or not path.is_file():
            raise V43RunError(f"run contains a non-regular artifact: {path.name}")
        observed.add(path.name)
    if observed != expected:
        raise V43RunError("run artifact inventory differs from its status contract")


def _verify_complete_compliance(
    manifest: V43RunManifestV1,
    library: MappingLibraryV2,
    recomputed: V43Compliance,
) -> None:
    compliance = manifest.compliance
    if compliance is None:
        raise V43RunError("complete run lacks compliance evidence")
    required_count = len(library.required_feature_registry.feature_ids)
    if (
        compliance.required_feature_count != required_count
        or compliance.available_required_feature_count != required_count
        or not compliance.v4_3_compliant
    ):
        raise V43RunError("run compliance feature bindings are inconsistent")
    if compliance != _compliance_model(recomputed):
        raise V43RunError("stored compliance differs from cache-only recomputation")


def _failure_from_exception(
    *,
    stage: V43FailureStage,
    exception: Exception,
    current: V43MinimalScoreRecordV1 | None,
    journal: V43PartialScoreJournal | None,
    store: V43ExternalRankStore | None,
) -> tuple[V43RunFailureV1, V43ProducerFailureDiagnosticsV1]:
    evaluated_count = journal.count if journal is not None else 0
    persisted_count = store.persisted_count if store is not None else 0
    partial_sha256 = journal.sha256 if journal is not None else hashlib.sha256().hexdigest()
    attempted_ordinal: int | None = None
    attempted_state_id: str | None = None
    attempted_record_sha256: str | None = None
    attempted_is_partial = False
    diagnostic_type = type(exception).__name__
    diagnostic_message = str(exception) or diagnostic_type
    if isinstance(exception, V43UniverseStreamError):
        attempted_ordinal = exception.input_ordinal
        attempted_state_id = exception.state_id
        attempted_record_sha256 = exception.candidate_record_sha256
        diagnostic_type = exception.cause_type
        diagnostic_message = exception.cause_message or diagnostic_type
    elif current is not None and stage in {
        V43FailureStage.PARTIAL_SCORE_JOURNAL,
        V43FailureStage.SCORE_STORE_APPEND,
        V43FailureStage.SCORE_STORE_COMMIT,
    }:
        attempted_ordinal = current.input_ordinal
        attempted_state_id = current.state_id
        attempted_record_sha256 = current.candidate_record_sha256
        attempted_is_partial = current.input_ordinal < evaluated_count
    producer_diagnostics = V43ProducerFailureDiagnosticsV1(
        producer_reported_stage=stage,
        attempted_input_ordinal=attempted_ordinal,
        attempted_record_is_in_partial_scores=attempted_is_partial,
        successfully_evaluated_count=evaluated_count,
        producer_reported_sqlite_inserted_count=(
            store.count if store is not None else 0
        ),
        producer_reported_sqlite_persisted_count=persisted_count,
        partial_score_records_sha256=partial_sha256,
    )
    failure_code, message = _FAILURE_SEMANTICS[stage]
    failure = V43RunFailureV1(
        producer_reported_stage=stage,
        failure_code=failure_code,
        error_type=failure_code,
        error_message=message,
        producer_reported_cause_type=diagnostic_type,
        producer_reported_cause_message=diagnostic_message,
        attempted_input_ordinal=attempted_ordinal,
        attempted_state_id=attempted_state_id,
        attempted_candidate_record_sha256=attempted_record_sha256,
        attempted_record_is_in_partial_scores=attempted_is_partial,
        successfully_evaluated_count=evaluated_count,
        persisted_scored_count=persisted_count,
        partial_score_records_sha256=partial_sha256,
        producer_diagnostics_sha256=sha256_json(producer_diagnostics),
    )
    return failure, producer_diagnostics


def _verify_failure_partial_scores(
    failure: V43RunFailureV1,
    *,
    partial_path: Path,
    partial_artifact: V43RunArtifactV1,
    manifest_unresolved_count: int,
    declared_count: int,
    responses: VerifiedV43DirectTargetResponses,
    session: CanonicalV43ScoringSession,
) -> None:
    if failure.successfully_evaluated_count > declared_count:
        raise V43RunError("failure evaluated-score count exceeds declared universe")
    if failure.persisted_scored_count != _expected_failure_persisted_count(failure):
        raise V43RunError("failure persisted-score count is not transactionally possible")
    partial_records = _iter_partial_score_records(partial_path)
    stream = session.stream_verified_universe(responses.artifact.observed_responses())
    sentinel = object()
    observed_count = 0
    unresolved_count: int | None = None
    attempted_verified = failure.attempted_input_ordinal is None
    try:
        while observed_count < failure.successfully_evaluated_count:
            expected = next(stream, sentinel)
            observed = next(partial_records, sentinel)
            if expected is sentinel or observed is sentinel:
                raise V43RunError("partial-score artifact length cannot be replayed")
            assert isinstance(expected, CanonicalV43CandidateEvaluation)
            assert isinstance(observed, V43MinimalScoreRecordV1)
            if _minimal_score_record(observed_count, expected) != observed:
                raise V43RunError("partial score differs from cache-only rescore")
            if unresolved_count is None:
                unresolved_count = observed.unresolved_observation_count
            elif unresolved_count != observed.unresolved_observation_count:
                raise V43RunError("partial scores contain inconsistent unresolved counts")
            if observed.input_ordinal == failure.attempted_input_ordinal:
                if (
                    not failure.attempted_record_is_in_partial_scores
                    or observed.state_id != failure.attempted_state_id
                    or observed.candidate_record_sha256
                    != failure.attempted_candidate_record_sha256
                ):
                    raise V43RunError("failure attempted-row binding changed")
                attempted_verified = True
            observed_count += 1
        if next(partial_records, sentinel) is not sentinel:
            raise V43RunError("partial-score artifact has undeclared extra rows")
        if (
            failure.attempted_input_ordinal is not None
            and not failure.attempted_record_is_in_partial_scores
        ):
            if failure.producer_reported_stage is V43FailureStage.EVALUATION:
                try:
                    next(stream)
                except V43UniverseStreamError as replayed:
                    if (
                        replayed.input_ordinal != failure.attempted_input_ordinal
                        or replayed.state_id != failure.attempted_state_id
                        or replayed.candidate_record_sha256
                        != failure.attempted_candidate_record_sha256
                        or replayed.cause_type
                        != failure.producer_reported_cause_type
                        or replayed.cause_message
                        != failure.producer_reported_cause_message
                    ):
                        raise V43RunError(
                            "evaluation failure identity differs from cache-only replay"
                        ) from replayed
                else:
                    raise V43RunError(
                        "recorded evaluation failure did not recur during replay"
                    )
            else:
                expected = next(stream, sentinel)
                if expected is sentinel:
                    raise V43RunError("failure attempted row is absent from the cache")
                assert isinstance(expected, CanonicalV43CandidateEvaluation)
                if (
                    expected.state_id != failure.attempted_state_id
                    or expected.candidate_record_sha256
                    != failure.attempted_candidate_record_sha256
                ):
                    raise V43RunError("failure attempted row differs from cache replay")
            attempted_verified = True
        elif failure.attempted_input_ordinal is None and (
            failure.successfully_evaluated_count == declared_count
        ):
            if next(stream, sentinel) is not sentinel:
                raise V43RunError("failure declared full evaluation before cache end")
    finally:
        stream.close()
    if not attempted_verified:
        raise V43RunError("failure attempted row was not verified")
    if partial_artifact.row_count != observed_count:
        raise V43RunError("partial-score artifact row count mismatch")
    if failure.successfully_evaluated_count != observed_count:
        raise V43RunError("failure evaluated-score count mismatch")
    if failure.partial_score_records_sha256 != partial_artifact.logical_sha256:
        raise V43RunError("failure partial-score logical hash mismatch")
    if (unresolved_count or 0) != manifest_unresolved_count:
        raise V43RunError("failure unresolved-observation count mismatch")


def _expected_failure_persisted_count(failure: V43RunFailureV1) -> int:
    evaluated = failure.successfully_evaluated_count
    if failure.producer_reported_stage is V43FailureStage.SCORE_STORE_OPEN:
        return 0
    if failure.producer_reported_stage is V43FailureStage.EVALUATION:
        return (evaluated // PARQUET_BATCH_ROWS) * PARQUET_BATCH_ROWS
    if failure.producer_reported_stage is V43FailureStage.PARTIAL_SCORE_JOURNAL:
        if failure.attempted_record_is_in_partial_scores and evaluated:
            evaluated -= 1
        return (evaluated // PARQUET_BATCH_ROWS) * PARQUET_BATCH_ROWS
    if failure.producer_reported_stage in {
        V43FailureStage.SCORE_STORE_APPEND,
        V43FailureStage.SCORE_STORE_COMMIT,
    }:
        if evaluated == 0:
            return 0
        return ((evaluated - 1) // PARQUET_BATCH_ROWS) * PARQUET_BATCH_ROWS
    return evaluated


def _expected_failure_inserted_count(
    *,
    stage: V43FailureStage,
    evaluated_count: int,
    attempted_record_is_in_partial_scores: bool,
) -> int:
    if stage is V43FailureStage.SCORE_STORE_OPEN:
        return 0
    if stage is V43FailureStage.PARTIAL_SCORE_JOURNAL:
        return evaluated_count - int(attempted_record_is_in_partial_scores)
    if stage is V43FailureStage.SCORE_STORE_APPEND:
        return max(evaluated_count - 1, 0)
    return evaluated_count


def _verify_producer_failure_diagnostics_internal_consistency(
    failure: V43RunFailureV1,
    diagnostics: V43ProducerFailureDiagnosticsV1,
) -> None:
    expected = {
        "producer-reported stage": (
            diagnostics.producer_reported_stage,
            failure.producer_reported_stage,
        ),
        "attempted ordinal": (
            diagnostics.attempted_input_ordinal,
            failure.attempted_input_ordinal,
        ),
        "attempted partial status": (
            diagnostics.attempted_record_is_in_partial_scores,
            failure.attempted_record_is_in_partial_scores,
        ),
        "evaluated count": (
            diagnostics.successfully_evaluated_count,
            failure.successfully_evaluated_count,
        ),
        "persisted count": (
            diagnostics.producer_reported_sqlite_persisted_count,
            failure.persisted_scored_count,
        ),
        "partial-score hash": (
            diagnostics.partial_score_records_sha256,
            failure.partial_score_records_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43RunError(
                f"failure {label} differs between producer diagnostic records"
            )
    expected_inserted = _expected_failure_inserted_count(
        stage=failure.producer_reported_stage,
        evaluated_count=failure.successfully_evaluated_count,
        attempted_record_is_in_partial_scores=(
            failure.attempted_record_is_in_partial_scores
        ),
    )
    if diagnostics.producer_reported_sqlite_inserted_count != expected_inserted:
        raise V43RunError(
            "producer-reported stage is inconsistent with producer operation counters"
        )


def _iter_partial_score_records(path: Path) -> Iterator[V43MinimalScoreRecordV1]:
    try:
        with path.open("rb") as handle:
            for line in handle:
                if not line.endswith(b"\n"):
                    raise V43RunError("partial-score line lacks canonical terminator")
                payload = line[:-1]
                parsed = json.loads(payload)
                if canonical_json_bytes(parsed) != payload:
                    raise V43RunError("partial-score row is not canonical JSON")
                yield V43MinimalScoreRecordV1.model_validate_json(
                    payload,
                    strict=True,
                )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43RunError):
            raise
        raise V43RunError("partial-score artifact is invalid") from exc


def _publish_failure_package(
    *,
    destination: Path,
    previous_staging: Path,
    journal: V43PartialScoreJournal | None,
    journal_directory: Path | None,
    failure: V43RunFailureV1,
    producer_diagnostics: V43ProducerFailureDiagnosticsV1,
    runtime_source: V43RuntimeSourceProvenanceV1,
    bindings: V43RunBindingsV1,
    declared_count: int,
    unresolved_mapping_ids: tuple[str, ...],
) -> tuple[Path, Exception | None]:
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.failure-staging-",
            dir=destination.parent,
        )
    )
    try:
        return _complete_and_publish_failure_package(
            staging=staging,
            destination=destination,
            previous_staging=previous_staging,
            journal=journal,
            journal_directory=journal_directory,
            failure=failure,
            producer_diagnostics=producer_diagnostics,
            runtime_source=runtime_source,
            bindings=bindings,
            declared_count=declared_count,
            unresolved_mapping_ids=unresolved_mapping_ids,
        )
    except Exception as exc:
        preserved = destination if destination.is_dir() and not staging.is_dir() else staging
        raise _V43FailurePackagePublicationError(preserved, exc) from exc


def _complete_and_publish_failure_package(
    *,
    staging: Path,
    destination: Path,
    previous_staging: Path,
    journal: V43PartialScoreJournal | None,
    journal_directory: Path | None,
    failure: V43RunFailureV1,
    producer_diagnostics: V43ProducerFailureDiagnosticsV1,
    runtime_source: V43RuntimeSourceProvenanceV1,
    bindings: V43RunBindingsV1,
    declared_count: int,
    unresolved_mapping_ids: tuple[str, ...],
) -> tuple[Path, Exception | None]:
    partial_path = staging / PARTIAL_SCORES_FILENAME
    if journal is None:
        with partial_path.open("xb") as handle:
            handle.flush()
            os.fsync(handle.fileno())
    else:
        journal.move_finalized(partial_path)
    if journal_directory is not None:
        with suppress(OSError):
            journal_directory.rmdir()
    partial_artifact = _partial_score_artifact(partial_path)
    if partial_artifact.row_count != failure.successfully_evaluated_count:
        raise V43RunError("failure journal count changed during publication")
    if partial_artifact.logical_sha256 != failure.partial_score_records_sha256:
        raise V43RunError("failure journal hash changed during publication")
    producer_diagnostics_path = write_new_canonical_json(
        staging / PRODUCER_FAILURE_DIAGNOSTICS_FILENAME,
        producer_diagnostics,
    )
    producer_diagnostics_artifact = V43RunArtifactV1(
        filename=PRODUCER_FAILURE_DIAGNOSTICS_FILENAME,
        sha256=sha256_file(producer_diagnostics_path),
        byte_count=producer_diagnostics_path.stat().st_size,
        row_count=1,
        logical_sha256=sha256_json(producer_diagnostics),
        logical_hash_strategy="sha256-canonical-json-v1",
        storage_format="canonical-json-v1",
    )
    failure_path = write_new_canonical_json(staging / FAILURE_FILENAME, failure)
    failure_artifact = V43RunArtifactV1(
        filename=FAILURE_FILENAME,
        sha256=sha256_file(failure_path),
        byte_count=failure_path.stat().st_size,
        row_count=1,
        logical_sha256=sha256_json(failure),
        logical_hash_strategy="sha256-canonical-json-v1",
        storage_format="canonical-json-v1",
    )
    manifest = V43RunManifestV1(
        runner_source_sha256=sha256_file(__file__),
        runtime_source_provenance=runtime_source,
        run_status="failed",
        bindings=bindings,
        declared_interval_count=declared_count,
        successfully_scored_count=failure.persisted_scored_count,
        successfully_evaluated_count=failure.successfully_evaluated_count,
        persisted_scored_count=failure.persisted_scored_count,
        score_records_sha256=failure.partial_score_records_sha256,
        failure_artifact=failure_artifact,
        producer_failure_diagnostics_artifact=producer_diagnostics_artifact,
        failure_diagnostics_scope=(
            "producer-reported-internal-consistency-only"
        ),
        partial_score_artifact=partial_artifact,
        substantive_tie_group_count=0,
        tied_candidate_count=0,
        unresolved_observation_count_per_candidate=(
            _partial_unresolved_count(partial_path)
        ),
        unresolved_mapping_ids=unresolved_mapping_ids,
    )
    write_new_canonical_json(staging / MANIFEST_FILENAME, manifest)
    _verify_artifact_file(staging, failure_artifact)
    _verify_artifact_file(staging, producer_diagnostics_artifact)
    _verify_artifact_file(staging, partial_artifact)
    _fsync_directory(staging)
    _atomic_publish_directory_noreplace(staging, destination)
    if previous_staging.is_dir():
        with suppress(OSError):
            shutil.rmtree(previous_staging)
    try:
        _fsync_directory(destination.parent)
    except OSError as exc:
        return destination, exc
    return destination, None


def _partial_score_artifact(path: Path) -> V43RunArtifactV1:
    digest = hashlib.sha256()
    row_count = 0
    for record in _iter_partial_score_records(path):
        line = canonical_json_bytes(record) + b"\n"
        digest.update(line)
        row_count += 1
    return V43RunArtifactV1(
        filename=PARTIAL_SCORES_FILENAME,
        sha256=sha256_file(path),
        byte_count=path.stat().st_size,
        row_count=row_count,
        logical_sha256=digest.hexdigest(),
        logical_hash_strategy=SCORE_HASH_STRATEGY,
        storage_format="canonical-json-lines-v1",
    )


def _partial_unresolved_count(path: Path) -> int:
    value: int | None = None
    for record in _iter_partial_score_records(path):
        if value is None:
            value = record.unresolved_observation_count
        elif value != record.unresolved_observation_count:
            raise V43RunError("partial scores contain inconsistent unresolved counts")
    return value or 0


def _ranked_arrow_schema(pa: Any) -> Any:
    fields = [
        pa.field("input_ordinal", pa.int64(), nullable=False),
        pa.field("state_id", pa.string(), nullable=False),
        pa.field("candidate_record_sha256", pa.string(), nullable=False),
        pa.field("utc_start", pa.string(), nullable=False),
        pa.field("utc_end_exclusive", pa.string(), nullable=False),
        pa.field("stable_duration_microseconds", pa.int64(), nullable=False),
        pa.field("evidence_rubric_bits", pa.float64(), nullable=False),
        pa.field("contradiction_rubric_bits", pa.float64(), nullable=False),
        pa.field("net_information", pa.float64(), nullable=False),
        pa.field("meaningful_contradictions", pa.int64(), nullable=False),
        pa.field("detailed_support", pa.float64(), nullable=False),
        pa.field("core_fit", pa.float64(), nullable=False),
        pa.field("unresolved_observation_count", pa.int64(), nullable=False),
        pa.field("rank_start", pa.int64(), nullable=False),
        pa.field("rank_end", pa.int64(), nullable=False),
        pa.field("midrank_numerator", pa.int64(), nullable=False),
        pa.field("midrank_denominator", pa.int64(), nullable=False),
        pa.field("substantively_tied", pa.bool_(), nullable=False),
    ]
    return pa.schema(
        fields,
        metadata={
            b"hdmatch.schema": b"v4-3-ranked-score-record-v1",
            b"hdmatch.ranking_policy": V43_RANKING_POLICY_VERSION.encode(),
        },
    )


def _ranked_physical_row(record: V43RankedScoreRecordV1) -> dict[str, object]:
    score = record.score
    return {
        **score.model_dump(
            mode="json",
            exclude={"schema_version", "utc_start", "utc_end_exclusive"},
        ),
        "utc_start": _utc_text(score.utc_start),
        "utc_end_exclusive": _utc_text(score.utc_end_exclusive),
        "rank_start": record.rank_start,
        "rank_end": record.rank_end,
        "midrank_numerator": record.midrank_numerator,
        "midrank_denominator": record.midrank_denominator,
        "substantively_tied": record.substantively_tied,
    }


def _iter_ranked_parquet(path: Path) -> Iterator[V43RankedScoreRecordV1]:
    pa, pq = _pyarrow_modules()
    try:
        parquet_file = pq.ParquetFile(path)
    except (OSError, ValueError) as exc:
        raise V43RunError(f"cannot read ranked Parquet artifact: {path}") from exc
    expected_schema = _ranked_arrow_schema(pa)
    if not parquet_file.schema_arrow.equals(expected_schema, check_metadata=True):
        raise V43RunError("ranked Parquet schema mismatch")
    for group_index in range(parquet_file.metadata.num_row_groups):
        row_group = parquet_file.metadata.row_group(group_index)
        for column_index in range(row_group.num_columns):
            if row_group.column(column_index).compression != "ZSTD":
                raise V43RunError("ranked Parquet column is not Zstandard-compressed")
    try:
        for batch in parquet_file.iter_batches(batch_size=PARQUET_BATCH_ROWS):
            for row in batch.to_pylist():
                score = V43MinimalScoreRecordV1(
                    input_ordinal=row["input_ordinal"],
                    state_id=row["state_id"],
                    candidate_record_sha256=row["candidate_record_sha256"],
                    utc_start=_parse_utc_text(row["utc_start"]),
                    utc_end_exclusive=_parse_utc_text(row["utc_end_exclusive"]),
                    stable_duration_microseconds=row[
                        "stable_duration_microseconds"
                    ],
                    evidence_rubric_bits=row["evidence_rubric_bits"],
                    contradiction_rubric_bits=row["contradiction_rubric_bits"],
                    net_information=row["net_information"],
                    meaningful_contradictions=row["meaningful_contradictions"],
                    detailed_support=row["detailed_support"],
                    core_fit=row["core_fit"],
                    unresolved_observation_count=row[
                        "unresolved_observation_count"
                    ],
                )
                yield V43RankedScoreRecordV1(
                    score=score,
                    rank_start=row["rank_start"],
                    rank_end=row["rank_end"],
                    midrank_numerator=row["midrank_numerator"],
                    midrank_denominator=row["midrank_denominator"],
                    substantively_tied=row["substantively_tied"],
                )
    except (KeyError, TypeError, ValueError) as exc:
        raise V43RunError("ranked Parquet contains malformed rows") from exc


def _pyarrow_modules() -> tuple[Any, Any]:
    try:
        return import_module("pyarrow"), import_module("pyarrow.parquet")
    except ModuleNotFoundError as exc:
        raise V43RunError(
            "Phase-4 run storage requires the 'cache' optional dependency"
        ) from exc


def _require_artifact_contract(
    artifact: V43RunArtifactV1,
    *,
    filename: str,
    logical_hash_strategy: str,
    storage_format: str,
) -> None:
    if artifact.filename != filename:
        raise V43RunError(f"run artifact filename must be {filename}")
    if artifact.logical_hash_strategy != logical_hash_strategy:
        raise V43RunError(f"run artifact logical hash strategy changed: {filename}")
    if artifact.storage_format != storage_format:
        raise V43RunError(f"run artifact storage format changed: {filename}")


def _verify_bounded_detail(
    path: Path,
    *,
    artifact: V43RunArtifactV1,
    store: V43ExternalRankStore,
    ranked_row_count: int,
    tie_group_count: int,
    unresolved_mapping_ids: tuple[str, ...],
) -> None:
    try:
        raw = path.read_bytes()
        observed = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise V43RunError("bounded detail artifact is not valid JSON") from exc
    if canonical_json_bytes(observed) != raw:
        raise V43RunError("bounded detail artifact is not canonical JSON")
    if sha256_json(observed) != artifact.logical_sha256:
        raise V43RunError("bounded detail logical hash mismatch")
    if not isinstance(observed, dict):
        raise V43RunError("bounded detail artifact must be an object")
    detail_limit = observed.get("detail_limit")
    if (
        isinstance(detail_limit, bool)
        or not isinstance(detail_limit, int)
        or detail_limit <= 0
        or detail_limit > MAX_DETAIL_ROWS
    ):
        raise V43RunError("bounded detail limit is invalid")
    top: list[dict[str, object]] = []
    tie_details: list[dict[str, object]] = []
    last_tie_rank_start: int | None = None
    for ranked in store.iter_ranked():
        if len(top) < detail_limit:
            top.append(ranked.model_dump(mode="json"))
        if (
            ranked.substantively_tied
            and ranked.rank_start != last_tie_rank_start
        ):
            last_tie_rank_start = ranked.rank_start
            if len(tie_details) < detail_limit:
                tie_details.append(
                    {
                        "rank_start": ranked.rank_start,
                        "rank_end": ranked.rank_end,
                        "substantive_rank_key": list(
                            ranked.score.substantive_rank_key
                        ),
                    }
                )
    expected = {
        "schema_version": "v4-3-bounded-run-detail-v1",
        "detail_limit": detail_limit,
        "detail_truncated": (
            ranked_row_count > detail_limit or tie_group_count > detail_limit
        ),
        "top_records": top,
        "tie_groups": tie_details,
        "all_ties_are_preserved_in": RANKED_FILENAME,
        "unresolved_mapping_ids": list(unresolved_mapping_ids),
    }
    if observed != expected:
        raise V43RunError("bounded detail differs from exact ranked artifact")
    if artifact.row_count != len(top):
        raise V43RunError("bounded detail row count mismatch")


def _verify_artifact_file(directory: Path, artifact: V43RunArtifactV1) -> None:
    path = directory / artifact.filename
    if path.is_symlink() or not path.is_file():
        raise V43RunError(f"run artifact is missing: {artifact.filename}")
    if path.stat().st_size != artifact.byte_count:
        raise V43RunError(f"run artifact byte count mismatch: {artifact.filename}")
    if sha256_file(path) != artifact.sha256:
        raise V43RunError(f"run artifact hash mismatch: {artifact.filename}")


def _load_manifest(path: Path) -> V43RunManifestV1:
    try:
        if path.is_symlink() or not path.is_file():
            raise V43RunError("V4.3 run manifest must be a regular file")
        raw = path.read_bytes()
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw:
            raise V43RunError("V4.3 run manifest is not canonical JSON")
        return V43RunManifestV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43RunError):
            raise
        raise V43RunError(f"invalid V4.3 run manifest: {path}") from exc


def _load_failure(path: Path) -> V43RunFailureV1:
    try:
        if path.is_symlink() or not path.is_file():
            raise V43RunError("V4.3 failure artifact must be a regular file")
        raw = path.read_bytes()
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw:
            raise V43RunError("V4.3 failure artifact is not canonical JSON")
        return V43RunFailureV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43RunError):
            raise
        raise V43RunError(f"invalid V4.3 failure artifact: {path}") from exc


def _load_producer_failure_diagnostics(
    path: Path,
) -> V43ProducerFailureDiagnosticsV1:
    try:
        if path.is_symlink() or not path.is_file():
            raise V43RunError(
                "V4.3 producer failure-diagnostics artifact must be a regular file"
            )
        raw = path.read_bytes()
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw:
            raise V43RunError(
                "V4.3 producer failure-diagnostics artifact is not canonical JSON"
            )
        return V43ProducerFailureDiagnosticsV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43RunError):
            raise
        raise V43RunError(
            f"invalid V4.3 producer failure-diagnostics artifact: {path}"
        ) from exc


def _verified_run(directory: Path, manifest: V43RunManifestV1) -> VerifiedV43Run:
    manifest_path = directory / MANIFEST_FILENAME
    return VerifiedV43Run(
        run_directory=directory,
        manifest_path=manifest_path,
        manifest_sha256=sha256_file(manifest_path),
        manifest=manifest,
    )


def _compliance_model(value: V43Compliance) -> V43RunComplianceV1:
    return V43RunComplianceV1.model_validate(asdict(value), strict=True)


def _duration_microseconds(delta: timedelta) -> int:
    return (
        delta.days * 86_400_000_000
        + delta.seconds * 1_000_000
        + delta.microseconds
    )


def _utc_text(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _utc_identity_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _utc_epoch_microseconds(value: datetime) -> int:
    return _duration_microseconds(
        value.astimezone(UTC) - datetime(1970, 1, 1, tzinfo=UTC)
    )


def _parse_utc_text(value: object) -> datetime:
    if not isinstance(value, str):
        raise V43RunError("ranked timestamp is not a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() != timedelta(0):
        raise V43RunError("ranked timestamp is not UTC")
    return parsed.astimezone(UTC)


def _require_clean_runtime_source(
    repository_root: Path,
) -> V43RuntimeSourceProvenanceV1:
    """Bind claim-grade execution to one exact clean committed runtime tree."""

    root = repository_root.resolve()
    executing_root = Path(__file__).resolve().parents[3]
    if root != executing_root:
        raise V43RunError(
            "claim-grade repository root differs from the executing hdmatch source tree"
        )
    return _collect_clean_runtime_source(root)


def _collect_clean_runtime_source(
    root: Path,
) -> V43RuntimeSourceProvenanceV1:
    """Collect a clean tree; split out so isolated fixture repositories are testable."""

    try:
        commit = _git_stdout(root, "rev-parse", "HEAD").strip()
        tree_oid = _git_stdout(root, "rev-parse", "HEAD^{tree}").strip()
        dirty = _git_stdout(
            root,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        )
        tracked_raw = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                "--",
                "src/hdmatch",
                "pyproject.toml",
                "requirements-dev.lock",
            ],
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise V43RunError(
            "claim-grade V4.3 run cannot identify its committed source tree"
        ) from exc
    if dirty:
        raise V43RunError(
            "claim-grade V4.3 run requires a clean committed source tree"
        )
    try:
        tracked_paths = tuple(
            sorted(
                item.decode("utf-8")
                for item in tracked_raw.split(b"\0")
                if item
            )
        )
    except UnicodeDecodeError as exc:
        raise V43RunError("runtime source path is not valid UTF-8") from exc
    if not tracked_paths or "src/hdmatch/model/v4_3_run.py" not in tracked_paths:
        raise V43RunError("tracked runtime source inventory is incomplete")
    source_files: list[V43RuntimeSourceFileV1] = []
    for relative in tracked_paths:
        path = root / relative
        if path.is_symlink() or not path.is_file():
            raise V43RunError(f"tracked runtime source is not a regular file: {relative}")
        source_files.append(
            V43RuntimeSourceFileV1(path=relative, sha256=sha256_file(path))
        )
    versions: dict[str, str] = {}
    for distribution in _RUNTIME_DEPENDENCY_DISTRIBUTIONS:
        try:
            versions[distribution] = metadata.version(distribution)
        except metadata.PackageNotFoundError as exc:
            raise V43RunError(
                f"claim-grade runtime dependency is unavailable: {distribution}"
            ) from exc
    inventory = tuple(source_files)
    return V43RuntimeSourceProvenanceV1(
        source_commit=commit,
        source_tree_git_oid=tree_oid,
        source_files=inventory,
        source_code_fingerprint_sha256=sha256_json(
            [item.model_dump(mode="json") for item in inventory]
        ),
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
        sqlite_version=sqlite3.sqlite_version,
        dependency_versions=dict(sorted(versions.items())),
    )


def _git_stdout(repository_root: Path, *arguments: str) -> str:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise V43RunError(
            f"Git source-provenance command failed: {' '.join(arguments)}"
        ) from exc


def _fsync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _path_is_present(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _atomic_publish_directory_noreplace(source: Path, destination: Path) -> None:
    """Atomically publish a sibling directory and reject every existing target."""

    if source.parent.resolve() != destination.parent.resolve():
        raise V43RunError("V4.3 publication requires sibling directories")
    renameat2 = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    if renameat2 is None:
        raise V43RunError(
            "atomic no-replace directory publication is unavailable on this host"
        )
    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    at_fdcwd = -100
    rename_noreplace = 1
    result = renameat2(
        at_fdcwd,
        os.fsencode(source),
        at_fdcwd,
        os.fsencode(destination),
        rename_noreplace,
    )
    if result == 0:
        return
    error_number = ctypes.get_errno()
    if error_number in {errno.EEXIST, errno.ENOTEMPTY}:
        raise FileExistsError(
            error_number,
            "V4.3 publication destination already exists",
            destination,
        )
    raise OSError(error_number, os.strerror(error_number), destination)
