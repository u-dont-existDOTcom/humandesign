"""Post-index source-only 1647 Brethren admission: known-count confound explicit."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class BrethrenPostIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = j(B / "recovery/LILLY_INDEX_BEFORE_B07ba.json")
        cls.now = j(WEST)
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.source = j(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_exact_22_append_without_rewrite(self):
        self.assertEqual(self.before["records_count"], 12969)
        self.assertEqual(self.now["records_count"], 12991)
        self.assertEqual(self.now["batches"][:-1], self.before["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07ba")
        self.assertEqual(sum(x["records_count"] for x in self.now["batches"]), 12991)

    def test_original_sha_before_and_after(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ba.json"),
            self.receipt["original_Western_index_SHA256"],
        )
        self.assertEqual(sha(WEST), self.receipt["new_Western_index_SHA256"])
        self.assertEqual(self.now["source_sha256"], self.before["source_sha256"])

    def test_unmodified_chinese_index_V7(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07ba.json"))
        self.assertEqual(self.receipt["Chinese_V7_SHA256"], sha(CHINA))

    def test_previous_sibling_ruling_not_miscast_as_success(self):
        self.assertTrue(self.source["source_strict_ptolemy_interpretation_predicts_few_siblings"])
        self.assertEqual(
            [
                self.source["source_author_reports_sibling_count_brothers"],
                self.source["source_author_reports_sibling_count_sisters"],
            ],
            [7, 1],
        )
        self.assertEqual(self.source["reported_sibling_count_independent_validation_count"], 0)
        self.assertEqual(self.now["empirical_validations"], 0)

    def test_exact_new_22_ids_and_right_boundary(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12970, 12992))
        )
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))
        self.assertEqual(self.now["next"]["chapter"], "CLXXIX")
        self.assertEqual(self.now["next"]["pdf_page"], 786)
        self.assertIn("R12992", self.now["next"]["position"])

    def test_physical_complete_not_original_critical_expert(self):
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 179)))
        self.assertEqual(self.now["read_headed_units_count"], 94)
        end = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(end["printed_chapter"], "CLXXVIII")
        self.assertTrue(end["physical_source_span_covered"])
        self.assertFalse(end["independent_expert_source_critical_edition_complete"])

    def test_archive_crc_sha_bytes_and_34_tests(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["member_SHA256_and_exact_bytes_passed"])
        self.assertTrue(self.release["independent_archive_extraction_34_tests_passed"])
        self.assertEqual(self.release["archive_SHA256"], self.receipt["archive_sha256"])
        self.assertEqual(self.receipt["portable_test_replays"], 34)

    def test_western_14k_documentary_not_real_predictions(self):
        self.assertEqual(self.receipt["Lilly_after"], 12991)
        self.assertEqual(self.receipt["Western_after"], 14057)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.source["independent_prospective_real_human_prediction_successes"], 0)

    def test_recovery_checkpoint_and_novelty(self):
        current = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,991", current)
        self.assertIn("R12992", current)
        self.assertIn("few siblings", current.lower())

    def test_parent_era_ephemeris_and_human_safety_not_promoted(self):
        self.assertFalse(self.source["historical_natal_chart_engine_verified"])
        self.assertFalse(self.source["independent_expert_original_text_collation_complete"])
        self.assertTrue(all(not r["runtime_model_promoted"] for r in self.rules["rules"]))


if __name__ == "__main__":
    unittest.main()
