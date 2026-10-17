import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"];W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rs,sp):
 assert len(rs)==32 and len(sp)==6
 assert [r["source_local_id"] for r in rs]==[f"GENITURE-C{k:03}" for k in range(1,33)]
 flat=[x for q in sp for x in q["mapped_local_ids"]]
 assert len(flat)==len(set(flat))==32
 assert set(flat)=={r["source_local_id"] for r in rs}
 lookup={r["source_local_id"]:r for r in rs}
 assert all(lookup[x]["source_span_id"]==q["span_id"] and set(lookup[x]["original_pdf_pages"]).issubset(set(q["original_pdf_pages"])) for q in sp for x in q["mapped_local_ids"])
 assert all(r["chapter"]=="CVI" for r in rs[:-3])
 assert all(r["chapter"]=="CVII_NAVIGATION_ONLY" for r in rs[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
    and not r["independently_verified_lord_geniture_personality"]
    and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
class Source(unittest.TestCase):
 def test_bidirectional_source_coverage(self):check(D,M)
 def test_page_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[565,566,567])
  for x in W["original_images"]:
   raw=(B/x["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
   self.assertEqual(len(raw),x["bytes"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_true_page_seams(self):
  self.assertEqual([r["original_pdf_pages"] for r in D if len(r["original_pdf_pages"])>1],[[565,566]])
  self.assertEqual(D[-1]["original_pdf_pages"],[567])
  self.assertEqual(W["following_heading_pdf"],566)
  self.assertEqual(W["prior_lilly_accepted"],6383)
 def test_distinct_rejected_Firmicus_and_accepted_Lilly(self):
  self.assertTrue(W["source_discarded_Firmicus_rule"])
  self.assertTrue(W["source_author_near_equal_planet_mixture"])
  content=" ".join((r["short_original_anchor_not_diplomatic"]+" "+r["historical_author_paraphrase"]+" "+r["original_source_qualifications"]).lower() for r in D)
  for phrase in ("rejected","aries","leo","venus","mercury","essential and accidental",
     "near-equal","mixture","moon","temperament"):
   self.assertIn(phrase,content,phrase)
 def test_separate_Greek_Moon_Mercury(self):
  self.assertTrue(any("Greek practitioners" in r["historical_author_paraphrase"] for r in D))
  self.assertTrue(any("mind or spirit" in r["historical_author_paraphrase"] for r in D))
  self.assertTrue(any("body" in r["historical_author_paraphrase"] for r in D))
 def test_no_proof_and_unresolved_thresholds(self):
  self.assertEqual(len(U["issues"]),19)
  self.assertFalse(any(r["independently_verified_lord_geniture_personality"] for r in D))
 def test_duplicate_mutant(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,s)
 def test_next_chapter_leak_mutant(self):
  rs=copy.deepcopy(D);rs[-1]["chapter"]="CVI"
  with self.assertRaises(AssertionError):check(rs,M)
 def test_empirical_inflation_mutant(self):
  rs=copy.deepcopy(D);rs[21]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(rs,M)
if __name__=="__main__":unittest.main(verbosity=2)
