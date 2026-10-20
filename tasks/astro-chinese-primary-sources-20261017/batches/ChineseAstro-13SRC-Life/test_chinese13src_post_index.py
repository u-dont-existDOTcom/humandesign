"""Chinese V13 post-final-principal-ZiWei source append, no human predictions."""
from __future__ import annotations
import json
from hashlib import sha256
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V12.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURR=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_13SRC_LIFE.md"
def r(p):return json.loads(p.read_text(encoding="utf-8"))
def h(p):return sha256(p.read_bytes()).hexdigest()

class V13SourceAfterGuardedAppend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=r(OLD);cls.new=r(NEW)
        cls.receipt=r(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.s=r(B/"ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json")
        cls.zip=r(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_before_after_documentary_counts(self):
        self.assertEqual(self.old["sum_source_annotations"],692)
        self.assertEqual(self.new["sum_source_annotations"],738)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.new["systems"]],
                         [(210,"BZI-R0211"),(528,"ZWD-R0529")])

    def test_02_prior_source_batches_and_bazi_untouched(self):
        self.assertEqual(self.old["accepted_batches"],self.new["accepted_batches"][:-1])
        self.assertEqual(self.old["systems"][0],self.new["systems"][0])
        self.assertEqual(self.new["accepted_batches"][-1]["id"],"ChineseAstro-13SRC-Life")
        self.assertEqual(self.new["accepted_batches"][-1]["added_ziwei_source_annotations"],46)

    def test_03_old_new_sha_previous_original_index_frozen(self):
        self.assertEqual(h(OLD),self.receipt["previous_V12_index_SHA256"])
        self.assertEqual(h(NEW),self.receipt["new_V13_index_SHA256"])
        self.assertEqual(h(B/"recovery/CHINESE_V12_BEFORE_13.json"),h(OLD))
        self.assertEqual(self.new["prior_index_sha256"],h(OLD))
        self.assertEqual(self.new["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V12.json")

    def test_04_source_quote_excerpt_original_sha(self):
        self.assertEqual(h(B/"ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"),
                         self.receipt["source_notes_SHA256"])
        self.assertEqual(h(B/"SOURCE_LIFE_FINAL_TWO_46_EXACT_OFFSET_WITNESS_V1.json"),
                         self.receipt["source_offset_witness_SHA256"])
        self.assertEqual(h(B/"SOURCE_1963110_LIFE_PALACE_FINAL_TWO_EXACT_EXCERPT.txt"),
                         self.receipt["source_excerpt_SHA256"])

    def test_05_exact_annotation_id_range_and_last_accepted(self):
        self.assertEqual([x["id"] for x in self.s["records"]],
                         [f"ZWD-R{i:04d}" for i in range(483,529)])
        self.assertEqual(self.new["systems"][1]["current_ids"],"ZWD-R0001–ZWD-R0528")
        self.assertEqual(self.new["systems"][1]["current_batch"],"ChineseAstro-13SRC-Life")

    def test_06_all_fourteen_main_star_prose_covered_only(self):
        batch=self.new["accepted_batches"][-1]
        self.assertTrue(batch["now_all_14_principal_star_source_profile_texts_completed"])
        self.assertTrue(self.receipt["all_14_principal_star_source_profiles_documented"])
        self.assertTrue(self.s["auxiliary_star_text_from_WenChang_through_Siblings_heading_unstudied"])
        self.assertFalse(self.s["complete_Life_palace_source_study"])

    def test_07_next_WenChang_auxiliary_boundary_unstudied(self):
        self.assertEqual(self.s["next_unstudied_star_native"],"文昌")
        self.assertEqual(self.s["next_unstudied_star_original_codepoint"],30135)
        self.assertIn("ZWD-R0529",self.new["next"])
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.s["complete_Life_palace_source_study"])

    def test_08_original_source_units_and_old_Wikitext_sha_unchanged(self):
        self.assertEqual(self.new["source_manifest"],self.old["source_manifest"])
        self.assertEqual(self.old["original_chinese_source_anchors_checked_against_revision"],620)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],666)
        self.assertEqual(self.new["initial_historical_witness"],self.old["initial_historical_witness"])

    def test_09_parallel_Western_snapshot_not_rebased_to_other_Western_branch(self):
        self.assertEqual(h(WEST),h(B/"recovery/WESTERN_B07bc_BEFORE_13.json"))
        self.assertEqual(r(WEST)["records_count"],13044)
        self.assertEqual(self.new["separate_lilly_source_count_at_this_revision"],13044)
        self.assertEqual(self.receipt["latest_separate_Western_B07bg_Lilly"],13236)

    def test_10_source_zip_independent_cold_SHA_replay(self):
        self.assertTrue(self.zip["zip_CRC_verified"])
        self.assertTrue(self.zip["all_member_SHA_and_bytes_verified"])
        self.assertEqual(self.zip["independently_cold_replayed_tests_green"],14)
        self.assertEqual(self.zip["original_source_member_count"],13)
        self.assertEqual(self.receipt["portable_source_archive_SHA256"],self.zip["archive_sha256"])

    def test_11_current_state_preserves_old_context_and_new_heading(self):
        before=(B/"recovery/CHINESE_CURRENT_BEFORE_13.md").read_text(encoding="utf-8")
        now=CURR.read_text(encoding="utf-8")
        self.assertTrue(now.endswith(before))
        heading=now.split("## Previous Chinese accepted source checkpoint retained",1)[0]
        self.assertIn("Chinese BaZi210 + ZiWei528=738",heading)
        self.assertTrue(LATEST.is_file())

    def test_12_no_real_human_validation_and_separate_historical_count(self):
        self.assertEqual(self.new["independently_validated_real_human_claims"],0)
        self.assertEqual(self.new["runtime_promotions"],0)
        self.assertEqual(self.receipt["real_human_blind_predictions_validated"],0)
        self.assertEqual(13236+1066+738,15040)
        self.assertEqual(self.receipt["aggregate_historical_source_annotations_across_branches"],15040)
        self.assertFalse(self.new["all_14_principal_stars_verified"])

if __name__=="__main__":unittest.main()
