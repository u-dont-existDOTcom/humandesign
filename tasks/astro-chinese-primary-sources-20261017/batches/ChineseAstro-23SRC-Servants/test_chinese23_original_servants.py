#!/usr/bin/env python3
"""Source integrity only: do not validate class or employment stereotypes."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V22.json"
NOTES=B/"ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_SERVANTS_26_OFFSET_WITNESS_V1.json"
EX=B/"SOURCE_1963110_SERVANTS_EXACT_EXCERPT.txt"
SOURCE_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA="3c3d74b9f53d10e7905f026733d902511bf19f2f0f64ae34bed9f4af894bba68"
def sha(b):return hashlib.sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class HistoricalServantsOriginal(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=RAW.read_bytes()
  cls.s=cls.raw.decode("utf-8")
  cls.notes=rd(NOTES)
  cls.records=cls.notes["records"]
  cls.wit=rd(WIT)
 def test_exact_full_transmitted_original_sha(self):
  self.assertEqual((len(self.raw),sha(self.raw)),(106736,SOURCE_SHA))
  self.assertEqual(len(self.s),48890)
 def test_prior_accepted_source_and_bazi_counts(self):
  self.assertEqual(sha(OLD.read_bytes()),OLD_SHA)
  idx=rd(OLD)
  self.assertEqual((idx["sum_source_annotations"],idx["systems"][0]["accepted_source_annotations"],idx["systems"][1]["accepted_source_annotations"]),(1120,210,910))
  self.assertEqual(idx["systems"][1]["next_id"],"ZWD-R0911")
 def test_exact_original_excerpt_and_next_section(self):
  self.assertEqual(EX.read_bytes(),self.s[43499:44429].encode("utf-8"))
  self.assertEqual(sha(EX.read_bytes()),"fb73b75c2b148e864a16fcffe9cdc6f28d9b86527c6fa0ee41543740794058f7")
  self.assertTrue(self.s[43499:].startswith("===八奴仆==="))
  self.assertTrue(self.s[44429:].startswith("===九官禄==="))
 def test_source_has_25_physical_lines_and_poem_tags(self):
  excerpt=self.s[43499:44429]
  physical=[l.strip() for l in excerpt.splitlines() if l.strip() and l.strip() not in ("<poem>","</poem>")]
  self.assertEqual(len(physical),25)
  self.assertEqual([r["original_Chinese_exact_quote"] for r in self.records[:-1]],physical)
  self.assertEqual([x[1] for x in self.notes["original_poem_markup"]],["<poem>","</poem>"])
 def test_original_26_source_ids_are_consecutive(self):
  self.assertEqual([r["id"] for r in self.records],[f"ZWD-R{i:04d}" for i in range(911,937)])
  self.assertEqual(self.records[0]["source_kind"],"SOURCE_HEADING")
  self.assertEqual(self.records[-1]["source_kind"],"NEXT_CAREER_HEADING_NAVIGATION_ONLY")
  self.assertEqual(self.records[-1]["absolute_cp"],44429)
  self.assertEqual(self.notes["next_id"],"ZWD-R0937")
 def test_every_quote_exact_original_unicode_utf8_and_hash(self):
  self.assertEqual(len(self.records),len(self.wit["records"]))
  for row,witness in zip(self.records,self.wit["records"]):
   q=row["original_Chinese_exact_quote"]
   cp=row["absolute_cp"];bp=row["absolute_utf8_offset"]
   encoded=q.encode("utf-8")
   self.assertEqual(self.s[cp:cp+len(q)],q,row["id"])
   self.assertEqual(self.raw[bp:bp+len(encoded)],encoded,row["id"])
   self.assertEqual(len(self.s[:cp].encode("utf-8")),bp,row["id"])
   self.assertEqual(sha(encoded),row["quote_SHA256"],row["id"])
   self.assertEqual((witness["id"],witness["cp"],witness["utf8_offset"],witness["quote_SHA256"]),(row["id"],cp,bp,sha(encoded)))
 def test_source_conditional_hierarchies_not_modern_employee_truth(self):
  self.assertTrue(self.notes["historic_class_and_trustworthiness_claims_unverified"])
  self.assertFalse(self.notes["early_printing_authenticated"])
  self.assertEqual((self.notes["real_human_blind_predictions_validated"],self.notes["runtime_promotions"]),(0,0))
  for r in self.records:
   self.assertFalse(r["original_Ming_woodblock_authenticated"])
   self.assertEqual((r["human_predictive_validations"],r["runtime_promotions"]),(0,0))
if __name__=="__main__":
 unittest.main()
