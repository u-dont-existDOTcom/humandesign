"""Original first-edition CLXII source-window integrity, no accepted new records."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


class SunSourceWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        backup = B / "recovery" / "INDEX_BEFORE_B07s.json"
        cls.pre_index = backup if backup.exists() else INDEX
        cls.index = j(cls.pre_index)
        cls.china = j(CHINA)

    def test_old_head(self):
        self.assertEqual(self.index["records_count"], 11415)
        self.assertEqual(self.index["batches"][-1]["id"], "B07r")
        self.assertEqual(sha(self.pre_index), self.win["prior_index_sha256"])

    def test_original_full_pdf_witness(self):
        self.assertEqual(self.win["original_pdf_bytes"], 141842963)
        self.assertEqual(
            self.win["original_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_clxii_ends_on_723_not_720(self):
        s = self.win["printed_clxii"]
        self.assertEqual(s["starts_frame"], 713)
        self.assertEqual(s["ends_frame"], 723)
        self.assertEqual(s["body_frames"], list(range(713, 724)))
        self.assertTrue(s["chapter_end_before_next_divider"])

    def test_next_clxiii_real_boundary(self):
        n = self.win["following_printed_clxiii"]
        self.assertEqual(n["starts_frame"], 723)
        self.assertEqual(n["ends_frame"], 725)
        self.assertEqual(n["next_printed_clxiiii_heading_frame"], 725)
        self.assertTrue(n["body_not_part_of_clxii"])

    def test_chinese_index_separate(self):
        self.assertEqual(self.win["independent_chinese_v2_count"], 97)
        self.assertEqual(self.china["sum_source_annotations"], 97)
        self.assertEqual(self.win["prior_retained_ptolemy"], 1066)

    def test_all_frames_present(self):
        self.assertEqual(list(self.win["photos"]), [str(n) for n in range(713, 726)])

    def test_source_formats_distinguished(self):
        for n in range(713, 726):
            photo = self.win["photos"][str(n)]
            if n <= 720:
                self.assertIn("PREVIOUS_B07q", photo["extraction_method"])
            else:
                self.assertIn("PDFTOPPM", photo["extraction_method"])

    def test_page_number_not_inferred(self):
        for n in range(713, 726):
            self.assertEqual(self.win["photos"][str(n)]["printed_page"], n - 34)

    def test_overlap_roles(self):
        self.assertIn("PRIOR_CLXI", self.win["photos"]["713"]["body_role"])
        self.assertIn("NEXT_CLXIII", self.win["photos"]["723"]["body_role"])
        self.assertIn("CLXIIII", self.win["photos"]["725"]["body_role"])

    def test_no_forecast_promotion(self):
        self.assertEqual(self.win["empirical_person_validations"], 0)
        self.assertEqual(self.win["runtime_promotions"], 0)
        self.assertTrue(self.win["source_only"])

    def test_next_id(self):
        self.assertEqual(self.win["new_source_record_starts"], "R11416")


def photo_test(n):
    def test(self):
        witness = self.win["photos"][str(n)]
        file = B / witness["file"]
        self.assertTrue(file.is_file())
        raw = file.read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(len(raw), witness["bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), witness["sha256"])
        self.assertGreater(len(raw), 150000)

    return test


for n in range(713, 726):
    setattr(SunSourceWindow, f"test_original_photo_{n}", photo_test(n))


if __name__ == "__main__":
    unittest.main()
