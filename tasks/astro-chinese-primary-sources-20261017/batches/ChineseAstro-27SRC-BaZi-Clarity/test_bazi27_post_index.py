#!/usr/bin/env python3
"""Independent post-index regression for historical Chinese V27 append."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import json,unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V26.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json"
RAW=B/"evidence/DiTianSui_21_oldid844371.wikitext"
NOTES=B/"BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS21_4_EXACT_OFFSET_WITNESS_V1.json"
V26="f4b69767eb143994766bc9a7c08f7ed1e519bddf234377c9ecc65bcb6080f94f"
V27="00de501124cfba8167a52e0fc294ed3a25d1bc90bb98a8ae039c8627301f9d39"
def sha(path):return sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text(encoding="utf-8"))

class V27Index(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=load(OLD);cls.new=load(NEW)
  cls.receipt=load(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  cls.archive=load(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 def test_original_old_and_new_index_exact_hash(self):
  self.assertEqual(sha(OLD),V26)
  self.assertEqual(sha(NEW),V27)
  self.assertEqual(self.new["prior_index_sha256"],V26)
 def test_prior_ziwei_and_history_untouched(self):
  self.assertEqual(self.new["systems"][1],self.old["systems"][1])
  self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
  self.assertEqual(self.new["systems"][0]["source_files"][:-1],self.old["systems"][0]["source_files"])
 def test_total_and_next_source_frontier(self):
  self.assertEqual((self.new["sum_source_annotations"],self.new["original_chinese_source_anchors_checked_against_revision"]),(1281,1209))
  self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in self.new["systems"]],[(222,"BZI-R0223"),(1059,"ZWD-R1060")])
 def test_exact_source_batch_verse_commentary(self):
  d=self.new["accepted_batches"][-1]
  self.assertEqual((d["id"],d["start"],d["end"],d["added_bazi_source_annotations"]),("ChineseAstro-27SRC-BaZi-Clarity","BZI-R0219","BZI-R0222",4))
  self.assertEqual((d["source_original_verses"],d["source_full_commentary_paragraphs"]),(2,2))
  self.assertEqual(d["source_full_original_SHA256"],sha(RAW))
 def test_witness_note_manifest_unchanged(self):
  d=self.new["accepted_batches"][-1]
  self.assertEqual((d["rules_sha256"],d["witness_sha256"]),(sha(NOTES),sha(WIT)))
  self.assertEqual(d["source_manifest_sha256"],sha(B/"PINNED_DITIAN_SUI_21_SOURCE_MANIFEST_V1.json"))
 def test_old_current_and_prior_index_recoverable(self):
  self.assertEqual(sha(B/"recovery/CHINESE_V26_BEFORE_27.json"),V26)
  prev=(B/"recovery/CHINESE_CURRENT_BEFORE_27.md").read_text(encoding="utf-8")
  cur=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
  self.assertIn(prev,cur)
  self.assertIn("BZI-R0223",cur)
 def test_archive_crc_member_hash_cold_replay(self):
  a=self.archive
  self.assertTrue(a["ZIP_CRC_verified"])
  self.assertEqual(a["independent_cold_source_tests_green"],10)
  zpath=Path(a["archive_path"])
  self.assertEqual(sha(zpath),a["archive_SHA256"])
  with ZipFile(zpath) as z:
   self.assertIsNone(z.testzip())
   man=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(man["source_file_checks"]),16)
   for path,proof in man["source_file_checks"].items():
    raw=z.read(path)
    self.assertEqual((sha256(raw).hexdigest(),len(raw)),(proof["sha256"],proof["bytes"]))
 def test_historical_source_not_human_predictions(self):
  self.assertEqual((self.new["independently_validated_real_human_claims"],self.new["runtime_promotions"]),(0,0))
  self.assertFalse(self.new["chinese_bazi_solar_term_engine_verified"])
  self.assertFalse(self.new["accepted_batches"][-1]["ancient_printing_original_critically_authenticated"])
  self.assertEqual((self.receipt["actual_human_blind_predictions_validated"],self.receipt["runtime_promotions"]),(0,0))
 def test_receipts_and_source_provenance(self):
  self.assertEqual((self.receipt["Chinese_before"],self.receipt["Chinese_after"]),(1277,1281))
  self.assertEqual(self.receipt["new_V27_index_SHA256"],V27)
  self.assertEqual(self.receipt["portable_archive_SHA256"],self.archive["archive_SHA256"])
if __name__=="__main__":
 unittest.main()
