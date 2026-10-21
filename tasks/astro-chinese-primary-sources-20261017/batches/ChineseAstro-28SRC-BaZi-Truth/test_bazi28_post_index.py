#!/usr/bin/env python3
"""Guarded post-index BaZi V28 historical source regression."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import json,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V28.json"
RAW=B/"evidence/DiTianSui_22_oldid844372.wikitext"
NOTES=B/"BAZI_DITIAN_SUI_22_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS22_4_EXACT_OFFSET_WITNESS_V1.json"
V27="00de501124cfba8167a52e0fc294ed3a25d1bc90bb98a8ae039c8627301f9d39"
V28="67fbee144329c39892a004c75213e08a0ca05189e0d5f548bb49927dbb44d4c0"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
class IndexV28(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=rd(OLD);cls.n=rd(NEW)
  cls.accept=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  cls.archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 def test_parent_and_new_source_exact_hashes(self):
  self.assertEqual(sha(OLD),V27)
  self.assertEqual(sha(NEW),V28)
  self.assertEqual(self.n["prior_index_sha256"],V27)
 def test_immutable_prior_history_and_ziwei(self):
  self.assertEqual(self.n["systems"][1],self.p["systems"][1])
  self.assertEqual(self.n["accepted_batches"][:-1],self.p["accepted_batches"])
  self.assertEqual(self.n["systems"][0]["source_files"][:-1],self.p["systems"][0]["source_files"])
 def test_totals_and_source_frontiers(self):
  self.assertEqual((self.n["sum_source_annotations"],self.n["original_chinese_source_anchors_checked_against_revision"]),(1285,1213))
  self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.n["systems"]],[(226,"BZI-R0227"),(1059,"ZWD-R1060")])
 def test_original_verse_commentary_batch_SHA(self):
  d=self.n["accepted_batches"][-1]
  self.assertEqual((d["id"],d["start"],d["end"],d["added_bazi_source_annotations"]),("ChineseAstro-28SRC-BaZi-Truth","BZI-R0223","BZI-R0226",4))
  self.assertEqual((d["source_complete_verse_count"],d["source_complete_commentary_count"]),(2,2))
  self.assertEqual((d["rules_sha256"],d["witness_sha256"],d["full_source_raw_SHA256"]),(sha(NOTES),sha(WIT),sha(RAW)))
 def test_previous_state_recovery(self):
  self.assertEqual(sha(B/"recovery/CHINESE_V27_BEFORE_28.json"),V27)
  text=(B/"recovery/CHINESE_CURRENT_BEFORE_28.md").read_text(encoding="utf-8")
  self.assertIn(text,(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8"))
 def test_archive_and_independent_cold_replay(self):
  a=self.archive;self.assertEqual(a["cold_extracted_source_tests_green"],9)
  path=Path(a["owner_archive_path"]);self.assertEqual(sha(path),a["archive_SHA256"])
  with ZipFile(path) as z:
   self.assertIsNone(z.testzip())
   man=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(man["file_witnesses"]),14)
   for file,proof in man["file_witnesses"].items():
    x=z.read(file)
    self.assertEqual((sha256(x).hexdigest(),len(x)),(proof["sha256"],proof["bytes"]))
 def test_original_print_and_human_accuracy_unverified(self):
  self.assertFalse(self.n["chinese_bazi_solar_term_engine_verified"])
  self.assertFalse(self.n["accepted_batches"][-1]["original_critical_print_authenticated"])
  self.assertEqual((self.n["independently_validated_real_human_claims"],self.n["runtime_promotions"]),(0,0))
  self.assertEqual((self.accept["human_blind_predictive_validations"],self.accept["runtime_promotions"]),(0,0))
if __name__=="__main__":unittest.main()
