#!/usr/bin/env python3
"""Scholarly astronomy / ritual almanac dates: model parity, not human validation."""
import json
from datetime import date, timedelta
from pathlib import Path
import unittest
from maya_calendar_reference import reference_calendar_for_date

ROOT=Path(__file__).parent
EVIDENCE=json.loads((ROOT/"MAYA_MADRID_CH6_CH7_READING_AND_DATE_PARITY_B03.json").read_text(encoding="utf-8"))

class MadridChapter6Chapter7Witnesses(unittest.TestCase):
    def test_scholarly_date_examples_are_seven_unique_sourced_claims(self):
        records=EVIDENCE["published_scholar_calendar_examples"]
        self.assertEqual(len(records),7)
        self.assertEqual(len({r["id"] for r in records}),7)
        self.assertTrue(all(r["source_printed_page"] in range(147,215) for r in records))
        self.assertTrue(all("origin" in r and r["origin"] for r in records))

    def test_source_date_models_match_independent_reference_formula(self):
        for r in EVIDENCE["published_scholar_calendar_examples"]:
            with self.subTest(source_date=r["id"]):
                out=reference_calendar_for_date(date.fromisoformat(r["gregorian"]),correlation=584283)
                self.assertEqual(out["tzolkin_number"],r["source_reported_number"])
                self.assertEqual(out["tzolkin_yucatec_name"],r["source_reported_yucatec"])
                if r["source_haab_day"] is None:
                    self.assertIsNone(r["source_haab_month"])
                else:
                    self.assertEqual((out["haab_day"],out["haab_month"]),
                         (r["source_haab_day"],r["source_haab_month"]))

    def test_GMT584285_alternative_not_silently_promoted(self):
        for r in EVIDENCE["published_scholar_calendar_examples"]:
            with self.subTest(source_date=r["id"]):
                out=reference_calendar_for_date(date.fromisoformat(r["gregorian"]),correlation=584285)
                self.assertNotEqual((out["tzolkin_number"],out["tzolkin_yucatec_name"]),
                                    (r["source_reported_number"],r["source_reported_yucatec"]))

    def test_Mayapan_classic_month_label_difference_not_sacred_date_shift(self):
        records=[r for r in EVIDENCE["published_scholar_calendar_examples"] if "mayapan_same_date_haab_day" in r]
        self.assertEqual(len(records),2)
        self.assertEqual({r["gregorian"] for r in records},{"0924-08-09","0924-10-26"})
        for r in records:
            self.assertEqual(r["source_haab_day"]-r["mayapan_same_date_haab_day"],1)
            actual=reference_calendar_for_date(date.fromisoformat(r["gregorian"]))
            self.assertEqual((actual["tzolkin_number"],actual["tzolkin_yucatec_name"]),
                             (r["source_reported_number"],r["source_reported_yucatec"]))

    def test_Madrid_73b_calendar_round_date_one_day_mutant_fails(self):
        record=[r for r in EVIDENCE["published_scholar_calendar_examples"]
               if r["id"]=="VAIL_M73B_1451"][0]
        good=reference_calendar_for_date(date(1451,8,5))
        bad=reference_calendar_for_date(date(1451,8,6))
        expected=(record["source_reported_number"],record["source_reported_yucatec"],
                  record["source_haab_day"],record["source_haab_month"])
        keys=("tzolkin_number","tzolkin_yucatec_name","haab_day","haab_month")
        self.assertEqual(tuple(good[k] for k in keys),expected)
        self.assertNotEqual(tuple(bad[k] for k in keys),expected)

    def test_no_borrowed_natal_personality_numerology(self):
        self.assertTrue(EVIDENCE["statistical_evidence"]["source_date_computations_are_correlation_dependent"])
        self.assertTrue(EVIDENCE["statistical_evidence"]["scholarly_generated_dates_not_independent_oracle"])
        self.assertEqual(EVIDENCE["statistical_evidence"]["untouched_human_natal_predictions"],0)
        self.assertEqual(EVIDENCE["statistical_evidence"]["human_validation_effects"],0)
        self.assertEqual(EVIDENCE["statistical_evidence"]["original_glyph_folio_personality_decipherments_added"],0)
        self.assertTrue(any("Do not count 15 almanac pairs" in x for x in EVIDENCE["guardrails"]))

    def test_original_book_copyright_remains_separate(self):
        source=EVIDENCE["source"]
        self.assertRegex(source["owner_held_pdf_sha256"],r"^[0-9a-f]{64}$")
        self.assertFalse(source["original_book_text_or_images_redistributed"])
        self.assertEqual(source["publication_year"],2004)
        self.assertTrue(EVIDENCE["methodological_points"])

if __name__=="__main__":
    unittest.main()
