import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==44 and len(spans)==7
 assert [r["source_local_id"] for r in rows]==[f"XCIV-C{i:03}" for i in range(1,45)]
 local=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(local)==len(set(local))==44
 assert set(local)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["source_span_id"]==s["span_id"] and
            set(by[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
            for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="XCIV" for r in rows[:-2])
 assert all(r["chapter"]=="XCV_NAVIGATION_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_horse_recovery"]
  and not r["independently_authenticated_theft_or_riders"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_complete_original_passages(self):check(D,M)
 def test_original_scanned_page_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[501,502])
  for x in W["original_images"]:
   p=B/x["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),x["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"feb88477f7a59cc51abf99601cb8833af70d8913577f7cd152125ac2dc381984")
 def test_printed_separate_dated_chart_and_index(self):
  self.assertEqual(W["previous_accepted_lilly"],5413)
  self.assertEqual(W["next_global_record"],5414)
  self.assertEqual(W["printed_chapter"],"XCIII")
  self.assertEqual(W["editorial_chapter"],"XCIV")
  self.assertEqual(W["following_heading_pdf"],502)
  self.assertEqual(W["next_printed_chapter"],"XCIV")
 def test_original_vs_reported_timing_and_date_uncertainty(self):
  text=" ".join((r["historical_author_paraphrase"]+" "+r["original_source_qualifications"]).lower() for r in D)
  for phrase in ("one or two days","after three days","one day earlier",
    "january 13 or 14","two or three days"):
   self.assertIn(phrase,text,phrase)
  self.assertTrue(W["author_original_one_two_day_forecast"])
  self.assertTrue(W["author_reported_three_days"])
  self.assertTrue(W["reported_exact_return_day_ambiguous"])
 def test_west_prediction_vs_northeast_conflict(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("horse went toward the west",text)
  self.assertIn("northeast",text)
  self.assertIn("no independent tracking", " ".join(r["original_source_qualifications"].lower() for r in D))
 def test_qualified_author_outcome_and_riders(self):
  self.assertTrue(any(r["role"]=="authorial_discrepancy" for r in D))
  self.assertTrue(any("rode the horse" in r["historical_author_paraphrase"].lower() for r in D))
  self.assertTrue(all(not r["independently_authenticated_theft_or_riders"] for r in D))
  self.assertEqual(len(U["issues"]),20)
 def test_cross_page_seam_and_next_case(self):
  self.assertEqual([s["original_pdf_pages"] for s in M if len(s["original_pdf_pages"])>1],[[501,502]])
  self.assertEqual(len([r for r in D if len(r["original_pdf_pages"])>1]),1)
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),2)
 def test_duplicate_span_mutant_rejected(self):
  spans=copy.deepcopy(M);spans[0]["mapped_local_ids"].append(spans[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,spans)
 def test_false_empirical_success_mutant_rejected(self):
  rows=copy.deepcopy(D);rows[24]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(rows,M)
 def test_next_case_intrusion_mutant_rejected(self):
  rows=copy.deepcopy(D);rows[-1]["chapter"]="XCIV"
  with self.assertRaises(AssertionError):check(rows,M)
if __name__=="__main__":unittest.main(verbosity=2)
