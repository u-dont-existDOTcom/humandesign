"""Frozen MoBa 5-15 external-validation derivation helpers.

This module contains no outcome fitting.  It converts a Norwegian registry
birth date/time into the already-frozen 5-15 predictor and low-frequency
calendar controls declared in
``reference/validation/moba_vitality_5_15_freeze_v1.json``.

The derivation is intentionally small enough to run inside a data-custodian or
secure-analysis environment so exact birth date/time need not be exported.
"""

from __future__ import annotations

import calendar
import math
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from typing import Final, Literal
from zoneinfo import ZoneInfo

from hdmatch.chart.calculator import ChartComputation, calculate_chart
from hdmatch.chart.ephemeris import EphemerisProvider

OSLO_TIMEZONE: Final[str] = "Europe/Oslo"
GATE_5_WINDOW_DEGREES: Final[tuple[float, float]] = (251.375, 257.0)
GATE_15_WINDOW_DEGREES: Final[tuple[float, float]] = (88.25, 93.875)


@dataclass(frozen=True, slots=True)
class MoBaCalendarControls:
    """Frozen low-frequency non-astronomical controls for external validation."""

    birth_year: int
    day_of_year_sin_1: float
    day_of_year_cos_1: float
    day_of_year_sin_2: float
    day_of_year_cos_2: float
    time_of_day_sin_1: float
    time_of_day_cos_1: float
    time_of_day_sin_2: float
    time_of_day_cos_2: float


@dataclass(frozen=True, slots=True)
class MoBaPredictorDerivation:
    """Privacy-minimized result of the frozen birth-state derivation."""

    status: Literal["resolved", "ambiguous_resolved", "unresolved_dst"]
    z_5_15: bool | None
    utc_candidates: tuple[datetime, ...]
    controls: MoBaCalendarControls


def z_5_15_from_chart(chart: ChartComputation) -> bool:
    """Return the frozen raw two-window co-occurrence for one chart."""

    return z_5_15_from_longitudes(tuple(item.longitude for item in chart.activations))


def z_5_15_from_longitudes(longitudes: tuple[float, ...]) -> bool:
    """Evaluate the frozen half-open 5 and 15 longitude windows."""

    has_gate_5 = any(_in_half_open_window(value, GATE_5_WINDOW_DEGREES) for value in longitudes)
    has_gate_15 = any(
        _in_half_open_window(value, GATE_15_WINDOW_DEGREES) for value in longitudes
    )
    return has_gate_5 and has_gate_15


def derive_moba_5_15(
    provider: EphemerisProvider,
    *,
    birth_date: date,
    hhmm: str,
) -> MoBaPredictorDerivation:
    """Derive the frozen predictor from Norwegian civil birth date and HHMM.

    An autumn clock-fold can map one local time to two UTC instants.  The case
    is accepted only when both instants yield the same predictor.  A spring
    clock-gap is invalid input and raises ``ValueError`` rather than being
    silently repaired.
    """

    utc_candidates = resolve_oslo_utc_candidates(birth_date=birth_date, hhmm=hhmm)
    controls = frozen_calendar_controls(birth_date=birth_date, hhmm=hhmm)
    states = tuple(z_5_15_from_chart(calculate_chart(provider, item)) for item in utc_candidates)
    if len(set(states)) == 1:
        return MoBaPredictorDerivation(
            status="resolved" if len(utc_candidates) == 1 else "ambiguous_resolved",
            z_5_15=states[0],
            utc_candidates=utc_candidates,
            controls=controls,
        )
    return MoBaPredictorDerivation(
        status="unresolved_dst",
        z_5_15=None,
        utc_candidates=utc_candidates,
        controls=controls,
    )


def resolve_oslo_utc_candidates(*, birth_date: date, hhmm: str) -> tuple[datetime, ...]:
    """Resolve Norwegian civil time to all valid UTC instants.

    ``zoneinfo`` permits construction of nonexistent wall times, so each fold
    candidate is round-tripped through UTC.  Zero valid candidates indicates a
    spring-forward gap; two distinct candidates indicate an autumn fold.
    """

    local_clock = _parse_hhmm(hhmm)
    naive = datetime.combine(birth_date, local_clock)
    zone = ZoneInfo(OSLO_TIMEZONE)
    candidates: set[datetime] = set()
    for fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=fold)
        utc_value = aware.astimezone(UTC)
        round_trip = utc_value.astimezone(zone).replace(tzinfo=None)
        if round_trip == naive:
            candidates.add(utc_value)
    if not candidates:
        raise ValueError(
            f"nonexistent {OSLO_TIMEZONE} local birth time: {birth_date.isoformat()} {hhmm}"
        )
    return tuple(sorted(candidates))


def frozen_calendar_controls(*, birth_date: date, hhmm: str) -> MoBaCalendarControls:
    """Return the predeclared year, seasonal, and clock-time control basis."""

    local_clock = _parse_hhmm(hhmm)
    days_in_year = 366 if calendar.isleap(birth_date.year) else 365
    day_index = birth_date.timetuple().tm_yday - 1
    day_phase = math.tau * day_index / days_in_year
    minute_of_day = local_clock.hour * 60 + local_clock.minute
    time_phase = math.tau * minute_of_day / (24 * 60)
    return MoBaCalendarControls(
        birth_year=birth_date.year,
        day_of_year_sin_1=math.sin(day_phase),
        day_of_year_cos_1=math.cos(day_phase),
        day_of_year_sin_2=math.sin(2.0 * day_phase),
        day_of_year_cos_2=math.cos(2.0 * day_phase),
        time_of_day_sin_1=math.sin(time_phase),
        time_of_day_cos_1=math.cos(time_phase),
        time_of_day_sin_2=math.sin(2.0 * time_phase),
        time_of_day_cos_2=math.cos(2.0 * time_phase),
    )


def _parse_hhmm(value: str) -> time:
    if len(value) != 4 or not value.isascii() or not value.isdigit():
        raise ValueError("birth time must be exactly four ASCII digits HHMM")
    hour = int(value[:2])
    minute = int(value[2:])
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("birth time HHMM is outside the valid 0000-2359 clock range")
    return time(hour=hour, minute=minute)


def _in_half_open_window(value: float, window: tuple[float, float]) -> bool:
    if not math.isfinite(value):
        raise ValueError("activation longitude must be finite")
    normalized = value % 360.0
    lower, upper = window
    return lower <= normalized < upper
