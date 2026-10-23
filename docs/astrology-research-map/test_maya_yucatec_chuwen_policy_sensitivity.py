#!/usr/bin/env python3
"""Check deterministic Chuwen source-date sensitivity, not astrology efficacy."""
from datetime import date, timedelta, datetime
import unittest
from maya_yucatec_chuwen_policy_sensitivity import (
  diagnostic_chuwen_day_sensitivity, FIXED_VARIANTS, PRIMARY_REFERENCE_VARIANT
)
from maya_calendar_reference import CalendarScopeError

class YucatecChuwenHypothesisSensitivity(unittest.TestCase):
    def test_fixed_four_historical_arithmetic_policies(self):
        self.assertEqual(FIXED_VARIANTS,(
          ("GMT584283_DATE_ONLY",584283,0),
          ("GMT584283_NEXT_SACRED_DAY",584283,1),
          ("GMT584285_DATE_ONLY",584285,0),
          ("GMT584285_NEXT_SACRED_DAY",584285,1)))
        self.assertEqual(PRIMARY_REFERENCE_VARIANT,"GMT584283_DATE_ONLY")

    def test_full_twenty_day_cycle_has_four_ambiguous_chuwen_classes(self):
        anchor=date(2020,1,1)
        x=[diagnostic_chuwen_day_sensitivity(anchor+timedelta(days=i)) for i in range(20)]
        self.assertEqual(sum(v["positive_in_any_policy"] for v in x),4)
        self.assertEqual(sum(v["calendar_policy_classification_disagrees"] for v in x),4)
        self.assertEqual(sum(v["positive_in_all_policies"] for v in x),0)
        self.assertEqual(sum(not v["positive_in_any_policy"] for v in x),16)

    def test_distinct_date_policy_names_are_calculated_not_selected(self):
        for i in range(40):
            v=diagnostic_chuwen_day_sensitivity(date(2022,1,1)+timedelta(days=i))
            self.assertTrue(v["candidate_sign_names_unique"])
            self.assertEqual([c["policy"] for c in v["candidate_policies"]],[x[0] for x in FIXED_VARIANTS])
            self.assertFalse(v["eligible_for_unfrozen_human_prediction"])

    def test_mutant_choice_of_closest_date_detectable(self):
        day=date(2020,1,1)
        cases=[diagnostic_chuwen_day_sensitivity(day+timedelta(days=i)) for i in range(20)]
        mixed=[v for v in cases if v["calendar_policy_classification_disagrees"]]
        self.assertEqual(len(mixed),4)
        for v in mixed:
            self.assertNotEqual(
              len({c["chuwen_class"] for c in v["candidate_policies"]}),1
            )
            self.assertFalse(v["allowed_to_choose_best_fitting_variant_after_response"])

    def test_calendar_support_not_human_validation_or_modern_clock(self):
        v=diagnostic_chuwen_day_sensitivity(date(2022,1,1))
        self.assertFalse(v["has_current_yucatec_birth_day_rule"])
        self.assertFalse(v["historical_source_personality_truth_verified"])
        self.assertTrue(v["does_not_measure_craft"])
        self.assertEqual(v["status"],"RESEARCH_DATE_SENSITIVITY_NOT_VALIDATED_NATAL_ASSIGNMENT")

    def test_birth_datetime_and_non_dates_rejected(self):
        for invalid in (datetime(2022,1,1,12,0),"2022-01-01",None,1):
            with self.subTest(arg=str(invalid)):
                with self.assertRaises(CalendarScopeError):
                    diagnostic_chuwen_day_sensitivity(invalid)

    def test_ce_max_date_rejected_before_overflow(self):
        with self.assertRaises(CalendarScopeError):
            diagnostic_chuwen_day_sensitivity(date.max)

    def test_no_current_personal_birth_information_in_reference_output(self):
        v=diagnostic_chuwen_day_sensitivity(date(2022,1,1))
        self.assertEqual(set(v.keys())-{
          "status","civil_date_Gregorian","candidate_policies",
          "declared_primary_reference","candidate_sign_names_unique",
          "positive_in_any_policy","positive_in_all_policies",
          "calendar_policy_classification_disagrees","does_not_measure_craft",
          "has_current_yucatec_birth_day_rule","historical_source_personality_truth_verified",
          "eligible_for_unfrozen_human_prediction",
          "allowed_to_choose_best_fitting_variant_after_response"},set())
if __name__=="__main__":
    unittest.main()
