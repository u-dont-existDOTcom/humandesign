"""Post-index append-only Lilly CLXXIX Parents source preservation regression tests."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
WEST = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class ParentsCanonicalIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = read(B / "recovery/LILLY_INDEX_BEFORE_B07bb.json")
        cls.new = read(WEST)
        cls.source = read(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json")
        cls.rules = read(B / "RULES.json")
        cls.canonical = read(B / "CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.archive = read(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_exact_source_record_count(self):
        self.assertEqual(self.old["records_count"], 12991)
        self.assertEqual(self.new["records_count"], 13017)
        self.assertEqual(self.canonical["new_historical_annotations"], 26)
        self.assertEqual(sum(x["records_count"] for x in self.new["batches"]), 13017)

    def test_old_record_batches_unchanged(self):
        self.assertEqual(self.new["batches"][:-1], self.old["batches"])
        self.assertEqual(self.new["batches"][-1]["id"], "B07bb")
        self.assertEqual(self.new["batches"][-1]["sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07bb.json"),
            self.canonical["original_index_sha256"],
        )

    def test_western_Ptolemy_same(self):
        self.assertEqual(self.new["source_sha256"], self.old["source_sha256"])
        self.assertEqual(self.new["ptolemy_registry"], self.old["ptolemy_registry"])
        self.assertEqual(self.canonical["Ptolemy_retained"], 1066)
        self.assertEqual(self.canonical["Western_after"], 13017 + 1066)

    def test_no_chinese_V7_overwritten(self):
        self.assertEqual(read(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07bb.json"))
        self.assertEqual(sha(CHINA), self.canonical["Chinese_V7_sha256"])

    def test_one_physical_Parents_chapter_closed(self):
        self.assertEqual(self.new["read_numbered_chapters"], list(range(1, 180)))
        self.assertEqual(self.new["read_headed_units_count"], 95)
        self.assertEqual(self.new["partial_numbered_chapters"], [])
        last = self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_chapter"], "CLXXIX")
        self.assertTrue(last["physical_source_span_covered"])
        self.assertFalse(last["source_expert_diplomatic_collation_complete"])

    def test_next_original_CLXXX_same_paper_printed_folio(self):
        nxt = self.new["next"]
        self.assertEqual(nxt["pdf_page"], 787)
        self.assertEqual(nxt["printed_page"], 753)
        self.assertEqual(nxt["chapter"], "CLXXX")
        self.assertEqual(nxt["editorial_source_sequence_ordinal"], 180)
        self.assertIn("Sicknesse", nxt["heading"])
        self.assertFalse(nxt["extracted"])
        self.assertEqual(self.canonical["next_R"], "R13018")

    def test_unverified_family_and_derived_parent_astro_status(self):
        last = self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertFalse(last["historical_parental_lifespan_verified"])
        self.assertFalse(last["derived_parent_birth_chart_independently_verified"])
        self.assertEqual(last["independent_human_predictions_validated"], 0)
        self.assertFalse(last["runtime_model_promoted"])

    def test_metadata_shas_match_source_and_canonical_index(self):
        self.assertEqual(
            self.canonical["source_notes_sha256"],
            sha(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(self.canonical["rules_sha256"], sha(B / "RULES.json"))
        self.assertEqual(self.canonical["new_index_sha256"], sha(WEST))

    def test_archive_42_replay_and_frozen_member_hashes(self):
        self.assertEqual(self.archive["portable_test_replays"], 42)
        self.assertTrue(self.archive["CRC_passed"])
        self.assertTrue(self.archive["member_SHA256_and_exact_bytes_passed"])
        self.assertTrue(self.archive["independent_archive_extraction_tests_passed"])
        self.assertEqual(self.archive["archive_sha256"], self.canonical["archive_sha256"])

    def test_no_prognostic_validation_or_runtime_promotions(self):
        self.assertEqual(self.new["empirical_validations"], 0)
        self.assertEqual(self.new["runtime_promotions"], 0)
        self.assertEqual(self.source["independently_validated_real_human_outcomes"], 0)
        self.assertEqual(self.source["independently_reconstructed_parent_natal_charts"], 0)

    def test_user_state_has_new_information(self):
        text = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("13,017 Lilly", text)
        self.assertIn("R13018", text)
        self.assertTrue(
            (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bb_PARENTS.md").is_file()
        )

    def test_all_26_rule_ids_and_before_after(self):
        self.assertEqual(
            [r["id"] for r in self.rules["rules"]], [f"R{i}" for i in range(12992, 13018)]
        )
        self.assertEqual(self.canonical["Lilly_before"], 12991)
        self.assertEqual(self.canonical["Lilly_after"], 13017)


if __name__ == "__main__":
    unittest.main()
