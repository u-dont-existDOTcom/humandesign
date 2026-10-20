"""Guarded Chinese source V14 post-original-auxiliary profile index checks."""
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V14.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURR=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_14SRC_LIFE.md"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def h(p):return sha256(p.read_bytes()).hexdigest()

class V14SourceAfterGuardedAppend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=rd(OLD);cls.new=rd(NEW)
        cls.receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.src=rd(B/"ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json")
        cls.zip=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_exact_source_totals_before_after(self):
        self.assertEqual(self.old["sum_source_annotations"],738)
        self.assertEqual(self.new["sum_source_annotations"],796)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.new["systems"]],
                         [(210,"BZI-R0211"),(586,"ZWD-R0587")])

    def test_02_all_old_source_batches_and_BaZi_unchanged(self):
        self.assertEqual(self.old["accepted_batches"],self.new["accepted_batches"][:-1])
        self.assertEqual(self.old["systems"][0],self.new["systems"][0])
        self.assertEqual(self.new["accepted_batches"][-1]["id"],"ChineseAstro-14SRC-Life")
        self.assertEqual(self.new["accepted_batches"][-1]["added_ziwei_source_annotations"],58)

    def test_03_immutable_prior_index_exact_SHA_and_snapshot(self):
        self.assertEqual(h(OLD),self.receipt["old_V13_index_SHA256"])
        self.assertEqual(h(NEW),self.receipt["new_V14_index_SHA256"])
        self.assertEqual(h(B/"recovery/CHINESE_V13_BEFORE_14.json"),h(OLD))
        self.assertEqual(self.new["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V13.json")
        self.assertEqual(self.new["prior_index_sha256"],h(OLD))

    def test_04_new_original_note_quote_offset_SHA(self):
        self.assertEqual(h(B/"ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"),
                         self.receipt["original_source_notes_SHA256"])
        self.assertEqual(h(B/"SOURCE_LIFE_FIRST_FOUR_AUXILIARY_58_EXACT_OFFSET_WITNESS_V1.json"),
                         self.receipt["original_source_witness_SHA256"])
        self.assertEqual(h(B/"SOURCE_1963110_LIFE_FIRST_FOUR_AUX_EXACT_EXCERPT.txt"),
                         self.receipt["source_excerpt_SHA256"])

    def test_05_source_annotation_exact_58_IDs_no_overlap(self):
        self.assertEqual([x["id"] for x in self.src["records"]],
                         [f"ZWD-R{i:04d}" for i in range(529,587)])
        self.assertEqual(self.new["systems"][1]["current_ids"],"ZWD-R0001–ZWD-R0586")
        self.assertEqual(self.new["systems"][1]["current_batch"],"ChineseAstro-14SRC-Life")
        self.assertEqual(self.receipt["next_ZWD"],"ZWD-R0587")

    def test_06_missing_YouBi_female_verse_and_grade_rows_preserved(self):
        batch=self.new["accepted_batches"][-1]
        self.assertTrue(batch["ZuoFu_YouBi_no_separate_palace_grade_rows"])
        self.assertTrue(batch["YouBi_no_female_poem_heading"])
        self.assertTrue(self.receipt["YouBi_female_verse_source_omission_preserved"])
        self.assertFalse(self.src["star_sections"][-1]["has_independent_original_female_poem_heading"])

    def test_07_auxiliary_source_still_partial_and_next_LuCun(self):
        self.assertEqual(self.src["next_unstudied_star"],"禄存")
        self.assertEqual(self.src["next_unstudied_original_codepoint"],31937)
        self.assertIn("ZWD-R0587",self.new["next"])
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.src["original_full_Life_palace_text_completed"])

    def test_08_original_quote_count_and_source_history_exact(self):
        self.assertEqual(self.old["original_chinese_source_anchors_checked_against_revision"],666)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],724)
        self.assertEqual(self.new["source_manifest"],self.old["source_manifest"])
        self.assertEqual(self.new["initial_historical_witness"],self.old["initial_historical_witness"])

    def test_09_inherited_Western_old_B07bc_snapshot_bytewise_unchanged(self):
        self.assertEqual(h(WEST),h(B/"recovery/WESTERN_B07bc_BEFORE_14.json"))
        self.assertEqual(rd(WEST)["records_count"],13044)
        self.assertEqual(self.new["separate_lilly_source_count_at_this_revision"],13044)
        self.assertEqual(self.receipt["newer_separate_Western_B07bg_Lilly"],13236)

    def test_10_cold_original_ZIP_and_byte_SHA_evidence(self):
        self.assertTrue(self.zip["ZIP_CRC_verified"])
        self.assertTrue(self.zip["each_member_hash_and_size_verified"])
        self.assertEqual(self.zip["independent_cold_source_tests_green"],13)
        self.assertEqual(self.zip["ZIP_member_count"],13)
        self.assertEqual(self.receipt["portable_source_archive_SHA256"],
                         self.zip["archive_sha256"])

    def test_11_current_state_history_preserved_exact_suffix(self):
        before=(B/"recovery/CHINESE_CURRENT_BEFORE_14.md").read_text(encoding="utf-8")
        now=CURR.read_text(encoding="utf-8")
        self.assertTrue(now.endswith(before))
        head=now.split("## Prior accepted Chinese original-source checkpoint retained",1)[0]
        self.assertIn("Chinese BaZi210 +ZiWei586 =796",head)
        self.assertTrue(LATEST.is_file())

    def test_12_no_actual_human_predictive_validations_no_model_promotions(self):
        self.assertEqual(self.new["independently_validated_real_human_claims"],0)
        self.assertEqual(self.new["runtime_promotions"],0)
        self.assertEqual(self.receipt["human_blind_validations"],0)
        self.assertEqual(13236+1066+796,15098)
        self.assertEqual(self.receipt["aggregate_historical_source_counts_across_separate_branches"],15098)
        self.assertFalse(self.new["all_14_principal_stars_verified"])

if __name__=="__main__":unittest.main()
