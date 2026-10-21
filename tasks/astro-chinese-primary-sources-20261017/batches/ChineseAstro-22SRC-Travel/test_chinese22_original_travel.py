#!/usr/bin/env python3
"""Pinned Wikitext textual-integrity tests for Zi Wei Travel source."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V21.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES=B/"ZIWEI_TRAVEL_26_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_TRAVEL_26_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_TRAVEL_EXACT_EXCERPT.txt"
def sha(b):return hashlib.sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class SourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=RAW.read_bytes()
  cls.s=cls.raw.decode("utf-8")
  cls.doc=rd(NOTES)
  cls.rows=cls.doc["records"]
  cls.wit=rd(WIT)
 def test_full_original_text_sha(self):
  self.assertEqual((len(self.raw),sha(self.raw)),(106736,"1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"))
 def test_previous_sources_sha(self):
  self.assertEqual(sha(OLD.read_bytes()),"0b22a13f164891fa60be0b8630aa6ed131cf27f425ad492557a9d814d7375c03")
  self.assertEqual(sha(WEST.read_bytes()),"c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")
  self.assertEqual(rd(OLD)["sum_source_annotations"],1094)
 def test_exact_excerpt_and_boundaries(self):
  self.assertEqual(EXCERPT.read_bytes(),self.s[42541:43499].encode("utf-8"))
  self.assertEqual(sha(EXCERPT.read_bytes()),"36a07bb63bb432864a60b16c89004812e6c8ba7b6c7210c22987ddaf55d44ba6")
  self.assertTrue(self.s[42541:].startswith("===七迁移==="))
  self.assertTrue(self.s[43499:].startswith("===八奴仆==="))
 def test_physical_source_lines_tags(self):
  x=self.s[42541:43499]
  lines=[l.strip() for l in x.splitlines() if l.strip() and l.strip() not in ("<poem>","</poem>")]
  self.assertEqual(len(lines),25)
  self.assertEqual([r["original_exact_Chinese_Wikitext_quote"] for r in self.rows[:-1]],lines)
  self.assertEqual([q[1] for q in self.doc["original_poem_markup"]],["<poem>","</poem>"])
 def test_every_exact_offset_quote_sha_and_witness(self):
  self.assertEqual(len(self.rows),len(self.wit["quote_witnesses"]))
  for a,b in zip(self.rows,self.wit["quote_witnesses"]):
   txt=a["original_exact_Chinese_Wikitext_quote"]
   cp=a["original_codepoint_offset"]
   byte=a["original_UTF8_byte_offset"]
   encoded=txt.encode("utf-8")
   self.assertEqual(self.s[cp:cp+len(txt)],txt,a["id"])
   self.assertEqual(self.raw[byte:byte+len(encoded)],encoded,a["id"])
   self.assertEqual(len(self.s[:cp].encode("utf-8")),byte,a["id"])
   self.assertEqual((sha(encoded),len(encoded)),(a["quote_SHA256"],a["quote_UTF8_bytes"]))
   self.assertEqual((b["id"],b["cp"],b["UTF8_offset"],b["quote_SHA256"]),(a["id"],cp,byte,sha(encoded)))
 def test_original_uncertainties_not_repaired(self):
  self.assertEqual([r["id"] for r in self.rows if r.get("suspicious_fuchi_segment")],["ZWD-R0892"])
  self.assertEqual([r["id"] for r in self.rows if r.get("taiyin_self_conjunction_source_ambiguous")],["ZWD-R0893"])
 def test_all_ids_and_following_navigation(self):
  self.assertEqual([r["id"] for r in self.rows],[f"ZWD-R{x:04d}" for x in range(885,911)])
  self.assertEqual(self.rows[-1]["source_kind"],"NEXT_SERVANTS_SOURCE_NAVIGATION_ONLY")
  self.assertEqual(self.rows[-1]["original_codepoint_offset"],43499)
  self.assertEqual(self.doc["next_id"],"ZWD-R0911")
 def test_historical_only_no_real_person_predictions(self):
  self.assertFalse(self.doc["original_printed_woodblock_authenticated"])
  self.assertEqual((self.doc["real_human_blind_forecasts_validated"],self.doc["runtime_astrology_promotions"]),(0,0))
  self.assertTrue(all(not r["Ming_woodblock_imprint_authenticated"] and not r["real_person_travel_outcomes_predictively_verified"] for r in self.rows))
 def test_new_candidate_source_arithmetic(self):
  a=rd(B/"ACCEPTANCE.json")
  self.assertEqual((a["Chinese_before"],a["new_source_documentary_annotations"],a["Chinese_after_if_accepted"]),(1094,26,1120))
  self.assertEqual((a["BaZi_retained"],a["ZiWei_after_if_accepted"]),(210,910))
  self.assertEqual((a["source_notes_SHA256"],a["source_witness_SHA256"]),(sha(NOTES.read_bytes()),sha(WIT.read_bytes())))
if __name__=="__main__":
 unittest.main()
