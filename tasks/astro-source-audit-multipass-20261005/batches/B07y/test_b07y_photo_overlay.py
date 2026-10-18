"""B07y first-edition 1647 annual rate photographic adjudication — source only.

Tests establish provenance and reproducible recording of a one-reader manual
visual check. They do not independently read glyphs or prove astrological math.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT = B.parent / "B07x"
ROOT = B.parents[3]
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
PRIMARY_PAIRS = {
    ("Leo", 0): (59, 34),
    ("Capricorn", 13): (66, 10),
    ("Aquarius", 0): (63, 33),
    ("Aquarius", 3): (62, 57),
    ("Pisces", 6): (56, 37),
}
PRINTED_ANOMALIES = {
    ("Libra", 22): (56, 32),
    ("Pisces", 5): (56, 6),
    ("Pisces", 22): (54, 0),
}
AMBIGUOUS = {("Capricorn", 15), ("Pisces", 24)}


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


class OriginalFirstEditionPhotoAdjudication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j(B / "PHOTO_ADJUDICATION_1647_V1.json")
        cls.overlay = j(B / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json")
        cls.inherited = j(PARENT / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
        cls.rows = {(r["sign"], r["degree"]): r for r in cls.overlay["rows"]}
        cls.original = {
            (r["sign"], r["zodiac_degree"]): r for r in cls.inherited["tentative_candidate_pairs"]
        }
        cls.review = {(r["sign"], r["degree"]): r for r in cls.a["photo_readings"]}

    def test_prior_original_source_pdf_sha(self):
        self.assertEqual(
            self.a["original_source"]["original_894_frame_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_first_edition_photo_binary_sha(self):
        pic = B / self.a["original_source"]["archived_3500_image"]
        self.assertEqual(sha(pic), self.a["original_source"]["source_3500_sha256"])
        self.assertGreater(pic.stat().st_size, 2_000_000)

    def test_separately_typeset_1659_image_sha(self):
        file = B / self.a["comparator_source"]["photo_file"]
        self.assertEqual(sha(file), self.a["comparator_source"]["photo_sha256"])
        self.assertGreater(file.stat().st_size, 200_000)
        self.assertEqual(self.a["comparator_source"]["page_number_in_djvu"], 740)

    def test_derivative_parent_source_unchanged(self):
        self.assertEqual(
            sha(PARENT / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"),
            self.overlay["inherited_previous_derivative_candidate_sha256"],
        )
        self.assertTrue(self.overlay["original_source_legacy_B07x_untouched"])

    def test_full_pair_location_coverage(self):
        self.assertEqual(len(self.overlay["rows"]), 372)
        self.assertEqual(len(self.rows), 372)
        self.assertEqual(set(self.rows), set(self.original))
        self.assertEqual(len(self.inherited["tentative_candidate_pairs"]), 372)

    def test_all_original_derivative_candidates_retained(self):
        for key, r in self.rows.items():
            p = self.original[key]
            self.assertEqual(
                r["B07x_derivative_candidate_as_originally_retained"],
                [
                    p["candidate_original_annual_equator_rate_minutes"],
                    p["candidate_original_annual_equator_rate_seconds"],
                ],
            )

    def test_24_manually_reviewed_provisional_values(self):
        self.assertEqual(len(self.review), 24)
        self.assertEqual(self.a["total_manual_review_positions"], 24)
        self.assertEqual(self.overlay["B07y_current_manually_reviewed_positions"], 24)
        self.assertEqual(self.overlay["B07y_confirmed_1647_one_reader_positions"], 22)
        self.assertEqual(self.overlay["B07y_ambiguous_glyph_positions"], 2)
        self.assertEqual(self.overlay["B07y_positions_not_directly_read_in_this_batch"], 348)

    def test_1647_corrective_differences_set_exactly_five(self):
        diff = {
            key
            for key, r in self.rows.items()
            if r["B07y_manual_1647_source_photo_read"] is not None
            and r["B07y_manual_1647_source_photo_read"]
            != r["B07x_derivative_candidate_as_originally_retained"]
        }
        self.assertEqual(diff, set(PRIMARY_PAIRS))
        self.assertEqual(self.overlay["B07y_conflicts_with_derivative_candidates"], 5)

    def test_leo_zero_source_vs_derivative(self):
        r = self.rows["Leo", 0]
        self.assertEqual(r["B07x_derivative_candidate_as_originally_retained"], [59, 24])
        self.assertEqual(r["B07y_manual_1647_source_photo_read"], [59, 34])

    def test_capricorn_13_source_vs_derivative(self):
        r = self.rows["Capricorn", 13]
        self.assertEqual(r["B07x_derivative_candidate_as_originally_retained"], [60, 10])
        self.assertEqual(r["B07y_manual_1647_source_photo_read"], [66, 10])

    def test_aquarius_0_previous_photo_claim_was_false(self):
        r = self.rows["Aquarius", 0]
        self.assertTrue(r["B07x_claimed_original_photo_match"])
        self.assertEqual(r["B07x_derivative_candidate_as_originally_retained"], [66, 33])
        self.assertEqual(r["B07y_manual_1647_source_photo_read"], [63, 33])
        self.assertEqual(r["B07y_review_status"], "DIFFERS_FROM_PRIOR_PHOTO_ATTESTATION")

    def test_aquarius_3_source_vs_derivative(self):
        r = self.rows["Aquarius", 3]
        self.assertEqual(r["B07x_derivative_candidate_as_originally_retained"], [63, 57])
        self.assertEqual(r["B07y_manual_1647_source_photo_read"], [62, 57])

    def test_pisces_6_source_vs_derivative(self):
        r = self.rows["Pisces", 6]
        self.assertEqual(r["B07x_derivative_candidate_as_originally_retained"], [56, 17])
        self.assertEqual(r["B07y_manual_1647_source_photo_read"], [56, 37])

    def test_three_printed_irregularities_not_math_corrected(self):
        for key, pair in PRINTED_ANOMALIES.items():
            r = self.rows[key]
            self.assertEqual(r["B07y_manual_1647_source_photo_read"], list(pair))
            self.assertEqual(r["B07x_derivative_candidate_as_originally_retained"], list(pair))
            self.assertIn(
                r["B07y_review_status"],
                ("PERSISTENT_PRINTED_ANOMALY", "SUSPECT_PRINTED_DISCONTINUITY"),
            )

    def test_two_glyph_ambiguities_have_no_assumed_source_value(self):
        self.assertEqual(
            {key for key, r in self.rows.items() if r["B07y_manual_original_glyph_alternatives"]},
            AMBIGUOUS,
        )
        for key in AMBIGUOUS:
            self.assertIsNone(self.rows[key]["B07y_manual_1647_source_photo_read"])
            self.assertFalse(self.rows[key]["B07y_source_verified_by_one_reader"])
        self.assertEqual(
            self.rows["Capricorn", 15]["B07y_manual_original_glyph_alternatives"],
            [[65, 57], [66, 2]],
        )
        self.assertEqual(
            self.rows["Pisces", 24]["B07y_manual_original_glyph_alternatives"], [[53, 43], [54, 43]]
        )

    def test_every_new_photo_read_is_anchored_to_one_original_frame(self):
        for row in self.a["photo_readings"]:
            self.assertEqual(row["source_page"], "PDF745/printed711")
            self.assertEqual(row["source_edit_applied_to_earlier_batch"], False)
            self.assertFalse(row["historical_performance_prediction_validated"])
            self.assertFalse(row["runtime_rule_promoted"])

    def test_no_auto_fill_other_348_rows(self):
        unreviewed = [
            r
            for r in self.rows.values()
            if r["B07y_review_status"] == "NO_NEW_DIRECT_PHOTO_ADJUDICATION"
        ]
        self.assertEqual(len(unreviewed), 348)
        for r in unreviewed:
            self.assertIsNone(r["B07y_manual_1647_source_photo_read"])
            self.assertFalse(r["B07y_source_verified_by_one_reader"])

    def test_second_edition_not_exaggerated(self):
        self.assertFalse(self.a["independent_second_reader_verified"])
        self.assertEqual(
            self.a["comparator_source"]["comparison_status"],
            "SECOND_EDITION_AUXILIARY_REFERENCE_NOT_FULLY_GLYPH_COLLATED",
        )

    def test_canonical_western_unmodified(self):
        self.assertEqual(j(WESTERN)["records_count"], 12472)
        self.assertEqual(j(WESTERN)["batches"][-1]["id"], "B07w")
        self.assertEqual(self.overlay["separate_western_Lilly_accepted_before_and_after"], 12472)

    def test_canonical_chinese_V3_unmodified(self):
        self.assertEqual(j(CHINESE)["sum_source_annotations"], 142)
        self.assertEqual(self.overlay["separate_chinese_V3_source_notes_retained"], 142)

    def test_all_372_source_values_not_person_forecasts(self):
        for r in self.rows.values():
            self.assertFalse(r["source_value_may_be_used_as_mathematical_truth"])
            self.assertFalse(r["source_value_may_be_used_in_person_forecasts"])
            self.assertFalse(r["source_fidelity_independently_expert_verified"])
            self.assertFalse(r["source_year_and_astrological_calendar_verified"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_no_human_validation_from_historical_text(self):
        self.assertEqual(self.overlay["actual_human_predictions_validated"], 0)
        self.assertEqual(self.overlay["runtime_promotions"], 0)
        self.assertFalse(self.a["full_1647_372_cells_verified"])
        self.assertEqual(self.a["human_prediction_validations"], 0)

    def test_inherited_b07x_photo_claims_not_auto_expert_verified(self):
        historical = [r for r in self.rows.values() if r["B07x_claimed_original_photo_match"]]
        self.assertEqual(len(historical), 12)
        self.assertTrue(
            any(
                r["B07y_review_status"] == "DIFFERS_FROM_PRIOR_PHOTO_ATTESTATION"
                for r in historical
            )
        )
        self.assertFalse(all(r["B07y_source_verified_by_one_reader"] for r in historical))


def one_read_test(key, expected):
    def test(self):
        r = self.rows[key]
        self.assertEqual(tuple(r["B07y_manual_1647_source_photo_read"]), expected)
        self.assertTrue(r["B07y_source_verified_by_one_reader"])
        self.assertFalse(r["source_value_may_be_used_as_mathematical_truth"])

    return test


for key, pair in PRIMARY_PAIRS.items():
    setattr(
        OriginalFirstEditionPhotoAdjudication,
        f"test_manual_glpyh_{key[0].lower()}_{key[1]:02d}",
        one_read_test(key, pair),
    )


if __name__ == "__main__":
    unittest.main()
