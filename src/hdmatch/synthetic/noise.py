"""Seeded, chart-independent questionnaire noise models."""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

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

    def __post_init__(self) -> None:
        for label, value in (
            ("missing_rate", self.missing_rate),
            ("flip_rate", self.flip_rate),
            ("cluster_dropout_rate", self.cluster_dropout_rate),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{label} must be in [0, 1]")
        for label, values in (
            ("confidence_values", self.confidence_values),
            ("reliability_values", self.reliability_values),
        ):
            if not values or any(not 0.0 <= value <= 1.0 for value in values):
                raise ValueError(f"{label} must be nonempty and within [0, 1]")


PARAMETERS: dict[NoiseTier, NoiseParameters] = {
    NoiseTier.ORACLE: NoiseParameters(0.0, 0.0, 0.0, (1.0,), (1.0,)),
    NoiseTier.LOW: NoiseParameters(0.05, 0.02, 0.0, (0.75, 1.0), (0.75, 1.0)),
    NoiseTier.MEDIUM: NoiseParameters(0.15, 0.10, 0.10, (0.5, 0.75, 1.0), (0.5, 0.75, 1.0)),
    NoiseTier.ADVERSARIAL: NoiseParameters(0.30, 0.25, 0.20, (0.25, 0.5, 0.75), (0.25, 0.5, 0.75)),
}


def noise_parameters_payload(tier: NoiseTier) -> dict[str, Any]:
    """Return canonical public simulator settings for manifests and audits."""

    parameters = PARAMETERS[tier]
    return {
        "missing_rate": parameters.missing_rate,
        "flip_rate": parameters.flip_rate,
        "cluster_dropout_rate": parameters.cluster_dropout_rate,
        "confidence_values": list(parameters.confidence_values),
        "reliability_values": list(parameters.reliability_values),
        "conditioning": "chart-independent-except-declared-measurement-domain",
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
