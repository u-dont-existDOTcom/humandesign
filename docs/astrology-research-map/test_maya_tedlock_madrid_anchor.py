#!/usr/bin/env python3
"""Ethnographic source-versus-engine regression; not a test of astrology in humans.

The ground-truth labels below were transcribed from Tedlock's *dated field reports*,
independent of the existing Smithonian-anchored lowland reference formula.
The copyrighted books are NOT required by/embedded in this unit test.
"""
import json
from pathlib import Path
from datetime import date
import unittest
from maya_calendar_reference import reference_calendar_for_date

EVIDENCE = Path(__file__).with_name("MAYA_TEDLOCK_MADRID_SOURCE_WITNESSES_V1.json")
DOC = json.loads(EVIDENCE.read_text(encoding="utf-8"))

# Exact dated field reports from 1992 revised Tedlock printing.
# Book p.108: "June 22, 1975 ... 9 Akabal"; p.100: March 2, 1977
# "4 Ik" and March 15 secretary "4 Tziquin". English short excerpts only.
KNOWN_DATED_FIELD_REPORTS = (
    ("1975-06-22", 108, 9, "AK’B’AL", "AQ’AB’AL", 7, "IMIX’"),
    ("1977-03-02", 100, 4, "IK’", "IQ’", 2, "AJAW"),
    ("1977-03-15", 100, 4, "MEN", "TZ’IKIN", 2, "B’EN"),
)

class TedlockCalendarWitnessTests(unittest.TestCase):
    def test_exact_three_book_report_anchor_cases(self):
        self.assertEqual(len(DOC["dated_ethnographic_day_witnesses"]), 3)
        for r, exp in zip(DOC["dated_ethnographic_day_witnesses"], KNOWN_DATED_FIELD_REPORTS):
            day, page, number, yuc, kiche, badnum, badyuc = exp
            with self.subTest(day=day):
                self.assertEqual((r["civil_gregorian_date"],r["printed_page"],r["source_number"]),
                                 (day,page,number))
                self.assertEqual((r["correct_GMT_584283_yucatec"],r["correct_GMT_584283_kiche"]),
                                 (yuc,kiche))
                self.assertEqual((r["alternative_GMT_584285_number"],r["alternative_GMT_584285_yucatec"]),
                                 (badnum,badyuc))

    def test_ethnographic_observations_match_not_fit_preexisting_formula(self):
        for d, p, num, yuc, kiche, _, _ in KNOWN_DATED_FIELD_REPORTS:
            with self.subTest(day=d):
                out=reference_calendar_for_date(date.fromisoformat(d),correlation=584283)
                self.assertEqual((out["tzolkin_number"],out["tzolkin_yucatec_name"],
                                  out["kiche_label_from_practitioner_crosswalk_only"]), (num,yuc,kiche))
                self.assertEqual(out["status"],"LOWLAND_REFERENCE_CALENDAR_ARITHMETIC_ONLY")

    def test_declared_other_correlation_fails_every_1975_1977_label(self):
        for d, _, num, yuc, _, badnum, badyuc in KNOWN_DATED_FIELD_REPORTS:
            with self.subTest(day=d):
                alternative=reference_calendar_for_date(date.fromisoformat(d),correlation=584285)
                self.assertEqual((alternative["tzolkin_number"],alternative["tzolkin_yucatec_name"]), (badnum,badyuc))
                self.assertNotEqual((alternative["tzolkin_number"],alternative["tzolkin_yucatec_name"]), (num,yuc))

    def test_calendar_1977_field_interval_preserves_number_and_advances_13_names(self):
        a=reference_calendar_for_date(date(1977,3,2))
        b=reference_calendar_for_date(date(1977,3,15))
        self.assertEqual((a["tzolkin_number"],b["tzolkin_number"]),(4,4))
        self.assertEqual((a["tzolkin_yucatec_name"],b["tzolkin_yucatec_name"]),("IK’","MEN"))

    def test_no_source_appears_to_establish_universal_epoch_or_birth_boundary(self):
        claim=DOC["ethnographic_cross_validation"]
        self.assertTrue(claim["one_author_three_dated_mentions_not_three_independent_ethnographers"])
        self.assertTrue(claim["march_1977_pair_related_by_13_day_interval"])
        self.assertIn("NOT full proof",claim["result_scope"])
        a=reference_calendar_for_date(date(1975,6,22))
        self.assertFalse(a["kiche_living_count_epoch_independently_verified"])
        self.assertFalse(a["birth_time_and_local_day_start_handled"])
        self.assertFalse(a["eligible_to_score_a_human"])

    def test_madrid_comparative_borgia_prognosis_not_natal_maya(self):
        by_id={x["id"]:x for x in DOC["source_critical_findings"]}
        self.assertEqual(by_id["MADRID-POHL-BORGIA-MARRIAGE"]["classification"],
                         "distinct_Nahua_Mixtec_elective_marriage_not_Maya_birth_traits")
        self.assertEqual(by_id["MADRID-VAIL-52YR-ALMANAC"]["classification"],
                         "calendar_ritual_yearbearer_not_natal_predictor")
        self.assertEqual(by_id["TEDLOCK-BIRTH-E"]["classification"],
                         "local_natal_role_prediction_not_independent_support_for_Zunil_travel_trait")

    def test_scope_no_new_human_evidence_or_unfrozen_claim_promotion(self):
        self.assertEqual(DOC["human_predictions_tested"],0)
        self.assertEqual(DOC["independently_validated_human_successes"],0)
        self.assertEqual(DOC["runtime_rule_promotions"],0)
        c=DOC["prospective_test_candidate"]
        self.assertEqual(c["candidate_status"],"PRE_REGISTRATION_DRAFT_NOT_ELIGIBLE_TO_SCORE")
        self.assertTrue(c["quantitative_freeze_status"].startswith("NOT_FROZEN"))
        self.assertEqual(c["birth_day_sign"],"NO’J")
        self.assertTrue(DOC["ethnographic_cross_validation"]["no_birthday_user_data_processed"])

    def test_source_bytes_verified_in_laptop_not_stored_in_repository(self):
        books=DOC["source_books"]
        self.assertEqual(len(books),2)
        self.assertTrue(all(b["verified_owner_file_sha256_current_turn"] for b in books))
        self.assertTrue(all(not b["original_source_file_in_repository"] for b in books))
        self.assertTrue(all(not b["fully_read"] for b in books))
        for b in books:self.assertRegex(b["owner_file_sha256"],r"^[0-9a-f]{64}$")

    def test_negative_mutant_shift_and_relabel_get_caught(self):
        for d, _, num, yuc, kiche, _, _ in KNOWN_DATED_FIELD_REPORTS:
            alternate_date=date.fromisoformat(d).toordinal()+1
            perturbed=reference_calendar_for_date(date.fromordinal(alternate_date))
            self.assertNotEqual((perturbed["tzolkin_number"],perturbed["tzolkin_yucatec_name"]), (num,yuc))
            self.assertNotEqual(perturbed["kiche_label_from_practitioner_crosswalk_only"],kiche)

if __name__=="__main__":
    unittest.main()
