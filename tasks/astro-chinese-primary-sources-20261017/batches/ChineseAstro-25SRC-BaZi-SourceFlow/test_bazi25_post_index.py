#!/usr/bin/env python3
"""Independent V25 guarded source-index regression, not human outcome evaluation."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import unittest
from zipfile import ZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V24.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V25.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
RAW=B/"evidence/DiTianSui_19_oldid844368.wikitext"
NOTES=B/"BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS19_6_EXACT_OFFSET_WITNESS_V1.json"
OLD_SHA="ff40d64df1f4d2a5525591c5e4b5fa7e823c9c81e420093413b01cc292a919d1"
NEW_SHA="f5d2c95d6225bddc4b8a99fc5ddd923d61424a2002d5bb146c8693f72644c0df"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
def sha(p:Path)->str:return sha256(p.read_bytes()).hexdigest()
def rd(p:Path)->dict:return json.loads(p.read_text(encoding="utf-8"))

class AcceptedChineseV25(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=rd(OLD)
        cls.new=rd(NEW)
        cls.receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")

    def test_prior_accepted_and_new_index_exact_hashes(self):
        self.assertEqual(sha(OLD),OLD_SHA)
        self.assertEqual(sha(NEW),NEW_SHA)
        self.assertEqual(self.new["prior_index_sha256"],OLD_SHA)

    def test_older_Chinese_ZiWei_source_and_all_batches_unchanged(self):
        self.assertEqual(self.new["systems"][1],self.old["systems"][1])
        self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
        self.assertEqual(self.new["systems"][0]["source_files"][:-1],
                         self.old["systems"][0]["source_files"])

    def test_total_next_and_unchanged_ziwei(self):
        self.assertEqual(self.new["sum_source_annotations"],1275)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],1203)
        self.assertEqual([(s["accepted_source_annotations"],s["next_id"]) for s in self.new["systems"]],
                         [(216,"BZI-R0217"),(1059,"ZWD-R1060")])
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])

    def test_source_chapter_19_with_exact_six_historical_components(self):
        batch=self.new["accepted_batches"][-1]
        self.assertEqual((batch["id"],batch["start"],batch["end"],batch["added_bazi_source_annotations"]),
                         ("ChineseAstro-25SRC-BaZi-SourceFlow","BZI-R0211","BZI-R0216",6))
        self.assertEqual((batch["one_source_verse"],batch["three_full_source_commentary_paragraphs"],
                          batch["two_original_hour_day_month_year_example_tables"]),(1,3,2))
        self.assertEqual(batch["source_oldid"],844368)
        self.assertEqual(batch["original_source_raw_SHA256"],sha(RAW))

    def test_note_and_witness_SHA_exact(self):
        batch=self.new["accepted_batches"][-1]
        self.assertEqual(batch["rules_sha256"],sha(NOTES))
        self.assertEqual(batch["witness_sha256"],sha(WIT))
        self.assertEqual(batch["original_source_manifest_sha256"],sha(B/"PINNED_DITIAN_SUI_19_SOURCE_MANIFEST_V1.json"))
        self.assertEqual(len(rd(NOTES)["records"]),6)

    def test_old_inherited_Western_and_prior_recovery_exact(self):
        self.assertEqual(sha(WEST),WEST_SHA)
        self.assertEqual((B/"recovery/WESTERN_B07bc_BEFORE_25.json").read_bytes(),WEST.read_bytes())
        self.assertEqual(sha(B/"recovery/CHINESE_V24_BEFORE_25.json"),OLD_SHA)

    def test_previous_current_source_state_recoverable(self):
        prev=(B/"recovery/CHINESE_CURRENT_BEFORE_25.md").read_text(encoding="utf-8")
        current=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn(prev,current)
        self.assertIn("BZI-R0217",current)

    def test_cold_archive_sha_crc_all_members_and_tests(self):
        self.assertEqual(self.archive["cold_extracted_source_test_green"],11)
        archive=Path(self.archive["local_archive_path"])
        self.assertTrue(archive.is_file())
        self.assertEqual(sha(archive),self.archive["archive_SHA256"])
        with ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            man=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
            self.assertEqual(len(man["original_file_SHA256_and_byte_sizes"]),15)
            for name,proof in man["original_file_SHA256_and_byte_sizes"].items():
                blob=z.read(name)
                self.assertEqual((sha256(blob).hexdigest(),len(blob)),
                                 (proof["sha256"],proof["UTF8_or_raw_bytes"]))

    def test_no_real_human_accuracy_or_original_book_authorship(self):
        self.assertEqual((self.new["independently_validated_real_human_claims"],
                          self.new["runtime_promotions"]),(0,0))
        self.assertFalse(self.new["chinese_bazi_solar_term_engine_verified"])
        self.assertFalse(self.new["accepted_batches"][-1]["historical_case_outcomes_independently_verified"])
        self.assertFalse(self.new["accepted_batches"][-1]["ancient_original_print_authorship_critical_text_verified"])
        self.assertEqual((self.receipt["human_blind_predictive_validations"],
                          self.receipt["runtime_astrology_promotions"]),(0,0))

if __name__=="__main__":
    unittest.main()
