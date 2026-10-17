"""Primary-source image, chapter seam and no-premature-admission checks."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


class WealthWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = json.loads((B / "SOURCE_WINDOW_20261017.json").read_text())

    def test_original_three_image_hashes_bytes(self):
        for page in self.w["images"].values():
            path = B / page["file"]
            raw = path.read_bytes()
            self.assertEqual(len(raw), page["size"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), page["sha256"])
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))

    def test_physical_source_folio_order(self):
        self.assertEqual(list(self.w["images"]), ["586", "587", "588"])
        self.assertEqual(
            [page["printed_folio_original"] for page in self.w["images"].values()],
            ["552", "553", "554"],
        )

    def test_unnumbered_section_not_skipped(self):
        headings = self.w["chapters"]
        self.assertEqual(headings["unnumbered_riches"]["original_pdf_start"], 586)
        self.assertEqual(headings["unnumbered_riches"]["original_pdf_end"], 587)
        self.assertEqual(headings["following_printed_numbered"]["printed_numeral"], "CXIIII")
        self.assertEqual(headings["following_printed_numbered"]["original_pdf_start"], 587)
        self.assertEqual(headings["following_following_printed"]["original_pdf_start"], 588)

    def test_source_window_not_canonical_admission(self):
        self.assertEqual(self.w["accepted_lilly_before_extraction"], 6808)
        self.assertEqual(self.w["accepted_combined_before_extraction"], 7874)
        self.assertEqual(self.w["next_new_source_id"], "R6809")
        self.assertEqual(self.w["new_documentary_records"], 0)
        root = B.parents[1] / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        if root.exists():
            index = json.loads(root.read_text())
            self.assertIn(index["records_count"], (6808, 6853))
            if index["records_count"] == 6808:
                self.assertEqual(index["next"]["chapter"], "UNNUMBERED_SECOND_HOUSE_RICHES")
                self.assertEqual(index["next"]["pdf_page"], 586)
            else:
                self.assertEqual(index["batches"][-1]["id"], "B05m")
                self.assertEqual(index["batches"][-1]["records_count"], 45)
                self.assertEqual(index["next"]["pdf_page"], 587)
            self.assertEqual(index["empirical_validations"], 0)
            self.assertEqual(index["runtime_promotions"], 0)

    def test_science_separation_and_workplan(self):
        self.assertEqual(self.w["empirical_validations"], 0)
        self.assertEqual(self.w["runtime_promotions"], 0)
        plan = " ".join(self.w["original_source_plan"])
        self.assertIn("without inventing", plan)
        self.assertIn("Ptolemy", plan)
        self.assertIn("Leovitius", plan)
        self.assertIn("CXIIII", plan)


if __name__ == "__main__":
    unittest.main()
