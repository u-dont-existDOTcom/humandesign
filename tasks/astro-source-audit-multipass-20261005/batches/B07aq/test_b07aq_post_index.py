"""Post-admission source fidelity for Lilly CLXIX, restored missing eleventh."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class CLXIXOriginalFullHouseCount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07aq.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.source = j(B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_historical_append_only_number(self):
        self.assertEqual(self.old["records_count"], 12704)
        self.assertEqual(self.new["records_count"], 12725)
        self.assertEqual(self.new["batches"][:-1], self.old["batches"])
        self.assertEqual(self.new["batches"][-1]["id"], "B07aq")
        self.assertEqual(sum(row["records_count"] for row in self.new["batches"]), 12725)

    def test_original_source_PDF_hash_immutable(self):
        self.assertEqual(self.new["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            self.receipt["prior_Western_index_sha256"],
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07aq.json"),
        )
        self.assertEqual(self.receipt["new_Western_index_sha256"], sha(INDEX))

    def test_complete_physical_CLXIX_not_expert_edition(self):
        self.assertEqual(self.old["read_numbered_chapters"], list(range(1, 169)))
        self.assertEqual(self.new["read_numbered_chapters"], list(range(1, 170)))
        self.assertEqual(self.new["read_headed_units_count"], 85)
        self.assertEqual(self.new["partial_numbered_chapters"], [])
        last = self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_chapter"], "CLXIX")
        self.assertTrue(last["complete"])
        self.assertFalse(last["full_source_critical_edition_complete"])

    def test_next_original_is_CLXX_not_duplicate_heading(self):
        self.assertEqual(self.new["next"]["chapter"], "CLXX")
        self.assertEqual(self.new["next"]["pdf_page"], 765)
        self.assertEqual(self.new["next"]["printed_page"], 731)
        self.assertEqual(self.new["next"]["editorial_source_sequence_ordinal"], 170)
        self.assertFalse(self.new["next"]["include_opening_paragraph"])
        self.assertIn("R12726", self.new["next"]["position"])

    def test_exact_21_records_no_recount(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12705, 12726))
        )
        self.assertEqual(self.receipt["new_historical_source_only_annotations"], 21)
        self.assertEqual(self.new["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_eleventh_original_photo_evidence_flag(self):
        self.assertTrue(self.source["source_original_1647_and_1659_both_contain_11th"])
        self.assertTrue(self.source["secondary_modern_html_transcription_omits_house11"])
        self.assertTrue(self.new["CLXIX_source_transcription_11th_missing_repair_note"])
        self.assertEqual(self.source["source_rows"][10]["profection_house_number"], 11)

    def test_all_houses_are_distinct_and_ordered(self):
        self.assertEqual(
            [r["profection_house_number"] for r in self.source["source_rows"][:12]],
            list(range(1, 13)),
        )

    def test_first_second_photo_SHA_persist(self):
        for v in self.source["source_six_original_primary_images"].values():
            p = ROOT / v["relative_file"]
            self.assertEqual(sha(p), v["sha256"])
            self.assertEqual(p.stat().st_size, v["bytes"])

    def test_chinese_V7_hash_still_unmodified(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07aq.json"))
        self.assertEqual(sha(CHINA), self.receipt["Chinese_V7_index_sha256"])

    def test_full_source_checksum_and_archive(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["all_members_SHA256_and_exact_bytes_passed"])
        self.assertTrue(self.release["independent_archive_test_replay_passed"])
        self.assertEqual(self.release["source_tests_replayed"], 35)
        self.assertEqual(self.receipt["archive_sha256"], self.release["archive_sha256"])

    def test_no_actual_life_event_predictions(self):
        self.assertEqual(self.new["empirical_validations"], 0)
        self.assertEqual(self.new["runtime_promotions"], 0)
        self.assertFalse(self.source["full_verified_astro_birth_chart_era_engine"])
        self.assertFalse(self.source["full_independent_expert_critical_edition_verified"])

    def test_Western_historical_Ptolemy_remains_distinct(self):
        self.assertEqual(self.receipt["Western_after"], 13791)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(self.new["ptolemy_registry"], self.old["ptolemy_registry"])

    def test_current_summary_human_readable(self):
        p = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
        t = p.read_text(encoding="utf-8")
        self.assertIn("12,725", t)
        self.assertIn("eleven", t)
        self.assertIn("R12726", t)

    def test_old_original_historical_batches_not_replaced(self):
        for x, y in zip(self.old["batches"], self.new["batches"], strict=False):
            self.assertEqual(x, y)


if __name__ == "__main__":
    unittest.main()
