"""Append-only original Chinese Di Tian Sui V6 source-registry acceptance."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class AcceptedChineseV6(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.versions = {i: j(P / f"CHINESE_SOURCE_AUDIT_INDEX_V{i}.json") for i in range(1, 7)}
        cls.pre = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.notes = j(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json")
        cls.meta = j(B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json")
        cls.witness = j(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json")

    def test_all_six_versions_exact_counts(self):
        self.assertEqual(
            [self.versions[i]["sum_source_annotations"] for i in range(1, 7)],
            [72, 97, 142, 207, 262, 315],
        )

    def test_old_index_SHA_recoverable_unchanged(self):
        path = P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json"
        self.assertEqual(sha(path), self.versions[6]["prior_index_sha256"])
        self.assertEqual(sha(path), self.receipt["prior_Chinese_V5_SHA256"])
        self.assertEqual(sha(path), sha(B / "recovery/CHINESE_V5_BEFORE_06.json"))

    def test_only_one_new_source_batch(self):
        old = [b["id"] for b in self.versions[5]["accepted_batches"]]
        new = [b["id"] for b in self.versions[6]["accepted_batches"]]
        self.assertEqual(new, old + ["ChineseAstro-06"])
        self.assertEqual(new[-1], "ChineseAstro-06")

    def test_new_bazi_source_count_and_next(self):
        b = self.versions[6]["systems"][0]
        self.assertEqual(b["accepted_source_annotations"], 154)
        self.assertEqual(b["next_id"], "BZI-R0155")
        self.assertEqual(b["current_batch"], "ChineseAstro-06")

    def test_ziwei_entire_current_subtree_byte_equivalent(self):
        self.assertEqual(self.versions[6]["systems"][1], self.versions[5]["systems"][1])
        self.assertEqual(self.versions[6]["systems"][1]["accepted_source_annotations"], 161)

    def test_sequential_fifty_three_new_ids(self):
        self.assertEqual(
            [r["id"] for r in self.notes["records"]], [f"BZI-R{x:04d}" for x in range(102, 155)]
        )
        self.assertEqual(self.receipt["new_Chinese_primary_source_notes"], 53)

    def test_source_manifest_and_quote_hashes(self):
        record = self.versions[6]["accepted_batches"][-1]
        self.assertEqual(
            record["rules_sha256"],
            sha(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"),
        )
        self.assertEqual(
            record["witness_sha256"],
            sha(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json"),
        )
        self.assertEqual(
            record["source_manifest_sha256"],
            sha(B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json"),
        )
        self.assertEqual(self.notes["source_annotations_added"], 53)

    def test_oldid_matches_full_original_raw_pages(self):
        self.assertEqual(len(self.meta), 6)
        for section, src in self.meta.items():
            file = B / "evidence" / src["raw_file_local"]
            self.assertEqual(sha(file), src["source_sha256"], section)
            self.assertEqual(file.stat().st_size, src["source_bytes"], section)
        self.assertEqual(self.witness["matched_independently_pinned_source_quotes"], 53)

    def test_exact_frozen_quote_numerical_delta(self):
        self.assertEqual(
            self.versions[5]["original_chinese_source_anchors_checked_against_revision"],
            190,
        )
        self.assertEqual(
            self.versions[6]["original_chinese_source_anchors_checked_against_revision"],
            243,
        )

    def test_previous_western_history_is_pinned_not_implicitly_merged(self):
        self.assertEqual(j(WEST)["records_count"], 12611)
        self.assertEqual(j(WEST)["batches"][-1]["id"], "B07al")
        self.assertEqual(self.versions[6]["separate_lilly_source_count_at_this_revision"], 12611)
        self.assertEqual(sha(WEST), sha(B / "recovery/WESTERN_INDEX_B07al_BEFORE_06.json"))

    def test_prior_bazi_files_append_not_replaced(self):
        self.assertEqual(
            self.versions[6]["systems"][0]["source_files"][:-1],
            self.versions[5]["systems"][0]["source_files"],
        )
        self.assertTrue(
            self.versions[6]["systems"][0]["source_files"][-1].endswith(
                "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"
            )
        )

    def test_replay_receipt_only_new_69_focused_tests(self):
        self.assertEqual(self.pre["source_focused_tests_replayed"], 69)
        self.assertTrue(self.pre["archive_crc_passed"])
        self.assertTrue(self.pre["all_file_SHA256_and_exact_bytes_passed"])
        self.assertTrue(self.pre["independently_extracted_archive_tests_passed"])
        self.assertFalse(self.pre["unmodified_historical_Chinese_earlier_test_suites_replayed"])

    def test_index_receipt_sha(self):
        self.assertEqual(
            self.receipt["new_Chinese_V6_SHA256"], sha(P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json")
        )
        self.assertEqual(self.receipt["archive_SHA256"], self.pre["archive_sha256"])

    def test_parent_remains_open_no_predictive_validation(self):
        self.assertFalse(self.versions[6]["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.versions[6]["chinese_bazi_solar_term_engine_verified"])
        self.assertFalse(self.versions[6]["all_14_principal_stars_verified"])
        self.assertEqual(self.versions[6]["independently_validated_real_human_claims"], 0)
        self.assertEqual(self.versions[6]["runtime_promotions"], 0)

    def test_state_current_mentions_v6_next(self):
        current = (ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("315", current)
        self.assertIn("BZI-R0155", current)
        self.assertIn("ZWD-R0162", current)
        self.assertTrue(
            (ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_06.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
