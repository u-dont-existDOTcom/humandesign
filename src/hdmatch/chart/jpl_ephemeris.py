"""Fail-closed JPL DE-file reference provider for numerical ephemeris audits.

This provider intentionally does not define a new astrological convention. It asks
Swiss Ephemeris to read a specific local JPL DE file and verifies that every
physical-body calculation actually returns the JPL flag. It is therefore useful
for checking the numerical Swiss-file ephemeris against independent JPL data while
keeping coordinate-system ablations separate.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from types import ModuleType
from typing import Final

from .ephemeris import (
    CelestialBody,
    EphemerisConfigurationError,
    EphemerisFallbackError,
    EphemerisFile,
    EphemerisMetadata,
    EclipticPosition,
    NodeConvention,
    _SWISS_LOCK,
)

_JPL_MAX_SPEEDS: Final[dict[CelestialBody, float]] = {
    CelestialBody.SUN: 1.1,
    CelestialBody.EARTH: 1.1,
    CelestialBody.MOON: 16.0,
    CelestialBody.MERCURY: 2.5,
    CelestialBody.VENUS: 1.5,
    CelestialBody.MARS: 1.0,
    CelestialBody.JUPITER: 0.3,
    CelestialBody.SATURN: 0.2,
    CelestialBody.URANUS: 0.1,
    CelestialBody.NEPTUNE: 0.08,
    CelestialBody.PLUTO: 0.06,
}
_MIN_SOLAR_SPEED: Final[float] = 0.9


@dataclass(frozen=True, slots=True)
class JplFileIdentity:
    """Frozen identity of the local DE file used by a differential audit."""

    filename: str
    sha256: str
    size_bytes: int


class JplEphemerisProvider:
    """Geocentric tropical reference positions from one pinned local JPL DE file."""

    def __init__(
        self,
        jpl_file: str | Path,
        *,
        _swe_module: ModuleType | None = None,
    ) -> None:
        path = Path(jpl_file).expanduser().resolve(strict=False)
        if not path.is_file():
            raise EphemerisConfigurationError(f"declared JPL ephemeris file is missing: {path}")

        if _swe_module is None:
            try:
                _swe_module = importlib.import_module("swisseph")
            except ModuleNotFoundError as exc:
                raise EphemerisConfigurationError(
                    "pyswisseph is required; install hdmatch[ephemeris]"
                ) from exc

        self._swe = _swe_module
        self._path = path
        identity = JplFileIdentity(
            filename=path.name,
            sha256=_sha256_file(path),
            size_bytes=path.stat().st_size,
        )
        self._identity = identity
        self._metadata = EphemerisMetadata(
            provider="jpl_de_file_via_swisseph",
            library_version=str(getattr(self._swe, "version", "unknown")),
            files=(
                EphemerisFile(
                    path=str(path),
                    sha256=identity.sha256,
                    size_bytes=identity.size_bytes,
                ),
            ),
            calculation_flags=("SEFLG_JPLEPH", "SEFLG_SPEED", "geocentric", "tropical"),
            coordinate_frame="geocentric_apparent_tropical_ecliptic_of_date",
            node_convention=NodeConvention.TRUE,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    @property
    def file_identity(self) -> JplFileIdentity:
        return self._identity

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        try:
            return _JPL_MAX_SPEEDS[body]
        except KeyError as exc:
            raise ValueError(
                f"JPL numerical audit does not support derived node body {body.value}"
            ) from exc

    def min_solar_speed_degrees_per_day(self) -> float:
        return _MIN_SOLAR_SPEED

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        at_utc = _require_utc(at_utc)
        if body is CelestialBody.EARTH:
            sun = self.position(CelestialBody.SUN, at_utc)
            return EclipticPosition(
                (sun.longitude + 180.0) % 360.0,
                sun.speed_degrees_per_day,
            )
        if body in {CelestialBody.NORTH_NODE, CelestialBody.SOUTH_NODE}:
            raise ValueError(
                "JPL numerical audit excludes lunar nodes because they are derived conventions"
            )

        planet_id = self._planet_id(body)
        flags = int(self._swe.FLG_JPLEPH) | int(self._swe.FLG_SPEED)
        julian_day = _julian_day_ut(self._swe, at_utc)

        with _SWISS_LOCK:
            self._swe.set_ephe_path(str(self._path.parent))
            self._swe.set_jpl_file(self._path.name)
            values, returned_flags = self._swe.calc_ut(julian_day, planet_id, flags)

        mask = (
            int(self._swe.FLG_JPLEPH)
            | int(self._swe.FLG_SWIEPH)
            | int(self._swe.FLG_MOSEPH)
        )
        used = returned_flags & mask
        if used != int(self._swe.FLG_JPLEPH):
            raise EphemerisFallbackError(
                "JPL reference calculation did not use the declared DE file for "
                f"{body.value} at {at_utc.isoformat()}; returned flags={returned_flags}"
            )
        return EclipticPosition(float(values[0]) % 360.0, float(values[3]))

    def _planet_id(self, body: CelestialBody) -> int:
        names = {
            CelestialBody.SUN: "SUN",
            CelestialBody.MOON: "MOON",
            CelestialBody.MERCURY: "MERCURY",
            CelestialBody.VENUS: "VENUS",
            CelestialBody.MARS: "MARS",
            CelestialBody.JUPITER: "JUPITER",
            CelestialBody.SATURN: "SATURN",
            CelestialBody.URANUS: "URANUS",
            CelestialBody.NEPTUNE: "NEPTUNE",
            CelestialBody.PLUTO: "PLUTO",
        }
        try:
            return int(getattr(self._swe, names[body]))
        except KeyError as exc:
            raise ValueError(f"unsupported JPL body: {body}") from exc


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("ephemeris timestamps must be timezone-aware")
    return value.astimezone(UTC)


def _julian_day_ut(swe: ModuleType, at_utc: datetime) -> float:
    hour = (
        at_utc.hour
        + at_utc.minute / 60.0
        + at_utc.second / 3600.0
        + at_utc.microsecond / 3_600_000_000.0
    )
    return float(swe.julday(at_utc.year, at_utc.month, at_utc.day, hour, swe.GREG_CAL))
