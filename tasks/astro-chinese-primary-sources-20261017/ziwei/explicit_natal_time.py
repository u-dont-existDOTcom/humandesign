"""Conservative modern civil-birth-time bridge to the original Zi Wei rules.

This computes only an explicitly defined, synthetic/local-clock -> instant
-> Chinese-calendar reference DATE and source-convention hour branch. It does
not decide which geographical, solar-hour, leap-month, Li Chun or late Zi
conventions are correct for a person's historical tradition.

No real-person evidence and no behavioral/astrological predictive validity.
The year range 1901..2100 is bounded by the separately documented two-calendar
software comparison; its 2057 conflicting interval fails closed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from hashlib import sha256
from pathlib import Path
from typing import Literal
from zoneinfo import TZPATH, ZoneInfo, ZoneInfoNotFoundError

from dual_witness_civil_lunar import (
    LUNAR_NEW_YEAR_POLICY,
    OfficialLunarDate,
    dual_library_reference_date,
)
from quan_shu_fourteen_stars import FourteenStarLayout, fourteen_from_lunar_inputs
from ziwei_source_mechanics import BRANCHES

BIRTH_CLOCK_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
CALENDAR_DATE_POLICIES = (
    "same_instant_fixed_utc_plus_8_calendar_day",
    "birth_site_civil_date_hko_lookup",
)
HOUR_POLICIES = ("recorded_local_civil_clock", "local_mean_solar_longitude")
LEAP_MONTH_POLICIES = (
    "transmitted_quan_shu_as_next",
    "modern_leap_same_month",
    "modern_leap_first_15_same_else_next",
)
LATE_ZI_POLICY = "midnight_day_boundary"
CALENDAR_STANDARD_OFFSET = timezone(timedelta(hours=8), name="UTC+08:00")
BIRTH_CALENDAR_BOUNDARY = LUNAR_NEW_YEAR_POLICY


class NatalTimeResolutionError(ValueError):
    """Do not derive natal charts from ambiguous / invalid time assumptions."""


@dataclass(frozen=True)
class CivilClockResolution:
    birth_local_clock: str
    birth_iana_timezone: str
    fold: int
    birth_utc_instant: str
    utc_offset_seconds: int
    tzif_sha256: str | None
    birthplace_civil_calendar_day: str
    same_instant_fixed_utc_plus_8_calendar_day: str
    standard_utc_plus_8_calendar_clock: str
    mean_solar_local_clock: str | None
    longitude_east_degrees: str | None
    recorded_civil_hour_branch: str
    mean_solar_hour_branch: str | None
    selected_hour_branch: str
    selected_hour_policy: str
    selected_chinese_calendar_day: str
    selected_calendar_day_policy: str
    day_boundary_policy: str
    status: str = "bounded modern civil-time translation; NOT natal astronomy parity"


@dataclass(frozen=True)
class CivilTimeFourteenStars:
    clock: CivilClockResolution
    official_chinese_lunar_date: OfficialLunarDate
    leap_rule_selected: str
    principal_stars: FourteenStarLayout
    status: str = "explicit civil-clock input, bounded modern 14-star placement only; no forecast"


def _parse_birth_clock(s: str) -> datetime:
    if not isinstance(s, str) or not BIRTH_CLOCK_PATTERN.fullmatch(s):
        raise NatalTimeResolutionError(
            "Require local clock exactly YYYY-MM-DDTHH:MM:SS, without offset"
        )
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as exc:
        raise NatalTimeResolutionError("Not a valid Gregorian local date and hour") from exc
    if dt.tzinfo is not None or dt.isoformat(timespec="seconds") != s:
        raise NatalTimeResolutionError("Local clock must not contain an implicit offset")
    if not 1901 <= dt.year <= 2100:
        raise NatalTimeResolutionError("Bounded time engine only supports birth dates 1901..2100")
    return dt


def _get_zone(zone_id: str) -> ZoneInfo:
    if not isinstance(zone_id, str) or not zone_id or zone_id.strip() != zone_id:
        raise NatalTimeResolutionError("An explicit canonical IANA time-zone ID is required")
    try:
        return ZoneInfo(zone_id)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise NatalTimeResolutionError("Unsupported or unknown IANA timezone") from exc


def _zone_binary_sha(zone_id: str) -> str | None:
    # Evidence fingerprint for reproducibility on current host. The zone
    # database has historical corrections: do not promise identical results
    # on another unpinned tzdb version.
    for root in TZPATH:
        path = Path(root) / zone_id
        if path.is_file() and path.resolve().is_relative_to(Path(root).resolve()):
            return sha256(path.read_bytes()).hexdigest()
    return None


def _disambiguate_local_clock(
    clock: datetime, zone: ZoneInfo, fold: int | None
) -> tuple[datetime, int]:
    candidates: dict[int, datetime] = {}
    for f in (0, 1):
        localized = clock.replace(tzinfo=zone, fold=f)
        utc = localized.astimezone(UTC)
        back = utc.astimezone(zone)
        if back.replace(tzinfo=None) == clock and back.fold == f:
            candidates[f] = localized
    if not candidates:
        raise NatalTimeResolutionError("Nonexistent local clock during timezone forward gap")
    if len(candidates) == 2 and candidates[0].utcoffset() != candidates[1].utcoffset():
        if fold is None:
            raise NatalTimeResolutionError(
                "Ambiguous DST/repeated local clock: specify fold 0 or 1"
            )
        if type(fold) is not int or fold not in (0, 1):
            raise NatalTimeResolutionError("Timezone fold must be exactly 0 or 1")
        return candidates[fold], fold
    if fold not in (None, 0):
        raise NatalTimeResolutionError("fold=1 invalid for an unambiguous local clock")
    return clock.replace(tzinfo=zone, fold=0), 0


def _longitude_to_solar_offset(longitude: float | int | str | Decimal) -> tuple[timedelta, str]:
    if isinstance(longitude, bool):
        raise NatalTimeResolutionError("Longitude must be explicitly numeric east-positive")
    try:
        x = Decimal(str(longitude))
    except (InvalidOperation, TypeError) as exc:
        raise NatalTimeResolutionError("Longitude must be finite numeric degrees") from exc
    if not x.is_finite() or not -180 <= x <= 180:
        raise NatalTimeResolutionError("Longitude must be within [-180,180] east-positive")
    # 360 degrees / 24 hours: 1 degree is 240 mean-solar seconds.
    microseconds = int((x * Decimal(240_000_000)).to_integral_value(rounding=ROUND_HALF_EVEN))
    return timedelta(microseconds=microseconds), str(x)


def _branch_for_hour(hour: int) -> str:
    if type(hour) is not int or not 0 <= hour <= 23:
        raise NatalTimeResolutionError("Hour must be an integer 0..23")
    return BRANCHES[((hour + 1) // 2) % 12]


def resolve_explicit_local_birth_clock(
    birth_local_clock: str,
    birth_iana_timezone: str,
    *,
    fold: int | None,
    calendar_day_policy: Literal[
        "same_instant_fixed_utc_plus_8_calendar_day",
        "birth_site_civil_date_hko_lookup",
    ],
    hour_time_policy: Literal["recorded_local_civil_clock", "local_mean_solar_longitude"],
    longitude_east_degrees: float | int | str | Decimal | None,
    late_zi_day_policy: str,
    recorded_clock_uncertainty_seconds: int,
) -> CivilClockResolution:
    """Exactly resolve wall time and record all calendar/hour assumptions.

    This intentionally does not infer birthplace or source tradition. The
    city's IANA zone and longitude are independent explicit required inputs.
    Gap/fold handling follows PEP 495. A 23:00 Zi-day start, apparent-solar
    equation of time, and nonzero uncertain birth time are not yet supported.
    """
    clock = _parse_birth_clock(birth_local_clock)
    if (
        type(recorded_clock_uncertainty_seconds) is not int
        or recorded_clock_uncertainty_seconds != 0
    ):
        raise NatalTimeResolutionError(
            "Nonzero birth-time uncertainty requires interval propagation, "
            "not implemented"
        )
    if late_zi_day_policy != LATE_ZI_POLICY:
        raise NatalTimeResolutionError(
            "Only explicit midnight lunar-day boundary is implemented; "
            "23:00 Zi-day not assumed"
        )
    if calendar_day_policy not in CALENDAR_DATE_POLICIES:
        raise NatalTimeResolutionError(
            "Explicit fixed UTC+8 instant-date versus "
            "birthplace civil-date policy required"
        )
    if hour_time_policy not in HOUR_POLICIES:
        raise NatalTimeResolutionError(
            "Explicit civil-clock or local-mean-solar hour method required"
        )
    if hour_time_policy == "local_mean_solar_longitude" and longitude_east_degrees is None:
        raise NatalTimeResolutionError(
            "Local mean solar hour requires explicit birthplace longitude"
        )

    zone = _get_zone(birth_iana_timezone)
    aware, chosen_fold = _disambiguate_local_clock(clock, zone, fold)
    utc = aware.astimezone(UTC)
    # Chinese official modern standard-calendar day follows UTC+08:00,
    # NOT historical Asia/Hong_Kong civil time during 1941..1979 summer DST.
    # Reference: HKO historical summer time and modern calendar UTC+8;
    # pre-20th-century/other historical new-moon standards unverified.
    standard_clock = utc.astimezone(CALENDAR_STANDARD_OFFSET)
    mean_dt: datetime | None = None
    longitude_str: str | None = None
    if longitude_east_degrees is not None:
        solar_delta, longitude_str = _longitude_to_solar_offset(longitude_east_degrees)
        mean_dt = utc.replace(tzinfo=None) + solar_delta
    if hour_time_policy == "local_mean_solar_longitude":
        if mean_dt is None:
            raise NatalTimeResolutionError("Local mean solar longitude input missing")
        selected_hour_branch = _branch_for_hour(mean_dt.hour)
    else:
        selected_hour_branch = _branch_for_hour(clock.hour)

    local_day = clock.date().isoformat()
    hk_day = standard_clock.date().isoformat()
    selected_day = (hk_day if calendar_day_policy == CALENDAR_DATE_POLICIES[0]
                    else local_day)
    if not 1901 <= int(selected_day[:4]) <= 2100:
        raise NatalTimeResolutionError(
            "Converted Chinese-calendar reference day outside tested 1901..2100 range"
        )

    utc_offset = aware.utcoffset()
    if utc_offset is None:
        raise NatalTimeResolutionError("No deterministic IANA UTC offset")
    return CivilClockResolution(
        birth_local_clock=birth_local_clock,
        birth_iana_timezone=birth_iana_timezone,
        fold=chosen_fold,
        birth_utc_instant=utc.isoformat(timespec="seconds"),
        utc_offset_seconds=int(utc_offset.total_seconds()),
        tzif_sha256=_zone_binary_sha(birth_iana_timezone),
        birthplace_civil_calendar_day=local_day,
        same_instant_fixed_utc_plus_8_calendar_day=hk_day,
        standard_utc_plus_8_calendar_clock=standard_clock.isoformat(timespec="seconds"),
        mean_solar_local_clock=(mean_dt.isoformat(timespec="microseconds") if mean_dt else None),
        longitude_east_degrees=longitude_str,
        recorded_civil_hour_branch=_branch_for_hour(clock.hour),
        mean_solar_hour_branch=_branch_for_hour(mean_dt.hour) if mean_dt else None,
        selected_hour_branch=selected_hour_branch,
        selected_hour_policy=hour_time_policy,
        selected_chinese_calendar_day=selected_day,
        selected_calendar_day_policy=calendar_day_policy,
        day_boundary_policy=late_zi_day_policy,
    )


def fourteen_stars_from_explicit_civil_birth(
    birth_local_clock: str,
    birth_iana_timezone: str,
    *,
    fold: int | None,
    calendar_day_policy: str,
    hour_time_policy: str,
    longitude_east_degrees: float | int | str | Decimal | None,
    late_zi_day_policy: str,
    recorded_clock_uncertainty_seconds: int,
    lunar_year_boundary_policy: str,
    leap_month_policy: str,
    documented_nayin_emendations: bool,
    documented_diagram_corrections: bool,
) -> CivilTimeFourteenStars:
    """Source-based major-star chart under ALL explicitly specified policies.

    No automatic 'best tradition' selection. External astronomy/calendar
    packages may disagree (notably 2057), in which case fail closed.
    """
    if lunar_year_boundary_policy != BIRTH_CALENDAR_BOUNDARY:
        raise NatalTimeResolutionError(
            "Li Chun year-stem policy unimplemented; explicit Lunar New Year required"
        )
    if leap_month_policy not in LEAP_MONTH_POLICIES:
        raise NatalTimeResolutionError("Leap month method must be selected, no implicit default")
    resolution = resolve_explicit_local_birth_clock(
        birth_local_clock, birth_iana_timezone,
        fold=fold, calendar_day_policy=calendar_day_policy,
        hour_time_policy=hour_time_policy,
        longitude_east_degrees=longitude_east_degrees,
        late_zi_day_policy=late_zi_day_policy,
        recorded_clock_uncertainty_seconds=recorded_clock_uncertainty_seconds,
    )
    lunar = dual_library_reference_date(resolution.selected_chinese_calendar_day)
    advance = (
        lunar.is_leap_month and (
            leap_month_policy == "transmitted_quan_shu_as_next"
            or (leap_month_policy == "modern_leap_first_15_same_else_next" and lunar.day > 15)
        )
    )
    chart = fourteen_from_lunar_inputs(
        lunar.year_heavenly_stem,
        lunar.month,
        resolution.selected_hour_branch,
        lunar.day,
        is_leap_month=advance,
        documented_nayin_emendations=documented_nayin_emendations,
        documented_diagram_corrections=documented_diagram_corrections,
    )
    return CivilTimeFourteenStars(resolution, lunar, leap_month_policy, chart)


ENGINE_SCOPE = {
    "local_named_timezone_PE495_disambiguated": True,
    "geographic_birthplace_inferred": False,
    "reference_calendar_day_policies_explicit": True,
    "longitude_local_mean_solar_supported": True,
    "astronomical_apparent_solar_equation_of_time": False,
    "late_zi_23_day_start_supported": False,
    "nonzero_birth_clock_uncertainty_propagation": False,
    "full_classical_historic_calendar_parity": False,
    "LiChun_year_boundary": False,
    "fourteen_principal_stars_only_not_full_chart": True,
    "validated_human_birth_chart_records": 0,
    "independent_blinded_predictive_human_tests": 0,
    "runtime_forecast_promotions": 0,
}
