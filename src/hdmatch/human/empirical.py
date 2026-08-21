"""Regularized generative chart-to-response model for development humans."""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from hdmatch.human.dataset import HumanCase
from hdmatch.human.splits import enforce_training_cohort
from hdmatch.util import sha256_json


def _feature_token(value: Any) -> str:
    if isinstance(value, list):
        return "|".join(sorted(str(item) for item in value))
    return str(value)


class ModelArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["empirical-model-v2"] = "empirical-model-v2"
    model_id: str
    training_dataset_hash: str
    split_manifest_hash: str
    questionnaire_version: str
    feature_schema_version: str = "chart-features-flat-v1"
    feature_names: tuple[str, ...]
    alpha: float = Field(gt=0.0)
    theory_strength: float = Field(ge=0.0)
    answer_vocabularies: dict[str, tuple[str, ...]]
    marginal_counts: dict[str, dict[str, float]]
    conditional_counts: dict[str, dict[str, dict[str, dict[str, float]]]]
    theory_priors: dict[str, dict[str, float]] = Field(default_factory=dict)
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("empirical-model timestamp must be timezone-aware")
        return value.astimezone(UTC)


class EmpiricalChartResponseModel:
    """Hierarchically smoothed categorical likelihoods with optional theory prior."""

    def __init__(
        self,
        artifact: ModelArtifact,
        theory_priors: Mapping[str, Mapping[str, float]] | None = None,
    ) -> None:
        self.artifact = artifact
        supplied = _normalize_theory_priors(theory_priors or {})
        frozen = _normalize_theory_priors(artifact.theory_priors)
        if supplied and supplied != frozen:
            raise ValueError("runtime theory priors do not match the frozen model artifact")
        self.theory_priors = frozen

    @classmethod
    def fit(
        cls,
        cases: Sequence[HumanCase],
        *,
        model_id: str,
        questionnaire_version: str,
        split_manifest_hash: str,
        feature_names: Sequence[str],
        alpha: float = 2.0,
        theory_priors: Mapping[str, Mapping[str, float]] | None = None,
        theory_strength: float = 0.0,
        feature_schema_version: str = "chart-features-flat-v1",
        created_at_utc: datetime | None = None,
    ) -> EmpiricalChartResponseModel:
        if alpha <= 0.0 or theory_strength < 0.0:
            raise ValueError("regularization strengths must be non-negative with alpha > 0")
        enforce_training_cohort(list(cases))
        if not cases:
            raise ValueError("at least one development person is required")
        if not feature_names or len(set(feature_names)) != len(feature_names):
            raise ValueError("feature_names must be a nonempty unique sequence")
        if not feature_schema_version:
            raise ValueError("feature_schema_version cannot be empty")
        frozen_theory_priors = _normalize_theory_priors(theory_priors or {})
        if theory_strength > 0.0 and not frozen_theory_priors:
            raise ValueError("positive theory_strength requires frozen theory priors")
        ordered_cases = tuple(sorted(cases, key=lambda case: case.participant_id))
        identifiers = [case.participant_id for case in ordered_cases]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("development people must be unique")
        marginal: dict[str, defaultdict[str, float]] = defaultdict(lambda: defaultdict(float))
        conditional: dict[str, dict[str, dict[str, defaultdict[str, float]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        )
        for case in ordered_cases:
            for question, answer in case.responses.items():
                reliability = case.response_reliability.get(question, 1.0)
                marginal[question][answer] += reliability
                for feature in feature_names:
                    if feature in case.chart_features:
                        token = _feature_token(case.chart_features[feature])
                        conditional[question][feature][token][answer] += reliability
        vocabularies = {question: tuple(sorted(counts)) for question, counts in marginal.items()}
        if not vocabularies:
            raise ValueError("development records contain no responses")
        artifact_payload = {
            "participants": identifiers,
            "responses": {case.participant_id: case.responses for case in ordered_cases},
            "response_reliability": {
                case.participant_id: case.response_reliability for case in ordered_cases
            },
            "features": {case.participant_id: case.chart_features for case in ordered_cases},
        }
        artifact = ModelArtifact(
            model_id=model_id,
            training_dataset_hash=sha256_json(artifact_payload),
            split_manifest_hash=split_manifest_hash,
            questionnaire_version=questionnaire_version,
            feature_schema_version=feature_schema_version,
            feature_names=tuple(feature_names),
            alpha=alpha,
            theory_strength=theory_strength,
            answer_vocabularies=vocabularies,
            marginal_counts={q: dict(counts) for q, counts in marginal.items()},
            conditional_counts={
                q: {
                    feature: {token: dict(counts) for token, counts in values.items()}
                    for feature, values in features.items()
                }
                for q, features in conditional.items()
            },
            theory_priors=frozen_theory_priors,
            created_at_utc=created_at_utc or datetime.now(UTC),
        )
        return cls(artifact)

    def response_distribution(
        self, question_id: str, chart_features: Mapping[str, Any]
    ) -> dict[str, float]:
        vocabulary = self.artifact.answer_vocabularies.get(question_id)
        if not vocabulary:
            return {}
        marginal = self.artifact.marginal_counts[question_id]
        total = sum(marginal.values())
        k = len(vocabulary)
        prior = {
            answer: (marginal.get(answer, 0) + self.artifact.alpha / k)
            / (total + self.artifact.alpha)
            for answer in vocabulary
        }
        log_weights = {answer: math.log(prior[answer]) for answer in vocabulary}
        evidence_layers = 1.0
        for feature in self.artifact.feature_names:
            if feature not in chart_features:
                continue
            token = _feature_token(chart_features[feature])
            counts = (
                self.artifact.conditional_counts.get(question_id, {}).get(feature, {}).get(token)
            )
            if not counts:
                continue
            feature_total = sum(counts.values())
            shrink = feature_total / (feature_total + self.artifact.alpha)
            for answer in vocabulary:
                conditional = (counts.get(answer, 0) + self.artifact.alpha * prior[answer]) / (
                    feature_total + self.artifact.alpha
                )
                log_weights[answer] += shrink * math.log(conditional / prior[answer])
            evidence_layers += shrink
        theory = self.theory_priors.get(question_id, {})
        if theory and self.artifact.theory_strength > 0.0:
            for answer in vocabulary:
                probability = max(theory.get(answer, 0.0), 1e-12)
                log_weights[answer] += self.artifact.theory_strength * math.log(probability)
            evidence_layers += self.artifact.theory_strength
        scaled = {answer: value / evidence_layers for answer, value in log_weights.items()}
        ceiling = max(scaled.values())
        weights = {answer: math.exp(value - ceiling) for answer, value in scaled.items()}
        normalizer = sum(weights.values())
        return {answer: value / normalizer for answer, value in weights.items()}

    def log2_score(
        self,
        responses: Mapping[str, str],
        chart_features: Mapping[str, Any],
        reliability: Mapping[str, float] | None = None,
    ) -> float:
        reliabilities = reliability or {}
        score = 0.0
        for question, answer in responses.items():
            distribution = self.response_distribution(question, chart_features)
            if not distribution or answer not in distribution:
                continue
            weight = reliabilities.get(question, 1.0)
            if not 0.0 <= weight <= 1.0:
                raise ValueError("response reliability must be within [0, 1]")
            score += weight * math.log2(max(distribution[answer], 1e-12))
        return score


def _normalize_theory_priors(
    priors: Mapping[str, Mapping[str, float]],
) -> dict[str, dict[str, float]]:
    normalized: dict[str, dict[str, float]] = {}
    for question_id, weights in sorted(priors.items()):
        converted = {str(answer): float(weight) for answer, weight in sorted(weights.items())}
        if not converted:
            raise ValueError(f"theory prior for {question_id} cannot be empty")
        if not all(math.isfinite(weight) and weight >= 0.0 for weight in converted.values()):
            raise ValueError("theory prior weights must be finite and nonnegative")
        total = sum(converted.values())
        if total <= 0.0:
            raise ValueError(f"theory prior for {question_id} must have positive mass")
        normalized[str(question_id)] = {
            answer: weight / total for answer, weight in converted.items()
        }
    return normalized
