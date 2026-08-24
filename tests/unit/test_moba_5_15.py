from __future__ import annotations

import math
from datetime import UTC, date, datetime

import pytest

from hdmatch.human.moba_5_15 import (
    frozen_calendar_controls,
    resolve_oslo_utc_candidates,
    z_5_15_from_longitudes,
)


def test_z_5_15_uses_frozen_half_open_windows() -> None:
    assert z_5_15_from_longitudes((251.375, 88.25)) is True
    assert z_5_15_from_longitudes((256.999999, 93.874999)) is True
    assert z_5_15_from_longitudes((257.0, 88.25)) is False
    assert z_5_15_from_longitudes((251.375, 93.875)) is False
    assert z_5_15_from_longitudes((611.375, -271.75)) is True


def test_z_5_15_rejects_nonfinite_longitudes() -> None:
    with pytest.raises(ValueError, match="finite"):
        z_5_15_from_longitudes((math.nan, 88.25))


def test_oslo_ordinary_time_resolves_once() -> None:
    candidates = resolve_oslo_utc_candidates(birth_date=date(2004, 6, 1), hhmm="1230")
    assert candidates == (datetime(2004, 6, 1, 10, 30, tzinfo=UTC),)


def test_oslo_autumn_fold_returns_both_real_instants() -> None:
    candidates = resolve_oslo_utc_candidates(birth_date=date(2004, 10, 31), hhmm="0230")
    assert candidates == (
        datetime(2004, 10, 31, 0, 30, tzinfo=UTC),
        datetime(2004, 10, 31, 1, 30, tzinfo=UTC),
    )


def test_oslo_spring_gap_fails_closed() -> None:
    with pytest.raises(ValueError, match="nonexistent"):
        resolve_oslo_utc_candidates(birth_date=date(2004, 3, 28), hhmm="0230")


@pytest.mark.parametrize("hhmm", ["123", "12:30", "abcd", "2400", "1260"])
def test_invalid_hhmm_fails_closed(hhmm: str) -> None:
    with pytest.raises(ValueError):
        resolve_oslo_utc_candidates(birth_date=date(2004, 1, 1), hhmm=hhmm)


def test_frozen_calendar_controls_are_deterministic_and_low_frequency() -> None:
    controls = frozen_calendar_controls(birth_date=date(2004, 1, 1), hhmm="0000")
    assert controls.birth_year == 2004
    assert controls.day_of_year_sin_1 == pytest.approx(0.0)
    assert controls.day_of_year_cos_1 == pytest.approx(1.0)
    assert controls.day_of_year_sin_2 == pytest.approx(0.0)
    assert controls.day_of_year_cos_2 == pytest.approx(1.0)
    assert controls.time_of_day_sin_1 == pytest.approx(0.0)
    assert controls.time_of_day_cos_1 == pytest.approx(1.0)
    assert controls.time_of_day_sin_2 == pytest.approx(0.0)
    assert controls.time_of_day_cos_2 == pytest.approx(1.0)
