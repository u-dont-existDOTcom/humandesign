"""Whole-profile positive-evidence chart identification and minimization.

This module deliberately treats unrecorded behaviors as unknown rather than as
contradictions. It is intended for sparse archival/profile datasets and rich
human case records where the observed positives are reliable but annotation
absence is not.

The model estimates chart-feature enrichment among people carrying each
observed label, relative to the feature's background prevalence. Candidate
charts are scored by the positive evidence actually observed for a person.
No term is added for a label that was not recorded for that person.

Development data may be used repeatedly for fitting, ablation, interaction
search, and minimization. The resulting model/object must be frozen before it
is used as confirmatory evidence on validation people.
"""

from __future__ import annotations

import hashlib
import math
import random
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.util import sha256_json


def _feature_token(value: Any) -> str:
    if isinstance(value, (list, tuple, set, frozenset)):
        return "|".join(sorted(str(item) for item in value))
    if isinstance(value, Mapping):
        return sha256_json(dict(sorted((str(key), value) for key, value in value.items())))
    return str(value)


class PositiveEvidenceRecord(BaseModel):
    """One person's observed positive evidence, chart, and decoy-matching strata."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str = Field(min_length=1)
    cohort: Literal["development", "validation", "final_test", "unassigned"]
    observed_labels: tuple[str, ...]
    chart_features: dict[str, Any]
    match_strata: dict[str, str] = Field(default_factory=dict)
    evidence_weights: dict[str, float] = Field(default_factory=dict)

    @field_validator("participant_id")
    @classmethod
    def normalize_participant_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("participant_id cannot be blank")
        return normalized

    @field_validator("observed_labels")
    @classmethod
    def normalize_observed_labels(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(sorted({item.strip() for item in value if item.strip()}))
        if not normalized:
            raise ValueError("at least one observed positive label is required")
        return normalized

    @model_validator(mode="after")
    def validate_weights(self) -> PositiveEvidenceRecord:
        unknown = set(self.evidence_weights) - set(self.observed_labels)
        if unknown:
            raise ValueError(f"weights supplied for unobserved labels: {sorted(unknown)}")
        invalid = sorted(
            label
            for label, weight in self.evidence_weights.items()
            if not math.isfinite(weight) or not 0.0 <= weight <= 1.0
        )
        if invalid:
            raise ValueError(f"evidence weights must be within [0, 1]: {invalid}")
        return self


class HolisticModelArtifact(BaseModel):
    """Frozen enrichment counts for positive-evidence whole-profile scoring."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["holistic-positive-evidence-v1"] = "holistic-positive-evidence-v1"
    model_id: str = Field(min_length=1)
    training_dataset_hash: str
    feature_names: tuple[str, ...]
    feature_clusters: dict[str, str]
    label_counts: dict[str, float]
    background_feature_counts: dict[str, dict[str, float]]
    label_feature_counts: dict[str, dict[str, dict[str, float]]]
    training_people: int = Field(gt=0)
    alpha: float = Field(gt=0.0)
    min_label_count: int = Field(ge=1)
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("holistic model timestamp must be timezone-aware")
        return value.astimezone(UTC)


