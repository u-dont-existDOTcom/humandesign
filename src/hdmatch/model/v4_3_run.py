"""Memory-bounded, cache-only canonical V4.3 universe runs.

This module has no chart-engine or cache-builder import.  It consumes only exact
artifacts that have already passed cache, mapping, response, and prevalence
verification.  Ranking uses the five frozen fields directly in an on-disk SQLite
sort; no scalar score is introduced.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import sqlite3
import tempfile
from collections.abc import Iterator
from contextlib import suppress
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from importlib import import_module
from itertools import zip_longest
from pathlib import Path
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
V43_RUNNER_VERSION: Final[str] = "v4.3-cache-stream-run-v1"
SCORE_HASH_STRATEGY: Final[str] = "sha256-canonical-json-lines-input-order-v1"
RANKED_HASH_STRATEGY: Final[str] = "sha256-canonical-json-lines-rank-order-v1"
RANKED_FILENAME: Final[str] = "ranked-scores.parquet.zst"
DETAIL_FILENAME: Final[str] = "bounded-detail.json"
FAILURE_FILENAME: Final[str] = "failure.json"
MANIFEST_FILENAME: Final[str] = "manifest.json"
PARQUET_BATCH_ROWS: Final[int] = 1024
MAX_DETAIL_ROWS: Final[int] = 10_000


class V43RunError(RuntimeError):
    """A Phase-4 run or its immutable output violates the cache-only contract."""


class V43RunFailedError(V43RunError):
    """Scoring/storage failed after preflight and a failure package was published."""

    def __init__(self, run_directory: Path, failure: V43RunFailureV1) -> None:
        self.run_directory = run_directory
        self.failure = failure
        super().__init__(
            f"V4.3 run failed at {failure.stage}; failure package: {run_directory}"
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
    byte_count: int = Field(gt=0)
    row_count: int = Field(ge=0)
    logical_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_hash_strategy: str = Field(min_length=1)
    storage_format: str = Field(min_length=1)


class V43RunFailureV1(_FrozenModel):
    schema_version: Literal["v4-3-run-failure-v1"] = "v4-3-run-failure-v1"
    stage: str = Field(min_length=1)
    error_type: str = Field(min_length=1)
    error_message: str = Field(min_length=1)
    input_ordinal: int | None = Field(default=None, ge=0)
    state_id: str | None = None
    candidate_record_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    successfully_scored_count: int = Field(ge=0)
    partial_score_records_sha256: str = Field(pattern=SHA256_PATTERN)
    score_hash_strategy: Literal[
        "sha256-canonical-json-lines-input-order-v1"
    ] = "sha256-canonical-json-lines-input-order-v1"


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
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)


class V43RunManifestV1(_FrozenModel):
    schema_version: Literal["v4-3-cache-run-manifest-v1"] = (
        "v4-3-cache-run-manifest-v1"
    )
    runner_version: Literal["v4.3-cache-stream-run-v1"] = (
        "v4.3-cache-stream-run-v1"
    )
    runner_source_sha256: str = Field(pattern=SHA256_PATTERN)
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
                or self.compliance is None
            ):
                raise ValueError("complete run artifact inventory is inconsistent")
        elif (
            self.failure_artifact is None
            or self.ranked_artifact is not None
            or self.bounded_detail_artifact is not None
            or self.compliance is not None
        ):
            raise ValueError("failed run must contain only a failure artifact")
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


class V43ExternalRankStore:
    """Disk-backed exact five-field ranking with bounded process memory."""

    def __init__(self, database_path: str | Path) -> None:
        self._path = Path(database_path)
        self._connection = sqlite3.connect(self._path)
        self._connection.execute("PRAGMA journal_mode=OFF")
        self._connection.execute("PRAGMA synchronous=OFF")
        self._connection.execute("PRAGMA temp_store=FILE")
        self._connection.execute(
            """
            CREATE TABLE score_records (
                input_ordinal INTEGER PRIMARY KEY,
                state_id TEXT NOT NULL UNIQUE,
                utc_start TEXT NOT NULL,
                net_information REAL NOT NULL,
                meaningful_contradictions INTEGER NOT NULL,
                detailed_support REAL NOT NULL,
                core_fit REAL NOT NULL,
                stable_duration_microseconds INTEGER NOT NULL,
                payload BLOB NOT NULL
            )
            """
        )
        self._digest = hashlib.sha256()
        self._count = 0
        self._finished = False
        self._append_mode: Literal["ordered", "verification-unordered"] | None = None

    @property
    def count(self) -> int:
        return self._count

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
            self._connection.commit()

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
            self._connection.commit()

    def _insert_record(
        self,
        record: V43MinimalScoreRecordV1,
        payload: bytes,
    ) -> None:
        self._connection.execute(
            """
            INSERT INTO score_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.input_ordinal,
                record.state_id,
                _utc_text(record.utc_start),
                record.net_information,
                record.meaningful_contradictions,
                record.detailed_support,
                record.core_fit,
                record.stable_duration_microseconds,
                payload,
            ),
        )

    def finish(self) -> None:
        if self._finished:
            raise V43RunError("external rank store was already finalized")
        self._connection.commit()
        self._finished = True

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
        self._connection.commit()
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
        utc_start,
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
    utc_start ASC,
    state_id ASC
