"""Deterministic Western relationship features for frozen AstroRRF models.

Planetary longitudes come from the same strict Swiss-backed ``ChartComputation`` used
by Human Design. Houses/angles are calculated only when exact coordinates are supplied.
No rectification, noon substitution, or outcome-guided feature selection occurs here.
"""

from __future__ import annotations

import importlib
import math
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any

from hdmatch.chart.calculator import ChartComputation
from hdmatch.chart.ephemeris import CelestialBody

MAJOR_ASPECT_ANGLES: dict[str, float] = {
    "conjunction": 0.0,
    "sextile": 60.0,
    "square": 90.0,
    "trine": 120.0,
    "opposition": 180.0,
}
DEFAULT_ASPECT_ORB = 3.0
WESTERN_BODIES: tuple[CelestialBody, ...] = (
    CelestialBody.SUN,
    CelestialBody.MOON,
    CelestialBody.MERCURY,
    CelestialBody.VENUS,
    CelestialBody.MARS,
    CelestialBody.JUPITER,
    CelestialBody.SATURN,
    CelestialBody.URANUS,
    CelestialBody.NEPTUNE,
    CelestialBody.PLUTO,
    CelestialBody.NORTH_NODE,
)


class AspectPolarity(StrEnum):
    HARD = "hard"
    SOFT = "soft"


@dataclass(frozen=True, slots=True)
class MajorAspect:
    body_a: str
    body_b: str
    aspect: str
    orb_degrees: float

    @property
    def polarity(self) -> AspectPolarity:
        if self.aspect in {"conjunction", "square", "opposition"}:
            return AspectPolarity.HARD
        return AspectPolarity.SOFT


@dataclass(frozen=True, slots=True)
class WesternNatalSnapshot:
    birth_utc: datetime
    longitudes: dict[str, float]
    latitude: float | None
    longitude: float | None
    ascendant: float | None
    midheaven: float | None
    house_cusps: tuple[float, ...] | None


@dataclass(frozen=True, slots=True)
class WesternRelationshipFeatures:
    natal_a: WesternNatalSnapshot
    natal_b: WesternNatalSnapshot
    synastry_aspects: tuple[MajorAspect, ...]
    composite_longitudes: dict[str, float]
    composite_aspects: tuple[MajorAspect, ...]
    b_planets_in_a_houses: dict[str, int]
    a_planets_in_b_houses: dict[str, int]


def natal_snapshot(
    chart: ChartComputation,
    *,
    latitude: float | None,
    longitude: float | None,
) -> WesternNatalSnapshot:
    longitudes = {
        activation.body.value: activation.longitude
        for activation in chart.activations
        if activation.side == "personality" and activation.body in WESTERN_BODIES
    }
    missing = {body.value for body in WESTERN_BODIES} - set(longitudes)
    if missing:
        raise ValueError(f"chart is missing Western bodies: {sorted(missing)}")
    ascendant: float | None = None
    midheaven: float | None = None
    cusps: tuple[float, ...] | None = None
    if latitude is not None or longitude is not None:
        if latitude is None or longitude is None:
            raise ValueError("latitude and longitude must be supplied together")
        cusps, ascendant, midheaven = placidus_houses(
            chart.personality_utc,
            latitude=latitude,
            longitude=longitude,
        )
    return WesternNatalSnapshot(
        birth_utc=chart.personality_utc,
        longitudes=longitudes,
        latitude=latitude,
        longitude=longitude,
        ascendant=ascendant,
        midheaven=midheaven,
        house_cusps=cusps,
    )


def relationship_features(
    natal_a: WesternNatalSnapshot,
    natal_b: WesternNatalSnapshot,
    *,
    max_orb: float = DEFAULT_ASPECT_ORB,
) -> WesternRelationshipFeatures:
    synastry = cross_aspects(natal_a.longitudes, natal_b.longitudes, max_orb=max_orb)
    composite = {
        body: circular_midpoint(natal_a.longitudes[body], natal_b.longitudes[body])
        for body in sorted(set(natal_a.longitudes) & set(natal_b.longitudes))
    }
    composite_aspect_values = within_chart_aspects(composite, max_orb=max_orb)
    b_in_a = _house_placements(natal_b.longitudes, natal_a.house_cusps)
    a_in_b = _house_placements(natal_a.longitudes, natal_b.house_cusps)
    return WesternRelationshipFeatures(
        natal_a=natal_a,
        natal_b=natal_b,
        synastry_aspects=synastry,
        composite_longitudes=composite,
        composite_aspects=composite_aspect_values,
        b_planets_in_a_houses=b_in_a,
        a_planets_in_b_houses=a_in_b,
    )


