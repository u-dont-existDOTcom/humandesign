import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==65 and len(spans)==6
 assert [r["source_local_id"] for r in rows]==[f"LIFESPAN-C{k:03}" for k in range(1,66)]
 ids=[i for s in spans for i in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==65
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["source_span_id"]==s["span_id"] and
  set(by[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
  for s in spans for k in s["mapped_local_ids"])
 assert all(r["chapter"]=="CIV" for r in rows[:-3])
 assert all(r["chapter"]=="CV_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_infant_survival_outcome"]
  and not r["medical_survival_predictive_validity"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class OriginalSource(unittest.TestCase):
 def test_source_groups_exact_bijection(self):check(D,M)
 def test_first_edition_consecutive_source_images(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[559,560,561])
  for x in W["original_images"]:
   raw=(B/x["path"]).read_bytes()
   self.assertEqual(len(raw),x["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_shared_hyleg_chapter_boundary_not_merged(self):
  self.assertEqual(W["previous_accepted_lilly"],6244)
  self.assertEqual(W["first_global_record"],6245)
  self.assertEqual(W["following_hyleg_heading_pdf"],561)
  self.assertEqual(W["following_printed_chapter"],"CIV")
  self.assertEqual(W["following_editorial_chapter"],"CV")
  self.assertEqual([r["role"] for r in D[-3:]],["next_navigation"]*3)
 def test_two_documentary_cross_page_clauses_only(self):
  x=[r["source_local_id"] for r in D if len(r["original_pdf_pages"])==2]
  self.assertEqual(len(x),2)
  self.assertEqual(W["original_chapter_body_pdf_pages"],[559,560,561])
 def test_favorable_unfavorable_and_qualifying_conditions(self):
  s=" ".join((r["historical_author_paraphrase"]+" "+r["original_source_qualifications"]).lower() for r in D)
  for word in ("parents","full-moon","new moon","jupiter","venus","diurnal","nocturnal","significators","rashly"):
   self.assertIn(word,s,word)
 def test_medical_mortality_not_accepted_as_validity(self):
  self.assertFalse(W["source_mortality_clinical_evidence"])
  self.assertEqual(W["independent_survival_outcome_cases"],0)
  self.assertEqual(W["empirical_predictive_validations"],0)
  self.assertEqual(W["runtime_promotions"],0)
  self.assertEqual(len(U["issues"]),25)
 def test_source_no_categorical_lunar_phase_simplification(self):
  s=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("unfavorable",s)
  self.assertIn("favorable",s)
  self.assertIn("old age",s)
 def test_dont_pronounce_death_rashly_included(self):
  self.assertTrue(W["original_explicit_do_not_pronounce_death_rashly"])
  self.assertTrue(any(r["role"]=="authorial_caution" and "rashly" in r["historical_author_paraphrase"] for r in D))
 def test_false_prediction_mutant_rejected(self):
  x=copy.deepcopy(D);x[30]["medical_survival_predictive_validity"]=True
  with self.assertRaises(AssertionError):check(x,M)
 def test_double_source_map_mutant_rejected(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,s)
 def test_next_chapter_lifespan_merged_rejected(self):
  x=copy.deepcopy(D);x[-1]["chapter"]="CIV"
  with self.assertRaises(AssertionError):check(x,M)
if __name__=="__main__":unittest.main(verbosity=2)
