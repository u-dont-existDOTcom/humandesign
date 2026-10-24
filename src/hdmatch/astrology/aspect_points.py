"""Two explicitly different geometrical aspect-point providers.

Source grounding: Martin Gansten, Primary Directions (2009), Ch. 5 pp.65–70,
Ch.8 pp.88–92, Appendix I pp.147–154, as summarized in the audited Kindle
research package GANSTEN_PRIMARY_DIRECTIONS_AUDIT.md §§1.3,2.1,3.3.
This is a GEOMETRIC RECONSTRUCTION, not a complete historical rulebook.

Zodiacal rays: λ_promissor ± aspect on the ecliptic; β_ray = 0. Longitude
is not right ascension and the resulting points must be transformed by
the actual obliquity-of-date. Body-latitude latitude aspects by Bianchini,
Morin, and other authors require DIFFERENT separate algorithms, not a switch.

Mundane semi-arc aspect: shift normalized positional phase u_fixed ± ψ
and invert using the moving promissor's own semi-arc. This is the explicit
mathematical phase reconstruction documented in the earlier audit; it is
not an ecliptic aspect and not necessarily the historical aspect as defined
by all named authors or all direction families.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from .geometry import (
    EquatorialPoint,
    GeometryUnavailable,
    _hour_angle,
    _phase,
    _semi_arcs,
    normalize,
)


class RayAspect(StrEnum):
    SEXTILE = "sextile"
    SQUARE = "square"
    TRINE = "trine"
    OPPOSITION = "opposition"


ASPECT_DEGREES: dict[RayAspect, float] = {
    RayAspect.SEXTILE: 60.0,
    RayAspect.SQUARE: 90.0,
    RayAspect.TRINE: 120.0,
    RayAspect.OPPOSITION: 180.0,
}


class RayBranch(StrEnum):
    POSITIVE = "positive_offset"
    NEGATIVE = "negative_offset"


@dataclass(frozen=True, slots=True)
class AspectPoint:
    aspect: RayAspect
    branch: RayBranch
    offset_deg: float
    ecliptic_longitude_deg: float
    ecliptic_latitude_deg: float
    equatorial: EquatorialPoint


def aspect_branches(aspect: RayAspect) -> tuple[RayBranch, ...]:
    """Opposition is unique modulo 360; other aspects have two placements."""
    return (
        (RayBranch.POSITIVE,)
        if RayAspect(aspect) is RayAspect.OPPOSITION
        else (RayBranch.POSITIVE, RayBranch.NEGATIVE)
    )


def ecliptic_to_equatorial(
    longitude_deg: float, latitude_deg: float, obliquity_deg: float
) -> EquatorialPoint:
    """Spherical rotation, preserving longitude quadrant with atan2."""
    if not all(math.isfinite(v) for v in (longitude_deg, latitude_deg, obliquity_deg)):
        raise ValueError("non-finite ecliptic coordinate or obliquity")
    if not -90 <= latitude_deg <= 90 or not 0 < obliquity_deg < 27:
        raise ValueError("latitude or obliquity outside supported astronomical domain")
    lam, beta, eps = map(math.radians, (longitude_deg, latitude_deg, obliquity_deg))
    cb = math.cos(beta)
    x = cb * math.cos(lam)
    y = cb * math.sin(lam) * math.cos(eps) - math.sin(beta) * math.sin(eps)
    z = cb * math.sin(lam) * math.sin(eps) + math.sin(beta) * math.cos(eps)
    ra = normalize(math.degrees(math.atan2(y, x)))
    dec = math.degrees(math.atan2(z, math.hypot(x, y)))
    return EquatorialPoint(ra, dec)


def zodiacal_promissor_ray(
    natal_longitude_deg: float,
    *,
    aspect: RayAspect,
    branch: RayBranch,
    obliquity_deg: float,
) -> AspectPoint:
    """Traditional zero-β longitude ray; no instantaneous-β propagation."""
    aspect = RayAspect(aspect)
    branch = RayBranch(branch)
    if branch not in aspect_branches(aspect):
        raise ValueError("opposition has one mathematically distinct branch")
    if not math.isfinite(natal_longitude_deg) or not 0 <= natal_longitude_deg < 360:
        raise ValueError("natal ecliptic longitude must be normalized")
    offset = ASPECT_DEGREES[aspect] * (1 if branch is RayBranch.POSITIVE else -1)
    longitude = normalize(natal_longitude_deg + offset)
    return AspectPoint(
        aspect=aspect,
        branch=branch,
        offset_deg=offset,
        ecliptic_longitude_deg=longitude,
        ecliptic_latitude_deg=0.0,
        equatorial=ecliptic_to_equatorial(longitude, 0, obliquity_deg),
    )


def mundane_semi_arc_phase_arc(
    latitude_deg: float,
    ramc_deg: float,
    fixed: EquatorialPoint,
    moving: EquatorialPoint,
    *,
    aspect: RayAspect,
    branch: RayBranch,
) -> float:
    """Proportional semi-arc positional aspect, *not* a zodiacal longitude ray."""
    aspect = RayAspect(aspect)
    branch = RayBranch(branch)
    if branch not in aspect_branches(aspect):
        raise ValueError("opposition has one mathematically distinct branch")
    ds_fixed, ns_fixed = _semi_arcs(latitude_deg, fixed.dec_deg)
    ds_moving, ns_moving = _semi_arcs(latitude_deg, moving.dec_deg)
    fixed_phase = _phase(fixed.ra_deg - ramc_deg, ds_fixed, ns_fixed)
    delta = ASPECT_DEGREES[aspect] * (1 if branch is RayBranch.POSITIVE else -1)
    target_phase = normalize(fixed_phase + delta)
    h = _hour_angle(target_phase, ds_moving, ns_moving)
    crossing_ra = normalize(ramc_deg + h)
    arc = normalize(moving.ra_deg - crossing_ra)
    if not math.isfinite(arc):
        raise GeometryUnavailable("mundane aspect calculation did not yield finite arc")
    return arc
