"""Swiss-file-only birth-coordinate snapshot for primary-direction research.

Reuses the strict SwissEphemerisProvider (hashes .se1 files, verifies returned
SWIEPH flags/current source files) and SwissAstronomyReferenceProvider (RA,
declination, ecliptic state). Neither silently accepts Moshier/JPL fallback.

Only apparent geocentric positions of the seven classical bodies are enabled;
true equator/equinox of date, geographic longitude east-positive. Angular
house computation is mathematical and source-separated.
"""

from __future__ import annotations

import importlib
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hdmatch.chart.astronomy_reference import (
    AstronomyProvenance,
    EphemerisFileProvenance,
    ObserverOrigin,
    ReferenceFrame,
    SwissAstronomyReferenceProvider,
)
from hdmatch.chart.ephemeris import (
    _SWISS_LOCK,
    CelestialBody,
    SwissEphemerisProvider,
)

from .geometry import EquatorialPoint, normalize

CLASSICAL_BODIES: tuple[CelestialBody, ...] = (
    CelestialBody.SUN,
    CelestialBody.MOON,
    CelestialBody.MERCURY,
    CelestialBody.VENUS,
    CelestialBody.MARS,
    CelestialBody.JUPITER,
    CelestialBody.SATURN,
)


@dataclass(frozen=True, slots=True)
class DirectionBirthSnapshot:
    birth_utc: datetime
    latitude_deg: float
    longitude_east_deg: float
    ramc_deg: float
    ascendant_ecliptic_lon_deg: float
    midheaven_ecliptic_lon_deg: float
    points: tuple[tuple[str, EquatorialPoint], ...]
    ephemeris_version: str
    ephemeris_mode: str
    ephemeris_file_sha256: tuple[tuple[str, str], ...]
    # Newly retained for ecliptic zodiacal aspect-point geometry; older
    # conjunction-only snapshots may omit them, and ray generation fails closed.
    ecliptic_positions: tuple[tuple[str, float, float], ...] = ()
    true_obliquity_deg: float | None = None
    coordinate_convention: str = (
        "apparent geocentric true-equator/equinox-of-date RA/Dec, "
        "east-positive geographic longitude, tropical zodiac"
    )

    def lookup(self) -> dict[str, EquatorialPoint]:
        return dict(self.points)

    def ecliptic_lookup(self) -> dict[str, tuple[float, float]]:
        return {name: (lon, lat) for name, lon, lat in self.ecliptic_positions}

    def provenance(self) -> dict[str, object]:
        return {
            "provider": "Swiss Ephemeris (strict, local .se1)",
            "ephemeris_mode": self.ephemeris_mode,
            "ephemeris_version": self.ephemeris_version,
            "ephemeris_files": dict(self.ephemeris_file_sha256),
            "coordinates": self.coordinate_convention,
        }


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("birth time must have an explicit UTC offset/time zone")
    out = dt.astimezone(UTC)
    if not 1800 <= out.year < 2400:
        # This adapter explicitly pins the 1800–2399 ephemeris pair.
        raise ValueError("v1 uses sepl_18.se1 + semo_18.se1 (1800–2399 only)")
    return out


def _hour(utc: datetime) -> float:
    return utc.hour + utc.minute / 60 + utc.second / 3600 + utc.microsecond / 3_600_000_000


def _validate_location(lat: float, lon: float) -> None:
    if not all(math.isfinite(x) for x in (lat, lon)):
        raise ValueError("latitude and longitude must be finite")
    if not -66 <= lat <= 66:
        raise ValueError("v1 Placidus-Ascendant construction limited to -66..+66 latitude")
    if not -180 <= lon <= 180:
        raise ValueError("longitude must lie in [-180,180], east positive")


