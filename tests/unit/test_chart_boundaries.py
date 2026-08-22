from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

import hdmatch.chart.boundaries as boundary_module
from hdmatch.chart.boundaries import (
    BOUNDARY_POLICY_VERSION,
    BoundaryCompletenessError,
    BoundaryProvenanceError,
    BoundaryResolution,
    audit_interval_partition,
    build_production_chart_state_intervals,
    build_stable_intervals,
    enumerate_chart_boundaries,
)
from hdmatch.chart.design_moment import solve_design_moment
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


class NonlinearDesignProvider(BoundaryProvider):
    """Monotone non-uniform Sun for rejecting fixed-day Design subtraction."""

    def __init__(self, epoch: datetime) -> None:
        super().__init__(epoch)
        desired_boundary = epoch + _seconds(300)
        self.design_boundary_utc = solve_design_moment(self, desired_boundary).design_utc

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        days = (at_utc - self.epoch).total_seconds() / 86400.0
        if body is CelestialBody.SUN:
            longitude = 100.0 + days + 0.001 * days * days
            speed = 1.0 + 0.002 * days
            return EclipticPosition(longitude % 360.0, speed)
        if body is not CelestialBody.MERCURY:
            return EclipticPosition(10.0, 0.0)
        elapsed = (at_utc - self.design_boundary_utc).total_seconds()
        if elapsed <= -600.0:
            return EclipticPosition(301.8, 0.0)
        if elapsed >= 600.0:
            return EclipticPosition(302.2, 0.0)
        return EclipticPosition(302.0 + elapsed / 3000.0, 28.8)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        if body is CelestialBody.SUN:
            return 1.2
        if body is CelestialBody.MERCURY:
            return 30.0
        return 0.1

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.75


class ExcessSpeedProvider(BoundaryProvider):
    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        if body is CelestialBody.MERCURY:
            return EclipticPosition(301.9, 121.0)
        return super().position(body, at_utc)


class NearSimultaneousProvider(BoundaryProvider):
    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        if body in (CelestialBody.MERCURY, CelestialBody.VENUS):
            elapsed = (at_utc - self.epoch).total_seconds()
            crossing = 30.0 if body is CelestialBody.MERCURY else 30.005
            longitude = 302.0 + (elapsed - crossing) / 3000.0
            return EclipticPosition(longitude % 360.0, 28.8)
        return super().position(body, at_utc)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        if body in (CelestialBody.MERCURY, CelestialBody.VENUS):
            return 30.0
        return super().max_abs_speed_degrees_per_day(body)


def _days(value: int):  # type annotation kept local to avoid obscuring test formulas
    from datetime import timedelta

    return timedelta(days=value)


def _seconds(value: float):
    from datetime import timedelta

    return timedelta(seconds=value)


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
    assert longitude_to_gate_line(
        provider.position(CelestialBody.MERCURY, start).longitude
    ).gate == longitude_to_gate_line(
        provider.position(CelestialBody.MERCURY, end).longitude
    ).gate

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


def test_design_boundaries_invert_exact_solar_arc_instead_of_subtracting_fixed_days() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = NonlinearDesignProvider(start)
    end = start + _seconds(600)

    events = enumerate_chart_boundaries(
        provider,
        start,
        end,
        bodies=(CelestialBody.MERCURY,),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.01,
    )

    assert [event for event in events if event.side == "personality"] == []
    design = [event for event in events if event.side == "design"]
    assert len(design) == 1
    assert (design[0].at_utc - start).total_seconds() == pytest.approx(300.0, abs=0.02)
    exact = solve_design_moment(provider, design[0].at_utc)
    assert abs((design[0].ephemeris_utc - exact.design_utc).total_seconds()) <= 0.02
    fixed_day_design = design[0].at_utc - _days(88)
    assert abs((design[0].ephemeris_utc - fixed_day_design).total_seconds()) > 86400.0


def test_observed_speed_above_declared_bound_fails_instead_of_missing_an_event() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = ExcessSpeedProvider(start)

    with pytest.raises(BoundaryCompletenessError, match="exceeds declared"):
        enumerate_chart_boundaries(
            provider,
            start,
            start + _seconds(60),
            bodies=(CelestialBody.MERCURY,),
            resolution=BoundaryResolution.GATE,
        )


def test_production_provenance_requirement_rejects_analytic_provider() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = BoundaryProvider(start)

    with pytest.raises(BoundaryProvenanceError, match="SwissEphemerisProvider"):
        enumerate_chart_boundaries(
            provider,
            start,
            start + _seconds(60),
            bodies=(CelestialBody.MERCURY,),
            resolution=BoundaryResolution.GATE,
            require_swieph_provenance=True,
        )


def test_near_simultaneous_roots_share_one_deterministic_interval_cut() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = NearSimultaneousProvider(start)

    events = enumerate_chart_boundaries(
        provider,
        start,
        start + _seconds(60),
        bodies=(CelestialBody.MERCURY, CelestialBody.VENUS),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.001,
        event_group_tolerance_seconds=0.01,
    )
    personality = [event for event in events if event.side == "personality"]

    assert len(personality) == 2
    assert {event.body for event in personality} == {
        CelestialBody.MERCURY,
        CelestialBody.VENUS,
    }
    assert len({event.at_utc for event in personality}) == 1
    assert (personality[0].at_utc - start).total_seconds() == pytest.approx(
        30.0025,
        abs=0.002,
    )


def test_boundary_policy_version_is_frozen_for_future_cache_manifests() -> None:
    assert BOUNDARY_POLICY_VERSION == "exact-gate-line-boundaries-v2"


def test_production_builder_freezes_grouping_to_exact_root_tolerance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_build(*_args: object, **kwargs: object) -> tuple[()]:
        captured.update(kwargs)
        return ()

    monkeypatch.setattr(boundary_module, "build_chart_state_intervals", fake_build)
    start = datetime(2020, 1, 1, tzinfo=UTC)

    result = build_production_chart_state_intervals(
        object(),  # type: ignore[arg-type]
        start,
        start + _seconds(60),
        root_tolerance_seconds=0.025,
    )

    assert result == ()
    assert captured["root_tolerance_seconds"] == 0.025
    assert captured["event_group_tolerance_seconds"] == 0.025
    assert captured["require_swieph_provenance"] is True


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


def test_stable_intervals_use_half_open_boundary_ownership() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    provider = BoundaryProvider(start, linear=True)
    end = start + _seconds(60)
    events = enumerate_chart_boundaries(
        provider,
        start,
        end,
        bodies=(CelestialBody.MERCURY,),
        resolution=BoundaryResolution.GATE,
        root_tolerance_seconds=0.01,
    )
    personality = tuple(event for event in events if event.side == "personality")
    intervals = build_stable_intervals(
        start,
        end,
        personality,
        lambda at: longitude_to_gate_line(
            provider.position(CelestialBody.MERCURY, at).longitude
        ).gate,
    )

    assert len(intervals) == 2
    assert intervals[0].features == 60
    assert intervals[1].features == 41
    assert intervals[0].end_utc == intervals[1].start_utc
    assert longitude_to_gate_line(
        provider.position(CelestialBody.MERCURY, intervals[1].start_utc).longitude
    ).gate == 41
