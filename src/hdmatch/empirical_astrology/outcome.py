"""Frozen IPIP-50 scoring and pair-distance outcome for the v1b protocol."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Final

SCALE_ORDER: Final[tuple[str, ...]] = (
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "emotional_stability",
    "intellect_imagination",
)

SCORING_KEY: Final[dict[str, dict[str, tuple[int, ...]]]] = {
    "extraversion": {
        "positive": (1, 11, 21, 31, 41),
        "negative": (6, 16, 26, 36, 46),
    },
    "agreeableness": {
        "positive": (7, 17, 27, 37, 42, 47),
        "negative": (2, 12, 22, 32),
    },
    "conscientiousness": {
        "positive": (3, 13, 23, 33, 43, 48),
        "negative": (8, 18, 28, 38),
    },
    "emotional_stability": {
        "positive": (9, 19),
        "negative": (4, 14, 24, 29, 34, 39, 44, 49),
    },
    "intellect_imagination": {
        "positive": (5, 15, 25, 35, 40, 45, 50),
        "negative": (10, 20, 30),
    },
}


def validate_ipip50_responses(responses: Mapping[int, int]) -> dict[int, int]:
    """Require one integer response in 1..5 for every official item 1..50."""

    if set(responses) != set(range(1, 51)):
        missing = sorted(set(range(1, 51)) - set(responses))
        extra = sorted(set(responses) - set(range(1, 51)))
        raise ValueError(f"IPIP-50 requires exactly items 1..50; missing={missing}, extra={extra}")
    result: dict[int, int] = {}
    for item in range(1, 51):
        value = responses[item]
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError(f"IPIP-50 item {item} must be an integer in 1..5")
        result[item] = value
    return result


def score_ipip50(responses: Mapping[int, int]) -> dict[str, float]:
    """Return the five frozen ten-item means without imputation or scaling."""

    valid = validate_ipip50_responses(responses)
    scores: dict[str, float] = {}
    for scale in SCALE_ORDER:
        key = SCORING_KEY[scale]
        values = [valid[item] for item in key["positive"]]
        values.extend(6 - valid[item] for item in key["negative"])
        if len(values) != 10:
            raise AssertionError(f"frozen scoring key for {scale} does not contain ten items")
        scores[scale] = sum(values) / 10.0
    return scores


def ipip_pair_distance(
    left_scores: Mapping[str, float],
    right_scores: Mapping[str, float],
) -> float:
    """Return normalized equal-scale RMS profile distance in [0,1]."""

    if set(left_scores) != set(SCALE_ORDER) or set(right_scores) != set(SCALE_ORDER):
        raise ValueError("both profiles must contain exactly the five frozen scales")
    squared: list[float] = []
    for scale in SCALE_ORDER:
        left = float(left_scores[scale])
        right = float(right_scores[scale])
        if not math.isfinite(left) or not math.isfinite(right):
            raise ValueError("profile scores must be finite")
        if not 1.0 <= left <= 5.0 or not 1.0 <= right <= 5.0:
            raise ValueError("profile scores must be in [1,5]")
        squared.append(((left - right) / 4.0) ** 2)
    result = math.sqrt(sum(squared) / len(SCALE_ORDER))
    if not 0.0 <= result <= 1.0:
        raise AssertionError("normalized profile distance left [0,1]")
    return result


def responses_to_pair_distance(
    left_responses: Mapping[int, int],
    right_responses: Mapping[int, int],
) -> float:
    """Score two complete response maps and return the primary outcome."""

    return ipip_pair_distance(score_ipip50(left_responses), score_ipip50(right_responses))
