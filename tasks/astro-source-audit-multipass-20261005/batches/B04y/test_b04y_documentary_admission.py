import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def valid(rs):
 assert len(rs)==188
 assert [r["record_number"] for r in rs]==list(range(5958,6146))
 assert [r["id"] for r in rs]==[f"R{i}" for i in range(5958,6146)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_authenticated_merchant_life_event"] and
  not r["independently_validated_birth_time_rectification"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="CI" for r in rs[:-3])
 assert all(r["chapter"]=="CII_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_global_records(self):valid(R)
 def test_no_edit_to_original_first_source(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter","printed_chapter",
      "original_pdf_pages","short_original_anchor_not_diplomatic",
      "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_reverse_bijection(self):
  ids=[q for s in M["source_spans"] for q in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],13)
 def test_exact_sha256_input_tracking(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_unfavorable_source_discrepancies_retained(self):
  self.assertTrue(A["source_fever_timing_mismatch_unresolved"])
  self.assertEqual(A["source_original_reported_fever"],"20y10m")
  self.assertEqual(A["source_directed_fever_fit"],"19y10m10d")
  self.assertEqual(A["source_biquintile_page546_misprint"],"105deg44")
  self.assertEqual(A["arithmetic_biquintile_correct"],"205deg44")
 def test_prior_and_next_chapter_counts(self):
  self.assertEqual(A["prior_lilly_accepted"],5957)
  self.assertEqual(A["new_documentary_records"],188)
  self.assertEqual(A["lilly_if_published"],6145)
  self.assertEqual(A["combined_if_published"],7211)
  self.assertEqual(A["next_heading_pdf"],553)
  self.assertEqual(A["following_printed_chapter"],"CI")
 def test_author_speculum_not_fully_digitized(self):
  self.assertFalse(A["source_speculum_full_numeric_data_complete"])
  self.assertTrue(A["event_fitting_in_sample_only"])
  self.assertEqual(A["independent_birth_times_verified"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertFalse(A["remote_published"])
 def test_mutant_nonexistent_birth_record(self):
  x=copy.deepcopy(R);x[163]["independently_validated_birth_time_rectification"]=True
  with self.assertRaises(AssertionError):valid(x)
 def test_mutant_false_human_events(self):
  x=copy.deepcopy(R);x[120]["independently_authenticated_merchant_life_event"]=True
  with self.assertRaises(AssertionError):valid(x)
 def test_mutant_next_chapter_intrusion(self):
  x=copy.deepcopy(R);x[-1]["chapter"]="CI"
  with self.assertRaises(AssertionError):valid(x)
if __name__=="__main__":unittest.main(verbosity=2)
