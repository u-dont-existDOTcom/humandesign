from __future__ import annotations

from datetime import datetime

import pytest

from hdmatch.chart.timezone import (
    AmbiguousLocalTimeError,
    LocalTimeStatus,
    NonexistentLocalTimeError,
    resolve_local_datetime,
)


def test_new_york_fall_back_returns_both_folds() -> None:
    result = resolve_local_datetime(datetime(2024, 11, 3, 1, 30), "America/New_York")

    assert result.status is LocalTimeStatus.AMBIGUOUS
    assert [item.fold for item in result.candidates] == [0, 1]
    assert [item.utc.isoformat() for item in result.candidates] == [
        "2024-11-03T05:30:00+00:00",
        "2024-11-03T06:30:00+00:00",
    ]
    with pytest.raises(AmbiguousLocalTimeError):
        result.require_unique()


def test_explicit_fold_selects_one_ambiguous_instant() -> None:
    result = resolve_local_datetime(
        datetime(2024, 11, 3, 1, 30),
        "America/New_York",
        fold=1,
    )

    assert result.status is LocalTimeStatus.UNIQUE
    assert result.require_unique().utc.isoformat() == "2024-11-03T06:30:00+00:00"


@pytest.mark.parametrize(
    ("local", "zone"),
    [
        (datetime(2024, 3, 10, 2, 30), "America/New_York"),
        (datetime(2011, 12, 30, 12, 0), "Pacific/Apia"),
    ],
)
def test_nonexistent_local_times_are_not_coerced(local: datetime, zone: str) -> None:
    result = resolve_local_datetime(local, zone)

    assert result.status is LocalTimeStatus.NONEXISTENT
    assert result.candidates == ()
    with pytest.raises(NonexistentLocalTimeError):
        result.require_unique()


def test_lord_howe_half_hour_fall_back_is_ambiguous() -> None:
    result = resolve_local_datetime(datetime(2024, 4, 7, 1, 45), "Australia/Lord_Howe")

    assert result.status is LocalTimeStatus.AMBIGUOUS
    assert (result.candidates[1].utc - result.candidates[0].utc).total_seconds() == 30 * 60


def test_pre_standard_local_mean_time_is_flagged() -> None:
    result = resolve_local_datetime(datetime(1880, 1, 1, 12), "Europe/Paris")

    assert result.status is LocalTimeStatus.UNIQUE
    assert result.pre_standard_time_uncertain is True


def test_abbreviation_and_aware_input_are_rejected() -> None:
    with pytest.raises(ValueError, match="IANA"):
        resolve_local_datetime(datetime(2024, 1, 1), "CST")
    with pytest.raises(ValueError, match="naive"):
        resolve_local_datetime(datetime.now().astimezone(), "Europe/Paris")
