#!/usr/bin/env python3
"""Guarded Chinese V29 source-only index regression."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import json,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V28.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V29.json"
RAW=B/"evidence/DiTianSui_23_oldid844373.wikitext"
NOTES=B/"BAZI_DITIAN_SUI_23_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS23_2_EXACT_OFFSET_WITNESS_V1.json"
V28="67fbee144329c39892a004c75213e08a0ca05189e0d5f548bb49927dbb44d4c0"
V29="dd692da5d0e1e9918cc2d99eb8935655970275a9151f934976f6647d3cfa205e"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class IndexV29(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=rd(OLD);cls.new=rd(NEW);cls.receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json");cls.arc=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 def test_prior_and_new_index_immutable_sha(self):
  self.assertEqual((sha(OLD),sha(NEW)),(V28,V29))
  self.assertEqual(self.new["prior_index_sha256"],V28)
 def test_old_bazi_history_and_ziwei_unchanged(self):
  self.assertEqual(self.new["systems"][1],self.old["systems"][1])
  self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
  self.assertEqual(self.new["systems"][0]["source_files"][:-1],self.old["systems"][0]["source_files"])
 def test_total_and_next_chapter(self):
  self.assertEqual((self.new["sum_source_annotations"],self.new["original_chinese_source_anchors_checked_against_revision"]),(1287,1215))
  self.assertEqual([(r["accepted_source_annotations"],r["next_id"]) for r in self.new["systems"]],[(228,"BZI-R0229"),(1059,"ZWD-R1060")])
 def test_accepted_new_historical_source_metadata(self):
  d=self.new["accepted_batches"][-1]
  self.assertEqual((d["id"],d["start"],d["end"],d["added_bazi_source_annotations"]),("ChineseAstro-29SRC-BaZi-Hidden","BZI-R0227","BZI-R0228",2))
  self.assertEqual((d["source_full_original_verse_count"],d["source_complete_commentary_paragraph_count"]),(1,1))
  self.assertEqual((d["rules_sha256"],d["witness_sha256"],d["full_raw_source_SHA256"]),(sha(NOTES),sha(WIT),sha(RAW)))
 def test_previous_snapshot_recoverable(self):
  self.assertEqual(sha(B/"recovery/CHINESE_V28_BEFORE_29.json"),V28)
  old=(B/"recovery/CHINESE_CURRENT_BEFORE_29.md").read_text(encoding="utf-8")
  self.assertIn(old,(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8"))
 def test_cold_source_archive_all_file_witnesses(self):
  self.assertEqual(self.arc["independent_cold_source_tests_green"],9)
  path=Path(self.arc["owner_archive_path"])
  self.assertEqual(sha(path),self.arc["archive_SHA256"])
  with ZipFile(path) as z:
   self.assertIsNone(z.testzip())
   m=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(m["file_witnesses"]),14)
   for n,proof in m["file_witnesses"].items():
    content=z.read(n)
    self.assertEqual((sha256(content).hexdigest(),len(content)),(proof["sha256"],proof["bytes"]))
 def test_no_human_evaluation_or_ancient_original_attestation(self):
  self.assertFalse(self.new["chinese_bazi_solar_term_engine_verified"])
  self.assertTrue(self.new["accepted_batches"][-1]["source_fortune_risk_reliability_claims_unverified"])
  self.assertEqual((self.new["independently_validated_real_human_claims"],self.new["runtime_promotions"]),(0,0))
  self.assertEqual((self.receipt["human_blind_predictive_validations"],self.receipt["runtime_promotions"]),(0,0))
if __name__=="__main__":unittest.main()
