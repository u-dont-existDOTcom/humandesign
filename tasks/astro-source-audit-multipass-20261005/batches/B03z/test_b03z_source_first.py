import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json");O=J("SOURCE_ORDER_DRAFT.json")
def valid(rows,spans):
 assert len(rows)==82 and len(spans)==13
 assert [r["source_local_id"] for r in rows]==[f"LXXX-C{i:03}" for i in range(1,83)]
 mapping=[v for s in spans for v in s["mapped_local_ids"]]
 assert len(mapping)==len(set(mapping))==82
 assert set(mapping)=={r["source_local_id"] for r in rows}
 byid={r["source_local_id"]:r for r in rows}
 assert all(set(byid[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
            and byid[k]["source_span_id"]==s["span_id"]
            for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="LXXX" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXI_NAVIGATION_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
            and not r["independently_authenticated_religious_political_outcome"]
            and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class SourceFirst(unittest.TestCase):
 def test_all_original_ids_map_once(self):
  valid(D["rows"],M["source_spans"])
  self.assertEqual(O["ordered_ids"],[r["source_local_id"] for r in D["rows"]])
 def test_exact_source_image_hashes(self):
  self.assertEqual([i["original_pdf_page"] for i in W["original_images"]],[473,474,475,476])
  for i in W["original_images"]:
   p=B/i["path"]
   self.assertEqual(p.stat().st_size,i["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),i["sha256"])
 def test_admitted_parent_identity_and_next_chapter(self):
  self.assertEqual(W["previous_accepted_lilly"],4549)
  self.assertEqual(W["next_global_record"],4550)
  self.assertEqual(W["next_numbered_chapter"],"LXXXI")
  self.assertEqual(W["following_heading_pdf"],476)
  self.assertEqual(W["original_body_pdf_pages"],[473,474,475,476])
 def test_original_page_seams_preserved(self):
  self.assertEqual([s["original_pdf_pages"] for s in M["source_spans"] if len(s["original_pdf_pages"])>1],[[473,474],[475,476]])
  self.assertEqual(len(O["next_heading_navigation_only"]),2)
 def test_conjectural_and_qualified_outcome_not_disappeared(self):
  text=" ".join(r["historical_author_paraphrase"]+" "+r["original_source_qualifications"] for r in D["rows"]).lower()
  for term in ("conjectural","three years","current form","amend","moderate","alternat"):
   self.assertIn(term,text,term)
 def test_timing_and_separate_figure(self):
  self.assertIn("1646",D["rows"][1]["historical_author_paraphrase"])
  self.assertIn("1647",D["rows"][-1]["historical_author_paraphrase"])
  self.assertEqual([r["role"] for r in D["rows"][-2:]],["next_navigation","next_navigation"])
 def test_planet_aspect_sequence(self):
  roles=[r["historical_author_paraphrase"].lower() for r in D["rows"]]
  order=[next(i for i,s in enumerate(roles) if phrase in s) for phrase in
         ("separates from venus","void of course","square mars","squares jupiter")]
  self.assertEqual(order,sorted(order))
 def test_distinct_opposition_and_partial_reform_branches(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  for key in ("younger members","older clergy","soldiers","financial contributions",
              "primitive","moderate","not to continue unchanged"):
   self.assertIn(key,text,key)
 def test_source_not_empirical(self):
  self.assertEqual(C["historically_independently_verified_outcomes"],0)
  self.assertEqual(C["independently_validated_predictive_results"],0)
  self.assertEqual(C["runtime_model_promotions"],0)
  self.assertEqual(len(U["issues"]),24)
 def test_duplicate_record_mutant_detected(self):
  changed=copy.deepcopy(M["source_spans"])
  changed[0]["mapped_local_ids"].append(changed[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D["rows"],changed)
 def test_chapter_leak_mutant_detected(self):
  changed=copy.deepcopy(D["rows"]);changed[-1]["chapter"]="LXXX"
  with self.assertRaises(AssertionError):valid(changed,M["source_spans"])
 def test_false_predictive_credit_mutant_detected(self):
  changed=copy.deepcopy(D["rows"]);changed[35]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(changed,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
