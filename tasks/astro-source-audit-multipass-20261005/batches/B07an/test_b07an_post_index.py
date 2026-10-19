"""B07an appended Lilly original profection time source without changing prior history."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class ProfectionTimePartialCanonical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07an.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.archive = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.source = j(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json")

    def test_only_exact_append_changes_record_count(self):
        self.assertEqual(self.old["records_count"], 12625)
        self.assertEqual(self.now["records_count"], 12649)
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07an")
        self.assertEqual(self.now["batches"][-1]["records_count"], 24)
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))
        self.assertEqual(sum(v["records_count"] for v in self.now["batches"]), 12649)

    def test_previously_accepted_original_source_sha_same(self):
        self.assertEqual(self.old["source_sha256"], self.now["source_sha256"])
        self.assertEqual(
            self.receipt["prior_Lilly_index_SHA256"],
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07an.json"),
        )

    def test_unaccepted_clxvii_source_remains_partial(self):
        self.assertEqual(self.now["read_numbered_chapters"], self.old["read_numbered_chapters"])
        self.assertEqual(self.now["read_headed_units_count"], self.old["read_headed_units_count"])
        self.assertEqual(len(self.now["partial_numbered_chapters"]), 1)
        p = self.now["partial_numbered_chapters"][0]
        self.assertFalse(p["complete"])
        self.assertEqual(p["next_unaccepted_pdf"], 759)
        self.assertEqual(p["next_record"], "R12650")
        self.assertFalse(p["all_original_degree_minute_table_glyphs_critically_verified"])

    def test_1647_source_next_physical_p725_and_same_chapter(self):
        self.assertEqual(self.now["next"]["pdf_page"], 759)
        self.assertEqual(self.now["next"]["printed_page"], 725)
        self.assertEqual(self.now["next"]["chapter"], "CLXVII")
        self.assertFalse(self.now["next"]["extracted"])
        self.assertIn("R12650", self.now["next"]["position"])

    def test_no_lost_prior_chinese_source(self):
        self.assertEqual(j(CHINESE)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINESE), sha(B / "recovery/CHINESE_V7_BEFORE_B07an.json"))
        self.assertEqual(self.receipt["Chinese_V7_SHA256"], sha(CHINESE))

    def test_source_error_preserved_literal_and_analytical(self):
        third = self.source["original_printed_1647_date_table_and_examples"][2]
        self.assertEqual(third["printed_arc"], [6, 23])
        self.assertEqual(third["printed_minute_row_actually_used"][0], 37)
        self.assertEqual(third["mathematically_corresponding_minute_row"][0], 23)
        self.assertEqual(third["printed_total_dhm"], [80, 13, 21])
        self.assertEqual(third["recalculated_total_using_23_row_dhm"], [77, 17, 11])

    def test_source_scope_only_nine_sampled_cells(self):
        self.assertEqual(len(self.source["source_sample_one_reader_table_rows"]), 9)
        self.assertFalse(self.source["source_full_30_and_60_digit_columns_critically_collated"])
        self.assertFalse(self.source["source_365day_month_table_all_cells_critically_collated"])

    def test_independent_archived_test_verification(self):
        self.assertEqual(self.archive["source_tests_replayed"], 40)
        self.assertTrue(self.archive["CRC_passed"])
        self.assertTrue(self.archive["member_SHA256_bytes_passed"])
        self.assertTrue(self.archive["independent_ZIP_extraction_test_replay_passed"])
        self.assertEqual(self.receipt["archive_SHA256"], self.archive["archive_sha256"])
        self.assertEqual(self.receipt["new_Lilly_index_SHA256"], sha(INDEX))

    def test_separate_Ptolemy_and_chinese_counts(self):
        self.assertEqual(self.receipt["Lilly_after"], 12649)
        self.assertEqual(self.receipt["Western_after"], 13715)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(self.receipt["Chinese_V7_retained"], 355)

    def test_no_actual_person_predicted_or_model_promoted(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertFalse(self.source["original_1647_natal_chart_ephemeris_conversion_verified"])
        self.assertEqual(self.source["independent_real_person_predictions_validated"], 0)
        for r in self.rules["rules"]:
            self.assertFalse(r["runtime_model_promoted"])


if __name__ == "__main__":
    unittest.main()