class HolisticPositiveEvidenceModel:
    """Score observed positive labels against complete candidate charts.

    For each observed label and chart feature token the model compares the
    feature-token prevalence among people carrying that label with its
    prevalence in all training people. Feature contributions are averaged
    within declared dependency clusters so redundant flags cannot multiply
    support merely by being expanded into many fields.
    """

    def __init__(self, artifact: HolisticModelArtifact) -> None:
        self.artifact = artifact

    @classmethod
    def fit(
        cls,
        records: Sequence[PositiveEvidenceRecord],
        *,
        model_id: str,
        feature_names: Sequence[str],
        feature_clusters: Mapping[str, str] | None = None,
        alpha: float = 4.0,
        min_label_count: int = 10,
        created_at_utc: datetime | None = None,
    ) -> HolisticPositiveEvidenceModel:
        if not records:
            raise ValueError("at least one development person is required")
        if any(record.cohort != "development" for record in records):
            raise ValueError("holistic fitting is restricted to DEVELOPMENT people")
        features = tuple(feature_names)
        if not features or len(features) != len(set(features)):
            raise ValueError("feature_names must be a nonempty unique sequence")
        if alpha <= 0.0 or min_label_count < 1:
            raise ValueError("alpha must be positive and min_label_count >= 1")
        ids = [record.participant_id for record in records]
        if len(ids) != len(set(ids)):
            raise ValueError("training participant_id values must be unique")

        clusters = {
            feature: str((feature_clusters or {}).get(feature, feature))
            for feature in features
        }
        background: dict[str, Counter[str]] = {feature: Counter() for feature in features}
        raw_label_counts: Counter[str] = Counter()
        raw_label_feature: dict[str, dict[str, Counter[str]]] = defaultdict(
            lambda: {feature: Counter() for feature in features}
        )

        ordered = tuple(sorted(records, key=lambda record: record.participant_id))
        for record in ordered:
            for feature in features:
                if feature in record.chart_features:
                    background[feature][_feature_token(record.chart_features[feature])] += 1.0
            for label in record.observed_labels:
                weight = record.evidence_weights.get(label, 1.0)
                raw_label_counts[label] += weight
                for feature in features:
                    if feature in record.chart_features:
                        raw_label_feature[label][feature][
                            _feature_token(record.chart_features[feature])
                        ] += weight

        retained = {
            label for label, count in raw_label_counts.items() if count >= min_label_count
        }
        if not retained:
            raise ValueError("no observed label reaches min_label_count")

        payload = {
            "participants": [record.participant_id for record in ordered],
            "labels": {record.participant_id: record.observed_labels for record in ordered},
            "weights": {record.participant_id: record.evidence_weights for record in ordered},
            "features": {
                record.participant_id: {
                    feature: record.chart_features.get(feature)
                    for feature in features
                    if feature in record.chart_features
                }
                for record in ordered
            },
        }
        artifact = HolisticModelArtifact(
            model_id=model_id,
            training_dataset_hash=sha256_json(payload),
            feature_names=features,
            feature_clusters=clusters,
            label_counts={label: float(raw_label_counts[label]) for label in sorted(retained)},
            background_feature_counts={
                feature: dict(sorted(counter.items())) for feature, counter in background.items()
            },
            label_feature_counts={
                label: {
                    feature: dict(sorted(raw_label_feature[label][feature].items()))
                    for feature in features
                }
                for label in sorted(retained)
            },
            training_people=len(ordered),
            alpha=alpha,
            min_label_count=min_label_count,
            created_at_utc=created_at_utc or datetime.now(UTC),
        )
        return cls(artifact)

    @property
    def retained_labels(self) -> tuple[str, ...]:
        return tuple(sorted(self.artifact.label_counts))

    def score(
        self,
        observed_labels: Sequence[str],
        chart_features: Mapping[str, Any],
        *,
        evidence_weights: Mapping[str, float] | None = None,
        enabled_features: Sequence[str] | None = None,
    ) -> float:
        """Return positive-evidence log2 enrichment for one candidate chart."""

        enabled = (
            frozenset(enabled_features)
            if enabled_features is not None
            else frozenset(self.artifact.feature_names)
        )
        unknown_features = enabled - set(self.artifact.feature_names)
        if unknown_features:
            raise ValueError(f"unknown enabled features: {sorted(unknown_features)}")
        weights = evidence_weights or {}
        score = 0.0

        for label in observed_labels:
            if label not in self.artifact.label_counts:
                continue
            label_weight = float(weights.get(label, 1.0))
            if not math.isfinite(label_weight) or not 0.0 <= label_weight <= 1.0:
                raise ValueError("evidence weights must be finite within [0, 1]")
            cluster_terms: dict[str, list[float]] = defaultdict(list)
            label_n = self.artifact.label_counts[label]

            for feature in self.artifact.feature_names:
                if feature not in enabled or feature not in chart_features:
                    continue
                token = _feature_token(chart_features[feature])
                background_counts = self.artifact.background_feature_counts[feature]
                if not background_counts:
                    continue
                label_counts = self.artifact.label_feature_counts[label][feature]

                vocabulary = set(background_counts)
                vocabulary.add(token)
                k = max(len(vocabulary), 1)
                background_total = sum(background_counts.values())
                label_total = sum(label_counts.values())

                p_background = (
                    background_counts.get(token, 0.0) + self.artifact.alpha / k
                ) / (background_total + self.artifact.alpha)
                p_label = (
                    label_counts.get(token, 0.0) + self.artifact.alpha * p_background
                ) / (label_total + self.artifact.alpha)

                token_support = background_counts.get(token, 0.0)
                shrink_label = label_n / (label_n + self.artifact.alpha)
                shrink_token = token_support / (token_support + self.artifact.alpha)
                term = (
                    shrink_label
                    * shrink_token
                    * math.log2(max(p_label, 1e-12) / max(p_background, 1e-12))
                )
                cluster_terms[self.artifact.feature_clusters[feature]].append(term)

            if cluster_terms:
                label_score = sum(
                    sum(terms) / len(terms) for terms in cluster_terms.values()
                )
                score += label_weight * label_score
        return score


