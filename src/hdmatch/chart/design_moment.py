"""Exact 88-degree solar-arc Design-moment root solving."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from .ephemeris import CelestialBody, EphemerisProvider


class DesignMomentError(RuntimeError):
    """Raised when the declared 88-degree root cannot be safely solved."""


@dataclass(frozen=True, slots=True)
class DesignMomentResult:
    birth_utc: datetime
    design_utc: datetime
    target_arc_degrees: float
    solved_arc_degrees: float
    residual_degrees: float
    bracket_start_utc: datetime
    bracket_end_utc: datetime
    iterations: int
    time_tolerance_seconds: float
    arc_tolerance_degrees: float


def backward_solar_arc_degrees(
    provider: EphemerisProvider,
    birth_utc: datetime,
    earlier_utc: datetime,
) -> float:
    """Return the forward tropical arc from earlier Sun to birth Sun."""

    birth = _require_utc(birth_utc)
    earlier = _require_utc(earlier_utc)
    if earlier >= birth:
        raise ValueError("earlier_utc must be before birth_utc")
    birth_longitude = provider.position(CelestialBody.SUN, birth).longitude
    earlier_longitude = provider.position(CelestialBody.SUN, earlier).longitude
    return (birth_longitude - earlier_longitude) % 360.0


def solve_design_moment(
    provider: EphemerisProvider,
    birth_utc: datetime,
    *,
    target_arc_degrees: float = 88.0,
    bracket_days_before: tuple[float, float] = (70.0, 110.0),
    time_tolerance_seconds: float = 0.01,
    arc_tolerance_degrees: float = 1e-8,
    max_iterations: int = 96,
) -> DesignMomentResult:
    """Solve ``Sun(birth) - Sun(design) = 88°`` by deterministic bisection.

    The bracket is stated as increasing days before birth.  The solar arc is
    monotone across the default sub-year bracket; a failed sign test is treated
    as an engine/configuration failure instead of switching to an approximate
    day offset.
    """

    birth = _require_utc(birth_utc)
    near_days, far_days = bracket_days_before
    if not (0.0 < near_days < far_days < 360.0):
        raise ValueError("bracket days must satisfy 0 < near < far < 360")
    if not (0.0 < target_arc_degrees < 180.0):
        raise ValueError("target arc must be between 0 and 180 degrees")
    if time_tolerance_seconds <= 0.0 or arc_tolerance_degrees <= 0.0:
        raise ValueError("root tolerances must be positive")
    if max_iterations < 1:
        raise ValueError("max_iterations must be positive")

    birth_sun = provider.position(CelestialBody.SUN, birth).longitude
    near = birth - timedelta(days=near_days)
    far = birth - timedelta(days=far_days)

    def residual(at_utc: datetime) -> float:
        longitude = provider.position(CelestialBody.SUN, at_utc).longitude
        return (birth_sun - longitude) % 360.0 - target_arc_degrees

    near_residual = residual(near)
    far_residual = residual(far)
    if near_residual == 0.0:
        return _result(
            birth,
            near,
            target_arc_degrees,
            near_residual,
            far,
            near,
            0,
            time_tolerance_seconds,
            arc_tolerance_degrees,
        )
    if far_residual == 0.0:
        return _result(
            birth,
            far,
            target_arc_degrees,
            far_residual,
            far,
            near,
            0,
            time_tolerance_seconds,
            arc_tolerance_degrees,
        )
    if not (near_residual < 0.0 < far_residual):
        raise DesignMomentError(
            "88-degree Design root is not bracketed by the declared window: "
            f"near residual={near_residual:.12g}, far residual={far_residual:.12g}"
        )

    # Work in increasing chronological order: far is earlier and positive;
    # near is later and negative.
    low_time, low_value = far, far_residual
    high_time, high_value = near, near_residual
    midpoint = low_time
    midpoint_value = low_value
    iterations = 0
    for iteration in range(1, max_iterations + 1):
        iterations = iteration
        midpoint = low_time + (high_time - low_time) / 2
        midpoint_value = residual(midpoint)
        if (
            abs(midpoint_value) <= arc_tolerance_degrees
            and (high_time - low_time).total_seconds() <= time_tolerance_seconds
        ):
            break
        if midpoint_value > 0.0:
            low_time, low_value = midpoint, midpoint_value
        else:
            high_time, high_value = midpoint, midpoint_value
    else:
        raise DesignMomentError(
            "Design root did not converge within max_iterations; "
            f"last residual={midpoint_value:.12g} degrees"
        )

    if not math.isfinite(low_value + high_value + midpoint_value):
        raise DesignMomentError("non-finite solar longitude encountered during root solve")
    return _result(
        birth,
        midpoint,
        target_arc_degrees,
        midpoint_value,
        far,
        near,
        iterations,
        time_tolerance_seconds,
        arc_tolerance_degrees,
    )


def _result(
    birth: datetime,
    design: datetime,
    target: float,
    residual: float,
    bracket_start: datetime,
    bracket_end: datetime,
    iterations: int,
    time_tolerance: float,
    arc_tolerance: float,
) -> DesignMomentResult:
    return DesignMomentResult(
        birth_utc=birth,
        design_utc=design,
        target_arc_degrees=target,
        solved_arc_degrees=target + residual,
        residual_degrees=residual,
        bracket_start_utc=bracket_start,
        bracket_end_utc=bracket_end,
        iterations=iterations,
        time_tolerance_seconds=time_tolerance,
        arc_tolerance_degrees=arc_tolerance,
    )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Design timestamps must be timezone-aware")
    return value.astimezone(UTC)
