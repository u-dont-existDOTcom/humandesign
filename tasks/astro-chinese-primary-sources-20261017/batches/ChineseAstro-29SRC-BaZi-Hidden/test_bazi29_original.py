#!/usr/bin/env python3
"""Independent Di Tian Sui chapter23 full original verse/commentary source tests."""
from pathlib import Path
from hashlib import sha256
import json,re,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_23_oldid844373.wikitext"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V28.json"
NOTES=B/"BAZI_DITIAN_SUI_23_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS23_2_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_23_SOURCE_MANIFEST_V1.json"
RAW_SHA="a883ddf8509bda86e3ecadcb9a8d1bfdf7b6cc8901fe20044c64f3b730e54ac1"
OLD_SHA="67fbee144329c39892a004c75213e08a0ca05189e0d5f548bb49927dbb44d4c0"
def sha(b):return sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class DTS23Source(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=RAW.read_bytes();cls.s=cls.raw.decode("utf-8")
  cls.d=rd(NOTES);cls.rows=cls.d["records"];cls.w=rd(WIT)
 def test_original_full_Wikitext_revision_sha(self):
  self.assertEqual((len(self.raw),len(self.s),sha(self.raw)),(391,197,RAW_SHA))
 def test_source_manifest_pin(self):
  m=rd(MAN)
  self.assertEqual((m["pinned_oldid"],m["raw_bytes"],m["raw_sha256"]),(844373,391,RAW_SHA))
 def test_prior_accepted_source_sha_and_next(self):
  self.assertEqual(sha(OLD.read_bytes()),OLD_SHA)
  old=rd(OLD)
  self.assertEqual(old["sum_source_annotations"],1285)
  self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]],[(226,"BZI-R0227"),(1059,"ZWD-R1060")])
 def test_one_complete_source_verse_and_commentary(self):
  verses=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",self.s,re.S)
  commentary=re.findall(r"(?m)^:　　(.+)$",self.s)
  self.assertEqual((len(verses),len(commentary)),(1,1))
  self.assertEqual([r["original_exact_chinese_quote"] for r in self.rows],[verses[0],commentary[0]])
 def test_each_source_quote_CP_UTF8_and_SHA(self):
  self.assertEqual(len(self.rows),len(self.w["original_quotes"]))
  for r,w in zip(self.rows,self.w["original_quotes"]):
   q=r["original_exact_chinese_quote"];cp=r["absolute_cp"];byte=r["absolute_utf8_byte"];enc=q.encode("utf-8")
   self.assertEqual(self.s[cp:cp+len(q)],q,r["id"])
   self.assertEqual(self.raw[byte:byte+len(enc)],enc,r["id"])
   self.assertEqual(byte,len(self.s[:cp].encode("utf-8")),r["id"])
   self.assertEqual((r["original_quote_SHA256"],r["original_quote_UTF8_bytes"]),(sha(enc),len(enc)),r["id"])
   self.assertEqual((w["id"],w["cp"],w["utf8_byte"],w["quote_SHA256"]),(r["id"],cp,byte,sha(enc)),r["id"])
 def test_contextual_good_bad_not_universal_forecast(self):
  self.assertIn("吉神太露",self.rows[0]["original_exact_chinese_quote"])
  self.assertIn("凶物深藏",self.rows[0]["original_exact_chinese_quote"])
  self.assertIn("歲運傷之",self.rows[1]["original_exact_chinese_quote"])
  self.assertIn("歲運扶之",self.rows[1]["original_exact_chinese_quote"])
  self.assertIn("制化得所者亦吉",self.rows[1]["original_exact_chinese_quote"])
 def test_ids_and_following_source_order(self):
  self.assertEqual([r["id"] for r in self.rows],["BZI-R0227","BZI-R0228"])
  self.assertEqual((self.d["next_id"],self.d["next_ZiWei_id"]),("BZI-R0229","ZWD-R1060"))
 def test_no_human_predictions_or_early_original(self):
  self.assertFalse(self.d["ancient_printing_authenticated"])
  self.assertFalse(self.d["independent_natal_engine_parity_verified"])
  self.assertEqual((self.d["human_blind_predictive_validations"],self.d["runtime_promotions"]),(0,0))
  self.assertTrue(all(not r["original_early_print_authenticated"] and r["blind_human_predictions_validated"]==0 for r in self.rows))
 def test_candidate_counts_and_source_sha(self):
  x=rd(B/"ACCEPTANCE.json")
  self.assertEqual((x["Chinese_before"],x["new_notes"],x["Chinese_after_if_accepted"]),(1285,2,1287))
  self.assertEqual((x["BaZi_before"],x["BaZi_after_if_accepted"],x["ZiWei_unchanged"]),(226,228,1059))
  self.assertEqual((x["notes_SHA256"],x["witness_SHA256"]),(sha(NOTES.read_bytes()),sha(WIT.read_bytes())))
if __name__=="__main__":unittest.main()