class CandidateChart(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    chart_id: str = Field(min_length=1)
    owner_participant_id: str | None = None
    chart_features: dict[str, Any]
    match_strata: dict[str, str] = Field(default_factory=dict)


class PersonRankResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str
    true_chart_id: str
    candidate_count: int = Field(ge=2)
    true_score: float
    true_rank_ascending: float
    percentile: float = Field(ge=0.0, le=1.0)
    match_fields: tuple[str, ...]


class HolisticEvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["holistic-evaluation-v1"] = "holistic-evaluation-v1"
    model_id: str
    people_evaluated: int
    mean_percentile: float
    median_percentile: float
    mean_reciprocal_rank: float
    randomization_p_value: float | None = None
    results: tuple[PersonRankResult, ...]


def _score_percentile(scores: Sequence[float], index: int) -> tuple[float, float]:
    target = scores[index]
    lower = sum(score < target for score in scores)
    equal = sum(math.isclose(score, target, rel_tol=0.0, abs_tol=1e-12) for score in scores)
    rank_ascending = lower + (equal + 1.0) / 2.0
    if len(scores) == 1:
        return rank_ascending, 0.5
    percentile = (rank_ascending - 1.0) / (len(scores) - 1.0)
    return rank_ascending, percentile


def rank_true_chart(
    model: HolisticPositiveEvidenceModel,
    person: PositiveEvidenceRecord,
    true_chart: CandidateChart,
    decoys: Sequence[CandidateChart],
    *,
    enabled_features: Sequence[str] | None = None,
    match_fields: Sequence[str] = (),
) -> PersonRankResult:
    if true_chart.owner_participant_id not in (None, person.participant_id):
        raise ValueError("true chart owner does not match participant")
    candidates = (true_chart, *decoys)
    if len(candidates) < 2:
        raise ValueError("at least one decoy chart is required")
    if len({candidate.chart_id for candidate in candidates}) != len(candidates):
        raise ValueError("candidate chart_id values must be unique")

    required_match = tuple(match_fields)
    for candidate in candidates:
        for field in required_match:
            if candidate.match_strata.get(field) != person.match_strata.get(field):
                raise ValueError(f"candidate {candidate.chart_id} mismatches stratum {field}")

    scores = [
        model.score(
            person.observed_labels,
            candidate.chart_features,
            evidence_weights=person.evidence_weights,
            enabled_features=enabled_features,
        )
        for candidate in candidates
    ]
    rank, percentile = _score_percentile(scores, 0)
    return PersonRankResult(
        participant_id=person.participant_id,
        true_chart_id=true_chart.chart_id,
        candidate_count=len(candidates),
        true_score=scores[0],
        true_rank_ascending=rank,
        percentile=percentile,
        match_fields=required_match,
    )


def _deterministic_sample(
    values: Sequence[CandidateChart],
    count: int,
    *,
    seed: int,
    participant_id: str,
) -> tuple[CandidateChart, ...]:
    if count >= len(values):
        return tuple(values)
    digest = hashlib.sha256(f"{seed}:{participant_id}".encode("utf-8")).digest()
    rng = random.Random(int.from_bytes(digest[:8], "big"))
    indices = sorted(rng.sample(range(len(values)), count))
    return tuple(values[index] for index in indices)


def evaluate_identification(
    model: HolisticPositiveEvidenceModel,
    people: Sequence[PositiveEvidenceRecord],
    charts: Sequence[CandidateChart],
    *,
    match_fields: Sequence[str] = (),
    max_decoys: int | None = None,
    seed: int = 0,
    enabled_features: Sequence[str] | None = None,
    randomization_iterations: int = 0,
) -> HolisticEvaluationResult:
    """Rank each person's true chart against matched charts from other people."""

    if max_decoys is not None and max_decoys < 1:
        raise ValueError("max_decoys must be at least 1")
    chart_by_owner: dict[str, CandidateChart] = {}
    for chart in charts:
        if chart.owner_participant_id is None:
            continue
        if chart.owner_participant_id in chart_by_owner:
            raise ValueError("one true chart per owner is required")
        chart_by_owner[chart.owner_participant_id] = chart

    results: list[PersonRankResult] = []
    score_vectors: list[tuple[float, ...]] = []
    required_match = tuple(match_fields)

    for person in people:
        true_chart = chart_by_owner.get(person.participant_id)
        if true_chart is None:
            continue
        decoys = [
            chart
            for chart in charts
            if chart.owner_participant_id != person.participant_id
            and all(
                chart.match_strata.get(field) == person.match_strata.get(field)
                for field in required_match
            )
        ]
        if not decoys:
            continue
        if max_decoys is not None:
            decoys = list(
                _deterministic_sample(
                    decoys,
                    max_decoys,
                    seed=seed,
                    participant_id=person.participant_id,
                )
            )
        result = rank_true_chart(
            model,
            person,
            true_chart,
            decoys,
            enabled_features=enabled_features,
            match_fields=required_match,
        )
        results.append(result)
        candidates = (true_chart, *decoys)
        score_vectors.append(
            tuple(
                model.score(
                    person.observed_labels,
                    candidate.chart_features,
                    evidence_weights=person.evidence_weights,
                    enabled_features=enabled_features,
                )
                for candidate in candidates
            )
        )

    if not results:
        raise ValueError("no evaluable people had a true chart plus matched decoy")

    percentiles = [result.percentile for result in results]
    reciprocal_ranks = [
        1.0 / (result.candidate_count - result.true_rank_ascending + 1.0)
        for result in results
    ]
    sorted_percentiles = sorted(percentiles)
    middle = len(sorted_percentiles) // 2
    if len(sorted_percentiles) % 2:
        median = sorted_percentiles[middle]
    else:
        median = (sorted_percentiles[middle - 1] + sorted_percentiles[middle]) / 2.0

    p_value: float | None = None
    if randomization_iterations > 0:
        rng = random.Random(seed)
        observed_mean = sum(percentiles) / len(percentiles)
        ge = 0
        for _ in range(randomization_iterations):
            null_percentiles: list[float] = []
            for vector in score_vectors:
                selected = rng.randrange(len(vector))
                _, percentile = _score_percentile(vector, selected)
                null_percentiles.append(percentile)
            if sum(null_percentiles) / len(null_percentiles) >= observed_mean:
                ge += 1
        p_value = (ge + 1.0) / (randomization_iterations + 1.0)

    return HolisticEvaluationResult(
        model_id=model.artifact.model_id,
        people_evaluated=len(results),
        mean_percentile=sum(percentiles) / len(percentiles),
        median_percentile=median,
        mean_reciprocal_rank=sum(reciprocal_ranks) / len(reciprocal_ranks),
        randomization_p_value=p_value,
        results=tuple(results),
    )


class AblationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled_groups: tuple[str, ...]
    enabled_features: tuple[str, ...]
    people_evaluated: int
    mean_percentile: float
    loss_from_full: float


class MinimizationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["holistic-minimization-v1"] = "holistic-minimization-v1"
    full_mean_percentile: float
    retained_groups: tuple[str, ...]
    retained_features: tuple[str, ...]
    path: tuple[AblationResult, ...]


def greedy_minimize_feature_groups(
    model: HolisticPositiveEvidenceModel,
    people: Sequence[PositiveEvidenceRecord],
    charts: Sequence[CandidateChart],
    *,
    feature_groups: Mapping[str, Sequence[str]],
    match_fields: Sequence[str] = (),
    max_decoys: int | None = None,
    seed: int = 0,
    max_absolute_percentile_loss: float = 0.01,
) -> MinimizationResult:
    """Greedily remove feature groups while preserving whole-profile ranking.

    This is a DEVELOPMENT optimization tool. Callers are responsible for not
    using validation outcomes to choose the retained groups.
    """

    if any(person.cohort != "development" for person in people):
        raise ValueError("feature minimization is restricted to DEVELOPMENT people")
    if max_absolute_percentile_loss < 0.0:
        raise ValueError("max_absolute_percentile_loss must be nonnegative")
    groups = {str(name): tuple(features) for name, features in feature_groups.items()}
    assigned: set[str] = set()
    for group, features in groups.items():
        if not features:
            raise ValueError(f"feature group {group} cannot be empty")
        unknown = set(features) - set(model.artifact.feature_names)
        if unknown:
            raise ValueError(f"feature group {group} contains unknown features: {sorted(unknown)}")
        overlap = assigned.intersection(features)
        if overlap:
            raise ValueError(f"features appear in multiple groups: {sorted(overlap)}")
        assigned.update(features)

    ungrouped = set(model.artifact.feature_names) - assigned
    if ungrouped:
        raise ValueError(f"feature groups omit model features: {sorted(ungrouped)}")

    current_groups = tuple(sorted(groups))
    current_features = tuple(feature for group in current_groups for feature in groups[group])
    full_eval = evaluate_identification(
        model,
        people,
        charts,
        match_fields=match_fields,
        max_decoys=max_decoys,
        seed=seed,
        enabled_features=current_features,
    )
    full_score = full_eval.mean_percentile
    path: list[AblationResult] = [
        AblationResult(
            enabled_groups=current_groups,
            enabled_features=tuple(sorted(current_features)),
            people_evaluated=full_eval.people_evaluated,
            mean_percentile=full_score,
            loss_from_full=0.0,
        )
    ]

    while len(current_groups) > 1:
        candidates: list[tuple[float, str, HolisticEvaluationResult, tuple[str, ...]]] = []
        for remove_group in current_groups:
            trial_groups = tuple(group for group in current_groups if group != remove_group)
            trial_features = tuple(feature for group in trial_groups for feature in groups[group])
            evaluation = evaluate_identification(
                model,
                people,
                charts,
                match_fields=match_fields,
                max_decoys=max_decoys,
                seed=seed,
                enabled_features=trial_features,
            )
            candidates.append(
                (full_score - evaluation.mean_percentile, remove_group, evaluation, trial_groups)
            )
        loss, _removed, best_eval, best_groups = min(
            candidates, key=lambda item: (item[0], item[1])
        )
        if loss > max_absolute_percentile_loss:
            break
        current_groups = best_groups
        current_features = tuple(feature for group in current_groups for feature in groups[group])
        path.append(
            AblationResult(
                enabled_groups=current_groups,
                enabled_features=tuple(sorted(current_features)),
                people_evaluated=best_eval.people_evaluated,
                mean_percentile=best_eval.mean_percentile,
                loss_from_full=loss,
            )
        )

    return MinimizationResult(
        full_mean_percentile=full_score,
        retained_groups=current_groups,
        retained_features=tuple(sorted(current_features)),
        path=tuple(path),
    )
