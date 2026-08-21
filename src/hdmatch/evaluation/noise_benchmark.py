"""Engineering-only comparison of revealed, frozen synthetic noise tiers.

This module consumes evaluation reports.  It deliberately has no dependency on
the synthetic generator, answer-key reveal functions, or recovery runtime.
"""

from __future__ import annotations

from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.experiments.canonical import sha256_json
from hdmatch.experiments.manifest import SHA256_PATTERN

from .failures import FailureRecord
from .metrics import AggregateRankMetrics
from .report import EvaluationReport


class NoiseBenchmarkInputError(ValueError):
    """A tier report or its comparison metadata violates the frozen contract."""


class NoiseTier(StrEnum):
    ORACLE = "oracle"
    LOW = "low"
    MEDIUM = "medium"
    ADVERSARIAL = "adversarial"


_TIER_ORDER = {
    NoiseTier.ORACLE: 0,
    NoiseTier.LOW: 1,
    NoiseTier.MEDIUM: 2,
    NoiseTier.ADVERSARIAL: 3,
}

UnitInterval = Annotated[float, Field(ge=0.0, le=1.0)]


class DeclaredNoiseSettings(BaseModel):
    """Exact simulator settings declared by a completed tier run."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    missing_rate: UnitInterval
    flip_rate: UnitInterval
    cluster_dropout_rate: UnitInterval
    behavioral_confidence_values: tuple[UnitInterval, ...] = Field(min_length=1)
    measurement_reliability_values: tuple[UnitInterval, ...] = Field(min_length=1)
    seed: int


class NoiseRunMetadata(BaseModel):
    """Non-secret bindings needed to make tier metrics scientifically comparable."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["noise-run-metadata-v1"] = "noise-run-metadata-v1"
    experiment_id: str = Field(min_length=1)
    tier: NoiseTier
    model_id: str = Field(min_length=1)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_universe: str = Field(min_length=1)
    candidate_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    case_set_sha256: str = Field(pattern=SHA256_PATTERN)
    declared_case_count: int = Field(ge=1)
    case_count_policy: Literal[
        "fixed-declared-case-set-unevaluable-zero-credit"
    ] = "fixed-declared-case-set-unevaluable-zero-credit"
    evaluation_sha256: str = Field(pattern=SHA256_PATTERN)
    noise: DeclaredNoiseSettings


class RevealedNoiseTierEvaluation(BaseModel):
    """One post-freeze, post-reveal synthetic report plus its explicit metadata."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    metadata: NoiseRunMetadata
    evaluation: EvaluationReport

    @model_validator(mode="after")
    def validate_bindings(self) -> RevealedNoiseTierEvaluation:
        if self.evaluation.claim_boundary != "synthetic-engineering-validation-only":
            raise ValueError("noise benchmark accepts synthetic engineering reports only")
        if self.metadata.experiment_id != self.evaluation.experiment_id:
            raise ValueError("metadata experiment_id does not match evaluation")
        if self.metadata.model_sha256 != self.evaluation.model_sha256:
            raise ValueError("metadata model_sha256 does not match evaluation")
        if self.metadata.declared_case_count != self.evaluation.aggregate.case_count:
            raise ValueError("declared case count does not match evaluation denominator")
        if self.metadata.evaluation_sha256 != sha256_json(self.evaluation):
            raise ValueError("metadata evaluation_sha256 does not match evaluation bytes")
        return self


class MetricDegradation(BaseModel):
    """Oracle minus tier metric; positive values mean worse recovery than oracle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    top_1: float | None
    top_3: float | None
    top_5: float | None
    mean_reciprocal_rank: float | None


class NoiseTierResult(BaseModel):
    """A preserved source evaluation with transparent derived comparison fields."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tier: NoiseTier
    declared_noise: DeclaredNoiseSettings
    aggregate: AggregateRankMetrics
    failures: tuple[FailureRecord, ...]
    failure_counts: dict[str, int]
    evaluated_case_ids: tuple[str, ...]
    unevaluable_case_ids: tuple[str, ...]
    degradation_from_oracle: MetricDegradation
    source: RevealedNoiseTierEvaluation


class NoiseBenchmarkReport(BaseModel):
    """Comparison output with no claim about Human Design validity in people."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["noise-benchmark-report-v1"] = "noise-benchmark-report-v1"
    model_id: str
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_universe: str
    candidate_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    case_set_sha256: str = Field(pattern=SHA256_PATTERN)
    case_count: int = Field(ge=1)
    case_count_policy: Literal[
        "fixed-declared-case-set-unevaluable-zero-credit"
    ] = "fixed-declared-case-set-unevaluable-zero-credit"
    tiers: tuple[NoiseTierResult, ...] = Field(min_length=4, max_length=4)
    claim_boundary: Literal["synthetic-engineering-validation-only"] = (
        "synthetic-engineering-validation-only"
    )
    interpretation: Literal["positive-degradation-means-worse-than-oracle"] = (
        "positive-degradation-means-worse-than-oracle"
    )


def _metric_drop(oracle: float | None, observed: float | None) -> float | None:
    if oracle is None or observed is None:
        return None
    return oracle - observed


