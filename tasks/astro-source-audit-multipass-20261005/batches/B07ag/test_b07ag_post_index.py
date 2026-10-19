"""Post-admission original Lilly CLXVI partial registry invariants, no full chapter."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class CLXVIPartialCanonical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ag.json")
        cls.rules = j(B / "RULES.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.canonical = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.china = j(CHINA)

    def test_source_history_count_progression(self):
        self.assertEqual(self.old["records_count"], 12472)
        self.assertEqual(self.index["records_count"], 12501)
        self.assertEqual(self.canonical["new_source_only_records"], 29)
        self.assertEqual(
            self.index["records_count"], sum(b["records_count"] for b in self.index["batches"])
        )

    def test_one_and_only_one_historical_append(self):
        self.assertEqual(
            [a["id"] for a in self.index["batches"]],
            [a["id"] for a in self.old["batches"]] + ["B07ag"],
        )

    def test_source_sha_preserved(self):
        self.assertEqual(self.index["source_sha256"], self.old["source_sha256"])
        self.assertEqual(self.index["ptolemy_registry"], self.old["ptolemy_registry"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ag.json"),
            self.canonical["original_index_SHA256"],
        )

    def test_record_IDs_not_repeated(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12473, 12502))
        )
        self.assertEqual(self.index["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_partial_clxvi_does_not_count_complete_chapter(self):
        self.assertEqual(self.index["read_numbered_chapters"], self.old["read_numbered_chapters"])
        self.assertEqual(self.index["read_headed_units_count"], self.old["read_headed_units_count"])
        self.assertEqual(len(self.index["partial_numbered_chapters"]), 1)
        self.assertFalse(self.index["partial_numbered_chapters"][0]["complete"])
        self.assertEqual(self.index["partial_numbered_chapters"][0]["printed_chapter"], "CLXVI")

    def test_same_clxvi_continues_on_first_edition_table(self):
        self.assertEqual(self.index["next"]["chapter"], "CLXVI")
        self.assertEqual(self.index["next"]["pdf_page"], 745)
        self.assertEqual(self.index["next"]["printed_page"], 711)
        self.assertFalse(self.index["next"]["extracted"])
        self.assertIn("R12502", self.index["next"]["position"])

    def test_historical_source_old_rate_table_not_promoted(self):
        self.assertFalse(
            self.index["partial_numbered_chapters"][0][
                "original_numerical_tables_exhaustively_verified"
            ]
        )
        self.assertIn(
            "not yet", self.index["chapter_CLXVI_partial_original_opening_acceptance_note"]
        )
        self.assertEqual(self.index["runtime_promotions"], 0)
        self.assertEqual(self.index["empirical_validations"], 0)

    def test_chinese_V5_still_262(self):
        self.assertEqual(self.china["sum_source_annotations"], 262)
        self.assertEqual(sha(CHINA), self.canonical["Chinese_V5_SHA256"])
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07ag.json"))
        self.assertEqual(self.china["runtime_promotions"], 0)

    def test_original_1647_historical_rate_discrepancy_kept(self):
        r = self.rules["rules"][-1]
        self.assertEqual(r["original_printed_next_day_sun_longitude_degrees_minutes"], [7, 36])
        self.assertEqual(r["modern_derivative_mistranscribed_next_day_sun_longitude"], [7, 37])

    def test_archive_and_canonical_receipt_agree(self):
        self.assertEqual(self.release["portable_test_replays"], 43)
        self.assertTrue(self.release["independently_extracted_tests_passed"])
        self.assertTrue(self.release["all_member_SHA256_and_sizes_passed"])
        self.assertEqual(self.release["archive_sha256"], self.canonical["release_archive_SHA256"])
        self.assertEqual(sha(INDEX), self.canonical["new_index_SHA256"])

    def test_previous_Western_current_recoverable(self):
        self.assertTrue((B / "recovery/CURRENT_BEFORE_B07ag.md").stat().st_size > 100)
        text = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,501 accepted Lilly", text)
        self.assertIn("partial", text.lower())

    def test_no_claim_of_full_physical_original_CLXVI(self):
        self.assertFalse(self.rules["original_full_chapter_CLXVI_completed"])
        self.assertFalse(
            self.rules["all_372_1647_original_annual_rate_glyphs_independently_verified"]
        )
        self.assertFalse(self.rules["historical_arc_to_age_engine_verified"])

    def test_Western_total_excludes_separate_Chinese(self):
        self.assertEqual(self.canonical["Western_historical_after"], 13567)
        self.assertEqual(self.canonical["ptolemy_retained"], 1066)
        self.assertEqual(self.canonical["Chinese_V5_retained"], 262)
        self.assertEqual(12501 + 1066, 13567)


if __name__ == "__main__":
    unittest.main()
