#!/usr/bin/env python3
"""Guarded post-index Chinese V16 source-only regression checks."""
import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V15.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V16.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE=B/"ZIWEI_LIFE_REMAINING_105_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_LIFE_REMAINING_105_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_REMAINING_EXACT_EXCERPT.txt"
V15="a5bf0e0cc4bd801b209caa98e1bd58558f2155fd73ba9a055d516472076311ad"
V16="e3e0aea4074ddf0837a4a6d3d5f785f6fc70f5e4e7f16c1734cbb76a78781a28"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding="utf-8"))


class ChineseV16PostIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=load(OLD);cls.after=load(NEW)
        cls.receipt=load(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.arch=load(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261021.json")
        cls.notes=load(SOURCE)

    def test_previous_and_new_canonical_exact_immutable_shas(self):
        self.assertEqual(sha(OLD),V15)
        self.assertEqual(sha(NEW),V16)
        self.assertEqual(self.after["prior_index_sha256"],V15)
        self.assertEqual(self.after["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V15.json")

    def test_exact_chinese_system_totals(self):
        self.assertEqual(self.after["sum_source_annotations"],955)
        self.assertEqual(self.after["original_chinese_source_anchors_checked_against_revision"],883)
        self.assertEqual([(s["accepted_source_annotations"],s["next_id"]) for s in self.after["systems"]],
            [(210,"BZI-R0211"),(745,"ZWD-R0746")])

    def test_unchanged_previous_chinese_history_and_bazi(self):
        self.assertEqual(self.after["systems"][0],self.before["systems"][0])
        self.assertEqual(self.after["accepted_batches"][:-1],self.before["accepted_batches"])
        self.assertEqual(self.after["systems"][1]["source_files"][:-1],self.before["systems"][1]["source_files"])
        self.assertEqual(self.after["accepted_batches"][-1]["id"],"ChineseAstro-16SRC-Life")

    def test_guarded_105_source_witnesses(self):
        b=self.after["accepted_batches"][-1]
        self.assertEqual((b["start"],b["end"],b["added_ziwei_source_annotations"]),
            ("ZWD-R0641","ZWD-R0745",105))
        self.assertEqual((b["substantive_original_lines"],b["following_section_navigation_only_records"]),(104,1))
        self.assertEqual(b["original_source_group_line_counts"],[7,7,9,6,8,3,2,4,5,8,11,11,16,5,2])
        self.assertEqual(b["rules_sha256"],sha(SOURCE))
        self.assertEqual(b["witness_sha256"],sha(WIT))
        self.assertEqual(b["original_excerpt_sha256"],sha(EXCERPT))

    def test_source_fidelity_preserved_and_next_heading(self):
        b=self.after["accepted_batches"][-1]
        self.assertTrue(b["original_HuoLing_JieKong_combined_groups_preserved"])
        self.assertTrue(b["mixed_original_HuaLu_traditional_simplified_variants_preserved"])
        self.assertTrue(b["online_original_Life_palace_through_Brothers_heading_documented"])
        self.assertFalse(b["original_critical_book_completed"])
        self.assertEqual(self.notes["next_original_section_codepoint"],37269)
        self.assertIn("Brothers/Siblings",self.after["next"])

    def test_unvalidated_and_remaining_houses_open(self):
        self.assertEqual((self.after["independently_validated_real_human_claims"],
            self.after["runtime_promotions"]),(0,0))
        self.assertFalse(self.after["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.after["ziwei_complete_natal_calendar_engine_verified"])
        self.assertTrue(self.after["accepted_batches"][-1]["other_11_houses_still_unstudied_as_complete_source_sections"])
        self.assertTrue(self.after["accepted_batches"][-1]["ancient_Ming_original_imprint_authenticity_unverified"])

    def test_old_western_source_immutable_and_recoverable(self):
        self.assertEqual(sha(WEST),"c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")
        self.assertEqual((B/"recovery/WESTERN_B07bc_BEFORE_16.json").read_bytes(),WEST.read_bytes())

    def test_original_previous_chinese_state_recovered(self):
        self.assertEqual(sha(B/"recovery/CHINESE_V15_BEFORE_16.json"),V15)
        prior=(B/"recovery/CHINESE_CURRENT_BEFORE_16.md").read_text(encoding="utf-8")
        current=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn(prior,current)
        self.assertIn("ZiWei745 =955",current)
        self.assertIn("ZWD-R0746",current)

    def test_cold_archive_crc_sizes_sha_and_tests(self):
        self.assertTrue(self.arch["ZIP_CRC_verified"])
        self.assertTrue(self.arch["each_member_hash_and_size_verified"])
        self.assertEqual((self.arch["independent_cold_source_tests_executed"],
            self.arch["independent_cold_source_tests_green"]),(12,12))
        p=Path(self.arch["archive_path_on_owner_computer"])
        self.assertTrue(p.is_file())
        self.assertEqual(sha(p),self.arch["archive_sha256"])
        with ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            manifest=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
            self.assertEqual(len(manifest["source_file_checks"]),14)
            self.assertEqual(manifest["source_oldid"],1963110)
            raw="tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
            self.assertEqual(hashlib.sha256(z.read(raw)).hexdigest(),
                manifest["source_file_checks"][raw]["sha256"])

    def test_guard_receipt_and_open_science_claims(self):
        self.assertEqual((self.receipt["Chinese_before"],self.receipt["Chinese_after"]),(850,955))
        self.assertEqual((self.receipt["ZiWei_before"],self.receipt["ZiWei_after"]),(640,745))
        self.assertEqual(self.receipt["new_V16_index_SHA256"],sha(NEW))
        self.assertEqual(self.receipt["portable_archive_SHA256"],self.arch["archive_sha256"])
        self.assertEqual((self.receipt["human_blind_validations"],self.receipt["runtime_astrological_promotions"]),(0,0))


if __name__=="__main__":
    unittest.main()
