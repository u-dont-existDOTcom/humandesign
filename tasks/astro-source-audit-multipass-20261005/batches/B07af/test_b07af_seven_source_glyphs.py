"""Second typeset original book witness for seven unresolved 1647 table glyphs."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
EXPECTED = {
    ("Virgo", 1): [[55, 10], [55, 13]],
    ("Virgo", 18): [[53, 58], [53, 59]],
    ("Capricorn", 9): [[66, 32], [66, 39]],
    ("Capricorn", 15): [[65, 57], [66, 2]],
    ("Aquarius", 5): [[62, 33], [62, 35]],
    ("Aquarius", 6): [[62, 22], [62, 24]],
    ("Pisces", 24): [[53, 43], [54, 43]],
}


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class SecondPrintingWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j(B / "SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json")
        cls.old = j(PARENT)
        cls.rows = {(r["sign"], r["degree"]): r for r in cls.a["entries"]}
        cls.source = {(r["sign"], r["degree"]): r for r in cls.old["rows"]}

    def test_full_wellcome_original_id(self):
        self.assertEqual(
            self.a["source_first_edition_full_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_two_distinct_prints_original_images_sha(self):
        f = B / "evidence/original_1647_annual_table_pdf745_3500.jpg"
        s = B / "evidence/second_edition_1659_annual_table_page740.jpg"
        self.assertEqual(sha(f), self.a["source_first_edition_photo_sha256"])
        self.assertEqual(sha(s), self.a["source_second_edition_original_image_sha256"])
        self.assertNotEqual(sha(f), sha(s))

    def test_second_edition_not_authority_over_original(self):
        self.assertTrue(self.a["do_not_promote_substitutions_from_1659_to_1647"])
        self.assertTrue(self.a["later_second_print_is_not_a_blinded_source_reader"])
        self.assertFalse(self.a["independent_human_historian_or_second_reader_verified"])

    def test_original_first_edition_V6_binary_sha_protected(self):
        self.assertEqual(sha(PARENT), self.a["source_previous_B07ad_photo_status_SHA256"])
        self.assertEqual(self.old["cumulative_one_reader_legible_original_1647"], 365)
        self.assertEqual(self.old["cumulative_original_print_unresolved_positions"], 7)

    def test_all_seven_original_missing_exact(self):
        self.assertEqual(set(self.rows), set(EXPECTED))
        for key, pairs in EXPECTED.items():
            self.assertEqual(self.rows[key]["original_first_edition_photo_glyph_candidates"], pairs)
            self.assertIsNone(self.rows[key]["source_original_first_edition_reading"])
            self.assertIsNone(self.source[key]["first_edition_1647_one_reader_photo_rate"])

    def test_later_edition_tentative_two_not_autocorrected(self):
        self.assertEqual(self.a["source_second_edition_tentative_glyph_matches"], 2)
        self.assertEqual(
            self.rows["Virgo", 1]["later_1659_independent_typesetting_tentative_reading"], [55, 10]
        )
        self.assertEqual(
            self.rows["Capricorn", 9]["later_1659_independent_typesetting_tentative_reading"],
            [66, 32],
        )
        for key in (("Virgo", 1), ("Capricorn", 9)):
            self.assertEqual(
                self.rows[key]["original_1647_glyph_status_after_second_edition"], "UNRESOLVED"
            )
            self.assertFalse(self.rows[key]["original_1647_value_silently_replaced"])

    def test_five_later_rows_low_resolution_stay_unknown(self):
        unknown = [
            key
            for key, r in self.rows.items()
            if r["later_1659_independent_typesetting_tentative_reading"] is None
        ]
        self.assertEqual(len(unknown), 5)
        self.assertEqual(self.a["source_second_edition_indeterminate_positions"], 5)
        for k in unknown:
            self.assertEqual(
                self.rows[k]["later_1659_printing_reading_confidence"],
                "LOW_RESOLUTION_SECOND_EDITION_NOT_DECISIVE",
            )

    def test_cumulative_original_unknown_remains_seven(self):
        self.assertEqual(self.a["source_first_edition_unresolved_before"], 7)
        self.assertEqual(self.a["source_first_edition_unresolved_after"], 7)
        self.assertTrue(self.a["source_first_edition_original_365_legible_7_unresolved_unchanged"])

    def test_seven_crop_filenames_correspond_to_physical_witness(self):
        for r in self.a["entries"]:
            path = B / "evidence" / r["later_photo_crop"]
            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 3000)
            self.assertEqual(sha(path), r["later_photo_crop_sha256"])
            self.assertEqual(r["later_1659_djvu_frame"], 740)
            self.assertEqual(r["original_pdf_frame"], 745)

    def test_no_change_to_registered_history_counters(self):
        self.assertEqual(j(WEST)["records_count"], 12472)
        self.assertEqual(j(CHINA)["sum_source_annotations"], 142)
        self.assertEqual(self.a["historical_western_Lilly_canonical_unchanged"], 12472)
        self.assertEqual(self.a["historical_chinese_V3_canonical_unchanged"], 142)

    def test_nonpromoted_human_claims(self):
        self.assertEqual(self.a["real_human_astrological_prediction_validated"], 0)
        self.assertEqual(self.a["model_runtime_promotions"], 0)
        for row in self.a["entries"]:
            self.assertFalse(row["runtime_promoted"])
            self.assertFalse(row["authoritative_birth_chart_calculation_allowed"])
            self.assertFalse(row["independent_human_event_accuracy_validated"])


def individual_unknown(key):
    def test(self):
        src = self.rows[key]
        before = self.source[key]
        self.assertEqual(
            src["original_first_edition_photo_glyph_candidates"],
            before["unresolved_original_source_glyph_options"],
        )
        self.assertIsNone(src["source_original_first_edition_reading"])
        self.assertFalse(src["original_1647_value_silently_replaced"])
        self.assertEqual(src["original_1647_glyph_status_after_second_edition"], "UNRESOLVED")

    return test


for sign, deg in EXPECTED:
    setattr(
        SecondPrintingWitness,
        f"test_unresolved_{sign.lower()}_{deg:02d}",
        individual_unknown((sign, deg)),
    )


if __name__ == "__main__":
    unittest.main()
