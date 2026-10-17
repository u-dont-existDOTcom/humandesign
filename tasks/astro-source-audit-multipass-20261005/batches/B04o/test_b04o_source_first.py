import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==53 and len(spans)==10
 assert [r["source_local_id"] for r in rows]==[f"XCV-C{i:03}" for i in range(1,54)]
 ids=[i for s in spans for i in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==53
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["source_span_id"]==s["span_id"] and
   by[k]["original_pdf_pages"]==s["original_pdf_pages"]
   for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="XCV" for r in rows[:-3])
 assert all(r["chapter"]=="XCVI_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
   and not r["independently_authenticated_occult_cause"]
   and not r["independently_authenticated_medical_diagnosis"]
   and not r["independently_verified_medical_recovery"]
   and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class SourceFirst(unittest.TestCase):
 def test_unique_original_span_mapping(self):check(D,M)
 def test_first_edition_original_image_hashes(self):
  self.assertEqual([a["original_pdf_page"] for a in W["original_images"]],[502,503,504])
  for a in W["original_images"]:
   p=B/a["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),a["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),a["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"d26b42ed22eb9851a9e768dc1fa0ad53dd381dafc81ae0b0197e46f3d6bdc639")
 def test_previous_accepted_and_printed_chapter(self):
  self.assertEqual(W["previous_accepted_lilly"],5457)
  self.assertEqual(W["next_global_record"],5458)
  self.assertEqual(W["next_numbered_chapter"],"XCVI")
  self.assertEqual(W["next_printed_chapter"],"XCV")
  self.assertEqual(W["following_heading_pdf"],504)
  self.assertEqual(W["original_body_pdf_pages"],[502,503])
 def test_witchcraft_suspicion_then_explicit_denial(self):
  self.assertTrue(W["initial_source_witchcraft_suspicion"])
  self.assertTrue(W["ultimate_source_witchcraft_denial"])
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("raised suspicion",t)
  self.assertIn("rejects the suspected bewitchment",t)
 def test_disease_hypothesis_not_confirmed(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for k in ("private parts","sexual activity","itching","blood was corrupted","declines to assert a definitive"):
   self.assertIn(k,t)
  self.assertEqual(len([r for r in D if r["role"]=="authorial_health_allegation"]),6)
  self.assertTrue(all(not r["independently_authenticated_medical_diagnosis"] for r in D))
 def test_medical_course_and_recovery_claims_separate(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for k in ("prior medicine","had not helped","had worsened","physicians again","regimen was changed","three weeks"):
   self.assertIn(k,t)
  self.assertTrue(W["author_claims_medical_recovery_approximately_three_weeks"])
  self.assertFalse(W["independently_authenticated_medical_record"])
 def test_dated_next_prisoner_chart_not_leaked(self):
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),3)
  self.assertTrue(all(r["chapter"]=="XCVI_NAVIGATION_ONLY" for r in D[-3:]))
  self.assertIn("6 June 1647",D[-2]["historical_author_paraphrase"])
 def test_source_limits_retained(self):
  self.assertEqual(len(U["issues"]),22)
  self.assertTrue(any("syphilis" in x["issue"].lower() for x in U["issues"]))
 def test_duplicate_map_mutant_detected(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,s)
 def test_false_confirmed_syphilis_mutant_detected(self):
  s=copy.deepcopy(D);s[44]["independently_authenticated_medical_diagnosis"]=True
  with self.assertRaises(AssertionError):check(s,M)
 def test_false_occult_causation_mutant_detected(self):
  s=copy.deepcopy(D);s[14]["independently_authenticated_occult_cause"]=True
  with self.assertRaises(AssertionError):check(s,M)
 def test_next_chapter_contamination_mutant_detected(self):
  s=copy.deepcopy(D);s[-1]["chapter"]="XCV"
  with self.assertRaises(AssertionError):check(s,M)
if __name__=="__main__":unittest.main(verbosity=2)
