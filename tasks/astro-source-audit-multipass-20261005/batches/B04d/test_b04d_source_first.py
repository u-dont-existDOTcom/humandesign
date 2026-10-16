import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json");C=J("CLAIM_LEDGER.json")
def valid(rows,spans):
 assert len(rows)==79 and len(spans)==15
 assert [r["source_local_id"] for r in rows]==[f"LXXXIV-C{i:03}" for i in range(1,80)]
 a=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(a)==len(set(a))==79
 assert set(a)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="LXXXIV" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXV_NAVIGATION_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_vocational_outcome"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_no_duplicate_or_missing_original_annotations(self):valid(D,M)
 def test_original_page_witnesses_and_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[484,485,486])
  for item in W["original_images"]:
   raw=(B/item["path"]).read_bytes()
   self.assertEqual(len(raw),item["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),item["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"afc8bfcda5efe804a6544db2a2966e241ec8e938c89af82e4c67a7bfbacfe6cb")
 def test_printed_window_and_next_historical_case(self):
  self.assertEqual(W["previous_accepted_lilly"],4875)
  self.assertEqual(W["original_body_pdf_pages"],[484,485])
  self.assertEqual(W["next_numbered_chapter"],"LXXXV")
  self.assertEqual(W["following_heading_pdf"],486)
  self.assertEqual([r["role"] for r in D[-2:]],["next_navigation","next_navigation"])
 def test_mars_venus_visual_glyph_and_horary_substitution(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("mars and venus",text)
  self.assertIn("time the question is asked",text)
  self.assertIn("exact birth times",text)
  audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").read_text()
  self.assertIn("Mars (♂) and Venus (♀)",audit)
 def test_sign_catalogues_and_pisces_derogation(self):
  src=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for s in ("taurus","gemini","leo","virgo","libra","scorpio","sagittarius","capricorn","aquarius","pisces","cancer"):
   self.assertIn(s,src)
  self.assertEqual(len([r for r in D if r["role"]=="authorial_characterization"]),1)
  self.assertIn("derogatorily",src)
 def test_no_career_validation(self):
  self.assertEqual(len(U["issues"]),24)
  self.assertEqual(C["real_vocational_predictions_independently_validated"],0)
  self.assertEqual(C["runtime_promotions"],0)
 def test_mutant_double_mapped(self):
  changed=copy.deepcopy(M)
  changed[0]["mapped_local_ids"].append(changed[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,changed)
 def test_mutant_next_chapter_contamination(self):
  changed=copy.deepcopy(D);changed[-1]["chapter"]="LXXXIV"
  with self.assertRaises(AssertionError):valid(changed,M)
 def test_mutant_false_empirical_credit(self):
  changed=copy.deepcopy(D);changed[40]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(changed,M)
if __name__=="__main__":unittest.main(verbosity=2)
