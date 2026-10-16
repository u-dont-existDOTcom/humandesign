import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json");O=J("SOURCE_ORDER_DRAFT.json")
def valid(rows,spans):
 assert len(rows)==141 and len(spans)==21
 assert [r["source_local_id"] for r in rows]==[f"LXXXII-C{i:03}" for i in range(1,142)]
 ids=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==141
 assert set(ids)=={r["source_local_id"] for r in rows}
 byid={r["source_local_id"]:r for r in rows}
 assert all(byid[k]["original_pdf_pages"]==s["original_pdf_pages"]
            and byid[k]["source_span_id"]==s["span_id"]
            for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="LXXXII" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXIII_NAVIGATION_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None
            and not r["historical_documentary_accepted"]
            and not r["independently_authenticated_office_outcome"]
            and not r["empirically_validated_prediction"]
            and not r["runtime_model_promoted"] for r in rows)
class OriginalSource(unittest.TestCase):
 def test_ids_mapping_and_source_immobility(self):
  valid(D["rows"],M["source_spans"])
  self.assertEqual(O["ordered_ids"],[r["source_local_id"] for r in D["rows"]])
 def test_exact_original_image_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[478,479,480,481,482])
  for x in W["original_images"]:
   p=B/x["path"]
   self.assertEqual(p.stat().st_size,x["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"b4cf1de8927a09a87b88368825174de28d4984b586215ec8e770a8fd76c5f714")
 def test_previous_accepted_index_and_next_boundary(self):
  self.assertEqual(W["previous_accepted_lilly"],4688)
  self.assertEqual(W["first_proposed_record"],4689)
  self.assertEqual(W["next_numbered_chapter"],"LXXXIII")
  self.assertEqual(W["following_heading_pdf"],482)
 def test_two_original_page_seams(self):
  self.assertEqual([s["original_pdf_pages"] for s in M["source_spans"] if len(s["original_pdf_pages"])>1],[[478,479],[480,481]])
  self.assertEqual(O["following_heading_only"],[r["source_local_id"] for r in D["rows"][-2:]])
 def test_separate_office_acquisition_and_retention(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  for term in ("applicant","desired place","current post","temporary","restoration","transfer","removal","fourth"):
   self.assertIn(term,text,term)
  self.assertTrue(C["separate_new_office_and_existing_office_endpoints"])
 def test_no_false_victory_from_materials(self):
  self.assertEqual(C["independently_verified_employment_outcomes"],0)
  self.assertEqual(C["new_empirically_validated_predictions"],0)
  self.assertEqual(C["runtime_promotions"],0)
  self.assertEqual(len(U["issues"]),26)
 def test_source_favorable_and_malefic_exceptions(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  for term in ("benefic","malefic","reception","without reception","combustion","sign boundary","opposition"):
   self.assertIn(term,text)
 def test_social_conflict_mitigated_without_success(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  self.assertIn("not become angry",text)
  self.assertIn("hoped-for office is not achieved",text)
 def test_under_earth_return_vs_nonreturn(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  self.assertIn("temporary departure",text)
  self.assertIn("nonreturn",text)
 def test_duplicate_source_map_mutant(self):
  changed=copy.deepcopy(M["source_spans"])
  changed[0]["mapped_local_ids"].append(changed[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D["rows"],changed)
 def test_next_chapter_leak_mutant(self):
  changed=copy.deepcopy(D["rows"]);changed[-1]["chapter"]="LXXXII"
  with self.assertRaises(AssertionError):valid(changed,M["source_spans"])
 def test_false_predictive_credit_mutant(self):
  changed=copy.deepcopy(D["rows"]);changed[75]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(changed,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
