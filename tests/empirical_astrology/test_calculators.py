from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

import pytest

from hdmatch.empirical_astrology import (
    AspectPhase,
    aspect_phase_from_forward_step,
    distance_to_aspect,
    karaka_kendra_feature,
    minimum_axis_distance,
    navamsa_sign_index,
    near_time_distance_minutes,
    rank_seven_karakas,
    rasi_sign_index,
    unsigned_angular_separation,
    within_sign_degree,
)


def test_unsigned_angular_separation_wraps_and_is_symmetric() -> None:
    assert unsigned_angular_separation(359.0, 1.0) == 2.0
    assert unsigned_angular_separation(1.0, 359.0) == 2.0
    assert unsigned_angular_separation(0.0, 180.0) == 180.0


def test_distance_to_aspect_uses_unsigned_exact_angle() -> None:
    assert distance_to_aspect(10.0, 97.0, aspect_angle=90.0) == 3.0
    assert distance_to_aspect(359.0, 1.0, aspect_angle=0.0) == 2.0
    with pytest.raises(ValueError, match="between 0 and 180"):
        distance_to_aspect(0.0, 1.0, aspect_angle=181.0)


@pytest.mark.parametrize(
    ("forward_b", "expected"),
    [
        (88.0, AspectPhase.APPLYING),
        (84.0, AspectPhase.SEPARATING),
        (85.0, AspectPhase.STATIONARY_OR_UNRESOLVED),
    ],
)
def test_aspect_phase_uses_forward_distance(
    forward_b: float,
    expected: AspectPhase,
) -> None:
    assert (
        aspect_phase_from_forward_step(
            0.0,
            85.0,
            0.0,
            forward_b,
            aspect_angle=90.0,
        )
        is expected
    )


def test_minimum_axis_distance_uses_all_four_axes() -> None:
    assert minimum_axis_distance(
        272.0,
        ascendant_longitude=0.0,
        midheaven_longitude=90.0,
    ) == 2.0


def test_near_time_distance_normalizes_timezones() -> None:
    left = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    right = datetime(2026, 1, 1, 13, 5, tzinfo=timezone(timedelta(hours=1)))
    assert near_time_distance_minutes(left, right) == 5.0
    with pytest.raises(ValueError, match="timezone-aware"):
        near_time_distance_minutes(left.replace(tzinfo=None), right)


def test_rasi_and_within_sign_degree_wrap() -> None:
    assert rasi_sign_index(30.0) == 1
    assert rasi_sign_index(390.0) == 1
    assert within_sign_degree(44.5) == 14.5


@pytest.mark.parametrize(
    ("longitude", "expected"),
    [(0.0, 0), (29.999, 8), (30.0, 9), (60.0, 6), (359.999, 11)],
)
def test_navamsa_sign_index(longitude: float, expected: int) -> None:
    assert navamsa_sign_index(longitude) == expected


def _seven() -> dict[str, float]:
    return {
        "sun": 29.0,
        "moon": 25.0,
        "mercury": 20.0,
        "venus": 15.0,
        "mars": 10.0,
        "jupiter": 5.0,
        "saturn": 1.0,
    }


def test_rank_seven_karakas_exposes_atma_and_sixth_putra_positions() -> None:
    ranked = rank_seven_karakas(_seven())
    assert ranked[0] == "sun"
    assert ranked[5] == "jupiter"


def test_karaka_kendra_feature_returns_intermediate_state() -> None:
    result = karaka_kendra_feature(_seven())
    assert result.atmakaraka_body == "sun"
    assert result.putrakaraka_body == "jupiter"
    assert result.kendra_in_rasi is True
    assert result.kendra_in_navamsa is False
    assert result.kendra_in_either is True


def test_karaka_rank_fails_closed_on_count_or_tie() -> None:
    with pytest.raises(ValueError, match="exactly seven"):
        rank_seven_karakas({"sun": 1.0})
    tied = _seven()
    tied["saturn"] = 35.0
    with pytest.raises(ValueError, match="rank is unresolved"):
        rank_seven_karakas(tied)
