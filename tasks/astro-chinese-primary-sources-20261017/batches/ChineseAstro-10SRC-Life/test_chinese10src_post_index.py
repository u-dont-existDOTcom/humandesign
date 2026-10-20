"""Guarded Chinese V10 original-source append, no chart/real-person evidence."""
from __future__ import annotations

import json
import unittest
from hashlib import sha256
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=TASK/"CHINESE_SOURCE_AUDIT_INDEX_V9.json"
NEW=TASK/"CHINESE_SOURCE_AUDIT_INDEX_V10.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_10SRC_LIFE.md"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def digest(p):return sha256(p.read_bytes()).hexdigest()

class AcceptedV10ChineseSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=rd(OLD)
        cls.new=rd(NEW)
        cls.rec=rd(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.source=rd(B/"ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json")
        cls.archive=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_old_chinese_v9_index_immutable_sha(self):
        self.assertEqual(digest(OLD),"b84922b8614017fb20403f1556a885f2b3d8ed55314566140d67109e4c2022ad")
        self.assertEqual(digest(B/"recovery/CHINESE_V9_BEFORE_10.json"),digest(OLD))
        self.assertEqual(self.rec["old_V9_index_SHA256"],digest(OLD))

    def test_02_exact_new_index_519_original_source_only(self):
        self.assertEqual(digest(NEW),self.rec["new_V10_index_SHA256"])
        self.assertEqual((self.old["sum_source_annotations"],self.new["sum_source_annotations"]),
                         (430,519))
        self.assertEqual(self.new["schema"],"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V10")
        self.assertEqual(self.new["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V9.json")
        self.assertEqual(self.new["prior_index_sha256"],digest(OLD))

    def test_03_bazi_210_source_count_byte_semantics_unchanged(self):
        self.assertEqual(self.new["systems"][0],self.old["systems"][0])
        self.assertEqual(self.new["systems"][0]["accepted_source_annotations"],210)
        self.assertEqual(self.new["systems"][0]["next_id"],"BZI-R0211")

    def test_04_ziwei_220_to309_source_count_only(self):
        self.assertEqual(self.old["systems"][1]["accepted_source_annotations"],220)
        self.assertEqual(self.new["systems"][1]["accepted_source_annotations"],309)
        self.assertEqual(self.new["systems"][1]["next_id"],"ZWD-R0310")
        self.assertEqual(self.new["systems"][1]["current_batch"],"ChineseAstro-10SRC-Life")
        self.assertEqual([x["accepted_source_annotations"] for x in self.new["systems"]],
                         [210,309])

    def test_05_old_historical_batches_exact_append_only(self):
        self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
        new=self.new["accepted_batches"][-1]
        self.assertEqual(new["id"],"ChineseAstro-10SRC-Life")
        self.assertEqual((new["added_bazi_source_annotations"],
                          new["added_ziwei_source_annotations"]),(0,89))
        self.assertEqual((new["start"],new["end"]),("ZWD-R0221","ZWD-R0309"))
        self.assertEqual(new["rules_sha256"],self.rec["source_note_SHA256"])

    def test_06_original_Historical_byte_offsets_89_anchor_count(self):
        self.assertEqual(self.old["original_chinese_source_anchors_checked_against_revision"],358)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],447)
        self.assertEqual(self.source["new_documentary_Chinese_ziwei_source_note_count"],89)
        self.assertEqual(self.new["accepted_batches"][-1]["witness_sha256"],
                         self.rec["source_quote_witness_SHA256"])

    def test_07_original_transmitted_not_Ming_authentic_or_complete_Life(self):
        b=self.new["accepted_batches"][-1]
        self.assertFalse(b["source_original_early_Ming_woodblock_edition_authenticated"])
        self.assertTrue(b["full_Life_palace_section_not_complete"])
        self.assertEqual(b["next_unstudied_star"],"天同")
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.new["ziwei_complete_natal_calendar_engine_verified"])

    def test_08_original_cold_ZIP_13_entries_all_byte_checksum_integrity(self):
        self.assertEqual(self.archive["source_zip_member_count"],13)
        self.assertTrue(self.archive["ZIP_CRC_validated"])
        self.assertTrue(self.archive["ZIP_member_SHA_and_bytes_validated"])
        self.assertEqual(self.archive["independently_extracted_test_count"],17)
        self.assertTrue(self.archive["independently_extracted_tests_all_green"])
        self.assertEqual(self.archive["archive_sha256"],self.rec["cold_ZIP_SHA256"])

    def test_09_parallel_old_Western_B07bc_source_untouched(self):
        self.assertEqual(digest(WEST),
                         digest(B/"recovery/WESTERN_B07bc_BEFORE_10.json"))
        self.assertEqual(rd(WEST)["records_count"],13044)
        self.assertEqual(self.new["separate_lilly_source_count_at_this_revision"],13044)
        self.assertEqual(self.new["separate_ptolemy_source_count_at_this_revision"],1066)
        self.assertTrue(self.rec["parallel_Western_bytes_unchanged"])

    def test_10_old_V9_index_never_rewritten_as_new_accepted_V10(self):
        self.assertEqual(self.old["systems"][1]["next_id"],"ZWD-R0221")
        self.assertEqual(self.old["sum_source_annotations"],430)
        self.assertEqual(self.new["systems"][1]["current_ids"],"ZWD-R0001–ZWD-R0309")
        self.assertTrue(self.new["systems"][1]["chapter_coverage"].find("PARTIAL")>=0)

    def test_11_current_state_appended_prior_state_preserved_exact(self):
        previous=(B/"recovery/CHINESE_CURRENT_BEFORE_10.md").read_text(encoding="utf-8")
        now=CURRENT.read_text(encoding="utf-8")
        self.assertTrue(now.endswith(previous))
        title=now.split("## Previous accepted historical source retained",1)[0]
        self.assertIn("ZWD-R0310",title)
        self.assertIn("519",title)
        self.assertTrue(LATEST.is_file())

    def test_12_new_exact_source_next_codepoint_TianTong(self):
        self.assertEqual(self.new["systems"][1]["next_id"],"ZWD-R0310")
        self.assertEqual(self.source["next_star_substantive_codepoint"],22909)
        self.assertEqual(self.source["records"][-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TIANTONG_CLAIMS")

    def test_13_human_and_runtime_zero_never_changed(self):
        self.assertEqual(self.old["independently_validated_real_human_claims"],0)
        self.assertEqual(self.new["independently_validated_real_human_claims"],0)
        self.assertEqual(self.new["runtime_promotions"],0)
        self.assertEqual(self.rec["genuine_real_human_predictive_tests"],0)
        self.assertEqual(self.rec["runtime_astrological_promotions"],0)

    def test_14_separate_branch_combined_source_count_not_prediction_success(self):
        self.assertEqual(self.new["sum_source_annotations"],519)
        self.assertEqual(self.rec["latest_distinct_Western_B07bg_Lilly"],13236)
        self.assertEqual(13236+1066+519,14821)
        self.assertEqual(self.new["accepted_batches"][-1]["human_predictive_validations"],0)


if __name__=="__main__":
    unittest.main()
