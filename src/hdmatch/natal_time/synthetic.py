"""Conspicuously synthetic ephemeris provider for foundation audits only."""

from __future__ import annotations

from datetime import UTC, datetime

from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisMetadata,
    NodeConvention,
)


class SyntheticAnalyticEphemerisProvider:
    """Moving-Sun analytic provider with no claim to astronomical validity."""

    def __init__(self, epoch: datetime = datetime(2020, 1, 1, tzinfo=UTC)) -> None:
        self.epoch = epoch
        self._metadata = EphemerisMetadata(
            provider="synthetic_analytic_natal_time_audit",
            library_version="1",
            files=(),
            calculation_flags=("synthetic_only",),
            coordinate_frame="synthetic_test",
            node_convention=NodeConvention.TRUE,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        days = (at_utc - self.epoch).total_seconds() / 86400.0
        if body is CelestialBody.SUN:
            return EclipticPosition((100.0 + days) % 360.0, 1.0)
        if body is CelestialBody.EARTH:
            return EclipticPosition((280.0 + days) % 360.0, 1.0)
        base = 15.0 + list(CelestialBody).index(body) * 21.0
        return EclipticPosition(base % 360.0, 0.0)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        if body in (CelestialBody.SUN, CelestialBody.EARTH):
            return 1.1
        return 0.01

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9
