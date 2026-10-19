"""Lilly original 1647/1659 CLXXII solar-return interpolation source checks."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class SolarReturnOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json")
        cls.rules = load(B / "RULES.json")
        cls.accept = load(B / "ACCEPTANCE.json")
        cls.example = cls.data["original_1646_literal_versus_computed_arithmetic"]

    def test_full_first_edition_original_1647_identity(self):
        self.assertEqual(
            self.data["original_full_1647_book_PDF_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_exact_four_original_physical_witness_hashes(self):
        photos = self.data["documentary_witness_photos"]
        self.assertEqual(len(photos), 4)
        self.assertEqual(set(x["source_year"] for x in photos.values()), {1647, 1659})
        for key, x in photos.items():
            file = ROOT / x["repository_path"]
            self.assertEqual(sha(file), x["raw_image_SHA256"], key)
            self.assertEqual(file.stat().st_size, x["raw_image_bytes"], key)
            self.assertGreater(file.stat().st_size, 150000)

    def test_24_new_historical_IDs_exact_cursor(self):
        self.assertEqual(self.rules["record_count"], 24)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12765, 12789))
        )
        self.assertEqual(self.rules["first_record"], "R12765")
        self.assertEqual(self.rules["last_record"], "R12788")
        self.assertEqual(self.rules["next_original_record"], "R12789")
        self.assertEqual(self.accept["next_original_PDF"], 770)

    def test_no_completed_CLXXII_original_source_claim(self):
        self.assertFalse(self.data["original_CLXXII_full_source_physical_span_read"])
        self.assertFalse(self.rules["source_full_CLXXII_complete"])
        self.assertFalse(self.accept["full_CLXXII_source_chapter_finished"])

    def test_natal_and_example_noon_positions_distinct(self):
        e = self.example
        self.assertEqual(e["original_natal_longitude_deg_min"], [6, 37])
        self.assertEqual(e["original_ephemeris_noon_deg_min"], [6, 12])
        self.assertEqual(e["remaining_arcminutes"], 25)
        self.assertEqual(e["example_year_written"], 1646)

    def test_daily_rate_differs_nearby_maginus_lookup(self):
        self.assertEqual(self.example["source_sun_daily_motion_arcminute_arcsecond"], [59, 10])
        self.assertEqual(self.example["historical_nearby_table_rate_arcminute_arcsecond"], [59, 8])
        self.assertTrue(self.example["printed_arithmetic_checked_not_actual_1646_sun_ephemeris"])

    def test_fractional_time_source_cells_sum_exact(self):
        x = self.example
        self.assertEqual(x["twenty_arcminute_time_hms"], [8, 7, 2])
        self.assertEqual(x["five_arcminute_time_hms"], [2, 1, 45])
        self.assertEqual(x["source_sum_unrounded_time_hms"], [10, 8, 47])
        self.assertEqual(
            (8 * 3600 + 7 * 60 + 2) + (2 * 3600 + 1 * 60 + 45), 10 * 3600 + 8 * 60 + 47
        )

    def test_full_minute_timing_truncation_not_equivalent_to_rounding(self):
        self.assertEqual(self.example["printed_later_minute_level_time_hm"], [10, 8])
        self.assertTrue(self.data["source_fractional_seconds_truncated_not_exactly_reconciled"])
        self.assertNotEqual(10 * 3600 + 8 * 60 + 47, 10 * 3600 + 8 * 60)

    def test_exact_meridian_correction_used_in_source(self):
        self.assertEqual(self.example["source_westward_meridian_subtract_hm"], [1, 7])
        self.assertEqual(self.example["source_local_time_after_noon_hm"], [9, 1])
        self.assertEqual(10 * 60 + 8 - 67, 9 * 60 + 1)

    def test_historical_noon_53deg_house_and_equation(self):
        self.assertEqual(self.example["house_table_latitude_degrees"], 53)
        self.assertEqual(self.example["house_table_noon_hm"], [12, 26])
        self.assertEqual(self.example["source_equation_of_time_hm"], [0, 16])
        self.assertEqual(self.example["source_house_table_final_hm"], [21, 43])
        self.assertEqual(9 * 60 + 1 + 12 * 60 + 26 + 16, 21 * 60 + 43)

    def test_historic_house_positions_not_persons(self):
        self.assertEqual(self.example["source_MC_zodiac_sign"], "Aquarius")
        self.assertEqual(self.example["source_MC_zodiac_degrees"], 23)
        self.assertEqual(self.example["source_ascendant_sign"], "Cancer")
        self.assertEqual(self.example["source_ascendant_deg_min"], [0, 32])

    def test_prior_Lilly_and_chinese_indexes_unmodified(self):
        self.assertEqual(load(INDEX)["records_count"], 12764)
        self.assertEqual(load(INDEX)["batches"][-1]["id"], "B07as")
        self.assertEqual(load(CHINA)["sum_source_annotations"], 355)

    def test_no_prediction_or_actual_calendar_parity_claim(self):
        self.assertFalse(self.example["calendar_style_independently_confirmed"])
        self.assertFalse(
            self.data["original_Lilly_solar_return_algorithm_ephemeris_correctness_verified"]
        )
        self.assertFalse(
            self.data[
                "solar_return_example_1646_true_birth_hour_calendar_and_meridian_parity_verified"
            ]
        )
        self.assertEqual(self.data["independent_real_life_predictions_validated"], 0)
        self.assertEqual(self.data["runtime_promotions"], 0)

    def test_parent_source_and_rules_immutable_hash(self):
        self.assertEqual(
            self.accept["source_photo_and_arithmetic_SHA256"],
            sha(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))


def one_source_note(index):
    def test(self):
        note = self.data["records"][index]
        rule = self.rules["rules"][index]
        self.assertEqual(note["id"], f"R{12765 + index}")
        self.assertEqual(note["id"], rule["id"])
        self.assertEqual(note["role"], rule["role"])
        self.assertEqual(note["original_pdf_frames"], rule["original_pdf_frames"])
        self.assertFalse(note["runtime_promoted"])
        self.assertFalse(rule["real_person_prediction_validated"])

    return test


for n in range(24):
    setattr(SolarReturnOriginal, f"test_doc_{n + 1:02d}", one_source_note(n))

if __name__ == "__main__":
    unittest.main()
