"""Unverified 372-cell annual direction-rate table protects original sign mapping.

Only twelve distinct original photographed original 1647 cells have direct
visual checks. This does NOT admit the other 360 candidate values for runtime.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
GOLDEN = {
    "Aries": (54, 26),
    "Taurus": (55, 40),
    "Gemini": (59, 52),
    "Cancer": (62, 18),
    "Virgo": (55, 16),
    "Libra": (54, 4),
    "Scorpio": (57, 24),
    "Sagittarius": (63, 32),
    "Capricorn": (66, 53),
    "Aquarius": (66, 33),
    "Pisces": (57, 35),
}
EXPECTED_BLOCKS = {
    "Aries": 9,
    "Taurus": 0,
    "Gemini": 1,
    "Cancer": 2,
    "Leo": 3,
    "Virgo": 4,
    "Libra": 10,
    "Scorpio": 5,
    "Sagittarius": 6,
    "Capricorn": 7,
    "Aquarius": 8,
    "Pisces": 11,
}


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class AnnualTableSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = j(B / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
        cls.window = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.cases = j(B / "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json")
        cls.rows = {(r["sign"], r["zodiac_degree"]): r for r in cls.d["tentative_candidate_pairs"]}

    def test_372_source_cell_locations(self):
        self.assertEqual(self.d["source_cells_expected"], 372)
        self.assertEqual(len(self.rows), 372)
        self.assertEqual(self.d["original_printed_degrees_inclusive"], [0, 30])
        self.assertEqual(self.d["printed_zodiac_signs"], 12)

    def test_source_photo_sha_matches_1647_witness(self):
        file = B / self.window["photos"]["745"]["file"]
        self.assertEqual(sha(file), self.d["source_photo_sha256"])

    def test_zodiac_original_to_derivative_block_mapping(self):
        self.assertEqual(self.d["sign_to_flattened_block"], EXPECTED_BLOCKS)
        self.assertEqual(len(set(EXPECTED_BLOCKS.values())), 12)
        self.assertTrue(self.d["derivative_flattened_order_bug"])

    def test_all_31_degree_positions_in_each_sign(self):
        for sign in EXPECTED_BLOCKS:
            self.assertEqual(
                [
                    r["zodiac_degree"]
                    for r in self.d["tentative_candidate_pairs"]
                    if r["sign"] == sign
                ],
                list(range(31)),
            )

    def test_each_cell_preserves_origin_block(self):
        for r in self.d["tentative_candidate_pairs"]:
            self.assertEqual(r["secondary_text_block_zero_based"], EXPECTED_BLOCKS[r["sign"]])

    def test_original_photo_checked_count_is_not_exaggerated(self):
        self.assertEqual(self.d["direct_original_photo_confirmed"], 12)
        self.assertEqual(self.d["cells_without_direct_photo_check"], 360)
        self.assertEqual(
            sum(r["verified_direct_first_edition_photo"] for r in self.rows.values()), 12
        )

    def test_libra_7_the_historical_printed_example(self):
        row = self.rows["Libra", 7]
        self.assertEqual(
            (
                row["candidate_original_annual_equator_rate_minutes"],
                row["candidate_original_annual_equator_rate_seconds"],
            ),
            (54, 25),
        )
        self.assertTrue(row["verified_direct_first_edition_photo"])
        self.assertEqual(self.cases["source_statements"][5]["original_numeric"]["minutes"], 54)
        self.assertEqual(self.cases["source_statements"][5]["original_numeric"]["seconds"], 25)

    def test_naive_block_6_would_get_wrong_libra(self):
        self.assertEqual(self.rows["Sagittarius", 7]["secondary_text_block_zero_based"], 6)
        wrong = self.rows["Sagittarius", 7]
        self.assertEqual(
            (
                wrong["candidate_original_annual_equator_rate_minutes"],
                wrong["candidate_original_annual_equator_rate_seconds"],
            ),
            (64, 47),
        )
        self.assertNotEqual((64, 47), (54, 25))

    def test_minutes_above_60_are_valid_raw_equatorial_arcminutes(self):
        self.assertTrue(self.d["rates_are_scalar_equatorial_arcminutes_up_to_around_66"])
        self.assertEqual(
            self.rows["Capricorn", 0]["candidate_original_annual_equator_rate_minutes"], 66
        )
        self.assertNotIn(
            "MINUTES_GE_60_REQUIRE_SEXAGESIMAL_INTERPRETATION",
            self.rows["Capricorn", 0]["source_flags"],
        )

    def test_Leo_zero_conflicting_original_glyph_not_autocorrected(self):
        r = self.rows["Leo", 0]
        self.assertEqual(
            (
                r["candidate_original_annual_equator_rate_minutes"],
                r["candidate_original_annual_equator_rate_seconds"],
            ),
            (59, 24),
        )
        self.assertFalse(r["verified_direct_first_edition_photo"])
        self.assertEqual(r["original_photo_glyph_alternative_unresolved"], [59, 34])
        self.assertIn(
            "SOURCE_GLYPH_CANDIDATE_59_34_DIFFERS_FROM_DERIVATIVE_59_24", r["source_flags"]
        )

    def test_critical_gap_candidates_do_not_become_validated(self):
        for sign, degree in (
            ("Libra", 22),
            ("Capricorn", 13),
            ("Capricorn", 14),
            ("Aquarius", 1),
            ("Aquarius", 4),
        ):
            r = self.rows[sign, degree]
            self.assertFalse(r["verified_direct_first_edition_photo"])
            self.assertTrue(r["source_flags"])

    def test_every_source_note_in_model_is_unpromoted(self):
        for row in self.rows.values():
            self.assertFalse(row["actual_human_prediction_validated"])
            self.assertFalse(row["runtime_promoted"])
            self.assertFalse(row["corrected_from_source_by_arithmetic"])

    def test_no_360_unchecked_cells_are_called_original_evidence(self):
        for r in self.rows.values():
            if not r["verified_direct_first_edition_photo"]:
                self.assertNotEqual(r["transcription_status"], "SELECTED_ORIGINAL_PHOTO_CHECKED")

    def test_annual_rate_not_full_verified_original(self):
        self.assertFalse(self.d["complete_1647_photo_table_transcription"])
        self.assertFalse(self.d["true_1647_epoch_vs_modern_ra_parity_verified"])
        self.assertEqual(self.d["runtime_promotions"], 0)
        self.assertEqual(self.d["independent_human_events_validated"], 0)

    def test_derived_372_values_remain_reversible(self):
        for row in self.rows.values():
            sign = row["sign"]
            self.assertIn(sign, self.d["sign_to_flattened_block"])
            self.assertEqual(
                row["secondary_text_block_zero_based"],
                self.d["sign_to_flattened_block"][sign],
            )

    def test_suspicious_rate_cases_remain_flagged(self):
        self.assertGreaterEqual(len(self.d["source_flags_summary"]), 10)
        self.assertLessEqual(len(self.d["source_flags_summary"]), 30)

    def test_sample_scorer_cannot_be_called_verified(self):
        self.assertNotIn("calibrated_probability", self.d)
        self.assertFalse(self.cases["original_1647_source_technical_epoch_chart_input_validated"])


def individual_source_sign_test(sign, expected):
    def test(self):
        row = self.rows[sign, 0]
        self.assertTrue(row["verified_direct_first_edition_photo"])
        self.assertEqual(
            (
                row["candidate_original_annual_equator_rate_minutes"],
                row["candidate_original_annual_equator_rate_seconds"],
            ),
            expected,
        )

    return test


for sign, expected in GOLDEN.items():
    setattr(
        AnnualTableSource,
        f"test_first_edition_row_zero_{sign.lower()}",
        individual_source_sign_test(sign, expected),
    )


if __name__ == "__main__":
    unittest.main()
