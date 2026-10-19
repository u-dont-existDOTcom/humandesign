"""Verify Maginus original first edition and separately typeset second edition evidence."""

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

from build_maginus_second_edition_source_comparison import days_per_fractional_arc

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
EXPECTED = [
    ("Mars_terms", [11, 55], 13, [11, 42], 42, 13, 284, Fraction(10585, 54)),
    ("Mars_opposition", [19, 52], 22, [19, 48], 48, 4, 324, Fraction(8030, 27)),
]


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class MaginusOriginalPrint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.info = j(B / "MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json")
        cls.parent = j(B.parent / "B07x/WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json")
        cls.photos = cls.info["source_photos"]
        cls.cases = cls.info["worked_cases"]

    def test_two_source_edition_years(self):
        self.assertEqual(self.info["source_years"], [1647, 1659])

    def test_original_full_1647_pdf_sha(self):
        self.assertEqual(
            self.info["Wellcome_1647_full_original_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_unmutated_western_index(self):
        self.assertEqual(j(WEST)["records_count"], 12472)
        self.assertEqual(self.info["canonical_Lilly_historical_count_retained"], 12472)

    def test_unmutated_chinese_index(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 142)
        self.assertEqual(self.info["Chinese_V3_historical_count_retained"], 142)

    def test_provenance_independent_physical_second_editions(self):
        self.assertEqual(
            set(self.photos),
            {
                "first_edition_1647_printed712_pdf746",
                "second_edition_1659_printed709_djvu738",
                "second_edition_1659_printed710_djvu739",
                "second_edition_1659_printed712_djvu741",
            },
        )
        self.assertIn("1659", self.info["1659_original_printed_djvu_commons_file"])
        self.assertFalse(self.info["independently_blinded_second_human_reader"])

    def test_original_1647_first_edition_actual_page(self):
        a = self.photos["first_edition_1647_printed712_pdf746"]
        self.assertEqual(a["original_pdf_frame"], 746)
        self.assertEqual(a["printed"], 712)
        self.assertEqual(sha(B / a["file"]), a["sha256"])

    def test_1659_second_edition_printed712_actual_page(self):
        a = self.photos["second_edition_1659_printed712_djvu741"]
        self.assertEqual(a["djvu_page"], 741)
        self.assertEqual(a["printed"], 712)
        self.assertEqual(sha(B / a["file"]), a["sha256"])

    def test_1659_original_context_printed709(self):
        a = self.photos["second_edition_1659_printed709_djvu738"]
        self.assertEqual(a["printed"], 709)
        self.assertEqual(sha(B / a["file"]), a["sha256"])

    def test_1659_original_context_printed710(self):
        a = self.photos["second_edition_1659_printed710_djvu739"]
        self.assertEqual(a["printed"], 710)
        self.assertEqual(sha(B / a["file"]), a["sha256"])

    def test_each_archived_scan_jpeg_magic_and_bytes(self):
        for a in self.photos.values():
            raw = (B / a["file"]).read_bytes()
            self.assertGreater(len(raw), 300_000)
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(hashlib.sha256(raw).hexdigest(), a["sha256"])

    def test_two_mag_numbers_both_editions_retained(self):
        self.assertTrue(
            self.info[
                "two_photographic_1659_worked_paragraphs_still_contain_source_numbers_42_and_48"
            ]
        )
        self.assertTrue(
            self.info["neither_edition_corrects_remaining_arc_from_13_or_4_in_the_worked_examples"]
        )
        self.assertEqual(len(self.cases), 2)

    def test_54_minute_annual_rate_not_54_minute25(self):
        for a in self.cases:
            self.assertEqual(a["source_annual_rate_arcminutes"], 54)
        self.assertNotEqual(Fraction(54, 1), Fraction(54 * 60 + 25, 60))

    def test_prev_original_case_document_no_promotions(self):
        self.assertEqual(self.parent["independent_human_life_event_predictions_validated"], 0)
        self.assertEqual(self.parent["runtime_promotions"], 0)

    def test_11_55_target_arithmetic(self):
        a = self.cases[0]
        self.assertEqual(a["1647_and_1659_original_printed_targets"], [11, 55])
        self.assertEqual(a["1647_and_1659_printed_attained_arc"], [11, 42])
        self.assertEqual(a["1647_and_1659_printed_completed_years"], 13)
        self.assertEqual(a["computed_target_arcminutes"] - (a["computed_attained_arcminutes"]), 13)

    def test_19_52_target_arithmetic(self):
        a = self.cases[1]
        self.assertEqual(a["1647_and_1659_original_printed_targets"], [19, 52])
        self.assertEqual(a["1647_and_1659_printed_attained_arc"], [19, 48])
        self.assertEqual(a["1647_and_1659_printed_completed_years"], 22)
        self.assertEqual(a["computed_target_arcminutes"] - (a["computed_attained_arcminutes"]), 4)

    def test_both_original_fraction_minutes_are_attained_not_remaining(self):
        self.assertEqual(
            [a["source_printed_fraction_used_in_partial_year"] for a in self.cases], [42, 48]
        )
        self.assertEqual([a["computed_remaining_arcminutes"] for a in self.cases], [13, 4])
        self.assertTrue(
            all(a["printed_fraction_is_attained_minutes_not_residual"] for a in self.cases)
        )

    def test_printed_284_is_from_42(self):
        self.assertEqual(days_per_fractional_arc(42), Fraction(5110, 18))
        self.assertLessEqual(abs(days_per_fractional_arc(42) - 284), Fraction(1, 2))
        self.assertEqual(days_per_fractional_arc(13), Fraction(4745, 54))

    def test_printed_324_is_from_48(self):
        self.assertEqual(days_per_fractional_arc(48), Fraction(2920, 9))
        self.assertLessEqual(abs(days_per_fractional_arc(48) - 324), Fraction(1, 2))
        self.assertEqual(days_per_fractional_arc(4), Fraction(730, 27))

    def test_discrepancy_days_first_case(self):
        self.assertEqual(
            Fraction(self.cases[0]["difference_in_365_day_nominal_days"]), Fraction(10585, 54)
        )

    def test_discrepancy_days_second_case(self):
        self.assertEqual(
            Fraction(self.cases[1]["difference_in_365_day_nominal_days"]), Fraction(8030, 27)
        )

    def test_365_nominal_is_not_civil_calendar_prediction(self):
        self.assertEqual(self.info["source_year_roughly_365_day_historical_example"], 365)
        self.assertTrue(
            self.info["historic_source_format_not_independent_human_forecast_validation"]
        )

    def test_original_context_names_three_distinct_conventions(self):
        self.assertEqual(len(self.info["distinct_period_methods"]), 3)
        self.assertTrue(any("Maginus" in s for s in self.info["distinct_period_methods"]))
        self.assertTrue(any("Naibod" in s for s in self.info["distinct_period_methods"]))
        self.assertTrue(any("Ptolemy" in s for s in self.info["distinct_period_methods"]))

    def test_fail_closed_negative_fraction(self):
        for a, b in ((-1, 54), (54, 0), (54, -1), (True, 54)):
            with self.assertRaises(ValueError):
                days_per_fractional_arc(a, b)

    def test_no_renaissance_astro_engine_parity(self):
        self.assertFalse(self.info["original_method_a_natal_chart_era_engine_verified"])
        self.assertEqual(self.info["independent_real_human_prediction_validations"], 0)
        self.assertEqual(self.info["runtime_promotions"], 0)


def original_case_test(i, expected):
    def test(self):
        name, target, years, attained, part, remaining, days, delta = expected
        a = self.cases[i]
        self.assertEqual(a["historical_example"], name)
        self.assertEqual(a["1647_and_1659_original_printed_targets"], target)
        self.assertEqual(a["1647_and_1659_printed_completed_years"], years)
        self.assertEqual(a["1647_and_1659_printed_attained_arc"], attained)
        self.assertEqual(a["source_printed_fraction_used_in_partial_year"], part)
        self.assertEqual(a["computed_remaining_arcminutes"], remaining)
        self.assertEqual(a["source_printed_partial_year_days"], days)
        self.assertEqual(Fraction(a["difference_in_365_day_nominal_days"]), delta)
        self.assertTrue(a["source_only_no_human_events"])

    return test


for i, item in enumerate(EXPECTED):
    setattr(MaginusOriginalPrint, f"test_case_{i + 1}", original_case_test(i, item))


if __name__ == "__main__":
    unittest.main()
