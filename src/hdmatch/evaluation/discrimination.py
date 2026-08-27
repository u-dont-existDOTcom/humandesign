"""Information-theoretic discrimination audit for century-wide candidate universes.

This module measures what the frozen symbolic model can distinguish before any
participant responses are observed.  The quantities here are partition entropies
and oracle ceilings, not claims about behavioral validity or probabilities that
Human Design is true.
"""

from __future__ import annotations

import math
from collections.abc import Hashable, Sequence
from dataclasses import dataclass, field
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.model.mapping_library import MappingLibrary, MappingRule
from hdmatch.runtime.century_cache import CenturyCacheManifest, GlobalCandidateState
from hdmatch.schemas import StructuralChartFeatures

_NO_UNIQUE_PREDICTION: Final[str] = "__no_unique_prediction__"
_TOP_K: Final[tuple[int, ...]] = (1, 5, 10)


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class FingerprintMetrics(_FrozenModel):
    """Discrimination of one deterministic fingerprint over a candidate universe."""

    candidate_count: int = Field(ge=1)
    unique_fingerprints: int = Field(ge=1)
    maximum_identity_bits: float = Field(ge=0.0)
    uniform_information_bits: float = Field(ge=0.0)
    duration_weighted_information_bits: float = Field(ge=0.0)
    uniform_top1_ceiling: float = Field(ge=0.0, le=1.0)
    uniform_top5_ceiling: float = Field(ge=0.0, le=1.0)
    uniform_top10_ceiling: float = Field(ge=0.0, le=1.0)
    duration_weighted_top1_ceiling: float = Field(ge=0.0, le=1.0)
    duration_weighted_top5_ceiling: float = Field(ge=0.0, le=1.0)
    duration_weighted_top10_ceiling: float = Field(ge=0.0, le=1.0)
    tie_size_p50: int = Field(ge=1)
    tie_size_p90: int = Field(ge=1)
    tie_size_p95: int = Field(ge=1)
    tie_size_max: int = Field(ge=1)


class QuestionInformation(_FrozenModel):
    """How much one model-visible question partitions the century universe."""

    question_id: str = Field(min_length=1)
    distinct_signatures: int = Field(ge=1)
    uniform_information_bits: float = Field(ge=0.0)
    duration_weighted_information_bits: float = Field(ge=0.0)
    largest_tie_group: int = Field(ge=1)


class CenturyDiscriminationAudit(_FrozenModel):
    """Auditable discrimination ceiling for the current frozen mapping library."""

    schema_version: str = "century-discrimination-audit-v1"
    cache_interval_count: int = Field(ge=1)
    cache_engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    cache_canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    mapping_library_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    model_predicate_features: tuple[str, ...]
    cached_features_not_model_visible: tuple[str, ...]
    coarse_structure: FingerprintMetrics
    canonical_answers: FingerprintMetrics
    scoring_rules: FingerprintMetrics
    full_cached_structure: FingerprintMetrics
    canonical_question_information: tuple[QuestionInformation, ...]
    scoring_question_information: tuple[QuestionInformation, ...]


@dataclass
class _GroupStat:
    count: int = 0
    total_duration: float = 0.0
    top_durations: list[float] = field(default_factory=list)

    def add(self, duration: float) -> None:
        self.count += 1
        self.total_duration += duration
        self.top_durations.append(duration)
        self.top_durations.sort(reverse=True)
        del self.top_durations[max(_TOP_K) :]


