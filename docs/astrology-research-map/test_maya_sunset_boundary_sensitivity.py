#!/usr/bin/env python3
"""Regression tests for published Maya day-count examples. No human data."""
import json
from pathlib import Path
from datetime import date, datetime
import unittest
from maya_sunset_boundary_sensitivity import sacred_day_sensitivity, KNOWN_PHASES
from maya_calendar_reference import CalendarScopeError

EVIDENCE=json.loads(Path(__file__).with_name(
    "MAYA_SUNSET_BOUNDARY_SOURCE_WITNESSES_V1.json").read_text(encoding="utf-8"))
KNOWN={
 ("1927-03-10","after_sunset"):(2,"Q’ANIL"),
 ("1927-03-15","after_sunset"):(7,"AJ"),
 ("1939-03-12","before_sunset"):(5,"E"),
 ("1939-03-12","after_sunset"):(6,"AJ"),
 ("1939-11-26","before_sunset"):(4,"B’ATZ’"),
 ("1939-11-26","after_sunset"):(5,"E"),
 ("1940-11-25","before_sunset"):(5,"AJMAQ"),
 ("1940-11-25","after_sunset"):(6,"NO’J"),
 ("2015-02-21","before_sunset"):(3,"E"),
 ("2015-02-21","after_sunset"):(4,"AJ"),
 ("2015-04-02","before_sunset"):(4,"E"),
 ("2015-04-02","after_sunset"):(5,"AJ"),
 ("2016-02-21","before_sunset"):(4,"NO’J"),
 ("2016-02-21","after_sunset"):(5,"TIJAX"),
}

class MayaSunsetSourceTests(unittest.TestCase):
    def test_source_entries_are_exhaustive_and_deduplicated(self):
        actual=EVIDENCE["dated_source_witnesses"]
        self.assertEqual(len(actual),len(KNOWN))
        self.assertEqual(len({v["id"] for v in actual}),len(actual))
        for v in actual:
            key=(v["civil_date"],v["phase"])
            self.assertIn(key,KNOWN)
            self.assertEqual((v["day_number"],v["kiche_name"]),KNOWN[key])
            self.assertTrue(v["provenance"])

    def test_all_published_date_labels_recalculate(self):
        for (d,phase),expected in KNOWN.items():
            with self.subTest(d=d,phase=phase):
                out=sacred_day_sensitivity(date.fromisoformat(d),phase)
                self.assertEqual(len(out["candidate_tzolkin_days"]),1)
                cand=out["candidate_tzolkin_days"][0]
                self.assertEqual((cand["day_number"],
                                  cand["kiche_name_crosswalk_only"]),expected)
                self.assertFalse(out["eligible_to_score_human"])

    def test_unknown_phase_has_both_options_and_abstains(self):
        v=sacred_day_sensitivity(date(2015,4,2),"unknown")
        self.assertEqual(v["status"],"REFERENCE_SENSITIVITY_ABSTAIN")
        self.assertEqual([(c["day_number"],c["kiche_name_crosswalk_only"])
                          for c in v["candidate_tzolkin_days"]],[(4,"E"),(5,"AJ")])
        self.assertEqual([c["calendar_reference_date"] for c in v["candidate_tzolkin_days"]],
                         ["2015-04-02","2015-04-03"])

    def test_not_shifting_solar_calendar_at_dusk(self):
        v=sacred_day_sensitivity(date(2015,4,2),"after_sunset")
        self.assertFalse(v["solar_ab_haab_or_long_count_inferred"])
        self.assertFalse(v["astronomical_sunset_computed"])
        self.assertFalse(any("haab" in k.lower() or "long_count" in k.lower()
                         for k in v["candidate_tzolkin_days"][0]))

    def test_other_GMT_variant_stays_unequal_and_labelled(self):
        a=sacred_day_sensitivity(date(2015,4,2),"before_sunset",correlation=584283)
        b=sacred_day_sensitivity(date(2015,4,2),"before_sunset",correlation=584285)
        self.assertNotEqual(a["candidate_tzolkin_days"],b["candidate_tzolkin_days"])
        self.assertEqual(b["GMT_correlation_JDN"],584285)
        self.assertFalse(b["can_select_favorable_variant_from_participant_answers"])

    def test_datetime_strings_and_invalid_phases_refused(self):
        for bad in [datetime(2015,4,2,19,0),"2015-04-02",None]:
            with self.subTest(bad=str(bad)):
                with self.assertRaises(CalendarScopeError):
                    sacred_day_sensitivity(bad,"after_sunset")
        self.assertEqual(KNOWN_PHASES,("before_sunset","after_sunset","unknown"))
        for bad in ["night","sunrise","19:00",None,False,1]:
            with self.subTest(bad=str(bad)):
                with self.assertRaises(CalendarScopeError):
                    sacred_day_sensitivity(date(2015,4,2),bad)

    def test_next_date_overflow_is_explicit_error(self):
        self.assertEqual(len(sacred_day_sensitivity(date.max,"before_sunset")
                             ["candidate_tzolkin_days"]),1)
        for phase in ("unknown","after_sunset"):
            with self.subTest(phase=phase):
                with self.assertRaises(CalendarScopeError):
                    sacred_day_sensitivity(date.max,phase)

    def test_unsupported_correlations_refused(self):
        for invalid in [584284,0,True,"584283",None]:
            with self.subTest(correlation=invalid):
                with self.assertRaises(CalendarScopeError):
                    sacred_day_sensitivity(date(2015,4,2),"unknown",
                                           correlation=invalid)

    def test_council_and_ninety_percent_refer_to_different_findings(self):
        src=EVIDENCE["source"]
        self.assertRegex(src["sha256"],r"^[a-f0-9]{64}$")
        self.assertTrue(src["sha256_checked_owner_local_pdf"])
        self.assertFalse(src["original_pdf_committed_to_repository"])
        p58=[p for p in src["page_locations"] if p.get("printed_page")==58][0]
        self.assertIn("NOT sunset agreement",p58["finding"])

    def test_unverified_birth_boundary_and_human_outcomes_stay_zero(self):
        c=EVIDENCE["closeout"]
        self.assertFalse(c["natal_local_practitioner_day_clock_confirmed"])
        self.assertFalse(c["day_sign_personality_prediction_validated"])
        self.assertEqual(c["actual_consenting_untouched_humans_tested"],0)
        self.assertEqual(c["runtime_rule_promotions"],0)
        v=sacred_day_sensitivity(date(2016,2,21),"unknown")
        self.assertFalse(v["regional_birth_day_assignment_independently_validated"])
        self.assertFalse(v["eligible_to_score_human"])

if __name__=="__main__":
    unittest.main()
