import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json")
O=J("SOURCE_ORDER_DRAFT.json")
def valid(rs,spans):
 assert len(rs)==72 and len(spans)==11
 assert [r["source_local_id"] for r in rs]==[f"LXXXV-C{i:03}" for i in range(1,73)]
 seen=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(seen)==len(set(seen))==72
 assert set(seen)=={r["source_local_id"] for r in rs}
 by={r["source_local_id"]:r for r in rs}
 assert all(s["original_pdf_pages"]==by[k]["original_pdf_pages"] for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rs)
 assert all(r["chapter"]=="LXXXV" for r in rs[:-2])
 assert all(r["chapter"]=="LXXXVI_NAVIGATION_ONLY" for r in rs[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and
   not r["independently_authenticated_wartime_outcome"] and
   not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
class SourceFirst(unittest.TestCase):
 def test_original_bidirectional_coverage(self):
  valid(D,M["source_spans"])
  self.assertEqual(O["ordered_ids"],[r["source_local_id"] for r in D])
 def test_four_original_page_witnesses(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[486,487,488,489])
  for x in W["original_images"]:
   p=B/x["path"]; self.assertEqual(p.stat().st_size,x["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x["sha256"])
 def test_previous_authenticated_checkpoint_and_next_chapter(self):
  self.assertEqual(W["previous_accepted_lilly"],4954)
  self.assertEqual(W["next_numbered_chapter"],"LXXXVI")
  self.assertEqual(W["following_heading_pdf"],489)
  self.assertEqual(W["original_body_pdf_pages"],[486,487,488])
  self.assertIn("1642",W["original_question_timestamp"])
 def test_source_physical_seams(self):
  self.assertEqual([s["original_pdf_pages"] for s in M["source_spans"] if len(s["original_pdf_pages"])>1],[[486,487],[487,488]])
 def test_independent_forecast_vs_retrospective_history(self):
  roles=[r["role"] for r in D]
  self.assertIn("source_internal_forecast",roles)
  self.assertIn("authorial_historical_claim",roles)
  self.assertIn("authorial_outcome_claim",roles)
  self.assertEqual(roles.count("authorial_error_admission"),1)
  self.assertEqual(C["authorial_partial_error_acknowledgements"],1)
  self.assertTrue(C["pre_question_Edgehill_references_not_predictions"])
  self.assertEqual(C["independent_wartime_outcomes_verified"],0)
 def test_preserve_literal_capture_error_and_survival(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for s in ("twenty-four hours","not be killed","parliament would eventually have rupert","error in part","escaped","earlier","edgehill"):
   self.assertIn(s,text,s)
 def test_retained_evidence_uncertainty(self):
  self.assertEqual(len(U["issues"]),25)
  self.assertFalse(J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["independent_second_diplomatic_transcription"])
  self.assertEqual(C["new_empirically_validated_predictions"],0)
  self.assertEqual(C["runtime_promotions"],0)
 def test_mutant_duplicate_source_fails(self):
  m=copy.deepcopy(M["source_spans"]);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,m)
 def test_mutant_next_chapter_leak_fails(self):
  d=copy.deepcopy(D);d[-1]["chapter"]="LXXXV"
  with self.assertRaises(AssertionError):valid(d,M["source_spans"])
 def test_mutant_empirical_hit_fails(self):
  d=copy.deepcopy(D);d[50]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(d,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
