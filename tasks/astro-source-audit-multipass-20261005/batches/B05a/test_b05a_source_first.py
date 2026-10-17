import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==29 and len(spans)==4
 assert [r["source_local_id"] for r in rows]==[f"NATAL-PREJUDGMENT-C{k:03}" for k in range(1,30)]
 ids=[x for s in spans for x in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==29 and set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[x]["source_span_id"]==s["span_id"] and by[x]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for x in s["mapped_local_ids"])
 assert all(r["chapter"]=="CIII" for r in rows[:-3])
 assert all(r["chapter"]=="CIV_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and
  not r["independently_verified_natal_outcome"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_original_to_source_rows_bijection(self):check(D,M)
 def test_original_image_sha256_and_sizes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[558,559])
  for x in W["original_images"]:
   raw=(B/x["path"]).read_bytes()
   self.assertEqual(len(raw),x["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_single_page_boundary_and_next_lifespan(self):
  self.assertTrue(W["original_chapter_only_one_page"])
  self.assertEqual(W["body_original_pdf_page"],558)
  self.assertEqual(W["next_original_pdf_page"],559)
  self.assertEqual(W["printed_chapter"],"CII")
  self.assertEqual(W["next_printed_chapter"],"CIII")
 def test_source_prerequisite_and_unquantified_orbs(self):
  self.assertTrue(W["source_accident_based_method_favored"])
  self.assertFalse(W["source_antiscia_numeric_orb_stated"])
  self.assertFalse(W["source_fixed_stars_small_latitude_numeric_threshold_stated"])
  q=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for p in ("part of fortune","antiscia","first or second magnitude","marriage","travel","corrected","significator"):
   self.assertIn(p,q)
 def test_no_derived_long_life_claim_merged(self):
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),3)
  self.assertEqual(len([r for r in D if r["role"]=="outcome_class"]),5)
  self.assertEqual(len(U["issues"]),17)
 def test_previous_accepted_history(self):
  self.assertEqual(W["previous_accepted_lilly"],6215)
  self.assertEqual(W["next_global_record"],6216)
  self.assertEqual(W["independent_predicted_person_cases"],0)
  self.assertEqual(W["runtime_promotions"],0)
 def test_double_source_id_mutant(self):
  p=copy.deepcopy(M);p[0]["mapped_local_ids"].append(p[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,p)
 def test_false_outcome_mutant(self):
  p=copy.deepcopy(D);p[12]["independently_verified_natal_outcome"]=True
  with self.assertRaises(AssertionError):check(p,M)
 def test_next_chapter_intrusion_mutant(self):
  p=copy.deepcopy(D);p[-1]["chapter"]="CIII"
  with self.assertRaises(AssertionError):check(p,M)
if __name__=="__main__":unittest.main(verbosity=2)
