"""Post-admission exact original CLXXII closing registry invariants."""

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


class AcceptedCLXXII(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cur = j(WEST)
        cls.prev = j(B / "recovery/LILLY_INDEX_BEFORE_B07au.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.rules = j(B / "RULES.json")
        cls.doc = j(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_exact_append_only_historical_count(self):
        self.assertEqual(self.prev["records_count"], 12788)
        self.assertEqual(self.cur["records_count"], 12803)
        self.assertEqual(self.cur["batches"][:-1], self.prev["batches"])
        self.assertEqual(self.cur["batches"][-1]["id"], "B07au")

    def test_first_physical_clxxii_covered_not_predictions(self):
        self.assertEqual(self.cur["read_numbered_chapters"], list(range(1, 173)))
        self.assertEqual(self.cur["partial_numbered_chapters"], [])
        self.assertEqual(self.cur["read_headed_units_count"], 88)
        self.assertFalse(
            self.cur["completed_original_source_units_with_uncertainty"][-1][
                "source_full_original_expert_critical_edition_verified"
            ]
        )

    def test_next_distinct_clxxiii_on_same_original_page(self):
        self.assertEqual(self.cur["next"]["chapter"], "CLXXIII")
        self.assertEqual(self.cur["next"]["pdf_page"], 772)
        self.assertEqual(self.cur["next"]["printed_page"], 738)
        self.assertIn("R12804", self.cur["next"]["position"])
        self.assertFalse(self.cur["next"]["extracted"])

    def test_source_original_photos_not_mutated(self):
        for r in self.doc["source_new_edition_photos"].values():
            f = ROOT / r["repository_path"]
            self.assertEqual(sha(f), r["sha256"])
            self.assertEqual(f.stat().st_size, r["bytes"])

    def test_old_lilly_and_chinese_index_sha_preserved(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07au.json"),
            self.receipt["prior_Lilly_index_SHA256"],
        )
        self.assertEqual(sha(WEST), self.receipt["new_Lilly_index_SHA256"])
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V7_BEFORE_B07au.json"))

    def test_original_documentary_rules_SHA(self):
        self.assertEqual(self.cur["batches"][-1]["sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12789, 12804))
        )
        self.assertEqual(self.receipt["new_source_only_records"], 15)

    def test_zip_portable_testing_crc_sha(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["all_members_SHA256_and_exact_bytes_passed"])
        self.assertEqual(self.release["independent_archive_extraction_replayed_tests"], 25)
        self.assertEqual(self.receipt["archive_SHA256"], self.release["archive_sha256"])

    def test_no_authorized_high_stakes_predictor(self):
        self.assertFalse(
            self.cur["completed_original_source_units_with_uncertainty"][-1][
                "solar_return_old_epoch_ephemeris_and_meridian_parity_verified"
            ]
        )
        self.assertEqual(self.cur["empirical_validations"], 0)
        self.assertEqual(self.cur["runtime_promotions"], 0)
        self.assertEqual(self.doc["independent_real_human_prediction_validations"], 0)


if __name__ == "__main__":
    unittest.main()
