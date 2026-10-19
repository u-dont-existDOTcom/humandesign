"""Post-index original second physical CLXVI annual-profections controls."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = P / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class AnnualProfectionsCanonical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07al.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.source = j(B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_exact_30_source_only_historical_append(self):
        self.assertEqual(self.old["records_count"], 12581)
        self.assertEqual(self.now["records_count"], 12611)
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07al")
        self.assertEqual(sum(x["records_count"] for x in self.now["batches"]), 12611)

    def test_30_new_ids_start_at_R12582(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]],
            list(range(12582, 12612)),
        )

    def test_duplicate_original_CLXVI_is_separate_second_unit(self):
        prev = self.old["completed_original_source_units_with_uncertainty"][-1]
        new = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(prev["printed_chapter"], "CLXVI")
        self.assertEqual(new["printed_chapter"], "CLXVI")
        self.assertEqual(new["editorial_source_ordinal"], 166)
        self.assertEqual(new["physical_start_pdf"], 749)
        self.assertEqual(new["physical_end_pdf"], 752)
        self.assertTrue(new["complete"])
        self.assertFalse(new["full_expert_critical_edition_complete"])

    def test_next_print_CLXVII_starts_same_p718(self):
        n = self.now["next"]
        self.assertEqual(n["editorial_source_sequence_ordinal"], 167)
        self.assertEqual(n["printed_chapter_numeral"], "CLXVII")
        self.assertEqual(n["pdf_page"], 752)
        self.assertEqual(n["printed_page"], 718)
        self.assertFalse(n["extracted"])

    def test_numbered_complete_editorial_source_ordinals(self):
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 167)))
        self.assertEqual(self.now["read_headed_units_count"], 82)
        self.assertEqual(self.now["partial_numbered_chapters"], [])

    def test_original_Merchant_glyphs_not_falsely_collated(self):
        self.assertEqual(self.source["original_merchant_table_physical_source_rows"], 72)
        self.assertFalse(self.source["all_merchant_table_zodiac_cells_expert_collated"])
        self.assertFalse(
            self.now["completed_original_source_units_with_uncertainty"][-1][
                "all_merchant_table_zodiac_cells_independently_verified"
            ]
        )

    def test_original_nonstandard_13_monthly_parts_retained(self):
        self.assertEqual(self.source["printed_monthly_profection_parts"], 13)
        self.assertEqual(self.source["printed_diurnal_sign_days_hours_minutes"], [2, 3, 54])

    def test_previous_source_index_and_photos_unchanged(self):
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07al.json"), self.receipt["prior_Western_SHA256"]
        )
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_Chinese_priorV5_exactly_unchanged(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07al.json"))

    def test_exact_final_receipts_portable_43_tests(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["members_sha256_bytes_passed"])
        self.assertTrue(self.release["independent_extracted_test_replay_passed"])
        self.assertEqual(self.release["test_count"], 43)
        self.assertEqual(self.receipt["new_Western_SHA256"], sha(INDEX))
        self.assertEqual(self.receipt["archive_SHA256"], self.release["archive_sha256"])

    def test_no_empirical_predictions_or_runtime_promotion(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.receipt["real_human_predictions_validated"], 0)
        self.assertEqual(self.source["real_person_outcome_predictions_validated"], 0)

    def test_Western_Ptolemy_Chinese_separate_counts(self):
        self.assertEqual(self.receipt["Lilly_after"], 12611)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(self.receipt["Western_after"], 13677)
        self.assertEqual(self.receipt["Chinese_V5_retained"], 262)


if __name__ == "__main__":
    unittest.main()