class _PartitionAccumulator:
    def __init__(self) -> None:
        self.groups: dict[Hashable, _GroupStat] = {}
        self.candidate_count = 0
        self.total_duration = 0.0

    def add(self, fingerprint: Hashable, duration: float) -> None:
        if duration <= 0.0:
            raise ValueError("candidate duration must be positive")
        group = self.groups.setdefault(fingerprint, _GroupStat())
        group.add(duration)
        self.candidate_count += 1
        self.total_duration += duration

    def metrics(self) -> FingerprintMetrics:
        if self.candidate_count == 0 or self.total_duration <= 0.0:
            raise ValueError("cannot summarize an empty fingerprint partition")
        counts = tuple(group.count for group in self.groups.values())
        uniform_bits = _entropy(tuple(count / self.candidate_count for count in counts))
        duration_bits = _entropy(
            tuple(group.total_duration / self.total_duration for group in self.groups.values())
        )
        uniform_top = {
            k: sum(min(k, count) for count in counts) / self.candidate_count for k in _TOP_K
        }
        duration_top = {
            k: sum(
                sum(group.top_durations[:k]) for group in self.groups.values()
            )
            / self.total_duration
            for k in _TOP_K
        }
        return FingerprintMetrics(
            candidate_count=self.candidate_count,
            unique_fingerprints=len(self.groups),
            maximum_identity_bits=math.log2(self.candidate_count),
            uniform_information_bits=uniform_bits,
            duration_weighted_information_bits=duration_bits,
            uniform_top1_ceiling=uniform_top[1],
            uniform_top5_ceiling=uniform_top[5],
            uniform_top10_ceiling=uniform_top[10],
            duration_weighted_top1_ceiling=duration_top[1],
            duration_weighted_top5_ceiling=duration_top[5],
            duration_weighted_top10_ceiling=duration_top[10],
            tie_size_p50=_candidate_weighted_tie_quantile(counts, 0.50),
            tie_size_p90=_candidate_weighted_tie_quantile(counts, 0.90),
            tie_size_p95=_candidate_weighted_tie_quantile(counts, 0.95),
            tie_size_max=max(counts),
        )

    def question_information(self, question_id: str) -> QuestionInformation:
        metrics = self.metrics()
        return QuestionInformation(
            question_id=question_id,
            distinct_signatures=metrics.unique_fingerprints,
            uniform_information_bits=metrics.uniform_information_bits,
            duration_weighted_information_bits=metrics.duration_weighted_information_bits,
            largest_tie_group=metrics.tie_size_max,
        )


def summarize_fingerprints(
    fingerprints: Sequence[Hashable], durations_seconds: Sequence[float]
) -> FingerprintMetrics:
    """Summarize an arbitrary deterministic partition; useful for tests and audits."""

    if len(fingerprints) != len(durations_seconds):
        raise ValueError("fingerprints and durations must have equal length")
    accumulator = _PartitionAccumulator()
    for fingerprint, duration in zip(fingerprints, durations_seconds, strict=True):
        accumulator.add(fingerprint, duration)
    return accumulator.metrics()


def audit_century_discrimination(
    states: Sequence[GlobalCandidateState],
    manifest: CenturyCacheManifest,
    library: MappingLibrary,
) -> CenturyDiscriminationAudit:
    """Measure present model discrimination without fitting or participant evidence."""

    if not states:
        raise ValueError("century discrimination audit requires candidate states")
    if len(states) != manifest.interval_count:
        raise ValueError("candidate state count does not match century-cache manifest")

    question_ids = tuple(sorted(spec.question_id for spec in library.answer_specs))
    mappings_by_question = _mappings_by_question(library, question_ids)
    predicate_features = tuple(
        sorted(
            {
                mapping.chart_feature_predicate.feature
                for mapping in library.frozen_mappings
                if mapping.chart_feature_predicate is not None
            }
        )
    )
    cached_extra = tuple(
        feature
        for feature in ("definition", "channels", "activation_gates")
        if feature not in predicate_features
    )

    coarse_partition = _PartitionAccumulator()
    canonical_partition = _PartitionAccumulator()
    scoring_partition = _PartitionAccumulator()
    full_partition = _PartitionAccumulator()
    canonical_questions = {question_id: _PartitionAccumulator() for question_id in question_ids}
    scoring_questions = {question_id: _PartitionAccumulator() for question_id in question_ids}

    model_cache: dict[
        tuple[str, str, str, str, tuple[str, ...]],
        tuple[tuple[str, ...], tuple[tuple[str, ...], ...]],
    ] = {}

    for state in states:
        features = state.chart_features
        duration = (state.end_utc - state.start_utc).total_seconds()
        coarse_key = _coarse_key(features)
        if coarse_key not in model_cache:
            model_cache[coarse_key] = _model_fingerprints(
                features, question_ids, mappings_by_question
            )
        canonical_fingerprint, scoring_fingerprint = model_cache[coarse_key]

        coarse_partition.add(coarse_key, duration)
        canonical_partition.add(canonical_fingerprint, duration)
        scoring_partition.add(scoring_fingerprint, duration)
        full_partition.add(_full_cached_key(features), duration)
        for index, question_id in enumerate(question_ids):
            canonical_questions[question_id].add(canonical_fingerprint[index], duration)
            scoring_questions[question_id].add(scoring_fingerprint[index], duration)

    canonical_information = tuple(
        sorted(
            (
                accumulator.question_information(question_id)
                for question_id, accumulator in canonical_questions.items()
            ),
            key=lambda item: (-item.duration_weighted_information_bits, item.question_id),
        )
    )
    scoring_information = tuple(
        sorted(
            (
                accumulator.question_information(question_id)
                for question_id, accumulator in scoring_questions.items()
            ),
            key=lambda item: (-item.duration_weighted_information_bits, item.question_id),
        )
    )

    return CenturyDiscriminationAudit(
        cache_interval_count=manifest.interval_count,
        cache_engine_fingerprint=manifest.engine_fingerprint,
        cache_canonical_rows_sha256=manifest.canonical_rows_sha256,
        mapping_library_sha256=library.sha256(),
        model_predicate_features=predicate_features,
        cached_features_not_model_visible=cached_extra,
        coarse_structure=coarse_partition.metrics(),
        canonical_answers=canonical_partition.metrics(),
        scoring_rules=scoring_partition.metrics(),
        full_cached_structure=full_partition.metrics(),
        canonical_question_information=canonical_information,
        scoring_question_information=scoring_information,
    )


