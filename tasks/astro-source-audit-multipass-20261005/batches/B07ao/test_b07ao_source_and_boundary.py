"""Verify original first and independently typeset second-edition CLXVII closing table."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
W = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
C = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class CLXVIILastOriginalPhoto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.rows = cls.source["record_rows"]

    def test_original_1647_full_book_SHA(self):
        self.assertEqual(
            self.source["source_full_first_1647_Wellcome_PDF_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_two_independently_typeset_physical_printing_photos(self):
        self.assertEqual(len(self.source["source_photo_images"]), 4)
        for key, meta in self.source["source_photo_images"].items():
            p = B / meta["path"]
            self.assertTrue(p.is_file(), key)
            self.assertEqual(p.stat().st_size, meta["byte_length"], key)
            self.assertEqual(sha(p), meta["sha256"], key)
            self.assertGreater(p.stat().st_size, 200000)

    def test_old_western_and_chinese_source_count(self):
        self.assertEqual(j(W)["records_count"], 12649)
        self.assertEqual(j(W)["batches"][-1]["id"], "B07an")
        self.assertEqual(j(C)["sum_source_annotations"], 355)

    def test_exact_22_new_contiguous_record_ids(self):
        self.assertEqual(self.source["historical_claims_source_count"], 22)
        self.assertEqual(len(self.rows), 22)
        self.assertEqual(self.rules["record_count"], 22)
        self.assertEqual([r["id"] for r in self.rows], [f"R{i}" for i in range(12650, 12672)])
        self.assertEqual(self.accept["next_R"], "R12672")

    def test_three_distinct_old_Hylegical_source_tables(self):
        self.assertEqual(
            self.source["original_CLXVII_last_p725_tabular_sections"], ["Mid-heaven", "Sun", "Moon"]
        )
        titles = [r["source_photo_locator_not_critical_diplomatic_quote"] for r in self.rows]
        self.assertTrue(any("Mid-heaven to Promittors" in x for x in titles))
        self.assertTrue(any("☉ unto Promittors" in x for x in titles))
        self.assertTrue(any("☽ unto Promittors" in x for x in titles))

    def test_selected_source_original_mid_heaven_physical_rows(self):
        vals = {
            r["source_photo_locator_not_critical_diplomatic_quote"]: r[
                "original_source_tabular_annual_arc_day"
            ]
            for r in self.rows
        }
        self.assertEqual(vals["To Termes of ♀"], 77)
        self.assertEqual(vals["Contrantiscion ♂"], 176)
        self.assertEqual(vals["Scorpions heart"], 241)

    def test_selected_original_sun_and_moon_rows_not_actual_forecasts(self):
        self.assertEqual(self.rows[7]["original_source_tabular_annual_arc_day"], 33)
        self.assertEqual(self.rows[11]["original_source_tabular_annual_arc_day"], 22)
        self.assertEqual(self.rows[13]["original_source_tabular_annual_arc_day"], 63)
        for row in self.rows:
            self.assertFalse(row["original_historical_human_event_outcome_observed"])
            self.assertFalse(row["runtime_astrology_promoted"])

    def test_doubled_boundary_first_clxvii_closed_next_clxviii(self):
        self.assertTrue(self.source["original_source_CLXVII_physical_span_fully_covered_as_pages"])
        self.assertTrue(self.source["original_printed_CLXVIII_begins_pdf760"])
        self.assertEqual(self.source["source_next_original_PDF"], 760)
        self.assertEqual(self.accept["next_original_chapter"], "CLXVIII")
        self.assertEqual(self.accept["previous_chapter"], "CLXVII")

    def test_source_clxviii_original_five_factors_not_tested(self):
        self.assertEqual(
            self.rows[-1]["original_pdf_frames"],
            [760],
        )
        self.assertIn("five", self.rows[-1]["source_photo_locator_not_critical_diplomatic_quote"])
        self.assertFalse(
            self.source["original_CLXVII_source_critical_diplomatic_validation_complete"]
        )

    def test_original_full_p725_numerical_cells_not_critically_checked(self):
        self.assertFalse(
            self.source["original_source_p725_full_row_by_row_critical_comparison_complete"]
        )
        self.assertFalse(self.rules["critical_historical_all_cells_and_edition_variants_verified"])
        self.assertEqual(self.source["verified_life_event_predictions"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)

    def test_prepared_acceptance_SHA_stable(self):
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["records_sha256"], sha(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json")
        )
        self.assertEqual(self.accept["Lilly_if_accepted"], 12671)
        self.assertEqual(self.accept["Western_if_accepted"], 13737)


def each_record(i):
    def check(self):
        a = self.rows[i]
        r = self.rules["rules"][i]
        self.assertEqual(a["id"], f"R{12650 + i}")
        self.assertEqual(r["record_number"], 12650 + i)
        self.assertEqual(a["original_pdf_frames"], r["original_pdf_frames"])
        self.assertFalse(a["runtime_astrology_promoted"])
        self.assertFalse(a["original_historical_human_event_outcome_observed"])

    return check


for i in range(22):
    setattr(CLXVIILastOriginalPhoto, f"test_source_annotation_{12650 + i}", each_record(i))


if __name__ == "__main__":
    unittest.main()
