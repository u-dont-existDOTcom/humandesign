import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];R=j("RULES.json")["rules"];A=j("ACCEPTANCE.json")
def valid(rr):
 assert len(rr)==10
 assert [x["record_number"] for x in rr]==list(range(5630,5640))
 assert all(x["historical_documentary_accepted"] and not x["source_numeric_cells_fully_transcribed"]
    and not x["empirically_validated_prediction"] and not x["runtime_model_promoted"] for x in rr)
class Admission(unittest.TestCase):
 def test_all_records_source_only(self):valid(R)
 def test_unchanged_source_and_cardinality(self):
  for x,y in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","original_pdf_pages","kind","historical_author_paraphrase"):self.assertEqual(x[k],y[k])
 def test_reverse_map_exact(self):
  z=j("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[x for group in z["source_spans"] for x in group["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
 def test_input_hashes(self):
  for f,key in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
                ("UNRESOLVED.json","unresolved_sha256"),
                ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
                ("TABLE_PAGE_SOURCE_SCHEMA_20261017.json","table_schema_sha256")):
   self.assertEqual(h(f),A[key])
 def test_next_printed_chapter(self):
  self.assertEqual(A["lilly_if_published"],5639)
  self.assertEqual(A["combined_if_published"],6705)
  self.assertEqual(A["next_printed_chapter"],"XCVII")
  self.assertEqual(A["next_original_pdf"],516)
 def test_digitization_remains_open(self):
  self.assertFalse(A["numeric_cell_transcription_complete"])
  self.assertTrue(A["next_numeric_transcription_still_open"])
  self.assertEqual(A["independent_empirical_validations"],0)
 def test_false_finished_digitization_mutant(self):
  z=copy.deepcopy(R);z[0]["source_numeric_cells_fully_transcribed"]=True
  with self.assertRaises(AssertionError):valid(z)
if __name__=="__main__":unittest.main(verbosity=2)
