import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json")
def valid(rows,spans):
 assert len(rows)==57 and len(spans)==11
 assert [r["source_local_id"] for r in rows]==[f"LXXXI-C{i:03}" for i in range(1,58)]
 ids=[i for s in spans for i in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==57
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[i]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for i in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="LXXXI" for r in rows[:-3])
 assert all(r["chapter"]=="LXXXII_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
            and not r["independently_authenticated_philosophers_stone_case"]
            and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class SourceFirst(unittest.TestCase):
 def test_one_to_one_span_mapping(self):valid(D["rows"],M["source_spans"])
 def test_original_1647_witness_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[476,477,478])
  for x in W["original_images"]:
   p=B/x["path"];self.assertEqual(p.stat().st_size,x["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x["sha256"])
 def test_source_window_and_authored_date(self):
  self.assertEqual(W["previous_accepted_lilly"],4631)
  self.assertEqual(W["first_proposed_record"],4632)
  self.assertEqual(W["following_chapter"],"LXXXII")
  self.assertEqual(W["next_heading_pdf"],478)
  self.assertIn("1647",W["source_figure_timestamp"])
  self.assertEqual(W["original_body_pdf_pages"],[476,477,478])
 def test_original_versus_following_section(self):
  self.assertEqual(len([r for r in D["rows"] if r["role"]=="next_navigation"]),3)
  self.assertEqual([s["original_pdf_pages"] for s in M["source_spans"] if len(s["original_pdf_pages"])>1],[[476,477],[477,478]])
 def test_belief_not_observed_stone(self):
  self.assertEqual(C["authorial_beliefs_about_elixir"],5)
  self.assertEqual(C["independently_proven_philosophers_stones"],0)
  self.assertEqual(C["new_empirical_predictive_validations"],0)
 def test_alchemy_warning_and_health_different_claims(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  for name in ("angels","enough knowledge","mars","mercury","earlier search",
               "consumption","sixth","twelfth"):
   self.assertIn(name,text,name)
  self.assertEqual(len([r for r in D["rows"] if r["role"]=="authorial_health_allegation"]),1)
 def test_preserve_event_phases(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D["rows"])
  for s in ("retrograde","moving direct","another square","gemini"):
   self.assertIn(s,text,s)
 def test_20_explicit_qualifications(self):
  self.assertEqual(len(U["issues"]),20)
  self.assertEqual(C["independently_authenticated_consumption_diagnoses"],0)
  self.assertEqual(C["runtime_promotions"],0)
 def test_double_count_mutant(self):
  m=copy.deepcopy(M["source_spans"])
  m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D["rows"],m)
 def test_next_house_leak_mutant(self):
  rs=copy.deepcopy(D["rows"]);rs[-1]["chapter"]="LXXXI"
  with self.assertRaises(AssertionError):valid(rs,M["source_spans"])
 def test_false_prediction_mutant(self):
  rs=copy.deepcopy(D["rows"]);rs[20]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(rs,M["source_spans"])
if __name__=="__main__":unittest.main(verbosity=2)
