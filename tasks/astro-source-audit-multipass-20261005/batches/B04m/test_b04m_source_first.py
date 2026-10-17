import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==75 and len(spans)==11
 assert [r["source_local_id"] for r in rows]==[f"XCIII-C{i:03}" for i in range(1,76)]
 ids=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==75
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["source_span_id"]==s["span_id"] and
            set(by[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
            for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="XCIII" for r in rows[:-3])
 assert all(r["chapter"]=="XCIV_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_occult_causation"]
  and not r["independently_authenticated_treatment_success"]
  and not r["empirically_validated_prediction"]
  and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_source_first_passage_bijection(self):check(D,M)
 def test_original_image_hashes(self):
  self.assertEqual([w["original_pdf_page"] for w in W["original_images"]],[498,499,500,501])
  for w in W["original_images"]:
   p=B/w["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),w["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),w["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"ea46176b20798b54660faae58ccb5995678231d265f51b0a2848c1c037fa7151")
 def test_chapter_number_and_original_window(self):
  self.assertEqual(W["previous_accepted_lilly"],5338)
  self.assertEqual(W["next_global_record"],5339)
  self.assertEqual(W["original_body_pdf_pages"],[498,499,500])
  self.assertEqual(W["next_numbered_chapter"],"XCIV")
  self.assertEqual(W["next_printed_chapter"],"XCIII")
  self.assertEqual(W["following_heading_pdf"],501)
 def test_page_seams_and_precise_record_scopes(self):
  self.assertEqual([s["original_pdf_pages"] for s in M if len(s["original_pdf_pages"])>1],
                   [[498,499],[499,500]])
  multi=[(r["source_local_id"],r["original_pdf_pages"]) for r in D if len(r["original_pdf_pages"])>1]
  self.assertEqual(multi,[("XCIII-C029",[498,499]),("XCIII-C055",[499,500])])
 def test_historical_subheading_not_duplicate_chapter(self):
  self.assertEqual(len([r for r in D if r["role"]=="subheading"]),1)
  self.assertIn("Naturall Remedies",next(r["short_original_anchor_not_diplomatic"] for r in D if r["role"]=="subheading"))
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),3)
 def test_health_supernatural_claims_not_evidence(self):
  self.assertEqual(len([r for r in D if r["role"]=="authorial_outcome_claim"]),1)
  self.assertTrue(any("illness" in r["historical_author_paraphrase"] for r in D))
  self.assertTrue(any("spirits" in r["historical_author_paraphrase"] for r in D))
  self.assertTrue(all(not r["independently_authenticated_occult_causation"] for r in D))
 def test_hazardous_rituals_source_only(self):
  hs=[r for r in D if r["role"]=="historical_ritual"]
  self.assertEqual(len(hs),10)
  self.assertTrue(any("burn" in r["original_source_qualifications"].lower() or
                      "fire" in r["original_source_qualifications"].lower() for r in hs))
  self.assertEqual(len(U["issues"]),28)
 def test_next_dated_horse_example_separate(self):
  tail=D[-3:]
  self.assertTrue(all(r["chapter"]=="XCIV_NAVIGATION_ONLY" for r in tail))
  self.assertIn("three-day outcome",tail[-1]["historical_author_paraphrase"])
 def test_duplicate_mapping_mutant(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,s)
 def test_wrong_chapter_boundary_mutant(self):
  rows=copy.deepcopy(D);rows[-1]["chapter"]="XCIII"
  with self.assertRaises(AssertionError):check(rows,M)
 def test_invalid_empirical_prediction_mutant(self):
  rows=copy.deepcopy(D);rows[24]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(rows,M)
 def test_invalid_occult_diagnosis_mutant(self):
  rows=copy.deepcopy(D);rows[16]["independently_authenticated_occult_causation"]=True
  with self.assertRaises(AssertionError):check(rows,M)
if __name__=="__main__":unittest.main(verbosity=2)
