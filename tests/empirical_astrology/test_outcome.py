from __future__ import annotations

import pytest

from hdmatch.empirical_astrology.outcome import (
    SCALE_ORDER,
    SCORING_KEY,
    ipip_pair_distance,
    responses_to_pair_distance,
    score_ipip50,
)


def _keyed_responses(high: bool) -> dict[int, int]:
    responses: dict[int, int] = {}
    for scale in SCALE_ORDER:
        for item in SCORING_KEY[scale]["positive"]:
            responses[item] = 5 if high else 1
        for item in SCORING_KEY[scale]["negative"]:
            responses[item] = 1 if high else 5
    assert set(responses) == set(range(1, 51))
    return responses


def test_ipip_key_has_five_complete_nonoverlapping_scales() -> None:
    all_items = [
        item
        for scale in SCALE_ORDER
        for direction in ("positive", "negative")
        for item in SCORING_KEY[scale][direction]
    ]
    assert sorted(all_items) == list(range(1, 51))
    assert all(
        len(SCORING_KEY[scale]["positive"]) + len(SCORING_KEY[scale]["negative"]) == 10
        for scale in SCALE_ORDER
    )


def test_ipip_scoring_and_distance_endpoints() -> None:
    low = _keyed_responses(False)
    high = _keyed_responses(True)
    assert score_ipip50(low) == {scale: 1.0 for scale in SCALE_ORDER}
    assert score_ipip50(high) == {scale: 5.0 for scale in SCALE_ORDER}
    assert responses_to_pair_distance(low, low) == 0.0
    assert responses_to_pair_distance(low, high) == 1.0
    assert ipip_pair_distance(score_ipip50(high), score_ipip50(low)) == 1.0


def test_ipip_rejects_missing_extra_and_invalid_responses() -> None:
    valid = _keyed_responses(True)
    for malformed in (
        {key: value for key, value in valid.items() if key != 50},
        {**valid, 51: 3},
        {**valid, 1: 0},
        {**valid, 1: True},
    ):
        with pytest.raises(ValueError):
            score_ipip50(malformed)
