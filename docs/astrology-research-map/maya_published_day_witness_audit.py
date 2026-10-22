#!/usr/bin/env python3
"""Diagnostic comparison of published ritual-calendar dates, NOT birth charts.

Never select a calendar variant because it improves matching a human response.
Published source labels are historical evidence; agreement with a chosen
algorithm does not validate any natal personality interpretation.
"""
from __future__ import annotations
from datetime import date, timedelta
from typing import Any
from maya_calendar_reference import (
    CalendarScopeError, KICHE_DAY_NAMES_BY_YUCATEC, reference_calendar_for_date
)

# A fixed universe, declared independently of observed source outcomes.
VARIANTS = (
    ("GMT584283_CIVIL", 584283, 0),
    ("GMT584283_AFTER_DUSK", 584283, 1),
    ("GMT584285_CIVIL", 584285, 0),
    ("GMT584285_AFTER_DUSK", 584285, 1),
)

def _only_date(day: date) -> None:
    if type(day) is not date:
        raise CalendarScopeError("Explicit Gregorian date required; no datetimes")

def _sig(day: date, correlation: int) -> tuple[int, str]:
    v = reference_calendar_for_date(day, correlation=correlation)
    return v["tzolkin_number"], v["kiche_label_from_practitioner_crosswalk_only"]

def diagnostic_published_day(
    civil_day: date,
    observed_number: int,
    observed_kiche: str,
) -> dict[str, Any]:
    """Compare fixed independent variants to reported PUBLIC (not human natal) label.

    Same civil day and +1 offset in two GMT correlations are the four DECLARED
    alternatives. This does not determine whether the witness spoke before or
    after sunset, what the date header means, or which culture's birth rule applies.
    """
    _only_date(civil_day)
    if type(observed_number) is not int or not 1 <= observed_number <= 13:
        raise CalendarScopeError("Expected calendar coefficient 1..13")
    if type(observed_kiche) is not str or observed_kiche not in KICHE_DAY_NAMES_BY_YUCATEC:
        raise CalendarScopeError("Expected an exact, source-crosswalk K'iche' day name")
    readings=[]
    for variant_id, correlation, offset in VARIANTS:
        try:
            expected_number, expected_name = _sig(civil_day + timedelta(days=offset),correlation)
        except OverflowError as ex:
            raise CalendarScopeError("Date offset is outside supported Gregorian years") from ex
        readings.append({
            "variant_id": variant_id,
            "correlation": correlation,
            "calendar_date_offset_days": offset,
            "predicted_number": expected_number,
            "predicted_kiche": expected_name,
            "matches_reported_label": (expected_number,expected_name) == (observed_number,observed_kiche),
        })
    compatible=[x["variant_id"] for x in readings if x["matches_reported_label"]]
    return {
        "civil_date_printed":civil_day.isoformat(),
        "reported_number":observed_number,
        "reported_kiche":observed_kiche,
        "declared_variant_results": readings,
        "compatible_variants_only_not_selected":compatible,
        "source_date_mismatch_under_preexisting_GMT584283_CIVIL":
            not readings[0]["matches_reported_label"],
        "variant_correctness_not_established":True,
        "time_of_day_not_inferred":True,
        "personality_eligibility":False,
        "human_predictive_validation":False,
    }

def residual_from_preexisting_gmt(civil_day:date, reported_number:int, reported_kiche:str)->list[int]:
    """Descriptive ±3-date residuals for source criticism, not tuning a model."""
    _only_date(civil_day)
    matches=[]
    for offset in range(-3,4):
        try:
            if _sig(civil_day+timedelta(days=offset),584283) == (reported_number,reported_kiche):
                matches.append(offset)
        except OverflowError:
            continue
    return matches
