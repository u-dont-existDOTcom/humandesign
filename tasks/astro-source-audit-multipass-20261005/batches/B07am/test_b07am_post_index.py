"""B07am post-index partial historical CLXVII source integrity."""

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


class PartialCLXVIISource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07am.json")
        cls.now = j(INDEX)
        cls.rec = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.orig = j(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_old_12611_new_12625(self):
        self.assertEqual(self.old["records_count"], 12611)
        self.assertEqual(self.now["records_count"], 12625)
        self.assertEqual(sum(a["records_count"] for a in self.now["batches"]), 12625)

    def test_one_appended_batch_and_unmodified_history(self):
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07am")
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_IDs_R12612_through_R12625(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12612, 12626))
        )

    def test_original_CLXVII_remains_partial(self):
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 167)))
        self.assertEqual(self.now["read_headed_units_count"], 82)
        self.assertEqual(len(self.now["partial_numbered_chapters"]), 1)
        self.assertFalse(self.now["partial_numbered_chapters"][0]["complete"])

    def test_next_original_conversion_table_PDF755(self):
        self.assertEqual(self.now["next"]["chapter"], "CLXVII")
        self.assertEqual(self.now["next"]["pdf_page"], 755)
        self.assertEqual(self.now["next"]["printed_page"], 721)
        self.assertEqual(self.now["partial_numbered_chapters"][-1]["next_record"], "R12626")

    def test_real_sources_shas_and_recovery(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07am.json"), self.rec["old_index_sha256"]
        )
        self.assertEqual(sha(INDEX), self.rec["new_index_sha256"])
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])

    def test_chinese_262_unmodified(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07am.json"))

    def test_archival_extracted_source_tests(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["member_shas_and_sizes_passed"])
        self.assertTrue(self.release["independent_archive_replayed_24_tests"])
        self.assertEqual(self.rec["archive_sha256"], self.release["archive_sha256"])

    def test_no_human_prediction_claim(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.orig["actual_human_predictions_verified"], 0)
        self.assertEqual(self.rules["real_person_predictions_validated"], 0)

    def test_ptolemy_and_chinese_separate(self):
        self.assertEqual(self.rec["Lilly_after"], 12625)
        self.assertEqual(self.rec["Ptolemy_retained"], 1066)
        self.assertEqual(self.rec["Western_after"], 13691)
        self.assertEqual(self.rec["Chinese_V5_retained"], 262)


if __name__ == "__main__":
    unittest.main()
