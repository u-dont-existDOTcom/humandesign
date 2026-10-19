"""Post-acceptance original 1647 Merchant Nativity exact append-only invariants."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class OriginalMerchantCanonical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ax.json")
        cls.index = j(INDEX)
        cls.chinese = j(CHINA)
        cls.canonical = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.source = j(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json")

    def test_old_count_and_exact_new_count(self):
        self.assertEqual(self.old["records_count"], 12870)
        self.assertEqual(self.index["records_count"], 12900)
        self.assertEqual(self.canonical["new_original_source_records"], 30)
        self.assertEqual(sum(x["records_count"] for x in self.index["batches"]), 12900)

    def test_append_only_one_new_source_batch(self):
        self.assertEqual(self.index["batches"][:-1], self.old["batches"])
        self.assertEqual(self.index["batches"][-1]["id"], "B07ax")
        self.assertEqual(self.index["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_original_book_source_and_prior_index_preserved(self):
        self.assertEqual(self.index["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ax.json"),
            self.canonical["prior_Western_index_SHA256"],
        )
        self.assertEqual(self.canonical["new_Western_index_SHA256"], sha(INDEX))

    def test_30_historical_source_ids_not_duplicates(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]],
            list(range(12871, 12901)),
        )
        self.assertEqual(self.rules["first_record"], "R12871")
        self.assertEqual(self.rules["last_record"], "R12900")

    def test_original_chapter_count_source_only(self):
        self.assertEqual(self.old["read_numbered_chapters"], list(range(1, 175)))
        self.assertEqual(self.index["read_numbered_chapters"], list(range(1, 176)))
        self.assertEqual(
            self.index["read_headed_units_count"],
            self.old["read_headed_units_count"] + 1,
        )
        self.assertEqual(self.index["partial_numbered_chapters"], [])

    def test_next_chapter_starts_on_same_printed_page(self):
        self.assertEqual(self.index["next"]["chapter"], "CLXXVI")
        self.assertEqual(self.index["next"]["pdf_page"], 779)
        self.assertEqual(self.index["next"]["printed_page"], 745)
        self.assertTrue(self.index["next"]["include_opening_paragraph"])
        self.assertIn("R12901", self.index["next"]["position"])
        self.assertFalse(self.index["next"]["extracted"])

    def test_original_source_math_discrepancy_not_edited_out(self):
        self.assertTrue(self.index["chapter_CLXXV_source_coverage_not_expert_critical_complete"])
        self.assertTrue(self.source["source_1647_Mercury_print_Pisces_26_06_not_silently_changed"])
        self.assertTrue(self.source["source_6_antiscia_math_equal_one_mismatch_Mercury"])

    def test_prior_Chinese_V7_exact_identity_preserved(self):
        self.assertEqual(self.chinese["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07ax.json"))
        self.assertEqual(self.canonical["Chinese_V7_SHA256"], sha(CHINA))
        self.assertEqual(self.chinese["systems"][0]["accepted_source_annotations"], 154)
        self.assertEqual(self.chinese["systems"][1]["accepted_source_annotations"], 201)

    def test_archive_verified_47_real_replays(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["member_SHA256_and_exact_bytes_passed"])
        self.assertTrue(self.release["independent_ZIP_extraction_test_replay_passed"])
        self.assertEqual(self.release["source_tests_replayed"], 47)
        self.assertEqual(self.canonical["archive_SHA256"], self.release["archive_sha256"])

    def test_source_only_known_nativity_never_human_validation(self):
        self.assertTrue(self.source["actual_known_person_case_not_independently_blinded"])
        self.assertEqual(self.index["empirical_validations"], 0)
        self.assertEqual(self.index["runtime_promotions"], 0)
        self.assertEqual(self.canonical["independent_actual_human_predictions_validated"], 0)
        self.assertFalse(
            self.source["merchant_original_chart_accurately_computed_with_original_era_ephemeris"]
        )

    def test_western_and_ptolemy_separate_history(self):
        self.assertEqual(self.canonical["Lilly_after"], 12900)
        self.assertEqual(self.canonical["Ptolemy_retained"], 1066)
        self.assertEqual(self.canonical["Western_after"], 13966)

    def test_final_progress_file_points_to_new_next_record(self):
        text = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("12,900", text)
        self.assertIn("R12901", text)
        self.assertIn("Mercury", text)


if __name__ == "__main__":
    unittest.main()
