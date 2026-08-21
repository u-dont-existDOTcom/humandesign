from __future__ import annotations

from datetime import UTC, datetime

import pytest

from hdmatch.chart.boundaries import (
    BoundaryResolution,
    audit_interval_partition,
    build_stable_intervals,
    enumerate_chart_boundaries,
)
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisMetadata,
    NodeConvention,
)
from hdmatch.chart.rave_mandala import longitude_to_gate_line


class BoundaryProvider:
    def __init__(self, epoch: datetime, *, design_only: bool = False, linear: bool = False) -> None:
        self.epoch = epoch
        self.design_only = design_only
        self.linear = linear
        self._metadata = EphemerisMetadata(
            provider="analytic-boundary-test",
            library_version="1",
            files=(),
            calculation_flags=("analytic",),
            coordinate_frame="test",
            node_convention=NodeConvention.TRUE,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        days = (at_utc - self.epoch).total_seconds() / 86400.0
        if body is CelestialBody.SUN:
            return EclipticPosition((100.0 + days) % 360.0, 1.0)
        if body is not CelestialBody.MERCURY:
            return EclipticPosition(10.0, 0.0)

        center = self.epoch
        if self.design_only:
            center = self.epoch.replace() - _days(88)
        elapsed = (at_utc - center).total_seconds()
        if self.linear:
            longitude = 301.99 + elapsed * (0.02 / 60.0)
            return EclipticPosition(longitude % 360.0, 28.8)
        if elapsed < 0.0 or elapsed > 600.0:
            return EclipticPosition(301.8, 0.0)
        if elapsed <= 300.0:
            longitude = 301.8 + elapsed * (0.4 / 300.0)
            speed = 115.2
        else:
            longitude = 302.2 - (elapsed - 300.0) * (0.4 / 300.0)
            speed = -115.2
        return EclipticPosition(longitude, speed)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        if body is CelestialBody.SUN:
            return 1.1
        if body is CelestialBody.MERCURY:
            return 120.0
        return 0.1

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9


def _days(value: int):  # type annotation kept local to avoid obscuring test formulas
    from datetime import timedelta

    return timedelta(days=value)


def test_boundary_inside_one_minute_is_found_to_declared_tolerance() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = BoundaryProvider(start, linear=True)

    events = enumerate_chart_boundaries(
        provider,
        start,
        start + _days(1) / 1440,
        bodies=(CelestialBody.MERCURY,),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.01,
    )
    personality = [item for item in events if item.side == "personality"]

    assert len(personality) == 1
    assert (personality[0].at_utc - start).total_seconds() == pytest.approx(30.0, abs=0.01)
    assert personality[0].before_gate == 60
    assert personality[0].after_gate == 41


def test_two_interior_crossings_found_when_endpoints_have_same_gate() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = BoundaryProvider(start)
    end = start + _days(1) / 144

    events = enumerate_chart_boundaries(
        provider,
        start,
        end,
        bodies=(CelestialBody.MERCURY,),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.01,
        max_scan_step_seconds=600.0,
    )
    personality = [item for item in events if item.side == "personality"]

    assert len(personality) == 2
    assert [(item.at_utc - start).total_seconds() for item in personality] == pytest.approx(
        [150.0, 450.0], abs=0.01
    )
    assert personality[0].before_gate == personality[1].after_gate == 60
    assert personality[0].after_gate == personality[1].before_gate == 41


def test_design_side_events_are_included_when_personality_is_stable() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = BoundaryProvider(start, design_only=True)
    end = start + _days(1) / 144

    events = enumerate_chart_boundaries(
        provider,
        start,
        end,
        bodies=(CelestialBody.MERCURY,),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.01,
        max_scan_step_seconds=600.0,
    )

    assert [item for item in events if item.side == "personality"] == []
    design = [item for item in events if item.side == "design"]
    assert len(design) == 2
    assert all(item.ephemeris_utc < item.at_utc for item in design)


def test_stable_intervals_are_continuous_and_preserve_a_b_a_states() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = BoundaryProvider(start)
    end = start + _days(1) / 144
    events = enumerate_chart_boundaries(
        provider,
        start,
        end,
        bodies=(CelestialBody.MERCURY,),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.01,
        max_scan_step_seconds=600.0,
    )
    personality_events = tuple(item for item in events if item.side == "personality")

    intervals = build_stable_intervals(
        start,
        end,
        personality_events,
        lambda at: (
            longitude_to_gate_line(provider.position(CelestialBody.MERCURY, at).longitude).gate
        ),
    )

    assert [item.features for item in intervals] == [60, 41, 60]
    assert len(intervals) == 3
    audit_interval_partition(intervals, start, end)
