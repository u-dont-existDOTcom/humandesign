#!/usr/bin/env python3
"""Source-limited Maya sunset-phase sensitivity, NOT a natal horoscope.

A Guatemalan 2016 source reports that Cholq'ij changes at dusk while
the solar Ab' changes at dawn. This reference sensitivity distinguishes
civil-date before/after the *observed* sunset without computing a sunset
clock time or presuming universal community/birth-time applicability.

The original date-only converter remains unchanged. Deliberately omit
Haab and Long Count fields: the solar Ab' does not roll at sunset.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from maya_calendar_reference import (
    CalendarScopeError,
    reference_calendar_for_date,
)

KNOWN_PHASES = ("before_sunset", "after_sunset", "unknown")
SOURCE_CLASS = "DOCUMENTED_2016_GUATEMALAN_CALENDAR_SUNSET_SENSITIVITY"
DOCUMENTED_POLICY = "Sacred count observed at dusk; solar Ab' separately at dawn"
UNVERIFIED_BOUNDARY = (
    "No verified universally applicable birth-specific rollover or sunset "
    "ephemeris; local practitioner/era-specific policy is still unresolved."
)


def _date_only(civil_date: date) -> None:
    if type(civil_date) is not date:
        raise CalendarScopeError(
            "Requires an explicit proleptic Gregorian civil date; "
            "birth datetime and implicit timezone conversion prohibited"
        )


def _tz_only(civil_date: date, *, correlation: int) -> dict[str, Any]:
    result = reference_calendar_for_date(civil_date, correlation=correlation)
    return {
        "calendar_reference_date": civil_date.isoformat(),
        "day_number": result["tzolkin_number"],
        "kiche_name_crosswalk_only": result["kiche_label_from_practitioner_crosswalk_only"],
        "yucatec_name_crosswalk_only": result["tzolkin_yucatec_name"],
    }


def sacred_day_sensitivity(
    civil_date: date,
    sunset_relation: str,
    *,
    correlation: int = 584283,
) -> dict[str, Any]:
    """Return *sensitivity* candidates, never a scored individual's chart.

    sunset_relation must be an EXTERNALLY OBSERVED (not inferred) phase:
       before_sunset: Gregorian-date lowland cycle label
       after_sunset:  next date's sacred-day label; solar calendar NOT shifted
       unknown:       both labels, mandatory ABSTAIN.

    No actual astronomical sunset is calculated, because latitude, longitude,
    timezone, civil-clock history and local practitioner rule are not inputs.
    Exactly the same computation may be run with GMT584285 as a separately
    declared historical correlation; never choose it by best answer fit.
    """
    _date_only(civil_date)
    if type(sunset_relation) is not str or sunset_relation not in KNOWN_PHASES:
        raise CalendarScopeError(
            "sunset_relation must be before_sunset, after_sunset, or unknown"
        )
    # Check correlation even for the input nearest max calendar date.
    reference_calendar_for_date(civil_date, correlation=correlation)
    wanted = (0, 1) if sunset_relation == "unknown" else (
        (1,) if sunset_relation == "after_sunset" else (0,)
    )
    if 1 in wanted and civil_date == date.max:
        raise CalendarScopeError("next calendar reference day lies outside CE 1..9999")
    candidates = [
        _tz_only(civil_date + timedelta(days=shift), correlation=correlation)
        for shift in wanted
    ]
    return {
        "status": "REFERENCE_SENSITIVITY_ABSTAIN" if sunset_relation == "unknown"
        else "SOURCE_GROUNDED_DAY_PHASE_SENSITIVITY_ONLY",
        "civil_date_proleptic_gregorian": civil_date.isoformat(),
        "declared_sunset_relation": sunset_relation,
        "GMT_correlation_JDN": correlation,
        "source_class": SOURCE_CLASS,
        "source_day_clock_policy": DOCUMENTED_POLICY,
        "candidate_tzolkin_days": candidates,
        "ambiguous_observed_sunset_phase": sunset_relation == "unknown",
        "regional_birth_day_assignment_independently_validated": False,
        "astronomical_sunset_computed": False,
        "solar_ab_haab_or_long_count_inferred": False,
        "can_select_favorable_variant_from_participant_answers": False,
        "eligible_to_score_human": False,
        "reason_to_abstain_from_human_scoring": UNVERIFIED_BOUNDARY,
    }
