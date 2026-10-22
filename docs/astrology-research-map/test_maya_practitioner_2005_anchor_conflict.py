#!/usr/bin/env python3
"""Published calendar witness audit: explicit contradictory examples retained."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import date, datetime
import unittest

from maya_published_day_witness_audit import (
    VARIANTS, diagnostic_published_day, residual_from_preexisting_gmt
)
from maya_calendar_reference import CalendarScopeError

HERE=Path(__file__).parent
DATA=json.loads((HERE/"MAYA_2005_PRACTITIONER_AND_2019_DATE_DISCREPANCY_V1.json").read_text(encoding="utf-8"))
TEDLOCK=json.loads((HERE/"MAYA_TEDLOCK_MADRID_SOURCE_WITNESSES_V1.json").read_text(encoding="utf-8"))

class DatedIndigenousDayWitnessChecks(unittest.TestCase):
    def test_reported_2005_sequence_is_fully_source_pinned(self):
        rows=DATA["dated_speaker_sequence"]
        self.assertEqual(len(rows),3)
        self.assertEqual([(x["civil_date_from_producer"],x["day_number"],x["kiche"]) for x in rows],[
            ("2005-02-12",7,"TZ’I’"),("2005-02-13",8,"B’ATZ’"),("2005-02-14",9,"E")])
        self.assertEqual([r["relative_position"] for r in rows],[0,1,2])
        self.assertTrue(rows[1]["derived_not_independently_dated"])
        self.assertTrue(rows[2]["derived_not_independently_dated"])

    def test_2005_today_disagrees_with_prior_fixed_GMT584283(self):
        a=diagnostic_published_day(date(2005,2,12),7,"TZ’I’")
        self.assertTrue(a["source_date_mismatch_under_preexisting_GMT584283_CIVIL"])
        r={x["variant_id"]:x for x in a["declared_variant_results"]}
        self.assertEqual((r["GMT584283_CIVIL"]["predicted_number"],r["GMT584283_CIVIL"]["predicted_kiche"]),(8,"B’ATZ’"))
        self.assertEqual((r["GMT584283_AFTER_DUSK"]["predicted_number"],r["GMT584283_AFTER_DUSK"]["predicted_kiche"]),(9,"E"))
        self.assertEqual((r["GMT584285_CIVIL"]["predicted_number"],r["GMT584285_CIVIL"]["predicted_kiche"]),(6,"TOJ"))
        self.assertEqual((r["GMT584285_AFTER_DUSK"]["predicted_number"],r["GMT584285_AFTER_DUSK"]["predicted_kiche"]),(7,"TZ’I’"))

    def test_2005_specific_alternative_is_conditional_not_correctness(self):
        got=diagnostic_published_day(date(2005,2,12),7,"TZ’I’")
        self.assertEqual(got["compatible_variants_only_not_selected"],["GMT584285_AFTER_DUSK"])
        self.assertTrue(got["variant_correctness_not_established"])
        self.assertTrue(got["time_of_day_not_inferred"])
        self.assertFalse(got["personality_eligibility"])

    def test_three_reported_2005_days_are_not_three_independent_dates(self):
        for row in DATA["dated_speaker_sequence"]:
            expected=diagnostic_published_day(date.fromisoformat(row["civil_date_from_producer"]),row["day_number"],row["kiche"])
            self.assertEqual(expected["compatible_variants_only_not_selected"],["GMT584285_AFTER_DUSK"])
        self.assertFalse(DATA["sources"][0]["time_of_day_recorded"])
        self.assertFalse(DATA["sources"][0]["producer_date_metadata_independently_verified"])

    def test_2019_8_batz_matches_original_584283_not_alternative(self):
        row=DATA["later_report"]
        self.assertEqual(row["civil_date"],"2019-05-10")
        a=diagnostic_published_day(date.fromisoformat(row["civil_date"]),row["day_number"],row["kiche"])
        self.assertEqual(a["compatible_variants_only_not_selected"],["GMT584283_CIVIL"])
        self.assertFalse(a["source_date_mismatch_under_preexisting_GMT584283_CIVIL"])
        self.assertTrue(DATA["nonpromotable_findings"]["vasquez_2019_GMT584283_date_only_concordant"])

    def test_residual_from_prior_GMT_is_negative_one_for_2005_and_zero_for_2019(self):
        self.assertEqual(residual_from_preexisting_gmt(date(2005,2,12),7,"TZ’I’"),[-1])
        self.assertEqual(residual_from_preexisting_gmt(date(2019,5,10),8,"B’ATZ’"),[0])

    def test_preexisting_tedlock_witnesses_unmodified_and_rechecked(self):
        self.assertEqual(len(TEDLOCK["dated_ethnographic_day_witnesses"]),3)
        for row in TEDLOCK["dated_ethnographic_day_witnesses"]:
            a=diagnostic_published_day(date.fromisoformat(row["civil_gregorian_date"]),row["source_number"],row["correct_GMT_584283_kiche"])
            self.assertEqual(a["compatible_variants_only_not_selected"],["GMT584283_CIVIL"])
        self.assertTrue(DATA["prior_tedlock"]["not_independent_of_self"])

    def test_independent_reporter_and_translator_not_conflated(self):
        sources=DATA["sources"]
        self.assertEqual(len(sources),4)
        self.assertEqual(sources[0]["witness"],"Andres Xiloj")
        self.assertEqual(sources[0]["translator"],"Allen J. Christenson")
        self.assertEqual(sources[1]["published_date"],"2019-05-15")
        self.assertEqual(sources[2]["type"],"journalistic_paraphrase_of_specialist")
        self.assertIn("No paired dated",sources[2]["limitation"])
        self.assertEqual(sources[3]["id"],"TEDLOCKS_2005_COMPANION")
        self.assertEqual(sources[3]["printed_recorded_date_span"],"2005-02-11 through 2005-02-12")
        self.assertFalse(sources[3]["independent_calendar_anchor"])
        self.assertFalse(sources[3]["film_segment_timestamp_verified"])
        self.assertTrue(DATA["nonpromotable_findings"]["xiloj_associated_filming_metadata_may_conflate_multiple_days"])
        self.assertRegex(sources[0]["source_sha256"],r"^[0-9a-f]{64}$")

    def test_fixed_variant_universe_kept_and_null_outputs(self):
        self.assertEqual([i for i,_,_ in VARIANTS],[
          "GMT584283_CIVIL","GMT584283_AFTER_DUSK","GMT584285_CIVIL","GMT584285_AFTER_DUSK"])
        for k in ("actual_human_predictive_validations","production_model_promotions"):
            self.assertEqual(DATA["nonpromotable_findings"][k],0)
        self.assertTrue(DATA["nonpromotable_findings"]["source_comparison_not_human_success"])

    def test_invalid_date_number_and_label_rejected(self):
        for d in ("2005-02-12",datetime(2005,2,12)):
            with self.assertRaises(CalendarScopeError):
                diagnostic_published_day(d,7,"TZ’I’")
        for num in (0,14,True,None):
            with self.subTest(num=num):
                with self.assertRaises(CalendarScopeError):
                    diagnostic_published_day(date(2005,2,12),num,"TZ’I’")
        for sign in ("",None,"TZI","Blue Eagle"):
            with self.subTest(sign=sign):
                with self.assertRaises(CalendarScopeError):
                    diagnostic_published_day(date(2005,2,12),7,sign)

    def test_unfavorable_mutant_may_2019_day_shift_would_not_be_same_report(self):
        correct=diagnostic_published_day(date(2019,5,10),8,"B’ATZ’")
        mutated=diagnostic_published_day(date(2019,5,11),8,"B’ATZ’")
        self.assertEqual(correct["compatible_variants_only_not_selected"],["GMT584283_CIVIL"])
        self.assertNotEqual(mutated["compatible_variants_only_not_selected"],correct["compatible_variants_only_not_selected"])

if __name__=="__main__":
    unittest.main()
