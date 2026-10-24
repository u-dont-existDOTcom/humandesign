"""Auditable, research-only primary-direction geometry.

Sources: previously independently checked Cartesian Regiomontanus, proportional
semi-arc phase, and signed Placidean under-pole equations in
docs/astrology-research-map/gansten-method-parity-20261023/ and the later
Morinus 9,600-case cross-quadrant parity audit. This module deliberately
implements only BODY CONJUNCTIONS and directions to Ascendant/Midheaven.
It does not implement direction of rays, terms, antiscia, fixed stars,
secondary motion, or any historical judgment rules.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

_EPS = 1e-10


class GeometryUnavailable(ValueError):
    """A contact does not exist in this method/domain or is singular."""


class GeometryMethod(StrEnum):
    PROPORTIONAL_SEMI_ARC = "proportional_semi_arc"
    PLACIDEAN_UNDER_POLE = "placidean_under_pole"
    REGIOMONTANIAN_POSITION_CIRCLE = "regiomontanian_position_circle"


@dataclass(frozen=True, slots=True)
class EquatorialPoint:
    ra_deg: float
    dec_deg: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(v) for v in (self.ra_deg, self.dec_deg)):
            raise ValueError("RA and declination must be finite")
        if not 0 <= self.ra_deg < 360:
            raise ValueError("RA must be normalized in [0,360)")
        if not -90 <= self.dec_deg <= 90:
            raise ValueError("declination must be in [-90,90]")


def normalize(angle: float) -> float:
    return angle % 360.0


def _sin(v: float) -> float:
    return math.sin(math.radians(v))


def _cos(v: float) -> float:
    return math.cos(math.radians(v))


def _tan(v: float) -> float:
    return math.tan(math.radians(v))


def _asin(v: float) -> float:
    if not math.isfinite(v) or abs(v) > 1 + _EPS:
        raise GeometryUnavailable("ascensional difference or pole intersection undefined")
    return math.degrees(math.asin(max(-1.0, min(1.0, v))))


def ascensional_difference(latitude: float, declination: float) -> float:
    if abs(latitude) >= 90 or abs(declination) >= 90:
        raise GeometryUnavailable("geographic/celestial pole is a singular domain")
    return _asin(_tan(latitude) * _tan(declination))


def _semi_arcs(latitude: float, declination: float) -> tuple[float, float]:
    ad = ascensional_difference(latitude, declination)
    return 90.0 + ad, 90.0 - ad


def _phase(h: float, day: float, night: float) -> float:
    """Measured in normalized diurnal quadrants; MC=0, DC=90, IC=180, AC=270."""
    h = normalize(h)
    if h <= day:
        return 90 * h / day
    if h <= 180:
        return 90 + 90 * (h - day) / night
    if h <= 360 - day:
        return 180 + 90 * (h - 180) / night
    return 270 + 90 * (h - 360 + day) / day


def _hour_angle(position: float, day: float, night: float) -> float:
    p = normalize(position)
    if p <= 90:
        return p * day / 90
    if p <= 180:
        return day + (p - 90) * night / 90
    if p <= 270:
        return 180 + (p - 180) * night / 90
    return 360 - day + (p - 270) * day / 90


def proportional_semi_arc(
    latitude: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint
) -> float:
    """Rotation needed to bring the moving body's phase to the fixed body's phase."""
    fd, fn = _semi_arcs(latitude, fixed.dec_deg)
    md, mn = _semi_arcs(latitude, moving.dec_deg)
    target = _phase(fixed.ra_deg - ramc, fd, fn)
    moving_hour_angle = _hour_angle(target, md, mn)
    crossing_ra = normalize(ramc + moving_hour_angle)
    return normalize(moving.ra_deg - crossing_ra)


def placidean_under_pole(
    latitude: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint
) -> float:
    """Signed AO/DO construction, all four sky quadrants and both hemispheres.

    The pole is determined by the fixed point's position within its day or
    night semi-arc. The source algorithm in Morinus SE 8.0.0 uses fabs(AODO)
    and incorrectly flips valid negative physical AO/DO coordinates. That
    defect is not reproduced here. This is a research implementation of one
    body-conjunction profile, NOT a universal Placidus direction engine.
    """
    dsa, nsa = _semi_arcs(latitude, fixed.dec_deg)
    h = normalize(fixed.ra_deg - ramc)
    east = h < 180.0
    above = h < dsa or h > 360 - dsa
    md = min(h, 360 - h) if above else abs(h - 180.0)
    sa = dsa if above else nsa
    if not 0 <= md <= sa:
        raise GeometryUnavailable("significator is outside the expected semi-arc")
    ad = dsa - 90
    ad_pole = md / sa * ad
    if abs(fixed.dec_deg) < 1e-9:
        # Continuously extend sin(ad_pole)/tan(delta) as delta approaches 0.
        pole = math.degrees(math.atan(md / sa * _tan(latitude)))
    else:
        pole = math.degrees(math.atan(_sin(ad_pole) / _tan(fixed.dec_deg)))
    difference = _asin(_tan(moving.dec_deg) * _tan(pole))
    fixed_coord = fixed.ra_deg - ad_pole if east else fixed.ra_deg + ad_pole
    moving_coord = moving.ra_deg - difference if east else moving.ra_deg + difference
    return normalize(moving_coord - fixed_coord)


def _vector(p: EquatorialPoint) -> tuple[float, float, float]:
    return (_cos(p.dec_deg) * _cos(p.ra_deg), _cos(p.dec_deg) * _sin(p.ra_deg), _sin(p.dec_deg))


def _cross(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def regiomontanian_position_circle(
    latitude: float, ramc: float, fixed: EquatorialPoint, moving: EquatorialPoint
) -> float:
    """Cartesian intersection with the fixed-sided Regiomontanian position circle."""
    if abs(latitude) >= 90 or abs(fixed.dec_deg) >= 90 or abs(moving.dec_deg) >= 90:
        raise GeometryUnavailable("polar coordinates require a separate construction")
    north = (-_sin(latitude) * _cos(ramc), -_sin(latitude) * _sin(ramc), _cos(latitude))
    sigvec = _vector(fixed)
    normal = _cross(north, sigvec)
    if math.sqrt(_dot(normal, normal)) < _EPS:
        raise GeometryUnavailable("fixed point equals the horizon pole")
    projection = _dot(north, sigvec)
    same_side = (
        sigvec[0] - projection * north[0],
        sigvec[1] - projection * north[1],
        sigvec[2] - projection * north[2],
    )
    hnorm = math.hypot(normal[0], normal[1])
    if hnorm < _EPS:
        raise GeometryUnavailable("position-circle intersection is underdetermined")
    cos_arg = -normal[2] * _tan(moving.dec_deg) / hnorm
    if abs(cos_arg) > 1 + _EPS:
        raise GeometryUnavailable("moving declination cannot meet the position circle")
    v = math.acos(max(-1.0, min(1.0, cos_arg)))
    gamma = math.atan2(normal[1], normal[0])
    candidates: list[float] = []
    for ra_radians in (gamma + v, gamma - v):
        ra = normalize(math.degrees(ra_radians))
        candidate = _vector(EquatorialPoint(ra, moving.dec_deg))
        if _dot(candidate, same_side) > _EPS:
            candidates.append(normalize(moving.ra_deg - ra))
    if not candidates:
        raise GeometryUnavailable("no intersection with fixed-sided semicircle")
    return min(candidates)


def direction_arc(
    method: GeometryMethod,
    latitude: float,
    ramc: float,
    fixed: EquatorialPoint,
    moving: EquatorialPoint,
) -> float:
    """Return full-circle positive rotation; reverse sense decided by caller."""
    if not math.isfinite(latitude) or abs(latitude) >= 90:
        raise ValueError("finite nonpolar geographic latitude required")
    if not math.isfinite(ramc):
        raise ValueError("RAMC must be finite")
    ramc = normalize(ramc)
    method = GeometryMethod(method)
    if method is GeometryMethod.PROPORTIONAL_SEMI_ARC:
        return proportional_semi_arc(latitude, ramc, fixed, moving)
    if method is GeometryMethod.PLACIDEAN_UNDER_POLE:
        return placidean_under_pole(latitude, ramc, fixed, moving)
    if method is GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE:
        return regiomontanian_position_circle(latitude, ramc, fixed, moving)
    raise AssertionError("unreachable geometry selection")


def direction_sense(raw_arc: float) -> tuple[str, float]:
    """Morinus-style shortest signed arc convention; not a universal traditional rule."""
    if not math.isfinite(raw_arc):
        raise ValueError("arc must be finite")
    arc = normalize(raw_arc)
    if arc <= 180:
        return "direct", arc
    return "converse", 360 - arc
