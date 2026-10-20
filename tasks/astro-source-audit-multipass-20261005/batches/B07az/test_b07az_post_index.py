"""Post-index Riches source-only archival and original chapter boundary checks."""

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


class RichesSourceAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07az.json")
        cls.new = j(WEST)
        cls.rules = j(B / "RULES.json")
        cls.docs = j(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
        cls.canonical = j(B / "CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_one_exact_append_to_historical_source_history(self):
        self.assertEqual(self.old["records_count"], 12940)
        self.assertEqual(self.new["records_count"], 12969)
        self.assertEqual(self.new["batches"][:-1], self.old["batches"])
        self.assertEqual(self.new["batches"][-1]["id"], "B07az")
        self.assertEqual(sum(x["records_count"] for x in self.new["batches"]), 12969)

    def test_index_parent_and_new_sha_exact(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07az.json"),
            self.canonical["prior_Western_SHA256"],
        )
        self.assertEqual(sha(WEST), self.canonical["new_Western_SHA256"])
        self.assertEqual(self.new["source_sha256"], self.old["source_sha256"])

    def test_chinese_V7_full_binary_unchanged(self):
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07az.json"))
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), self.canonical["Chinese_V7_SHA256"])

    def test_documentary_ids_contiguous(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12941, 12970))
        )
        self.assertEqual(self.new["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_source_pages_cover_riches_only_until_next_divider(self):
        self.assertEqual(self.docs["actual_chapter_folios"], [749, 750, 751])
        self.assertEqual(self.new["next"]["chapter"], "CLXXVIII")
        self.assertEqual(self.new["next"]["pdf_page"], 785)
        self.assertEqual(self.new["next"]["printed_page"], 751)
        self.assertIn("R12970", self.new["next"]["position"])
        self.assertFalse(self.new["next"]["extracted"])

    def test_physical_source_chapter_closed_not_expert_text(self):
        self.assertEqual(self.new["read_numbered_chapters"], list(range(1, 178)))
        self.assertEqual(self.new["read_headed_units_count"], 93)
        self.assertEqual(self.new["partial_numbered_chapters"], [])
        last = self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_chapter"], "CLXXVII")
        self.assertTrue(last["complete"])
        self.assertFalse(last["all_original_early_print_critical_expert_collation_finished"])

    def test_known_merchant_no_predictions_validated(self):
        self.assertTrue(self.docs["source_is_retrospective_unblinded_individual_reading"])
        self.assertEqual(
            self.docs["independent_biographical_wealth_predicted_outcomes_validated"], 0
        )
        self.assertEqual(self.new["empirical_validations"], 0)
        self.assertEqual(self.new["runtime_promotions"], 0)

    def test_original_print_numeral_not_float(self):
        self.assertEqual(
            self.docs["original_fixed_second_cusp_print_Aquarius_degree_minute"], [23, 30]
        )
        self.assertEqual(
            self.docs["secondary_searchable_derivative_truncates_minutes"], "Aquarius 23.3"
        )

    def test_portable_archive_integrity_and_replay(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["member_SHA256_exact_bytes_passed"])
        self.assertEqual(self.release["independent_archive_extracted_test_replay_passed"], 41)
        self.assertEqual(self.release["archive_sha256"], self.canonical["archive_SHA256"])

    def test_total_Western_excludes_Chinese(self):
        self.assertEqual(self.canonical["Lilly_after"], 12969)
        self.assertEqual(self.canonical["Ptolemy_retained"], 1066)
        self.assertEqual(self.canonical["Western_after"], 14035)
        self.assertEqual(self.canonical["Chinese_V7_retained"], 355)

    def test_progress_current_has_recovery_cursor(self):
        current = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,969", current)
        self.assertIn("R12970", current)
        self.assertIn("not independently verified outcomes", current.lower())

    def test_admission_does_not_raise_personal_high_stakes_authority(self):
        self.assertFalse(self.docs["original_17th_century_natal_chart_engine_verified"])
        self.assertEqual(self.docs["runtime_promotions"], 0)
        self.assertTrue(
            all(not r["independent_real_human_prediction_validated"] for r in self.rules["rules"])
        )


if __name__ == "__main__":
    unittest.main()
