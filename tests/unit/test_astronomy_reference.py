"""Tests for explicit astronomy state and coordinate-projection separation."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.chart.astronomy_reference import (
    PROJECTION_SPECS,
    AstronomyProvenance,
    AstronomyReferenceError,
    AstronomyState,
    ObserverOrigin,
    ProjectionKind,
    ReferenceFrame,
    SwissAstronomyReferenceProvider,
    UnsupportedAstronomyProjection,
    astrohd_gate,
    iau_constellation,
    projection_spec,
    sidereal_longitude,
)


def _provenance() -> AstronomyProvenance:
    return AstronomyProvenance(
        provider="swisseph",
        provider_version="test",
        package="pyswisseph-test",
        input_time_scale="UT",
        origin=ObserverOrigin.GEOCENTRIC,
        native_frame=ReferenceFrame.ECLIPTIC_OF_DATE,
        calculation_flags=("FLG_SWIEPH", "FLG_SPEED"),
    )


def _state() -> AstronomyState:
    return AstronomyState(
        observed_at_utc=datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
        julian_day_ut=2446094.934027778,
        body="Sun",
        provenance=_provenance(),
        ecliptic_longitude_deg=309.25,
        ecliptic_latitude_deg=0.0,
        distance_au=0.985,
        right_ascension_deg=311.0,
        declination_deg=-17.5,
        cartesian_position_au=(0.1, -0.9, -0.3),
        cartesian_velocity_au_per_day=(0.01, 0.01, 0.0),
    )


def test_projection_registry_keeps_coordinate_hypotheses_distinct() -> None:
    assert {spec.kind for spec in PROJECTION_SPECS} == set(ProjectionKind)
    assert projection_spec(ProjectionKind.TROPICAL_EQUINOX_OF_DATE).status == "implemented"
    assert projection_spec(ProjectionKind.ASTROHD_GATE).status == "implemented"
    assert projection_spec(ProjectionKind.IAU_CONSTELLATION).status == "registered_fail_closed"


def test_sidereal_projection_requires_explicit_ayanamsa() -> None:
    state = _state()
    assert sidereal_longitude(state, ayanamsa_name="example", ayanamsa_deg=24.0) == 285.25
    with pytest.raises(ValueError, match="ayanamsa_name"):
        sidereal_longitude(state, ayanamsa_name="", ayanamsa_deg=24.0)


def test_astrohd_gate_projection_uses_frozen_mandala_mapper() -> None:
    position = astrohd_gate(_state())
    assert position.gate == 19
    assert position.line == 2
    assert position.longitude == 309.25


def test_iau_constellation_fails_closed_without_boundary_dataset() -> None:
    with pytest.raises(UnsupportedAstronomyProjection, match="boundary dataset"):
        iau_constellation(_state())


def test_reference_state_requires_timezone_aware_utc_input() -> None:
    payload = _state().model_dump()
    payload["observed_at_utc"] = datetime(1985, 1, 29, 10, 25)
    with pytest.raises(ValidationError, match="timezone-aware"):
        AstronomyState.model_validate(payload)


class _FakeSwissEngine:
    FLG_SWIEPH = 2
    FLG_SPEED = 256
    FLG_EQUATORIAL = 2048
    FLG_XYZ = 4096

    def calc_ut(
        self,
        _jd_ut: float,
        _body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        if flags & self.FLG_XYZ:
            return ((1.0, 2.0, 3.0, 0.1, 0.2, 0.3), flags)
        if flags & self.FLG_EQUATORIAL:
            return ((361.0, -20.0, 0.9, 0.0, 0.0, 0.0), flags)
        return ((-1.0, 4.0, 0.9, 0.5, 0.1, 0.0), flags)


class _FallbackSwissEngine(_FakeSwissEngine):
    def calc_ut(
        self,
        jd_ut: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        values, _ = super().calc_ut(jd_ut, body, flags)
        return values, flags & ~self.FLG_SWIEPH


def test_swiss_reference_provider_preserves_richer_state() -> None:
    provider = SwissAstronomyReferenceProvider(
        engine=_FakeSwissEngine(),
        provenance=_provenance(),
    )
    state = provider.state(
        jd_ut=2446094.934,
        observed_at_utc=datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
        body_name="Sun",
        body_id=0,
    )
    assert state.ecliptic_longitude_deg == 359.0
    assert state.right_ascension_deg == 1.0
    assert state.cartesian_position_au == (1.0, 2.0, 3.0)
    assert state.cartesian_velocity_au_per_day == (0.1, 0.2, 0.3)


def test_swiss_reference_provider_rejects_silent_non_swiss_fallback() -> None:
    provider = SwissAstronomyReferenceProvider(
        engine=_FallbackSwissEngine(),
        provenance=_provenance(),
    )
    with pytest.raises(AstronomyReferenceError, match="silent fallback"):
        provider.state(
            jd_ut=2446094.934,
            observed_at_utc=datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
            body_name="Sun",
            body_id=0,
        )
