"""Guard post-admission original Lilly 1647/1659 merchant Friends source."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class MerchantFriendsOriginalIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = read(B / "recovery/LILLY_INDEX_BEFORE_B07bh.json")
        cls.new = read(INDEX)
        cls.receipt = read(B / "CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.rules = read(B / "RULES.json")
        cls.manifest = read(B / "ORIGINAL_SOURCE_WITNESS_20261021.json")
        cls.archive = read(B / "SOURCE_RELEASE_RECEIPT_20261021.json")

    def test_01_exact_append_35_not_repeat_prior(self):
        self.assertEqual(self.old["records_count"], 13236)
        self.assertEqual(self.new["records_count"], 13271)
        self.assertEqual(sum(b["records_count"] for b in self.new["batches"]), 13271)
        self.assertEqual(self.new["batches"][-1]["id"], "B07bh")
        self.assertEqual(self.new["batches"][-1]["records_count"], 35)

    def test_02_preserves_all_prior_batch_definitions_unchanged(self):
        self.assertEqual(self.new["batches"][:-1], self.old["batches"])

    def test_03_preserves_source_and_ptolemy_identity(self):
        for k in (
            "source_id",
            "source_sha256",
            "ptolemy_registry",
            "original_printed_chapter_heading_crosswalk",
        ):
            self.assertEqual(self.old[k], self.new[k], k)
        self.assertEqual(self.new["empirical_validations"], 0)
        self.assertEqual(self.new["runtime_promotions"], 0)

    def test_04_preserves_old_original_units_and_adds_exact_new(self):
        self.assertEqual(
            self.new["completed_original_source_units_with_uncertainty"][:-1],
            self.old["completed_original_source_units_with_uncertainty"],
        )
        last = self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["source_batch"], "B07bh")
        self.assertEqual(last["editorial_ordinal"], 185)
        self.assertEqual(last["printed_chapter"], "CLXXXIII")
        self.assertEqual(last["printed_folios"], [762, 763])
        self.assertEqual(last["historical_end"], "R13271")
        self.assertTrue(last["source_merchant_known_before_astrologer_wrote_example"])
        self.assertFalse(last["actual_known_merchant_friends_or_trade_profit_verified"])

    def test_05_read_headed_and_numbered_increment_one(self):
        self.assertEqual(self.old["read_headed_units_count"], 100)
        self.assertEqual(self.new["read_headed_units_count"], 101)
        self.assertEqual(self.old["read_numbered_chapters"], list(range(1, 185)))
        self.assertEqual(self.new["read_numbered_chapters"], list(range(1, 186)))

    def test_06_literal_next_imprisonment_and_later_death_separate(self):
        n = self.new["next"]
        self.assertEqual(n["chapter"], "CLXXXIV")
        self.assertEqual(n["printed_chapter_numeral"], "CLXXXIV")
        self.assertEqual(n["editorial_source_sequence_ordinal"], 186)
        self.assertEqual(n["pdf_page"], 797)
        self.assertEqual(n["printed_page"], 763)
        self.assertFalse(n["extracted"])
        self.assertIn("CLXXXV", n["position"])

    def test_07_previous_index_sha_and_new_index_sha(self):
        self.assertEqual(
            sha(B / "recovery/LILLY_INDEX_BEFORE_B07bh.json"),
            self.receipt["old_index_sha256"],
        )
        self.assertEqual(sha(INDEX), self.receipt["new_index_sha256"])

    def test_08_lilly_1647_and_1659_pair_photo_source(self):
        self.assertEqual(len(self.manifest["photos"]), 5)
        for entry in self.manifest["photos"].values():
            self.assertEqual(sha(B / entry["path"]), entry["sha256"])
        self.assertEqual(sha(B / "RULES.json"), self.receipt["rules_sha256"])

    def test_09_chinese_inherited_V7_byte_identical(self):
        self.assertEqual(sha(CHINESE), sha(B / "recovery/CHINESE_V7_BEFORE_B07bh.json"))
        self.assertEqual(sha(CHINESE), self.receipt["Chinese_V7_SHA256_unchanged"])

    def test_10_second_chinese_V14_count_is_outside_this_index(self):
        self.assertEqual(self.receipt["Chinese_V14_separate_accepted_source_notes"], 796)
        self.assertEqual(self.receipt["Ptolemy_retained"], 1066)
        self.assertEqual(self.receipt["Western_after"], 14337)
        self.assertFalse(any(x["id"].startswith("Chinese") for x in self.new["batches"]))

    def test_11_cold_zip_replay_and_owner_download_location(self):
        self.assertEqual(self.archive["independent_cold_source_tests_green"], 18)
        self.assertTrue(self.archive["all_members_exact_SHA_and_bytes_check_passed"])
        self.assertTrue(self.archive["zip_CRC_check_passed"])
        self.assertEqual(
            sha(self.archive["archive_path_on_owner_machine"]),
            self.receipt["portable_archive_sha256"],
        )
        self.assertIn("Téléchargements", self.archive["archive_path_on_owner_machine"])

    def test_12_zero_new_human_evidence_or_live_scorer(self):
        self.assertEqual(self.receipt["real_human_blind_predictive_validations"], 0)
        self.assertEqual(self.receipt["runtime_astrological_promotions"], 0)
        self.assertFalse(
            any(x["independent_human_blind_forecast_tested"] for x in self.rules["rules"])
        )
        self.assertFalse(any(x["runtime_astrological_rule_promoted"] for x in self.rules["rules"]))

    def test_13_latest_current_progress_record_hashes(self):
        for path, key in (
            (
                ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261021_B07bh_FRIENDS.md",
                "latest_sha256",
            ),
            (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md", "current_sha256"),
            (ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md", "progress_sha256"),
        ):
            self.assertEqual(sha(path), self.receipt[key])


if __name__ == "__main__":
    unittest.main()
