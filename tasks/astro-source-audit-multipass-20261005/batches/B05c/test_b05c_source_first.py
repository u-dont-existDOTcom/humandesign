import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==74 and len(spans)==7
 assert [r["source_local_id"] for r in rows]==[f"HYLEG-C{k:03}" for k in range(1,75)]
 ids=[x for s in spans for x in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==74
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[x]["source_span_id"]==s["span_id"] and
 set(by[x]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
 for s in spans for x in s["mapped_local_ids"])
 assert all(r["chapter"]=="CV" for r in rows[:-3])
 assert all(r["chapter"]=="CVI_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and
 not r["independently_authenticated_death_or_survival"] and
 not r["medical_longevity_prediction_validated"] and not r["empirically_validated_prediction"] and
 not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_first_edition_source_to_clause_bijection(self):check(D,M)
 def test_six_full_page_sha256_witnesses(self):
  self.assertEqual([w["original_pdf_page"] for w in W["original_images"]],list(range(561,567)))
  for w in W["original_images"]:
   raw=(B/w["path"]).read_bytes()
   self.assertEqual(len(raw),w["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),w["sha256"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_continuity_and_distinct_following_chapter(self):
  self.assertEqual(W["prior_lilly_accepted"],6309)
  self.assertEqual(W["next_global_record"],6310)
  self.assertEqual(W["following_heading_pdf_page"],565)
  self.assertEqual(W["following_printed_chapter"],"CV")
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),3)
  self.assertEqual(len([r for r in D if len(r["original_pdf_pages"])>1]),3)
 def test_proper_degrees_and_fallbacks(self):
  self.assertTrue(W["source_25_degree_ascendant_exception"])
  self.assertEqual(W["source_Anareta_eighth_cusp_window_before_after_degrees"],[5,25])
  alltext=" ".join((r["historical_author_paraphrase"]+" "+r["original_source_qualifications"]).lower() for r in D)
  for q in ("ascendant","nighttime","day","eighth","moon","part of fortune","syzygy","three essential"):
   self.assertIn(q,alltext,q)
 def test_source_author_explicitly_uncertain(self):
  self.assertTrue(W["source_hyleg_anareta_alcochodon_uncertainty_admitted"])
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("unsatisfied",t)
  self.assertIn("not satisfied",t)
  self.assertIn("does not approve",t)
 def test_three_source_terms_and_multiple_competing_models(self):
  txt=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for word in ("hyleg","anareta","alcochodon","sextiles","comets","eclipses","other methods"):
   self.assertIn(word,txt,word)
 def test_nobody_scored_or_clinically_validated(self):
  self.assertEqual(W["independent_actual_deaths_or_birth_times"],0)
  self.assertFalse(W["source_Alcochodon_numeric_year_values_independently_verified"])
  self.assertEqual(W["empirical_validations"],0)
  self.assertEqual(W["runtime_promotions"],0)
  self.assertEqual(len(U["issues"]),30)
 def test_next_chapter_nav_does_not_import_dignity_rules(self):
  self.assertTrue(all(r["chapter"]=="CVI_NAVIGATION_ONLY" for r in D[-3:]))
  self.assertTrue(all(r["original_pdf_pages"][0]>=565 for r in D[-3:]))
 def test_fabricated_verified_death_mutant_fails(self):
  x=copy.deepcopy(D);x[22]["independently_authenticated_death_or_survival"]=True
  with self.assertRaises(AssertionError):check(x,M)
 def test_duplicate_source_span_mutant_fails(self):
  x=copy.deepcopy(M);x[0]["mapped_local_ids"].append(x[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,x)
 def test_next_chapter_contamination_mutant_fails(self):
  x=copy.deepcopy(D);x[-1]["chapter"]="CV"
  with self.assertRaises(AssertionError):check(x,M)
if __name__=="__main__":unittest.main(verbosity=2)
