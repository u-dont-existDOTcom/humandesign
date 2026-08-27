"""Frozen secondary-progression time mapping for longitudinal AstroHD tests.

Progressions are treated as a hypothesis to test, not as a repair applied after a
natal prediction misses. The convention here is explicit: one ephemeris day after
birth corresponds to one tropical year of elapsed life.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Final

from .ephemeris import CelestialBody, EclipticPosition, EphemerisProvider

TROPICAL_YEAR_DAYS: Final[float] = 365.24219


@dataclass(frozen=True, slots=True)
class SecondaryProgressionConvention:
    """Immutable day-for-year convention used by confirmatory progression tests."""

    name: str = "secondary_day_for_tropical_year_v1"
    year_length_days: float = TROPICAL_YEAR_DAYS

    def __post_init__(self) -> None:
        if self.year_length_days <= 0.0:
            raise ValueError("year_length_days must be positive")


DEFAULT_SECONDARY_PROGRESSION_CONVENTION: Final = SecondaryProgressionConvention()


@dataclass(frozen=True, slots=True)
class ProgressedPosition:
    body: CelestialBody
    position: EclipticPosition


@dataclass(frozen=True, slots=True)
class ProgressionSnapshot:
    """One age-indexed progressed state with its exact mapped ephemeris instant."""

    birth_utc: datetime
    observed_at_utc: datetime
    progressed_at_utc: datetime
    elapsed_age_years: float
    convention: SecondaryProgressionConvention
    positions: tuple[ProgressedPosition, ...]


def secondary_progressed_instant(
    birth_utc: datetime,
    observed_at_utc: datetime,
    *,
    convention: SecondaryProgressionConvention = DEFAULT_SECONDARY_PROGRESSION_CONVENTION,
) -> datetime:
    """Map an observed age to the corresponding day-for-year ephemeris instant."""

    birth = _require_utc(birth_utc)
    observed = _require_utc(observed_at_utc)
    if observed < birth:
        raise ValueError("observed_at_utc cannot precede birth_utc")
    elapsed_days = (observed - birth).total_seconds() / 86_400.0
    progressed_days = elapsed_days / convention.year_length_days
    return birth + timedelta(days=progressed_days)


def secondary_progressed_instant_for_age(
    birth_utc: datetime,
    age_years: float,
    *,
    convention: SecondaryProgressionConvention = DEFAULT_SECONDARY_PROGRESSION_CONVENTION,
) -> datetime:
    """Return the day-for-year ephemeris instant for an explicit decimal age."""

    birth = _require_utc(birth_utc)
    if age_years < 0.0:
        raise ValueError("age_years cannot be negative")
    return birth + timedelta(days=age_years)


def progression_snapshot(
    provider: EphemerisProvider,
    *,
    birth_utc: datetime,
    observed_at_utc: datetime,
    bodies: tuple[CelestialBody, ...],
    convention: SecondaryProgressionConvention = DEFAULT_SECONDARY_PROGRESSION_CONVENTION,
) -> ProgressionSnapshot:
    """Calculate a frozen progressed state for a real observation date."""

    birth = _require_utc(birth_utc)
    observed = _require_utc(observed_at_utc)
    progressed = secondary_progressed_instant(
        birth,
        observed,
        convention=convention,
    )
    elapsed_days = (observed - birth).total_seconds() / 86_400.0
    age_years = elapsed_days / convention.year_length_days
    positions = tuple(
        ProgressedPosition(body=body, position=provider.position(body, progressed))
        for body in bodies
    )
    return ProgressionSnapshot(
        birth_utc=birth,
        observed_at_utc=observed,
        progressed_at_utc=progressed,
        elapsed_age_years=age_years,
        convention=convention,
        positions=positions,
    )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("progression timestamps must be timezone-aware")
    return value.astimezone(UTC)
