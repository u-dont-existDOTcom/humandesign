"""Guarded post-index Chinese V11 exact source-only tests, no human outcomes."""
from __future__ import annotations
import json
from hashlib import sha256
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURR=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_11SRC_LIFE.md"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def h(p):return sha256(p.read_bytes()).hexdigest()

class AfterV11SourceIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=rd(OLD)
        cls.new=rd(NEW)
        cls.rec=rd(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.src=rd(B/"ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json")
        cls.portable=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_old_and_new_original_source_totals(self):
        self.assertEqual((self.old["sum_source_annotations"],
                          self.new["sum_source_annotations"]),(519,609))
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"])
                          for x in self.new["systems"]],
                         [(210,"BZI-R0211"),(399,"ZWD-R0400")])
        self.assertEqual(self.new["accepted_batches"][-1]["added_ziwei_source_annotations"],90)

    def test_02_original_all_prior_Chinese_batches_unchanged(self):
        self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
        self.assertEqual(self.new["systems"][0],self.old["systems"][0])
        self.assertEqual(self.new["accepted_batches"][-1]["id"],"ChineseAstro-11SRC-Life")

    def test_03_old_index_SHA_saved_and_new_SHA_readback(self):
        self.assertEqual(h(OLD),self.rec["old_V10_index_sha256"])
        self.assertEqual(h(NEW),self.rec["new_V11_index_sha256"])
        self.assertEqual(h(B/"recovery/CHINESE_V10_BEFORE_11.json"),h(OLD))
        self.assertEqual(self.new["prior_index_sha256"],h(OLD))
        self.assertEqual(self.new["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V10.json")

    def test_04_source_quote_and_offset_original_sha_verified(self):
        self.assertEqual(h(B/"ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"),
                         self.rec["source_notes_sha256"])
        self.assertEqual(h(B/"SOURCE_LIFE_NEXT_FOUR_90_EXACT_OFFSET_WITNESS_V1.json"),
                         self.rec["source_witness_sha256"])
        self.assertEqual(h(B/"SOURCE_1963110_LIFE_PALACE_NEXT_FOUR_EXACT_EXCERPT.txt"),
                         self.rec["source_excerpt_sha256"])
        self.assertEqual(self.new["accepted_batches"][-1]["rules_sha256"],
                         self.rec["source_notes_sha256"])

    def test_05_source_original_90_sequential_ids(self):
        self.assertEqual([x["id"] for x in self.src["records"]],
                         [f"ZWD-R{i:04d}" for i in range(310,400)])
        self.assertEqual(self.new["systems"][1]["current_ids"],"ZWD-R0001–ZWD-R0399")
        self.assertEqual(self.new["systems"][1]["current_batch"],"ChineseAstro-11SRC-Life")

    def test_06_original_next_star_TanLang_not_falsely_annotated(self):
        self.assertEqual(self.src["next_unstudied_star_native"],"贪狼")
        self.assertEqual(self.src["next_unstudied_star_original_codepoint"],25795)
        self.assertTrue(self.src["only_four_additional_of_all_original_Life_palace_stars"])
        self.assertFalse(self.src["complete_Life_palace_source_study"])
        self.assertIn("Tan Lang",self.new["next"])
        self.assertIn("ZWD-R0400",self.new["next"])

    def test_07_source_unchanged_root_and_prior_provenance(self):
        self.assertEqual(self.new["source_manifest"],self.old["source_manifest"])
        self.assertEqual(self.new["initial_historical_witness"],self.old["initial_historical_witness"])
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],537)
        self.assertEqual(self.old["original_chinese_source_anchors_checked_against_revision"],447)

    def test_08_parent_western_snapshot_unchanged_not_current_western(self):
        self.assertEqual(h(WEST),h(B/"recovery/WESTERN_B07bc_BEFORE_11.json"))
        west=rd(WEST)
        self.assertEqual(west["records_count"],13044)
        self.assertEqual(self.new["separate_lilly_source_count_at_this_revision"],13044)
        self.assertEqual(self.rec["distinct_newer_Western_B07bg_Lilly"],13236)
        self.assertIn("not merged",self.new["source_parallel_western_history_binding"])

    def test_09_cold_original_archived_test_and_zip_checksum(self):
        self.assertEqual(self.portable["independently_cold_replayed_tests_green"],15)
        self.assertTrue(self.portable["zip_CRC_verified"])
        self.assertTrue(self.portable["all_member_SHA_and_bytes_verified"])
        self.assertEqual(self.portable["original_source_member_count"],13)
        self.assertEqual(self.rec["portable_cold_archive_sha256"],
                         self.portable["archive_sha256"])

    def test_10_current_state_prior_byte_prefix_suffix_preserved(self):
        prev=(B/"recovery/CHINESE_CURRENT_BEFORE_11.md").read_text(encoding="utf-8")
        now=CURR.read_text(encoding="utf-8")
        self.assertTrue(now.endswith(prev))
        self.assertIn("Chinese BaZi210 unchanged + ZiWei399 =609",
                      now.split("## Previous Chinese accepted source checkpoint retained",1)[0])
        self.assertTrue(LATEST.is_file())

    def test_11_source_only_old_social_medical_not_production_rules(self):
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.new["all_14_principal_stars_verified"])
        self.assertFalse(self.new["chinese_bazi_solar_term_engine_verified"])
        self.assertEqual(self.new["independently_validated_real_human_claims"],0)
        self.assertEqual(self.new["runtime_promotions"],0)

    def test_12_separate_aggregate_source_count_not_human_scores(self):
        self.assertEqual(self.new["sum_source_annotations"],609)
        self.assertEqual(self.rec["historical_source_counts_aggregate_across_separate_branches"],14911)
        self.assertEqual(13236+1066+609,14911)
        self.assertEqual(self.rec["independent_real_human_predictive_tests"],0)
        self.assertEqual(self.rec["runtime_astrological_promotions"],0)

if __name__=="__main__":unittest.main()
