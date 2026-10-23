#!/usr/bin/env python3
"""No-birth-input diagnostic: sensitivity of a historical Yucatec CHUWEN claim.

NOT a living daykeeper converter, date-based horoscope, age inference or
human predictive validator. Computes *declared* arithmetic alternatives
only. Outputs no person's horoscope/trait.
"""
from __future__ import annotations

from datetime import date, timedelta

from maya_calendar_reference import (
    CalendarScopeError, reference_calendar_for_date,
)

FIXED_VARIANTS = (
    ("GMT584283_DATE_ONLY", 584283, 0),
    ("GMT584283_NEXT_SACRED_DAY", 584283, 1),
    ("GMT584285_DATE_ONLY", 584285, 0),
    ("GMT584285_NEXT_SACRED_DAY", 584285, 1),
)
PRIMARY_REFERENCE_VARIANT = "GMT584283_DATE_ONLY"
PRIMARY_SIGN = "CHUWEN"

def diagnostic_chuwen_day_sensitivity(civil_day: date) -> dict:
    """Show all four candidate labels; never select them after seeing responses.

    The +1 day shift is a *what-if* boundary sensitivity inferred from
    other Maya contexts, NOT a demonstrated Yucatec natal rollover.
    GMT 584285 is a fixed competing offset, not posteriorly chosen.
    """
    if type(civil_day) is not date:
        raise CalendarScopeError("Explicit date required; no datetime, birth place or timezone")
    if civil_day == date.max:
        raise CalendarScopeError("After-date alternative exceeds supported civil years")
    candidates=[]
    for policy, corr, shift in FIXED_VARIANTS:
        actual=reference_calendar_for_date(civil_day+timedelta(days=shift),correlation=corr)
        candidates.append({
          "policy":policy,
          "correlation_JDN":corr,
          "hypothetical_date_shift":shift,
          "sacred_day_number":actual["tzolkin_number"],
          "sacred_day_name":actual["tzolkin_yucatec_name"],
          "chuwen_class":actual["tzolkin_yucatec_name"]==PRIMARY_SIGN,
        })
    flags=[c["chuwen_class"] for c in candidates]
    return {
      "status":"RESEARCH_DATE_SENSITIVITY_NOT_VALIDATED_NATAL_ASSIGNMENT",
      "civil_date_Gregorian":civil_day.isoformat(),
      "candidate_policies":candidates,
      "declared_primary_reference":PRIMARY_REFERENCE_VARIANT,
      "candidate_sign_names_unique":len({c["sacred_day_name"] for c in candidates})==len(candidates),
      "positive_in_any_policy":any(flags),
      "positive_in_all_policies":all(flags),
      "calendar_policy_classification_disagrees":len(set(flags))>1,
      "does_not_measure_craft":True,
      "has_current_yucatec_birth_day_rule":False,
      "historical_source_personality_truth_verified":False,
      "eligible_for_unfrozen_human_prediction":False,
      "allowed_to_choose_best_fitting_variant_after_response":False,
    }
