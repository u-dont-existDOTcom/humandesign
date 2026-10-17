import json,hashlib,copy,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=j("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=j("SOURCE_WINDOW_MANIFEST.json")
U=j("UNRESOLVED_SOURCE_LIMITS.json")
def valid(rows,spans):
 assert len(rows)==99 and len(spans)==13
 assert [r["source_local_id"] for r in rows]==[f"RECTIFY-C{i:03}" for i in range(1,100)]
 ids=[i for s in spans for i in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==99
 assert set(ids)=={r["source_local_id"] for r in rows}
 mapping={r["source_local_id"]:r for r in rows}
 assert all(mapping[k]["source_span_id"]==s["span_id"] and mapping[k]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for k in s["mapped_local_ids"])
 assert all(r["section"]=="TRUTINE_AND_OTHER_RECTIFICATION_METHODS" for r in rows[:-3])
 assert all(r["section"]=="NEXT_ANIMODAR_NAV_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and
  not r["independently_verified_conception_event"] and not r["independently_verified_natal_birth_time"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_bijective_image_source_records(self):valid(D,M)
 def test_original_full_page_hashes(self):
  self.assertEqual([w["original_pdf_page"] for w in W["original_images"]],list(range(534,540)))
  for w in W["original_images"]:
   data=(B/w["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(data).hexdigest(),w["sha256"])
   self.assertEqual(len(data),w["bytes"])
  self.assertEqual(W["original_images"][0]["sha256"],"a08044de064e653f3c24b4320ac183a4b93ad238b5c5cad62e668248ca8a689a")
 def test_index_boundary_and_next_Animodar(self):
  self.assertEqual(W["previous_accepted_lilly"],5824)
  self.assertEqual(W["next_global_record"],5825)
  self.assertEqual(W["next_heading_pdf"],539)
  self.assertEqual(W["next_printed_chapter"],"XCIX")
  self.assertEqual(W["next_editorial_chapter"],"C")
 def test_calendar_numeric_replay(self):
  self.assertEqual(1616%4,0)
  self.assertEqual(244+19,263)
  self.assertEqual(263+366-285,344)
  self.assertEqual(334+10,344)
  self.assertEqual(W["merchant_prenatal_gestation_days_source"],285)
  self.assertEqual(W["merchant_assumed_conception"],"10 December 1615")
 def test_trutine_sign_not_exact_degree(self):
  self.assertTrue(W["trutine_sign_help_reported_exact_degree_rare"])
  alltext=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("seldom fixed",alltext)
  self.assertIn("identifying which zodiac sign",alltext)
 def test_13_degree_threshold_and_discretionary_excuses(self):
  txt=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for phrase in ("13°","good planetary aspects","adverse aspects"):
   self.assertIn(phrase,txt)
 def test_source_negative_conception_hour_and_accidents(self):
  self.assertTrue(W["source_says_hour_of_conception_alternative_not_credited"])
  txt=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("does not credit it",txt)
  self.assertIn("accidents/life events",txt)
  self.assertIn("midheaven",txt)
 def test_undigitized_gestation_table_and_human_uncertainty(self):
  self.assertFalse(W["full_gestation_table_numeric_transcribed"])
  self.assertEqual(len(U["issues"]),27)
  self.assertTrue(all(not r["independently_verified_natal_birth_time"] for r in D))
 def test_next_chapter_separate(self):
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),3)
  self.assertTrue(all(r["section"]=="NEXT_ANIMODAR_NAV_ONLY" for r in D[-3:]))
 def test_mutant_doubled_span_detected(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,s)
 def test_mutant_false_birth_verified_detected(self):
  r=copy.deepcopy(D);r[75]["independently_verified_natal_birth_time"]=True
  with self.assertRaises(AssertionError):valid(r,M)
 def test_mutant_next_chapter_import_detected(self):
  r=copy.deepcopy(D);r[-1]["section"]="TRUTINE_AND_OTHER_RECTIFICATION_METHODS"
  with self.assertRaises(AssertionError):valid(r,M)
if __name__=="__main__":unittest.main(verbosity=2)
