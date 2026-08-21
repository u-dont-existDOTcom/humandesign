"""Leakage-safe, person-level human model comparison and final-test release controls.

The scorer accepts response-only blind cases. True candidate identities live in a separate
answer-key object that is accepted only by the post-freeze evaluator. Fitting accepts the
development partition only; validation and final-test people cannot enter any fitted model.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from functools import partial
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.evaluation.metrics import (
    AggregateRankMetrics,
    CaseRankMetrics,
    aggregate_rank_metrics,
    evaluate_ranked_case,
)
from hdmatch.evaluation.permutation import empirical_p_value
from hdmatch.human.baselines import calendar_features, permute_chart_assignments
from hdmatch.human.dataset import HumanCase
from hdmatch.human.empirical import EmpiricalChartResponseModel, ModelArtifact
from hdmatch.human.splits import PersonSplitManifest, enforce_training_cohort
from hdmatch.util import sha256_json

SHA256_PATTERN = r"^[0-9a-f]{64}$"
FINAL_TEST_RELEASE_ACKNOWLEDGEMENT: Literal[
    "authorize-frozen-model-untouched-final-test-release"
] = "authorize-frozen-model-untouched-final-test-release"
CALENDAR_FEATURE_NAMES = ("year", "month", "day", "season_quarter")
PRIMARY_METHOD_IDS = (
    "symbolic_v4",
    "empirical_hd",
    "hybrid_hd",
    "calendar_season",
    "uniform_chance",
)

Cohort = Literal["development", "validation", "final_test"]
MethodFamily = Literal[
    "symbolic",
    "empirical",
    "hybrid",
    "calendar_season",
    "chance",
    "permuted_hd",
]


class SymbolicModelReference(BaseModel):
    """Immutable identity for a caller-supplied, source-bounded symbolic scorer."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    model_id: str = Field(min_length=1)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)


