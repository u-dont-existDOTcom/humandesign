#!/usr/bin/env python3
"""Independent post-index source-only regression for V30."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import json,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V29.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V30.json"
RAW=B/"evidence/DiTianSui_24_oldid844375.wikitext"
NOTES=B/"BAZI_DITIAN_SUI_24_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS24_2_EXACT_OFFSET_WITNESS_V1.json"
V29="dd692da5d0e1e9918cc2d99eb8935655970275a9151f934976f6647d3cfa205e"
V30="6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
class IndexV30(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=rd(OLD);cls.new=rd(NEW);cls.receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  cls.archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 def test_accepted_old_and_new_index_exact_SHA(self):
  self.assertEqual((sha(OLD),sha(NEW)),(V29,V30))
  self.assertEqual(self.new["prior_index_sha256"],V29)
 def test_preserved_old_bazi_batches_and_ziwei(self):
  self.assertEqual(self.new["systems"][1],self.old["systems"][1])
  self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
  self.assertEqual(self.new["systems"][0]["source_files"][:-1],self.old["systems"][0]["source_files"])
 def test_new_total_and_next_source_frontiers(self):
  self.assertEqual((self.new["sum_source_annotations"],self.new["original_chinese_source_anchors_checked_against_revision"]),(1289,1217))
  self.assertEqual([(r["accepted_source_annotations"],r["next_id"]) for r in self.new["systems"]],[(230,"BZI-R0231"),(1059,"ZWD-R1060")])
 def test_new_original_verse_and_commentary_sha(self):
  d=self.new["accepted_batches"][-1]
  self.assertEqual((d["id"],d["start"],d["end"],d["added_bazi_source_annotations"]),("ChineseAstro-30SRC-BaZi-StrongWeak","BZI-R0229","BZI-R0230",2))
  self.assertEqual((d["source_full_original_verse_count"],d["source_complete_commentary_paragraph_count"]),(1,1))
  self.assertEqual((d["rules_sha256"],d["witness_sha256"],d["full_raw_source_SHA256"]),(sha(NOTES),sha(WIT),sha(RAW)))
  self.assertTrue(d["source_majority_minority_elemental_claims_unverified"])
 def test_previous_source_state_recoverable(self):
  self.assertEqual(sha(B/"recovery/CHINESE_V29_BEFORE_30.json"),V29)
  prior=(B/"recovery/CHINESE_CURRENT_BEFORE_30.md").read_text(encoding="utf-8")
  self.assertIn(prior,(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8"))
 def test_cold_source_ZIP_CRC_and_each_hash(self):
  a=self.archive;self.assertEqual(a["independent_cold_source_tests_green"],9)
  p=Path(a["owner_archive_path"])
  self.assertEqual(sha(p),a["archive_SHA256"])
  with ZipFile(p) as z:
   self.assertIsNone(z.testzip())
   manifest=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(manifest["file_witnesses"]),14)
   for name,proof in manifest["file_witnesses"].items():
    blob=z.read(name)
    self.assertEqual((sha256(blob).hexdigest(),len(blob)),(proof["sha256"],proof["bytes"]))
 def test_no_original_printing_or_real_human_validations(self):
  self.assertFalse(self.new["chinese_bazi_solar_term_engine_verified"])
  self.assertFalse(self.new["accepted_batches"][-1]["original_ancient_print_critically_authenticated"])
  self.assertEqual((self.new["independently_validated_real_human_claims"],self.new["runtime_promotions"]),(0,0))
  self.assertEqual((self.receipt["human_blind_predictive_validations"],self.receipt["runtime_promotions"]),(0,0))
if __name__=="__main__":unittest.main()
