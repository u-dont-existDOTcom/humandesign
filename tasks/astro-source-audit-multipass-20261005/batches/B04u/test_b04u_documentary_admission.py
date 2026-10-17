import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=j("RULES.json")["rules"];A=j("ACCEPTANCE.json")
def valid(rr):
 assert len(rr)==114
 assert [r["record_number"] for r in rr]==list(range(5640,5754))
 assert [r["id"] for r in rr]==[f"R{k}" for k in range(5640,5754)]
 assert all(r["historical_documentary_accepted"] and not r["independently_validated_planetary_hour_effect"]
    and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rr)
 assert all(r["chapter"]=="XCVIII" for r in rr[:-5])
 assert all(r["chapter"]=="BOOK_III_NAVIGATION_ONLY" for r in rr[-5:])
class Admission(unittest.TestCase):
 def test_all_records_historical_not_empirical(self):valid(R)
 def test_draft_semantics_unchanged(self):
  for a,b in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter","original_pdf_pages",
     "short_original_anchor_not_diplomatic","historical_author_paraphrase",
     "original_source_qualifications"):self.assertEqual(a[k],b[k])
 def test_reverse_map_exact(self):
  m=j("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[i for s in m["source_spans"] for i in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(m["span_count"],13)
 def test_hashes_and_clock_vectors(self):
  for n,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("WORKED_HOUR_REPLAY_VECTORS_20261017.json","clock_vectors_sha256")):self.assertEqual(h(n),A[k])
 def test_total_and_new_book(self):
  self.assertEqual(A["prior_lilly_accepted"],5639)
  self.assertEqual(A["new_documentary_records"],114)
  self.assertEqual(A["lilly_if_published"],5753)
  self.assertEqual(A["combined_if_published"],6819)
  self.assertEqual(A["following_book_title_pdf"],521)
  self.assertTrue(A["signed_book_ii_conclusion_found"])
 def test_numeric_source_still_open(self):
  self.assertFalse(A["planetary_table_complete_numeric_transcription"])
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
  self.assertEqual(A["worked_clock_examples_arithmetically_replayed"],3)
 def test_mutant_claims_inbook_when_next(self):
  z=copy.deepcopy(R);z[-1]["chapter"]="XCVIII"
  with self.assertRaises(AssertionError):valid(z)
 def test_mutant_false_predictive_validation(self):
  z=copy.deepcopy(R);z[30]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(z)
if __name__=="__main__":unittest.main(verbosity=2)
