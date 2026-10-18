"""Standalone original first-edition printed Sun fixed stars physical-boundary tests."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


class OriginalCLXIIIPhysicalWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        old = B / "recovery" / "INDEX_BEFORE_B07t.json"
        cls.old = old if old.exists() else INDEX
        cls.prior = j(cls.old)
        cls.china = j(CHINA)

    def test_01_prior_accepted_exact_hash(self):
        self.assertEqual(sha(self.old), self.win["parent_lilly_index_sha256"])

    def test_02_no_prior_count_replaced(self):
        self.assertEqual(self.prior["records_count"], 11721)
        self.assertEqual(self.prior["batches"][-1]["id"], "B07s")

    def test_03_accepted_next_chapter(self):
        self.assertEqual(self.prior["next"]["chapter"], "CLXIII")
        self.assertEqual(self.prior["next"]["pdf_page"], 723)

    def test_04_original_pdf_fingerprint(self):
        self.assertEqual(
            self.win["full_source_894_frame_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_05_exact_body_and_dividers(self):
        self.assertEqual(self.win["body_original_pdf_frames"], [723, 724, 725])
        self.assertEqual(self.win["next_chapter"], "CLXIIII")
        self.assertEqual(self.win["next_heading_pdf"], 725)

    def test_06_unchanged_chinese_source_lane(self):
        self.assertEqual(self.win["separate_chinese_v2"], 97)
        self.assertEqual(self.china["sum_source_annotations"], 97)
        self.assertEqual(self.win["parent_ptolemy"], 1066)

    def test_07_source_photographs_original_hashes(self):
        for n in (723, 724, 725):
            w = self.win["photos"][str(n)]
            pic = B / w["file"]
            self.assertEqual(sha(pic), w["sha256"])
            self.assertEqual(pic.stat().st_size, w["bytes"])
            self.assertGreater(w["bytes"], 150000)

    def test_08_explicit_cross_chapter_roles(self):
        self.assertIn("prior_CLXII", self.win["photos"]["723"]["role"])
        self.assertIn("next_CLXIIII", self.win["photos"]["725"]["role"])

    def test_09_no_technical_or_human_validation(self):
        self.assertFalse(self.win["original_star_epoch_and_modern_identity_parity_verified"])
        self.assertFalse(self.win["original_direction_arc_to_date_engine_verified"])
        self.assertEqual(self.win["independent_real_person_predictions_validated"], 0)
        self.assertEqual(self.win["runtime_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
