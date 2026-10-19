"""B07av post-index append-only original-source invariants and Roman variant."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class AcceptedHistoricalCLXXIII(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = j(B / "recovery/LILLY_INDEX_BEFORE_B07av.json")
        cls.after = j(INDEX)
        cls.rules = j(B / "RULES.json")
        cls.canonical = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.archive = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.roman = j(B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json")

    def test_historical_43_source_only_increment(self):
        self.assertEqual(self.before["records_count"], 12803)
        self.assertEqual(self.after["records_count"], 12846)
        self.assertEqual(self.canonical["Lilly_after"], 12846)
        self.assertEqual(self.rules["record_count"], 43)
        self.assertEqual(sum(x["records_count"] for x in self.after["batches"]), 12846)

    def test_one_batch_old_source_history_unchanged(self):
        self.assertEqual(self.after["batches"][:-1], self.before["batches"])
        self.assertEqual(self.after["batches"][-1]["id"], "B07av")
        self.assertEqual(self.after["batches"][-1]["sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07av.json"),
            self.canonical["prior_Western_index_SHA256"],
        )

    def test_one_finished_original_printed_source_chapter(self):
        self.assertEqual(self.before["read_numbered_chapters"], list(range(1, 173)))
        self.assertEqual(self.after["read_numbered_chapters"], list(range(1, 174)))
        self.assertEqual(self.before["read_headed_units_count"], 88)
        self.assertEqual(self.after["read_headed_units_count"], 89)
        self.assertEqual(self.after["partial_numbered_chapters"], [])
        self.assertTrue(
            self.after["completed_original_source_units_with_uncertainty"][-1][
                "physical_source_span_covered"
            ]
        )

    def test_1647_first_and_1659_second_printed_numerals_differ(self):
        nxt = self.after["next"]
        self.assertEqual(nxt["printed_chapter_numeral"], "CLXXIIII")
        self.assertEqual(nxt["second_1659_edition_printed_chapter_numeral"], "CLXXIV")
        self.assertEqual(nxt["editorial_source_sequence_ordinal"], 174)
        self.assertEqual(self.roman["original_1647_literal_chapter_heading"], "CHAP. CLXXIIII.")
        self.assertEqual(
            self.roman["independently_typeset_1659_literal_chapter_heading"], "CHAP. CLXXIV."
        )

    def test_next_original_printed_transits_source_is_not_accepted_yet(self):
        nxt = self.after["next"]
        self.assertEqual(nxt["chapter"], "CLXXIV")
        self.assertEqual(nxt["pdf_page"], 775)
        self.assertEqual(nxt["printed_page"], 741)
        self.assertIn("TRANSIT", nxt["heading"].upper())
        self.assertFalse(nxt["extracted"])
        self.assertEqual(self.canonical["next_R"], "R12847")

    def test_source_matrix_human_prediction_no_conflation(self):
        self.assertEqual(self.after["empirical_validations"], 0)
        self.assertEqual(self.after["runtime_promotions"], 0)
        self.assertEqual(self.canonical["real_human_outcome_predictions_validated"], 0)
        self.assertEqual(
            self.after["completed_original_source_units_with_uncertainty"][-1][
                "blind_real_people_predictions_validated"
            ],
            0,
        )
        self.assertFalse(
            self.after["completed_original_source_units_with_uncertainty"][-1][
                "full_independent_expert_diplomatic_edition_review"
            ]
        )

    def test_chinese_historical_registry_bytewise_unchanged(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07av.json"))
        self.assertEqual(sha(CHINA), self.canonical["Chinese_V7_SHA256"])

    def test_portable_archive_54_independently_replayed(self):
        self.assertTrue(self.archive["CRC_passed"])
        self.assertTrue(self.archive["all_member_sha256_and_exact_bytes_passed"])
        self.assertEqual(self.archive["independent_archive_extracted_test_replays"], 54)
        self.assertEqual(self.canonical["portable_archive_tests_replayed"], 54)
        self.assertEqual(
            self.archive["archive_sha256"], self.canonical["original_source_archive_SHA256"]
        )

    def test_exact_source_SHA_and_acceptance(self):
        self.assertEqual(sha(INDEX), self.canonical["new_Western_index_SHA256"])
        self.assertEqual(
            sha(B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"),
            self.canonical["source_original_cross_edition_next_heading_SHA256"],
        )
        self.assertEqual(
            self.canonical["source_matrix_SHA256"],
            sha(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json"),
        )

    def test_current_state_human_readable_without_false_accuracy(self):
        current = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,846", current)
        self.assertIn("CLXXIIII", current)
        self.assertIn("Zero blinded real-person", current)


if __name__ == "__main__":
    unittest.main()