def _case_partitions(
    item: RevealedNoiseTierEvaluation,
) -> tuple[tuple[str, ...], tuple[str, ...], frozenset[str]]:
    aggregate = item.evaluation.aggregate
    evaluated = tuple(sorted(case.case_id for case in item.evaluation.cases))
    if len(evaluated) != len(set(evaluated)):
        raise NoiseBenchmarkInputError(f"tier {item.metadata.tier}: duplicate evaluated case")
    if len(evaluated) != aggregate.evaluated_case_count:
        raise NoiseBenchmarkInputError(
            f"tier {item.metadata.tier}: evaluated case count does not match report"
        )

    failure_ids = tuple(failure.case_id for failure in item.evaluation.failures)
    observed_failure_counts = sum(item.evaluation.failure_counts.values())
    if observed_failure_counts != len(failure_ids):
        raise NoiseBenchmarkInputError(
            f"tier {item.metadata.tier}: failure counts do not preserve every failure"
        )
    all_case_ids = frozenset((*evaluated, *failure_ids))
    unevaluable = tuple(sorted(all_case_ids.difference(evaluated)))
    if len(unevaluable) != aggregate.unevaluable_case_count:
        raise NoiseBenchmarkInputError(
            f"tier {item.metadata.tier}: unevaluable case identities are incomplete"
        )
    if len(all_case_ids) != aggregate.case_count:
        raise NoiseBenchmarkInputError(
            f"tier {item.metadata.tier}: case identities do not cover the declared denominator"
        )
    return evaluated, unevaluable, all_case_ids


def compare_revealed_noise_tiers(
    evaluations: Sequence[RevealedNoiseTierEvaluation],
) -> NoiseBenchmarkReport:
    """Compare four already-evaluated tiers without keys, recovery, or noise generation."""

    by_tier: dict[NoiseTier, RevealedNoiseTierEvaluation] = {}
    for item in evaluations:
        if item.metadata.tier in by_tier:
            raise NoiseBenchmarkInputError(f"duplicate tier: {item.metadata.tier}")
        by_tier[item.metadata.tier] = item
    missing = set(NoiseTier).difference(by_tier)
    if missing:
        labels = ", ".join(sorted(tier.value for tier in missing))
        raise NoiseBenchmarkInputError(f"missing required tiers: {labels}")

    ordered = tuple(sorted(by_tier.values(), key=lambda item: _TIER_ORDER[item.metadata.tier]))
    oracle = by_tier[NoiseTier.ORACLE]
    oracle_noise = oracle.metadata.noise
    if (
        oracle_noise.missing_rate != 0.0
        or oracle_noise.flip_rate != 0.0
        or oracle_noise.cluster_dropout_rate != 0.0
        or oracle_noise.behavioral_confidence_values != (1.0,)
        or oracle_noise.measurement_reliability_values != (1.0,)
    ):
        raise NoiseBenchmarkInputError("oracle tier must declare zero noise and unit reliability")

    shared_fields = (
        "model_id",
        "model_sha256",
        "candidate_universe",
        "candidate_universe_sha256",
        "case_set_sha256",
        "declared_case_count",
        "case_count_policy",
    )
    for item in ordered[1:]:
        mismatches = [
            field
            for field in shared_fields
            if getattr(item.metadata, field) != getattr(oracle.metadata, field)
        ]
        if mismatches:
            raise NoiseBenchmarkInputError(
                f"tier {item.metadata.tier} is not comparable; mismatched metadata: "
                + ", ".join(mismatches)
            )
        for report_field in ("question_bank_sha256", "mapping_sha256"):
            if getattr(item.evaluation, report_field) != getattr(oracle.evaluation, report_field):
                raise NoiseBenchmarkInputError(
                    f"tier {item.metadata.tier} is not comparable; "
                    f"mismatched {report_field}"
                )

    oracle_aggregate = oracle.evaluation.aggregate
    case_partitions = {item.metadata.tier: _case_partitions(item) for item in ordered}
    oracle_case_set = case_partitions[NoiseTier.ORACLE][2]
    for tier, (_, _, case_set) in case_partitions.items():
        if case_set != oracle_case_set:
            raise NoiseBenchmarkInputError(f"tier {tier} does not contain the oracle case set")

    results: list[NoiseTierResult] = []
    for item in ordered:
        aggregate = item.evaluation.aggregate
        evaluated, unevaluable, _ = case_partitions[item.metadata.tier]
        results.append(
            NoiseTierResult(
                tier=item.metadata.tier,
                declared_noise=item.metadata.noise,
                aggregate=aggregate,
                failures=item.evaluation.failures,
                failure_counts=dict(item.evaluation.failure_counts),
                evaluated_case_ids=evaluated,
                unevaluable_case_ids=unevaluable,
                degradation_from_oracle=MetricDegradation(
                    top_1=_metric_drop(oracle_aggregate.top_1, aggregate.top_1),
                    top_3=_metric_drop(oracle_aggregate.top_3, aggregate.top_3),
                    top_5=_metric_drop(oracle_aggregate.top_5, aggregate.top_5),
                    mean_reciprocal_rank=_metric_drop(
                        oracle_aggregate.mean_reciprocal_rank,
                        aggregate.mean_reciprocal_rank,
                    ),
                ),
                source=item,
            )
        )

    metadata = oracle.metadata
    return NoiseBenchmarkReport(
        model_id=metadata.model_id,
        model_sha256=metadata.model_sha256,
        candidate_universe=metadata.candidate_universe,
        candidate_universe_sha256=metadata.candidate_universe_sha256,
        case_set_sha256=metadata.case_set_sha256,
        case_count=metadata.declared_case_count,
        tiers=tuple(results),
    )
