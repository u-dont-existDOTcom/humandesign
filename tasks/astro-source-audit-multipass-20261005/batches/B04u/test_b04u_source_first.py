import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=j("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=j("SOURCE_WINDOW_MANIFEST.json");V=j("WORKED_HOUR_REPLAY_VECTORS_20261017.json")
def check(rows,spans):
 assert len(rows)==114 and len(spans)==13
 assert [r["source_local_id"] for r in rows]==[f"XCVIII-C{k:03}" for k in range(1,115)]
 ids=[x for s in spans for x in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==114
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[x]["source_span_id"]==s["span_id"] and set(by[x]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"])) for s in spans for x in s["mapped_local_ids"])
 assert all(r["chapter"]=="XCVIII" for r in rows[:-5])
 assert all(r["chapter"]=="BOOK_III_NAVIGATION_ONLY" for r in rows[-5:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
   and not r["independently_validated_planetary_hour_effect"] and not r["empirically_validated_prediction"]
   and not r["runtime_model_promoted"] for r in rows)
def minute(t):
 a,b=map(int,t.split(":"))
 assert 0<=a<=24 and 0<=b<60 and (a!=24 or b==0)
 return a*60+b
class SourceFirst(unittest.TestCase):
 def test_original_passage_mapping(self):check(D,M)
 def test_source_witness_file_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],list(range(516,522)))
  for x in W["original_images"]:
   p=B/x["path"];data=p.read_bytes()
   self.assertEqual(len(data),x["bytes"])
   self.assertEqual(hashlib.sha256(data).hexdigest(),x["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"90c7e9d1fb07bebf45045a3b0aedb5064d5e246234f4959175e5623e18ade064")
 def test_correct_numbering_and_next_book(self):
  self.assertEqual(W["prior_accepted_lilly"],5639)
  self.assertEqual(W["editorial_chapter"],"XCVIII")
  self.assertEqual(W["source_final_printed_chapter"],"XCVII")
  self.assertEqual(W["following_book_title_pdf"],521)
  self.assertTrue(all(x["printed_pages"]==[None] for x in D[-5:]))
  self.assertFalse(W["previous_table_full_numeric_transcription_complete"])
 def test_precise_cross_page_records(self):
  spans=[s["original_pdf_pages"] for s in M if len(s["original_pdf_pages"])>1]
  self.assertEqual(spans,[[516,517],[517,518],[518,519],[519,520]])
  rows=[r["source_local_id"] for r in D if len(r["original_pdf_pages"])>1]
  self.assertEqual(rows,["XCVIII-C027","XCVIII-C045","XCVIII-C072","XCVIII-C101"])
 def test_source_hourly_cycle_and_weekday_list(self):
  s=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for term in ("sun, venus, mercury, moon, saturn, jupiter, mars",
   "sunrise to sunset","sunset to sunrise","aries or libra","monday",
   "plants","sigils","lilly","11 june"):
   self.assertIn(term,s,term)
 def test_three_independent_source_calculations(self):
  self.assertEqual(len(V["examples"]),3)
  cycle=V["hourly_planet_cycle"]
  monday=cycle.index(V["weekday_planet"])
  results=[]
  for e in V["examples"]:
   t=minute(e["target_local_hhmm"]);bound=[minute(e["starting_solar_boundary"])]+[minute(x) for x in e["column_end_hhmm"]]
   self.assertEqual(bound,sorted(bound))
   indices=[i for i in range(len(bound)-1) if bound[i]<=t<bound[i+1]]
   self.assertEqual(len(indices),1,e["id"])
   ordinal=e["hour_ordinals"][indices[0]]
   self.assertEqual(ordinal,e["expected_planetary_hour_ordinal"])
   planet=cycle[(monday+ordinal-1)%7]
   self.assertEqual(planet,e["expected_ruler"])
   results.append((ordinal,planet))
  self.assertEqual(results,[(4,"Mars"),(12,"Sun"),(18,"Mars")])
 def test_64_minute_example(self):
  self.assertEqual(minute("07:51")-minute("06:47"),64)
  self.assertEqual(120-64,56)
 def test_medical_claims_no_outcomes(self):
  body=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("medicine",body)
  self.assertIn("sigils",body)
  self.assertTrue(all(not r["independently_validated_planetary_hour_effect"] for r in D))
 def test_source_uncertainties_not_omitted(self):
  self.assertEqual(len(j("UNRESOLVED_SOURCE_LIMITS.json")["issues"]),30)
 def test_mutant_false_empirical_prediction_rejected(self):
  rows=copy.deepcopy(D);rows[47]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(rows,M)
 def test_mutant_next_book_contamination_rejected(self):
  rows=copy.deepcopy(D);rows[-1]["chapter"]="XCVIII"
  with self.assertRaises(AssertionError):check(rows,M)
 def test_mutant_duplicate_source_mapping_rejected(self):
  spans=copy.deepcopy(M);spans[0]["mapped_local_ids"].append(spans[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,spans)
if __name__=="__main__":unittest.main(verbosity=2)
