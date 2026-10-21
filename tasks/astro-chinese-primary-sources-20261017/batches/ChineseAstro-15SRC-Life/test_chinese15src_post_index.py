#!/usr/bin/env python3
"""Post-index regression checks for guarded Chinese source V15 admission."""
from __future__ import annotations
import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V14.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V15.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE=B/"ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json"
WITNESS=B/"SOURCE_LIFE_SECOND_FOUR_AUXILIARY_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_SECOND_FOUR_AUX_EXACT_EXCERPT.txt"
V15="a5bf0e0cc4bd801b209caa98e1bd58558f2155fd73ba9a055d516472076311ad"
V14="c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding="utf-8"))


class ChineseV15IndexRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=load(OLD)
        cls.after=load(NEW)
        cls.receipt=load(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.archive=load(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261021.json")
        cls.notes=load(SOURCE)

    def test_frozen_old_and_new_index_byte_sha(self):
        self.assertEqual(sha(OLD),V14)
        self.assertEqual(sha(NEW),V15)
        self.assertEqual(self.after["prior_index_sha256"],V14)

    def test_separate_system_totals_exact(self):
        self.assertEqual(self.after["sum_source_annotations"],850)
        self.assertEqual([(s["accepted_source_annotations"],s["next_id"]) for s in self.after["systems"]],
            [(210,"BZI-R0211"),(640,"ZWD-R0641")])
        self.assertEqual(self.after["original_chinese_source_anchors_checked_against_revision"],778)

    def test_prior_batches_and_bazi_untouched(self):
        self.assertEqual(self.after["systems"][0],self.before["systems"][0])
        self.assertEqual(self.after["accepted_batches"][:-1],self.before["accepted_batches"])
        self.assertEqual(self.after["systems"][1]["source_files"][:-1],self.before["systems"][1]["source_files"])
        self.assertEqual(self.after["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V14.json")

    def test_new_batch_maps_all_54_exact_lines_without_previous_navigation(self):
        batch=self.after["accepted_batches"][-1]
        self.assertEqual((batch["start"],batch["end"],batch["added_ziwei_source_annotations"]),
            ("ZWD-R0587","ZWD-R0640",54))
        self.assertEqual((batch["substantive_original_lines"],batch["navigation_only_records"]),(53,1))
        self.assertEqual(batch["original_star_source_line_counts"],[14,6,17,16])
        self.assertEqual(batch["rules_sha256"],sha(SOURCE))
        self.assertEqual(batch["witness_sha256"],sha(WITNESS))
        self.assertEqual(batch["original_excerpt_sha256"],sha(EXCERPT))
        self.assertEqual(batch["next_unstudied_auxiliary_star"],"火星")

    def test_source_text_novelty_semantics_original_omissions_retained(self):
        batch=self.after["accepted_batches"][-1]
        self.assertTrue(batch["QingYang_original_male_heading_twice"])
        self.assertTrue(batch["TuoLuo_female_verse_missing_opening_markup"])
        self.assertTrue(batch["KuiYue_dedicated_sex_time_headings_absent"])
        self.assertEqual(self.notes["next_unstudied_original_codepoint"],33783)

    def test_untested_research_flags_remain_false(self):
        self.assertFalse(self.after["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.after["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.after["chinese_bazi_solar_term_engine_verified"])
        self.assertEqual((self.after["independently_validated_real_human_claims"],
            self.after["runtime_promotions"]),(0,0))
        self.assertTrue(self.after["accepted_batches"][-1]["ancient_Ming_original_imprint_authenticity_unverified"])

    def test_old_western_index_bytewise_preserved(self):
        self.assertEqual(sha(WEST),"c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")
        r=B/"recovery/WESTERN_B07bc_BEFORE_15.json"
        self.assertEqual(r.read_bytes(),WEST.read_bytes())

    def test_old_source_checkpoint_is_recoverable(self):
        self.assertEqual(sha(B/"recovery/CHINESE_V14_BEFORE_15.json"),V14)
        old_current=(B/"recovery/CHINESE_CURRENT_BEFORE_15.md").read_text(encoding="utf-8")
        new_current=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn(old_current,new_current)
        self.assertIn("Zi Wei640 =850",new_current)
        self.assertIn("ZWD-R0641",new_current)

    def test_archive_and_cold_extraction_receipt(self):
        self.assertTrue(self.archive["ZIP_CRC_verified"])
        self.assertTrue(self.archive["each_member_hash_and_size_verified"])
        self.assertEqual(self.archive["independent_cold_source_tests_green"],13)
        fp=Path(self.archive["archive_path_on_owner_computer"])
        self.assertTrue(fp.is_file())
        self.assertEqual(sha(fp),self.archive["archive_sha256"])
        with ZipFile(fp) as z:
            self.assertIsNone(z.testzip())
            manifest=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
            self.assertEqual((manifest["source_oldid"],manifest["human_predictive_validations"]),(1963110,0))
            self.assertEqual(len(manifest["source_file_checks"]),14)
            rawrel="tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
            self.assertEqual(hashlib.sha256(z.read(rawrel)).hexdigest(),
                manifest["source_file_checks"][rawrel]["sha256"])

    def test_receipt_consistency_and_next_source(self):
        self.assertEqual((self.receipt["Chinese_before"],self.receipt["Chinese_after"]),(796,850))
        self.assertEqual((self.receipt["ZiWei_before"],self.receipt["ZiWei_after"]),(586,640))
        self.assertEqual(self.receipt["new_V15_index_SHA256"],sha(NEW))
        self.assertEqual(self.receipt["portable_archive_SHA256"],self.archive["archive_sha256"])
        self.assertEqual((self.receipt["human_blind_validations"],self.receipt["runtime_astrological_promotions"]),(0,0))
        self.assertIn("cp33783",self.after["next"])


if __name__=="__main__":
    unittest.main()
