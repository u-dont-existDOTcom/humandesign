#!/usr/bin/env python3
"""Two independent-library Four Pillars development oracle, NOT natal prediction.

Input is a fictional precise Gregorian reference-clock wall time under FIXED UTC+8,
not a place-of-birth civil time. Explicit China calendar/LiChun/Jie conventions.
Never feed a human DOB here or present this as a verified original BaZi calculator.
"""
from __future__ import annotations
from datetime import date, datetime, timedelta
from importlib.metadata import version
from typing import Any

PINNED_DEPENDENCIES = {"lunar-python": "1.4.8", "sxtwl": "2.0.7"}
STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
PILLARS = ("year", "month", "day", "hour")
POLICY = {
    "scope": "FICTIONAL_PRECISE_REFERENCE_CLOCK_FIXED_UTC_PLUS_08_ONLY",
    "birthplace_or_real_subject_mode": "UNSUPPORTED",
    "year_boundary": "LiChun exact solar term reference-clock instant",
    "month_boundary": "Jie exact solar term reference-clock instant",
    "day_boundary": "midnight (lunar-python EightChar sect 2)",
    "hour_branch": "recorded reference-clock two-hour branch, no true solar time",
    "leap_month_effect_on_bazi_month": "solar terms rather than lunar month",
    "timezone_conversion_or_historical_tzif": "NOT IMPLEMENTED",
    "original_ancient_BaZi_printed_source_authenticated": False,
    "predictive_accuracy_in_real_people_validated": False,
}


class WitnessError(ValueError):
    """Unsupported policy, witness absence or invalid sample."""


def _import_witnesses():
    try:
        import sxtwl
        from lunar_python import Solar
    except ImportError as err:
        raise WitnessError("PINNED_TWO_CALENDAR_PACKAGES_REQUIRED; do not invent an output") from err
    for dep,pin in PINNED_DEPENDENCIES.items():
        try:
            got = version(dep)
        except Exception as err:
            raise WitnessError(f"Cannot attest version for {dep}") from err
        if got != pin:
            raise WitnessError(f"Dependency {dep} expected {pin}, received {got}")
    return sxtwl, Solar


def _as_canonical_sample(t: datetime) -> datetime:
    if not isinstance(t, datetime) or t.tzinfo is not None:
        raise WitnessError("Only fictional, naive fixed UTC+8 wall clock datetime permitted")
    if not (1901 <= t.year <= 2100) or t.microsecond:
        raise WitnessError("Only years 1901–2100 and whole-second precision are supported")
    return t


def _as_stem_branch(gz) -> str:
    if gz.tg not in range(10) or gz.dz not in range(12):
        raise WitnessError("Invalid original GanZhi index from external source")
    return STEMS[gz.tg] + BRANCHES[gz.dz]


def _solar_term_local_datetime(day,sxtwl) -> datetime | None:
    if not day.hasJieQi():
        return None
    term = sxtwl.JD2DD(day.getJieQiJD())
    try:
        start = datetime(int(term.Y),int(term.M),int(term.D),
                         int(term.h),int(term.m),0)
        return start + timedelta(seconds=float(term.s))
    except (TypeError,ValueError,OverflowError) as err:
        raise WitnessError("Unable to resolve exact term time; fail closed") from err


def sxtwl_fourpillars(t: datetime, *, day_transition_correction: bool = True) -> dict[str,Any]:
    """sxtwl date-level year/month corrected with its own exact Jie instant."""
    t = _as_canonical_sample(t)
    sxtwl, _ = _import_witnesses()
    d = sxtwl.fromSolar(t.year,t.month,t.day)
    exact_term = _solar_term_local_datetime(d,sxtwl)
    solar_stem_day = d
    before_jie = exact_term is not None and t < exact_term
    if before_jie and day_transition_correction:
        yesterday = date(t.year,t.month,t.day) - timedelta(days=1)
        solar_stem_day = sxtwl.fromSolar(yesterday.year,yesterday.month,yesterday.day)
    vals = [_as_stem_branch(solar_stem_day.getYearGZ(False)),
            _as_stem_branch(solar_stem_day.getMonthGZ()),
            _as_stem_branch(d.getDayGZ()),
            _as_stem_branch(d.getHourGZ(t.hour,True))]
    return {
        "pillars": dict(zip(PILLARS,vals)),
        "sxtwl_day_start_month_before_exact_solar_term": bool(before_jie),
        "month_year_exact_Jie_term_datetime": exact_term.isoformat(timespec="microseconds") if exact_term else None,
        "sxtwl_lookup_corrected_to_previous_day": bool(before_jie and day_transition_correction),
        "year_policy": "getYearGZ(False) LiChun, not Chinese Lunar New Year",
        "hour_policy": "getHourGZ(hour, True) early/late Zi branch",
        "witness": "sxtwl 2.0.7",
    }


def lunar_python_fourpillars(t: datetime) -> dict[str,Any]:
    t = _as_canonical_sample(t)
    _, Solar = _import_witnesses()
    chart = Solar.fromYmdHms(t.year,t.month,t.day,t.hour,t.minute,t.second).getLunar().getEightChar()
    chart.setSect(2)
    vals = [chart.getYear(),chart.getMonth(),chart.getDay(),chart.getTime()]
    if any(len(v) != 2 or v[0] not in STEMS or v[1] not in BRANCHES for v in vals):
        raise WitnessError("Invalid lunar-python four-pillar returned values")
    return {
        "pillars": dict(zip(PILLARS,vals)),
        "year_policy": "EightChar LiChun",
        "day_policy": "EightChar sect2 midnight",
        "witness": "lunar-python 1.4.8",
    }


def compare_fictional_reference_clock(t: datetime) -> dict[str,Any]:
    t = _as_canonical_sample(t)
    a = sxtwl_fourpillars(t)
    b = lunar_python_fourpillars(t)
    differing = [name for name in PILLARS if a["pillars"][name]!=b["pillars"][name]]
    termstr = a["month_year_exact_Jie_term_datetime"]
    delta = (t - datetime.fromisoformat(termstr)).total_seconds() if termstr else None
    return {
        "schema": "DEVELOPMENT_ONLY_BAZI_FOURPILLARS_DUAL_WITNESS_V1",
        "fake_china_reference_clock_sample": t.isoformat(timespec="seconds"),
        "source_sxtwl":a,"source_lunar_python":b,
        "difference_components":differing,
        "witness_agreement":not differing,
        "status":"AGREE_ENGINEERING_ONLY" if not differing else "ABSTAIN_DIFFERENT_GANZHI_WITNESSES",
        "distance_seconds_from_sxtwl_jie":delta,
        "near_term_60_seconds_extra_caution":delta is not None and abs(delta)<=60,
        "real_human_blind_predictions":0,
        "production_natal_chart_ready":False,
    }
