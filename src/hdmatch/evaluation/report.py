"""Frozen-run evaluator for the documented predictions-v1 and answer-key-v1 shapes."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator

from hdmatch.experiments.canonical import load_json_bytes, sha256_file, write_new_canonical_json
from hdmatch.experiments.freeze import FreezeRecord, verify_frozen_predictions
from hdmatch.experiments.manifest import SHA256_PATTERN
from hdmatch.experiments.reveal import verify_reveal_record

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


class EvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["evaluation-report-v1"] = "evaluation-report-v1"
    experiment_id: str
    created_at_utc: datetime
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    reveal_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    aggregate: AggregateRankMetrics
    cases: tuple[CaseRankMetrics, ...]
    failures: tuple[FailureRecord, ...]
    failure_counts: dict[str, int]
    restoration_curves: tuple[CurvePoint, ...]
    leave_one_cluster_out: tuple[ClusterAblationSummary, ...]
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
    created_at_utc: datetime | None = None,
) -> EvaluationReport:
    """Evaluate exact documented payload shapes after a caller verifies frozen bytes."""

    leakage_report = scan_prediction_payload(predictions)
    if not leakage_report.passed:
        raise EvaluationInputError("predictions contain concealed-target leakage")
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
    case_metrics: list[CaseRankMetrics] = []
    failures: list[FailureRecord] = []
    curves: list[CurveObservation] = []
    ablations: list[LeaveOneClusterOutObservation] = []
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
            failures.append(
                classify_oracle_failure(
                    case_id=case_id,
                    true_candidate_present=True,
                    unresolved_mapping_ids=tuple(unresolved),
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
        blind_input_sha256=freeze.blind_input_sha256,
        model_sha256=freeze.model_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        mapping_sha256=freeze.mapping_sha256,
        aggregate=aggregate_rank_metrics(case_metrics, total_case_count=len(keyed_cases)),
        cases=tuple(case_metrics),
        failures=tuple(failures),
        failure_counts=dict(sorted(counts.items())),
        restoration_curves=aggregate_restoration_curves(curves),
        leave_one_cluster_out=aggregate_leave_one_cluster_out(ablations),
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
    freeze = verify_frozen_predictions(directory, freeze_path=resolved_freeze)
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
    )
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
        created_at_utc=created_at_utc,
    )
    if report.created_at_utc < reveal.revealed_at_utc:
        raise EvaluationInputError("evaluation timestamp cannot predate answer-key reveal")
    destination = Path(output_path) if output_path is not None else directory / "evaluation.json"
    write_new_canonical_json(destination, report)
    return report