"""


def run_verified_v4_3_cache(
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
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
    destination = Path(output_directory)
    if destination.exists():
        raise FileExistsError(f"V4.3 run destination already exists: {destination}")
    library, responses, prevalence, session = _preflight(
        repository_root=repository_root,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        prevalence_plan_path=prevalence_plan_path,
        prevalence_artifact_path=prevalence_artifact_path,
        response_artifact_path=response_artifact_path,
    )
    bindings = _run_bindings(session.bindings, responses)
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
    store = V43ExternalRankStore(staging / ".rank.sqlite3")
    current: V43MinimalScoreRecordV1 | None = None
    stage = "scoring"
    try:
        for ordinal, evaluation in enumerate(
            session.stream_verified_universe(responses.artifact.observed_responses())
        ):
            current = _minimal_score_record(ordinal, evaluation)
            stage = "score-store-write"
            store.append(current)
            stage = "scoring"
        store.finish()
        if store.count != declared_count:
            raise V43RunError("score store count differs from declared cache universe")
        stage = "ranked-artifact-write"
        ranked_summary = _write_and_verify_ranked_artifact(
            staging / RANKED_FILENAME,
            store,
            detail_limit=detail_limit,
        )
        stage = "bounded-detail-write"
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
        stage = "compliance-mint"
        complete = session.require_streamed_universe_compliance()
        if complete.response_set_sha256 != responses.artifact.response_set_sha256:
            raise V43RunError("streamed response-set identity mismatch")
        compliance = _compliance_model(complete.compliance)
        store.close()
        (staging / ".rank.sqlite3").unlink(missing_ok=True)
        manifest = V43RunManifestV1(
            runner_source_sha256=sha256_file(__file__),
            run_status="complete",
            bindings=bindings,
            declared_interval_count=declared_count,
            successfully_scored_count=store.count,
            score_records_sha256=store.score_records_sha256,
            ranked_artifact=ranked_summary.artifact,
            bounded_detail_artifact=detail_artifact,
            substantive_tie_group_count=(
                ranked_summary.substantive_tie_group_count
            ),
            tied_candidate_count=ranked_summary.tied_candidate_count,
            unresolved_observation_count_per_candidate=(
                current.unresolved_observation_count if current is not None else 0
            ),
            unresolved_mapping_ids=unresolved_ids,
            compliance=compliance,
        )
        stage = "manifest-last"
        write_new_canonical_json(staging / MANIFEST_FILENAME, manifest)
        _fsync_directory(staging)
        stage = "staged-verification"
        verify_v4_3_run(
            staging,
            repository_root=repository_root,
            cache_directory=cache_directory,
            trust_lock_path=trust_lock_path,
            mapping_library_path=mapping_library_path,
            mapping_source_library_path=mapping_source_library_path,
            prevalence_plan_path=prevalence_plan_path,
            prevalence_artifact_path=prevalence_artifact_path,
            response_artifact_path=response_artifact_path,
        )
        if destination.exists():
            raise FileExistsError(
                f"V4.3 run destination appeared before publish: {destination}"
            )
        os.rename(staging, destination)
        _fsync_directory(destination.parent)
        return _verified_run(destination, manifest)
    except Exception as exc:
        partial_count = store.count
        partial_hash = store.partial_score_records_sha256
        with suppress(sqlite3.Error):
            store.close()
        if isinstance(exc, V43UniverseStreamError):
            failure = V43RunFailureV1(
                stage="evaluation",
                error_type=exc.cause_type,
                error_message=exc.cause_message or exc.cause_type,
                input_ordinal=exc.input_ordinal,
                state_id=exc.state_id,
                candidate_record_sha256=exc.candidate_record_sha256,
                successfully_scored_count=partial_count,
                partial_score_records_sha256=partial_hash,
            )
        else:
            row_bound_failure = stage == "score-store-write"
            failure = V43RunFailureV1(
                stage=stage,
                error_type=type(exc).__name__,
                error_message=str(exc) or type(exc).__name__,
                input_ordinal=(
                    current.input_ordinal
                    if row_bound_failure and current is not None
                    else None
                ),
                state_id=(
                    current.state_id
                    if row_bound_failure and current is not None
                    else None
                ),
                candidate_record_sha256=(
                    current.candidate_record_sha256
                    if row_bound_failure and current is not None
                    else None
                ),
                successfully_scored_count=partial_count,
                partial_score_records_sha256=partial_hash,
            )
        published_failure = _publish_failure_package(
            destination=destination,
            previous_staging=staging,
            failure=failure,
            bindings=bindings,
            declared_count=declared_count,
            unresolved_mapping_ids=unresolved_ids,
        )
        raise V43RunFailedError(published_failure, failure) from exc


def verify_v4_3_run(
    run_directory: str | Path,
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    prevalence_plan_path: str | Path,
    prevalence_artifact_path: str | Path,
    response_artifact_path: str | Path,
) -> VerifiedV43Run:
    """Re-hash ranks, ties, order, and bindings without invoking astronomy."""

    directory = Path(run_directory)
    manifest = _load_manifest(directory / MANIFEST_FILENAME)
    library, responses, prevalence, session = _preflight(
        repository_root=repository_root,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
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
    )
    return _verified_run(directory, manifest)


def _preflight(
    *,
    repository_root: str | Path,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
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
    session = CanonicalV43ScoringSession.open(
        mapping_library=library,
        cache_directory=cache_directory,
        trust_lock_path=trust_lock_path,
        prevalence=prevalence,
    )
    expected = _run_bindings(session.bindings, responses)
    if responses.artifact.mapping_library_sha256 != expected.mapping_library_sha256:
        raise V43RunError("response/mapping library identity mismatch")
    if responses.artifact.mapping_source_library_sha256 != (
        expected.mapping_source_library_sha256
    ):
        raise V43RunError("response/mapping source-library identity mismatch")
    return library, responses, prevalence, session


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
        logical_universe_sha256=bindings.logical_universe_sha256,
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
) -> None:
    manifest_path = directory / MANIFEST_FILENAME
    if sha256_file(__file__) != manifest.runner_source_sha256:
        raise V43RunError("run was produced by different runner source bytes")
    if _run_bindings(session.bindings, responses) != manifest.bindings:
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
        _require_artifact_contract(
            manifest.failure_artifact,
            filename=FAILURE_FILENAME,
            logical_hash_strategy="sha256-canonical-json-v1",
            storage_format="canonical-json-v1",
        )
        _verify_artifact_file(directory, manifest.failure_artifact)
        if manifest.failure_artifact.row_count != 1:
            raise V43RunError("failure artifact row count must equal one")
        failure_path = directory / manifest.failure_artifact.filename
        failure = _load_failure(failure_path)
        if failure.successfully_scored_count != manifest.successfully_scored_count:
            raise V43RunError("failure partial score count differs from manifest")
        if failure.partial_score_records_sha256 != manifest.score_records_sha256:
            raise V43RunError("failure partial score hash differs from manifest")
        _verify_failure_partial_scores(
            failure,
            declared_count=manifest.declared_interval_count,
            responses=responses,
            session=session,
        )
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
    database_path = directory / ".verify-rank.sqlite3"
    if database_path.exists():
        raise V43RunError("verification scratch path unexpectedly exists")
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
            rescored_count += 1
        if rescored_count != manifest.declared_interval_count:
            raise V43RunError("cache-only rescore count mismatch")
        complete = session.require_streamed_universe_compliance()
        if complete.response_set_sha256 != manifest.bindings.response_set_sha256:
            raise V43RunError("verified response-set identity mismatch")
    finally:
        store.close()
        database_path.unlink(missing_ok=True)
    _verify_complete_compliance(manifest, library, complete.compliance)
    if manifest_path.read_bytes() != canonical_json_bytes(manifest):
        raise V43RunError("run manifest bytes changed after canonical load")


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


def _verify_failure_partial_scores(
    failure: V43RunFailureV1,
    *,
    declared_count: int,
    responses: VerifiedV43DirectTargetResponses,
    session: CanonicalV43ScoringSession,
) -> None:
    if failure.successfully_scored_count > declared_count:
        raise V43RunError("failure partial score count exceeds declared universe")
    row_bound = failure.input_ordinal is not None
    if row_bound:
        if (
            failure.input_ordinal != failure.successfully_scored_count
            or failure.state_id is None
            or failure.candidate_record_sha256 is None
        ):
            raise V43RunError("failure row binding is incomplete or out of order")
    elif failure.state_id is not None or failure.candidate_record_sha256 is not None:
        raise V43RunError("failure row fields exist without an input ordinal")
    elif failure.successfully_scored_count != declared_count:
        raise V43RunError(
            "partial-universe failure lacks the exact next-row identity"
        )

    digest = hashlib.sha256()
    observed_count = 0
    found_failure_row = False
    stream = session.stream_verified_universe(
        responses.artifact.observed_responses()
    )
    try:
        for evaluation in stream:
            if observed_count < failure.successfully_scored_count:
                record = _minimal_score_record(observed_count, evaluation)
                payload = canonical_json_bytes(record)
                digest.update(payload)
                digest.update(b"\n")
                observed_count += 1
                continue
            if not row_bound:
                raise V43RunError(
                    "failure declared complete scoring but cache has extra rows"
                )
            if (
                evaluation.state_id != failure.state_id
                or evaluation.candidate_record_sha256
                != failure.candidate_record_sha256
            ):
                raise V43RunError("failure row differs from cache-only rescore")
            found_failure_row = True
            break
    except V43UniverseStreamError as exc:
        if (
            not row_bound
            or exc.input_ordinal != failure.input_ordinal
            or exc.state_id != failure.state_id
            or exc.candidate_record_sha256 != failure.candidate_record_sha256
        ):
            raise V43RunError(
                "failure location differs from cache-only rescore"
            ) from exc
        found_failure_row = True
    finally:
        stream.close()
    if observed_count != failure.successfully_scored_count:
        raise V43RunError("failure partial score count cannot be replayed")
    if row_bound and not found_failure_row:
        raise V43RunError("failure row is absent from the verified cache")
    if digest.hexdigest() != failure.partial_score_records_sha256:
        raise V43RunError("failure partial score hash differs from cache-only replay")


def _publish_failure_package(
    *,
    destination: Path,
    previous_staging: Path,
    failure: V43RunFailureV1,
    bindings: V43RunBindingsV1,
    declared_count: int,
    unresolved_mapping_ids: tuple[str, ...],
) -> Path:
    if previous_staging.is_dir():
        shutil.rmtree(previous_staging)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.failure-staging-",
            dir=destination.parent,
        )
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
        run_status="failed",
        bindings=bindings,
        declared_interval_count=declared_count,
        successfully_scored_count=failure.successfully_scored_count,
        score_records_sha256=failure.partial_score_records_sha256,
        failure_artifact=failure_artifact,
        substantive_tie_group_count=0,
        tied_candidate_count=0,
        unresolved_observation_count_per_candidate=0,
        unresolved_mapping_ids=unresolved_mapping_ids,
    )
    write_new_canonical_json(staging / MANIFEST_FILENAME, manifest)
    _verify_artifact_file(staging, failure_artifact)
    _fsync_directory(staging)
    if destination.exists():
        raise FileExistsError(
            f"V4.3 run destination appeared before failure publish: {destination}"
        )
    os.rename(staging, destination)
    _fsync_directory(destination.parent)
    return destination


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
    if not path.is_file():
        raise V43RunError(f"run artifact is missing: {artifact.filename}")
    if path.stat().st_size != artifact.byte_count:
        raise V43RunError(f"run artifact byte count mismatch: {artifact.filename}")
    if sha256_file(path) != artifact.sha256:
        raise V43RunError(f"run artifact hash mismatch: {artifact.filename}")


def _load_manifest(path: Path) -> V43RunManifestV1:
    try:
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
        raw = path.read_bytes()
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw:
            raise V43RunError("V4.3 failure artifact is not canonical JSON")
        return V43RunFailureV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43RunError):
            raise
        raise V43RunError(f"invalid V4.3 failure artifact: {path}") from exc


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
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parse_utc_text(value: object) -> datetime:
    if not isinstance(value, str):
        raise V43RunError("ranked timestamp is not a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() != timedelta(0):
        raise V43RunError("ranked timestamp is not UTC")
    return parsed.astimezone(UTC)


def _fsync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
