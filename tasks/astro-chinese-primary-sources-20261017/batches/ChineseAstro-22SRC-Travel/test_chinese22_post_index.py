#!/usr/bin/env python3
"""Independent guarded source-only V22 cumulative index regression."""
from pathlib import Path
import hashlib,json,subprocess,unittest
from zipfile import ZipFile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V21.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V22.json"
SOURCE=B/"ZIWEI_TRAVEL_26_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_TRAVEL_26_EXACT_OFFSET_WITNESS_V1.json"
EX=B/"SOURCE_1963110_TRAVEL_EXACT_EXCERPT.txt"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class IndexV22(unittest.TestCase):
 def test_previous_index_exact(self):
  self.assertEqual(sha(OLD),"0b22a13f164891fa60be0b8630aa6ed131cf27f425ad492557a9d814d7375c03")
 def test_existing_bazi_and_batches_preserved(self):
  o,n=rd(OLD),rd(NEW)
  self.assertEqual(n["systems"][0],o["systems"][0])
  self.assertEqual(n["accepted_batches"][:-1],o["accepted_batches"])
  self.assertEqual(n["systems"][1]["source_files"][:-1],o["systems"][1]["source_files"])
 def test_new_counts_and_frontier(self):
  n=rd(NEW)
  self.assertEqual(n["sum_source_annotations"],1120)
  self.assertEqual(n["original_chinese_source_anchors_checked_against_revision"],1048)
  self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in n["systems"]],[(210,"BZI-R0211"),(910,"ZWD-R0911")])
 def test_new_documentary_record_sha(self):
  n=rd(NEW)["accepted_batches"][-1]
  self.assertEqual((n["id"],n["start"],n["end"],n["added_ziwei_source_annotations"]),("ChineseAstro-22SRC-Travel","ZWD-R0885","ZWD-R0910",26))
  self.assertEqual((n["rules_sha256"],n["witness_sha256"],n["original_excerpt_sha256"]),(sha(SOURCE),sha(WIT),sha(EX)))
  self.assertEqual(n["original_codepoints"],[42541,43499])
 def test_index_blob_and_offline_archive(self):
  receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  expected=receipt["new_index_blob_sha"]
  got=subprocess.check_output(["git","hash-object",str(NEW)],cwd=ROOT,text=True).strip()
  self.assertEqual(got,expected)
  a=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
  p=Path(a["local_archive_path"])
  self.assertEqual(sha(p),a["archive_SHA256"])
  self.assertEqual(a["cold_extracted_source_tests_green"],9)
  with ZipFile(p) as z:self.assertIsNone(z.testzip())
 def test_no_human_accuracy_or_ming_authority_claim(self):
  n=rd(NEW)
  self.assertEqual((n["independently_validated_real_human_claims"],n["runtime_promotions"]),(0,0))
  self.assertFalse(n["ziwei_complete_natal_calendar_engine_verified"])
  self.assertFalse(n["full_ziwei_original_text_collation_finished"])
  self.assertFalse(n["accepted_batches"][-1]["original_woodblock_authenticated"])
if __name__=="__main__":unittest.main()
