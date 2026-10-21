#!/usr/bin/env python3
"""Post-index regression checks for preserved original Zi Wei online Volume II evidence."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import unittest
from zipfile import ZipFile

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = T/"CHINESE_SOURCE_AUDIT_INDEX_V23.json"
NEW = T/"CHINESE_SOURCE_AUDIT_INDEX_V24.json"
WEST = ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES = B/"ZIWEI_FINAL_FOUR_123_SOURCE_NOTES_V1.json"
WIT = B/"SOURCE_FINAL_FOUR_123_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B/"SOURCE_1963110_FINAL_FOUR_EXACT_EXCERPT.txt"
OLD_SHA = "0bc5836d92c332a458a7d4a74dbb25488705344aa38df256dc721c6c5a673a0e"
NEW_SHA = "ff40d64df1f4d2a5525591c5e4b5fa7e823c9c81e420093413b01cc292a919d1"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"

def sha(p:Path)->str:
    return sha256(p.read_bytes()).hexdigest()
def load(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))

class VolumeIIV24Index(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=load(OLD)
        cls.new=load(NEW)
        cls.receipt=load(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.archive=load(B/"SOURCE_RELEASE_RECEIPT_20261021.json")

    def test_prior_and_current_exact_index_SHA(self):
        self.assertEqual(sha(OLD),OLD_SHA)
        self.assertEqual(sha(NEW),NEW_SHA)
        self.assertEqual(self.new["prior_index_sha256"],OLD_SHA)

    def test_previous_BaZi_and_Chinese_history_byte_semantics(self):
        self.assertEqual(self.new["systems"][0],self.old["systems"][0])
        self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
        self.assertEqual(self.new["systems"][1]["source_files"][:-1],
                         self.old["systems"][1]["source_files"])

    def test_new_source_totals_and_next_without_human_claim(self):
        self.assertEqual(self.new["sum_source_annotations"],1269)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],1197)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.new["systems"]],
                         [(210,"BZI-R0211"),(1059,"ZWD-R1060")])
        self.assertEqual((self.new["independently_validated_real_human_claims"],self.new["runtime_promotions"]),(0,0))

    def test_four_pinned_original_source_sections_with_site_markup_excluded(self):
        batch=self.new["accepted_batches"][-1]
        self.assertEqual((batch["id"],batch["start"],batch["end"],batch["added_ziwei_source_annotations"]),
                         ("ChineseAstro-24SRC-FinalPalaces","ZWD-R0937","ZWD-R1059",123))
        self.assertEqual(batch["original_historical_line_counts"],[38,24,28,33])
        self.assertEqual(batch["terminal_site_wrapper_metadata_excluded"],2)
        self.assertEqual(batch["original_source_codepoint_range"],[44429,48890])
        self.assertEqual(batch["original_source_palaces"],["Career","Estate","Fortune","Parents"])

    def test_original_quotes_and_offset_witness_sha_frozen(self):
        batch=self.new["accepted_batches"][-1]
        self.assertEqual(batch["rules_sha256"],sha(NOTES))
        self.assertEqual(batch["witness_sha256"],sha(WIT))
        self.assertEqual(batch["original_excerpt_sha256"],sha(EXCERPT))
        self.assertEqual(len(load(NOTES)["records"]),123)

    def test_online_volume_completion_distinct_from_old_printing_authentication(self):
        self.assertTrue(self.new["online_ZiWei_Volume_II_twelve_house_source_lines_documented"])
        self.assertEqual(self.new["online_Volume_II_end_codepoint"],48890)
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.new["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.new["accepted_batches"][-1]["original_Ming_printing_critically_collated"])

    def test_old_inherited_Western_index_unmodified(self):
        self.assertEqual(sha(WEST),WEST_SHA)
        self.assertEqual(WEST.read_bytes(),(B/"recovery/WESTERN_B07bc_BEFORE_24.json").read_bytes())
    def test_old_Chinese_current_state_exactly_recoverable(self):
        self.assertEqual(sha(B/"recovery/CHINESE_V23_BEFORE_24.json"),OLD_SHA)
        old=(B/"recovery/CHINESE_CURRENT_BEFORE_24.md").read_text(encoding="utf-8")
        new=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn(old,new)
        self.assertIn("ZWD-R1060",new)

    def test_original_source_archive_SHA_CRC_and_member_hashes(self):
        self.assertEqual(self.archive["independent_cold_source_tests_green"],14)
        self.assertTrue(self.archive["all_members_sha256_and_bytes_verified"])
        path=Path(self.archive["archive_path_on_owner_computer"])
        self.assertTrue(path.is_file())
        self.assertEqual(sha(path),self.archive["archive_SHA256"])
        with ZipFile(path) as z:
            self.assertIsNone(z.testzip())
            man=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
            self.assertEqual(len(man["file_checks"]),15)
            for rel,proof in man["file_checks"].items():
                data=z.read(rel)
                self.assertEqual((sha256(data).hexdigest(),len(data)),
                                 (proof["sha256"],proof["bytes"]))

    def test_guards_and_receipts_match_last_original_source_end(self):
        receipt=self.receipt
        self.assertEqual((receipt["Chinese_before"],receipt["Chinese_after"]),(1146,1269))
        self.assertEqual((receipt["ZiWei_before"],receipt["ZiWei_after"]),(936,1059))
        self.assertEqual(receipt["new_V24_index_SHA256"],sha(NEW))
        self.assertEqual(receipt["source_archive_SHA256"],self.archive["archive_SHA256"])
        self.assertTrue(receipt["online_volume_II_twelve_house_literal_source_complete"])
        self.assertEqual((receipt["human_blind_predictive_validations"],
                          receipt["runtime_astrological_promotions"]),(0,0))

if __name__ == "__main__":
    unittest.main()
