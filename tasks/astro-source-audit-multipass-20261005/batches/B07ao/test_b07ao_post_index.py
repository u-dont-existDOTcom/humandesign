"""Verify Lilly original CLXVII source-only closure and next CLXVIII boundary."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class CLXVIICanonicalFinal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ao.json")
        cls.now = j(INDEX)
        cls.r = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_append_only_22_new_historical_document_records(self):
        self.assertEqual(self.old["records_count"], 12649)
        self.assertEqual(self.now["records_count"], 12671)
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07ao")
        self.assertEqual(self.now["batches"][-1]["records_count"], 22)
        self.assertEqual(sum(b["records_count"] for b in self.now["batches"]), 12671)

    def test_old_original_source_pdf_SHA_did_not_change(self):
        self.assertEqual(self.old["source_sha256"], self.now["source_sha256"])
        self.assertEqual(
            self.r["prior_Western_index_SHA256"], sha(B / "recovery/LILLY_INDEX_BEFORE_B07ao.json")
        )

    def test_first_CLXVII_physically_covered_and_recorded_as_uncertain(self):
        self.assertEqual(self.old["read_numbered_chapters"], list(range(1, 167)))
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 168)))
        self.assertEqual(self.now["partial_numbered_chapters"], [])
        p = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertTrue(p["complete"])
        self.assertFalse(p["critical_source_edition_all_table_cells_verified"])
        self.assertEqual(p["closed_by_batch"], "B07ao")

    def test_next_source_clxviii_same_original_p726(self):
        self.assertEqual(self.now["next"]["pdf_page"], 760)
        self.assertEqual(self.now["next"]["printed_page"], 726)
        self.assertEqual(self.now["next"]["chapter"], "CLXVIII")
        self.assertEqual(self.now["next"]["editorial_source_sequence_ordinal"], 168)
        self.assertFalse(self.now["next"]["extracted"])
        self.assertEqual(self.r["next_R"], "R12672")

    def test_no_older_lilly_data_lost(self):
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["read_headed_units_count"], 83)
        self.assertEqual(self.old["read_headed_units_count"], 82)
        self.assertEqual(sha(INDEX), self.r["new_Western_index_SHA256"])

    def test_chinese_V7_byte_identical(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07ao.json"))
        self.assertEqual(sha(CHINA), self.r["Chinese_V7_SHA256"])

    def test_new_rule_source_record_integrity(self):
        rules = j(B / "RULES.json")
        self.assertEqual(rules["record_count"], 22)
        self.assertEqual([x["record_number"] for x in rules["rules"]], list(range(12650, 12672)))
        self.assertEqual(sha(B / "RULES.json"), self.r["rules_SHA256"])

    def test_release_archive_original_sha_and_portable_tests(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["all_member_SHA256_sizes_passed"])
        self.assertTrue(self.release["extracted_test_replay_passed"])
        self.assertEqual(self.release["portable_source_tests"], 33)
        self.assertEqual(self.release["archive_sha256"], self.r["source_archive_SHA256"])

    def test_western_ptolemy_total(self):
        self.assertEqual(self.r["Lilly_after"], 12671)
        self.assertEqual(self.r["Ptolemy_retained"], 1066)
        self.assertEqual(self.r["Western_after"], 13737)

    def test_no_person_predictions_or_runtime_promotion(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.r["human_predictions_validated"], 0)
        self.assertFalse(
            j(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json")[
                "original_source_p725_full_row_by_row_critical_comparison_complete"
            ]
        )


if __name__ == "__main__":
    unittest.main()
