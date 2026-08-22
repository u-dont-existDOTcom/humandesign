"""Claim-bound paired Model A versus prospective Model B V2 comparison.

The loader consumes public, already-revealed run artifacts.  It has no key,
decrypt, answer-key, recovery, or scoring interface.  Every arm is verified from
its blind input through its evaluation before any cross-model statistic is
computed.
"""

from __future__ import annotations

import calendar
import math
import statistics
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from hdmatch.evaluation.ablation import (
    ClusterAblationSummary,
    CurveObservation,
    CurvePoint,
    LeaveOneClusterOutObservation,
    aggregate_leave_one_cluster_out,
    aggregate_restoration_curves,
)
from hdmatch.evaluation.failures import (
    FailureClassification,
    FailureRecord,
    classify_oracle_failure,
)
from hdmatch.evaluation.metrics import (
    AggregateRankMetrics,
    CaseRankMetrics,
    aggregate_rank_metrics,
    evaluate_ranked_case,
)
from hdmatch.evaluation.report import EvaluationReport
from hdmatch.experiments.answer_key_commitments import revealed_local_date_set_hash
from hdmatch.experiments.canonical import (
    load_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import (
    ArtifactBindings,
    FreezeRecord,
    FreezeVerificationError,
    verify_frozen_predictions,
)
from hdmatch.experiments.manifest import (
    SHA256_PATTERN,
    RunManifest,
    load_run_manifest,
)
from hdmatch.experiments.paired import (
    PairedExperimentBindingError,
    PairedExperimentPlan,
    PairedGenerationReceiptBinding,
    load_paired_experiment_plan,
    verify_paired_generation_receipt_binding,
)
from hdmatch.experiments.paired_freeze import (
    PairedFreezeArmArtifacts,
    PairedPredictionFreezeReceipt,
    verify_paired_prediction_freeze_receipt,
)
from hdmatch.experiments.reveal import RevealRecord, verify_reveal_record
from hdmatch.runtime.symbolic_adapter import MODEL_A_ID, MODEL_B_V2_NEW_ID
from hdmatch.synthetic.noise import NoiseTier, noise_parameters_payload


class PairedModelComparisonError(ValueError):
    """A run or pair fails the frozen public comparison contract."""


class FrozenComparisonModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RecoverySettingsBinding(FrozenComparisonModel):
    aggregation: str = Field(min_length=1)
    threshold_rubric_bits: float
    workers: int = Field(ge=1)
    cache_policy: Literal["hash-bound exact month universes"] = "hash-bound exact month universes"


class BlindCaseConstraint(FrozenComparisonModel):
    case_id: str = Field(min_length=1)
    candidate_universe: Literal["known_month"]
    known_birth_year: int
    known_birth_month: int = Field(ge=1, le=12)
    known_birth_day: None = None
    iana_timezone: str = Field(min_length=1)


class RecomputedKnownMonthEvaluation(FrozenComparisonModel):
    """Metrics derived again from frozen predictions and authenticated public dates."""

    aggregate: AggregateRankMetrics
    cases: tuple[CaseRankMetrics, ...]
    failures: tuple[FailureRecord, ...]
    failure_counts: dict[str, int]
    restoration_curves: tuple[CurvePoint, ...]
    leave_one_cluster_out: tuple[ClusterAblationSummary, ...]


class VerifiedPublicRun(FrozenComparisonModel):
    """Public evidence extracted only after full byte-chain verification."""

    model_id: Literal["MODEL-A-CORE-V1", "MODEL-B-DETAILED-V2-NEW"]
    experiment_id: str = Field(min_length=1)
    run_manifest: RunManifest
    recomputed_evaluation: RecomputedKnownMonthEvaluation
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    reveal_sha256: str = Field(pattern=SHA256_PATTERN)
    evaluation_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_receipt_sha256: str = Field(pattern=SHA256_PATTERN)
    isolation_receipt_sha256: str = Field(pattern=SHA256_PATTERN)
    public_config_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_started_at_utc: datetime
    evaluation_created_at_utc: datetime
    reveal_created_at_utc: datetime
    revealed_target_set_sha256: str = Field(pattern=SHA256_PATTERN)
    revealed_local_date_set_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_seed_commitment_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_prediction_freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_arm_id: str = Field(min_length=1)
    case_ids: tuple[str, ...] = Field(min_length=1)
    candidate_constraints: tuple[BlindCaseConstraint, ...] = Field(min_length=1)
    candidate_constraints_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_sha256: dict[str, str] = Field(min_length=1)
    candidate_cache_sha256: dict[str, str] = Field(min_length=1)
    isolation_software_tree: str = Field(pattern=r"^[a-f0-9]{40}$")
    recovery_settings: RecoverySettingsBinding
    model_capabilities: dict[str, Any]
    difference_gate: dict[str, Any] | None = None

    @field_validator(
        "generation_started_at_utc",
        "evaluation_created_at_utc",
        "reveal_created_at_utc",
    )
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("generation timestamp must be timezone-aware")
        return value.astimezone(UTC)


class VerifiedPairedExperimentEvidence(FrozenComparisonModel):
    """Exact public plan and per-arm generation bindings verified before comparison."""

    plan: PairedExperimentPlan
    plan_file_sha256: str = Field(pattern=SHA256_PATTERN)
    public_config_file_sha256: str = Field(pattern=SHA256_PATTERN)
    model_a_generation_binding: PairedGenerationReceiptBinding
    model_a_generation_binding_file_sha256: str = Field(pattern=SHA256_PATTERN)
    model_b_generation_binding: PairedGenerationReceiptBinding
    model_b_generation_binding_file_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_prediction_freeze: PairedPredictionFreezeReceipt
    paired_prediction_freeze_file_sha256: str = Field(pattern=SHA256_PATTERN)


class ScalarMetricDelta(FrozenComparisonModel):
    model_a: float | None
    model_b: float | None
    b_minus_a: float | None


class PairedCaseResult(FrozenComparisonModel):
    case_id: str
    true_local_date: str | None
    candidate_count: int | None = Field(default=None, ge=1)
    model_a: CaseRankMetrics | None
    model_b: CaseRankMetrics | None
    b_minus_a_midrank: float | None
    b_minus_a_percentile: float | None
    b_minus_a_reciprocal_rank: float | None
    b_minus_a_top_1_credit: float | None
    b_minus_a_top_3_credit: float | None
    b_minus_a_top_5_credit: float | None
    outcome: Literal["improved", "unchanged", "worsened", "unevaluable"]
    model_a_tied: bool | None
    model_b_tied: bool | None
    model_a_failure_classes: tuple[str, ...]
    model_b_failure_classes: tuple[str, ...]


class PairedOutcomeCounts(FrozenComparisonModel):
    improved: int = Field(ge=0)
    unchanged: int = Field(ge=0)
    worsened: int = Field(ge=0)
    unevaluable: int = Field(ge=0)


class ChanceCalendarBaseline(FrozenComparisonModel):
    interpretation: Literal["all-known-month-dates-tied-random-order-calendar-only"] = (
        "all-known-month-dates-tied-random-order-calendar-only"
    )
    top_1: float = Field(ge=0.0, le=1.0)
    top_3: float = Field(ge=0.0, le=1.0)
    top_5: float = Field(ge=0.0, le=1.0)
    mean_reciprocal_rank: float = Field(ge=0.0, le=1.0)
    mean_midrank: float = Field(ge=1.0)
    mean_percentile: float = Field(ge=0.0, le=1.0)


class RestorationDifference(FrozenComparisonModel):
    method: Literal["random", "active", "leave_one_out"]
    cluster_count: int = Field(ge=0)
    model_a: CurvePoint | None
    model_b: CurvePoint | None
    mean_midrank: ScalarMetricDelta
    mean_reciprocal_rank: ScalarMetricDelta
    top_1: ScalarMetricDelta
    top_3: ScalarMetricDelta
    top_5: ScalarMetricDelta
    tie_rate: ScalarMetricDelta


class AblationDifference(FrozenComparisonModel):
    cluster_id: str
    model_a: ClusterAblationSummary | None
    model_b: ClusterAblationSummary | None
    mean_rank_change: ScalarMetricDelta
    median_rank_change: ScalarMetricDelta
    worsened_fraction: ScalarMetricDelta


class PairedModelComparisonReport(FrozenComparisonModel):
    schema_version: Literal["model-a-v2-new-paired-comparison-v1"] = (
        "model-a-v2-new-paired-comparison-v1"
    )
    created_at_utc: datetime
    experiment_id: str
    case_count: int = Field(ge=1)
    model_a_id: Literal["MODEL-A-CORE-V1"] = "MODEL-A-CORE-V1"
    model_b_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    paired_experiment_evidence: VerifiedPairedExperimentEvidence
    model_a_provenance: VerifiedPublicRun
    model_b_provenance: VerifiedPublicRun
    model_a_aggregate: AggregateRankMetrics
    model_b_aggregate: AggregateRankMetrics
    top_1: ScalarMetricDelta
    top_3: ScalarMetricDelta
    top_5: ScalarMetricDelta
    mean_reciprocal_rank: ScalarMetricDelta
    mean_midrank: ScalarMetricDelta
    mean_percentile: ScalarMetricDelta
    outcomes: PairedOutcomeCounts
    model_a_failure_counts: dict[str, int]
    model_b_failure_counts: dict[str, int]
    model_a_tied_case_count: int = Field(ge=0)
    model_b_tied_case_count: int = Field(ge=0)
    cases: tuple[PairedCaseResult, ...] = Field(min_length=1)
    restoration_differences: tuple[RestorationDifference, ...]
    ablation_differences: tuple[AblationDifference, ...]
    chance_calendar_baseline: ChanceCalendarBaseline
    assignment_scope: Literal["discovery_only"] = "discovery_only"
    holdout_status: Literal["frozen-withheld-not-evaluated"] = "frozen-withheld-not-evaluated"
    claim_boundary: Literal[
        "synthetic-engineering-discovery-only-not-holdout-or-human-validation"
    ] = "synthetic-engineering-discovery-only-not-holdout-or-human-validation"
    score_semantics: Literal["rubric-bits-not-probabilities"] = "rubric-bits-not-probabilities"

    @field_validator("created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("comparison timestamp must be timezone-aware")
        return value.astimezone(UTC)


def _canonical_object(path: Path, label: str) -> dict[str, Any]:
    try:
        raw = load_json_bytes(path, require_canonical=True)
    except (OSError, ValueError) as exc:
        raise PairedModelComparisonError(f"invalid canonical {label}: {path}") from exc
    if not isinstance(raw, dict):
        raise PairedModelComparisonError(f"{label} must be a JSON object")
    return raw


def _require_sha_map(value: object, label: str) -> dict[str, str]:
    if not isinstance(value, dict) or not value:
        raise PairedModelComparisonError(f"{label} must be a nonempty hash map")
    result: dict[str, str] = {}
    for raw_name, raw_digest in value.items():
        if (
            not isinstance(raw_name, str)
            or not raw_name
            or not isinstance(raw_digest, str)
            or len(raw_digest) != 64
            or any(character not in "0123456789abcdef" for character in raw_digest)
        ):
            raise PairedModelComparisonError(f"{label} contains an invalid SHA-256 binding")
        result[raw_name] = raw_digest
    return dict(sorted(result.items()))


def _blind_constraints(blind: Mapping[str, Any]) -> tuple[BlindCaseConstraint, ...]:
    cases = blind.get("cases")
    if not isinstance(cases, list) or not cases:
        raise PairedModelComparisonError("blind input contains no cases")
    output: list[BlindCaseConstraint] = []
    seen: set[str] = set()
    for raw in cases:
        if not isinstance(raw, dict):
            raise PairedModelComparisonError("blind input contains a non-object case")
        try:
            constraint = BlindCaseConstraint.model_validate(
                {
                    "case_id": raw.get("case_id"),
                    "candidate_universe": raw.get("candidate_universe"),
                    "known_birth_year": raw.get("known_birth_year"),
                    "known_birth_month": raw.get("known_birth_month"),
                    "known_birth_day": raw.get("known_birth_day"),
                    "iana_timezone": raw.get("iana_timezone"),
                }
            )
        except ValidationError as exc:
            raise PairedModelComparisonError("invalid known-month blind case constraint") from exc
        if constraint.case_id in seen:
            raise PairedModelComparisonError(f"duplicate blind case {constraint.case_id}")
        seen.add(constraint.case_id)
        output.append(constraint)
    return tuple(sorted(output, key=lambda item: item.case_id))


def _recovery_settings(manifest: RunManifest, *, is_v2: bool) -> RecoverySettingsBinding:
    payload = manifest.config_payload
    if not isinstance(payload, dict):
        raise PairedModelComparisonError("run manifest lacks exact recovery settings")
    common = {"aggregation", "threshold_rubric_bits", "workers", "cache_policy"}
    allowed = common | {"paired_experiment"} | ({"model_b_v2_difference_gate"} if is_v2 else set())
    if set(payload) != allowed:
        raise PairedModelComparisonError("run manifest has missing or unexpected recovery fields")
    try:
        settings = RecoverySettingsBinding.model_validate({name: payload[name] for name in common})
    except ValidationError as exc:
        raise PairedModelComparisonError("invalid recovery settings") from exc
    if settings.aggregation != manifest.aggregation_rule:
        raise PairedModelComparisonError("manifest aggregation fields disagree")
    if not math.isfinite(settings.threshold_rubric_bits):
        raise PairedModelComparisonError("recovery threshold must be finite")
    return settings


def _parse_utc(value: object, label: str) -> datetime:
    if not isinstance(value, str):
        raise PairedModelComparisonError(f"{label} is missing")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PairedModelComparisonError(f"{label} is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise PairedModelComparisonError(f"{label} must be timezone-aware")
    return parsed.astimezone(UTC)


def _canonical_date(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise PairedModelComparisonError(f"{label} must be a canonical local date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise PairedModelComparisonError(f"{label} must be a canonical local date") from exc
    if parsed.isoformat() != value:
        raise PairedModelComparisonError(f"{label} must use YYYY-MM-DD form")
    return value


def _expected_calendar_dates(constraint: BlindCaseConstraint) -> tuple[str, ...]:
    count = calendar.monthrange(constraint.known_birth_year, constraint.known_birth_month)[1]
    return tuple(
        f"{constraint.known_birth_year:04d}-{constraint.known_birth_month:02d}-{day:02d}"
        for day in range(1, count + 1)
    )


def _stage_metrics(
    *,
    case_id: str,
    stage_label: str,
    stage: object,
    true_date: str,
    constraint: BlindCaseConstraint,
) -> CaseRankMetrics:
    if not isinstance(stage, dict):
        raise PairedModelComparisonError(f"case {case_id} {stage_label} must be an object")
    ranked_dates = stage.get("ranked_dates")
    if not isinstance(ranked_dates, list) or not ranked_dates:
        raise PairedModelComparisonError(f"case {case_id} {stage_label} lacks ranked_dates")
    observed_dates: list[str] = []
    for index, candidate in enumerate(ranked_dates):
        if not isinstance(candidate, dict):
            raise PairedModelComparisonError(
                f"case {case_id} {stage_label}.ranked_dates[{index}] is invalid"
            )
        observed_dates.append(
            _canonical_date(
                candidate.get("local_date"),
                f"case {case_id} {stage_label}.ranked_dates[{index}].local_date",
            )
        )
        raw_score = candidate.get("date_score")
        if isinstance(raw_score, bool) or not isinstance(raw_score, (int, float)):
            raise PairedModelComparisonError(
                f"case {case_id} {stage_label}.ranked_dates[{index}] lacks a numeric score"
            )
        if not math.isfinite(float(raw_score)):
            raise PairedModelComparisonError(
                f"case {case_id} {stage_label}.ranked_dates[{index}] score is not finite"
            )
    expected_dates = _expected_calendar_dates(constraint)
    if len(observed_dates) != len(set(observed_dates)):
        raise PairedModelComparisonError(
            f"case {case_id} {stage_label} contains duplicate candidate dates"
        )
    if set(observed_dates) != set(expected_dates):
        raise PairedModelComparisonError(
            f"case {case_id} {stage_label} is not the exact known-month universe"
        )
    try:
        return evaluate_ranked_case(
            case_id=case_id,
            candidates=ranked_dates,
            true_candidate_id=true_date,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise PairedModelComparisonError(
            f"case {case_id} {stage_label} ranking is invalid"
        ) from exc


def _authenticated_local_dates(
    evaluation: EvaluationReport,
    reveal: RevealRecord,
    case_ids: tuple[str, ...],
) -> dict[str, str]:
    if evaluation.evaluation_target != "local_date" or evaluation.rectification_cases:
        raise PairedModelComparisonError("paired comparison requires local-date evaluation")
    if len(evaluation.cases) != len(case_ids):
        raise PairedModelComparisonError(
            "every paired case needs a publicly revealed local date for recomputation"
        )
    dates: dict[str, str] = {}
    for item in evaluation.cases:
        if item.case_id in dates:
            raise PairedModelComparisonError("evaluation contains duplicate public case dates")
        dates[item.case_id] = _canonical_date(
            item.true_candidate_id,
            f"evaluation case {item.case_id} true local date",
        )
    if set(dates) != set(case_ids):
        raise PairedModelComparisonError(
            "evaluation public local-date identities differ from blind cases"
        )
    try:
        observed_hash = revealed_local_date_set_hash(
            {case_id: {"true_local_date": true_date} for case_id, true_date in dates.items()}
        )
    except ValueError as exc:
        raise PairedModelComparisonError("invalid revealed local-date identity") from exc
    if observed_hash != reveal.revealed_local_date_set_sha256:
        raise PairedModelComparisonError(
            "public case/date identities do not match the authenticated reveal-v3 commitment"
        )
    return dates


def _recompute_known_month_evaluation(
    *,
    predictions: Mapping[str, Any],
    constraints: tuple[BlindCaseConstraint, ...],
    true_dates: Mapping[str, str],
) -> RecomputedKnownMonthEvaluation:
    raw_cases = predictions.get("predictions")
    if not isinstance(raw_cases, list):
        raise PairedModelComparisonError("predictions contain no case list")
    predicted_cases: dict[str, dict[str, Any]] = {}
    for raw in raw_cases:
        if not isinstance(raw, dict) or not isinstance(raw.get("case_id"), str):
            raise PairedModelComparisonError("predictions contain an invalid case")
        case_id = raw["case_id"]
        if case_id in predicted_cases:
            raise PairedModelComparisonError(f"duplicate prediction case {case_id}")
        predicted_cases[case_id] = raw
    constraints_by_case = {item.case_id: item for item in constraints}
    if set(predicted_cases) != set(constraints_by_case) or set(true_dates) != set(
        constraints_by_case
    ):
        raise PairedModelComparisonError("prediction, blind, and revealed case sets differ")

    case_metrics: list[CaseRankMetrics] = []
    failures: list[FailureRecord] = []
    curves: list[CurveObservation] = []
    ablations: list[LeaveOneClusterOutObservation] = []
    for case_id in sorted(constraints_by_case):
        predicted = predicted_cases[case_id]
        constraint = constraints_by_case[case_id]
        true_date = true_dates[case_id]
        if true_date not in _expected_calendar_dates(constraint):
            raise PairedModelComparisonError(
                f"case {case_id} revealed date is outside its blind month"
            )
        candidate_universe = predicted.get("candidate_universe", "known_month")
        if candidate_universe != "known_month":
            raise PairedModelComparisonError(
                f"case {case_id} prediction is not a known-month result"
            )
        unresolved = predicted.get("unresolved_mapping_ids", [])
        if (
            not isinstance(unresolved, list)
            or not all(isinstance(item, str) and item for item in unresolved)
            or len(unresolved) != len(set(unresolved))
        ):
            raise PairedModelComparisonError(f"case {case_id} has invalid unresolved_mapping_ids")

        metrics = _stage_metrics(
            case_id=case_id,
            stage_label="final",
            stage=predicted,
            true_date=true_date,
            constraint=constraint,
        )
        case_metrics.append(metrics)
        variants = predicted.get("aggregation_variants", {})
        if not isinstance(variants, dict):
            raise PairedModelComparisonError(f"case {case_id} has invalid aggregation_variants")
        if metrics.best_rank != 1:
            best_state_metrics: CaseRankMetrics | None = None
            if "best_state" in variants:
                best_state_metrics = _stage_metrics(
                    case_id=case_id,
                    stage_label="aggregation_variants.best_state",
                    stage=variants["best_state"],
                    true_date=true_date,
                    constraint=constraint,
                )
            failures.append(
                classify_oracle_failure(
                    case_id=case_id,
                    true_candidate_present=True,
                    unresolved_mapping_ids=tuple(unresolved),
                    state_winner_but_date_loser=(
                        best_state_metrics is not None and best_state_metrics.best_rank == 1
                    ),
                    evidence={"best_rank": metrics.best_rank, "midrank": metrics.midrank},
                )
            )

        zero_metrics = _stage_metrics(
            case_id=case_id,
            stage_label="zero_cluster",
            stage=predicted.get("zero_cluster"),
            true_date=true_date,
            constraint=constraint,
        )
        for method in ("random", "active"):
            curves.append(
                CurveObservation(
                    case_id=case_id,
                    method=method,
                    cluster_count=0,
                    midrank=zero_metrics.midrank,
                    candidate_count=zero_metrics.candidate_count,
                    tie_size=zero_metrics.tie_size,
                )
            )

        for field, method in (
            ("random_restoration", "random"),
            ("active_restoration", "active"),
        ):
            restoration = predicted.get(field)
            if not isinstance(restoration, list):
                raise PairedModelComparisonError(f"case {case_id} has invalid {field}")
            seen_counts: set[int] = set()
            for point in restoration:
                if not isinstance(point, dict):
                    raise PairedModelComparisonError(f"case {case_id} has invalid {field} point")
                cluster_count = point.get("cluster_count")
                if (
                    isinstance(cluster_count, bool)
                    or not isinstance(cluster_count, int)
                    or cluster_count < 1
                    or cluster_count in seen_counts
                ):
                    raise PairedModelComparisonError(
                        f"case {case_id} has invalid {field} cluster count"
                    )
                seen_counts.add(cluster_count)
                stage_metrics = _stage_metrics(
                    case_id=case_id,
                    stage_label=f"{field} step",
                    stage=point,
                    true_date=true_date,
                    constraint=constraint,
                )
                curves.append(
                    CurveObservation(
                        case_id=case_id,
                        method=cast(Literal["random", "active", "leave_one_out"], method),
                        cluster_count=cluster_count,
                        midrank=stage_metrics.midrank,
                        candidate_count=stage_metrics.candidate_count,
                        tie_size=stage_metrics.tie_size,
                    )
                )

        leave_one_out = predicted.get("leave_one_cluster_out")
        if not isinstance(leave_one_out, list):
            raise PairedModelComparisonError(f"case {case_id} has invalid leave_one_cluster_out")
        seen_clusters: set[str] = set()
        for point in leave_one_out:
            if not isinstance(point, dict):
                raise PairedModelComparisonError(
                    f"case {case_id} has invalid leave_one_cluster_out point"
                )
            cluster_id = point.get("cluster_id")
            if not isinstance(cluster_id, str) or not cluster_id or cluster_id in seen_clusters:
                raise PairedModelComparisonError(
                    f"case {case_id} has invalid leave-one-out cluster"
                )
            seen_clusters.add(cluster_id)
            ablated = _stage_metrics(
                case_id=case_id,
                stage_label="leave_one_cluster_out step",
                stage=point,
                true_date=true_date,
                constraint=constraint,
            )
            ablations.append(
                LeaveOneClusterOutObservation(
                    case_id=case_id,
                    cluster_id=cluster_id,
                    full_midrank=metrics.midrank,
                    ablated_midrank=ablated.midrank,
                )
            )

    observed_counts = Counter(item.classification.value for item in failures)
    failure_counts = {
        classification.value: observed_counts[classification.value]
        for classification in FailureClassification
    }
    return RecomputedKnownMonthEvaluation(
        aggregate=aggregate_rank_metrics(case_metrics, total_case_count=len(constraints_by_case)),
        cases=tuple(case_metrics),
        failures=tuple(failures),
        failure_counts=dict(sorted(failure_counts.items())),
        restoration_curves=aggregate_restoration_curves(curves),
        leave_one_cluster_out=aggregate_leave_one_cluster_out(ablations),
    )


def _validate_isolation_receipt(
    receipt: Mapping[str, Any],
    *,
    model_id: str,
    blind_sha256: str,
    manifest: RunManifest,
    manifest_sha256: str,
    prediction_sha256: str,
    predictions: Mapping[str, Any],
    question_bank_sha256: str,
) -> tuple[dict[str, str], dict[str, str], str, datetime]:
    if receipt.get("schema_version") != "keyless-recovery-isolation-receipt-v1":
        raise PairedModelComparisonError("missing claim-grade keyless recovery receipt")
    controls = receipt.get("runtime_controls")
    required_controls = {
        "network_namespace": "unshared",
        "user_namespace": "unshared-uid-gid-65534",
        "nested_user_namespaces": "disabled",
        "capabilities": "all-dropped",
        "evaluator_secret_mounts": "absent",
        "reveal_or_key_cli_surface": False,
    }
    if not isinstance(controls, dict) or any(
        controls.get(name) != expected for name, expected in required_controls.items()
    ):
        raise PairedModelComparisonError("keyless isolation runtime controls are incomplete")
    runtime = receipt.get("isolation_runtime")
    if (
        not isinstance(runtime, dict)
        or runtime.get("name") != "bubblewrap"
        or not isinstance(runtime.get("version"), str)
        or not runtime.get("version")
        or not isinstance(runtime.get("executable_sha256"), str)
        or len(runtime["executable_sha256"]) != 64
        or any(character not in "0123456789abcdef" for character in runtime["executable_sha256"])
    ):
        raise PairedModelComparisonError("Bubblewrap runtime identity is incomplete")
    mounts = receipt.get("mount_contract")
    required_mounts = {
        "tracked_decoder_source": "read-only",
        "python_environment": "read-only",
        "blind_input": "read-only-single-file",
        "mapping_artifact": "read-only-single-file",
        "question_bank_artifact": "read-only-single-file",
        "ephemeris": "read-only-declared-se1-files",
        "candidate_cache": "read-only-declared-month-files",
        "run_output": "read-write-single-directory",
        "host_parent_directories": "absent",
        "evaluator_key_plaintext_envelope": "absent",
        "paired_plan": "read-only-single-file",
        "paired_public_config": "read-only-single-file",
        "paired_generation_receipt": "read-only-single-file",
        "paired_generation_binding": "read-only-single-file",
    }
    if not isinstance(mounts, dict) or any(
        mounts.get(name) != expected for name, expected in required_mounts.items()
    ):
        raise PairedModelComparisonError("keyless isolation mount contract is incomplete")
    if model_id == MODEL_B_V2_NEW_ID:
        v2_mounts = {
            "model_b_v2_compiled_artifact": "read-only-single-file",
            "model_b_v2_freeze_receipt": "read-only-single-file",
            "model_b_v2_difference_audit": "read-only-single-file",
            "model_b_v2_difference_cache": "read-only-single-file",
        }
        if any(mounts.get(name) != expected for name, expected in v2_mounts.items()):
            raise PairedModelComparisonError("V2 public mounts are incomplete")
    command = receipt.get("command_contract")
    if (
        not isinstance(command, dict)
        or command.get("entrypoint") != "python -m hdmatch.cli recover"
        or command.get("exit_status") != 0
        or command.get("key_or_reveal_arguments") is not False
    ):
        raise PairedModelComparisonError("keyless recovery command contract is invalid")
    settings = _recovery_settings(manifest, is_v2=model_id == MODEL_B_V2_NEW_ID)
    for name, expected in {
        "workers": settings.workers,
        "aggregation": settings.aggregation,
        "threshold_rubric_bits": settings.threshold_rubric_bits,
    }.items():
        if command.get(name) != expected:
            raise PairedModelComparisonError(f"isolation receipt {name} differs from manifest")
    direct = {
        "model_id": model_id,
        "blind_input_sha256": blind_sha256,
        "question_bank_sha256": question_bank_sha256,
        "run_manifest_sha256": manifest_sha256,
        "prediction_sha256": prediction_sha256,
        "software_commit": manifest.software_commit,
    }
    for name, expected in direct.items():
        if receipt.get(name) != expected:
            raise PairedModelComparisonError(f"isolation receipt {name} is mismatched")
    paired_isolation = {
        "paired_plan_sha256": manifest.input_hashes.get("paired_experiment_plan"),
        "paired_public_config_sha256": manifest.input_hashes.get("paired_public_config"),
        "paired_generation_receipt_sha256": manifest.input_hashes.get("paired_generation_receipt"),
        "paired_generation_binding_sha256": manifest.input_hashes.get("paired_generation_binding"),
    }
    if any(receipt.get(name) != expected for name, expected in paired_isolation.items()):
        raise PairedModelComparisonError("isolation paired artifact hashes are mismatched")
    if receipt.get("claim_boundary") != (
        "OS-isolated synthetic engineering recovery only; this does not validate "
        "Human Design in humans"
    ):
        raise PairedModelComparisonError("isolation claim boundary is invalid")
    if receipt.get("mapping_sha256") != manifest.input_hashes.get("model_a_mapping_library"):
        raise PairedModelComparisonError("isolation Model A base mapping is mismatched")
    ephemeris = _require_sha_map(receipt.get("ephemeris_sha256"), "ephemeris hashes")
    manifest_ephemeris = {
        name.removeprefix("ephemeris:"): digest
        for name, digest in manifest.input_hashes.items()
        if name.startswith("ephemeris:")
    }
    if ephemeris != dict(sorted(manifest_ephemeris.items())):
        raise PairedModelComparisonError("isolation ephemeris hashes differ from manifest")
    cache = _require_sha_map(receipt.get("candidate_cache_sha256"), "candidate cache hashes")
    prediction_cache = _require_sha_map(
        predictions.get("candidate_cache_sha256"), "prediction candidate cache hashes"
    )
    if cache != prediction_cache:
        raise PairedModelComparisonError("isolation and prediction cache hashes differ")
    software_tree = receipt.get("software_tree")
    if (
        not isinstance(software_tree, str)
        or len(software_tree) != 40
        or any(character not in "0123456789abcdef" for character in software_tree)
    ):
        raise PairedModelComparisonError("isolation source-tree identity is invalid")
    created = _parse_utc(receipt.get("created_at_utc"), "isolation receipt timestamp")
    return ephemeris, cache, software_tree, created


def load_verified_public_run(
    run_dir: str | Path,
    *,
    expected_model_id: Literal["MODEL-A-CORE-V1", "MODEL-B-DETAILED-V2-NEW"],
) -> VerifiedPublicRun:
    """Verify one already-revealed public run without opening or decrypting its key."""

    directory = Path(run_dir)
    blind_path = directory / "blind_cases.json"
    manifest_path = directory / "run.manifest.json"
    prediction_path = directory / "predictions.json"
    freeze_path = directory / "prediction.freeze.json"
    reveal_path = directory / "answer-key.reveal.json"
    evaluation_path = directory / "evaluation.json"
    generation_path = directory / "generation.receipt.json"
    isolation_path = directory / "keyless-isolation.receipt.json"

    blind = _canonical_object(blind_path, "blind input")
    predictions = _canonical_object(prediction_path, "predictions")
    generation = _canonical_object(generation_path, "generation receipt")
    isolation = _canonical_object(isolation_path, "keyless isolation receipt")
    try:
        manifest = load_run_manifest(manifest_path)
        evaluation = EvaluationReport.model_validate(
            load_json_bytes(evaluation_path, require_canonical=True)
        )
    except (OSError, ValueError, ValidationError) as exc:
        raise PairedModelComparisonError("invalid manifest or evaluation report") from exc

    blind_sha256 = sha256_file(blind_path)
    if blind.get("schema_version") != "blind-synthetic-v1":
        raise PairedModelComparisonError("unsupported blind input schema")
    if blind.get("generator") != "frozen-chart-to-response-model":
        raise PairedModelComparisonError("unsupported synthetic generator")
    if blind.get("candidate_universe") != "known_month":
        raise PairedModelComparisonError("paired comparison requires known-month runs")
    if blind.get("noise_tier") != NoiseTier.ORACLE.value or blind.get(
        "noise_parameters"
    ) != noise_parameters_payload(NoiseTier.ORACLE):
        raise PairedModelComparisonError("paired comparison requires the frozen oracle tier")
    if blind.get("model_id") != expected_model_id:
        raise PairedModelComparisonError("blind input has the wrong model identity")
    constraints = _blind_constraints(blind)
    case_ids = tuple(item.case_id for item in constraints)

    for name, expected in {
        "experiment_id": blind.get("experiment_id"),
        "model_id": expected_model_id,
        "blind_input_sha256": blind_sha256,
        "model_sha256": blind.get("model_sha256"),
        "question_bank_sha256": blind.get("question_bank_sha256"),
        "mapping_sha256": blind.get("mapping_sha256"),
    }.items():
        if predictions.get(name) != expected:
            raise PairedModelComparisonError(f"predictions {name} differs from blind input")
    prediction_cases = predictions.get("predictions")
    if not isinstance(prediction_cases, list):
        raise PairedModelComparisonError("prediction case IDs differ from blind input")
    prediction_case_ids: list[str] = []
    for item in prediction_cases:
        if not isinstance(item, dict) or not isinstance(item.get("case_id"), str):
            raise PairedModelComparisonError("prediction case IDs differ from blind input")
        prediction_case_ids.append(item["case_id"])
    if tuple(sorted(prediction_case_ids)) != case_ids:
        raise PairedModelComparisonError("prediction case IDs differ from blind input")

    if manifest.software_dirty:
        raise PairedModelComparisonError("paired comparison requires a clean recovery manifest")
    if manifest.experiment_id != blind.get("experiment_id"):
        raise PairedModelComparisonError("manifest experiment differs from blind input")
    if manifest.model_id != expected_model_id:
        raise PairedModelComparisonError("manifest has the wrong model identity")
    if manifest.candidate_universe != "known_month":
        raise PairedModelComparisonError("manifest candidate universe is not known-month")
    if manifest.input_hashes.get("blind_cases.json") != blind_sha256:
        raise PairedModelComparisonError("manifest does not bind the blind input")
    if manifest.seed != int(blind_sha256[:16], 16):
        raise PairedModelComparisonError("manifest public recovery seed is invalid")
    settings = _recovery_settings(manifest, is_v2=expected_model_id == MODEL_B_V2_NEW_ID)

    bindings = ArtifactBindings(
        blind_input_sha256=blind_sha256,
        model_sha256=str(blind.get("model_sha256", "")),
        question_bank_sha256=str(blind.get("question_bank_sha256", "")),
        mapping_sha256=str(blind.get("mapping_sha256", "")),
    )
    try:
        freeze = verify_frozen_predictions(
            directory,
            freeze_path=freeze_path,
            expected_bindings=bindings,
            expected_experiment_id=str(blind.get("experiment_id", "")),
            run_manifest_path=manifest_path,
            require_run_manifest=True,
        )
        reveal = verify_reveal_record(
            directory,
            freeze=freeze,
            freeze_path=freeze_path,
            reveal_record_path=reveal_path,
        )
    except (ValueError, FreezeVerificationError) as exc:
        raise PairedModelComparisonError("invalid prediction/freeze/reveal chain") from exc
    if (
        reveal.schema_version != "answer-key-reveal-v3"
        or reveal.revealed_target_set_sha256 is None
        or reveal.revealed_local_date_set_sha256 is None
        or reveal.generation_seed_commitment_sha256 is None
        or reveal.paired_prediction_freeze_sha256 is None
        or reveal.paired_plan_sha256 is None
        or reveal.paired_arm_id is None
    ):
        raise PairedModelComparisonError(
            "paired comparison requires authenticated answer-key reveal v3 commitments"
        )
    _validate_evaluation_chain(
        evaluation,
        freeze=freeze,
        reveal=reveal,
        manifest=manifest,
        manifest_path=manifest_path,
        freeze_path=freeze_path,
        reveal_path=reveal_path,
    )

    if generation.get("schema_version") != "generation-receipt-v1":
        raise PairedModelComparisonError("unsupported generation receipt")
    generation_direct = {
        "experiment_id": blind.get("experiment_id"),
        "model_id": expected_model_id,
        "blind_input_sha256": blind_sha256,
        "encrypted_answer_key_sha256": reveal.encrypted_answer_key_sha256,
        "model_sha256": blind.get("model_sha256"),
        "question_bank_sha256": blind.get("question_bank_sha256"),
        "mapping_sha256": blind.get("mapping_sha256"),
        "case_count": len(case_ids),
        "seed_status": "sealed-in-answer-key-only",
        "claim_boundary": "synthetic-engineering-validation-only",
    }
    for name, expected in generation_direct.items():
        if generation.get(name) != expected:
            raise PairedModelComparisonError(f"generation receipt {name} is mismatched")
    public_config_sha256 = generation.get("public_config_sha256")
    if not isinstance(public_config_sha256, str) or len(public_config_sha256) != 64:
        raise PairedModelComparisonError("generation receipt lacks public config binding")
    generation_started = _parse_utc(
        generation.get("generation_started_at_utc"), "generation start timestamp"
    )
    if generation_started > manifest.created_at_utc:
        raise PairedModelComparisonError("recovery manifest predates synthetic generation")

    ephemeris, candidate_cache, isolation_tree, isolation_created = _validate_isolation_receipt(
        isolation,
        model_id=expected_model_id,
        blind_sha256=blind_sha256,
        manifest=manifest,
        manifest_sha256=sha256_file(manifest_path),
        prediction_sha256=sha256_file(prediction_path),
        predictions=predictions,
        question_bank_sha256=str(blind.get("question_bank_sha256", "")),
    )
    if not (manifest.created_at_utc <= isolation_created <= freeze.created_at_utc):
        raise PairedModelComparisonError("isolation receipt timestamp is out of order")

    true_dates = _authenticated_local_dates(evaluation, reveal, case_ids)
    recomputed = _recompute_known_month_evaluation(
        predictions=predictions,
        constraints=constraints,
        true_dates=true_dates,
    )

    capabilities = blind.get("model_capabilities")
    if not isinstance(capabilities, dict) or predictions.get("model_capabilities") != capabilities:
        raise PairedModelComparisonError("model capabilities are absent or inconsistent")
    difference_gate: dict[str, Any] | None = None
    if expected_model_id == MODEL_B_V2_NEW_ID:
        if (
            capabilities.get("assignment_scope") != "discovery_only"
            or capabilities.get("holdout") != "frozen-withheld"
            or capabilities.get("scientific_claim")
            != "engineering-discovery-only-not-holdout-validation"
        ):
            raise PairedModelComparisonError("V2 runtime is not frozen discovery-only")
        raw_gate = blind.get("model_b_v2_difference_gate")
        if not isinstance(raw_gate, dict):
            raise PairedModelComparisonError("V2 blind input lacks its verified difference gate")
        if (
            predictions.get("model_b_v2_difference_gate") != raw_gate
            or manifest.config_payload is None
            or manifest.config_payload.get("model_b_v2_difference_gate") != raw_gate
            or generation.get("model_b_v2_difference_gate") != raw_gate
            or isolation.get("model_b_v2_difference_gate") != raw_gate
        ):
            raise PairedModelComparisonError("V2 difference-gate binding is inconsistent")
        v2_receipt_hashes = {
            "model_b_v2_compiled_sha256": manifest.input_hashes.get("model_b_v2_compiled_artifact"),
            "model_b_v2_freeze_sha256": manifest.input_hashes.get("model_b_v2_freeze_receipt"),
            "model_b_v2_difference_audit_sha256": raw_gate.get("audit_file_sha256"),
            "model_b_v2_difference_cache_sha256": raw_gate.get("candidate_cache_file_sha256"),
        }
        if any(isolation.get(name) != expected for name, expected in v2_receipt_hashes.items()):
            raise PairedModelComparisonError("V2 isolation artifact hashes are inconsistent")
        audited_at = _parse_utc(raw_gate.get("audited_at_utc"), "difference audit timestamp")
        if audited_at > generation_started:
            raise PairedModelComparisonError("V2 generation predates its difference audit")
        difference_gate = raw_gate
    elif "model_b_v2_difference_gate" in blind:
        raise PairedModelComparisonError("Model A blind input contains a V2 difference gate")

    return VerifiedPublicRun(
        model_id=expected_model_id,
        experiment_id=str(blind["experiment_id"]),
        run_manifest=manifest,
        recomputed_evaluation=recomputed,
        model_sha256=freeze.model_sha256,
        mapping_sha256=freeze.mapping_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        blind_input_sha256=blind_sha256,
        prediction_sha256=sha256_file(prediction_path),
        freeze_sha256=sha256_file(freeze_path),
        reveal_sha256=sha256_file(reveal_path),
        evaluation_sha256=sha256_file(evaluation_path),
        encrypted_answer_key_sha256=reveal.encrypted_answer_key_sha256,
        generation_receipt_sha256=sha256_file(generation_path),
        isolation_receipt_sha256=sha256_file(isolation_path),
        public_config_sha256=public_config_sha256,
        generation_started_at_utc=generation_started,
        evaluation_created_at_utc=evaluation.created_at_utc,
        reveal_created_at_utc=reveal.revealed_at_utc,
        revealed_target_set_sha256=reveal.revealed_target_set_sha256,
        revealed_local_date_set_sha256=reveal.revealed_local_date_set_sha256,
        generation_seed_commitment_sha256=(reveal.generation_seed_commitment_sha256),
        paired_prediction_freeze_sha256=reveal.paired_prediction_freeze_sha256,
        paired_plan_sha256=reveal.paired_plan_sha256,
        paired_arm_id=reveal.paired_arm_id,
        case_ids=case_ids,
        candidate_constraints=constraints,
        candidate_constraints_sha256=sha256_json(constraints),
        ephemeris_sha256=ephemeris,
        candidate_cache_sha256=candidate_cache,
        isolation_software_tree=isolation_tree,
        recovery_settings=settings,
        model_capabilities=capabilities,
        difference_gate=difference_gate,
    )


def _validate_evaluation_chain(
    evaluation: EvaluationReport,
    *,
    freeze: FreezeRecord,
    reveal: RevealRecord,
    manifest: RunManifest,
    manifest_path: Path,
    freeze_path: Path,
    reveal_path: Path,
) -> None:
    expected: dict[str, object] = {
        "experiment_id": freeze.experiment_id,
        "prediction_sha256": freeze.prediction_sha256,
        "freeze_sha256": sha256_file(freeze_path),
        "reveal_sha256": sha256_file(reveal_path),
        "run_manifest_sha256": sha256_file(manifest_path),
        "encrypted_answer_key_file": reveal.encrypted_answer_key_file,
        "encrypted_answer_key_sha256": reveal.encrypted_answer_key_sha256,
        "answer_key_payload_sha256": reveal.answer_key_payload_sha256,
        "blind_input_sha256": freeze.blind_input_sha256,
        "model_sha256": freeze.model_sha256,
        "question_bank_sha256": freeze.question_bank_sha256,
        "mapping_sha256": freeze.mapping_sha256,
        "revealed_target_set_sha256": reveal.revealed_target_set_sha256,
        "revealed_local_date_set_sha256": reveal.revealed_local_date_set_sha256,
        "generation_seed_commitment_sha256": (reveal.generation_seed_commitment_sha256),
        "claim_boundary": "synthetic-engineering-validation-only",
        "score_semantics": "rubric-bits-not-probabilities",
        "evaluation_target": "local_date",
    }
    for name, value in expected.items():
        if getattr(evaluation, name) != value:
            raise PairedModelComparisonError(f"evaluation {name} differs from provenance chain")
    if not (
        manifest.created_at_utc
        <= freeze.created_at_utc
        <= reveal.revealed_at_utc
        <= evaluation.created_at_utc
    ):
        raise PairedModelComparisonError(
            "manifest/freeze/reveal/evaluation timestamps are reversed"
        )


def _delta(model_a: float | None, model_b: float | None) -> ScalarMetricDelta:
    return ScalarMetricDelta(
        model_a=model_a,
        model_b=model_b,
        b_minus_a=(None if model_a is None or model_b is None else model_b - model_a),
    )


def _metrics_by_case(
    report: RecomputedKnownMonthEvaluation,
) -> dict[str, CaseRankMetrics]:
    result = {item.case_id: item for item in report.cases}
    if len(result) != len(report.cases):
        raise PairedModelComparisonError("evaluation contains duplicate case metrics")
    return result


def _failures_by_case(
    report: RecomputedKnownMonthEvaluation,
) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for failure in report.failures:
        grouped.setdefault(failure.case_id, []).append(failure.classification.value)
    observed = Counter(item for values in grouped.values() for item in values)
    declared = {name: count for name, count in report.failure_counts.items() if count}
    if dict(sorted(observed.items())) != dict(sorted(declared.items())):
        raise PairedModelComparisonError("evaluation failure counts are inconsistent")
    return {name: tuple(sorted(values)) for name, values in grouped.items()}


def load_verified_paired_experiment_evidence(
    *,
    paired_plan_path: str | Path,
    public_config_path: str | Path,
    model_a_generation_binding_path: str | Path,
    model_b_generation_binding_path: str | Path,
    model_a_generation_receipt_path: str | Path,
    model_b_generation_receipt_path: str | Path,
    paired_prediction_freeze_path: str | Path,
    model_a_run_dir: str | Path,
    model_b_run_dir: str | Path,
) -> VerifiedPairedExperimentEvidence:
    """Verify the public paired plan and both exact generation-receipt bindings."""

    try:
        plan = load_paired_experiment_plan(paired_plan_path)
        by_role = {arm.role: arm for arm in plan.arms}
        if set(by_role) != {"model_a", "model_b_v2"}:
            raise PairedExperimentBindingError("paired plan lacks the required model roles")
        model_a_binding = verify_paired_generation_receipt_binding(
            model_a_generation_binding_path,
            plan_path=paired_plan_path,
            public_config_path=public_config_path,
            generation_receipt_path=model_a_generation_receipt_path,
            expected_arm_id=by_role["model_a"].arm_id,
        )
        model_b_binding = verify_paired_generation_receipt_binding(
            model_b_generation_binding_path,
            plan_path=paired_plan_path,
            public_config_path=public_config_path,
            generation_receipt_path=model_b_generation_receipt_path,
            expected_arm_id=by_role["model_b_v2"].arm_id,
        )
        paired_freeze = verify_paired_prediction_freeze_receipt(
            paired_prediction_freeze_path,
            plan_path=paired_plan_path,
            public_config_path=public_config_path,
            arms=(
                PairedFreezeArmArtifacts(
                    role="model_a",
                    arm_id=by_role["model_a"].arm_id,
                    run_logical_label="model-a",
                    run_dir=Path(model_a_run_dir),
                    generation_receipt_path=Path(model_a_generation_receipt_path),
                    generation_binding_path=Path(model_a_generation_binding_path),
                    isolation_receipt_path=(
                        Path(model_a_run_dir) / "keyless-isolation.receipt.json"
                    ),
                ),
                PairedFreezeArmArtifacts(
                    role="model_b_v2",
                    arm_id=by_role["model_b_v2"].arm_id,
                    run_logical_label="model-b-v2",
                    run_dir=Path(model_b_run_dir),
                    generation_receipt_path=Path(model_b_generation_receipt_path),
                    generation_binding_path=Path(model_b_generation_binding_path),
                    isolation_receipt_path=(
                        Path(model_b_run_dir) / "keyless-isolation.receipt.json"
                    ),
                ),
            ),
        )
    except (OSError, ValueError, PairedExperimentBindingError) as exc:
        raise PairedModelComparisonError(
            "paired plan or generation-receipt binding is invalid"
        ) from exc
    return VerifiedPairedExperimentEvidence(
        plan=plan,
        plan_file_sha256=sha256_file(paired_plan_path),
        public_config_file_sha256=sha256_file(public_config_path),
        model_a_generation_binding=model_a_binding,
        model_a_generation_binding_file_sha256=sha256_file(model_a_generation_binding_path),
        model_b_generation_binding=model_b_binding,
        model_b_generation_binding_file_sha256=sha256_file(model_b_generation_binding_path),
        paired_prediction_freeze=paired_freeze,
        paired_prediction_freeze_file_sha256=sha256_file(paired_prediction_freeze_path),
    )


def _validate_run_against_plan(
    run: VerifiedPublicRun,
    *,
    role: Literal["model_a", "model_b_v2"],
    evidence: VerifiedPairedExperimentEvidence,
) -> None:
    plan = evidence.plan
    arms = tuple(arm for arm in plan.arms if arm.role == role)
    if len(arms) != 1:
        raise PairedModelComparisonError(f"paired plan has no unique {role} arm")
    arm = arms[0]
    binding = (
        evidence.model_a_generation_binding
        if role == "model_a"
        else evidence.model_b_generation_binding
    )
    expected = {
        "experiment ID": (run.experiment_id, plan.paired_experiment_id),
        "arm model ID": (run.model_id, arm.model_id),
        "arm model SHA": (run.model_sha256, arm.model_sha256),
        "arm mapping SHA": (run.mapping_sha256, arm.mapping_sha256),
        "arm question-bank SHA": (
            run.question_bank_sha256,
            arm.question_bank_sha256,
        ),
        "public config SHA": (
            run.public_config_sha256,
            plan.public_config.file.sha256,
        ),
        "seed commitment": (
            run.generation_seed_commitment_sha256,
            plan.generation_seed_commitment_sha256,
        ),
        "binding blind input SHA": (
            binding.blind_input_sha256,
            run.blind_input_sha256,
        ),
        "binding encrypted envelope SHA": (
            binding.encrypted_answer_key_sha256,
            run.encrypted_answer_key_sha256,
        ),
        "paired freeze SHA": (
            run.paired_prediction_freeze_sha256,
            evidence.paired_prediction_freeze_file_sha256,
        ),
        "paired reveal plan SHA": (
            run.paired_plan_sha256,
            evidence.plan_file_sha256,
        ),
        "paired reveal arm ID": (run.paired_arm_id, arm.arm_id),
    }
    for label, (recorded, planned) in expected.items():
        if recorded != planned:
            raise PairedModelComparisonError(f"{label} differs from paired plan")
    if binding.arm != arm:
        raise PairedModelComparisonError("paired generation binding has the wrong arm")
    if binding.generation_receipt.sha256 != run.generation_receipt_sha256:
        raise PairedModelComparisonError(
            "paired generation binding does not bind the current generation receipt"
        )
    if run.generation_started_at_utc < plan.planned_at_utc:
        raise PairedModelComparisonError("generation started before the paired plan")

    config = plan.public_config.payload
    if len(run.case_ids) != config.case_count:
        raise PairedModelComparisonError("run case count differs from paired public config")
    for constraint in run.candidate_constraints:
        if (
            constraint.known_birth_year < config.year_start
            or constraint.known_birth_year > config.year_end
            or constraint.known_birth_month != config.month
            or constraint.iana_timezone != config.timezone
        ):
            raise PairedModelComparisonError(
                "run candidate constraints differ from paired public config"
            )
    if role == "model_b_v2":
        if run.difference_gate != plan.verified_v2_audit.model_dump(mode="json"):
            raise PairedModelComparisonError("Model B V2 difference audit differs from paired plan")
        if (
            run.run_manifest.input_hashes.get("model_b_v2_compiled_artifact")
            != arm.compiled_file_sha256
            or run.run_manifest.input_hashes.get("model_b_v2_freeze_receipt")
            != arm.freeze_receipt_file_sha256
        ):
            raise PairedModelComparisonError(
                "Model B V2 compiled/freeze identities differ from paired plan"
            )


def _chance_baseline(cases: Sequence[PairedCaseResult]) -> ChanceCalendarBaseline:
    counts = [item.candidate_count for item in cases if item.candidate_count is not None]
    if len(counts) != len(cases):
        raise PairedModelComparisonError("chance baseline requires every candidate count")
    values = [int(value) for value in counts]
    return ChanceCalendarBaseline(
        top_1=statistics.fmean(1.0 / count for count in values),
        top_3=statistics.fmean(min(3, count) / count for count in values),
        top_5=statistics.fmean(min(5, count) / count for count in values),
        mean_reciprocal_rank=statistics.fmean(
            sum(1.0 / rank for rank in range(1, count + 1)) / count for count in values
        ),
        mean_midrank=statistics.fmean((count + 1.0) / 2.0 for count in values),
        mean_percentile=statistics.fmean(1.0 if count == 1 else 0.5 for count in values),
    )


def _restoration_differences(
    model_a: Sequence[CurvePoint], model_b: Sequence[CurvePoint]
) -> tuple[RestorationDifference, ...]:
    a = {(item.method, item.cluster_count): item for item in model_a}
    b = {(item.method, item.cluster_count): item for item in model_b}
    if len(a) != len(model_a) or len(b) != len(model_b):
        raise PairedModelComparisonError("duplicate restoration curve point")
    output: list[RestorationDifference] = []
    for method, count in sorted(set(a) | set(b)):
        left, right = a.get((method, count)), b.get((method, count))
        output.append(
            RestorationDifference(
                method=method,
                cluster_count=count,
                model_a=left,
                model_b=right,
                mean_midrank=_delta(
                    left.mean_midrank if left else None,
                    right.mean_midrank if right else None,
                ),
                mean_reciprocal_rank=_delta(
                    left.mean_reciprocal_rank if left else None,
                    right.mean_reciprocal_rank if right else None,
                ),
                top_1=_delta(left.top_1 if left else None, right.top_1 if right else None),
                top_3=_delta(left.top_3 if left else None, right.top_3 if right else None),
                top_5=_delta(left.top_5 if left else None, right.top_5 if right else None),
                tie_rate=_delta(left.tie_rate if left else None, right.tie_rate if right else None),
            )
        )
    return tuple(output)


def _ablation_differences(
    model_a: Sequence[ClusterAblationSummary],
    model_b: Sequence[ClusterAblationSummary],
) -> tuple[AblationDifference, ...]:
    a = {item.cluster_id: item for item in model_a}
    b = {item.cluster_id: item for item in model_b}
    if len(a) != len(model_a) or len(b) != len(model_b):
        raise PairedModelComparisonError("duplicate ablation cluster")
    return tuple(
        AblationDifference(
            cluster_id=cluster,
            model_a=a.get(cluster),
            model_b=b.get(cluster),
            mean_rank_change=_delta(
                a[cluster].mean_rank_change if cluster in a else None,
                b[cluster].mean_rank_change if cluster in b else None,
            ),
            median_rank_change=_delta(
                a[cluster].median_rank_change if cluster in a else None,
                b[cluster].median_rank_change if cluster in b else None,
            ),
            worsened_fraction=_delta(
                a[cluster].worsened_fraction if cluster in a else None,
                b[cluster].worsened_fraction if cluster in b else None,
            ),
        )
        for cluster in sorted(set(a) | set(b))
    )


def compare_verified_public_runs(
    model_a: VerifiedPublicRun,
    model_b: VerifiedPublicRun,
    *,
    paired_experiment_evidence: VerifiedPairedExperimentEvidence,
    created_at_utc: datetime | None = None,
) -> PairedModelComparisonReport:
    """Compare two verified arms only after all shared-pair invariants hold."""

    if model_a.model_id != MODEL_A_ID or model_b.model_id != MODEL_B_V2_NEW_ID:
        raise PairedModelComparisonError("comparison requires Model A then Model B V2")
    _validate_run_against_plan(model_a, role="model_a", evidence=paired_experiment_evidence)
    _validate_run_against_plan(model_b, role="model_b_v2", evidence=paired_experiment_evidence)
    if paired_experiment_evidence.paired_prediction_freeze.created_at_utc > min(
        model_a.reveal_created_at_utc,
        model_b.reveal_created_at_utc,
    ):
        raise PairedModelComparisonError(
            "one paired answer-key reveal predates the two-arm prediction freeze"
        )
    required_equal = (
        "experiment_id",
        "public_config_sha256",
        "revealed_target_set_sha256",
        "revealed_local_date_set_sha256",
        "generation_seed_commitment_sha256",
        "case_ids",
        "candidate_constraints",
        "candidate_constraints_sha256",
        "ephemeris_sha256",
        "candidate_cache_sha256",
        "isolation_software_tree",
        "recovery_settings",
    )
    mismatched = [
        name for name in required_equal if getattr(model_a, name) != getattr(model_b, name)
    ]
    if mismatched:
        raise PairedModelComparisonError(
            "paired runs differ on required shared inputs: " + ", ".join(mismatched)
        )
    if model_a.run_manifest.software_commit != model_b.run_manifest.software_commit:
        raise PairedModelComparisonError("paired runs used different software commits")
    if model_a.run_manifest.software_environment != model_b.run_manifest.software_environment:
        raise PairedModelComparisonError("paired runs used different software environments")
    if model_a.run_manifest.input_hashes.get(
        "model_a_mapping_library"
    ) != model_b.run_manifest.input_hashes.get("model_a_mapping_library"):
        raise PairedModelComparisonError("paired runs used different Model A base mappings")
    if model_a.question_bank_sha256 != model_b.question_bank_sha256:
        raise PairedModelComparisonError("paired runs used different question banks")
    if model_b.difference_gate is None:
        raise PairedModelComparisonError("Model B V2 run lacks a verified difference gate")
    audited_at = _parse_utc(
        model_b.difference_gate.get("audited_at_utc"), "difference audit timestamp"
    )
    if model_a.generation_started_at_utc < audited_at:
        raise PairedModelComparisonError("Model A generation predates the required PASS audit")

    metrics_a = _metrics_by_case(model_a.recomputed_evaluation)
    metrics_b = _metrics_by_case(model_b.recomputed_evaluation)
    failures_a = _failures_by_case(model_a.recomputed_evaluation)
    failures_b = _failures_by_case(model_b.recomputed_evaluation)
    cases: list[PairedCaseResult] = []
    constraints_by_case = {item.case_id: item for item in model_a.candidate_constraints}
    for case_id in model_a.case_ids:
        left, right = metrics_a.get(case_id), metrics_b.get(case_id)
        constraint = constraints_by_case[case_id]
        declared_candidate_count = calendar.monthrange(
            constraint.known_birth_year, constraint.known_birth_month
        )[1]
        if left is not None and right is not None:
            if left.true_candidate_id != right.true_candidate_id:
                raise PairedModelComparisonError(
                    f"paired case {case_id} has different revealed true dates"
                )
            if left.candidate_count != right.candidate_count:
                raise PairedModelComparisonError(
                    f"paired case {case_id} has different candidate counts"
                )
            if left.candidate_count != declared_candidate_count:
                raise PairedModelComparisonError(
                    f"paired case {case_id} candidate count differs from its calendar month"
                )
            rank_delta = right.midrank - left.midrank
            outcome: Literal["improved", "unchanged", "worsened", "unevaluable"] = (
                "improved" if rank_delta < 0 else "worsened" if rank_delta > 0 else "unchanged"
            )
            true_date: str | None = left.true_candidate_id
            candidate_count: int | None = declared_candidate_count
        else:
            rank_delta = None
            outcome = "unevaluable"
            observed = left or right
            true_date = observed.true_candidate_id if observed else None
            if observed is not None and observed.candidate_count != declared_candidate_count:
                raise PairedModelComparisonError(
                    f"paired case {case_id} candidate count differs from its calendar month"
                )
            candidate_count = declared_candidate_count
        cases.append(
            PairedCaseResult(
                case_id=case_id,
                true_local_date=true_date,
                candidate_count=candidate_count,
                model_a=left,
                model_b=right,
                b_minus_a_midrank=rank_delta,
                b_minus_a_percentile=(
                    None if left is None or right is None else right.percentile - left.percentile
                ),
                b_minus_a_reciprocal_rank=(
                    None
                    if left is None or right is None
                    else right.reciprocal_rank - left.reciprocal_rank
                ),
                b_minus_a_top_1_credit=(
                    None
                    if left is None or right is None
                    else right.top_1_credit - left.top_1_credit
                ),
                b_minus_a_top_3_credit=(
                    None
                    if left is None or right is None
                    else right.top_3_credit - left.top_3_credit
                ),
                b_minus_a_top_5_credit=(
                    None
                    if left is None or right is None
                    else right.top_5_credit - left.top_5_credit
                ),
                outcome=outcome,
                model_a_tied=left.tied if left else None,
                model_b_tied=right.tied if right else None,
                model_a_failure_classes=failures_a.get(case_id, ()),
                model_b_failure_classes=failures_b.get(case_id, ()),
            )
        )
    aggregate_a = model_a.recomputed_evaluation.aggregate
    aggregate_b = model_b.recomputed_evaluation.aggregate
    outcome_counts = Counter(item.outcome for item in cases)
    created = created_at_utc or datetime.now(UTC)
    if created < max(
        model_a.evaluation_created_at_utc,
        model_b.evaluation_created_at_utc,
    ):
        raise PairedModelComparisonError("comparison timestamp predates arm evaluation")
    return PairedModelComparisonReport(
        created_at_utc=created,
        experiment_id=model_a.experiment_id,
        case_count=len(cases),
        paired_experiment_evidence=paired_experiment_evidence,
        model_a_provenance=model_a,
        model_b_provenance=model_b,
        model_a_aggregate=aggregate_a,
        model_b_aggregate=aggregate_b,
        top_1=_delta(aggregate_a.top_1, aggregate_b.top_1),
        top_3=_delta(aggregate_a.top_3, aggregate_b.top_3),
        top_5=_delta(aggregate_a.top_5, aggregate_b.top_5),
        mean_reciprocal_rank=_delta(
            aggregate_a.mean_reciprocal_rank, aggregate_b.mean_reciprocal_rank
        ),
        mean_midrank=_delta(aggregate_a.mean_midrank, aggregate_b.mean_midrank),
        mean_percentile=_delta(aggregate_a.mean_percentile, aggregate_b.mean_percentile),
        outcomes=PairedOutcomeCounts(
            improved=outcome_counts["improved"],
            unchanged=outcome_counts["unchanged"],
            worsened=outcome_counts["worsened"],
            unevaluable=outcome_counts["unevaluable"],
        ),
        model_a_failure_counts=dict(sorted(model_a.recomputed_evaluation.failure_counts.items())),
        model_b_failure_counts=dict(sorted(model_b.recomputed_evaluation.failure_counts.items())),
        model_a_tied_case_count=sum(item.model_a_tied is True for item in cases),
        model_b_tied_case_count=sum(item.model_b_tied is True for item in cases),
        cases=tuple(cases),
        restoration_differences=_restoration_differences(
            model_a.recomputed_evaluation.restoration_curves,
            model_b.recomputed_evaluation.restoration_curves,
        ),
        ablation_differences=_ablation_differences(
            model_a.recomputed_evaluation.leave_one_cluster_out,
            model_b.recomputed_evaluation.leave_one_cluster_out,
        ),
        chance_calendar_baseline=_chance_baseline(cases),
    )


def compare_model_a_v2_new_run_dirs(
    model_a_run_dir: str | Path,
    model_b_run_dir: str | Path,
    *,
    paired_plan_path: str | Path,
    public_config_path: str | Path,
    model_a_generation_binding_path: str | Path,
    model_b_generation_binding_path: str | Path,
    paired_prediction_freeze_path: str | Path,
    created_at_utc: datetime | None = None,
) -> PairedModelComparisonReport:
    """Verify and compare the fixed model pair without accepting secret inputs."""

    model_a = load_verified_public_run(model_a_run_dir, expected_model_id="MODEL-A-CORE-V1")
    model_b = load_verified_public_run(model_b_run_dir, expected_model_id="MODEL-B-DETAILED-V2-NEW")
    paired_evidence = load_verified_paired_experiment_evidence(
        paired_plan_path=paired_plan_path,
        public_config_path=public_config_path,
        model_a_generation_binding_path=model_a_generation_binding_path,
        model_b_generation_binding_path=model_b_generation_binding_path,
        model_a_generation_receipt_path=(Path(model_a_run_dir) / "generation.receipt.json"),
        model_b_generation_receipt_path=(Path(model_b_run_dir) / "generation.receipt.json"),
        paired_prediction_freeze_path=paired_prediction_freeze_path,
        model_a_run_dir=model_a_run_dir,
        model_b_run_dir=model_b_run_dir,
    )
    return compare_verified_public_runs(
        model_a,
        model_b,
        paired_experiment_evidence=paired_evidence,
        created_at_utc=created_at_utc,
    )


def write_paired_model_comparison_report(
    report: PairedModelComparisonReport, output_path: str | Path
) -> Path:
    """Write the immutable canonical public comparison report."""

    return write_new_canonical_json(output_path, report)
