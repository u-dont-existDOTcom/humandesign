import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_PROVISIONAL_20261017.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==42 and len(spans)==7
 assert [r["source_local_id"] for r in rows]==[f"XCVI-C{i:03}" for i in range(1,43)]
 mapped=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(mapped)==len(set(mapped))==42
 assert set(mapped)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["source_span_id"]==s["span_id"] and
   set(by[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
   for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[n-34 for n in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="XCVI" for r in rows[:-3])
 assert all(r["chapter"]=="XCVII_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
   and not r["independently_verified_escaped_prisoner_identity"]
   and not r["independently_authenticated_fugitive_recapture"]
   and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class SourceFirst(unittest.TestCase):
 def test_full_bijection_and_no_unsupported_validation(self):check(D,M)
 def test_original_images_per_file_exact_hash(self):
  self.assertEqual([i["original_pdf_page"] for i in W["original_images"]],[504,505])
  for i in W["original_images"]:
   raw=(B/i["path"]).read_bytes()
   self.assertEqual(len(raw),i["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),i["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"1d5bf971c464f834e356589e5099519ff10e5da12fb513c5d1b6cd5b2a323dfc")
 def test_accepted_baseline_and_separate_next_chapter(self):
  self.assertEqual(W["parent_accepted_lilly"],5510)
  self.assertEqual(W["next_global_record_number"],5511)
  self.assertEqual(W["chapter_editorial"],"XCVI")
  self.assertEqual(W["chapter_printed"],"XCV")
  self.assertEqual(W["following_heading_pdf"],505)
  self.assertEqual(W["following_heading_printed"],"XCVI")
  self.assertTrue(W["next_chapter_has_distinct_horary_figure"])
 def test_page_seam_precise_provenance(self):
  self.assertEqual([s["original_pdf_pages"] for s in M if len(s["original_pdf_pages"])>1],[[504,505]])
  self.assertEqual([(r["source_local_id"],r["original_pdf_pages"]) for r in D if len(r["original_pdf_pages"])>1],[("XCVI-C032",[504,505])])
 def test_direction_night_hide_and_recapture_separate(self):
  s=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for term in ("eastern","one night","recaptured","official or authority","letter","six or seven days"):
   self.assertIn(term,s,term)
 def test_historical_outcomes_nonindependent(self):
  self.assertEqual(len([r for r in D if r["role"]=="authorial_outcome_claim"]),5)
  self.assertTrue(any("letter" in r["historical_author_paraphrase"] for r in D))
  self.assertTrue(any("following sunday" in r["historical_author_paraphrase"].lower() for r in D))
  self.assertTrue(all(not r["empirically_validated_prediction"] for r in D))
  self.assertEqual(len(U["issues"]),20)
 def test_mutant_false_recapture_verification_rejected(self):
  d=copy.deepcopy(D);d[36]["independently_authenticated_fugitive_recapture"]=True
  with self.assertRaises(AssertionError):check(d,M)
 def test_mutant_duplicate_passage_rejected(self):
  m=copy.deepcopy(M);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,m)
 def test_mutant_next_chapter_leak_rejected(self):
  d=copy.deepcopy(D);d[-1]["chapter"]="XCVI"
  with self.assertRaises(AssertionError):check(d,M)
 def test_mutant_false_predictive_credit_rejected(self):
  d=copy.deepcopy(D);d[22]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(d,M)
if __name__=="__main__":unittest.main(verbosity=2)
