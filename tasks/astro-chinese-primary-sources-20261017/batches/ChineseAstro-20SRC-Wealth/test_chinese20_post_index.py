#!/usr/bin/env python3
"""Verify the accepted V20 Chinese historical-source index is a lossless append."""
import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V19.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V20.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class IndexV20(unittest.TestCase):
 def test_original_index_and_new_SHA(self):
  self.assertEqual(sha(OLD),"52c5d51a281d5e641d2e029af81929e7a327d04eb5e1b510534d45b78c27fcb2")
  self.assertEqual(sha(NEW),"a6b051ed03f19f663d5a363af9a5c4efbf2ca2aea4997e94920023fdcf32f9b5")
 def test_systems_and_counts(self):
  n=rd(NEW)
  self.assertEqual(n["sum_source_annotations"],1069)
  self.assertEqual(n["original_chinese_source_anchors_checked_against_revision"],997)
  self.assertEqual([(i["accepted_source_annotations"],i["next_id"]) for i in n["systems"]],[(210,"BZI-R0211"),(859,"ZWD-R0860")])
 def test_prior_batches_unchanged(self):
  o,n=rd(OLD),rd(NEW)
  self.assertEqual(n["systems"][0],o["systems"][0])
  self.assertEqual(n["accepted_batches"][:-1],o["accepted_batches"])
  self.assertEqual(n["systems"][1]["source_files"][:-1],o["systems"][1]["source_files"])
 def test_new_source_witness(self):
  b=rd(NEW)["accepted_batches"][-1]
  self.assertEqual((b["start"],b["end"],b["added_ziwei_source_annotations"]),("ZWD-R0829","ZWD-R0859",31))
  self.assertEqual((b["source_wrapped_condition_continuations"],b["source_star_or_combination_lines"]),(6,23))
  self.assertEqual(b["rules_sha256"],sha(B/"ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json"))
  self.assertEqual(b["witness_sha256"],sha(B/"SOURCE_WEALTH_31_EXACT_OFFSET_WITNESS_V1.json"))
  self.assertEqual(b["original_excerpt_sha256"],sha(B/"SOURCE_1963110_WEALTH_EXACT_EXCERPT.txt"))
 def test_western_recovery(self):
  self.assertEqual(sha(WEST),"c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")
  self.assertEqual(WEST.read_bytes(),(B/"recovery/WESTERN_B07bc_BEFORE_20.json").read_bytes())
 def test_archive_and_receipts(self):
  a=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
  receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  self.assertEqual((receipt["Chinese_before"],receipt["Chinese_after"]),(1038,1069))
  self.assertEqual(a["independent_cold_extracted_source_tests_green"],11)
  p=Path(a["archive_path_on_owner_computer"])
  self.assertEqual(sha(p),a["archive_sha256"])
  with ZipFile(p) as z:
   self.assertIsNone(z.testzip())
   m=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(m["members"]),14)
   for f,x in m["members"].items():
    data=z.read(f)
    self.assertEqual((hashlib.sha256(data).hexdigest(),len(data)),(x["sha256"],x["bytes"]))
 def test_historical_validation_not_human_accuracy(self):
  n=rd(NEW)
  self.assertEqual((n["independently_validated_real_human_claims"],n["runtime_promotions"]),(0,0))
  self.assertFalse(n["ziwei_complete_natal_calendar_engine_verified"])
  self.assertFalse(n["full_ziwei_original_text_collation_finished"])
 def test_old_checkpoint_in_current(self):
  self.assertEqual(sha(B/"recovery/CHINESE_V19_BEFORE_20.json"),sha(OLD))
  self.assertIn((B/"recovery/CHINESE_CURRENT_BEFORE_20.md").read_text(),(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text())
if __name__=="__main__":
 unittest.main()
