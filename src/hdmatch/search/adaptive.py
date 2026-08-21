"""Answer-blind expected-information-gain question selection."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


def _entropy(probabilities: Sequence[float]) -> float:
    return -sum(value * math.log2(value) for value in probabilities if value > 0.0)


def _normalized(weights: Sequence[float]) -> tuple[float, ...]:
    total = sum(weights)
    if total <= 0.0:
        raise ValueError("candidate weights must contain positive mass")
    return tuple(value / total for value in weights)


@dataclass(frozen=True)
class QuestionUtility:
    question_id: str
    expected_information_gain: float
    adjusted_utility: float
    expected_reliability: float
    burden: float


def expected_information_gain(
    candidate_weights: Sequence[float],
    answer_likelihoods: Sequence[Mapping[str, float]],
) -> float:
    """Compute IG without access to any hidden/true candidate identity."""

    if len(candidate_weights) != len(answer_likelihoods):
        raise ValueError("one likelihood distribution is required per candidate")
    prior = _normalized(candidate_weights)
    answers = sorted({answer for row in answer_likelihoods for answer in row})
    expected_posterior_entropy = 0.0
    for answer in answers:
        joint = [
            prior[index] * answer_likelihoods[index].get(answer, 0.0) for index in range(len(prior))
        ]
        answer_probability = sum(joint)
        if answer_probability <= 0.0:
            continue
        posterior = [value / answer_probability for value in joint]
        expected_posterior_entropy += answer_probability * _entropy(posterior)
    return _entropy(prior) - expected_posterior_entropy


def select_next_question(
    candidate_weights: Sequence[float],
    likelihoods_by_question: Mapping[str, Sequence[Mapping[str, float]]],
    expected_reliability: Mapping[str, float] | None = None,
    burden: Mapping[str, float] | None = None,
) -> QuestionUtility | None:
    reliability = expected_reliability or {}
    costs = burden or {}
    candidates: list[QuestionUtility] = []
    for question_id in sorted(likelihoods_by_question):
        ig = expected_information_gain(candidate_weights, likelihoods_by_question[question_id])
        answerability = reliability.get(question_id, 1.0)
        cost = costs.get(question_id, 0.0)
        if not 0.0 <= answerability <= 1.0:
            raise ValueError("expected reliability must be within [0, 1]")
        candidates.append(
            QuestionUtility(
                question_id=question_id,
                expected_information_gain=ig,
                adjusted_utility=ig * answerability - cost,
                expected_reliability=answerability,
                burden=cost,
            )
        )
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item.adjusted_utility, item.question_id))
