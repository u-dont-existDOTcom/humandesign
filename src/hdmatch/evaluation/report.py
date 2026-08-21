"""Frozen-run evaluator for the documented predictions-v1 and answer-key-v1 shapes."""

from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Mapping
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
    sha256_file,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import FreezeRecord, verify_frozen_predictions
from hdmatch.experiments.manifest import SHA256_PATTERN
from hdmatch.experiments.reveal import verify_reveal_record
from hdmatch.schemas import ScoredState
from hdmatch.search.candidate_universe import local_date_utc_bounds
from hdmatch.search.minute_rectifier import (
    KnownDateIntervalRanking,
    RankedIntervalGroup,
    RankedStableInterval,
    RevealedIntervalIdentification,
    identify_revealed_interval,
)
from hdmatch.util import sha256_json

from .ablation import (
    ClusterAblationSummary,
    CurveObservation,
    CurvePoint,
    LeaveOneClusterOutObservation,
    aggregate_leave_one_cluster_out,
    aggregate_restoration_curves,
)
from .failures import FailureClassification, FailureRecord, classify_oracle_failure
from .leakage import scan_prediction_payload
from .metrics import (
    AggregateRankMetrics,
    CaseRankMetrics,
    aggregate_rank_metrics,
    evaluate_ranked_case,
)


class EvaluationInputError(ValueError):
    """Predictions or revealed labels violate their frozen cross-file contract."""


