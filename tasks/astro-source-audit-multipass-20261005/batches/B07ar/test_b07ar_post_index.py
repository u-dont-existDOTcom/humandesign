"""Append-only original Lilly CLXX source count, boundary and no-promotion."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class CLXXAccepted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = j(WEST)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ar.json")
        cls.rec = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.source = j(B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_only_one_new_batch_seventeen_new_historical_records(self):
        self.assertEqual(self.old["records_count"], 12725)
        self.assertEqual(self.new["records_count"], 12742)
        self.assertEqual(self.new["batches"][:-1], self.old["batches"])
        self.assertEqual(self.new["batches"][-1]["id"], "B07ar")
        self.assertEqual(sum(r["records_count"] for r in self.new["batches"]), 12742)

    def test_original_book_hash_preserved(self):
        self.assertEqual(self.new["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ar.json"), self.rec["old_Western_index_sha256"]
        )
        self.assertEqual(sha(WEST), self.rec["new_Western_index_sha256"])

    def test_source_chapter_physically_covered_not_predictions(self):
        self.assertEqual(self.new["read_numbered_chapters"], list(range(1, 171)))
        self.assertEqual(self.new["read_headed_units_count"], 86)
        self.assertEqual(self.new["partial_numbered_chapters"], [])
        item = self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(item["printed_chapter"], "CLXX")
        self.assertTrue(item["complete"])
        self.assertFalse(item["full_source_critical_edition_complete"])

    def test_next_printed_CLXXI_same_original_page(self):
        self.assertEqual(self.new["next"]["chapter"], "CLXXI")
        self.assertEqual(self.new["next"]["pdf_page"], 766)
        self.assertEqual(self.new["next"]["printed_page"], 732)
        self.assertFalse(self.new["next"]["include_opening_paragraph"])
        self.assertIn("R12743", self.new["next"]["position"])

    def test_17_record_IDs_and_original_12_houses(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]], list(range(12726, 12743))
        )
        self.assertEqual(
            [x["profection_house"] for x in self.source["records"][:12]], list(range(1, 13))
        )
        self.assertEqual(self.rec["new_documentary_notes"], 17)

    def test_parallel_chinese_same_sha_and_count(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07ar.json"))
        self.assertEqual(sha(CHINA), self.rec["Chinese_V7_sha256"])

    def test_separate_original_second_prints_still_hashed(self):
        for info in self.source["all_four_original_first_second_printed_photo_sha256s"].values():
            file = ROOT / info["source_relative_path"]
            self.assertEqual(file.stat().st_size, info["file_bytes"])
            self.assertEqual(sha(file), info["file_sha256"])

    def test_archive_replays_and_canonicity(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["all_member_SHA256_bytes_passed"])
        self.assertTrue(self.release["independent_extraction_test_replay_passed"])
        self.assertEqual(self.release["portable_tests"], 30)
        self.assertEqual(self.rec["archive_sha256"], self.release["archive_sha256"])
        self.assertEqual(self.new["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_zero_independent_human_life_results(self):
        self.assertEqual(self.new["empirical_validations"], 0)
        self.assertEqual(self.new["runtime_promotions"], 0)
        self.assertFalse(self.source["personal_astrological_predictive_accuracy_verified"])
        self.assertFalse(self.source["full_1647_epoch_calendar_engine_verified"])

    def test_western_total_only_one_Ptolemy_registry(self):
        self.assertEqual(self.rec["Western_after"], 13808)
        self.assertEqual(self.rec["Ptolemy_retained"], 1066)
        self.assertEqual(self.new["ptolemy_registry"], self.old["ptolemy_registry"])

    def test_new_human_readable_current_progress(self):
        t = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,742", t)
        self.assertIn("R12743", t)
        self.assertIn("Chinese V7", t)


if __name__ == "__main__":
    unittest.main()
