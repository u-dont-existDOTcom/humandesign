"""Pure geometry and time-distance primitives from the Wave 3 specification.

The functions deliberately do not select planets, aspect angles, orbs, trait
mappings, interactions, or model weights.  Those choices are a Pro decision.
"""

from __future__ import annotations

import math
from datetime import datetime
from enum import StrEnum


class AspectPhase(StrEnum):
    """Direction of motion relative to aspect exactness over a forward step."""

    APPLYING = "applying"
    SEPARATING = "separating"
    STATIONARY_OR_UNRESOLVED = "stationary_or_unresolved"


def _finite(value: float, *, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _longitude(value: float, *, name: str) -> float:
    return _finite(value, name=name) % 360.0


def unsigned_angular_separation(longitude_a: float, longitude_b: float) -> float:
    """Return the shortest unsigned separation in degrees, in ``[0, 180]``."""

    a = _longitude(longitude_a, name="longitude_a")
    b = _longitude(longitude_b, name="longitude_b")
    raw = abs(a - b)
    return min(raw, 360.0 - raw)


def distance_to_aspect(
    longitude_a: float,
    longitude_b: float,
    *,
    aspect_angle: float,
) -> float:
    """Return absolute degrees from an exact unsigned aspect angle."""

    angle = _finite(aspect_angle, name="aspect_angle")
    if not 0.0 <= angle <= 180.0:
        raise ValueError("aspect_angle must be between 0 and 180 degrees")
    return abs(unsigned_angular_separation(longitude_a, longitude_b) - angle)


def aspect_phase_from_forward_step(
    longitude_a: float,
    longitude_b: float,
    forward_longitude_a: float,
    forward_longitude_b: float,
    *,
    aspect_angle: float,
    tolerance_degrees: float = 1e-12,
) -> AspectPhase:
    """Classify an aspect as applying or separating from a forward ephemeris step.

    The caller controls the step size and ephemeris.  This function only compares
    present and forward distances to exactness and fails closed inside a supplied
    numerical tolerance.
    """

    tolerance = _finite(tolerance_degrees, name="tolerance_degrees")
    if tolerance < 0.0:
        raise ValueError("tolerance_degrees must be non-negative")
    current = distance_to_aspect(
        longitude_a,
        longitude_b,
        aspect_angle=aspect_angle,
    )
    forward = distance_to_aspect(
        forward_longitude_a,
        forward_longitude_b,
        aspect_angle=aspect_angle,
    )
    change = forward - current
    if change < -tolerance:
        return AspectPhase.APPLYING
    if change > tolerance:
        return AspectPhase.SEPARATING
    return AspectPhase.STATIONARY_OR_UNRESOLVED


def minimum_axis_distance(
    body_longitude: float,
    *,
    ascendant_longitude: float,
    midheaven_longitude: float,
) -> float:
    """Return minimum ecliptic-longitude distance to ASC/DSC/MC/IC."""

    ascendant = _longitude(ascendant_longitude, name="ascendant_longitude")
    midheaven = _longitude(midheaven_longitude, name="midheaven_longitude")
    axes = (
        ascendant,
        (ascendant + 180.0) % 360.0,
        midheaven,
        (midheaven + 180.0) % 360.0,
    )
    return min(unsigned_angular_separation(body_longitude, axis) for axis in axes)


def near_time_distance_minutes(left: datetime, right: datetime) -> float:
    """Return absolute elapsed minutes between two timezone-aware birth times."""

    for name, value in (("left", left), ("right", right)):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{name} must be timezone-aware")
    return abs((left - right).total_seconds()) / 60.0