def snapshot_from_swiss_files(
    birth_utc: datetime,
    *,
    latitude_deg: float,
    longitude_east_deg: float,
    ephemeris_directory: str | Path,
    _swe_module: Any | None = None,
) -> DirectionBirthSnapshot:
    """Return a hash-provenanced natal sky state; fail on missing/fallback files."""
    utc = _utc(birth_utc)
    _validate_location(latitude_deg, longitude_east_deg)
    root = Path(ephemeris_directory).expanduser().resolve()
    files = (root / "sepl_18.se1", root / "semo_18.se1")
    swe: Any = _swe_module if _swe_module is not None else importlib.import_module("swisseph")
    strict = SwissEphemerisProvider(files, _swe_module=swe)
    provenance = AstronomyProvenance(
        provider="Swiss Ephemeris",
        provider_version=strict.metadata.library_version,
        package="pyswisseph",
        input_time_scale="UT",
        origin=ObserverOrigin.GEOCENTRIC,
        native_frame=ReferenceFrame.ECLIPTIC_OF_DATE,
        calculation_flags=("FLG_SWIEPH", "FLG_SPEED", "FLG_EQUATORIAL", "apparent"),
        source_files=tuple(
            EphemerisFileProvenance(name=Path(f.path).name, sha256=f.sha256)
            for f in strict.metadata.files
        ),
    )
    reference = SwissAstronomyReferenceProvider(engine=swe, provenance=provenance)
    jd = float(swe.julday(utc.year, utc.month, utc.day, _hour(utc), swe.GREG_CAL))
    body_ids = {
        CelestialBody.SUN: int(swe.SUN),
        CelestialBody.MOON: int(swe.MOON),
        CelestialBody.MERCURY: int(swe.MERCURY),
        CelestialBody.VENUS: int(swe.VENUS),
        CelestialBody.MARS: int(swe.MARS),
        CelestialBody.JUPITER: int(swe.JUPITER),
        CelestialBody.SATURN: int(swe.SATURN),
    }
    positions: list[tuple[str, EquatorialPoint]] = []
    ecliptic_positions: list[tuple[str, float, float]] = []
    with _SWISS_LOCK:
        swe.set_ephe_path(str(root))
        for body in CLASSICAL_BODIES:
            # The existing adapter audits actual source files and returned flags.
            strict.position(body, utc)
            state = reference.state(
                jd_ut=jd,
                observed_at_utc=utc,
                body_name=body.value,
                body_id=body_ids[body],
            )
            positions.append(
                (
                    body.value,
                    EquatorialPoint(state.right_ascension_deg, state.declination_deg),
                )
            )
            ecliptic_positions.append(
                (body.value, state.ecliptic_longitude_deg, state.ecliptic_latitude_deg)
            )
        try:
            _cusps, ascmc = swe.houses_ex(
                jd,
                latitude_deg,
                longitude_east_deg,
                b"P",
                0,
            )
        except Exception as exc:
            raise ValueError("unable to calculate natal Placidus angles") from exc
        if len(ascmc) < 3:
            raise ValueError("Swiss houses_ex returned incomplete angle positions")
        asc_ecl = normalize(float(ascmc[0]))
        mc_ecl = normalize(float(ascmc[1]))
        ramc = normalize(float(ascmc[2]))
        if abs((ramc - (swe.sidtime(jd) * 15 + longitude_east_deg) + 180) % 360 - 180) > 1e-4:
            raise ValueError("house ARMC disagrees with independently calculated sidereal time")
        # True obliquity, not mean; matching apparent planetary RA/Dec of date.
        epsilon = float(swe.calc_ut(jd, swe.ECL_NUT, swe.FLG_SWIEPH)[0][0])
        asc_ra, asc_dec, _distance = swe.cotrans(
            (asc_ecl, 0.0, 1.0),
            -epsilon,
        )
        # Reuse spherical coordinates for the actual eastern ecliptic/horizon
        # crossing, not a generic RA=RAMC+90° surrogate.
        positions.append(("asc", EquatorialPoint(normalize(asc_ra), float(asc_dec))))
        # The MC significator is the MERIDIAN, not the ecliptic MC body;
        # declination 0 is an unambiguous representative of its great circle.
        positions.append(("mc", EquatorialPoint(ramc, 0.0)))
    return DirectionBirthSnapshot(
        birth_utc=utc,
        latitude_deg=latitude_deg,
        longitude_east_deg=longitude_east_deg,
        ramc_deg=ramc,
        ascendant_ecliptic_lon_deg=asc_ecl,
        midheaven_ecliptic_lon_deg=mc_ecl,
        points=tuple(positions),
        ephemeris_version=strict.metadata.library_version,
        ephemeris_mode="SWIEPH verified for all seven classical bodies",
        ephemeris_file_sha256=tuple((Path(f.path).name, f.sha256) for f in strict.metadata.files),
        ecliptic_positions=tuple(ecliptic_positions),
        true_obliquity_deg=epsilon,
    )