class StableIntervalEvaluation(BaseModel):
    """Post-reveal result without an invented point-time prediction."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    declared_local_date: date
    timezone: str
    true_utc: datetime
    matched_state_id: str
    start_utc: datetime
    end_utc: datetime
    eligible_start_utc: datetime
    eligible_end_utc: datetime
    source_interval_width_seconds: float = Field(gt=0.0)
    eligible_width_seconds: float = Field(gt=0.0)
    universe_boundary_truncated: bool
    rank_start: int = Field(ge=1)
    rank_end: int = Field(ge=1)
    midrank: float = Field(ge=1.0)
    tie_size: int = Field(ge=1)
    net_rubric_bits: float
    point_estimate_utc: None = None
    interval_resolution_status: Literal[
        "stable_interval", "unresolved_universe_boundary_clipped"
    ]
    resolution_semantics: Literal["source-half-open-interval-not-point"] = (
        "source-half-open-interval-not-point"
    )

    @field_validator(
        "true_utc",
        "start_utc",
        "end_utc",
        "eligible_start_utc",
        "eligible_end_utc",
    )
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("rectification timestamps must be timezone-aware")
        return value.astimezone(UTC)


class EvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["evaluation-report-v1"] = "evaluation-report-v1"
    experiment_id: str
    created_at_utc: datetime
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    reveal_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_file: str | None = None
    encrypted_answer_key_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    answer_key_payload_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    revealed_target_set_sha256: str | None = Field(
        default=None, pattern=SHA256_PATTERN
    )
    evaluation_target: Literal["local_date", "stable_interval"] = "local_date"
    aggregate: AggregateRankMetrics
    cases: tuple[CaseRankMetrics, ...]
    failures: tuple[FailureRecord, ...]
    failure_counts: dict[str, int]
    restoration_curves: tuple[CurvePoint, ...]
    leave_one_cluster_out: tuple[ClusterAblationSummary, ...]
    rectification_cases: tuple[StableIntervalEvaluation, ...] = ()
    tie_policy: Literal["fractional-credit-random-within-tie"] = (
        "fractional-credit-random-within-tie"
    )
    score_semantics: Literal["rubric-bits-not-probabilities"] = (
        "rubric-bits-not-probabilities"
    )
    claim_boundary: Literal["synthetic-engineering-validation-only"] = (
        "synthetic-engineering-validation-only"
    )

    @field_validator("created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("evaluation timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("encrypted_answer_key_file")
    @classmethod
    def require_safe_envelope_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or value in {"", "."}:
            raise ValueError("encrypted_answer_key_file must be a safe run-relative path")
        return path.as_posix()

    @model_validator(mode="after")
    def require_complete_reveal_provenance(self) -> EvaluationReport:
        fields = (
            self.encrypted_answer_key_file,
            self.encrypted_answer_key_sha256,
            self.answer_key_payload_sha256,
        )
        if any(item is not None for item in fields) and not all(
            item is not None for item in fields
        ):
            raise ValueError("evaluation reveal provenance must be complete or legacy-absent")
        return self


def _unique_cases(payload: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    cases = payload.get("cases" if label == "answer key" else "predictions")
    if not isinstance(cases, list):
        raise EvaluationInputError(f"{label} must contain a case list")
    result: dict[str, dict[str, Any]] = {}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("case_id"), str):
            raise EvaluationInputError(f"{label} contains a case without a string case_id")
        case_id = case["case_id"]
        if case_id in result:
            raise EvaluationInputError(f"{label} contains duplicate case_id {case_id!r}")
        result[case_id] = case
    if not result:
        raise EvaluationInputError(f"{label} contains no cases")
    return result


def _validate_cross_file_bindings(
    predictions: dict[str, Any], answer_key: dict[str, Any], freeze: FreezeRecord
) -> None:
    if predictions.get("schema_version") != "predictions-v1":
        raise EvaluationInputError("unsupported predictions schema")
    if answer_key.get("schema_version") != "answer-key-v1":
        raise EvaluationInputError("unsupported answer-key schema")
    for payload, name in ((predictions, "predictions"), (answer_key, "answer key")):
        if payload.get("experiment_id") != freeze.experiment_id:
            raise EvaluationInputError(f"{name} experiment_id does not match freeze")
        if payload.get("blind_input_sha256") != freeze.blind_input_sha256:
            raise EvaluationInputError(f"{name} blind input hash does not match freeze")
    for field in ("model_sha256", "question_bank_sha256", "mapping_sha256"):
        if predictions.get(field) != getattr(freeze, field):
            raise EvaluationInputError(f"predictions {field} does not match freeze")


def _require_iso_date(value: Any, *, label: str) -> str:
    if not isinstance(value, str):
        raise EvaluationInputError(f"{label} must be an ISO local-date string")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise EvaluationInputError(f"{label} must be an ISO local-date string") from exc
    if parsed.isoformat() != value:
        raise EvaluationInputError(f"{label} must use canonical YYYY-MM-DD form")
    return value


def _require_utc_datetime(value: Any, *, label: str) -> datetime:
    if not isinstance(value, str):
        raise EvaluationInputError(f"{label} must be a canonical UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvaluationInputError(f"{label} must be a canonical UTC timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EvaluationInputError(f"{label} must be timezone-aware")
    normalized = parsed.astimezone(UTC)
    if normalized.isoformat().replace("+00:00", "Z") != value:
        raise EvaluationInputError(f"{label} must use canonical UTC Z form")
    return normalized


def _utc_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _revealed_target_set_hash(
    keyed_cases: Mapping[str, dict[str, Any]],
) -> str | None:
    """Hash concealed target tuples after reveal, excluding experiment identity."""

    extended_field_present = [
        "true_utc" in keyed or "true_chart_features_hash" in keyed
        for keyed in keyed_cases.values()
    ]
    if not any(extended_field_present):
        return None
    if not all(
        "true_utc" in keyed and "true_chart_features_hash" in keyed
        for keyed in keyed_cases.values()
    ):
        raise EvaluationInputError(
            "answer key cases must all include true_utc and true_chart_features_hash"
        )
    tuples: list[tuple[str, str, str, str]] = []
    for case_id in sorted(keyed_cases):
        keyed = keyed_cases[case_id]
        true_utc = _require_utc_datetime(
            keyed.get("true_utc"), label=f"answer key case {case_id} true_utc"
        )
        true_date = _require_iso_date(
            keyed.get("true_local_date"),
            label=f"answer key case {case_id} true_local_date",
        )
        chart_hash = keyed.get("true_chart_features_hash")
        if not isinstance(chart_hash, str) or re.fullmatch(SHA256_PATTERN, chart_hash) is None:
            raise EvaluationInputError(
                f"answer key case {case_id} true_chart_features_hash must be SHA-256"
            )
        tuples.append((case_id, _utc_text(true_utc), true_date, chart_hash))
    return sha256_json(
        {
            "schema_version": "revealed-target-set-v1",
            "targets": tuples,
        }
    )


def _require_rank(value: Any, *, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise EvaluationInputError(f"{label} must be a positive integer")
    return int(value)


def _require_finite_float(value: Any, *, label: str, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EvaluationInputError(f"{label} must be a finite number")
    converted = float(value)
    if not math.isfinite(converted) or (positive and converted <= 0.0):
        raise EvaluationInputError(f"{label} must be a finite positive number")
    return converted


def _parse_interval_stage(
    *,
    case_id: str,
    stage_label: str,
    stage: Any,
) -> KnownDateIntervalRanking:
    if not isinstance(stage, dict):
        raise EvaluationInputError(f"case {case_id} {stage_label} must be an object")
    local_date_text = _require_iso_date(
        stage.get("local_date"), label=f"case {case_id} {stage_label}.local_date"
    )
    local_day = date.fromisoformat(local_date_text)
    timezone_name = stage.get("timezone")
    if not isinstance(timezone_name, str) or not timezone_name:
        raise EvaluationInputError(f"case {case_id} {stage_label}.timezone must be a string")
    if stage.get("interval_semantics") != "half-open-[start,end)":
        raise EvaluationInputError(
            f"case {case_id} {stage_label} must declare half-open interval semantics"
        )
    date_start = _require_utc_datetime(
        stage.get("date_start_utc"),
        label=f"case {case_id} {stage_label}.date_start_utc",
    )
    date_end = _require_utc_datetime(
        stage.get("date_end_utc"),
        label=f"case {case_id} {stage_label}.date_end_utc",
    )
    try:
        expected_start, expected_end = local_date_utc_bounds(local_day, timezone_name)
    except (KeyError, ValueError) as exc:
        raise EvaluationInputError(
            f"case {case_id} {stage_label} has invalid local date/timezone bounds"
        ) from exc
    if (date_start, date_end) != (expected_start, expected_end):
        raise EvaluationInputError(
            f"case {case_id} {stage_label} date bounds do not match local date/timezone"
        )

    raw_records = stage.get("ranked_intervals")
    if not isinstance(raw_records, list) or not raw_records:
        raise EvaluationInputError(f"case {case_id} {stage_label} lacks ranked_intervals")
    records: list[RankedStableInterval] = []
    seen_ids: set[str] = set()
    score_fields = tuple(ScoredState.model_fields)
    for index, raw_record in enumerate(raw_records):
        label = f"case {case_id} {stage_label}.ranked_intervals[{index}]"
        if not isinstance(raw_record, dict):
            raise EvaluationInputError(f"{label} must be an object")
        state_id = raw_record.get("state_id")
        if not isinstance(state_id, str) or not state_id:
            raise EvaluationInputError(f"{label}.state_id must be a string")
        if state_id in seen_ids:
            raise EvaluationInputError(f"case {case_id} {stage_label} repeats state_id {state_id}")
        seen_ids.add(state_id)
        start = _require_utc_datetime(raw_record.get("start_utc"), label=f"{label}.start_utc")
        end = _require_utc_datetime(raw_record.get("end_utc"), label=f"{label}.end_utc")
        eligible_start = _require_utc_datetime(
            raw_record.get("eligible_start_utc"), label=f"{label}.eligible_start_utc"
        )
        eligible_end = _require_utc_datetime(
            raw_record.get("eligible_end_utc"), label=f"{label}.eligible_end_utc"
        )
        if not start <= eligible_start < eligible_end <= end:
            raise EvaluationInputError(f"{label} has inconsistent full/eligible bounds")
        source_width = _require_finite_float(
            raw_record.get("source_interval_width_seconds"),
            label=f"{label}.source_interval_width_seconds",
            positive=True,
        )
        eligible_width = _require_finite_float(
            raw_record.get("eligible_width_seconds"),
            label=f"{label}.eligible_width_seconds",
            positive=True,
        )
        if abs(source_width - (end - start).total_seconds()) > 1e-6:
            raise EvaluationInputError(f"{label} source width does not match bounds")
        if abs(eligible_width - (eligible_end - eligible_start).total_seconds()) > 1e-6:
            raise EvaluationInputError(f"{label} eligible width does not match bounds")
        try:
            score = ScoredState.model_validate(
                {field: raw_record.get(field) for field in score_fields}
            )
        except ValueError as exc:
            raise EvaluationInputError(f"{label} has invalid score fields") from exc
        if score.state_id != state_id or not math.isfinite(score.net_rubric_bits):
            raise EvaluationInputError(f"{label} has inconsistent or non-finite score fields")
        rank_start = _require_rank(raw_record.get("rank_start"), label=f"{label}.rank_start")
        rank_end = _require_rank(raw_record.get("rank_end"), label=f"{label}.rank_end")
        if rank_end < rank_start:
            raise EvaluationInputError(f"{label} has a reversed rank interval")
        expected_midrank = (rank_start + rank_end) / 2.0
        if raw_record.get("midrank") != expected_midrank:
            raise EvaluationInputError(f"{label}.midrank does not match rank bounds")
        if raw_record.get("tied") is not (rank_end > rank_start):
            raise EvaluationInputError(f"{label}.tied does not match rank bounds")
        universe_boundary_truncated = raw_record.get("universe_boundary_truncated")
        if not isinstance(universe_boundary_truncated, bool):
            raise EvaluationInputError(
                f"{label}.universe_boundary_truncated must be boolean"
            )
        records.append(
            RankedStableInterval(
                state_id=state_id,
                start_utc=start,
                end_utc=end,
                eligible_start_utc=eligible_start,
                eligible_end_utc=eligible_end,
                stable_width=timedelta(seconds=source_width),
                eligible_width=timedelta(seconds=eligible_width),
                score=score,
                rank_start=rank_start,
                rank_end=rank_end,
                universe_boundary_truncated=universe_boundary_truncated,
            )
        )

    expected_order = sorted(
        records,
        key=lambda item: (
            -item.score.net_rubric_bits,
            item.eligible_start_utc,
            item.eligible_end_utc,
            item.state_id,
        ),
    )
    if [item.state_id for item in records] != [item.state_id for item in expected_order]:
        raise EvaluationInputError(
            f"case {case_id} {stage_label} interval records are not deterministically ranked"
        )

    groups: list[RankedIntervalGroup] = []
    position = 0
    while position < len(records):
        end_position = position + 1
        while (
            end_position < len(records)
            and records[end_position].score.net_rubric_bits
            == records[position].score.net_rubric_bits
        ):
            end_position += 1
        rank_start = position + 1
        rank_end = end_position
        members = tuple(records[position:end_position])
        if any(
            item.rank_start != rank_start or item.rank_end != rank_end for item in members
        ):
            raise EvaluationInputError(
                f"case {case_id} {stage_label} record ranks do not match exact score ties"
            )
        groups.append(
            RankedIntervalGroup(
                net_rubric_bits=members[0].score.net_rubric_bits,
                rank_start=rank_start,
                rank_end=rank_end,
                intervals=members,
            )
        )
        position = end_position

    expected_groups = [
        {
            "net_rubric_bits": group.net_rubric_bits,
            "rank_start": group.rank_start,
            "rank_end": group.rank_end,
            "midrank": float(group.midrank),
            "tied": group.tied,
            "state_ids": [item.state_id for item in group.intervals],
        }
        for group in groups
    ]
    if stage.get("interval_groups") != expected_groups:
        raise EvaluationInputError(
            f"case {case_id} {stage_label} interval_groups do not match ranked records"
        )

    chronological = sorted(
        records,
        key=lambda item: (item.eligible_start_utc, item.eligible_end_utc, item.state_id),
    )
    cursor = date_start
    for item in chronological:
        if item.eligible_start_utc != cursor:
            relation = "gap" if item.eligible_start_utc > cursor else "overlap"
            raise EvaluationInputError(
                f"case {case_id} {stage_label} interval partition has a {relation}"
            )
        cursor = item.eligible_end_utc
    if cursor != date_end:
        raise EvaluationInputError(
            f"case {case_id} {stage_label} interval partition does not cover the local date"
        )
    return KnownDateIntervalRanking(
        local_date=local_day,
        timezone_name=timezone_name,
        date_start_utc=date_start,
        date_end_utc=date_end,
        groups=tuple(groups),
    )


def _evaluate_interval_stage(
    *,
    case_id: str,
    stage_label: str,
    stage: Any,
    true_utc: datetime,
) -> tuple[
    CaseRankMetrics | None,
    int,
    KnownDateIntervalRanking,
    RevealedIntervalIdentification | None,
]:
    ranking = _parse_interval_stage(case_id=case_id, stage_label=stage_label, stage=stage)
    try:
        identification = identify_revealed_interval(ranking, true_utc)
    except ValueError:
        return None, len(ranking.records), ranking, None
    candidates = [
        {
            "state_id": interval.state_id,
            "net_rubric_bits": interval.score.net_rubric_bits,
        }
        for interval in ranking.records
    ]
    try:
        metrics = evaluate_ranked_case(
            case_id=case_id,
            candidates=candidates,
            true_candidate_id=identification.interval.state_id,
            id_field="state_id",
            score_field="net_rubric_bits",
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise EvaluationInputError(str(exc)) from exc
    return metrics, len(ranking.records), ranking, identification


def _stable_interval_evaluation(
    case_id: str,
    ranking: KnownDateIntervalRanking,
    identification: RevealedIntervalIdentification,
) -> StableIntervalEvaluation:
    interval = identification.interval
    return StableIntervalEvaluation(
        case_id=case_id,
        declared_local_date=ranking.local_date,
        timezone=ranking.timezone_name,
        true_utc=identification.true_utc,
        matched_state_id=interval.state_id,
        start_utc=interval.start_utc,
        end_utc=interval.end_utc,
        eligible_start_utc=interval.eligible_start_utc,
        eligible_end_utc=interval.eligible_end_utc,
        source_interval_width_seconds=interval.stable_width.total_seconds(),
        eligible_width_seconds=interval.eligible_width.total_seconds(),
        universe_boundary_truncated=interval.universe_boundary_truncated,
        rank_start=interval.rank_start,
        rank_end=interval.rank_end,
        midrank=float(interval.midrank),
        tie_size=interval.rank_end - interval.rank_start + 1,
        net_rubric_bits=interval.score.net_rubric_bits,
        interval_resolution_status=(
            "unresolved_universe_boundary_clipped"
            if interval.universe_boundary_truncated
            else "stable_interval"
        ),
    )


def _evaluate_stage_ranking(
    *,
    case_id: str,
    stage_label: str,
    stage: Any,
    true_date: str,
) -> tuple[CaseRankMetrics | None, int]:
    if not isinstance(stage, dict):
        raise EvaluationInputError(f"case {case_id} {stage_label} must be an object")
    ranked_dates = stage.get("ranked_dates")
    if not isinstance(ranked_dates, list) or not ranked_dates:
        raise EvaluationInputError(f"case {case_id} {stage_label} lacks ranked_dates")
    for index, candidate in enumerate(ranked_dates):
        if not isinstance(candidate, dict):
            raise EvaluationInputError(
                f"case {case_id} {stage_label}.ranked_dates[{index}] must be an object"
            )
        _require_iso_date(
            candidate.get("local_date"),
            label=f"case {case_id} {stage_label}.ranked_dates[{index}].local_date",
        )
    try:
        metrics = evaluate_ranked_case(
            case_id=case_id,
            candidates=ranked_dates,
            true_candidate_id=true_date,
        )
    except (KeyError, TypeError, ValueError) as exc:
        if "absent" in str(exc):
            return None, len(ranked_dates)
        raise EvaluationInputError(str(exc)) from exc
    return metrics, len(ranked_dates)


def evaluate_frozen_payloads(
    *,
    predictions: dict[str, Any],
    answer_key: dict[str, Any],
    freeze: FreezeRecord,
    freeze_sha256: str,
    reveal_sha256: str,
    encrypted_answer_key_file: str,
    encrypted_answer_key_sha256: str,
    answer_key_payload_sha256: str,
    created_at_utc: datetime | None = None,
) -> EvaluationReport:
    """Evaluate exact documented payload shapes after a caller verifies frozen bytes."""

    leakage_report = scan_prediction_payload(predictions)
    if not leakage_report.passed:
        raise EvaluationInputError("predictions contain concealed-target leakage")
    if sha256_bytes(canonical_json_bytes(answer_key)) != answer_key_payload_sha256:
        raise EvaluationInputError("answer key does not match its declared reveal binding")
    _validate_cross_file_bindings(predictions, answer_key, freeze)
    predicted_cases = _unique_cases(predictions, "predictions")
    keyed_cases = _unique_cases(answer_key, "answer key")
    if predicted_cases.keys() != keyed_cases.keys():
        missing_predictions = sorted(keyed_cases.keys() - predicted_cases.keys())
        missing_keys = sorted(predicted_cases.keys() - keyed_cases.keys())
        raise EvaluationInputError(
            "case sets differ; "
            f"missing predictions={missing_predictions}, missing keys={missing_keys}"
        )
    declared_universes: set[str] = set()
    for case in predicted_cases.values():
        candidate_universe = case.get("candidate_universe", "known_month")
        if not isinstance(candidate_universe, str) or candidate_universe not in {
            "known_month",
            "known_date",
        }:
            raise EvaluationInputError(
                "predictions contain an unsupported candidate universe"
            )
        declared_universes.add(candidate_universe)
    if len(declared_universes) != 1:
        raise EvaluationInputError("mixed candidate-universe evaluation is not allowed")
    evaluation_target: Literal["local_date", "stable_interval"] = (
        "stable_interval" if declared_universes == {"known_date"} else "local_date"
    )
    revealed_target_set_sha256 = _revealed_target_set_hash(keyed_cases)
    case_metrics: list[CaseRankMetrics] = []
    failures: list[FailureRecord] = []
    curves: list[CurveObservation] = []
    ablations: list[LeaveOneClusterOutObservation] = []
    rectification_cases: list[StableIntervalEvaluation] = []
    for case_id in sorted(keyed_cases):
        predicted = predicted_cases[case_id]
        keyed = keyed_cases[case_id]
        true_date = _require_iso_date(
            keyed.get("true_local_date"), label=f"answer key case {case_id} true_local_date"
        )
        unresolved = predicted.get("unresolved_mapping_ids", [])
        if not isinstance(unresolved, list) or not all(
            isinstance(item, str) for item in unresolved
        ):
            raise EvaluationInputError(f"case {case_id} has invalid unresolved_mapping_ids")
        if predicted.get("candidate_universe") == "known_date":
            true_utc = _require_utc_datetime(
                keyed.get("true_utc"), label=f"answer key case {case_id} true_utc"
            )
            metrics, _, ranking, identification = _evaluate_interval_stage(
                case_id=case_id,
                stage_label="final",
                stage=predicted,
                true_utc=true_utc,
            )
            if ranking.local_date.isoformat() != true_date:
                raise EvaluationInputError(
                    f"case {case_id} known local date does not match revealed local date"
                )
            if metrics is None or identification is None:
                failures.append(
                    classify_oracle_failure(
                        case_id=case_id,
                        true_candidate_present=False,
                        evidence={
                            "declared_local_date": ranking.local_date.isoformat(),
                            "interval_count": len(ranking.records),
                        },
                    )
                )
            else:
                case_metrics.append(metrics)
                rectification_cases.append(
                    _stable_interval_evaluation(case_id, ranking, identification)
                )
                if metrics.best_rank != 1:
                    failures.append(
                        classify_oracle_failure(
                            case_id=case_id,
                            true_candidate_present=True,
                            unresolved_mapping_ids=tuple(unresolved),
                            evidence={
                                "best_rank": metrics.best_rank,
                                "worst_rank": metrics.worst_rank,
                                "midrank": metrics.midrank,
                                "source_interval_start_utc": _utc_text(
                                    identification.interval.start_utc
                                ),
                                "source_interval_end_utc": _utc_text(
                                    identification.interval.end_utc
                                ),
                                "universe_boundary_truncated": (
                                    identification.interval.universe_boundary_truncated
                                ),
                            },
                        )
                    )

            zero_metrics, zero_count, zero_ranking, _ = _evaluate_interval_stage(
                case_id=case_id,
                stage_label="zero_cluster",
                stage=predicted.get("zero_cluster"),
                true_utc=true_utc,
            )
            if (
                zero_ranking.local_date != ranking.local_date
                or zero_ranking.timezone_name != ranking.timezone_name
            ):
                raise EvaluationInputError(
                    f"case {case_id} zero_cluster changes the known-date universe"
                )
            curves.extend(
                CurveObservation(
                    case_id=case_id,
                    method=cast(Literal["random", "active", "leave_one_out"], method),
                    cluster_count=0,
                    midrank=zero_metrics.midrank if zero_metrics is not None else None,
                    candidate_count=zero_count,
                    tie_size=zero_metrics.tie_size if zero_metrics is not None else 1,
                )
                for method in ("random", "active")
            )
            for field, method in (
                ("random_restoration", "random"),
                ("active_restoration", "active"),
            ):
                restoration = predicted.get(field, [])
                if not isinstance(restoration, list):
                    raise EvaluationInputError(f"case {case_id} has invalid {field}")
                for point in restoration:
                    if not isinstance(point, dict):
                        raise EvaluationInputError(
                            f"case {case_id} has invalid {field} point"
                        )
                    try:
                        stage_metrics, stage_count, stage_ranking, _ = (
                            _evaluate_interval_stage(
                                case_id=case_id,
                                stage_label=f"{field} step",
                                stage=point,
                                true_utc=true_utc,
                            )
                        )
                        if (
                            stage_ranking.local_date != ranking.local_date
                            or stage_ranking.timezone_name != ranking.timezone_name
                        ):
                            raise EvaluationInputError(
                                f"case {case_id} {field} changes the known-date universe"
                            )
                        curves.append(
                            CurveObservation(
                                case_id=case_id,
                                method=cast(
                                    Literal["random", "active", "leave_one_out"], method
                                ),
                                cluster_count=point["cluster_count"],
                                midrank=(
                                    stage_metrics.midrank
                                    if stage_metrics is not None
                                    else None
                                ),
                                candidate_count=stage_count,
                                tie_size=(
                                    stage_metrics.tie_size
                                    if stage_metrics is not None
                                    else 1
                                ),
                            )
                        )
                    except (KeyError, TypeError, ValueError) as exc:
                        raise EvaluationInputError(
                            f"case {case_id} has malformed {field} point"
                        ) from exc
            leave_one_out = predicted.get("leave_one_cluster_out", [])
            if not isinstance(leave_one_out, list):
                raise EvaluationInputError(
                    f"case {case_id} has invalid leave_one_cluster_out"
                )
            for point in leave_one_out:
                if not isinstance(point, dict):
                    raise EvaluationInputError(
                        f"case {case_id} has invalid leave_one_cluster_out point"
                    )
                try:
                    stage_metrics, _, stage_ranking, _ = _evaluate_interval_stage(
                        case_id=case_id,
                        stage_label="leave_one_cluster_out step",
                        stage=point,
                        true_utc=true_utc,
                    )
                    if (
                        stage_ranking.local_date != ranking.local_date
                        or stage_ranking.timezone_name != ranking.timezone_name
                    ):
                        raise EvaluationInputError(
                            f"case {case_id} leave-one-out changes the known-date universe"
                        )
                    ablations.append(
                        LeaveOneClusterOutObservation(
                            case_id=case_id,
                            cluster_id=point["cluster_id"],
                            full_midrank=metrics.midrank if metrics is not None else None,
                            ablated_midrank=(
                                stage_metrics.midrank if stage_metrics is not None else None
                            ),
                        )
                    )
                except (KeyError, TypeError, ValueError) as exc:
                    raise EvaluationInputError(
                        f"case {case_id} has malformed leave_one_cluster_out point"
                    ) from exc
            continue
        metrics, _ = _evaluate_stage_ranking(
            case_id=case_id,
            stage_label="final",
            stage=predicted,
            true_date=true_date,
        )
        if metrics is None:
            failures.append(
                classify_oracle_failure(case_id=case_id, true_candidate_present=False)
            )
        else:
            case_metrics.append(metrics)
        if metrics is not None and metrics.best_rank != 1:
            variants = predicted.get("aggregation_variants", {})
            if not isinstance(variants, dict):
                raise EvaluationInputError(
                    f"case {case_id} has invalid aggregation_variants"
                )
            best_state_metrics: CaseRankMetrics | None = None
            if "best_state" in variants:
                best_state_metrics, _ = _evaluate_stage_ranking(
                    case_id=case_id,
                    stage_label="aggregation_variants.best_state",
                    stage=variants["best_state"],
                    true_date=true_date,
                )
            failures.append(
                classify_oracle_failure(
                    case_id=case_id,
                    true_candidate_present=True,
                    unresolved_mapping_ids=tuple(unresolved),
                    state_winner_but_date_loser=(
                        best_state_metrics is not None
                        and best_state_metrics.best_rank == 1
                    ),
                    evidence={"best_rank": metrics.best_rank, "midrank": metrics.midrank},
                )
            )
        zero_metrics, zero_count = _evaluate_stage_ranking(
            case_id=case_id,
            stage_label="zero_cluster",
            stage=predicted.get("zero_cluster"),
            true_date=true_date,
        )
        curves.extend(
            CurveObservation(
                case_id=case_id,
                method=cast(Literal["random", "active", "leave_one_out"], method),
                cluster_count=0,
                midrank=zero_metrics.midrank if zero_metrics is not None else None,
                candidate_count=zero_count,
                tie_size=zero_metrics.tie_size if zero_metrics is not None else 1,
            )
            for method in ("random", "active")
        )
        for field, method in (("random_restoration", "random"), ("active_restoration", "active")):
            restoration = predicted.get(field, [])
            if not isinstance(restoration, list):
                raise EvaluationInputError(f"case {case_id} has invalid {field}")
            for point in restoration:
                if not isinstance(point, dict):
                    raise EvaluationInputError(f"case {case_id} has invalid {field} point")
                try:
                    stage_metrics, stage_count = _evaluate_stage_ranking(
                        case_id=case_id,
                        stage_label=f"{field} step",
                        stage=point,
                        true_date=true_date,
                    )
                    curves.append(
                        CurveObservation(
                            case_id=case_id,
                            method=cast(
                                Literal["random", "active", "leave_one_out"], method
                            ),
                            cluster_count=point["cluster_count"],
                            midrank=(
                                stage_metrics.midrank if stage_metrics is not None else None
                            ),
                            candidate_count=stage_count,
                            tie_size=(
                                stage_metrics.tie_size if stage_metrics is not None else 1
                            ),
                        )
                    )
                except (KeyError, TypeError, ValueError) as exc:
                    raise EvaluationInputError(
                        f"case {case_id} has malformed {field} point"
                    ) from exc
        leave_one_out = predicted.get("leave_one_cluster_out", [])
        if not isinstance(leave_one_out, list):
            raise EvaluationInputError(f"case {case_id} has invalid leave_one_cluster_out")
        for point in leave_one_out:
            if not isinstance(point, dict):
                raise EvaluationInputError(
                    f"case {case_id} has invalid leave_one_cluster_out point"
                )
            try:
                stage_metrics, _ = _evaluate_stage_ranking(
                    case_id=case_id,
                    stage_label="leave_one_cluster_out step",
                    stage=point,
                    true_date=true_date,
                )
                ablations.append(
                    LeaveOneClusterOutObservation(
                        case_id=case_id,
                        cluster_id=point["cluster_id"],
                        full_midrank=metrics.midrank if metrics is not None else None,
                        ablated_midrank=(
                            stage_metrics.midrank if stage_metrics is not None else None
                        ),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise EvaluationInputError(
                    f"case {case_id} has malformed leave_one_cluster_out point"
                ) from exc
    observed_counts = Counter(failure.classification.value for failure in failures)
    counts = {
        classification.value: observed_counts[classification.value]
        for classification in FailureClassification
    }
    return EvaluationReport(
        experiment_id=freeze.experiment_id,
        created_at_utc=created_at_utc or datetime.now(UTC),
        prediction_sha256=freeze.prediction_sha256,
        freeze_sha256=freeze_sha256,
        reveal_sha256=reveal_sha256,
        encrypted_answer_key_file=encrypted_answer_key_file,
        encrypted_answer_key_sha256=encrypted_answer_key_sha256,
        answer_key_payload_sha256=answer_key_payload_sha256,
        blind_input_sha256=freeze.blind_input_sha256,
        model_sha256=freeze.model_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        mapping_sha256=freeze.mapping_sha256,
        revealed_target_set_sha256=revealed_target_set_sha256,
        evaluation_target=evaluation_target,
        aggregate=aggregate_rank_metrics(case_metrics, total_case_count=len(keyed_cases)),
        cases=tuple(case_metrics),
        failures=tuple(failures),
        failure_counts=dict(sorted(counts.items())),
        restoration_curves=aggregate_restoration_curves(curves),
        leave_one_cluster_out=aggregate_leave_one_cluster_out(ablations),
        rectification_cases=tuple(rectification_cases),
    )


def evaluate_frozen_run(
    run_dir: str | Path,
    *,
    answer_key: dict[str, Any],
    freeze_path: str | Path | None = None,
    reveal_record_path: str | Path | None = None,
    output_path: str | Path | None = None,
    created_at_utc: datetime | None = None,
) -> EvaluationReport:
    """Refuse evaluation unless the predictions still match a valid canonical freeze."""

    directory = Path(run_dir)
    resolved_freeze = (
        Path(freeze_path) if freeze_path is not None else directory / "prediction.freeze.json"
    )
    freeze = verify_frozen_predictions(
        directory,
        freeze_path=resolved_freeze,
        require_run_manifest=True,
    )
    resolved_reveal = (
        Path(reveal_record_path)
        if reveal_record_path is not None
        else directory / "answer-key.reveal.json"
    )
    reveal = verify_reveal_record(
        directory,
        freeze=freeze,
        freeze_path=resolved_freeze,
        reveal_record_path=resolved_reveal,
        require_complete_binding=True,
    )
    envelope_file = reveal.encrypted_answer_key_file
    envelope_sha256 = reveal.encrypted_answer_key_sha256
    answer_key_sha256 = reveal.answer_key_payload_sha256
    if envelope_file is None or envelope_sha256 is None or answer_key_sha256 is None:
        raise EvaluationInputError("reveal record lacks complete answer-key bindings")
    supplied_answer_key_sha256 = sha256_bytes(canonical_json_bytes(answer_key))
    if supplied_answer_key_sha256 != answer_key_sha256:
        raise EvaluationInputError("supplied answer key does not match the reveal binding")
    predictions_path = directory / freeze.prediction_file
    try:
        predictions = load_json_bytes(predictions_path)
    except (OSError, ValueError) as exc:
        raise EvaluationInputError("frozen predictions are not valid JSON") from exc
    if not isinstance(predictions, dict):
        raise EvaluationInputError("frozen predictions must be a JSON object")
    report = evaluate_frozen_payloads(
        predictions=predictions,
        answer_key=answer_key,
        freeze=freeze,
        freeze_sha256=sha256_file(resolved_freeze),
        reveal_sha256=sha256_file(resolved_reveal),
        encrypted_answer_key_file=envelope_file,
        encrypted_answer_key_sha256=envelope_sha256,
        answer_key_payload_sha256=answer_key_sha256,
        created_at_utc=created_at_utc,
    )
    if report.created_at_utc < reveal.revealed_at_utc:
        raise EvaluationInputError("evaluation timestamp cannot predate answer-key reveal")
    destination = Path(output_path) if output_path is not None else directory / "evaluation.json"
    write_new_canonical_json(destination, report)
    return report
