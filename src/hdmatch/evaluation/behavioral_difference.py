"""Answer-key-free gate proving that prospective V2 changes behavior and ranking.

This audit is deliberately run on a public candidate universe before generating a
synthetic experiment.  It does not identify any candidate as true.  Instead, it
looks for two exact chart intervals that Model A treats as the same state, verifies
that prospective V2 produces a non-unknown detailed response difference, and then
checks that V2 splits the Model A scoring tie for responses sourced from one of the
two public candidates.
"""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import load_json_bytes, sha256_file
from hdmatch.model_b_v2_new import FrozenModelBV2New
from hdmatch.runtime.symbolic_adapter import FrozenSymbolicModel, candidate_prevalence
from hdmatch.runtime.universe_cache import CachedUniverse, MonthRequest, load_cached_universe
from hdmatch.schemas import BehavioralResponse, CandidateState, ScoredState
from hdmatch.util import sha256_json

SHA256_PATTERN = r"^[a-f0-9]{64}$"


class FrozenAuditModel(BaseModel):
    """Strict immutable base for a canonicalizable public audit artifact."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class PairwiseTieSplit(FrozenAuditModel):
    """One public same-core pair whose V2 responses and scores differ."""

    source_state_id: str
    comparison_state_id: str
    model_a_signature_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    model_a_response_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    source_v2_response_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    comparison_v2_response_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    non_unknown_detailed_delta_question_ids: tuple[str, ...] = Field(min_length=1)
    model_a_source_score: ScoredState
    model_a_comparison_score: ScoredState
    model_b_source_score: ScoredState
    model_b_comparison_score: ScoredState
    model_a_pair_relation: Literal["tie"] = "tie"
    model_b_pair_relation: Literal[
        "source_above_comparison", "comparison_above_source"
    ]

    @model_validator(mode="after")
    def validate_score_identity_and_relation(self) -> PairwiseTieSplit:
        if self.source_state_id == self.comparison_state_id:
            raise ValueError("a tie-split witness requires two distinct states")
        source_scores = (self.model_a_source_score, self.model_b_source_score)
        comparison_scores = (
            self.model_a_comparison_score,
            self.model_b_comparison_score,
        )
        if any(score.state_id != self.source_state_id for score in source_scores):
            raise ValueError("source witness score state IDs are inconsistent")
        if any(score.state_id != self.comparison_state_id for score in comparison_scores):
            raise ValueError("comparison witness score state IDs are inconsistent")
        if not math.isclose(
            self.model_a_source_score.net_rubric_bits,
            self.model_a_comparison_score.net_rubric_bits,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ValueError("a Model A tie-split witness must contain a Model A score tie")
        source_above = (
            self.model_b_source_score.net_rubric_bits
            > self.model_b_comparison_score.net_rubric_bits
        )
        comparison_above = (
            self.model_b_comparison_score.net_rubric_bits
            > self.model_b_source_score.net_rubric_bits
        )
        expected = (
            "source_above_comparison" if source_above else "comparison_above_source"
        )
        if not (source_above or comparison_above) or self.model_b_pair_relation != expected:
            raise ValueError("V2 witness relation is inconsistent with its exact scores")
        return self


class BehavioralDifferenceMonthRequest(FrozenAuditModel):
    """Canonical public identity of the exact month audited."""

    year: int
    month: int = Field(ge=1, le=12)
    timezone_name: str = Field(min_length=1)

    @classmethod
    def from_runtime(cls, request: MonthRequest) -> BehavioralDifferenceMonthRequest:
        return cls(
            year=request.year,
            month=request.month,
            timezone_name=request.timezone_name,
        )

    def to_runtime(self) -> MonthRequest:
        return MonthRequest(self.year, self.month, self.timezone_name)


class BehavioralDifferenceAudit(FrozenAuditModel):
    """Transparent pre-benchmark result with no truth or answer-key dependency."""

    schema_version: Literal["model-b-v2-new-behavioral-difference-audit-v2"] = (
        "model-b-v2-new-behavioral-difference-audit-v2"
    )
    audited_at_utc: datetime
    status: Literal["passed", "failed"]
    model_a_id: Literal["MODEL-A-CORE-V1"] = "MODEL-A-CORE-V1"
    model_b_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    model_a_sha256: str = Field(pattern=SHA256_PATTERN)
    model_a_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_compiled_file_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_freeze_receipt_file_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_cache_file_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_engine_fingerprint: str = Field(pattern=SHA256_PATTERN)
    candidate_universe_request: BehavioralDifferenceMonthRequest
    candidate_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_state_count: int = Field(ge=1)
    same_core_group_count: int = Field(ge=0)
    groups_with_non_unknown_response_delta: int = Field(ge=0)
    groups_with_pairwise_tie_split: int = Field(ge=0)
    groups_with_source_favoring_tie_split: int = Field(ge=0)
    groups_with_adverse_tie_split: int = Field(ge=0)
    witnesses: tuple[PairwiseTieSplit, ...]
    failure_reasons: tuple[str, ...]
    answer_keys_used: Literal[False] = False
    candidate_truth_used: Literal[False] = False
    claim_boundary: Literal[
        "engineering-difference-gate-only-not-human-validation"
    ] = "engineering-difference-gate-only-not-human-validation"

    @field_validator("audited_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("behavioral-difference audit timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_internal_consistency(self) -> BehavioralDifferenceAudit:
        if self.model_b_mapping_sha256 != self.model_b_compiled_file_sha256:
            raise ValueError("V2 mapping hash must equal the exact compiled-file hash")
        counts = (
            self.groups_with_non_unknown_response_delta,
            self.groups_with_pairwise_tie_split,
            self.groups_with_source_favoring_tie_split,
            self.groups_with_adverse_tie_split,
        )
        if any(value > self.same_core_group_count for value in counts):
            raise ValueError("difference-group count exceeds the same-core group count")
        if self.groups_with_pairwise_tie_split > self.groups_with_non_unknown_response_delta:
            raise ValueError("a pairwise split requires a non-unknown response delta")
        if (
            self.groups_with_source_favoring_tie_split
            > self.groups_with_pairwise_tie_split
            or self.groups_with_adverse_tie_split
            > self.groups_with_pairwise_tie_split
        ):
            raise ValueError("directional split count exceeds pairwise split groups")
        favorable_witnesses = sum(
            item.model_b_pair_relation == "source_above_comparison" for item in self.witnesses
        )
        adverse_witnesses = sum(
            item.model_b_pair_relation == "comparison_above_source" for item in self.witnesses
        )
        if favorable_witnesses != self.groups_with_source_favoring_tie_split:
            raise ValueError("source-favoring witness count is inconsistent")
        if adverse_witnesses != self.groups_with_adverse_tie_split:
            raise ValueError("adverse witness count is inconsistent")
        should_pass = (
            self.groups_with_source_favoring_tie_split > 0
            and self.groups_with_adverse_tie_split == 0
            and bool(self.witnesses)
        )
        if (self.status == "passed") != should_pass:
            raise ValueError("audit status is inconsistent with its tie-split evidence")
        if self.status == "passed" and self.failure_reasons:
            raise ValueError("a passing audit cannot contain failure reasons")
        if self.status == "failed" and not self.failure_reasons:
            raise ValueError("a failed audit must preserve at least one failure reason")
        return self


class VerifiedBehavioralDifferenceBinding(FrozenAuditModel):
    """Immutable public proof returned only after complete gate verification."""

    schema_version: Literal["model-b-v2-new-verified-difference-binding-v1"] = (
        "model-b-v2-new-verified-difference-binding-v1"
    )
    audit_file_sha256: str = Field(pattern=SHA256_PATTERN)
    audited_at_utc: datetime
    model_a_sha256: str = Field(pattern=SHA256_PATTERN)
    model_a_mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_compiled_file_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_freeze_receipt_file_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_cache_file_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_engine_fingerprint: str = Field(pattern=SHA256_PATTERN)
    candidate_universe_request: BehavioralDifferenceMonthRequest
    candidate_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_state_count: int = Field(ge=1)

    @field_validator("audited_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("verified audit timestamp must be timezone-aware")
        return value.astimezone(UTC)


def audit_behavioral_difference(
    candidate_universe: CachedUniverse,
    model_a: FrozenSymbolicModel,
    model_b: FrozenModelBV2New,
    *,
    engine_fingerprint: str,
    audited_at_utc: datetime | None = None,
) -> BehavioralDifferenceAudit:
    """Audit public candidate pairs without accepting answer keys or truth labels."""

    states = candidate_universe.states
    if not states:
        raise ValueError("behavioral difference audit requires candidate states")
    if model_a.question_bank_sha256 != model_b.question_bank_sha256:
        raise ValueError("Model A and V2 must bind the same question bank")
    if sha256_file(candidate_universe.path) != candidate_universe.sha256:
        raise ValueError("candidate cache bytes changed after the exact universe was loaded")
    if len(engine_fingerprint) != 64 or any(
        character not in "0123456789abcdef" for character in engine_fingerprint
    ):
        raise ValueError("candidate engine fingerprint must be a SHA-256 digest")
    timestamp = audited_at_utc or datetime.now(UTC)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("behavioral-difference audit timestamp must be timezone-aware")
    if model_b.freeze_receipt.frozen_at_utc > timestamp:
        raise ValueError("V2 model freeze must predate the behavioral-difference audit")

    state_tuple = tuple(sorted(states, key=lambda item: item.state_id))
    groups: dict[tuple[object, ...], list[CandidateState]] = defaultdict(list)
    for state in state_tuple:
        groups[model_a.score_signature(state.chart_features)].append(state)
    same_core_groups = tuple(
        (signature, tuple(items))
        for signature, items in sorted(
            groups.items(), key=lambda item: sha256_json(item[0])
        )
        if len(items) >= 2
    )

    model_a_prevalence = candidate_prevalence(state_tuple, model_a.library)
    model_b_prevalence = model_b.prepare_prevalence(state_tuple)
    response_delta_groups = 0
    tie_split_groups = 0
    source_favoring_groups = 0
    adverse_groups = 0
    witnesses: list[PairwiseTieSplit] = []
    for signature, group in same_core_groups:
        favorable, adverse, has_response_delta = _directional_tie_splits(
            group,
            signature=signature,
            model_a=model_a,
            model_b=model_b,
            model_a_prevalence=model_a_prevalence,
            model_b_prevalence=model_b_prevalence,
        )
        response_delta_groups += int(has_response_delta)
        tie_split_groups += int(favorable is not None or adverse is not None)
        source_favoring_groups += int(favorable is not None)
        adverse_groups += int(adverse is not None)
        witnesses.extend(item for item in (favorable, adverse) if item is not None)

    reasons: list[str] = []
    if not same_core_groups:
        reasons.append("no Model A equivalence group contained at least two exact states")
    if not response_delta_groups:
        reasons.append(
            "V2 produced no non-unknown detailed response delta inside a Model A group"
        )
    if not source_favoring_groups:
        reasons.append(
            "V2 did not split a Model A tie in favor of its own response-source state"
        )
    if adverse_groups:
        reasons.append(
            "V2 produced an adverse split that ranked a comparison above its own "
            "response-source state"
        )
    status: Literal["passed", "failed"] = (
        "passed" if source_favoring_groups and not adverse_groups else "failed"
    )
    return BehavioralDifferenceAudit(
        audited_at_utc=timestamp,
        status=status,
        model_a_sha256=model_a.model_sha256,
        model_b_sha256=model_b.model_sha256,
        model_a_mapping_sha256=model_a.mapping_sha256,
        model_b_mapping_sha256=model_b.mapping_sha256,
        model_b_compiled_file_sha256=sha256_file(model_b.compiled_artifact_path),
        model_b_freeze_receipt_file_sha256=sha256_file(model_b.freeze_receipt_path),
        question_bank_sha256=model_a.question_bank_sha256,
        candidate_cache_file_sha256=candidate_universe.sha256,
        candidate_engine_fingerprint=engine_fingerprint,
        candidate_universe_request=BehavioralDifferenceMonthRequest.from_runtime(
            candidate_universe.request
        ),
        candidate_universe_sha256=_candidate_universe_sha256(state_tuple),
        candidate_state_count=len(state_tuple),
        same_core_group_count=len(same_core_groups),
        groups_with_non_unknown_response_delta=response_delta_groups,
        groups_with_pairwise_tie_split=tie_split_groups,
        groups_with_source_favoring_tie_split=source_favoring_groups,
        groups_with_adverse_tie_split=adverse_groups,
        witnesses=tuple(witnesses),
        failure_reasons=tuple(reasons),
    )


def require_behavioral_difference(audit: BehavioralDifferenceAudit) -> None:
    """Fail closed when a benchmark is attempted without a passing difference gate."""

    if (
        audit.status != "passed"
        or not audit.witnesses
        or audit.groups_with_source_favoring_tie_split < 1
        or audit.groups_with_adverse_tie_split != 0
        or audit.failure_reasons
    ):
        detail = "; ".join(audit.failure_reasons) or "no passing witness"
        raise ValueError(f"MODEL-B-DETAILED-V2-NEW difference gate failed: {detail}")


def load_behavioral_difference_audit(path: str | Path) -> BehavioralDifferenceAudit:
    """Load one exact canonical audit artifact without accepting alternate encodings."""

    try:
        raw = load_json_bytes(path, require_canonical=True)
        return BehavioralDifferenceAudit.model_validate(raw)
    except (OSError, ValueError) as exc:
        raise ValueError(f"invalid or non-canonical behavioral-difference audit: {path}") from exc


def verify_behavioral_difference_audit(
    audit_path: str | Path,
    *,
    model_a: FrozenSymbolicModel,
    model_b: FrozenModelBV2New,
    candidate_cache_path: str | Path,
    candidate_request: MonthRequest,
    engine_fingerprint: str,
    expected_binding: VerifiedBehavioralDifferenceBinding | None = None,
) -> VerifiedBehavioralDifferenceBinding:
    """Verify a passed public audit against every current model and cache byte.

    This interface deliberately has no truth, answer-key, reveal, or decrypt input.
    Cache validation only reads an already-materialized exact universe; it never
    generates candidate states.
    """

    audit = load_behavioral_difference_audit(audit_path)
    require_behavioral_difference(audit)
    cache = load_cached_universe(
        candidate_cache_path,
        request=candidate_request,
        engine_fingerprint=engine_fingerprint,
    )
    current_compiled_sha256 = sha256_file(model_b.compiled_artifact_path)
    current_freeze_sha256 = sha256_file(model_b.freeze_receipt_path)
    current_universe_sha256 = _candidate_universe_sha256(
        tuple(sorted(cache.states, key=lambda item: item.state_id))
    )
    current_request = BehavioralDifferenceMonthRequest.from_runtime(candidate_request)
    if model_b.freeze_receipt.frozen_at_utc > audit.audited_at_utc:
        raise ValueError("behavioral-difference audit predates the V2 model freeze")
    expected_fields: tuple[tuple[str, object, object], ...] = (
        ("model_a_sha256", audit.model_a_sha256, model_a.model_sha256),
        (
            "model_a_mapping_sha256",
            audit.model_a_mapping_sha256,
            model_a.mapping_sha256,
        ),
        ("model_b_sha256", audit.model_b_sha256, model_b.model_sha256),
        (
            "model_b_mapping_sha256",
            audit.model_b_mapping_sha256,
            model_b.mapping_sha256,
        ),
        (
            "model_b_compiled_file_sha256",
            audit.model_b_compiled_file_sha256,
            current_compiled_sha256,
        ),
        (
            "model_b_freeze_receipt_file_sha256",
            audit.model_b_freeze_receipt_file_sha256,
            current_freeze_sha256,
        ),
        (
            "question_bank_sha256",
            audit.question_bank_sha256,
            model_a.question_bank_sha256,
        ),
        (
            "model_b_question_bank_sha256",
            audit.question_bank_sha256,
            model_b.question_bank_sha256,
        ),
        (
            "candidate_cache_file_sha256",
            audit.candidate_cache_file_sha256,
            cache.sha256,
        ),
        (
            "candidate_engine_fingerprint",
            audit.candidate_engine_fingerprint,
            engine_fingerprint,
        ),
        (
            "candidate_universe_request",
            audit.candidate_universe_request,
            current_request,
        ),
        (
            "candidate_state_count",
            audit.candidate_state_count,
            len(cache.states),
        ),
        (
            "candidate_universe_sha256",
            audit.candidate_universe_sha256,
            current_universe_sha256,
        ),
    )
    for label, recorded, current in expected_fields:
        if recorded != current:
            raise ValueError(f"behavioral-difference audit {label} is stale or mismatched")

    states_by_id = {state.state_id: state for state in cache.states}
    for witness in audit.witnesses:
        if (
            witness.source_state_id not in states_by_id
            or witness.comparison_state_id not in states_by_id
        ):
            raise ValueError("behavioral-difference witness is outside the bound universe")
        source_signature = model_a.score_signature(
            states_by_id[witness.source_state_id].chart_features
        )
        comparison_signature = model_a.score_signature(
            states_by_id[witness.comparison_state_id].chart_features
        )
        if source_signature != comparison_signature:
            raise ValueError("behavioral-difference witness is not a current Model A tie group")

    recomputed = audit_behavioral_difference(
        cache,
        model_a,
        model_b,
        engine_fingerprint=engine_fingerprint,
        audited_at_utc=audit.audited_at_utc,
    )
    if recomputed != audit:
        raise ValueError(
            "behavioral-difference audit result does not match deterministic recomputation"
        )

    binding = VerifiedBehavioralDifferenceBinding(
        audit_file_sha256=sha256_file(audit_path),
        audited_at_utc=audit.audited_at_utc,
        model_a_sha256=audit.model_a_sha256,
        model_a_mapping_sha256=audit.model_a_mapping_sha256,
        model_b_compiled_file_sha256=current_compiled_sha256,
        model_b_freeze_receipt_file_sha256=current_freeze_sha256,
        model_b_sha256=audit.model_b_sha256,
        question_bank_sha256=audit.question_bank_sha256,
        candidate_cache_file_sha256=cache.sha256,
        candidate_engine_fingerprint=engine_fingerprint,
        candidate_universe_request=current_request,
        candidate_universe_sha256=current_universe_sha256,
        candidate_state_count=len(cache.states),
    )
    if expected_binding is not None and binding != expected_binding:
        raise ValueError("behavioral-difference audit does not match the expected binding")
    return binding


def _directional_tie_splits(
    states: tuple[CandidateState, ...],
    *,
    signature: tuple[object, ...],
    model_a: FrozenSymbolicModel,
    model_b: FrozenModelBV2New,
    model_a_prevalence: object,
    model_b_prevalence: object,
) -> tuple[PairwiseTieSplit | None, PairwiseTieSplit | None, bool]:
    response_by_state = {
        state.state_id: tuple(model_b.oracle_responses(state.chart_features)) for state in states
    }
    model_a_question_ids = {
        response.question_id
        for response in model_a.oracle_responses(states[0].chart_features)
    }
    saw_non_unknown_delta = False
    first_favorable: PairwiseTieSplit | None = None
    first_adverse: PairwiseTieSplit | None = None
    for left_index, left in enumerate(states):
        for right in states[left_index + 1 :]:
            left_responses = response_by_state[left.state_id]
            right_responses = response_by_state[right.state_id]
            delta_questions = _non_unknown_detailed_delta(
                left_responses,
                right_responses,
                base_question_ids=model_a_question_ids,
            )
            if not delta_questions:
                continue
            saw_non_unknown_delta = True
            for source, comparison, source_responses, comparison_responses in (
                (left, right, left_responses, right_responses),
                (right, left, right_responses, left_responses),
            ):
                if not any(
                    _answer_for(source_responses, question_id) != "unknown"
                    for question_id in delta_questions
                ):
                    continue
                witness = _score_direction(
                    source,
                    comparison,
                    source_responses,
                    comparison_responses,
                    delta_questions=delta_questions,
                    signature=signature,
                    model_a=model_a,
                    model_b=model_b,
                    model_a_prevalence=model_a_prevalence,
                    model_b_prevalence=model_b_prevalence,
                )
                if witness is None:
                    continue
                if witness.model_b_pair_relation == "source_above_comparison":
                    first_favorable = first_favorable or witness
                else:
                    first_adverse = first_adverse or witness
    return first_favorable, first_adverse, saw_non_unknown_delta


def _score_direction(
    source: CandidateState,
    comparison: CandidateState,
    source_responses: tuple[BehavioralResponse, ...],
    comparison_responses: tuple[BehavioralResponse, ...],
    *,
    delta_questions: tuple[str, ...],
    signature: tuple[object, ...],
    model_a: FrozenSymbolicModel,
    model_b: FrozenModelBV2New,
    model_a_prevalence: object,
    model_b_prevalence: object,
) -> PairwiseTieSplit | None:
    model_a_source = model_a.score(
        source,
        source_responses,
        model_a_prevalence,  # type: ignore[arg-type]
    )
    model_a_comparison = model_a.score(
        comparison,
        source_responses,
        model_a_prevalence,  # type: ignore[arg-type]
    )
    if not _scores_tied(model_a_source, model_a_comparison):
        raise AssertionError(
            "states sharing a Model A signature did not receive the same Model A score"
        )
    model_b_source = model_b.score(
        source,
        source_responses,
        model_b_prevalence,  # type: ignore[arg-type]
    )
    model_b_comparison = model_b.score(
        comparison,
        source_responses,
        model_b_prevalence,  # type: ignore[arg-type]
    )
    if _scores_tied(model_b_source, model_b_comparison):
        return None
    relation: Literal["source_above_comparison", "comparison_above_source"] = (
        "source_above_comparison"
        if model_b_source.net_rubric_bits > model_b_comparison.net_rubric_bits
        else "comparison_above_source"
    )
    return PairwiseTieSplit(
        source_state_id=source.state_id,
        comparison_state_id=comparison.state_id,
        model_a_signature_sha256=sha256_json(signature),
        model_a_response_sha256=_responses_sha256(
            tuple(model_a.oracle_responses(source.chart_features))
        ),
        source_v2_response_sha256=_responses_sha256(source_responses),
        comparison_v2_response_sha256=_responses_sha256(comparison_responses),
        non_unknown_detailed_delta_question_ids=delta_questions,
        model_a_source_score=model_a_source,
        model_a_comparison_score=model_a_comparison,
        model_b_source_score=model_b_source,
        model_b_comparison_score=model_b_comparison,
        model_b_pair_relation=relation,
    )


def _answer_for(responses: tuple[BehavioralResponse, ...], question_id: str) -> str:
    return next(
        (item.answer for item in responses if item.question_id == question_id),
        "unknown",
    )


def _non_unknown_detailed_delta(
    left: tuple[BehavioralResponse, ...],
    right: tuple[BehavioralResponse, ...],
    *,
    base_question_ids: set[str],
) -> tuple[str, ...]:
    left_answers = {item.question_id: item.answer for item in left}
    right_answers = {item.question_id: item.answer for item in right}
    questions = (set(left_answers) | set(right_answers)) - base_question_ids
    return tuple(
        sorted(
            question_id
            for question_id in questions
            if left_answers.get(question_id, "unknown")
            != right_answers.get(question_id, "unknown")
            and {
                left_answers.get(question_id, "unknown"),
                right_answers.get(question_id, "unknown"),
            }
            != {"unknown"}
        )
    )


def _scores_tied(left: ScoredState, right: ScoredState) -> bool:
    return math.isclose(
        left.net_rubric_bits,
        right.net_rubric_bits,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def _responses_sha256(responses: tuple[BehavioralResponse, ...]) -> str:
    return sha256_json(
        [
            item.model_dump(mode="json")
            for item in sorted(responses, key=lambda response: response.question_id)
        ]
    )


def _candidate_universe_sha256(states: tuple[CandidateState, ...]) -> str:
    return sha256_json(
        [state.model_dump(mode="json") for state in states]
    )
