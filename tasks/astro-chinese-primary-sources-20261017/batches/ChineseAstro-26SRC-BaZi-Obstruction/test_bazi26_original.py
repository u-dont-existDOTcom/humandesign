#!/usr/bin/env python3
"""Original BaZi Di Tian Sui section20 text source-only focused regression."""
from pathlib import Path
import hashlib,json,unittest,re
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_20_oldid844370.wikitext"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V25.json"
NOTES=B/"BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS20_2_EXACT_OFFSET_WITNESS_V1.json"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
class SourceOnly(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=RAW.read_bytes();cls.s=cls.raw.decode("utf-8")
  cls.doc=rd(NOTES);cls.rows=cls.doc["records"];cls.w=rd(WIT)
 def test_full_original_sha_utf8_bytes(self):
  self.assertEqual((len(self.raw),sha(self.raw)),(577,"f646b66d51d6cd69a376e2b4e754c0b872ccbe24879772954579e03ae3639022"))
  self.assertEqual(len(self.s),259)
 def test_source_manifest_actual_revision(self):
  m=rd(B/"PINNED_DITIAN_SUI_20_SOURCE_MANIFEST_V1.json")
  self.assertEqual((m["oldid"],m["source_UTF8_bytes"],m["sha256"]),
    (844370,577,"f646b66d51d6cd69a376e2b4e754c0b872ccbe24879772954579e03ae3639022"))
 def test_prior_V25_source_index_and_next(self):
  self.assertEqual(sha(OLD.read_bytes()),"f5d2c95d6225bddc4b8a99fc5ddd923d61424a2002d5bb146c8693f72644c0df")
  i=rd(OLD)
  self.assertEqual((i["sum_source_annotations"],i["systems"][0]["next_id"]),(1275,"BZI-R0217"))
 def test_original_verse_and_one_full_commentary(self):
  self.assertEqual([x["source_layer"] for x in self.rows],
    ["transmitted_verse","original_full_commentary"])
  self.assertEqual(self.rows[0]["original_exact_Chinese_quote"],
    "兩意本相通，中間有關隔，此關若通也，到處歡相得。")
  self.assertIn("木土而得火",self.rows[1]["original_exact_Chinese_quote"])
  self.assertIn("關通則滿局皆順遂矣",self.rows[1]["original_exact_Chinese_quote"])
  self.assertEqual(len(re.findall(r"(?m)^:　　(.+)$",self.s)),1)
 def test_independent_byte_unicode_and_SHA_witnesses(self):
  self.assertEqual(len(self.w["source_quotes"]),2)
  for r,w in zip(self.rows,self.w["source_quotes"]):
   q=r["original_exact_Chinese_quote"];cp=r["original_source_codepoint_offset"]
   b=r["original_source_utf8_byte_offset"];enc=q.encode("utf-8")
   self.assertEqual(self.s[cp:cp+len(q)],q,r["id"])
   self.assertEqual(self.raw[b:b+len(enc)],enc,r["id"])
   self.assertEqual(len(self.s[:cp].encode("utf-8")),b,r["id"])
   self.assertEqual(sha(enc),r["quote_SHA256"],r["id"])
   self.assertEqual((w["id"],w["codepoint"],w["utf8_byte_offset"],w["quote_sha256"]),
    (r["id"],cp,b,sha(enc)))
 def test_two_consecutive_ids_and_next(self):
  self.assertEqual([r["id"] for r in self.rows],["BZI-R0217","BZI-R0218"])
  self.assertEqual(self.doc["next_id"],"BZI-R0219")
  self.assertEqual(self.doc["next_ZiWei_source_unchanged"],"ZWD-R1060")
 def test_no_ancient_print_or_blinded_human_claim(self):
  self.assertFalse(self.doc["original_ancient_book_critically_authenticated"])
  self.assertFalse(self.doc["source_hidden_stems_and_chart_engine_independently_verified"])
  self.assertEqual((self.doc["real_human_blind_predictions_validated"],self.doc["runtime_astrological_promotions"]),(0,0))
  for r in self.rows:
   self.assertFalse(r["original_early_print_authority_authenticated"])
   self.assertEqual((r["real_human_predictions_validated"],r["runtime_astrology_promotions"]),(0,0))
 def test_acceptance_candidate_exact_counts(self):
  a=rd(B/"ACCEPTANCE.json")
  self.assertEqual((a["Chinese_before"],a["new_original_source_notes"],a["Chinese_after_if_accepted"]),
   (1275,2,1277))
  self.assertEqual((a["BaZi_before"],a["BaZi_after_if_accepted"],a["ZiWei_unchanged"]),(216,218,1059))
  self.assertEqual((a["source_note_sha256"],a["source_witness_sha256"]),(sha(NOTES.read_bytes()),sha(WIT.read_bytes())))
if __name__=="__main__":unittest.main()
