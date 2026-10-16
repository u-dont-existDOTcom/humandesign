import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json")
def valid(rows,spans):
 assert len(rows)==46 and len(spans)==8
 assert [r["source_local_id"] for r in rows]==[f"LXXXIII-C{i:03}" for i in range(1,47)]
 ids=[i for s in spans for i in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==46
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for k in s["mapped_local_ids"])
 assert all(r["printed_pages"]==[v-34 for v in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="LXXXIII" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXIV_NAVIGATION_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_restoration_outcome"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_bijection_and_original_order(self):valid(D,M)
 def test_sha256_of_original_scan_pages(self):
  self.assertEqual([r["original_pdf_page"] for r in W["original_images"]],[482,483,484])
  for item in W["original_images"]:
   raw=(B/item["path"]).read_bytes()
   self.assertEqual(len(raw),item["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),item["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"f59597c9313d60ebdfd0e24629b551f47153c4854778f23ad3254f80e7050921")
 def test_previous_publication_checkpoint_and_new_divider(self):
  self.assertEqual(W["previous_accepted_lilly"],4829)
  self.assertEqual(W["next_numbered_chapter"],"LXXXIV")
  self.assertEqual(W["following_heading_pdf"],484)
  self.assertEqual([s["original_pdf_pages"] for s in M if len(s["original_pdf_pages"])>1],[[482,483]])
 def test_outcome_distinctions(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for term in ("restoration","sovereignty somewhere else","another country","negative prediction","former position","accelerate return"):
   self.assertIn(term,text,term)
 def test_explicit_negative_and_fortunate_exception(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("benefic planet is an exception",text)
  self.assertIn("negative prediction",text)
  self.assertIn("nonreturn",text)
 def test_four_mutable_and_eight_restoration_signs(self):
  entries=[r["historical_author_paraphrase"] for r in D]
  self.assertTrue(any("Eight specified zodiac signs" in x for x in entries))
  self.assertTrue(any("four mutable signs" in x.lower() for x in entries))
 def test_issues_and_science_separate(self):
  self.assertEqual(len(U["issues"]),17)
  self.assertEqual(C["independently_verified_restoration_outcomes"],0)
  self.assertEqual(C["empirically_validated_predictions"],0)
  self.assertEqual(C["runtime_promotions"],0)
 def test_mutant_duplicate_source_rejected(self):
  m=copy.deepcopy(M);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,m)
 def test_mutant_next_heading_leak_rejected(self):
  d=copy.deepcopy(D);d[-1]["chapter"]="LXXXIII"
  with self.assertRaises(AssertionError):valid(d,M)
 def test_mutant_false_validation_rejected(self):
  d=copy.deepcopy(D);d[20]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(d,M)
if __name__=="__main__":unittest.main(verbosity=2)
