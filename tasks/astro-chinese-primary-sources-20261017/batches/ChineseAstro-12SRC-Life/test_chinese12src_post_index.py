"""Chinese V12 post-original-ZiWei source append, no human predictions."""
from __future__ import annotations
import json
from hashlib import sha256
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V12.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURR=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_12SRC_LIFE.md"
def r(p):return json.loads(p.read_text(encoding="utf-8"))
def h(p):return sha256(p.read_bytes()).hexdigest()

class V12SourceAfterGuardedAppend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=r(OLD);cls.new=r(NEW)
        cls.receipt=r(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.s=r(B/"ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json")
        cls.zip=r(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_before_after_documentary_counts(self):
        self.assertEqual(self.old["sum_source_annotations"],609)
        self.assertEqual(self.new["sum_source_annotations"],692)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.new["systems"]],
                         [(210,"BZI-R0211"),(482,"ZWD-R0483")])

    def test_02_prior_source_batches_and_bazi_untouched(self):
        self.assertEqual(self.old["accepted_batches"],self.new["accepted_batches"][:-1])
        self.assertEqual(self.old["systems"][0],self.new["systems"][0])
        self.assertEqual(self.new["accepted_batches"][-1]["id"],"ChineseAstro-12SRC-Life")
        self.assertEqual(self.new["accepted_batches"][-1]["added_ziwei_source_annotations"],83)

    def test_03_old_new_sha_previous_original_index_frozen(self):
        self.assertEqual(h(OLD),self.receipt["previous_V11_index_SHA256"])
        self.assertEqual(h(NEW),self.receipt["new_V12_index_SHA256"])
        self.assertEqual(h(B/"recovery/CHINESE_V11_BEFORE_12.json"),h(OLD))
        self.assertEqual(self.new["prior_index_sha256"],h(OLD))
        self.assertEqual(self.new["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V11.json")

    def test_04_source_quote_excerpt_original_sha(self):
        self.assertEqual(h(B/"ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json"),
                         self.receipt["source_notes_SHA256"])
        self.assertEqual(h(B/"SOURCE_LIFE_THIRD_FOUR_83_EXACT_OFFSET_WITNESS_V1.json"),
                         self.receipt["source_quote_witness_SHA256"])
        self.assertEqual(h(B/"SOURCE_1963110_LIFE_PALACE_THIRD_FOUR_EXACT_EXCERPT.txt"),
                         self.receipt["source_excerpt_SHA256"])

    def test_05_exact_annotation_id_range_and_last_accepted(self):
        self.assertEqual([x["id"] for x in self.s["records"]],
                         [f"ZWD-R{i:04d}" for i in range(400,483)])
        self.assertEqual(self.new["systems"][1]["current_ids"],"ZWD-R0001–ZWD-R0482")
        self.assertEqual(self.new["systems"][1]["current_batch"],"ChineseAstro-12SRC-Life")

    def test_06_source_absent_female_verse_not_normalized(self):
        batch=self.new["accepted_batches"][-1]
        self.assertTrue(batch["no_dedicated_TianLiang_female_poem_heading_in_original"])
        self.assertTrue(self.receipt["TianLiang_missing_distinct_female_heading_preserved"])
        self.assertFalse(self.s["star_original_sections"][-1][
            "distinct_original_female_poem_heading_present"])

    def test_07_next_QiSha_boundary_and_life_section_not_complete(self):
        self.assertEqual(self.s["next_unstudied_star_native"],"七杀")
        self.assertEqual(self.s["next_unstudied_star_original_codepoint"],28621)
        self.assertIn("ZWD-R0483",self.new["next"])
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.s["complete_Life_palace_source_study"])

    def test_08_original_source_units_and_old_Wikitext_sha_unchanged(self):
        self.assertEqual(self.new["source_manifest"],self.old["source_manifest"])
        self.assertEqual(self.old["original_chinese_source_anchors_checked_against_revision"],537)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],620)
        self.assertEqual(self.new["initial_historical_witness"],self.old["initial_historical_witness"])

    def test_09_parallel_Western_snapshot_not_rebased_to_other_Western_branch(self):
        self.assertEqual(h(WEST),h(B/"recovery/WESTERN_B07bc_BEFORE_12.json"))
        self.assertEqual(r(WEST)["records_count"],13044)
        self.assertEqual(self.new["separate_lilly_source_count_at_this_revision"],13044)
        self.assertEqual(self.receipt["newer_separate_Western_B07bg_Lilly"],13236)

    def test_10_source_zip_independent_cold_SHA_replay(self):
        self.assertTrue(self.zip["zip_CRC_verified"])
        self.assertTrue(self.zip["all_member_SHA_and_bytes_verified"])
        self.assertEqual(self.zip["independently_cold_replayed_tests_green"],15)
        self.assertEqual(self.zip["original_source_member_count"],13)
        self.assertEqual(self.receipt["cold_zip_SHA256"],self.zip["archive_sha256"])

    def test_11_current_state_preserves_old_context_and_new_heading(self):
        before=(B/"recovery/CHINESE_CURRENT_BEFORE_12.md").read_text(encoding="utf-8")
        now=CURR.read_text(encoding="utf-8")
        self.assertTrue(now.endswith(before))
        heading=now.split("## Previous Chinese accepted source checkpoint retained",1)[0]
        self.assertIn("Chinese BaZi210 + ZiWei482 =692",heading)
        self.assertTrue(LATEST.is_file())

    def test_12_no_real_human_validation_and_separate_historical_count(self):
        self.assertEqual(self.new["independently_validated_real_human_claims"],0)
        self.assertEqual(self.new["runtime_promotions"],0)
        self.assertEqual(self.receipt["real_human_predictive_validations"],0)
        self.assertEqual(13236+1066+692,14994)
        self.assertEqual(self.receipt["aggregate_original_source_notes_across_separate_branches"],14994)
        self.assertFalse(self.new["all_14_principal_stars_verified"])

if __name__=="__main__":unittest.main()
