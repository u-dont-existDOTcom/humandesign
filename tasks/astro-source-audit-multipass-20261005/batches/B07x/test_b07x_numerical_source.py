"""Focused original CLXVI numerical-method source and exact arithmetic tests."""

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

from lilly_1647_direction_time_mechanics import (
    Angle,
    OldTabularTime,
    annual_rate_division,
    difference,
    fraction_of_year_of_remainder,
    naibod_recombine,
    ptolemy_360_days,
    source_demo_cases,
)

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class OldLillyNumericalMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.source = j(B / "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json")
        previous = B / "recovery" / "INDEX_BEFORE_B07x.json"
        cls.index_path = previous if previous.exists() else INDEX
        cls.idx = j(cls.index_path)
        cls.demo = source_demo_cases()

    def test_index_unchanged(self):
        self.assertEqual(self.idx["records_count"], 12472)
        self.assertEqual(self.idx["batches"][-1]["id"], "B07w")
        self.assertEqual(self.idx["next"]["chapter"], "CLXVI")
        self.assertEqual(sha(self.index_path), self.window["source_index_parent_sha256"])

    def test_first_edition_source_hash(self):
        self.assertEqual(
            self.window["full_source_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_source_seam_and_repeated_numeral(self):
        self.assertEqual(self.window["starts_pdf"], 742)
        self.assertEqual(self.window["ends_pdf"], 749)
        self.assertEqual(self.window["following_heading_starts_pdf"], 749)
        self.assertTrue(self.window["following_heading_is_duplicate_printed_numeral"])
        self.assertEqual(self.window["following_heading_printed_numeral"], "CLXVI")
        self.assertEqual(self.window["following_CLXVII_starts_pdf"], 752)

    def test_exact_solar_ascendant_values(self):
        self.assertEqual(difference(Angle(324, 5), Angle(312, 10)), Angle(11, 55))
        self.assertEqual(difference(Angle(332, 2), Angle(312, 10)), Angle(19, 52))

    def test_ptolemy_360_day_result_terms(self):
        self.assertEqual(ptolemy_360_days(Angle(11, 55)), (11, 11, 0))

    def test_ptolemy_360_day_result_opposition(self):
        self.assertEqual(ptolemy_360_days(Angle(19, 52)), (19, 10, 12))

    def test_ptolemy_not_real_gregorian_dates(self):
        self.assertTrue(self.demo["not_validated_astronomy_or_birth_chart"])
        self.assertTrue(self.demo["not_a_real_human_forecast"])

    def test_maginus_natal_sun_ra_difference(self):
        self.assertEqual(difference(Angle(186, 58), Angle(186, 4)), Angle(0, 54))

    def test_maginus_terms_integer_years_and_residual(self):
        self.assertEqual(annual_rate_division(Angle(11, 55), Angle(0, 54)), (13, Angle(0, 13)))

    def test_maginus_opposition_integer_years_and_residual(self):
        self.assertEqual(annual_rate_division(Angle(19, 52), Angle(0, 54)), (22, Angle(0, 4)))

    def test_maginus_original_first_partial_is_not_residual(self):
        row = self.source["source_statements"][6]["original_numeric"]
        self.assertEqual(row["achieved_arc"], [11, 42])
        self.assertEqual(row["target_arc"], [11, 55])
        self.assertEqual(row["printed_partial_minutes_used"], 42)
        self.assertEqual(row["reconstructed_remaining_minutes"], 13)
        self.assertNotEqual(42, 13)

    def test_maginus_original_second_partial_is_not_residual(self):
        row = self.source["source_statements"][7]["original_numeric"]
        self.assertEqual(row["achieved_arc"], [19, 48])
        self.assertEqual(row["target_arc"], [19, 52])
        self.assertEqual(row["printed_partial_minutes_used"], 48)
        self.assertEqual(row["reconstructed_remaining_minutes"], 4)

    def test_maginus_exact_fractional_year_first(self):
        self.assertEqual(
            fraction_of_year_of_remainder(Angle(0, 13), Angle(0, 54)), Fraction(13, 54)
        )

    def test_maginus_exact_fractional_year_second(self):
        self.assertEqual(fraction_of_year_of_remainder(Angle(0, 4), Angle(0, 54)), Fraction(2, 27))

    def test_annual_table_seven_libra_cell(self):
        s = self.source["source_statements"][5]["original_numeric"]
        self.assertEqual((s["rounded_lookup_degree"], s["minutes"], s["seconds"]), (7, 54, 25))

    def test_annual_table_vs_sun_ra_rounded_variation(self):
        self.assertNotEqual(Angle(0, 54), Angle(0, 54, 25))
        self.assertEqual(
            annual_rate_division(Angle(19, 52), Angle(0, 54, 25)), (21, Angle(0, 49, 15))
        )
        self.assertEqual(
            annual_rate_division(Angle(11, 55), Angle(0, 54, 25)), (13, Angle(0, 7, 35))
        )

    def test_original_naibod_degree_table_rows(self):
        r = self.source["source_statements"][8]["original_numeric"]
        self.assertEqual(r["one_degree_year_day_hour"], [1, 5, 8])
        self.assertEqual(r["11_degrees_year_day_hour"], [11, 58, 21])
        self.assertEqual(r["19_degrees_year_day_hour"], [19, 101, 17])

    def test_original_naibod_minutes_table_rows(self):
        r = self.source["source_statements"][9]["original_numeric"]
        self.assertEqual(r["55_minutes_days_hours"], [339, 17])
        self.assertEqual(r["52_minutes_days_hours"], [321, 4])

    def test_naibod_first_original_worked_age(self):
        self.assertEqual(
            naibod_recombine(OldTabularTime(11, 58, 21), OldTabularTime(0, 339, 17)),
            OldTabularTime(12, 33, 14),
        )

    def test_naibod_second_original_worked_age(self):
        self.assertEqual(
            naibod_recombine(OldTabularTime(19, 101, 17), OldTabularTime(0, 321, 4)),
            OldTabularTime(20, 57, 21),
        )

    def test_naibod_hour_carry_is_not_lost(self):
        self.assertEqual(
            naibod_recombine(OldTabularTime(0, 364, 23), OldTabularTime(0, 0, 2)),
            OldTabularTime(1, 0, 1),
        )

    def test_naibod_not_using_360_for_year_carry(self):
        with self.assertRaises(ValueError):
            naibod_recombine(OldTabularTime(1, 58, 21), OldTabularTime(0, 339, 17), year_days=360)

    def test_explicit_nonvalid_inputs(self):
        for args in ((0, 60, 0), (361, 0, 0), (-1, 0, 0), (360, 0, 1), (0, -1, 0)):
            with self.assertRaises(ValueError):
                Angle(*args)

    def test_no_implicit_direction_winding(self):
        with self.assertRaises(ValueError):
            difference(Angle(1), Angle(360))

    def test_zero_annual_rate_rejected(self):
        with self.assertRaises(ValueError):
            annual_rate_division(Angle(11), Angle(0))
        with self.assertRaises(ValueError):
            fraction_of_year_of_remainder(Angle(0, 1), Angle(0))

    def test_bad_old_tabular_time_rejected(self):
        with self.assertRaises(ValueError):
            OldTabularTime(1, -1, 3)
        with self.assertRaises(ValueError):
            OldTabularTime(True, 2, 4)

    def test_source_12_witness_propositions(self):
        self.assertEqual(len(self.source["source_statements"]), 12)
        for row in self.source["source_statements"]:
            self.assertIn(row["photo"], range(742, 750))
            self.assertGreaterEqual(len(row["anchor"]), 12)
            self.assertIn("status", row)

    def test_completeness_not_implicitly_claimed(self):
        self.assertEqual(self.source["annual_measure_cells_visually_verified"], 1)
        self.assertEqual(self.source["first_edition_annual_measure_table_cells_expected"], 372)
        self.assertFalse(self.source["all_original_numerical_table_cells_collated"])

    def test_old_tables_need_followup(self):
        self.assertEqual(self.source["naibod_degree_table_rows_expected"], 90)
        self.assertEqual(self.source["naibod_minute_table_rows_expected"], 60)
        self.assertTrue(
            self.source["anomalous_first_edition_examples_need_secondary_edition_comparison"]
        )

    def test_no_human_prediction_or_promotion(self):
        self.assertEqual(self.source["independent_human_life_event_predictions_validated"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)
        self.assertFalse(self.source["original_1647_source_technical_epoch_chart_input_validated"])

    def test_chinese_not_conflated(self):
        self.assertEqual(self.window["Chinese_v2_records_unchanged"], 97)
        self.assertEqual(self.window["ptolemy_records_unchanged"], 1066)


def make_photo_test(page):
    def test(self):
        row = self.window["photos"][str(page)]
        pic = B / row["file"]
        self.assertTrue(pic.is_file())
        self.assertEqual(sha(pic), row["sha256"])
        self.assertEqual(pic.stat().st_size, row["bytes"])
        self.assertEqual(pic.read_bytes()[:2], bytes.fromhex("ffd8"))

    return test


for page in range(742, 751):
    setattr(OldLillyNumericalMethods, f"test_image_{page}", make_photo_test(page))


if __name__ == "__main__":
    unittest.main()
