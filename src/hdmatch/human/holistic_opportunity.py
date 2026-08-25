"""Opportunity-conditioned, source-blocked whole-chart neighborhood scoring.

Sparse archival annotations are positive-unlabeled data. A missing label is not
an observed negative, and a missing ontology branch is not even evidence that
the construct was assessed. This module therefore estimates each label only
among training people who have at least one annotation in that label's declared
opportunity cluster.

The neighborhood may additionally be blocked by source/site fields. Blocking
is applied to the TRAINING pool as well as candidate matching; matching decoys
by source while allowing the model to learn across source corpora is not a
sufficient control for archive-selection leakage.

All routines here are for DEVELOPMENT/model-selection unless a completely
frozen instance is later carried unchanged to independent validation data.
"""

from __future__ import annotations

import hashlib
import math
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .holistic import CandidateChart, PersonRankResult, PositiveEvidenceRecord
from .holistic_cv import deterministic_person_fold


def taxonomy_opportunity(label: str) -> str:
    """Return a conservative observation-opportunity cluster for ADB-like labels.

    ``Vocation`` is treated as one opportunity because its children are alternate
    occupational classifications. Other hierarchical labels use the first two
    taxonomy levels, e.g. ``Family : Relationship`` or ``Traits : Personality``.
    Callers with a different ontology should supply an explicit mapping instead.
    """

    parts = tuple(part.strip() for part in label.split(":") if part.strip())
    if not parts:
        raise ValueError("label cannot be blank")
    if parts[0].casefold() == "vocation":
        return parts[0]
    return " : ".join(parts[: min(2, len(parts))])


def build_label_opportunities(labels: Sequence[str]) -> dict[str, str]:
    return {label: taxonomy_opportunity(label) for label in sorted(set(labels))}


def _feature_token(value: Any) -> str:
    if isinstance(value, (tuple, list, set, frozenset)):
        return "|".join(sorted(str(item) for item in value))
    return str(value)


def _block_key(strata: Mapping[str, str], fields: Sequence[str]) -> tuple[str, ...]:
    return tuple(str(strata.get(field, "")) for field in fields)


@dataclass(frozen=True, slots=True)
class _TrainingRow:
    participant_id: str
    feature_tokens: tuple[str, ...]
    observed_labels: frozenset[str]
    opportunities: frozenset[str]
    block_key: tuple[str, ...]


