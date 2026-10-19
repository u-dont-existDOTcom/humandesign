"""Lilly original 1647/1659 p711–712 Maginus text and exact rational math."""

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class OriginalMaginusTableUse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = j(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.rules = j(B / "RULES.json")
        cls.photo = cls.data["original_source_photo_four_print_witnesses"]
        cls.records = cls.data["records"]
        cls.rows = cls.data["original_24_years_source_table"]
        cls.examples = cls.data["historical_arithmetic_cases"]

    def test_original_first_source_pdf_sha(self):
        self.assertEqual(
            self.data["source_original_1647_full_PDF_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_four_original_printed_photo_binary_shas(self):
        self.assertEqual(len(self.photo), 4)
        for name, info in self.photo.items():
            f = ROOT / info["file"]
            self.assertTrue(f.is_file(), name)
            self.assertGreater(f.stat().st_size, 200000)
            self.assertEqual(f.stat().st_size, info["bytes"])
            self.assertEqual(sha(f), info["sha256"])

    def test_source_printed_page745_and746_boundary(self):
        self.assertEqual(self.data["original_source_pdf_frames"], [745, 746])
        self.assertEqual(self.data["original_source_partial_folios"], [711, 712])
        self.assertEqual(
            [r["source_pdf_frame_first_1647"] for r in self.records[:8]],
            [745] * 8,
        )
        self.assertEqual(
            [r["source_pdf_frame_first_1647"] for r in self.records[8:]],
            [746] * 23,
        )

    def test_31_partial_rules_no_reused_canonical_ID(self):
        self.assertEqual(self.data["new_historical_annotation_count"], 31)
        self.assertEqual(self.rules["record_count"], 31)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12516, 12547))
        )
        self.assertEqual(self.accept["Lilly_if_accepted"], 12546)
        self.assertEqual(self.accept["next_R"], "R12547")

    def test_solar_rounding_threshold_and_worked_Libra_7(self):
        roles = {r["role"]: r for r in self.records}
        self.assertIn("round_up_strict_over_30", roles)
        self.assertIn("worked_select_7_libra", roles)
        self.assertEqual(
            self.data["original_7_libra_annual_table_rate_arcminutes_arcseconds"],
            [54, 25],
        )
        cross = j(BASE / "B07ah/ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json")
        src = next(
            r
            for r in cross["rows"]
            if r["sign"] == "Libra" and r["original_zodiac_degree_row"] == 7
        )
        self.assertEqual(
            src["literal_original_1647_single_reader_rate_arcminutes_arcseconds"],
            [54, 25],
        )

    def test_source_rounds_54_arcminutes_per_year_after_omitting_seconds(self):
        self.assertEqual(self.data["original_54_arcminutes_per_year_worked_simplification"], 54)
        self.assertNotEqual(Fraction(54), Fraction(54 * 60 + 25, 60))
        self.assertEqual(self.rows[0]["one_reader_original_1647_printed_remaining_arcminute"], 54)

    def test_all_24_years_cumulatively_exact_rate_54(self):
        self.assertEqual(len(self.rows), 24)
        for i, row in enumerate(self.rows, 1):
            self.assertEqual(row["printed_whole_year"], i)
            self.assertEqual(row["analytical_54_times_years_arcminutes"], 54 * i)
            self.assertEqual(
                60 * row["one_reader_original_1647_printed_accumulated_degree"]
                + row["one_reader_original_1647_printed_remaining_arcminute"],
                54 * i,
            )
        self.assertEqual(self.rows[12]["printed_whole_year"], 13)
        self.assertEqual(self.rows[21]["printed_whole_year"], 22)

    def test_source_6_days_18_hours_equals_27_4_days(self):
        self.assertTrue(self.data["original_one_arcminute_expressly_6d18h"])
        self.assertEqual(Fraction(6) + Fraction(18, 24), Fraction(27, 4))
        self.assertEqual(Fraction(54) * Fraction(27, 4), Fraction(729, 2))
        self.assertTrue(self.data["exact_54_arcminutes_times_6d18h_is_364_point_5_days"])

    def test_terms_printed_fraction_not_subtraction_remainder(self):
        case = self.examples[0]
        self.assertEqual(case["target_arc_degrees_minutes"], [11, 55])
        self.assertEqual(case["attained_source_table_degrees_minutes"], [11, 42])
        self.assertEqual(case["whole_years_completed"], 13)
        self.assertEqual(case["original_printed_fraction_arcminutes"], 42)
        self.assertEqual(case["true_arithmetic_remaining_arcminutes"], 13)
        self.assertEqual(Fraction(case["source_printed_fraction_exact_days"]), Fraction(567, 2))
        self.assertEqual(
            Fraction(case["mathematical_target_residual_exact_days"]), Fraction(351, 4)
        )
        self.assertEqual(Fraction(case["difference_exact_nominal_days"]), Fraction(783, 4))

    def test_opposition_printed_fraction_not_subtraction_remainder(self):
        case = self.examples[1]
        self.assertEqual(case["target_arc_degrees_minutes"], [19, 52])
        self.assertEqual(case["attained_source_table_degrees_minutes"], [19, 48])
        self.assertEqual(case["whole_years_completed"], 22)
        self.assertEqual(case["original_printed_fraction_arcminutes"], 48)
        self.assertEqual(case["true_arithmetic_remaining_arcminutes"], 4)
        self.assertEqual(Fraction(case["source_printed_fraction_exact_days"]), Fraction(324))
        self.assertEqual(Fraction(case["mathematical_target_residual_exact_days"]), Fraction(27))
        self.assertEqual(Fraction(case["difference_exact_nominal_days"]), Fraction(297))

    def test_photographic_sources_include_Naibod_intro_not_table_yet(self):
        roles = {r["role"] for r in self.records}
        self.assertIn("naibod_third_method", roles)
        self.assertIn("naibod_when_sufficient_time", roles)
        self.assertIn("ptolemy_shortcut_when_little_time", roles)
        self.assertFalse(self.data["naibod_actual_degree_minute_tables_source_verified"])
        self.assertEqual(self.accept["next_PDF"], 747)

    def test_numeric_historical_print_persistent_two_editions(self):
        self.assertTrue(self.data["1647_vs_1659_print_42_48_and_284_324_correspond"])
        previous = j(BASE / "B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json")
        self.assertEqual(
            [r["source_printed_fraction_used_in_partial_year"] for r in previous["worked_cases"]],
            [42, 48],
        )
        self.assertEqual(
            [r["computed_remaining_arcminutes"] for r in previous["worked_cases"]], [13, 4]
        )

    def test_source_only_not_real_people_or_full_chapter(self):
        self.assertFalse(self.data["full_original_CLXVI_chapter_complete"])
        self.assertFalse(self.data["natal_1647_ascendant_and_true_solar_time_engine_validated"])
        self.assertTrue(self.data["source_first_second_printing_not_independent_human_test"])
        self.assertEqual(self.data["actual_real_person_predictions_validated"], 0)
        self.assertEqual(self.data["runtime_promotions"], 0)

    def test_previous_canonical_indexes_unmutated(self):
        self.assertEqual(j(WEST)["records_count"], 12515)
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(self.data["Lilly_before"], 12515)
        self.assertEqual(self.data["Chinese_V5_retained"], 262)

    def test_source_risk_fields_all_false(self):
        for r in self.records:
            self.assertFalse(r["human_event_time_predictive_accuracy_validated"])
            self.assertFalse(r["high_stakes_prediction_or_personality_advice_permitted"])
            self.assertFalse(r["original_solar_epoch_natal_calculation_validated"])
            self.assertFalse(r["runtime_model_promoted"])
        for row in self.rules["rules"]:
            self.assertFalse(row["runtime_model_promoted"])
            self.assertFalse(row["independent_health_or_death_prediction_validated"])


def one_original_record(n):
    def test(self):
        r = self.records[n]
        rule = self.rules["rules"][n]
        self.assertEqual(r["id"], f"R{12516 + n}")
        self.assertEqual(r["id"], rule["id"])
        self.assertEqual(r["record_number"], 12516 + n)
        self.assertEqual(r["source_pdf_frame_first_1647"], rule["original_pdf_frames"][0])
        self.assertTrue(r["modern_flattened_source_navigator_anchor_not_diplomatic"])
        self.assertFalse(r["runtime_model_promoted"])

    return test


for number in range(31):
    setattr(
        OriginalMaginusTableUse,
        f"test_original_source_note_{number + 1:02d}",
        one_original_record(number),
    )


def one_table_year(n):
    def test(self):
        r = self.rows[n - 1]
        self.assertEqual(r["printed_whole_year"], n)
        self.assertEqual(r["analytical_54_times_years_arcminutes"], n * 54)
        self.assertTrue(r["source_readings_are_not_independent_annual_ephemeris_validations"])

    return test


for year in range(1, 25):
    setattr(OriginalMaginusTableUse, f"test_year_table_{year:02d}", one_table_year(year))


if __name__ == "__main__":
    unittest.main()
