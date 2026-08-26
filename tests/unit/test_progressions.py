"""Tests for the frozen day-for-year progression convention."""

from datetime import UTC, datetime, timedelta

import pytest

from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisMetadata,
    NodeConvention,
)
from hdmatch.chart.progressions import (
    TROPICAL_YEAR_DAYS,
    progression_snapshot,
    secondary_progressed_instant,
    secondary_progressed_instant_for_age,
)


class _FakeProvider:
    @property
    def metadata(self) -> EphemerisMetadata:
        return EphemerisMetadata(
            provider="fake",
            library_version="test",
            files=(),
            calculation_flags=(),
            coordinate_frame="test",
            node_convention=NodeConvention.TRUE,
        )

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        offset = (at_utc - datetime(2000, 1, 1, tzinfo=UTC)).total_seconds() / 86_400.0
        return EclipticPosition(offset % 360.0, float(len(body.value)))

    def max_abs_speed_degrees_per_day(self, _body: CelestialBody) -> float:
        return 20.0

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9


def test_age_26_maps_to_26_ephemeris_days() -> None:
    birth = datetime(1985, 1, 29, 10, 25, tzinfo=UTC)
    observed = birth + timedelta(days=TROPICAL_YEAR_DAYS * 26.0)
    assert secondary_progressed_instant(birth, observed) == birth + timedelta(days=26.0)
    assert secondary_progressed_instant_for_age(birth, 26.0) == birth + timedelta(days=26.0)


def test_progression_snapshot_uses_mapped_instant_for_all_bodies() -> None:
    birth = datetime(2000, 1, 1, tzinfo=UTC)
    observed = birth + timedelta(days=TROPICAL_YEAR_DAYS * 5.0)
    snapshot = progression_snapshot(
        _FakeProvider(),
        birth_utc=birth,
        observed_at_utc=observed,
        bodies=(CelestialBody.SUN, CelestialBody.MOON),
    )
    assert snapshot.progressed_at_utc == birth + timedelta(days=5.0)
    assert snapshot.elapsed_age_years == pytest.approx(5.0)
    assert [item.body for item in snapshot.positions] == [CelestialBody.SUN, CelestialBody.MOON]


def test_progression_rejects_prebirth_observation() -> None:
    birth = datetime(2000, 1, 2, tzinfo=UTC)
    with pytest.raises(ValueError, match="precede"):
        secondary_progressed_instant(birth, datetime(2000, 1, 1, tzinfo=UTC))