class FrozenHumanModelBundle(BaseModel):
    """Development-only fitted models and all choices needed to reproduce comparison."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-model-bundle-v1"] = "human-model-bundle-v1"
    bundle_id: str = Field(min_length=1)
    questionnaire_version: str = Field(min_length=1)
    split_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    development_participant_ids: tuple[str, ...]
    symbolic_model: SymbolicModelReference
    empirical_model: ModelArtifact
    calendar_season_model: ModelArtifact | None
    permuted_hd_models: tuple[ModelArtifact, ...]
    permutation_seeds: tuple[int, ...]
    empirical_feature_names: tuple[str, ...]
    calendar_feature_names: tuple[str, ...] = CALENDAR_FEATURE_NAMES
    hybrid_symbolic_weight: float = Field(gt=0.0)
    development_issues: tuple[str, ...] = ()
    created_at_utc: datetime
    claim_scope: Literal["development-fitted-models-not-predictive-validation"] = (
        "development-fitted-models-not-predictive-validation"
    )

    @model_validator(mode="after")
    def validate_bindings(self) -> FrozenHumanModelBundle:
        if not self.development_participant_ids:
            raise ValueError("model bundle requires development people")
        if len(set(self.development_participant_ids)) != len(self.development_participant_ids):
            raise ValueError("development participant IDs must be unique")
        artifacts = (self.empirical_model,) + self.permuted_hd_models
        if self.calendar_season_model is not None:
            artifacts += (self.calendar_season_model,)
        for artifact in artifacts:
            if artifact.split_manifest_hash != self.split_manifest_sha256:
                raise ValueError("model artifact is bound to a different person split")
            if artifact.questionnaire_version != self.questionnaire_version:
                raise ValueError("model artifact uses a different questionnaire")
        if self.empirical_model.feature_names != self.empirical_feature_names:
            raise ValueError("empirical feature list does not match its artifact")
        if self.calendar_season_model is not None:
            if self.calendar_season_model.feature_names != self.calendar_feature_names:
                raise ValueError("calendar feature list does not match its artifact")
            if self.calendar_season_model.feature_schema_version != "calendar-season-v1":
                raise ValueError("calendar baseline uses an unexpected feature schema")
        if len(self.permuted_hd_models) != len(self.permutation_seeds):
            raise ValueError("every permuted-HD model must retain its seed")
        if not self.permuted_hd_models:
            raise ValueError("at least one person-level chart permutation is required")
        for artifact in self.permuted_hd_models:
            if artifact.feature_names != self.empirical_feature_names:
                raise ValueError("permuted-HD model uses a different feature list")
        return self

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("model-bundle timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def sha256(self) -> str:
        return sha256_json(self)


class FrozenHumanEvaluationProtocol(BaseModel):
    """Frozen cohort, model, metrics, and claim boundary before blind scoring."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-evaluation-protocol-v1"] = "human-evaluation-protocol-v1"
    protocol_id: str = Field(min_length=1)
    cohort: Cohort
    participant_ids: tuple[str, ...]
    questionnaire_version: str = Field(min_length=1)
    split_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    model_bundle_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_universe_rule: str = Field(min_length=1)
    selected_primary_method: str
    declared_metrics: tuple[str, ...] = (
        "top_1",
        "top_3",
        "top_5",
        "mean_reciprocal_rank",
        "mean_percentile",
        "tie_rate",
    )
    tie_policy: Literal["exact-score-fractional-credit"] = "exact-score-fractional-credit"
    tuning_source: Literal["development-only"] = "development-only"
    tuning_locked: Literal[True] = True
    final_test_release_id: str | None = None
    final_test_release_acknowledgement: (
        Literal["authorize-frozen-model-untouched-final-test-release"] | None
    ) = None
    created_at_utc: datetime

    @model_validator(mode="after")
    def validate_release(self) -> FrozenHumanEvaluationProtocol:
        if not self.participant_ids or len(set(self.participant_ids)) != len(self.participant_ids):
            raise ValueError("protocol participant IDs must be nonempty and unique")
        if self.cohort == "final_test" and not self.final_test_release_id:
            raise ValueError("final-test protocol requires an explicit release ID")
        if self.cohort == "final_test" and (
            self.final_test_release_acknowledgement != FINAL_TEST_RELEASE_ACKNOWLEDGEMENT
        ):
            raise ValueError("final-test protocol requires an explicit release acknowledgement")
        if self.cohort != "final_test" and self.final_test_release_id is not None:
            raise ValueError("only a final-test protocol may carry a release ID")
        if self.cohort != "final_test" and self.final_test_release_acknowledgement is not None:
            raise ValueError("only a final-test protocol may carry a release acknowledgement")
        return self

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("protocol timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def sha256(self) -> str:
        return sha256_json(self)


class HumanCandidate(BaseModel):
    """One public candidate; it contains no indication that it is the true candidate."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str = Field(min_length=1)
    chart_features: dict[str, Any]
    local_year: int | None = None
    local_month: int | None = Field(default=None, ge=1, le=12)
    local_day: int | None = Field(default=None, ge=1, le=31)

    @model_validator(mode="after")
    def validate_local_date(self) -> HumanCandidate:
        parts = (self.local_year, self.local_month, self.local_day)
        if any(item is not None for item in parts) and not all(item is not None for item in parts):
            raise ValueError("candidate local date must be complete or entirely absent")
        if (
            self.local_year is not None
            and self.local_month is not None
            and self.local_day is not None
        ):
            date(self.local_year, self.local_month, self.local_day)
        return self

    def calendar_features(self) -> dict[str, int] | None:
        if self.local_year is None or self.local_month is None or self.local_day is None:
            return None
        return dict(calendar_features(self.local_year, self.local_month, self.local_day))


class HumanBlindCase(BaseModel):
    """Response-only evaluation case. Extra truth/birth fields are rejected."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str = Field(min_length=1)
    cohort: Cohort
    questionnaire_version: str = Field(min_length=1)
    responses: dict[str, str]
    response_reliability: dict[str, float] = Field(default_factory=dict)
    candidates: tuple[HumanCandidate, ...]

    @model_validator(mode="after")
    def validate_reliability(self) -> HumanBlindCase:
        unknown = set(self.response_reliability) - set(self.responses)
        if unknown:
            raise ValueError(f"reliability supplied for unanswered questions: {sorted(unknown)}")
        invalid = sorted(
            question
            for question, value in self.response_reliability.items()
            if not math.isfinite(value) or not 0.0 <= value <= 1.0
        )
        if invalid:
            raise ValueError(f"response reliability must be within [0, 1]: {invalid}")
        return self


class HumanCohortAnswerKey(BaseModel):
    """Separate reveal material; never an input to blind scoring."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-cohort-answer-key-v1"] = "human-cohort-answer-key-v1"
    cohort: Cohort
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    true_candidate_ids: dict[str, str]
    final_test_release_id: str | None = None

    @model_validator(mode="after")
    def validate_release(self) -> HumanCohortAnswerKey:
        if self.cohort == "final_test" and not self.final_test_release_id:
            raise ValueError("final-test key requires its release ID")
        if self.cohort != "final_test" and self.final_test_release_id is not None:
            raise ValueError("non-final key cannot carry a final-test release ID")
        return self


class RankedHumanCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str
    score: float
    best_rank: int = Field(ge=1)
    worst_rank: int = Field(ge=1)
    midrank: float = Field(ge=1.0)
    tie_size: int = Field(ge=1)


class HumanMethodRanking(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    method_id: str
    family: MethodFamily
    score_semantics: str
    status: Literal["scored", "unevaluable"]
    candidates: tuple[RankedHumanCandidate, ...] = ()
    failure_reason: str | None = None

    @model_validator(mode="after")
    def validate_status(self) -> HumanMethodRanking:
        if self.status == "scored" and (not self.candidates or self.failure_reason is not None):
            raise ValueError("scored method requires candidates and no failure")
        if self.status == "unevaluable" and (self.candidates or not self.failure_reason):
            raise ValueError("unevaluable method requires a failure and no candidates")
        return self


class HumanCasePredictions(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str
    cohort: Cohort
    methods: tuple[HumanMethodRanking, ...]

    @model_validator(mode="after")
    def unique_methods(self) -> HumanCasePredictions:
        identifiers = [method.method_id for method in self.methods]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("case prediction contains duplicate method IDs")
        return self


class HumanPredictionSet(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-predictions-v1"] = "human-predictions-v1"
    protocol_id: str
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    model_bundle_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    cohort: Cohort
    cases: tuple[HumanCasePredictions, ...]
    created_at_utc: datetime
    answer_key_accessed: Literal[False] = False

    @model_validator(mode="after")
    def unique_people(self) -> HumanPredictionSet:
        identifiers = [case.participant_id for case in self.cases]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("prediction set contains duplicate participant IDs")
        if any(case.cohort != self.cohort for case in self.cases):
            raise ValueError("prediction cases must match the prediction-set cohort")
        return self

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("prediction timestamp must be timezone-aware")
        return value.astimezone(UTC)


class HumanPredictionFreeze(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-prediction-freeze-v1"] = "human-prediction-freeze-v1"
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    model_bundle_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    created_at_utc: datetime
    answer_key_revealed: Literal[False] = False

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("prediction-freeze timestamp must be timezone-aware")
        return value.astimezone(UTC)


class HumanEvaluationFailure(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str
    method_id: str
    reason: Literal[
        "answer_key_missing_truth",
        "prediction_case_missing",
        "prediction_method_missing",
        "method_unevaluable",
        "true_candidate_absent",
    ]
    detail: str


class HumanMethodEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    method_id: str
    family: MethodFamily
    metrics: AggregateRankMetrics
    cases: tuple[CaseRankMetrics, ...]
    failures: tuple[HumanEvaluationFailure, ...]


class HumanPermutationBaseline(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    null_kind: Literal["development-person-chart-assignment-permutation"] = (
        "development-person-chart-assignment-permutation"
    )
    observed_method_id: Literal["empirical_hd"] = "empirical_hd"
    observed_mean_reciprocal_rank: float
    null_mean_reciprocal_ranks: tuple[float, ...]
    permutation_count: int = Field(ge=1)
    minimum_attainable_p_value: float = Field(gt=0.0, le=0.5)
    p_value_greater: float = Field(gt=0.0, le=1.0)
    interpretation: Literal["baseline-comparison-not-a-calibrated-probability"] = (
        "baseline-comparison-not-a-calibrated-probability"
    )

    @model_validator(mode="after")
    def validate_resolution(self) -> HumanPermutationBaseline:
        if self.permutation_count != len(self.null_mean_reciprocal_ranks):
            raise ValueError("permutation count does not match the retained null values")
        expected = 1.0 / (self.permutation_count + 1.0)
        if not math.isclose(self.minimum_attainable_p_value, expected):
            raise ValueError("minimum permutation p-value does not match plus-one resolution")
        return self


class HumanComparisonReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-comparison-report-v1"] = "human-comparison-report-v1"
    protocol_id: str
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    model_bundle_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    cohort: Cohort
    selected_primary_method: str
    method_evaluations: tuple[HumanMethodEvaluation, ...]
    permutation_baseline: HumanPermutationBaseline
    claim_boundary: str
    warnings: tuple[str, ...]
    evaluated_at_utc: datetime

    @field_validator("evaluated_at_utc")
    @classmethod
    def normalize_evaluated_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("comparison timestamp must be timezone-aware")
        return value.astimezone(UTC)


SymbolicScoreCallable = Callable[[Mapping[str, str], Mapping[str, Any], Mapping[str, float]], float]


@dataclass(frozen=True)
class BoundSymbolicScorer:
    """Runtime implementation bound to the exact symbolic artifact frozen in the bundle."""

    reference: SymbolicModelReference
    score: SymbolicScoreCallable


def _symbolic_candidate_score(
    candidate: HumanCandidate,
    *,
    responses: Mapping[str, str],
    reliability: Mapping[str, float],
    scorer: SymbolicScoreCallable,
) -> float:
    return scorer(responses, candidate.chart_features, reliability)


def _empirical_candidate_score(
    candidate: HumanCandidate,
    *,
    responses: Mapping[str, str],
    reliability: Mapping[str, float],
    model: EmpiricalChartResponseModel,
) -> float:
    return model.log2_score(responses, candidate.chart_features, reliability)


def _hybrid_candidate_score(
    candidate: HumanCandidate,
    *,
    responses: Mapping[str, str],
    reliability: Mapping[str, float],
    empirical: EmpiricalChartResponseModel,
    symbolic: SymbolicScoreCallable,
    symbolic_weight: float,
) -> float:
    return empirical.log2_score(
        responses, candidate.chart_features, reliability
    ) + symbolic_weight * symbolic(responses, candidate.chart_features, reliability)


def fit_development_model_bundle(
    cases: Sequence[HumanCase],
    *,
    manifest: PersonSplitManifest,
    bundle_id: str,
    questionnaire_version: str,
    symbolic_model: SymbolicModelReference,
    empirical_feature_names: Sequence[str],
    alpha: float = 2.0,
    hybrid_symbolic_weight: float = 1.0,
    permutation_count: int = 32,
    permutation_seed: int = 0,
    created_at_utc: datetime | None = None,
) -> FrozenHumanModelBundle:
    """Fit all learned models on exactly the person-level development split."""

    enforce_training_cohort(list(cases))
    if permutation_count < 1:
        raise ValueError("at least one chart-assignment permutation is required")
    ordered_cases = tuple(sorted(cases, key=lambda case: case.participant_id))
    identifiers = [case.participant_id for case in ordered_cases]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("development people must be unique")
    if set(identifiers) != set(manifest.development_ids):
        raise ValueError("fitting requires exactly the manifest development people")
    if hybrid_symbolic_weight <= 0.0 or not math.isfinite(hybrid_symbolic_weight):
        raise ValueError("hybrid symbolic weight must be finite and positive")
    feature_names = tuple(empirical_feature_names)
    if not feature_names or len(feature_names) != len(set(feature_names)):
        raise ValueError("empirical feature names must be nonempty and unique")
    timestamp = created_at_utc or datetime.now(UTC)
    split_hash = sha256_json(manifest)
    empirical = EmpiricalChartResponseModel.fit(
        ordered_cases,
        model_id=f"{bundle_id}:empirical",
        questionnaire_version=questionnaire_version,
        split_manifest_hash=split_hash,
        feature_names=feature_names,
        alpha=alpha,
        created_at_utc=timestamp,
    ).artifact

    calendar_cases: list[HumanCase] = []
    issues: list[str] = []
    for case in ordered_cases:
        if case.birth_year is None or case.birth_month is None or case.birth_day is None:
            issues.append(f"calendar_baseline_missing_birth_date:{case.participant_id}")
            continue
        calendar_cases.append(
            case.model_copy(
                update={
                    "chart_features": dict(
                        calendar_features(case.birth_year, case.birth_month, case.birth_day)
                    )
                }
            )
        )
    calendar_model: ModelArtifact | None = None
    if calendar_cases:
        calendar_model = EmpiricalChartResponseModel.fit(
            calendar_cases,
            model_id=f"{bundle_id}:calendar-season",
            questionnaire_version=questionnaire_version,
            split_manifest_hash=split_hash,
            feature_names=CALENDAR_FEATURE_NAMES,
            alpha=alpha,
            feature_schema_version="calendar-season-v1",
            created_at_utc=timestamp,
        ).artifact
    else:
        issues.append("calendar_baseline_unavailable:no_development_birth_dates")

    seed_source = random.Random(permutation_seed)
    permutation_seeds = tuple(seed_source.getrandbits(64) for _ in range(permutation_count))
    permuted_models: list[ModelArtifact] = []
    for index, seed in enumerate(permutation_seeds):
        assignment = permute_chart_assignments(ordered_cases, seed)
        permuted_cases = [
            case.model_copy(update={"chart_features": assignment[case.participant_id]})
            for case in ordered_cases
        ]
        permuted_models.append(
            EmpiricalChartResponseModel.fit(
                permuted_cases,
                model_id=f"{bundle_id}:permuted-hd:{index:03d}",
                questionnaire_version=questionnaire_version,
                split_manifest_hash=split_hash,
                feature_names=feature_names,
                alpha=alpha,
                created_at_utc=timestamp,
            ).artifact
        )
    return FrozenHumanModelBundle(
        bundle_id=bundle_id,
        questionnaire_version=questionnaire_version,
        split_manifest_sha256=split_hash,
        development_participant_ids=tuple(sorted(identifiers)),
        symbolic_model=symbolic_model,
        empirical_model=empirical,
        calendar_season_model=calendar_model,
        permuted_hd_models=tuple(permuted_models),
        permutation_seeds=permutation_seeds,
        empirical_feature_names=feature_names,
        hybrid_symbolic_weight=hybrid_symbolic_weight,
        development_issues=tuple(sorted(issues)),
        created_at_utc=timestamp,
    )


def freeze_human_evaluation_protocol(
    bundle: FrozenHumanModelBundle,
    manifest: PersonSplitManifest,
    *,
    protocol_id: str,
    cohort: Literal["development", "validation"],
    candidate_universe_rule: str,
    selected_primary_method: str,
    created_at_utc: datetime | None = None,
) -> FrozenHumanEvaluationProtocol:
    """Freeze a development or validation protocol; final test uses a separate gate."""

    return _freeze_protocol(
        bundle,
        manifest,
        protocol_id=protocol_id,
        cohort=cohort,
        candidate_universe_rule=candidate_universe_rule,
        selected_primary_method=selected_primary_method,
        final_test_release_id=None,
        created_at_utc=created_at_utc,
    )


def freeze_final_test_protocol(
    bundle: FrozenHumanModelBundle,
    manifest: PersonSplitManifest,
    *,
    protocol_id: str,
    candidate_universe_rule: str,
    selected_primary_method: str,
    final_test_release_id: str,
    release_authorization: str,
    created_at_utc: datetime | None = None,
) -> FrozenHumanEvaluationProtocol:
    """Create an explicit frozen-model release artifact for an untouched final test.

    This pure function cannot enforce globally one-time use. The high-level CLI persists
    append-only cohort/release/freeze/reveal receipts in its declared external ledger and
    rejects reuse there.
    """

    if release_authorization != FINAL_TEST_RELEASE_ACKNOWLEDGEMENT:
        raise PermissionError("final-test release requires the explicit release acknowledgement")
    if not final_test_release_id:
        raise ValueError("final_test_release_id cannot be empty")
    return _freeze_protocol(
        bundle,
        manifest,
        protocol_id=protocol_id,
        cohort="final_test",
        candidate_universe_rule=candidate_universe_rule,
        selected_primary_method=selected_primary_method,
        final_test_release_id=final_test_release_id,
        created_at_utc=created_at_utc,
    )


def _freeze_protocol(
    bundle: FrozenHumanModelBundle,
    manifest: PersonSplitManifest,
    *,
    protocol_id: str,
    cohort: Cohort,
    candidate_universe_rule: str,
    selected_primary_method: str,
    final_test_release_id: str | None,
    created_at_utc: datetime | None,
) -> FrozenHumanEvaluationProtocol:
    split_hash = sha256_json(manifest)
    if split_hash != bundle.split_manifest_sha256:
        raise ValueError("model bundle and evaluation protocol use different person splits")
    available_methods = _method_ids(bundle)
    if selected_primary_method not in available_methods:
        raise ValueError("selected primary method is absent from the frozen model bundle")
    participant_ids = tuple(sorted(getattr(manifest, f"{cohort}_ids")))
    timestamp = created_at_utc or datetime.now(UTC)
    if timestamp < bundle.created_at_utc:
        raise ValueError("evaluation protocol timestamp cannot predate model bundle")
    return FrozenHumanEvaluationProtocol(
        protocol_id=protocol_id,
        cohort=cohort,
        participant_ids=participant_ids,
        questionnaire_version=bundle.questionnaire_version,
        split_manifest_sha256=split_hash,
        model_bundle_sha256=bundle.sha256,
        candidate_universe_rule=candidate_universe_rule,
        selected_primary_method=selected_primary_method,
        final_test_release_id=final_test_release_id,
        final_test_release_acknowledgement=(
            FINAL_TEST_RELEASE_ACKNOWLEDGEMENT if cohort == "final_test" else None
        ),
        created_at_utc=timestamp,
    )


def score_blind_human_cohort(
    cases: Sequence[HumanBlindCase],
    *,
    bundle: FrozenHumanModelBundle,
    protocol: FrozenHumanEvaluationProtocol,
    symbolic_scorer: BoundSymbolicScorer,
    created_at_utc: datetime | None = None,
) -> HumanPredictionSet:
    """Score all frozen methods without accepting any answer-key parameter."""

    _verify_bundle_protocol(bundle, protocol)
    if symbolic_scorer.reference != bundle.symbolic_model:
        raise ValueError("runtime symbolic scorer does not match the frozen symbolic artifact")
    identifiers = [case.participant_id for case in cases]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("blind cohort contains duplicate participants")
    if set(identifiers) != set(protocol.participant_ids):
        raise ValueError("blind cohort must contain exactly the protocol participants")
    for case in cases:
        if case.cohort != protocol.cohort:
            raise ValueError("blind case cohort does not match the frozen protocol")
        if case.questionnaire_version != protocol.questionnaire_version:
            raise ValueError("blind case questionnaire does not match the frozen protocol")

    empirical = EmpiricalChartResponseModel(bundle.empirical_model)
    calendar = (
        EmpiricalChartResponseModel(bundle.calendar_season_model)
        if bundle.calendar_season_model is not None
        else None
    )
    permutations = tuple(EmpiricalChartResponseModel(item) for item in bundle.permuted_hd_models)
    predictions: list[HumanCasePredictions] = []
    for case in sorted(cases, key=lambda item: item.participant_id):
        responses = case.responses
        reliability = case.response_reliability
        methods = [
            _score_method(
                case,
                method_id="symbolic_v4",
                family="symbolic",
                semantics="symbolic_rubric_bits_not_probability",
                scorer=partial(
                    _symbolic_candidate_score,
                    responses=responses,
                    reliability=reliability,
                    scorer=symbolic_scorer.score,
                ),
            ),
            _score_method(
                case,
                method_id="empirical_hd",
                family="empirical",
                semantics="regularized_response_log2_likelihood_not_calibrated_probability",
                scorer=partial(
                    _empirical_candidate_score,
                    responses=responses,
                    reliability=reliability,
                    model=empirical,
                ),
            ),
            _score_method(
                case,
                method_id="hybrid_hd",
                family="hybrid",
                semantics=("frozen_composite_empirical_log2_plus_weighted_symbolic_rubric_bits"),
                scorer=partial(
                    _hybrid_candidate_score,
                    responses=responses,
                    reliability=reliability,
                    empirical=empirical,
                    symbolic=symbolic_scorer.score,
                    symbolic_weight=bundle.hybrid_symbolic_weight,
                ),
            ),
            _score_calendar_method(case, calendar),
            _score_method(
                case,
                method_id="uniform_chance",
                family="chance",
                semantics="equal_score_fractional_tie_credit",
                scorer=lambda _candidate: 0.0,
            ),
        ]
        for index, model in enumerate(permutations):
            methods.append(
                _score_method(
                    case,
                    method_id=f"permuted_hd_{index:03d}",
                    family="permuted_hd",
                    semantics="development_person_chart_assignment_permutation_log2_likelihood",
                    scorer=partial(
                        _empirical_candidate_score,
                        responses=responses,
                        reliability=reliability,
                        model=model,
                    ),
                )
            )
        predictions.append(
            HumanCasePredictions(
                participant_id=case.participant_id,
                cohort=case.cohort,
                methods=tuple(methods),
            )
        )
    timestamp = created_at_utc or datetime.now(UTC)
    if timestamp < protocol.created_at_utc:
        raise ValueError("prediction timestamp cannot predate evaluation protocol")
    return HumanPredictionSet(
        protocol_id=protocol.protocol_id,
        protocol_sha256=protocol.sha256,
        model_bundle_sha256=bundle.sha256,
        blind_input_sha256=sha256_json(
            [
                case.model_dump(mode="json")
                for case in sorted(cases, key=lambda item: item.participant_id)
            ]
        ),
        cohort=protocol.cohort,
        cases=tuple(predictions),
        created_at_utc=timestamp,
    )


def _score_calendar_method(
    case: HumanBlindCase,
    model: EmpiricalChartResponseModel | None,
) -> HumanMethodRanking:
    if model is None:
        return _unevaluable(
            "calendar_season", "calendar_season", "calendar baseline was unavailable at freeze"
        )
    if any(candidate.calendar_features() is None for candidate in case.candidates):
        return _unevaluable(
            "calendar_season", "calendar_season", "candidate calendar date is missing"
        )
    return _score_method(
        case,
        method_id="calendar_season",
        family="calendar_season",
        semantics="regularized_calendar_season_response_log2_likelihood",
        scorer=lambda candidate: model.log2_score(
            case.responses,
            candidate.calendar_features() or {},
            case.response_reliability,
        ),
    )


def _score_method(
    case: HumanBlindCase,
    *,
    method_id: str,
    family: MethodFamily,
    semantics: str,
    scorer: Callable[[HumanCandidate], float],
) -> HumanMethodRanking:
    if not case.candidates:
        return _unevaluable(method_id, family, "candidate universe is empty")
    identities = [candidate.candidate_id for candidate in case.candidates]
    if len(identities) != len(set(identities)):
        return _unevaluable(method_id, family, "candidate universe has duplicate identities")
    try:
        scores = {candidate.candidate_id: float(scorer(candidate)) for candidate in case.candidates}
    except Exception as exc:  # noqa: BLE001 - failures are retained, not erased
        return _unevaluable(method_id, family, f"scorer failed:{type(exc).__name__}")
    if not all(math.isfinite(score) for score in scores.values()):
        return _unevaluable(method_id, family, "scorer returned a non-finite score")
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    ranked: list[RankedHumanCandidate] = []
    position = 0
    while position < len(ordered):
        score = ordered[position][1]
        end = position + 1
        while end < len(ordered) and ordered[end][1] == score:
            end += 1
        best = position + 1
        worst = end
        tie_size = end - position
        for candidate_id, candidate_score in ordered[position:end]:
            ranked.append(
                RankedHumanCandidate(
                    candidate_id=candidate_id,
                    score=candidate_score,
                    best_rank=best,
                    worst_rank=worst,
                    midrank=(best + worst) / 2.0,
                    tie_size=tie_size,
                )
            )
        position = end
    return HumanMethodRanking(
        method_id=method_id,
        family=family,
        score_semantics=semantics,
        status="scored",
        candidates=tuple(ranked),
    )


def _unevaluable(method_id: str, family: MethodFamily, reason: str) -> HumanMethodRanking:
    return HumanMethodRanking(
        method_id=method_id,
        family=family,
        score_semantics="unavailable",
        status="unevaluable",
        failure_reason=reason,
    )


def freeze_human_predictions(
    predictions: HumanPredictionSet,
    *,
    bundle: FrozenHumanModelBundle,
    protocol: FrozenHumanEvaluationProtocol,
    created_at_utc: datetime | None = None,
) -> HumanPredictionFreeze:
    """Hash predictions and all frozen bindings before an answer key can be evaluated."""

    _verify_bundle_protocol(bundle, protocol)
    if predictions.protocol_sha256 != protocol.sha256:
        raise ValueError("predictions are bound to a different protocol")
    if predictions.protocol_id != protocol.protocol_id or predictions.cohort != protocol.cohort:
        raise ValueError("prediction identity or cohort does not match the protocol")
    if predictions.model_bundle_sha256 != bundle.sha256:
        raise ValueError("predictions are bound to a different model bundle")
    timestamp = created_at_utc or datetime.now(UTC)
    if timestamp < predictions.created_at_utc:
        raise ValueError("prediction-freeze timestamp cannot predate predictions")
    return HumanPredictionFreeze(
        protocol_sha256=protocol.sha256,
        model_bundle_sha256=bundle.sha256,
        blind_input_sha256=predictions.blind_input_sha256,
        prediction_sha256=sha256_json(predictions),
        created_at_utc=timestamp,
    )


def reveal_and_evaluate_human_cohort(
    predictions: HumanPredictionSet,
    freeze: HumanPredictionFreeze,
    answer_key: HumanCohortAnswerKey,
    *,
    bundle: FrozenHumanModelBundle,
    protocol: FrozenHumanEvaluationProtocol,
    evaluated_at_utc: datetime | None = None,
) -> HumanComparisonReport:
    """Verify the prediction freeze, then evaluate every person/method including failures."""

    verify_human_prediction_freeze(
        predictions,
        freeze,
        bundle=bundle,
        protocol=protocol,
    )
    evaluation_time = evaluated_at_utc or datetime.now(UTC)
    if evaluation_time < freeze.created_at_utc:
        raise ValueError("human evaluation timestamp cannot predate prediction freeze")
    _verify_bundle_protocol(bundle, protocol)
    if predictions.protocol_sha256 != protocol.sha256:
        raise ValueError("predictions are bound to a different protocol")
    if answer_key.protocol_sha256 != protocol.sha256 or answer_key.cohort != protocol.cohort:
        raise ValueError("answer key is bound to a different frozen protocol")
    if answer_key.blind_input_sha256 != predictions.blind_input_sha256:
        raise ValueError("answer key is bound to a different blind input")
    extra_keys = set(answer_key.true_candidate_ids) - set(protocol.participant_ids)
    if extra_keys:
        raise ValueError(
            f"answer key contains people outside the frozen cohort: {sorted(extra_keys)}"
        )
    if (
        protocol.cohort == "final_test"
        and answer_key.final_test_release_id != protocol.final_test_release_id
    ):
        raise ValueError("final-test answer key release does not match the frozen protocol")

    prediction_by_person = {case.participant_id: case for case in predictions.cases}
    method_ids = _method_ids(bundle)
    method_results: list[HumanMethodEvaluation] = []
    for method_id in method_ids:
        metrics: list[CaseRankMetrics] = []
        failures: list[HumanEvaluationFailure] = []
        family = _family_for_method(method_id)
        for participant_id in protocol.participant_ids:
            truth = answer_key.true_candidate_ids.get(participant_id)
            if truth is None:
                failures.append(
                    _failure(
                        participant_id,
                        method_id,
                        "answer_key_missing_truth",
                        "no revealed candidate identity was supplied",
                    )
                )
                continue
            case_prediction = prediction_by_person.get(participant_id)
            if case_prediction is None:
                failures.append(
                    _failure(
                        participant_id,
                        method_id,
                        "prediction_case_missing",
                        "frozen predictions omitted this protocol participant",
                    )
                )
                continue
            ranking = next(
                (item for item in case_prediction.methods if item.method_id == method_id), None
            )
            if ranking is None:
                failures.append(
                    _failure(
                        participant_id,
                        method_id,
                        "prediction_method_missing",
                        "frozen case predictions omitted this method",
                    )
                )
                continue
            if ranking.status == "unevaluable":
                failures.append(
                    _failure(
                        participant_id,
                        method_id,
                        "method_unevaluable",
                        ranking.failure_reason or "method was unevaluable",
                    )
                )
                continue
            candidate_rows = [
                {"candidate_id": candidate.candidate_id, "score": candidate.score}
                for candidate in ranking.candidates
            ]
            if truth not in {row["candidate_id"] for row in candidate_rows}:
                failures.append(
                    _failure(
                        participant_id,
                        method_id,
                        "true_candidate_absent",
                        "revealed candidate was outside the frozen ranking",
                    )
                )
                continue
            metrics.append(
                evaluate_ranked_case(
                    case_id=participant_id,
                    candidates=candidate_rows,
                    true_candidate_id=truth,
                    id_field="candidate_id",
                    score_field="score",
                )
            )
        method_results.append(
            HumanMethodEvaluation(
                method_id=method_id,
                family=family,
                metrics=aggregate_rank_metrics(
                    metrics, total_case_count=len(protocol.participant_ids)
                ),
                cases=tuple(metrics),
                failures=tuple(failures),
            )
        )

    by_method = {result.method_id: result for result in method_results}
    observed = by_method["empirical_hd"].metrics.mean_reciprocal_rank or 0.0
    null_values = tuple(
        by_method[method_id].metrics.mean_reciprocal_rank or 0.0
        for method_id in method_ids
        if method_id.startswith("permuted_hd_")
    )
    permutation = HumanPermutationBaseline(
        observed_mean_reciprocal_rank=observed,
        null_mean_reciprocal_ranks=null_values,
        permutation_count=len(null_values),
        minimum_attainable_p_value=1.0 / (len(null_values) + 1.0),
        p_value_greater=empirical_p_value(observed, null_values, alternative="greater"),
    )
    warnings = [
        "Rubric bits and composite rank scores are not calibrated probabilities.",
        "Unevaluable people and method failures remain in aggregate denominators.",
        "An HD-specific claim requires outperforming chance, permutation, and "
        "calendar/season controls.",
        f"Permutation comparison uses {len(null_values)} development chart-assignment "
        f"permutations; minimum attainable plus-one p-value is "
        f"{1.0 / (len(null_values) + 1.0):.6f}.",
    ]
    if protocol.cohort == "final_test":
        warnings.append(
            "This artifact binds a final-test release ID but cannot enforce global one-time "
            "use; an untouched claim requires the CLI's persistent single-use ledger receipts."
        )
    return HumanComparisonReport(
        protocol_id=protocol.protocol_id,
        protocol_sha256=protocol.sha256,
        model_bundle_sha256=bundle.sha256,
        blind_input_sha256=predictions.blind_input_sha256,
        prediction_sha256=freeze.prediction_sha256,
        prediction_freeze_sha256=sha256_json(freeze),
        answer_key_sha256=sha256_json(answer_key),
        cohort=protocol.cohort,
        selected_primary_method=protocol.selected_primary_method,
        method_evaluations=tuple(method_results),
        permutation_baseline=permutation,
        claim_boundary=_claim_boundary(protocol.cohort),
        warnings=tuple(warnings),
        evaluated_at_utc=evaluation_time,
    )


def verify_human_prediction_freeze(
    predictions: HumanPredictionSet,
    freeze: HumanPredictionFreeze,
    *,
    bundle: FrozenHumanModelBundle,
    protocol: FrozenHumanEvaluationProtocol,
) -> None:
    """Verify prediction bytes semantically before any answer-key file is opened."""

    _verify_bundle_protocol(bundle, protocol)
    if freeze.protocol_sha256 != protocol.sha256:
        raise ValueError("prediction freeze is bound to a different protocol")
    if freeze.model_bundle_sha256 != bundle.sha256:
        raise ValueError("prediction freeze is bound to a different model bundle")
    if freeze.blind_input_sha256 != predictions.blind_input_sha256:
        raise ValueError("prediction freeze blind-input hash does not match predictions")
    if freeze.prediction_sha256 != sha256_json(predictions):
        raise ValueError("predictions changed after freeze")
    if predictions.protocol_sha256 != protocol.sha256:
        raise ValueError("predictions are bound to a different protocol")
    if predictions.protocol_id != protocol.protocol_id or predictions.cohort != protocol.cohort:
        raise ValueError("prediction identity or cohort does not match the protocol")
    if predictions.model_bundle_sha256 != bundle.sha256:
        raise ValueError("predictions are bound to a different model bundle")


def _failure(
    participant_id: str,
    method_id: str,
    reason: Literal[
        "answer_key_missing_truth",
        "prediction_case_missing",
        "prediction_method_missing",
        "method_unevaluable",
        "true_candidate_absent",
    ],
    detail: str,
) -> HumanEvaluationFailure:
    return HumanEvaluationFailure(
        participant_id=participant_id,
        method_id=method_id,
        reason=reason,
        detail=detail,
    )


def _method_ids(bundle: FrozenHumanModelBundle) -> tuple[str, ...]:
    return PRIMARY_METHOD_IDS + tuple(
        f"permuted_hd_{index:03d}" for index in range(len(bundle.permuted_hd_models))
    )


def _family_for_method(method_id: str) -> MethodFamily:
    families: dict[str, MethodFamily] = {
        "symbolic_v4": "symbolic",
        "empirical_hd": "empirical",
        "hybrid_hd": "hybrid",
        "calendar_season": "calendar_season",
        "uniform_chance": "chance",
    }
    if method_id.startswith("permuted_hd_"):
        return "permuted_hd"
    return families[method_id]


def _verify_bundle_protocol(
    bundle: FrozenHumanModelBundle,
    protocol: FrozenHumanEvaluationProtocol,
) -> None:
    if protocol.model_bundle_sha256 != bundle.sha256:
        raise ValueError("evaluation protocol is bound to a different model bundle")
    if protocol.split_manifest_sha256 != bundle.split_manifest_sha256:
        raise ValueError("evaluation protocol is bound to a different person split")
    if protocol.questionnaire_version != bundle.questionnaire_version:
        raise ValueError("evaluation protocol uses a different questionnaire")


def _claim_boundary(cohort: Cohort) -> str:
    if cohort == "development":
        return "in-sample development fit; not predictive validation"
    if cohort == "validation":
        return (
            "person-held-out internal validation; eligible for model selection, not untouched "
            "final evidence"
        )
    return (
        "final-test evaluation from the pure API; an untouched claim additionally requires "
        "the CLI's persistent protocol/freeze/reveal ledger receipts"
    )
