import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(records,spans):
 assert len(records)==34 and len(spans)==5
 assert [r["source_local_id"] for r in records]==[f"ANIMODAR-C{i:03}" for i in range(1,35)]
 ids=[x for s in spans for x in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==34
 assert set(ids)=={r["source_local_id"] for r in records}
 indexed={r["source_local_id"]:r for r in records}
 assert all(indexed[x]["source_span_id"]==s["span_id"] and indexed[x]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for x in s["mapped_local_ids"])
 assert all(r["chapter"]=="C" for r in records[:-3])
 assert all(r["chapter"]=="CI_NAVIGATION_ONLY" for r in records[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
 and not r["independently_authenticated_birth_time"]
 and not r["independently_validated_Animodar_accuracy"]
 and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in records)
class Source(unittest.TestCase):
 def test_original_mapping_one_to_one(self):check(D,M)
 def test_original_page_images_hash_and_size(self):
  self.assertEqual([a["original_pdf_page"] for a in W["original_images"]],[539,540,541])
  for a in W["original_images"]:
   f=B/a["path"];raw=f.read_bytes()
   self.assertEqual(len(raw),a["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),a["sha256"])
 def test_prior_accepted_and_next_chapter(self):
  self.assertEqual(W["previous_lilly_accepted"],5923)
  self.assertEqual(W["next_global_record"],5924)
  self.assertEqual(W["following_heading_pdf"],541)
  self.assertEqual(W["printed_chapter"],"XCIX")
  self.assertEqual(W["editorial_chapter"],"C")
 def test_main_input_branches(self):
  s=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for q in ("new moon","full moon","above the earth","ascendant","midheaven","dignities"):
   self.assertIn(q,s,q)
 def test_dignity_tie_is_not_new_case(self):
  s=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("tie",s)
  self.assertIn("nearer the ascendant",s)
 def test_no_independent_success_in_sample(self):
  self.assertTrue(W["source_author_deems_Animodar_less_sure_than_accidents"])
  self.assertFalse(W["independent_birth_time_certificate"])
  self.assertTrue(W["no_externally_verified_natal_success"])
  self.assertEqual(len(U["issues"]),22)
 def test_three_next_chapter_navigation_only(self):
  self.assertTrue(all(r["role"]=="next_navigation" for r in D[-3:]))
  self.assertTrue(all(r["chapter"]=="CI_NAVIGATION_ONLY" for r in D[-3:]))
 def test_duplicate_span_mutant(self):
  z=copy.deepcopy(M);z[0]["mapped_local_ids"].append(z[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,z)
 def test_false_birth_accuracy_mutant(self):
  z=copy.deepcopy(D);z[18]["independently_validated_Animodar_accuracy"]=True
  with self.assertRaises(AssertionError):check(z,M)
 def test_next_chapter_leak_mutant(self):
  z=copy.deepcopy(D);z[-1]["chapter"]="C"
  with self.assertRaises(AssertionError):check(z,M)
if __name__=="__main__":unittest.main(verbosity=2)
