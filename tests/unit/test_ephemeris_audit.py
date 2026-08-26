"""Tests for provider-to-reference ephemeris differential audits."""

from datetime import UTC, datetime

import pytest

from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisMetadata,
    NodeConvention,
)
from hdmatch.chart.ephemeris_audit import (
    AuditSample,
    compare_providers,
    equal_bin_assignment_changed,
    signed_circular_difference_deg,
    summarize_audit,
)


class _OffsetProvider:
    def __init__(self, offset_deg: float) -> None:
        self.offset_deg = offset_deg

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

    def position(self, body: CelestialBody, _at_utc: datetime) -> EclipticPosition:
        base = 359.999 if body is CelestialBody.SUN else 120.0
        return EclipticPosition((base + self.offset_deg) % 360.0, 1.0)

    def max_abs_speed_degrees_per_day(self, _body: CelestialBody) -> float:
        return 20.0

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9


def test_signed_circular_difference_handles_wraparound() -> None:
    assert signed_circular_difference_deg(0.001, 359.999) == pytest.approx(0.002)
    assert signed_circular_difference_deg(359.999, 0.001) == pytest.approx(-0.002)


def test_compare_and_summarize_are_purely_numerical() -> None:
    timestamp = datetime(2026, 8, 26, tzinfo=UTC)
    samples = compare_providers(
        _OffsetProvider(0.001),
        _OffsetProvider(0.0),
        bodies=(CelestialBody.SUN, CelestialBody.MOON),
        timestamps_utc=(timestamp,),
    )
    summary = summarize_audit(samples, tolerance_arcsec=4.0)
    assert summary.sample_count == 2
    assert summary.max_abs_error_arcsec == pytest.approx(3.6)
    assert summary.all_within_tolerance


def test_boundary_audit_detects_small_error_that_changes_symbol() -> None:
    sample = AuditSample(
        body=CelestialBody.SUN,
        at_utc=datetime(2026, 8, 26, tzinfo=UTC),
        candidate_longitude_deg=0.001,
        reference_longitude_deg=359.999,
        signed_error_arcsec=7.2,
        abs_error_arcsec=7.2,
    )
    assert equal_bin_assignment_changed(sample, bins=12)
    assert not equal_bin_assignment_changed(sample, bins=1)
