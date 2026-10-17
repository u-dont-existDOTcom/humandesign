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
 assert len(rows)==65
 assert [r["record_number"] for r in rows]==list(range(6245,6310))
 assert [r["id"] for r in rows]==[f"R{n}" for n in range(6245,6310)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_authenticated_infant_survival_outcome"] and
  not r["medical_survival_predictive_validity"] and
  not r["empirically_validated_prediction"] and
  not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="CIV" for r in rows[:-3])
 assert all(r["chapter"]=="CV_NAVIGATION_ONLY" for r in rows[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_historical_records_only(self):check(R)
 def test_source_first_details_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","printed_chapter","role",
    "original_pdf_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_exact_record_reverse_bijection(self):
  ids=[q for s in M["source_spans"] for q in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],6)
 def test_file_sha256_provenance(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_counts_and_next_separate_chapter(self):
  self.assertEqual(A["previous_lilly"],6244)
  self.assertEqual(A["new_historical_documentary_records"],65)
  self.assertEqual(A["lilly_if_published"],6309)
  self.assertEqual(A["combined_if_published"],7375)
  self.assertEqual(A["next_heading_pdf_page"],561)
  self.assertEqual(A["next_printed_chapter"],"CIV")
 def test_no_mortality_medical_predictive_credit(self):
  self.assertTrue(A["source_asserted_survival_predictions_unvalidated"])
  self.assertEqual(A["actual_independently_verified_infant_survival_records"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
  self.assertFalse(A["remote_published"])
 def test_false_medical_validity_mutant(self):
  b=copy.deepcopy(R);b[20]["medical_survival_predictive_validity"]=True
  with self.assertRaises(AssertionError):check(b)
 def test_next_hyleg_chapter_contamination(self):
  b=copy.deepcopy(R);b[-1]["chapter"]="CIV"
  with self.assertRaises(AssertionError):check(b)
if __name__=="__main__":unittest.main(verbosity=2)
