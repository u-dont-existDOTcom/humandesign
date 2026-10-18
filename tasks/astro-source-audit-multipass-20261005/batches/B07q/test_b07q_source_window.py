"""Original Lilly CLX next-source original page window; no admitted claims."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"


class OriginalMidheavenSourceWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = json.loads((B / "ORIGINAL_SOURCE_WINDOW_V1.json").read_text())
        pre_index = B / "recovery" / "INDEX_BEFORE_B07q.json"
        cls.index_source = pre_index if pre_index.exists() else IDX
        cls.index = json.loads(cls.index_source.read_text())
        cls.chinese = json.loads(CHINA.read_text())

    def test_01_original_photographs_sha_bytes_folios(self):
        self.assertEqual(list(self.window["photos"]), [str(i) for i in range(702, 721)])
        for obj in self.window["photos"].values():
            raw = (B / obj["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), obj["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), obj["sha256"])

    def test_02_no_change_accepted_source_index_or_records(self):
        self.assertEqual(self.index["records_count"], 11067)
        self.assertEqual(self.index["batches"][-1]["id"], "B07p")
        self.assertEqual(
            self.window["accepted_index_sha256"],
            hashlib.sha256(self.index_source.read_bytes()).hexdigest(),
        )
        self.assertEqual(self.window["historical_records_added"], 0)
        self.assertEqual(self.window["numbered_chapters_added"], 0)

    def test_03_original_CLX_starts_at_both_edge_pdf702(self):
        self.assertEqual(self.index["next"]["chapter"], "CLX")
        self.assertEqual(self.index["next"]["pdf_page"], 702)
        self.assertEqual(self.window["printed_CLX"]["starts_original_pdf"], 702)
        self.assertEqual(self.window["printed_CLX"]["starts_printed_page"], 668)

    def test_04_original_CLX_body_complete_photo_frames(self):
        self.assertEqual(
            self.window["printed_CLX"]["body_original_pdf_frames"],
            list(range(702, 712)),
        )
        self.assertEqual(self.window["printed_CLX"]["ends_original_pdf"], 711)

    def test_05_CLXI_separate_fixed_stars_joins_pdf711(self):
        self.assertEqual(self.window["following_printed_CLXI"]["heading_original_pdf"], 711)
        self.assertEqual(
            self.window["following_printed_CLXI"]["body_original_pdf_frames"],
            [711, 712, 713],
        )
        self.assertIn("FIXED STARRES", self.window["following_printed_CLXI"]["heading"])

    def test_06_CLXII_sun_separate_from_midheaven_pdf713(self):
        self.assertEqual(self.window["following_printed_CLXII"]["heading_original_pdf"], 713)
        self.assertEqual(
            self.window["following_printed_CLXII"]["context_pdfs"],
            list(range(713, 721)),
        )

    def test_07_photos_not_assigned_to_wrong_printed_chapter(self):
        photos = self.window["photos"]
        self.assertTrue(all("printed_CLX_body" in photos[str(n)]["role"] for n in range(702, 712)))
        self.assertTrue(all("following_printed_CLXI" in photos[str(n)]["role"] for n in (712, 713)))
        self.assertTrue(
            all("CLXII_source_context_not_CLX" in photos[str(n)]["role"] for n in range(714, 721))
        )

    def test_08_parallel_chinese_source_unmodified(self):
        self.assertEqual(self.chinese["sum_source_annotations"], 72)
        self.assertEqual(self.chinese["runtime_promotions"], 0)
        self.assertEqual(self.window["parallel_chinese_source_annotations"], 72)

    def test_09_no_human_predictions_or_runtime_promotions(self):
        self.assertFalse(self.window["complete_CLX_diplomatic_transcription"])
        self.assertFalse(self.window["actual_primary_directions_chart_engine_verified"])
        self.assertEqual(self.window["independent_human_predictions_validated"], 0)
        self.assertEqual(self.window["runtime_rule_promotions"], 0)
        self.assertEqual(self.index["empirical_validations"], 0)
        self.assertEqual(self.index["runtime_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