def placidus_houses(
    birth_utc: datetime,
    *,
    latitude: float,
    longitude: float,
) -> tuple[tuple[float, ...], float, float]:
    if birth_utc.tzinfo is None or birth_utc.utcoffset() is None:
        raise ValueError("birth_utc must be timezone-aware")
    swe: Any = importlib.import_module("swisseph")
    utc = birth_utc.astimezone(__import__("datetime").UTC)
    hour = utc.hour + utc.minute / 60.0 + utc.second / 3600.0 + utc.microsecond / 3.6e9
    jd = swe.julday(utc.year, utc.month, utc.day, hour, swe.GREG_CAL)
    raw_cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b"P", 0)
    cusps = tuple(float(value) % 360.0 for value in raw_cusps[:12])
    if len(cusps) != 12:
        raise RuntimeError("Swiss houses_ex did not return 12 Placidus cusps")
    return cusps, float(ascmc[0]) % 360.0, float(ascmc[1]) % 360.0


def cross_aspects(
    a: dict[str, float],
    b: dict[str, float],
    *,
    max_orb: float,
) -> tuple[MajorAspect, ...]:
    aspects: list[MajorAspect] = []
    for body_a, longitude_a in sorted(a.items()):
        for body_b, longitude_b in sorted(b.items()):
            match = classify_major_aspect(longitude_a, longitude_b, max_orb=max_orb)
            if match is not None:
                aspect, orb = match
                aspects.append(MajorAspect(body_a, body_b, aspect, orb))
    return tuple(aspects)


def within_chart_aspects(
    longitudes: dict[str, float],
    *,
    max_orb: float,
) -> tuple[MajorAspect, ...]:
    bodies = sorted(longitudes)
    aspects: list[MajorAspect] = []
    for index, body_a in enumerate(bodies):
        for body_b in bodies[index + 1 :]:
            match = classify_major_aspect(
                longitudes[body_a], longitudes[body_b], max_orb=max_orb
            )
            if match is not None:
                aspect, orb = match
                aspects.append(MajorAspect(body_a, body_b, aspect, orb))
    return tuple(aspects)


def classify_major_aspect(
    longitude_a: float,
    longitude_b: float,
    *,
    max_orb: float = DEFAULT_ASPECT_ORB,
) -> tuple[str, float] | None:
    separation = angular_separation(longitude_a, longitude_b)
    candidates = [
        (name, abs(separation - angle)) for name, angle in MAJOR_ASPECT_ANGLES.items()
    ]
    name, orb = min(candidates, key=lambda item: item[1])
    if orb > max_orb:
        return None
    return name, orb


def angular_separation(longitude_a: float, longitude_b: float) -> float:
    raw = abs((longitude_a - longitude_b) % 360.0)
    return min(raw, 360.0 - raw)


def circular_midpoint(longitude_a: float, longitude_b: float) -> float:
    signed_delta = ((longitude_b - longitude_a + 180.0) % 360.0) - 180.0
    return (longitude_a + signed_delta / 2.0) % 360.0


def house_for_longitude(longitude: float, cusps: tuple[float, ...]) -> int:
    if len(cusps) != 12:
        raise ValueError("house cusps must contain 12 values")
    value = longitude % 360.0
    for index, start in enumerate(cusps):
        end = cusps[(index + 1) % 12]
        if _in_circular_interval(value, start, end):
            return index + 1
    raise RuntimeError("longitude could not be assigned to a house")


def _house_placements(
    planets: dict[str, float],
    cusps: tuple[float, ...] | None,
) -> dict[str, int]:
    if cusps is None:
        return {}
    return {body: house_for_longitude(longitude, cusps) for body, longitude in planets.items()}


def _in_circular_interval(value: float, start: float, end: float) -> bool:
    value %= 360.0
    start %= 360.0
    end %= 360.0
    if math.isclose(start, end, abs_tol=1e-12):
        return True
    if start < end:
        return start <= value < end
    return value >= start or value < end
