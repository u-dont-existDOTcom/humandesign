"""Seeded, chart-independent questionnaire noise models."""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum

from hdmatch.schemas import BehavioralResponse


class NoiseTier(StrEnum):
    ORACLE = "oracle"
    LOW = "low"
    MEDIUM = "medium"
    ADVERSARIAL = "adversarial"


@dataclass(frozen=True)
class NoiseParameters:
    missing_rate: float
    flip_rate: float
    cluster_dropout_rate: float
    confidence_values: tuple[float, ...]
    reliability_values: tuple[float, ...]


PARAMETERS: dict[NoiseTier, NoiseParameters] = {
    NoiseTier.ORACLE: NoiseParameters(0.0, 0.0, 0.0, (1.0,), (1.0,)),
    NoiseTier.LOW: NoiseParameters(0.05, 0.02, 0.0, (0.75, 1.0), (0.75, 1.0)),
    NoiseTier.MEDIUM: NoiseParameters(0.15, 0.10, 0.10, (0.5, 0.75, 1.0), (0.5, 0.75, 1.0)),
    NoiseTier.ADVERSARIAL: NoiseParameters(0.30, 0.25, 0.20, (0.25, 0.5, 0.75), (0.25, 0.5, 0.75)),
}


def apply_noise(
    responses: Sequence[BehavioralResponse],
    *,
    answer_spaces: Mapping[str, Sequence[str]],
    seed: int,
    tier: NoiseTier,
) -> tuple[BehavioralResponse, ...]:
    """Apply declared noise without conditioning on chart or hidden birth state."""

    parameters = PARAMETERS[tier]
    rng = random.Random(seed)
    cluster_dropout: dict[str, bool] = defaultdict(bool)
    for cluster_id in sorted({response.cluster_id for response in responses}):
        cluster_dropout[cluster_id] = rng.random() < parameters.cluster_dropout_rate
    result: list[BehavioralResponse] = []
    for response in responses:
        if cluster_dropout[response.cluster_id] or rng.random() < parameters.missing_rate:
            continue
        answer = response.answer
        alternatives = sorted(set(answer_spaces.get(response.question_id, ())) - {answer})
        if alternatives and rng.random() < parameters.flip_rate:
            answer = rng.choice(alternatives)
        result.append(
            response.model_copy(
                update={
                    "answer": answer,
                    "behavioral_confidence": rng.choice(parameters.confidence_values),
                    "measurement_reliability": rng.choice(parameters.reliability_values),
                }
            )
        )
    return tuple(result)
