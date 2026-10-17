"""Integrity tests for pending Lilly first-edition face/hair *source window*."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


class FrozenSourceWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = json.loads((B / "SOURCE_WINDOW_20261017.json").read_text())

    def test_scan_sequence_and_original_page_misprints(self):
        self.assertEqual(list(self.w["original_scans"]), [str(n) for n in range(581, 587)])
        self.assertEqual(
            list(self.w["printed_folios_original_scans"].values()),
            ["539", "548", "549", "542", "543", "552"],
        )
        self.assertIn("Never reorder", self.w["source_pagination_note"])

    def test_sha256_and_bytes(self):
        for ref in self.w["original_scans"].values():
            source = B / ref["file"]
            raw = source.read_bytes()
            self.assertEqual(len(raw), ref["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), ref["sha256"])
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))

    def test_next_original_chapter_boundary(self):
        c = self.w["next_chapter"]
        self.assertEqual(c["original_pdf_start"], 581)
        self.assertEqual(c["original_pdf_end"], 583)
        self.assertEqual(c["following_heading_pdf_page"], 583)
        self.assertEqual(c["following_following_heading_pdf_page"], 585)

    def test_source_index_freeze_not_bumped(self):
        self.assertEqual(self.w["baseline_accepted_lilly"], 6671)
        self.assertEqual(self.w["baseline_historical_total"], 7737)
        self.assertEqual(self.w["next_record_id"], "R6672")
        self.assertEqual(self.w["admission"]["historical_records_added"], 0)
        index_path = B.parents[1] / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        if index_path.is_file():
            index = json.loads(index_path.read_text())
            self.assertEqual(index["records_count"], 6671)
            self.assertEqual(index["next"]["pdf_page"], 581)
            self.assertEqual(index["batches"][-1]["id"], "B05i")

    def test_not_biometric_or_clinical_evidence(self):
        a = self.w["admission"]
        self.assertFalse(a["race_or_ancestry_predictions_authorized"])
        self.assertFalse(a["clinical_disability_predictions_authorized"])
        self.assertEqual(a["empirical_human_stature_validations"], 0)
        self.assertEqual(a["empirical_hair_or_face_validations"], 0)
        self.assertEqual(a["runtime_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
