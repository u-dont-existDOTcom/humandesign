"""Post-index original Lilly 1647/1659 transit archive acceptance regression."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class TransitHistoricalIndexAdmitted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = read(INDEX)
        cls.before = read(B / "recovery/LILLY_INDEX_BEFORE_B07aw.json")
        cls.rules = read(B / "RULES.json")
        cls.source = read(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json")
        cls.record = read(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.archive = read(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_source_history_exact_25_increment(self):
        self.assertEqual(self.before["records_count"], 12845)
        self.assertEqual(self.now["records_count"], 12870)
        self.assertEqual(self.record["new_transit_documentary_source_notes"], 25)
        self.assertEqual(sum(x["records_count"] for x in self.now["batches"]), 12870)

    def test_prior_accepted_batches_unchanged(self):
        self.assertEqual(self.now["batches"][:-1], self.before["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07aw")
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_original_1647_full_pdf_provenance_unchanged(self):
        self.assertEqual(self.now["source_sha256"], self.before["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07aw.json"),
            self.record["prior_Lilly_index_SHA256"],
        )

    def test_read_numbered_chapters_only_174_appended(self):
        self.assertEqual(
            self.now["read_numbered_chapters"],
            self.before["read_numbered_chapters"] + [174],
        )
        self.assertEqual(self.now["read_headed_units_count"], 90)
        self.assertEqual(self.now["partial_numbered_chapters"], [])

    def test_next_merchant_175_chapter_separately_named(self):
        nxt = self.now["next"]
        self.assertEqual(nxt["chapter"], "CLXXV")
        self.assertEqual(nxt["printed_chapter_numeral"], "CLXXV")
        self.assertEqual(nxt["editorial_source_sequence_ordinal"], 175)
        self.assertEqual(nxt["pdf_page"], 776)
        self.assertEqual(nxt["printed_page"], 742)
        self.assertFalse(nxt["extracted"])

    def test_original_first_and_second_edition_distinction_not_lost(self):
        self.assertEqual(self.record["original_1647_chapter_numeral"], "CLXXIIII")
        self.assertEqual(self.record["original_1659_chapter_numeral"], "CLXXIV")
        self.assertTrue(self.record["source_mars_duration_days_vs_years"])
        self.assertIn(
            "two or three dayes",
            self.now["chapter_CLXXIIII_1647_vs_CLXXIV_1659_transit_source_note"],
        )
        self.assertIn(
            "two or three years",
            self.now["chapter_CLXXIIII_1647_vs_CLXXIV_1659_transit_source_note"],
        )

    def test_25_sequential_record_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]],
            list(range(12846, 12871)),
        )
        self.assertEqual(self.source["next_unaccepted_source_record"], "R12871")

    def test_all_chinese_source_state_bytes_unchanged(self):
        self.assertEqual(read(CHINESE)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINESE), sha(B / "recovery/CHINESE_V7_BEFORE_B07aw.json"))
        self.assertEqual(sha(CHINESE), self.record["Chinese_V7_SHA256"])

    def test_self_contained_archive_verification_receipt(self):
        self.assertTrue(self.archive["CRC_passed"])
        self.assertTrue(self.archive["all_members_SHA256_and_bytes_passed"])
        self.assertTrue(self.archive["independent_archive_test_replay_passed"])
        self.assertEqual(self.archive["focused_source_tests_replayed"], 42)
        self.assertEqual(self.record["release_archive_SHA256"], self.archive["archive_sha256"])

    def test_index_and_source_sha_receipt(self):
        self.assertEqual(sha(INDEX), self.record["new_Lilly_index_SHA256"])
        self.assertEqual(
            sha(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json"),
            self.record["source_document_SHA256"],
        )

    def test_western_plus_ptolemy_count_separate_chinese(self):
        self.assertEqual(self.record["Western_historical_after"], 13936)
        self.assertEqual(self.record["Lilly_after"], 12870)
        self.assertEqual(self.record["Ptolemy_retained"], 1066)
        self.assertEqual(12870 + 1066, 13936)

    def test_no_false_predictive_claim_or_critical_edition(self):
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertFalse(
            self.source["historical_source_first_1647_complete_expert_diplomatic_collation"]
        )
        self.assertFalse(self.source["modern_calendar_ephemeris_natal_house_parity_validated"])

    def test_progress_state_next_source(self):
        current = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,870", current)
        self.assertIn("R12871", current)
        self.assertTrue(
            (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aw_TRANSITS.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
