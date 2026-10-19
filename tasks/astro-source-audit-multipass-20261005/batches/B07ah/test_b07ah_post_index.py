"""Post-index partial Lilly CLXVI annual-rate source registry consistency."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = BASE / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class CanonicalPartialAnnualRate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ah.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.rules = j(B / "RULES.json")
        cls.cross = j(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")

    def test_old_source_12501_new_source_12515(self):
        self.assertEqual(self.old["records_count"], 12501)
        self.assertEqual(self.now["records_count"], 12515)
        self.assertEqual(self.receipt["new_historical_source_annotations"], 14)

    def test_exactly_one_new_source_batch(self):
        self.assertEqual(
            [a["id"] for a in self.now["batches"]],
            [a["id"] for a in self.old["batches"]] + ["B07ah"],
        )
        self.assertEqual(sum(a["records_count"] for a in self.now["batches"]), 12515)
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_source_folio_711_and_12_stars_31_rows(self):
        self.assertEqual(self.rules["body_pdf_frames"], [745])
        self.assertEqual(self.cross["original_rate_printed_folio"], 711)
        self.assertEqual(self.cross["original_rate_table_sign_count"], 12)
        self.assertEqual(self.cross["original_rate_total_physical_positions"], 372)

    def test_source_full_CLXVI_still_not_read(self):
        self.assertEqual(self.now["read_numbered_chapters"], self.old["read_numbered_chapters"])
        self.assertEqual(self.now["read_headed_units_count"], self.old["read_headed_units_count"])
        self.assertEqual(len(self.now["partial_numbered_chapters"]), 1)
        p = self.now["partial_numbered_chapters"][0]
        self.assertFalse(p["complete"])
        self.assertEqual(p["accepted_through_pdf"], 745)
        self.assertEqual(p["next_unaccepted_pdf"], 746)
        self.assertFalse(p["original_1647_full_372_source_glyphs_critically_verified"])

    def test_next_historical_source_still_same_chapter(self):
        self.assertEqual(self.now["next"]["chapter"], "CLXVI")
        self.assertEqual(self.now["next"]["pdf_page"], 746)
        self.assertEqual(self.now["next"]["printed_page"], 712)
        self.assertIn("R12516", self.now["next"]["position"])
        self.assertFalse(self.now["next"]["extracted"])

    def test_original_source_pdf_sha_persists(self):
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            self.now["source_sha256"], self.cross["source_original_1647_full_pdf_sha256"]
        )

    def test_all_previous_Lilly_rules_preserved(self):
        oldbatch = self.old["batches"]
        newbatch = self.now["batches"]
        self.assertEqual(newbatch[: len(oldbatch)], oldbatch)

    def test_chinese_source_registry_is_identical(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07ah.json"))
        self.assertEqual(sha(CHINA), self.receipt["Chinese_V5_SHA256"])

    def test_source_crosswalk_count_and_sha(self):
        self.assertEqual(self.cross["original_1647_one_reader_legible"], 365)
        self.assertEqual(self.cross["original_1647_unresolved"], 7)
        self.assertEqual(self.cross["original_vs_derived_searchable_text_disagreements"], 14)
        self.assertEqual(
            sha(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"),
            self.receipt["source_crosswalk_SHA256"],
        )

    def test_previous_1647_source_archive_sha_unchanged(self):
        self.assertEqual(
            self.cross["origin_source_overlay_sha256"],
            sha(BASE / "batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"),
        )

    def test_original_source_index_old_snapshot_unchanged(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ah.json"),
            self.receipt["prior_Western_index_SHA256"],
        )
        self.assertEqual(sha(INDEX), self.receipt["new_Western_index_SHA256"])

    def test_archive_replayed_and_untouched_canonical_data(self):
        self.assertEqual(self.release["portable_test_count"], 386)
        self.assertTrue(self.release["independent_archive_extracted_test_replay_passed"])
        self.assertTrue(self.release["member_SHA256_and_sizes_passed"])
        self.assertEqual(self.release["archive_sha256"], self.receipt["archive_SHA256"])

    def test_zero_human_predictive_accuracy_and_runtime_promotion(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.cross["empirical_real_human_validations"], 0)
        self.assertFalse(
            self.cross["model_use_as_accurate_astro_calendar_or_event_prediction_authorized"]
        )
        self.assertEqual(self.receipt["real_human_prediction_validations"], 0)
        self.assertEqual(self.receipt["runtime_promotions"], 0)

    def test_current_user_progress_points_to_new_b07ah(self):
        progress = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,515 Lilly", progress)
        self.assertIn("R12516", progress)
        self.assertIn("PARTIALLY", progress)


if __name__ == "__main__":
    unittest.main()
