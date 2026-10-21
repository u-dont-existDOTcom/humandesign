#!/usr/bin/env python3
"""BaZi DTS22 source text regression; ancient ethics/wealth claims not human evidence."""
from pathlib import Path
from hashlib import sha256
import json,re,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_22_oldid844372.wikitext"
PRIOR=T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json"
NOTES=B/"BAZI_DITIAN_SUI_22_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS22_4_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_22_SOURCE_MANIFEST_V1.json"
ACC=B/"ACCEPTANCE.json"
SOURCE_SHA="50779be0d79b31711371bca6669a85c36110d4f5c25937d5e794c5c8c7515333"
OLD_SHA="00de501124cfba8167a52e0fc294ed3a25d1bc90bb98a8ae039c8627301f9d39"
def sha(b):return sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class DTS22Original(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=RAW.read_bytes();cls.s=cls.raw.decode("utf-8")
  cls.doc=rd(NOTES);cls.rows=cls.doc["records"];cls.witness=rd(WIT)
 def test_original_raw_revision_sha_bytes(self):
  self.assertEqual((sha(self.raw),len(self.raw),len(self.s)),(SOURCE_SHA,1121,457))
 def test_pinned_source_manifest(self):
  m=rd(MAN)
  self.assertEqual((m["online_oldid"],m["raw_UTF8_bytes"],m["raw_SHA256"]),(844372,1121,SOURCE_SHA))
 def test_accepted_previous_index_exact(self):
  self.assertEqual(sha(PRIOR.read_bytes()),OLD_SHA)
  x=rd(PRIOR)
  self.assertEqual((x["sum_source_annotations"],x["systems"][0]["next_id"],x["systems"][1]["accepted_source_annotations"]),(1281,"BZI-R0223",1059))
 def test_complete_original_verses_and_commentaries(self):
  verses=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",self.s,re.S)
  comments=re.findall(r"(?m)^:　　(.+)$",self.s)
  self.assertEqual((len(verses),len(comments)),(2,2))
  self.assertEqual([x["original_chinese_exact_quote"] for x in self.rows],[verses[0],comments[0],verses[1],comments[1]])
 def test_all_quote_cp_utf8_hash_exact(self):
  self.assertEqual(len(self.rows),len(self.witness["quotes"]))
  for r,w in zip(self.rows,self.witness["quotes"]):
   q=r["original_chinese_exact_quote"];cp=r["original_codepoint_offset"];bp=r["original_utf8_byte_offset"];enc=q.encode("utf-8")
   self.assertEqual(self.s[cp:cp+len(q)],q,r["id"])
   self.assertEqual(self.raw[bp:bp+len(enc)],enc,r["id"])
   self.assertEqual(bp,len(self.s[:cp].encode("utf-8")),r["id"])
   self.assertEqual((r["original_quote_sha256"],r["original_quote_utf8_bytes"]),(sha(enc),len(enc)),r["id"])
   self.assertEqual((w["id"],w["cp"],w["utf8_byte"],w["quote_sha256"]),(r["id"],cp,bp,sha(enc)),r["id"])
 def test_contingent_hidden_source_conditions_preserved(self):
  self.assertIn("令上尋真聚得真",self.rows[0]["original_chinese_exact_quote"])
  self.assertIn("真假參差難辨論",self.rows[2]["original_chinese_exact_quote"])
  self.assertIn("生寅月",self.rows[1]["original_chinese_exact_quote"])
  self.assertIn("戊巳轉生",self.rows[3]["original_chinese_exact_quote"])
  self.assertIn("乙庚暗化",self.rows[3]["original_chinese_exact_quote"])
 def test_ids_frontier(self):
  self.assertEqual([r["id"] for r in self.rows],[f"BZI-R{i:04d}" for i in range(223,227)])
  self.assertEqual(self.doc["next_id"],"BZI-R0227")
  self.assertEqual(self.doc["next_ZiWei_id"],"ZWD-R1060")
 def test_unverified_status_and_no_person_claims(self):
  self.assertFalse(self.doc["original_printed_critical_edition_authenticated"])
  self.assertFalse(self.doc["calendar_and_natal_computation_independently_validated"])
  self.assertEqual((self.doc["human_blind_predictive_validations"],self.doc["runtime_astrology_promotions"]),(0,0))
  for r in self.rows:
   self.assertFalse(r["early_original_print_authenticated"])
   self.assertEqual((r["independently_blinded_human_predictions_validated"],r["runtime_promotions"]),(0,0))
 def test_acceptance_candidates_and_hashes(self):
  a=rd(ACC)
  self.assertEqual((a["Chinese_before"],a["new_records"],a["Chinese_after"]),(1281,4,1285))
  self.assertEqual((a["BaZi_before"],a["BaZi_after"],a["ZiWei_unchanged"]),(222,226,1059))
  self.assertEqual((a["notes_sha256"],a["witness_sha256"]),(sha(NOTES.read_bytes()),sha(WIT.read_bytes())))
if __name__=="__main__":unittest.main()
