#!/usr/bin/env python3
"""Guarded V26 historical Chinese source-index immutable append verification."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import json,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V25.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V26.json"
SRC=B/"evidence/DiTianSui_20_oldid844370.wikitext"
NOTES=B/"BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS20_2_EXACT_OFFSET_WITNESS_V1.json"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
class IndexV26(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.o=rd(OLD);cls.n=rd(NEW)
  cls.r=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  cls.archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 def test_original_parent_and_new_index_sha(self):
  self.assertEqual(sha(OLD),"f5d2c95d6225bddc4b8a99fc5ddd923d61424a2002d5bb146c8693f72644c0df")
  self.assertEqual(sha(NEW),"f4b69767eb143994766bc9a7c08f7ed1e519bddf234377c9ecc65bcb6080f94f")
  self.assertEqual(self.n["prior_index_sha256"],sha(OLD))
 def test_prior_ZiWei_history_immutable(self):
  self.assertEqual(self.n["systems"][1],self.o["systems"][1])
  self.assertEqual(self.n["accepted_batches"][:-1],self.o["accepted_batches"])
  self.assertEqual(self.n["systems"][0]["source_files"][:-1],self.o["systems"][0]["source_files"])
 def test_total_and_next_source_indices(self):
  self.assertEqual(self.n["sum_source_annotations"],1277)
  self.assertEqual(self.n["original_chinese_source_anchors_checked_against_revision"],1205)
  self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.n["systems"]],
   [(218,"BZI-R0219"),(1059,"ZWD-R1060")])
 def test_new_original_verse_and_commentary_exact_sha(self):
  d=self.n["accepted_batches"][-1]
  self.assertEqual((d["id"],d["start"],d["end"],d["added_bazi_source_annotations"]),
   ("ChineseAstro-26SRC-BaZi-Obstruction","BZI-R0217","BZI-R0218",2))
  self.assertEqual((d["source_original_verse_count"],d["source_complete_commentary_paragraph_count"]),(1,1))
  self.assertEqual(d["original_raw_source_sha256"],sha(SRC))
  self.assertEqual((d["rules_sha256"],d["witness_sha256"]),(sha(NOTES),sha(WIT)))
 def test_preserve_previous_state(self):
  self.assertEqual(sha(B/"recovery/CHINESE_V25_BEFORE_26.json"),sha(OLD))
  self.assertIn((B/"recovery/CHINESE_CURRENT_BEFORE_26.md").read_text(),
   (ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text())
 def test_archive_provenance_and_cold_replay(self):
  a=self.archive
  self.assertEqual(a["independent_cold_source_test_count"],8)
  p=Path(a["archive_path"])
  self.assertEqual(sha(p),a["archive_sha256"])
  with ZipFile(p) as z:
   self.assertIsNone(z.testzip())
   manifest=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(manifest["original_member_SHA256_and_size"]),14)
   for name,v in manifest["original_member_SHA256_and_size"].items():
    b=z.read(name)
    self.assertEqual((sha256(b).hexdigest(),len(b)),(v["sha256"],v["bytes"]))
 def test_no_historical_source_as_real_human_prediction(self):
  self.assertEqual((self.n["independently_validated_real_human_claims"],self.n["runtime_promotions"]),(0,0))
  self.assertFalse(self.n["chinese_bazi_solar_term_engine_verified"])
  self.assertTrue(self.n["accepted_batches"][-1]["ancient_print_authenticity_unverified"])
  self.assertEqual((self.r["real_human_blind_predictive_validations"],self.r["runtime_promotions"]),(0,0))
if __name__=="__main__":unittest.main()
