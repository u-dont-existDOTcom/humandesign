"""Post-V7 exact append-only Zi Wei source registry invariants."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parents[1]
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class AcceptedV7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = {i: j(P / f"CHINESE_SOURCE_AUDIT_INDEX_V{i}.json") for i in range(1, 8)}
        cls.notes = j(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json")
        cls.pre = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")

    def test_all_seven_index_counts(self):
        self.assertEqual(
            [self.v[i]["sum_source_annotations"] for i in range(1, 8)],
            [72, 97, 142, 207, 262, 315, 355],
        )

    def test_previous_v6_source_original_exact_sha(self):
        p = P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json"
        self.assertEqual(sha(p), self.v[7]["prior_index_sha256"])
        self.assertEqual(sha(p), self.receipt["prior_Chinese_V6_sha256"])
        self.assertEqual(sha(p), sha(B / "recovery/CHINESE_V6_BEFORE_07.json"))

    def test_ZiWei_ids_append_only(self):
        self.assertEqual(self.v[7]["systems"][1]["accepted_source_annotations"], 201)
        self.assertEqual(self.v[7]["systems"][1]["next_id"], "ZWD-R0202")
        self.assertEqual(
            [r["id"] for r in self.notes["record_rows"]], [f"ZWD-R{i:04d}" for i in range(162, 202)]
        )

    def test_bazi_entire_source_state_identical(self):
        self.assertEqual(self.v[6]["systems"][0], self.v[7]["systems"][0])
        self.assertEqual(self.v[7]["systems"][0]["accepted_source_annotations"], 154)
        self.assertEqual(self.v[7]["systems"][0]["next_id"], "BZI-R0155")

    def test_only_single_new_batch(self):
        self.assertEqual(self.v[7]["accepted_batches"][:-1], self.v[6]["accepted_batches"])
        self.assertEqual(self.v[7]["accepted_batches"][-1]["id"], "ChineseAstro-07")

    def test_note_hash_witness_and_pinned_original(self):
        last = self.v[7]["accepted_batches"][-1]
        self.assertEqual(
            last["rules_sha256"],
            sha(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(
            last["witness_sha256"], sha(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json")
        )
        self.assertEqual(
            last["source_original_raw_sha256"],
            sha(B / "SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"),
        )
        self.assertEqual(
            last["source_original_raw_sha256"],
            "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72",
        )

    def test_40_new_chinese_anchor_count(self):
        self.assertEqual(
            self.v[7]["original_chinese_source_anchors_checked_against_revision"],
            self.v[6]["original_chinese_source_anchors_checked_against_revision"] + 40,
        )
        self.assertEqual(self.v[7]["original_chinese_source_anchors_checked_against_revision"], 283)

    def test_58_archive_tests_actual_receipt(self):
        self.assertTrue(self.pre["CRC_passed"])
        self.assertTrue(self.pre["all_member_SHA256_exact_bytes_passed"])
        self.assertEqual(self.pre["extracted_original_source_tests_passed"], 58)
        self.assertEqual(self.receipt["portable_tests_replayed"], 58)
        self.assertEqual(self.receipt["portable_archive_sha256"], self.pre["archive_sha256"])

    def test_western_parallel_source_no_loss(self):
        self.assertEqual(j(WEST)["records_count"], 12611)
        self.assertEqual(sha(WEST), sha(B / "recovery/WESTERN_INDEX_B07al_BEFORE_07.json"))
        self.assertEqual(self.v[7]["separate_lilly_source_count_at_this_revision"], 12611)
        self.assertTrue(self.receipt["separate_parallel_Western_B07am_not_merged"])

    def test_uncertainty_flags_and_zero_human_promotions(self):
        self.assertFalse(self.v[7]["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.v[7]["all_14_principal_stars_verified"])
        self.assertEqual(self.v[7]["independently_validated_real_human_claims"], 0)
        self.assertEqual(self.v[7]["runtime_promotions"], 0)
        self.assertFalse(
            self.v[7]["accepted_batches"][-1]["original_calendar_or_diagram_decoder_validated"]
        )

    def test_index_sha_and_status(self):
        self.assertEqual(
            sha(P / "CHINESE_SOURCE_AUDIT_INDEX_V7.json"), self.receipt["new_Chinese_V7_sha256"]
        )
        self.assertEqual(self.receipt["Chinese_after"], 355)

    def test_current_checkpoint(self):
        state = (ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("355", state)
        self.assertIn("ZWD-R0202", state)
        self.assertTrue(
            (ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_07.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