def _mappings_by_question(
    library: MappingLibrary, question_ids: Sequence[str]
) -> dict[str, tuple[MappingRule, ...]]:
    grouped: dict[str, list[MappingRule]] = {question_id: [] for question_id in question_ids}
    for mapping in library.frozen_mappings:
        for question_id in mapping.question_ids:
            grouped.setdefault(question_id, []).append(mapping)
    return {
        question_id: tuple(sorted(mappings, key=lambda mapping: mapping.mapping_id))
        for question_id, mappings in grouped.items()
    }


def _model_fingerprints(
    features: StructuralChartFeatures,
    question_ids: Sequence[str],
    mappings_by_question: dict[str, tuple[MappingRule, ...]],
) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    canonical: list[str] = []
    scoring: list[tuple[str, ...]] = []
    for question_id in question_ids:
        matches = tuple(
            mapping
            for mapping in mappings_by_question.get(question_id, ())
            if mapping.chart_feature_predicate is not None
            and mapping.chart_feature_predicate.matches(features)
        )
        tokens = {
            mapping.predicted_response.canonical_answer_token
            for mapping in matches
            if mapping.predicted_response is not None
        }
        canonical.append(next(iter(tokens)) if len(tokens) == 1 else _NO_UNIQUE_PREDICTION)
        scoring.append(tuple(mapping.mapping_id for mapping in matches))
    return tuple(canonical), tuple(scoring)


def _coarse_key(
    features: StructuralChartFeatures,
) -> tuple[str, str, str, str, tuple[str, ...]]:
    return (
        features.type,
        features.strategy,
        features.authority,
        features.profile,
        tuple(sorted(features.defined_centers)),
    )


def _full_cached_key(features: StructuralChartFeatures) -> Hashable:
    return (
        features.type,
        features.strategy,
        features.authority,
        features.profile,
        features.definition,
        tuple(sorted(features.defined_centers)),
        tuple(sorted(features.channels)),
        tuple(sorted(features.activation_gates.items())),
    )


def _entropy(probabilities: Sequence[float]) -> float:
    return -sum(probability * math.log2(probability) for probability in probabilities if probability)


def _candidate_weighted_tie_quantile(counts: Sequence[int], quantile: float) -> int:
    if not 0.0 <= quantile <= 1.0:
        raise ValueError("quantile must be in [0, 1]")
    total_candidates = sum(counts)
    if total_candidates <= 0:
        raise ValueError("tie quantile requires candidates")
    threshold = max(1, math.ceil(total_candidates * quantile))
    cumulative = 0
    for tie_size in sorted(counts):
        cumulative += tie_size
        if cumulative >= threshold:
            return tie_size
    return max(counts)
