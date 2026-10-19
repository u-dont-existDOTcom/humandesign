"""Append-only B07aw original transits registry integrity and active next source."""

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


class TransitAppendOnlyAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(WEST)
        cls.before = j(B / "recovery/LILLY_INDEX_BEFORE_B07aw.json")
        cls.record = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.data = j(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json")
        cls.archive = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_previous_and_current_lilly_counter(self):
        self.assertEqual(self.before["records_count"], 12846)
        self.assertEqual(self.now["records_count"], 12868)
        self.assertEqual(self.record["added_historical_source_notes"], 22)
        self.assertEqual(sum(b["records_count"] for b in self.now["batches"]), 12868)

    def test_prior_accepted_batches_identical(self):
        self.assertEqual(self.now["batches"][:-1], self.before["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07aw")
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_original_1647_full_book_source_same_hash(self):
        self.assertEqual(self.now["source_sha256"], self.before["source_sha256"])
        self.assertEqual(
            self.now["source_sha256"], self.data["source_original_1647_full_book_pdf_sha256"]
        )

    def test_old_index_can_be_recovered_exact(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07aw.json"), self.record["old_Lilly_index_SHA256"]
        )
        self.assertEqual(sha(WEST), self.record["new_Lilly_index_SHA256"])

    def test_one_physical_transit_chapter_completed_not_prediction_validation(self):
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 175)))
        self.assertEqual(self.now["read_headed_units_count"], 90)
        self.assertEqual(self.now["partial_numbered_chapters"], [])
        latest = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(latest["original_first_1647_chapter_numeral"], "CLXXIIII")
        self.assertEqual(latest["second_1659_chapter_numeral"], "CLXXIV")
        self.assertTrue(latest["source_physically_complete"])
        self.assertFalse(latest["critical_two_reader_source_collation_complete"])

    def test_next_CLXXV_distinct_source_boundary(self):
        nxt = self.now["next"]
        self.assertEqual(nxt["chapter"], "CLXXV")
        self.assertEqual(nxt["editorial_source_sequence_ordinal"], 175)
        self.assertEqual(nxt["pdf_page"], 776)
        self.assertEqual(nxt["printed_page"], 742)
        self.assertFalse(nxt["extracted"])
        self.assertEqual(self.record["next_R"], "R12869")

    def test_exact_source_transcription_errors_preserved(self):
        self.assertEqual(self.record["Mars_duration_original_printings"], ["dayes", "yeares"])
        self.assertEqual(
            self.record["Ascendant_favorable_planets_original_printings"], ["Jupiter", "Venus"]
        )
        self.assertTrue(
            self.data["original_1647_1659_Jupiter_or_Venus_ascendant_not_secondary_Jupiter_or_Mars"]
        )

    def test_raw_chinese_registry_unmodified(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07aw.json"))
        self.assertEqual(sha(CHINA), self.record["Chinese_V7_SHA256"])

    def test_portable_archive_replayed_source_tests(self):
        self.assertEqual(self.archive["independent_ZIP_test_replay_passed"], 40)
        self.assertEqual(self.record["portable_test_replays"], 40)
        self.assertEqual(self.record["archive_SHA256"], self.archive["archive_sha256"])
        self.assertTrue(self.archive["crc_passed"])
        self.assertTrue(self.archive["member_hashes_and_bytes_passed"])

    def test_pinned_original_photo_source_sha(self):
        self.assertEqual(
            sha(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json"),
            self.record["source_SHA256"],
        )
        self.assertEqual(sha(B / "RULES.json"), self.record["rules_SHA256"])

    def test_no_human_predictions_validated(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertFalse(self.data["chart_derived_human_event_prediction_accuracy_validated"])
        self.assertEqual(self.record["empirical_human_outcome_validations"], 0)
        self.assertEqual(self.record["runtime_promotions"], 0)

    def test_western_and_chinese_summaries_do_not_pool(self):
        self.assertEqual(self.record["Western_after"], 12868 + 1066)
        self.assertEqual(self.record["Chinese_V7_retained"], 355)
        self.assertEqual(self.record["Ptolemy_retained"], 1066)

    def test_owner_visible_source_progress(self):
        text = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,868 Lilly", text)
        self.assertIn("R12869", text)
        self.assertTrue(
            (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aw_TRANSITS.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
