"""Post-admission original first printed CLXVI source-boundary bookkeeping."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class OriginalLillyCLXVIBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ak.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.source = j(B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_exact_append_only_count(self):
        self.assertEqual(self.old["records_count"], 12567)
        self.assertEqual(self.now["records_count"], 12581)
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07ak")
        self.assertEqual(sum(x["records_count"] for x in self.now["batches"]), 12581)

    def test_close_only_physically_first_printed_CLXVI(self):
        self.assertEqual(self.old["read_numbered_chapters"], list(range(1, 165)))
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 166)))
        self.assertEqual(self.now["read_headed_units_count"], 81)
        self.assertEqual(self.now["partial_numbered_chapters"], [])
        complete = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertTrue(complete["complete"])
        self.assertEqual(complete["closed_by_batch"], "B07ak")
        self.assertFalse(complete["full_source_critical_edition_complete"])

    def test_original_duplicate_CLXVI_printed_heading_preserved(self):
        self.assertEqual(self.now["next"]["pdf_page"], 749)
        self.assertEqual(self.now["next"]["printed_page"], 715)
        self.assertEqual(self.now["next"]["printed_chapter_numeral"], "CLXVI")
        self.assertEqual(self.now["next"]["editorial_source_sequence_ordinal"], 166)
        self.assertIn("annual Profections", self.now["next"]["heading"])
        self.assertFalse(self.now["next"]["extracted"])

    def test_next_unaccepted_R_and_exact_original_photo(self):
        self.assertEqual(self.receipt["next_historical_R"], "R12582")
        self.assertEqual(self.source["cases"][0]["after_365day_year_carry"], [12, 33, 14])
        self.assertEqual(self.source["cases"][1]["after_365day_year_carry"], [20, 57, 21])
        self.assertTrue(self.source["second_distinct_original_PRINTED_CLXVI_starts_same_PDF749"])

    def test_Western_and_chinese_source_unchanged_prior_accepted(self):
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ak.json"),
            self.receipt["prior_Western_index_SHA256"],
        )
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07ak.json"))

    def test_source_critical_verification_not_falsely_completed(self):
        complete = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertFalse(complete["original_1647_full_372_source_glyphs_critically_verified"])
        self.assertTrue(complete["minute_27_print_label_omitted"])
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)

    def test_portable_archive_SHA_and_exact_index_receipt(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["all_member_SHA256_bytes_passed"])
        self.assertTrue(self.release["independent_archive_extraction_tests_passed"])
        self.assertEqual(self.release["portable_test_replays"], 26)
        self.assertEqual(self.receipt["new_Western_index_SHA256"], sha(INDEX))
        self.assertEqual(self.receipt["archive_SHA256"], self.release["archive_sha256"])

    def test_total_separate_Ptolemy_and_Chinese(self):
        self.assertEqual(self.receipt["Lilly_after"], 12581)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(self.receipt["Western_after"], 13647)
        self.assertEqual(self.receipt["Chinese_V5_retained"], 262)


if __name__ == "__main__":
    unittest.main()
