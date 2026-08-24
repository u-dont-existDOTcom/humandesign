"""Person-level cross-fitting for holistic positive-evidence development.

Every reported development rank in this module is produced by a model fitted
without that person.  The same DEVELOPMENT people may participate in other
folds' training sets; this is model-selection hygiene, not confirmatory
validation.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .holistic import (
    AblationResult,
    CandidateChart,
    HolisticEvaluationResult,
    HolisticPositiveEvidenceModel,
    MinimizationResult,
    PersonRankResult,
    PositiveEvidenceRecord,
    evaluate_identification,
)


class CrossFittedEvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["holistic-crossfit-v1"] = "holistic-crossfit-v1"
    model_id: str
    fold_count: int = Field(ge=2)
    people_evaluated: int
    fold_people_evaluated: tuple[int, ...]
    mean_percentile: float
    median_percentile: float
    mean_reciprocal_rank: float
    results: tuple[PersonRankResult, ...]


def deterministic_person_fold(participant_id: str, *, folds: int, seed: int) -> int:
    if folds < 2:
        raise ValueError("folds must be at least 2")
    digest = hashlib.sha256(f"{seed}:{participant_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % folds


def _combine_fold_results(
    model_id: str,
    folds: int,
    fold_results: Sequence[HolisticEvaluationResult],
) -> CrossFittedEvaluationResult:
    results = tuple(
        result
        for fold_result in fold_results
        for result in fold_result.results
    )
    if not results:
        raise ValueError("cross-fitting produced no evaluable people")
    percentiles = sorted(result.percentile for result in results)
    middle = len(percentiles) // 2
    median = (
        percentiles[middle]
        if len(percentiles) % 2
        else (percentiles[middle - 1] + percentiles[middle]) / 2.0
    )
    reciprocal_ranks = [
        1.0 / (result.candidate_count - result.true_rank_ascending + 1.0)
        for result in results
    ]
    return CrossFittedEvaluationResult(
        model_id=model_id,
        fold_count=folds,
        people_evaluated=len(results),
        fold_people_evaluated=tuple(result.people_evaluated for result in fold_results),
        mean_percentile=sum(result.percentile for result in results) / len(results),
        median_percentile=median,
        mean_reciprocal_rank=sum(reciprocal_ranks) / len(reciprocal_ranks),
        results=results,
    )


def cross_fitted_identification(
    records: Sequence[PositiveEvidenceRecord],
    charts: Sequence[CandidateChart],
    *,
    model_id: str,
    feature_names: Sequence[str],
    feature_clusters: Mapping[str, str] | None = None,
    alpha: float = 4.0,
    min_label_count: int = 10,
    folds: int = 5,
    fold_seed: int = 0,
    match_fields: Sequence[str] = (),
    max_decoys: int | None = None,
    decoy_seed: int = 0,
    enabled_features: Sequence[str] | None = None,
    created_at_utc: datetime | None = None,
) -> CrossFittedEvaluationResult:
    """Fit on K-1 DEVELOPMENT folds and rank charts for the held-out fold."""

    if not records:
        raise ValueError("at least one DEVELOPMENT record is required")
    if any(record.cohort != "development" for record in records):
        raise ValueError("cross-fitted identification is DEVELOPMENT-only")
    if len({record.participant_id for record in records}) != len(records):
        raise ValueError("participant_id values must be unique")

    assignments = {
        record.participant_id: deterministic_person_fold(
            record.participant_id,
            folds=folds,
            seed=fold_seed,
        )
        for record in records
    }
    fold_results: list[HolisticEvaluationResult] = []
    timestamp = created_at_utc or datetime.now(UTC)

    for fold in range(folds):
        training = tuple(
            record for record in records if assignments[record.participant_id] != fold
        )
        held_out = tuple(
            record for record in records if assignments[record.participant_id] == fold
        )
        if not training or not held_out:
            raise ValueError("deterministic fold assignment produced an empty fold")
        model = HolisticPositiveEvidenceModel.fit(
            training,
            model_id=f"{model_id}:fold-{fold}",
            feature_names=feature_names,
            feature_clusters=feature_clusters,
            alpha=alpha,
            min_label_count=min_label_count,
            created_at_utc=timestamp,
        )
        try:
            evaluation = evaluate_identification(
                model,
                held_out,
                charts,
                match_fields=match_fields,
                max_decoys=max_decoys,
                seed=decoy_seed,
                enabled_features=enabled_features,
                randomization_iterations=0,
            )
        except ValueError as exc:
            raise ValueError(f"fold {fold} is not evaluable: {exc}") from exc
        fold_results.append(evaluation)

    return _combine_fold_results(model_id, folds, fold_results)


def greedy_cross_fitted_minimize_feature_groups(
    records: Sequence[PositiveEvidenceRecord],
    charts: Sequence[CandidateChart],
    *,
    model_id: str,
    feature_names: Sequence[str],
    feature_groups: Mapping[str, Sequence[str]],
    feature_clusters: Mapping[str, str] | None = None,
    alpha: float = 4.0,
    min_label_count: int = 10,
    folds: int = 5,
    fold_seed: int = 0,
    match_fields: Sequence[str] = (),
    max_decoys: int | None = None,
    decoy_seed: int = 0,
    max_absolute_percentile_loss: float = 0.01,
    created_at_utc: datetime | None = None,
) -> MinimizationResult:
    """Ablate feature groups using only cross-fitted DEVELOPMENT performance."""

    if max_absolute_percentile_loss < 0.0:
        raise ValueError("max_absolute_percentile_loss must be nonnegative")
    features = tuple(feature_names)
    groups = {str(group): tuple(items) for group, items in feature_groups.items()}
    assigned: set[str] = set()
    for group, items in groups.items():
        if not items:
            raise ValueError(f"feature group {group} cannot be empty")
        unknown = set(items) - set(features)
        if unknown:
            raise ValueError(f"feature group {group} contains unknown features: {sorted(unknown)}")
        overlap = assigned.intersection(items)
        if overlap:
            raise ValueError(f"features appear in multiple groups: {sorted(overlap)}")
        assigned.update(items)
    omitted = set(features) - assigned
    if omitted:
        raise ValueError(f"feature groups omit model features: {sorted(omitted)}")

    timestamp = created_at_utc or datetime.now(UTC)

    def evaluate(enabled: Sequence[str]) -> CrossFittedEvaluationResult:
        return cross_fitted_identification(
            records,
            charts,
            model_id=model_id,
            feature_names=features,
            feature_clusters=feature_clusters,
            alpha=alpha,
            min_label_count=min_label_count,
            folds=folds,
            fold_seed=fold_seed,
            match_fields=match_fields,
            max_decoys=max_decoys,
            decoy_seed=decoy_seed,
            enabled_features=enabled,
            created_at_utc=timestamp,
        )

    current_groups = tuple(sorted(groups))
    current_features = tuple(
        feature for group in current_groups for feature in groups[group]
    )
    full = evaluate(current_features)
    full_score = full.mean_percentile
    path: list[AblationResult] = [
        AblationResult(
            enabled_groups=current_groups,
            enabled_features=tuple(sorted(current_features)),
            people_evaluated=full.people_evaluated,
            mean_percentile=full_score,
            loss_from_full=0.0,
        )
    ]

    while len(current_groups) > 1:
        candidates: list[
            tuple[float, str, CrossFittedEvaluationResult, tuple[str, ...]]
        ] = []
        for removed in current_groups:
            trial_groups = tuple(group for group in current_groups if group != removed)
            trial_features = tuple(
                feature for group in trial_groups for feature in groups[group]
            )
            trial = evaluate(trial_features)
            candidates.append(
                (full_score - trial.mean_percentile, removed, trial, trial_groups)
            )
        loss, _removed, best, best_groups = min(
            candidates,
            key=lambda item: (item[0], item[1]),
        )
        if loss > max_absolute_percentile_loss:
            break
        current_groups = best_groups
        current_features = tuple(
            feature for group in current_groups for feature in groups[group]
        )
        path.append(
            AblationResult(
                enabled_groups=current_groups,
                enabled_features=tuple(sorted(current_features)),
                people_evaluated=best.people_evaluated,
                mean_percentile=best.mean_percentile,
                loss_from_full=loss,
            )
        )

    return MinimizationResult(
        full_mean_percentile=full_score,
        retained_groups=current_groups,
        retained_features=tuple(sorted(current_features)),
        path=tuple(path),
    )
