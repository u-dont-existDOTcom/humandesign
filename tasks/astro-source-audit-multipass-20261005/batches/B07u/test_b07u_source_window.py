"""Original first-edition CLXIIII source-window integrity tests; no clause promotion."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class PrintedMoonSourceWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        backup = B / "recovery" / "INDEX_BEFORE_B07u.json"
        cls.oldindex = backup if backup.exists() else INDEX
        cls.prior = j(cls.oldindex)
        cls.china = j(CHINA)

    def test_source_original_pdf_sha(self):
        self.assertEqual(
            self.window["full_source_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_previous_index_sha(self):
        self.assertEqual(sha(self.oldindex), self.window["previous_index_sha256"])

    def test_prior_accepted_boundary(self):
        self.assertEqual(self.prior["records_count"], 11825)
        self.assertEqual(self.prior["batches"][-1]["id"], "B07t")
        self.assertEqual(self.prior["next"]["chapter"], "CLXIIII")
        self.assertEqual(self.prior["next"]["pdf_page"], 725)

    def test_clxiiii_start(self):
        self.assertEqual(self.window["starts_original_pdf"], 725)
        self.assertEqual(self.window["starts_printed_folio"], 691)
        self.assertIn("Moon to PROMITTORS", self.window["printed_numbered_heading"])

    def test_unnumbered_next_headed_unit(self):
        self.assertEqual(self.window["following_heading_original_pdf"], 735)
        self.assertFalse(self.window["following_heading_numbered"])
        self.assertIn(
            "Moon Directed to FIXED STARRES", self.window["following_unnumbered_headed_unit"]
        )

    def test_last_moon_promittor_is_pdf735(self):
        self.assertEqual(self.window["body_frames"], list(range(725, 736)))
        self.assertEqual(self.window["ends_original_pdf"], 735)
        self.assertEqual(self.window["ends_printed_folio"], 701)

    def test_original_next_context(self):
        self.assertEqual(self.window["following_context_pdf"], 736)
        self.assertIn("UNNUMBERED_FIXED_STARS", self.window["photos"]["736"]["scope"])

    def test_scan_page_folios(self):
        for n in range(725, 737):
            self.assertEqual(self.window["photos"][str(n)]["printed_folio"], n - 34)

    def test_complete_photographic_window(self):
        self.assertEqual(sorted(map(int, self.window["photos"])), list(range(725, 737)))

    def test_source_only_not_empirical(self):
        self.assertTrue(self.window["source_only"])
        self.assertEqual(self.window["empirical_human_validations"], 0)
        self.assertEqual(self.window["runtime_promotions"], 0)

    def test_chinese_record_count_unmodified(self):
        self.assertEqual(self.window["accepted_chinese_v2"], 97)
        self.assertEqual(self.china["sum_source_annotations"], 97)

    def test_ptolemy_not_included(self):
        self.assertEqual(self.window["accepted_ptolemy"], 1066)

    def test_next_record_protected(self):
        self.assertEqual(self.window["first_unaccepted_source_record"], "R11826")

    def test_first_frame_prior_and_new(self):
        self.assertIn("B07t", self.window["photos"]["725"]["raster_source"])
        self.assertIn("CLXIIII", self.window["photos"]["725"]["scope"])

    def test_source_render_method_not_undisclosed(self):
        for n in range(726, 737):
            self.assertIn("POPPLER", self.window["photos"][str(n)]["raster_source"])

    def test_photo_no_missing_sha_or_bytes(self):
        for record in self.window["photos"].values():
            self.assertEqual(len(record["sha256"]), 64)
            self.assertGreater(record["bytes"], 150000)


def make_photo_test(n):
    def test(self):
        record = self.window["photos"][str(n)]
        file = B / record["file"]
        raw = file.read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(sha(file), record["sha256"])
        self.assertEqual(len(raw), record["bytes"])

    return test


for n in range(725, 737):
    setattr(PrintedMoonSourceWindow, f"test_photo_{n}", make_photo_test(n))


if __name__ == "__main__":
    unittest.main()
