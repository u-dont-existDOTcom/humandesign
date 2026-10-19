"""Post-index source-only Naibod original 1647 document checks."""

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


class NaibodPartialAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07aj.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.source = j(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")

    def test_historical_count_and_batches_only_one_added(self):
        self.assertEqual(self.old["records_count"], 12546)
        self.assertEqual(self.now["records_count"], 12567)
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07aj")
        self.assertEqual(sum(x["records_count"] for x in self.now["batches"]), 12567)

    def test_source_and_exact_sha_retained(self):
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07aj.json"), self.receipt["prior_Western_SHA256"]
        )
        self.assertEqual(sha(INDEX), self.receipt["new_Western_SHA256"])

    def test_partial_original_clxvi_not_complete(self):
        self.assertEqual(self.now["read_numbered_chapters"], self.old["read_numbered_chapters"])
        p = self.now["partial_numbered_chapters"][-1]
        self.assertFalse(p["complete"])
        self.assertEqual(p["accepted_through_pdf"], 748)
        self.assertEqual(p["next_record"], "R12568")
        self.assertFalse(p["naibod_full_critical_edition_finished"])

    def test_next_original_pdf749_printed715(self):
        self.assertEqual(self.now["next"]["chapter"], "CLXVI")
        self.assertEqual(self.now["next"]["pdf_page"], 749)
        self.assertEqual(self.now["next"]["printed_page"], 715)
        self.assertFalse(self.now["next"]["extracted"])

    def test_naibod_degree_minute_count_and_missing_label(self):
        self.assertEqual(self.source["source_degree_rows"], 90)
        self.assertEqual(self.source["source_minute_rows_visible"], 59)
        self.assertEqual(self.source["missing_original_1647_printed_minute_labels"], [27])
        self.assertEqual(self.receipt["new_source_notes"], 21)

    def test_all_rules_are_non_predictive(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12547, 12568))
        )
        self.assertTrue(all(not r["runtime_model_promoted"] for r in self.rules["rules"]))
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)

    def test_original_source_crosswalk_unchanged(self):
        self.assertEqual(
            self.receipt["source_crosswalk_SHA256"],
            sha(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"),
        )
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_chinese_source_index_unchanged(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07aj.json"))

    def test_portable_snapshot_verified(self):
        self.assertTrue(self.release["archive_crc_passed"])
        self.assertTrue(self.release["archive_members_sha_bytes_verified"])
        self.assertTrue(self.release["extracted_test_replay_passed"])
        self.assertEqual(self.release["test_count"], 160)
        self.assertEqual(self.receipt["archive_SHA256"], self.release["archive_sha256"])

    def test_western_total_separate_ptolemy(self):
        self.assertEqual(self.receipt["Western_after"], 13633)
        self.assertEqual(12567 + 1066, 13633)


if __name__ == "__main__":
    unittest.main()
