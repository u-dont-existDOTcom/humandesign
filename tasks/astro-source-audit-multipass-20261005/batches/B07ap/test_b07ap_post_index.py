"""Post-admission evidence for first-edition Lilly CLXVIII, source only."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class AcceptedOriginalLillyCLXVIII(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ap.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.source = j(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_exact_historical_annotation_delta(self):
        self.assertEqual(self.old["records_count"], 12671)
        self.assertEqual(self.now["records_count"], 12704)
        self.assertEqual(self.receipt["new_source_annotations"], 33)
        self.assertEqual(sum(b["records_count"] for b in self.now["batches"]), 12704)

    def test_prior_batches_are_exactly_preserved(self):
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07ap")
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_prior_book_source_SHA_not_renormalized(self):
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ap.json"), self.receipt["prior_Western_SHA256"]
        )

    def test_original_CLXVIII_new_physical_source_closed(self):
        self.assertEqual(self.now["read_numbered_chapters"], list(range(1, 169)))
        self.assertEqual(self.old["read_numbered_chapters"], list(range(1, 168)))
        self.assertEqual(self.now["read_headed_units_count"], 84)
        self.assertEqual(self.now["partial_numbered_chapters"], [])
        done = self.now["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(done["printed_chapter"], "CLXVIII")
        self.assertTrue(done["complete"])
        self.assertFalse(done["full_source_critical_edition_complete"])

    def test_next_is_distinct_CLXIX_not_reused_heading_rule(self):
        self.assertEqual(self.now["next"]["chapter"], "CLXIX")
        self.assertEqual(self.now["next"]["pdf_page"], 763)
        self.assertEqual(self.now["next"]["printed_page"], 729)
        self.assertEqual(self.now["next"]["editorial_source_sequence_ordinal"], 169)
        self.assertFalse(self.now["next"]["include_opening_paragraph"])
        self.assertIn("R12705", self.now["next"]["position"])

    def test_33_records_are_consecutive_without_duplicate(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12672, 12705))
        )
        self.assertEqual(self.rules["first_record"], "R12672")
        self.assertEqual(self.rules["last_record"], "R12704")
        self.assertFalse(any(r["runtime_model_promoted"] for r in self.rules["rules"]))

    def test_1647_and_1659_original_images_not_modified(self):
        witness = j(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json")
        self.assertEqual(len(witness["full_image_sha_and_exact_bytes"]), 8)
        for v in witness["full_image_sha_and_exact_bytes"].values():
            f = B / v["relative_file"]
            self.assertEqual(f.stat().st_size, v["source_exact_bytes"])
            self.assertEqual(sha(f), v["photo_sha256"])

    def test_year_ruler_Pisces_remainder_arithmetic(self):
        case = self.source["source_example"]
        self.assertEqual(case["radical_pisces_degrees_minutes"], [6, 37])
        self.assertEqual(case["remainder_degrees_minutes"], [23, 23])
        self.assertEqual(case["printed_combined_time_d_h_m"], [284, 16, 28])
        self.assertFalse(case["nominal_calendar_independently_verified"])

    def test_original_source_edition_not_actual_people(self):
        self.assertFalse(self.source["full_expert_diplomatic_comparison_completed"])
        self.assertFalse(self.source["true_solar_time_epoch_lunisolar_engine_verified"])
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)

    def test_chinese_V7_not_modified(self):
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07ap.json"))
        self.assertEqual(sha(CHINA), self.receipt["Chinese_V7_SHA256"])

    def test_portable_46_and_exact_index_SHA(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["SHA_exact_bytes_passed"])
        self.assertTrue(self.release["independent_archive_replay_passed"])
        self.assertEqual(self.release["tests"], 46)
        self.assertEqual(sha(INDEX), self.receipt["new_Western_SHA256"])
        self.assertEqual(self.receipt["release_archive_SHA256"], self.release["archive_sha256"])

    def test_Western_total_separate_from_Chinese(self):
        self.assertEqual(self.receipt["Western_after"], 13770)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(12704 + 1066, 13770)

    def test_state_points_to_new_source_checkpoint(self):
        t = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,704", t)
        self.assertIn("R12705", t)
        self.assertIn("Chinese V7", t)

    def test_index_parent_source_beyond_current_scope_unchanged(self):
        self.assertEqual(self.now["ptolemy_registry"], self.old["ptolemy_registry"])
        self.assertEqual(self.now["read_numbered_chapters"][-1], 168)


if __name__ == "__main__":
    unittest.main()