class OpportunityNeighborArtifact(BaseModel):
    """Auditable configuration/provenance for a fitted development model."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["opportunity-neighbor-v1"] = "opportunity-neighbor-v1"
    model_id: str = Field(min_length=1)
    feature_names: tuple[str, ...]
    label_opportunities: dict[str, str]
    training_block_fields: tuple[str, ...]
    neighbor_count: int = Field(ge=1)
    alpha: float = Field(gt=0.0)
    min_label_count: int = Field(ge=1)
    min_opportunity_count: int = Field(ge=1)
    training_people: int = Field(ge=1)
    training_dataset_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class OpportunityConditionedNeighborModel:
    """K-nearest categorical whole-chart scorer with missing-as-unknown semantics."""

    def __init__(
        self,
        artifact: OpportunityNeighborArtifact,
        rows: Sequence[_TrainingRow],
    ) -> None:
        self.artifact = artifact
        self._rows = tuple(rows)
        by_block: dict[tuple[str, ...], list[_TrainingRow]] = defaultdict(list)
        for row in self._rows:
            by_block[row.block_key].append(row)
        self._rows_by_block = {
            key: tuple(sorted(values, key=lambda item: item.participant_id))
            for key, values in by_block.items()
        }

    @classmethod
    def fit(
        cls,
        records: Sequence[PositiveEvidenceRecord],
        *,
        model_id: str,
        feature_names: Sequence[str],
        label_opportunities: Mapping[str, str] | None = None,
        training_block_fields: Sequence[str] = (),
        neighbor_count: int = 200,
        alpha: float = 4.0,
        min_label_count: int = 5,
        min_opportunity_count: int = 20,
    ) -> OpportunityConditionedNeighborModel:
        if not records:
            raise ValueError("at least one DEVELOPMENT training record is required")
        if any(record.cohort != "development" for record in records):
            raise ValueError("opportunity-conditioned fitting is DEVELOPMENT-only")
        identifiers = [record.participant_id for record in records]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("training participant_id values must be unique")
        features = tuple(feature_names)
        if not features or len(features) != len(set(features)):
            raise ValueError("feature_names must be a nonempty unique sequence")
        if neighbor_count < 1 or alpha <= 0.0:
            raise ValueError("neighbor_count and alpha must be positive")
        if min_label_count < 1 or min_opportunity_count < 1:
            raise ValueError("minimum counts must be at least one")
        block_fields = tuple(training_block_fields)
        if len(block_fields) != len(set(block_fields)):
            raise ValueError("training_block_fields must be unique")

        observed_universe = sorted(
            {label for record in records for label in record.observed_labels}
        )
        opportunities = (
            build_label_opportunities(observed_universe)
            if label_opportunities is None
            else {str(label): str(value) for label, value in label_opportunities.items()}
        )
        missing = set(observed_universe) - set(opportunities)
        if missing:
            raise ValueError(f"label_opportunities missing labels: {sorted(missing)}")
        if any(not value.strip() for value in opportunities.values()):
            raise ValueError("opportunity cluster names cannot be blank")

        rows: list[_TrainingRow] = []
        payload_rows: list[dict[str, object]] = []
        for record in sorted(records, key=lambda item: item.participant_id):
            absent_features = set(features) - set(record.chart_features)
            if absent_features:
                raise ValueError(
                    f"record {record.participant_id} lacks chart features: "
                    f"{sorted(absent_features)}"
                )
            labels = frozenset(record.observed_labels)
            row_opportunities = frozenset(opportunities[label] for label in labels)
            tokens = tuple(_feature_token(record.chart_features[name]) for name in features)
            block = _block_key(record.match_strata, block_fields)
            rows.append(
                _TrainingRow(
                    participant_id=record.participant_id,
                    feature_tokens=tokens,
                    observed_labels=labels,
                    opportunities=row_opportunities,
                    block_key=block,
                )
            )
            payload_rows.append(
                {
                    "id": record.participant_id,
                    "features": tokens,
                    "labels": sorted(labels),
                    "opportunities": sorted(row_opportunities),
                    "block": block,
                }
            )
        digest = hashlib.sha256(
            repr((features, sorted(opportunities.items()), block_fields, payload_rows)).encode()
        ).hexdigest()
        artifact = OpportunityNeighborArtifact(
            model_id=model_id,
            feature_names=features,
            label_opportunities=opportunities,
            training_block_fields=block_fields,
            neighbor_count=neighbor_count,
            alpha=alpha,
            min_label_count=min_label_count,
            min_opportunity_count=min_opportunity_count,
            training_people=len(rows),
            training_dataset_sha256=digest,
        )
        return cls(artifact, rows)

    def _candidate_tokens(self, chart: CandidateChart) -> tuple[str, ...]:
        missing = set(self.artifact.feature_names) - set(chart.chart_features)
        if missing:
            raise ValueError(f"candidate {chart.chart_id} lacks features: {sorted(missing)}")
        return tuple(
            _feature_token(chart.chart_features[name])
            for name in self.artifact.feature_names
        )

    @staticmethod
    def _similarity(left: Sequence[str], right: Sequence[str]) -> int:
        return sum(a == b for a, b in zip(left, right, strict=True))

    def score_candidate(
        self,
        person: PositiveEvidenceRecord,
        chart: CandidateChart,
    ) -> float | None:
        """Score observed positives; return ``None`` if no label is estimable."""

        block = _block_key(chart.match_strata, self.artifact.training_block_fields)
        pool = self._rows_by_block.get(block, ())
        candidate_tokens = self._candidate_tokens(chart)
        score = 0.0
        used_labels = 0
        for label in person.observed_labels:
            opportunity = self.artifact.label_opportunities.get(label)
            if opportunity is None:
                continue
            opportunity_pool = tuple(
                row for row in pool if opportunity in row.opportunities
            )
            if len(opportunity_pool) < max(
                self.artifact.neighbor_count,
                self.artifact.min_opportunity_count,
            ):
                continue
            global_positive = sum(
                label in row.observed_labels for row in opportunity_pool
            )
            if global_positive < self.artifact.min_label_count:
                continue
            nearest = tuple(
                sorted(
                    opportunity_pool,
                    key=lambda row: (
                        -self._similarity(candidate_tokens, row.feature_tokens),
                        row.participant_id,
                    ),
                )[: self.artifact.neighbor_count]
            )
            global_rate = global_positive / len(opportunity_pool)
            local_positive = sum(label in row.observed_labels for row in nearest)
            local_rate = (
                local_positive + self.artifact.alpha * global_rate
            ) / (len(nearest) + self.artifact.alpha)
            weight = float(person.evidence_weights.get(label, 1.0))
            if not math.isfinite(weight) or not 0.0 <= weight <= 1.0:
                raise ValueError("evidence weights must be finite within [0, 1]")
            score += weight * math.log2(
                max(local_rate, 1e-12) / max(global_rate, 1e-12)
            )
            used_labels += 1
        return score if used_labels else None


class OpportunityCrossFitResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["opportunity-neighbor-crossfit-v1"] = (
        "opportunity-neighbor-crossfit-v1"
    )
    model_id: str
    fold_count: int = Field(ge=2)
    people_evaluated: int
    people_skipped_unestimable: int
    mean_percentile: float
    median_percentile: float
    randomization_p_value: float | None
    results: tuple[PersonRankResult, ...]


def _percentile(scores: Sequence[float], index: int) -> tuple[float, float]:
    target = scores[index]
    lower = sum(score < target for score in scores)
    equal = sum(
        math.isclose(score, target, abs_tol=1e-12, rel_tol=0.0) for score in scores
    )
    rank = lower + (equal + 1.0) / 2.0
    return rank, (rank - 1.0) / (len(scores) - 1.0)


def cross_fitted_opportunity_identification(
    records: Sequence[PositiveEvidenceRecord],
    charts: Sequence[CandidateChart],
    *,
    model_id: str,
    feature_names: Sequence[str],
    label_opportunities: Mapping[str, str] | None = None,
    training_block_fields: Sequence[str] = (),
    candidate_match_fields: Sequence[str] = (),
    neighbor_count: int = 200,
    alpha: float = 4.0,
    min_label_count: int = 5,
    min_opportunity_count: int = 20,
    folds: int = 5,
    fold_seed: int = 0,
    max_decoys: int = 200,
    decoy_seed: int = 0,
    randomization_iterations: int = 0,
) -> OpportunityCrossFitResult:
    """Cross-fit whole-chart identification with training-source blocking.

    Training block fields must also be candidate-match fields. This keeps every
    chart in one person's comparison set on the same fitted source/site baseline.
    """

    block_fields = tuple(training_block_fields)
    match_fields = tuple(candidate_match_fields)
    if not set(block_fields).issubset(match_fields):
        raise ValueError(
            "training_block_fields must be included in candidate_match_fields"
        )
    if max_decoys < 1:
        raise ValueError("max_decoys must be at least one")
    if any(record.cohort != "development" for record in records):
        raise ValueError("cross-fitted opportunity evaluation is DEVELOPMENT-only")
    chart_by_owner = {
        chart.owner_participant_id: chart
        for chart in charts
        if chart.owner_participant_id is not None
    }
    chart_owner_count = sum(chart.owner_participant_id is not None for chart in charts)
    if len(chart_by_owner) != chart_owner_count:
        raise ValueError("one chart per owner is required")
    assignments = {
        record.participant_id: deterministic_person_fold(
            record.participant_id, folds=folds, seed=fold_seed
        )
        for record in records
    }
    all_results: list[PersonRankResult] = []
    score_vectors: list[tuple[float, ...]] = []
    skipped = 0

    for fold in range(folds):
        training = tuple(
            record for record in records if assignments[record.participant_id] != fold
        )
        held_out = tuple(
            record for record in records if assignments[record.participant_id] == fold
        )
        model = OpportunityConditionedNeighborModel.fit(
            training,
            model_id=f"{model_id}:fold-{fold}",
            feature_names=feature_names,
            label_opportunities=label_opportunities,
            training_block_fields=block_fields,
            neighbor_count=neighbor_count,
            alpha=alpha,
            min_label_count=min_label_count,
            min_opportunity_count=min_opportunity_count,
        )
        for person in held_out:
            true_chart = chart_by_owner.get(person.participant_id)
            if true_chart is None:
                skipped += 1
                continue
            candidates = [
                chart
                for chart in charts
                if chart.owner_participant_id != person.participant_id
                and all(
                    chart.match_strata.get(field) == person.match_strata.get(field)
                    for field in match_fields
                )
            ]
            digest = hashlib.sha256(
                f"{decoy_seed}:{person.participant_id}".encode()
            ).digest()
            rng = random.Random(int.from_bytes(digest[:8], "big"))
            if len(candidates) > max_decoys:
                indices = sorted(rng.sample(range(len(candidates)), max_decoys))
                candidates = [candidates[index] for index in indices]
            scored: list[tuple[CandidateChart, float]] = []
            true_score = model.score_candidate(person, true_chart)
            if true_score is None:
                skipped += 1
                continue
            for candidate in candidates:
                candidate_score = model.score_candidate(person, candidate)
                if candidate_score is not None:
                    scored.append((candidate, candidate_score))
            if not scored:
                skipped += 1
                continue
            vector = (true_score, *(value for _chart, value in scored))
            rank, percentile = _percentile(vector, 0)
            all_results.append(
                PersonRankResult(
                    participant_id=person.participant_id,
                    true_chart_id=true_chart.chart_id,
                    candidate_count=len(vector),
                    true_score=true_score,
                    true_rank_ascending=rank,
                    percentile=percentile,
                    match_fields=match_fields,
                )
            )
            score_vectors.append(vector)

    if not all_results:
        raise ValueError("no evaluable people after opportunity/source controls")
    percentiles = [result.percentile for result in all_results]
    ordered = sorted(percentiles)
    mid = len(ordered) // 2
    median = (
        ordered[mid]
        if len(ordered) % 2
        else (ordered[mid - 1] + ordered[mid]) / 2
    )

    p_value: float | None = None
    if randomization_iterations > 0:
        rng = random.Random(decoy_seed)
        observed = sum(percentiles) / len(percentiles)
        ge = 0
        for _ in range(randomization_iterations):
            null_values = []
            for vector in score_vectors:
                selected = rng.randrange(len(vector))
                _, value = _percentile(vector, selected)
                null_values.append(value)
            if sum(null_values) / len(null_values) >= observed:
                ge += 1
        p_value = (ge + 1.0) / (randomization_iterations + 1.0)

    return OpportunityCrossFitResult(
        model_id=model_id,
        fold_count=folds,
        people_evaluated=len(all_results),
        people_skipped_unestimable=skipped,
        mean_percentile=sum(percentiles) / len(percentiles),
        median_percentile=median,
        randomization_p_value=p_value,
        results=tuple(all_results),
    )
