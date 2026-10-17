import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=j("RULES.json")["rules"];A=j("ACCEPTANCE.json")
def valid(rr):
 assert len(rr)==71
 assert [x["record_number"] for x in rr]==list(range(5754,5825))
 assert [x["id"] for x in rr]==[f"R{k}" for k in range(5754,5825)]
 assert all(x["historical_documentary_accepted"] and
  x["global_record_number"]==x["record_number"] and
  not x["full_reference_tables_numeric_cells_transcribed"] and
  not x["independently_validated_birth_time_rectification"] and
  not x["empirically_validated_prediction"] and not x["runtime_model_promoted"] for x in rr)
 assert all(x["section"]=="BOOK_III_INTRO_AND_TABLES" for x in rr[:-3])
 assert all(x["section"]=="NEXT_RECTIFICATION_CHAPTER_NAVIGATION" for x in rr[-3:])
class Admission(unittest.TestCase):
 def test_all_historical_records_only(self):valid(R)
 def test_original_claims_unchanged(self):
  for a,b in zip(D,R,strict=True):
   for f in ("source_local_id","source_span_id","section","original_pdf_pages","printed_pages",
    "short_original_anchor_not_diplomatic","historical_author_paraphrase","original_source_qualifications"):self.assertEqual(a[f],b[f])
   self.assertIsNone(a["global_record_number"])
 def test_reverse_map_bijection(self):
  m=j("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[q for s in m["source_spans"] for q in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
 def test_exact_rule_hashes(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):self.assertEqual(h(f),A[k])
 def test_published_totals_if_authenticated(self):
  self.assertEqual(A["prior_lilly"],5753)
  self.assertEqual(A["lilly_if_published"],5824)
  self.assertEqual(A["combined_if_published"],6890)
  self.assertEqual(A["next_editorial_chapter"],"XCIX")
  self.assertEqual(A["next_original_pdf_page"],534)
 def test_two_degree_discrepancy_still_open(self):
  self.assertEqual(A["original_arithmetic_discrepancy_arcminutes"],120)
  self.assertEqual(A["original_printed_ascendant_lookup"],"230deg20min")
  self.assertEqual(A["mathematically_correct_summation"],"232deg20min")
  self.assertFalse(A["full_numeric_table_transcription_complete"])
  self.assertEqual(A["independent_rectified_birth_times_verified"],0)
 def test_mutant_false_human_validation(self):
  x=copy.deepcopy(R);x[35]["independently_validated_birth_time_rectification"]=True
  with self.assertRaises(AssertionError):valid(x)
 def test_mutant_next_chapter_contamination(self):
  x=copy.deepcopy(R);x[-1]["section"]="BOOK_III_INTRO_AND_TABLES"
  with self.assertRaises(AssertionError):valid(x)
if __name__=="__main__":unittest.main(verbosity=2)
