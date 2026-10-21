#!/usr/bin/env python3
"""Guarded post-index source regressions; text is not real human prediction."""
import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V20.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V21.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class V21(unittest.TestCase):
 def test_old_and_new_immutable_SHA(self):
  self.assertEqual(sha(OLD),"a6b051ed03f19f663d5a363af9a5c4efbf2ca2aea4997e94920023fdcf32f9b5")
  self.assertEqual(sha(NEW),"0b22a13f164891fa60be0b8630aa6ed131cf27f425ad492557a9d814d7375c03")
 def test_old_batches_bazi_unchanged(self):
  o,n=rd(OLD),rd(NEW)
  self.assertEqual(n["systems"][0],o["systems"][0])
  self.assertEqual(n["accepted_batches"][:-1],o["accepted_batches"])
  self.assertEqual(n["systems"][1]["source_files"][:-1],o["systems"][1]["source_files"])
 def test_sum_new_next_and_human_zero(self):
  n=rd(NEW)
  self.assertEqual(n["sum_source_annotations"],1094)
  self.assertEqual(n["original_chinese_source_anchors_checked_against_revision"],1022)
  self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in n["systems"]],[(210,"BZI-R0211"),(884,"ZWD-R0885")])
  self.assertEqual((n["independently_validated_real_human_claims"],n["runtime_promotions"]),(0,0))
 def test_source_witnesses_append(self):
  b=rd(NEW)["accepted_batches"][-1]
  self.assertEqual((b["start"],b["end"],b["added_ziwei_source_annotations"]),("ZWD-R0860","ZWD-R0884",25))
  self.assertEqual(b["source_original_codepoint_range"],[41672,42541])
  self.assertTrue(b["source_yangling_ambiguous_two_contexts_preserved"])
  for key,name in (("rules_sha256","ZIWEI_DISEASE_25_SOURCE_NOTES_V1.json"),("witness_sha256","SOURCE_DISEASE_25_EXACT_OFFSET_WITNESS_V1.json"),("original_excerpt_sha256","SOURCE_1963110_DISEASE_EXACT_EXCERPT.txt")):
   self.assertEqual(b[key],sha(B/name))
 def test_old_western_and_previous_current(self):
  self.assertEqual(sha(WEST),"c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")
  self.assertEqual(WEST.read_bytes(),(B/"recovery/WESTERN_B07bc_BEFORE_21.json").read_bytes())
  self.assertEqual(sha(B/"recovery/CHINESE_V20_BEFORE_21.json"),sha(OLD))
  self.assertIn((B/"recovery/CHINESE_CURRENT_BEFORE_21.md").read_text(),(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text())
 def test_archive_CRC_member_hash_and_cold_tests(self):
  a=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
  self.assertEqual(a["independent_cold_original_source_tests_green"],12)
  p=Path(a["archive_path_on_owner_computer"])
  self.assertEqual(sha(p),a["archive_sha256"])
  with ZipFile(p) as z:
   self.assertIsNone(z.testzip())
   m=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
   self.assertEqual(len(m["members"]),15)
   for name,record in m["members"].items():
    raw=z.read(name)
    self.assertEqual((hashlib.sha256(raw).hexdigest(),len(raw)),(record["sha256"],record["bytes"]))
 def test_acceptance_report(self):
  receipt=rd(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
  self.assertEqual((receipt["Chinese_before"],receipt["Chinese_after"]),(1069,1094))
  self.assertEqual(receipt["new_index_V21_SHA256"],sha(NEW))
  self.assertEqual((receipt["real_human_blind_predictive_validations"],receipt["runtime_astrological_promotions"]),(0,0))
if __name__=="__main__":
 unittest.main()
