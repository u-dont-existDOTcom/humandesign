"""Post-admission exact append-only Lilly CLXVI source integrity."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = P / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class MaginusPartialAccepted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.now = j(INDEX)
        cls.old = j(B / "recovery/LILLY_INDEX_BEFORE_B07ai.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.source = j(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")

    def test_historical_counts_and_exact_31_append(self):
        self.assertEqual(self.old["records_count"], 12515)
        self.assertEqual(self.now["records_count"], 12546)
        self.assertEqual(len(self.rules["rules"]), 31)
        self.assertEqual(self.receipt["new_source_only_records"], 31)
        self.assertEqual(sum(x["records_count"] for x in self.now["batches"]), 12546)

    def test_bytewise_prior_batch_list(self):
        self.assertEqual(self.now["batches"][:-1], self.old["batches"])
        self.assertEqual(self.now["batches"][-1]["id"], "B07ai")
        self.assertEqual(self.now["batches"][-1]["sha256"], sha(B / "RULES.json"))

    def test_original_source_identity_unchanged(self):
        self.assertEqual(self.now["source_sha256"], self.old["source_sha256"])
        self.assertEqual(
            self.now["source_sha256"], self.source["source_original_1647_full_PDF_sha256"]
        )
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07ai.json"),
            self.receipt["prior_Lilly_index_SHA256"],
        )

    def test_partial_chapter_has_not_been_promoted_as_complete(self):
        self.assertEqual(self.now["read_numbered_chapters"], self.old["read_numbered_chapters"])
        self.assertEqual(self.now["read_headed_units_count"], self.old["read_headed_units_count"])
        self.assertFalse(self.now["partial_numbered_chapters"][-1]["complete"])
        self.assertEqual(self.now["partial_numbered_chapters"][-1]["next_record"], "R12547")
        self.assertEqual(self.now["partial_numbered_chapters"][-1]["next_unaccepted_pdf"], 747)

    def test_exact_source_next_R12547_and_naibod(self):
        self.assertEqual(self.now["next"]["chapter"], "CLXVI")
        self.assertEqual(self.now["next"]["pdf_page"], 747)
        self.assertEqual(self.now["next"]["printed_page"], 713)
        self.assertIn("Naibod", self.now["next"]["heading"])
        self.assertFalse(self.now["next"]["extracted"])

    def test_24_year_exact_rational_conventions(self):
        years = self.source["original_24_years_source_table"]
        self.assertEqual(len(years), 24)
        self.assertEqual(years[12]["analytical_54_times_years_arcminutes"], 702)
        self.assertEqual(years[21]["analytical_54_times_years_arcminutes"], 1188)
        self.assertEqual(
            [
                e["true_arithmetic_remaining_arcminutes"]
                for e in self.source["historical_arithmetic_cases"]
            ],
            [13, 4],
        )
        self.assertEqual(
            [
                e["original_printed_fraction_arcminutes"]
                for e in self.source["historical_arithmetic_cases"]
            ],
            [42, 48],
        )

    def test_archive_receipt_replays_70(self):
        self.assertEqual(self.release["source_tests_replayed"], 70)
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["independent_archive_extracted_test_replay_passed"])
        self.assertEqual(self.receipt["portable_replayed_tests"], 70)
        self.assertEqual(self.receipt["release_archive_SHA256"], self.release["archive_SHA256"])

    def test_no_mutation_to_chinese_index(self):
        self.assertEqual(sha(CHINA), sha(B / "recovery/CHINESE_V5_BEFORE_B07ai.json"))
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(self.receipt["Chinese_V5_SHA256"], sha(CHINA))

    def test_index_receipt_exact_hash(self):
        self.assertEqual(self.receipt["new_Lilly_index_SHA256"], sha(INDEX))
        self.assertEqual(
            self.receipt["source_records_SHA256"],
            sha(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json"),
        )

    def test_all_old_record_ids_still_consistent(self):
        ids = [r["record_number"] for r in self.rules["rules"]]
        self.assertEqual(ids, list(range(12516, 12547)))
        self.assertEqual(self.rules["first_record"], "R12516")
        self.assertEqual(self.rules["last_record"], "R12546")

    def test_no_personal_high_stakes_prediction_engine(self):
        self.assertEqual(self.now["empirical_validations"], 0)
        self.assertEqual(self.now["runtime_promotions"], 0)
        self.assertFalse(self.source["natal_1647_ascendant_and_true_solar_time_engine_validated"])
        self.assertFalse(self.source["full_original_CLXVI_chapter_complete"])

    def test_older_source_state_recoverable(self):
        self.assertTrue((B / "recovery/CURRENT_BEFORE_B07ai.md").stat().st_size > 100)
        progress = (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("12,546", progress)
        self.assertIn("R12547", progress)


if __name__ == "__main__":
    unittest.main()
