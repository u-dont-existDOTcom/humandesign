import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def valid(rs,sp):
 assert len(rs)==86 and len(sp)==14
 assert [r["source_local_id"] for r in rs]==[f"MANNERS-C{i:03}" for i in range(1,87)]
 keys=[i for s in sp for i in s["mapped_local_ids"]]
 assert len(keys)==len(set(keys))==86
 assert set(keys)=={r["source_local_id"] for r in rs}
 by={r["source_local_id"]:r for r in rs}
 assert all(by[k]["source_span_id"]==s["span_id"] and set(by[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"])) for s in sp for k in s["mapped_local_ids"])
 assert all(r["chapter"]=="CVIII" for r in rs[:-3])
 assert all(r["chapter"]=="CIX_NAVIGATION_ONLY" for r in rs[-3:])
 assert all(not r["historical_documentary_accepted"] and r["global_record_number"] is None
  and not r["independently_validated_human_personality"]
  and not r["independently_validated_criminal_or_medical_prognosis"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
class Source(unittest.TestCase):
 def test_bijective_primary_source_trace(self):valid(D,M)
 def test_8_hash_frozen_original_pages(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],list(range(568,576)))
  for x in W["original_images"]:
   p=B/x["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),x["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_source_page_seams_and_next_heading(self):
  self.assertEqual([r["original_pdf_pages"] for r in D if len(r["original_pdf_pages"])>1],[[569,570],[570,571]])
  self.assertTrue(all(r["original_pdf_pages"]==[573] for r in D[-3:]))
  self.assertEqual(W["following_heading_pdf"],573)
  self.assertEqual(W["previous_accepted_lilly"],6474)
  self.assertEqual(W["next_global_record"],6475)
 def test_sign_stereotypes_all_twelve_and_four_humours(self):
  self.assertEqual(len([r for r in D if r["role"]=="sign_trait"]),12)
  self.assertEqual(len([r for r in D if r["role"]=="humour_manners"]),4)
  s=" ".join(r["short_original_anchor_not_diplomatic"].lower() for r in D)
  for z in ("aries","taurus","gemini","cancer","leo","virgo","libra","scorpio","sagittarius","capricorn","aquarius","pisces"):
   self.assertIn(z,s)
 def test_several_ascendant_mercury_moon_fallbacks_preserved(self):
  self.assertTrue(W["source_Mercury_Moon_Ascendant_fallbacks_multiple"])
  self.assertTrue(W["Moon_direction_manners_change_source"])
  self.assertTrue(len([r for r in D if r["role"]=="fallback"])>=4)
  self.assertTrue(any(r["role"]=="tie_rule" for r in D))
 def test_fixed_star_and_violent_claims_not_truth_labels(self):
  self.assertTrue(W["specific_fixed_star_violent_accusations_historical_only"])
  self.assertGreaterEqual(len([r for r in D if r["role"]=="star_trait"]),10)
  self.assertTrue(any(r["role"]=="historical_accusation" for r in D))
  self.assertTrue(all(not r["independently_validated_criminal_or_medical_prognosis"] for r in D))
 def test_author_rejects_fine_rising_degree_Angelus(self):
  self.assertTrue(W["Johannes_Angelus_fine_degree_scheme_author_rejected"])
  self.assertTrue(any("too rigid" in r["historical_author_paraphrase"] for r in D))
 def test_source_uncertainties_and_no_personality_test(self):
  self.assertEqual(len(U["issues"]),30)
  self.assertEqual(W["independently_validated_human_personality_matches"],0)
 def test_duplicate_passage_mutant_rejected(self):
  sp=copy.deepcopy(M);sp[0]["mapped_local_ids"].append(sp[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,sp)
 def test_false_verified_personality_mutant(self):
  rows=copy.deepcopy(D);rows[52]["independently_validated_human_personality"]=True
  with self.assertRaises(AssertionError):valid(rows,M)
 def test_false_violence_prediction_mutant(self):
  rows=copy.deepcopy(D);rows[64]["independently_validated_criminal_or_medical_prognosis"]=True
  with self.assertRaises(AssertionError):valid(rows,M)
 def test_next_chapter_merge_mutant(self):
  rows=copy.deepcopy(D);rows[-1]["chapter"]="CVIII"
  with self.assertRaises(AssertionError):valid(rows,M)
if __name__=="__main__":unittest.main(verbosity=2)
