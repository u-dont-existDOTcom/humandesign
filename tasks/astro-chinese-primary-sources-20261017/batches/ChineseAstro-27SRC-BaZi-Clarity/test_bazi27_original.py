#!/usr/bin/env python3
"""Independent source-only checks for Di Tian Sui chapter 21."""
from pathlib import Path
from hashlib import sha256
import json,re,unittest
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_21_oldid844371.wikitext"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V26.json"
NOTES=B/"BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS21_4_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_21_SOURCE_MANIFEST_V1.json"
ACCEPT=B/"ACCEPTANCE.json"
EXPECTED_SOURCE="9ff7673e7a7a8af1cace52457d801d631ca117f5923e8e3433f7b1d05729be0f"
EXPECTED_INDEX="f4b69767eb143994766bc9a7c08f7ed1e519bddf234377c9ecc65bcb6080f94f"
def digest(blob):return sha256(blob).hexdigest()
def load(path):return json.loads(path.read_text(encoding="utf-8"))
class DTS21Source(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=RAW.read_bytes();cls.text=cls.raw.decode("utf-8")
  cls.docs=load(NOTES);cls.rows=cls.docs["records"];cls.wit=load(WIT)
 def test_full_original_raw_sha_length(self):
  self.assertEqual((len(self.raw),len(self.text),digest(self.raw)),(1172,474,EXPECTED_SOURCE))
 def test_source_manifest_revision(self):
  m=load(MAN)
  self.assertEqual((m["original_online_oldid"],m["raw_source_UTF8_bytes"],m["sha256"]),(844371,1172,EXPECTED_SOURCE))
 def test_previous_chinese_source_index_pinned(self):
  self.assertEqual(digest(OLD.read_bytes()),EXPECTED_INDEX)
  prev=load(OLD)
  self.assertEqual((prev["sum_source_annotations"],prev["systems"][0]["next_id"],prev["systems"][1]["accepted_source_annotations"]),(1277,"BZI-R0219",1059))
 def test_original_four_complete_source_units(self):
  verses=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",self.text,re.S)
  commentary=re.findall(r"(?m)^:　　(.+)$",self.text)
  self.assertEqual([row["original_chinese_exact_quote"] for row in self.rows],[verses[0],commentary[0],verses[1],commentary[1]])
  self.assertEqual((len(verses),len(commentary)),(2,2))
 def test_exact_byte_cp_and_quote_sha_replay(self):
  self.assertEqual(len(self.rows),len(self.wit["quotes"]))
  for row,wit in zip(self.rows,self.wit["quotes"]):
   q=row["original_chinese_exact_quote"];cp=row["original_codepoint_offset"]
   bp=row["original_utf8_byte_offset"];raw=q.encode("utf-8")
   self.assertEqual(self.text[cp:cp+len(q)],q,row["id"])
   self.assertEqual(self.raw[bp:bp+len(raw)],raw,row["id"])
   self.assertEqual(bp,len(self.text[:cp].encode("utf-8")),row["id"])
   self.assertEqual((row["original_quote_sha256"],row["original_quote_utf8_bytes"]),(digest(raw),len(raw)),row["id"])
   self.assertEqual((wit["id"],wit["cp"],wit["utf8_byte"],wit["quote_sha256"]),(row["id"],cp,bp,digest(raw)),row["id"])
 def test_verse_polarity_in_pinned_source(self):
  self.assertIn("一清到底有清神",self.rows[0]["original_chinese_exact_quote"])
  self.assertIn("半濁半清無去取",self.rows[2]["original_chinese_exact_quote"])
  self.assertNotIn("半濁半清猶是可",self.text)
 def test_source_ids_and_next_frontier(self):
  self.assertEqual([row["id"] for row in self.rows],["BZI-R0219","BZI-R0220","BZI-R0221","BZI-R0222"])
  self.assertEqual(self.docs["next_id"],"BZI-R0223")
  self.assertEqual(self.docs["next_ZiWei_id"],"ZWD-R1060")
 def test_accepted_witness_sha_and_candidate_arithmetic(self):
  acc=load(ACCEPT)
  self.assertEqual((acc["Chinese_before"],acc["new_records"],acc["Chinese_after"]),(1277,4,1281))
  self.assertEqual((acc["BaZi_after"],acc["ZiWei_unchanged"]),(222,1059))
  self.assertEqual((acc["notes_sha256"],acc["witness_sha256"]),(digest(NOTES.read_bytes()),digest(WIT.read_bytes())))
 def test_original_only_not_human_success(self):
  self.assertFalse(self.docs["original_printed_critical_edition_authenticated"])
  self.assertFalse(self.docs["calendar_and_natal_computation_independently_validated"])
  self.assertEqual((self.docs["human_blind_predictive_validations"],self.docs["runtime_astrology_promotions"]),(0,0))
  for row in self.rows:
   self.assertFalse(row["original_early_print_authenticated"])
   self.assertEqual((row["independent_blinded_human_predictions_validated"],row["runtime_promotions"]),(0,0))
 def test_readonly_freezer_reconstruction(self):
  from freeze_bazi21_source import verify
  self.assertEqual(len(verify()["records"]),4)
if __name__=="__main__":unittest.main()
