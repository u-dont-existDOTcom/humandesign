"""Bounded source arithmetic for Robbins/Ptolemy III.9-III.10.

No birth-chart engine, health/identity predictor, or validated forecasting API.
Signed-distance helpers operate only on already supplied source quantities.
"""
from __future__ import annotations

import math
from numbers import Real

PROROGATIVE_PRIORITY = (
    "MIDHEAVEN", "ORIENT", "SUCCEDENT_TO_MIDHEAVEN",
    "OCCIDENT", "PRECEDING_MIDHEAVEN",
)

def _finite(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, not bool or text")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def sexagesimal(degrees: float, minutes: float = 0, seconds: float = 0) -> float:
    """Nonnegative source sexagesimal quantity; signs are handled separately."""
    d, m, s = (_finite(degrees, "degrees"), _finite(minutes, "minutes"),
               _finite(seconds, "seconds"))
    if d < 0 or not 0 <= m < 60 or not 0 <= s < 60:
        raise ValueError("Use nonnegative degrees and minute/second fields in [0,60)")
    return d + m / 60 + s / 3600

def fortune_main_text(ascendant: float, sun: float, moon: float, *, sect: str) -> float:
    """Adopted III.10 main text explicitly uses this formula for BOTH sects."""
    if sect not in ("DAY", "NIGHT"):
        raise ValueError("sect must be DAY or NIGHT")
    a, s, m = (_finite(ascendant, "ascendant"), _finite(sun, "sun"),
               _finite(moon, "moon"))
    return (a + m - s) % 360

def ordinary_hour_magnitude(semiarc_equinoctial_times: float) -> float:
    """One ordinary hour is one-sixth of the relevant supplied semiarc."""
    arc = _finite(semiarc_equinoctial_times, "semiarc")
    if not 0 < arc < 180:
        raise ValueError("This bounded fixture requires an ordinary rising/setting semiarc")
    return arc / 6

def directed_example_interval(initial_signed_distance: float,
                              target_signed_ordinary_hours: float,
                              subsequent_hour_magnitude: float) -> float:
    """Initial minus target equatorial distance; east positive, west negative.

    This is a source-example replay, not a general choice of arc/meridian/epoch.
    Negative results remain negative, never silently absolutized or wrapped.
    """
    initial = _finite(initial_signed_distance, "initial distance")
    hours = _finite(target_signed_ordinary_hours, "ordinary hours")
    magnitude = _finite(subsequent_hour_magnitude, "horary magnitude")
    if not -6 <= hours <= 6:
        raise ValueError("Only a supplied six-ordinary-hour quadrant is covered")
    if magnitude <= 0:
        raise ValueError("Horary magnitude must be positive")
    return initial - hours * magnitude

def quadrant_interpolation(start: float, end: float, hours_from_start: float) -> float:
    """Ptolemy's stated approximate interpolation between neighbouring angles."""
    a, b, h = (_finite(start, "start"), _finite(end, "end"),
               _finite(hours_from_start, "hours"))
    if not 0 <= h <= 6:
        raise ValueError("hours must lie within a six-hour quadrant")
    return a + (h / 6) * (b - a)

def protective_ray_distance_only(contact: float, already_qualified_ray: float,
                                benefic: str) -> bool:
    """Distance component only, not a complete protective testimony.

    The caller must separately establish the source's allowed aspect,
    visibility, term, direction-mode, topical and competing-rule conditions.
    """
    limits = {"JUPITER": 12, "VENUS": 8}
    if benefic not in limits:
        raise ValueError("Only Jupiter and Venus have a numerical limit here")
    contact = _finite(contact, "contact")
    ray = _finite(already_qualified_ray, "ray")
    return (ray - contact) % 360 <= limits[benefic]

def cardanus_opposition_example(lon_a: float, lat_a: float,
                                lon_b: float, lat_b: float,
                                *, numeric_tolerance: float = 1e-9) -> bool:
    """Geometry of the COMMENTATOR'S example, not Ptolemy's resolved definition.

    Tolerance is numerical test precision, not an astrologically sourced orb.
    """
    a,b,x,y,t = (_finite(lon_a,"lon_a"), _finite(lon_b,"lon_b"),
                 _finite(lat_a,"lat_a"), _finite(lat_b,"lat_b"),
                 _finite(numeric_tolerance,"tolerance"))
    if not -90 <= x <= 90 or not -90 <= y <= 90 or t < 0:
        raise ValueError("Invalid latitude or numerical tolerance")
    return abs((b-a) % 360 - 180) <= t and abs(x+y) <= t
