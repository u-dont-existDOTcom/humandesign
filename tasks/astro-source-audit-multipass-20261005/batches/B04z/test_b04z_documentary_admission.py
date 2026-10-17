import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(rows):
 assert len(rows)==70
 assert [r["record_number"] for r in rows]==list(range(6146,6216))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(6146,6216)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_verified_natal_birth_instant"] and
  not r["full_source_numeric_tables_independently_parity_checked"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="CII" for r in rows[:-3])
 assert all(r["chapter"]=="CIII_NAVIGATION_ONLY" for r in rows[-3:])
class Admission(unittest.TestCase):
 def test_all_contiguous_global_ordinals(self):check(R)
 def test_first_edition_claims_not_modified(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","printed_chapter","role",
    "original_pdf_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_reverse_map_onto_accepted_rules(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],6)
 def test_exact_sha_inputs(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_NUMERIC_ARITHMETIC_AUDIT_20261017.json","arithmetic_audit_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_counts_next_and_arithmetic_disposition(self):
  self.assertEqual(A["previous_lilly"],6145)
  self.assertEqual(A["added_historical_records"],70)
  self.assertEqual(A["lilly_if_published"],6215)
  self.assertEqual(A["combined_if_published"],7281)
  self.assertEqual(A["next_original_pdf_page"],558)
  self.assertEqual(A["printed_vs_interpolated_ascendant_discrepancy_minutes_approximately"],3)
 def test_no_predicted_observed_people(self):
  self.assertEqual(A["independent_natal_birth_time_verified"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
  self.assertFalse(A["remote_published"])
 def test_false_chart_parity_mutant(self):
  b=copy.deepcopy(R);b[37]["full_source_numeric_tables_independently_parity_checked"]=True
  with self.assertRaises(AssertionError):check(b)
 def test_next_chapter_contamination_mutant(self):
  b=copy.deepcopy(R);b[-1]["chapter"]="CII"
  with self.assertRaises(AssertionError):check(b)
if __name__=="__main__":unittest.main(verbosity=2)
