"""B07ac first-edition annual table source checks, no personal chart inference."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class SagittariusCapricornPhoto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read(B / "PHOTO_SOURCE_SAGITTARIUS_CAPRICORN_V1.json")
        cls.current = read(B / "ANNUAL_RATE_PHOTO_OVERLAY_V5.json")
        cls.parent = read(B.parent / "B07ab/ANNUAL_RATE_PHOTO_OVERLAY_V4.json")
        cls.records = {(r["sign"], r["degree"]): r for r in cls.source["records"]}
        cls.rows = {(r["sign"], r["degree"]): r for r in cls.current["rows"]}
        cls.old = {(r["sign"], r["degree"]): r for r in cls.parent["rows"]}

    def test_source_original_full_pdf_identity(self):
        self.assertEqual(
            self.source["full_1647_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_source_primary_photo_binary(self):
        f = B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
        self.assertEqual(self.source["original_1647_image_pdf745_sha256"], sha(f))
        self.assertEqual(self.current["original_photo_pdf745_sha256"], sha(f))

    def test_source_62_disjoint_fields(self):
        self.assertEqual(len(self.records), 62)
        for s in ("Sagittarius", "Capricorn"):
            self.assertEqual([d for name, d in self.records if name == s], list(range(31)))

    def test_old_Capricorn_B07y_four_positions_no_double_count(self):
        old = {k for k, r in self.records.items() if r["previous_source_photo_review"]}
        self.assertEqual(
            old, {("Capricorn", 12), ("Capricorn", 13), ("Capricorn", 14), ("Capricorn", 15)}
        )
        for key in old:
            self.assertEqual(self.rows[key]["source_read_batch"], "B07y")

    def test_new_source_57_legible_and_one_unclear(self):
        self.assertEqual(self.source["new_1647_photo_legible_positions"], 57)
        self.assertEqual(self.source["new_photo_unresolved_positions"], 1)
        self.assertEqual(self.current["B07ac_new_one_reader_legible"], 57)
        self.assertEqual(self.current["B07ac_new_ambiguous_source_glyphs"], 1)

    def test_new_unresolved_Capricorn_9_not_filled_by_math(self):
        k = ("Capricorn", 9)
        self.assertIsNone(self.records[k]["first_edition_1647_printed_rate"])
        self.assertEqual(
            self.records[k]["unresolved_print_glyph_alternatives"], [[66, 32], [66, 39]]
        )
        self.assertIsNone(self.rows[k]["first_edition_1647_one_reader_photo_rate"])
        self.assertEqual(self.rows[k]["source_read_batch"], "B07ac")

    def test_old_Capricorn15_ambiguity_preserved(self):
        k = ("Capricorn", 15)
        self.assertEqual(self.rows[k]["source_read_batch"], "B07y")
        self.assertEqual(
            self.rows[k]["unresolved_original_source_glyph_options"],
            self.old[k]["unresolved_original_source_glyph_options"],
        )
        self.assertIsNone(self.rows[k]["first_edition_1647_one_reader_photo_rate"])

    def test_Sagittarius6_original_differs_from_derivative(self):
        self.assertEqual(self.rows["Sagittarius", 6]["frozen_B07x_derivative_candidate"], [64, 27])
        self.assertEqual(
            self.rows["Sagittarius", 6]["first_edition_1647_one_reader_photo_rate"], [64, 37]
        )

    def test_Sagittarius22_original_nonmonotonic_unchanged(self):
        self.assertEqual(self.rows["Sagittarius", 22]["frozen_B07x_derivative_candidate"], [66, 31])
        self.assertEqual(
            self.rows["Sagittarius", 22]["first_edition_1647_one_reader_photo_rate"], [66, 30]
        )
        self.assertEqual(
            self.rows["Sagittarius", 21]["first_edition_1647_one_reader_photo_rate"], [66, 32]
        )
        self.assertEqual(
            self.rows["Sagittarius", 23]["first_edition_1647_one_reader_photo_rate"], [66, 40]
        )

    def test_exact_two_new_source_vs_derivative_errors(self):
        s = self.current["B07ac_printed_vs_derivative"]
        self.assertEqual(
            [(r["sign"], r["degree"]) for r in s], [("Sagittarius", 6), ("Sagittarius", 22)]
        )
        self.assertEqual(
            [(r["printed_1647"], r["derivative_originally_frozen"]) for r in s],
            [([64, 37], [64, 27]), ([66, 30], [66, 31])],
        )

    def test_capricorn13_previously_corrected(self):
        self.assertEqual(
            self.rows["Capricorn", 13]["first_edition_1647_one_reader_photo_rate"], [66, 10]
        )
        self.assertEqual(self.rows["Capricorn", 13]["source_read_batch"], "B07y")

    def test_all_372_cumulative_counts(self):
        self.assertEqual(len(self.rows), 372)
        self.assertEqual(self.current["cumulative_one_reader_legible_original"], 320)
        self.assertEqual(self.current["cumulative_original_source_glyph_ambiguities"], 5)
        self.assertEqual(self.current["cumulative_positions_original_unread"], 47)
        self.assertEqual(320 + 5 + 47, 372)

    def test_prior_372_source_rows_immutable_for_unchanged(self):
        for key, prior in self.old.items():
            r = self.rows[key]
            if key not in self.records:
                self.assertEqual(r, prior)
            else:
                self.assertEqual(
                    r["frozen_B07x_derivative_candidate"], prior["frozen_B07x_derivative_candidate"]
                )

    def test_crops_are_source_derivatives_not_new_witnesses(self):
        for f in (
            "Sagittarius_first_half.png",
            "Sagittarius_second_half.png",
            "Capricorn_first_half.png",
            "Capricorn_second_half.png",
            "Sag_4_10.png",
            "Sag_19_26.png",
            "Cap_12_16.png",
            "Cap_15_21.png",
            "Sagittarius_5_through_10.png",
            "Sagittarius_19_through_25.png",
            "Capricorn_14_through_22.png",
        ):
            self.assertTrue((B / "evidence" / f).is_file(), f)
        self.assertFalse(self.source["source_reading_not_independently_blinded"] is False)

    def test_canonical_historical_indices_retained(self):
        self.assertEqual(read(WEST)["records_count"], 12472)
        self.assertEqual(read(CHINA)["sum_source_annotations"], 142)
        self.assertEqual(self.current["Lilly_accepted_canonical_source_registry_unchanged"], 12472)
        self.assertEqual(self.current["Chinese_V3_registry_unchanged"], 142)

    def test_no_predictions_promoted(self):
        self.assertFalse(self.current["all_original_source_rate_cells_collated"])
        self.assertFalse(self.current["independent_second_source_reader_review_complete"])
        self.assertFalse(self.current["historical_angular_year_math_or_natal_engine_verified"])
        self.assertEqual(self.current["real_people_predictive_validations"], 0)
        self.assertEqual(self.current["runtime_model_promotions"], 0)
        for r in self.current["rows"]:
            self.assertFalse(r["runtime_promoted"])


def one_cell(sign, d):
    def test(self):
        k = (sign, d)
        src = self.records[k]
        cur = self.rows[k]
        self.assertEqual(src["original_pdf_frame"], 745)
        self.assertEqual(
            src["photo_crop"], sign + ("_first_half.png" if d < 16 else "_second_half.png")
        )
        if src["previous_source_photo_review"]:
            self.assertEqual(cur["source_read_batch"], "B07y")
        else:
            self.assertEqual(cur["source_read_batch"], "B07ac")
        self.assertEqual(
            cur["first_edition_1647_one_reader_photo_rate"], src["first_edition_1647_printed_rate"]
        )
        self.assertFalse(cur["runtime_promoted"])

    return test


for s in ("Sagittarius", "Capricorn"):
    for degree in range(31):
        setattr(SagittariusCapricornPhoto, f"test_{s.lower()}_deg{degree:02d}", one_cell(s, degree))


if __name__ == "__main__":
    unittest.main()
