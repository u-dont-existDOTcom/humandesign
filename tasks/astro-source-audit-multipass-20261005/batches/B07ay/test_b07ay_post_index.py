"""Post-acceptance source-only original Lilly CLXXVI registry invariants."""

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


class PublishedManners(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(WEST)
        cls.before = j(B / "recovery/LILLY_INDEX_BEFORE_B07ay.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.rules = j(B / "RULES.json")
        cls.notes = j(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_exact_append_and_totals(self):
        self.assertEqual(self.before["records_count"], 12900)
        self.assertEqual(self.now["records_count"], 12940)
        self.assertEqual(self.now["batches"][:-1], self.before["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07ay")
        self.assertEqual(sum(b["records_count"] for b in self.now["batches"]), 12940)
        self.assertEqual(self.receipt["Western_historical_after"], 14006)

    def test_exact_old_index_sha_and_new_sha(self):
        self.assertEqual(
            self.receipt["original_Western_index_SHA256"],
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ay.json"),
        )
        self.assertEqual(self.receipt["new_Western_index_SHA256"], sha(WEST))
        self.assertEqual(self.now["source_sha256"], self.before["source_sha256"])

    def test_chinese_exact_old_snapshot_bytes(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07ay.json"))
        self.assertEqual(sha(CHINA), self.receipt["parallel_Chinese_V7_SHA256"])

    def test_no_duplicate_record_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12901, 12941))
        )
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_exclusion_of_historical_negatives_from_successes(self):
        negative = [r for r in self.rules["rules"] if r["role"] == "THROAT_MARK_SATURN_NEGATIVE"]
        self.assertEqual(len(negative), 1)
        self.assertEqual(negative[0]["literal_historical_author_observation"], "I can find none.")
        self.assertEqual(self.receipt["negative_author_observations"], 1)
        self.assertEqual(self.now["empirical_validations"], 0)

    def test_original_physical_divider_boundary(self):
        self.assertEqual(self.now["next"]["chapter"], "CLXXVII")
        self.assertEqual(self.now["next"]["pdf_page"], 783)
        self.assertEqual(self.now["next"]["printed_page"], 749)
        self.assertEqual(self.now["next"]["editorial_source_sequence_ordinal"], 177)
        self.assertFalse(self.now["next"]["extracted"])
        self.assertIn("R12941", self.now["next"]["position"])

    def test_correct_headed_unit_count(self):
        self.assertEqual(self.before["read_headed_units_count"], 91)
        self.assertEqual(self.now["read_headed_units_count"], 92)
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 177)))
        self.assertEqual(self.now["partial_numbered_chapters"], [])

    def test_critical_review_not_falsely_completed(self):
        unit = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(unit["printed_chapter"], "CLXXVI")
        self.assertTrue(unit["physical_source_span_covered"])
        self.assertFalse(unit["full_independent_classical_critical_edition_verified"])
        self.assertTrue(unit["source_case_author_knew_subject"])
        self.assertEqual(unit["empirical_human_predictions_validated"], 0)

    def test_archive_crc_bytes_replay_and_source_metadata(self):
        self.assertTrue(self.release["archive_CRC_passed"])
        self.assertTrue(self.release["archive_exact_SHA256_and_byte_size_passed"])
        self.assertEqual(self.release["independent_extracted_source_tests_passed"], 52)
        self.assertEqual(
            self.release["archive_SHA256"], self.receipt["portable_source_archive_SHA256"]
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_data_SHA256"],
            sha(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json"),
        )

    def test_progress_checkpoint_contains_explicit_owner_gap(self):
        progress = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,940", progress)
        self.assertIn("R12941", progress)
        self.assertIn("I can find none.", progress)

    def test_one_reader_is_not_independent_human_forecast(self):
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.notes["independent_actual_human_forecast_validations"], 0)
        self.assertFalse(
            self.notes["historical_original_first_printed_1616_chart_era_ephemeris_validated"]
        )


if __name__ == "__main__":
    unittest.main()
