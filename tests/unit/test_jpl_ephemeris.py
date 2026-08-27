"""Tests for the pinned JPL DE-file numerical reference provider."""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.chart.ephemeris import (
    CelestialBody,
    EphemerisConfigurationError,
    EphemerisFallbackError,
)
from hdmatch.chart.jpl_ephemeris import JplEphemerisProvider


class _FakeJplEngine:
    version = "fake"
    FLG_JPLEPH = 1
    FLG_SWIEPH = 2
    FLG_MOSEPH = 4
    FLG_SPEED = 256
    GREG_CAL = 1
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9

    def __init__(self) -> None:
        self.ephe_path: str | None = None
        self.jpl_file: str | None = None

    def set_ephe_path(self, path: str) -> None:
        self.ephe_path = path

    def set_jpl_file(self, filename: str) -> None:
        self.jpl_file = filename

    def julday(
        self,
        _year: int,
        _month: int,
        _day: int,
        _hour: float,
        _calendar: int,
    ) -> float:
        return 2446094.934

    def calc_ut(
        self,
        _jd_ut: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        return ((309.0 + body, 0.0, 1.0, 0.9, 0.0, 0.0), flags)


class _FallbackEngine(_FakeJplEngine):
    def calc_ut(
        self,
        jd_ut: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        values, _ = super().calc_ut(jd_ut, body, flags)
        return values, self.FLG_SWIEPH | self.FLG_SPEED


def _jpl_file(tmp_path: Path) -> Path:
    path = tmp_path / "de440.eph"
    path.write_bytes(b"frozen-test-jpl-file")
    return path


def test_jpl_provider_requires_declared_local_file(tmp_path: Path) -> None:
    with pytest.raises(EphemerisConfigurationError, match="missing"):
        JplEphemerisProvider(tmp_path / "missing.eph", _swe_module=_FakeJplEngine())


def test_jpl_provider_hashes_file_and_verifies_jpl_flag(tmp_path: Path) -> None:
    path = _jpl_file(tmp_path)
    engine = _FakeJplEngine()
    provider = JplEphemerisProvider(path, _swe_module=engine)
    position = provider.position(
        CelestialBody.SUN,
        datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
    )
    assert position.longitude == 309.0
    assert position.speed_degrees_per_day == 0.9
    assert provider.file_identity.filename == "de440.eph"
    assert len(provider.file_identity.sha256) == 64
    assert engine.ephe_path == str(path.parent)
    assert engine.jpl_file == path.name


def test_jpl_provider_rejects_swiss_fallback(tmp_path: Path) -> None:
    provider = JplEphemerisProvider(
        _jpl_file(tmp_path),
        _swe_module=_FallbackEngine(),
    )
    with pytest.raises(EphemerisFallbackError, match="did not use"):
        provider.position(
            CelestialBody.MARS,
            datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
        )


def test_jpl_reference_excludes_derived_nodes(tmp_path: Path) -> None:
    provider = JplEphemerisProvider(
        _jpl_file(tmp_path),
        _swe_module=_FakeJplEngine(),
    )
    with pytest.raises(ValueError, match="derived conventions"):
        provider.position(
            CelestialBody.NORTH_NODE,
            datetime(1985, 1, 29, 10, 25, tzinfo=UTC),
        )
