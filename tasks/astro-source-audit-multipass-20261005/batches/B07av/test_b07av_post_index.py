"""Post-admission source-only Lilly CLXXIII first/second edition invariants."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = (
    ROOT / "tasks/astro-source-audit-multipass-20261005" / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CHINESE = (
    ROOT / "tasks/astro-chinese-primary-sources-20261017" / "CHINESE_SOURCE_AUDIT_INDEX_V7.json"
)


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class AcceptedCLXXIIISourceOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = j(B / "recovery/LILLY_INDEX_BEFORE_B07av.json")
        cls.after = j(INDEX)
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.source = j(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json")

    def test_before_after_Western_history_append_is_exact(self):
        self.assertEqual(self.before["records_count"], 12803)
        self.assertEqual(self.after["records_count"], 12845)
        self.assertEqual(self.after["batches"][:-1], self.before["batches"])
        self.assertEqual(self.after["batches"][-1]["id"], "B07av")
        self.assertEqual(sum(x["records_count"] for x in self.after["batches"]), 12845)

    def test_exact_original_source_Wellcome_sha_preserved(self):
        self.assertEqual(self.after["source_sha256"], self.before["source_sha256"])
        self.assertEqual(
            self.after["source_sha256"], self.source["original_full_1647_source_pdf_sha256"]
        )
        self.assertEqual(
            self.receipt["old_Western_index_sha256"],
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07av.json"),
        )

    def test_physical_source_coverage_does_not_claim_critical_fidelity(self):
        self.assertEqual(self.after["read_numbered_chapters"], list(range(1, 174)))
        self.assertEqual(self.after["read_headed_units_count"], 89)
        self.assertEqual(self.after["partial_numbered_chapters"], [])
        entry = self.after["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(entry["printed_chapter"], "CLXXIII")
        self.assertTrue(entry["complete"])
        self.assertFalse(entry["independent_original_philological_expert_verified"])
        self.assertFalse(entry["original_1647_natal_planetary_return_engine_verified"])

    def test_next_original_transit_heading_literal_1647(self):
        self.assertEqual(self.after["next"]["printed_chapter_numeral"], "CLXXIIII")
        self.assertEqual(self.after["next"]["chapter"], "CLXXIIII")
        self.assertEqual(
            self.after["next"]["second_edition_1659_printed_chapter_numeral"],
            "CLXXIV",
        )
        self.assertEqual(self.after["next"]["editorial_source_sequence_ordinal"], 174)
        self.assertEqual(self.after["next"]["pdf_page"], 775)
        self.assertEqual(self.after["next"]["printed_page"], 741)
        self.assertFalse(self.after["next"]["extracted"])

    def test_all_forty_two_source_slots_contiguous(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]], list(range(12804, 12846))
        )
        self.assertEqual(self.after["batches"][-1]["sha256"], sha(B / "RULES.json"))
        self.assertEqual(self.receipt["new_historical_documentary_notes"], 42)
        self.assertEqual(self.receipt["next_R"], "R12846")

    def test_chinese_original_index_unchanged(self):
        self.assertEqual(j(CHINESE)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINESE), self.receipt["Chinese_V7_sha256"])
        self.assertEqual(sha(CHINESE), sha(B / "recovery/CHINESE_V7_BEFORE_B07av.json"))

    def test_verified_independent_archive_replay_106(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["member_SHA256_bytes_verified"])
        self.assertTrue(self.release["independent_extracted_archive_tests_passed"])
        self.assertEqual(self.release["archive_test_replays_total"], 106)
        self.assertEqual(self.receipt["portable_archive_sha256"], self.release["archive_sha256"])

    def test_canonical_sha_and_no_numeric_natal_engine(self):
        self.assertEqual(self.receipt["new_Western_index_sha256"], sha(INDEX))
        self.assertFalse(self.source["source_old_1647_chart_mechanics_verified"])
        self.assertEqual(self.after["empirical_validations"], 0)
        self.assertEqual(self.after["runtime_promotions"], 0)
        self.assertEqual(self.receipt["independent_human_predictions_validated"], 0)

    def test_portable_documentary_source_keeps_edition_variant(self):
        row = self.source["original_1647_to_1659_first_next_transit_chapter_heading_variant"]
        self.assertEqual(
            row["source_original_first_1647_literal_printed_heading"],
            "CHAP. CLXXIIII.",
        )
        self.assertEqual(
            row["source_second_1659_literal_printed_heading"],
            "CHAP. CLXXIV.",
        )
        self.assertFalse(row["actual_person_prediction_validated"])

    def test_owner_current_state_identifies_R12846_next(self):
        progress = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,845 Lilly", progress)
        self.assertIn("R12846", progress)
        self.assertIn("CLXXIIII", progress)
        self.assertTrue(
            (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07av_RADIX_RETURNS.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
