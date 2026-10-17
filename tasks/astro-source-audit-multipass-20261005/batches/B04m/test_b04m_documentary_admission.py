import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
U=J("UNRESOLVED.json")
def check(rs):
 assert len(rs)==75
 assert [r["record_number"] for r in rs]==list(range(5339,5414))
 assert [r["id"] for r in rs]==[f"R{i}" for i in range(5339,5414)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_authenticated_occult_causation"] and
  not r["independently_authenticated_treatment_success"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="XCIII" for r in rs[:-3])
 assert all(r["chapter"]=="XCIV_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_record_ordinals_and_no_promotion(self):check(R)
 def test_source_first_fields_preserved(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter","original_pdf_pages",
    "printed_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k],k)
   self.assertIsNone(d["global_record_number"])
 def test_exact_reverse_page_coverage(self):
  ids=[k for s in M["source_spans"] for k in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(len(ids),75)
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],11)
 def test_admission_input_hashes(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_documentary_counts_and_chapter_scope(self):
  self.assertEqual(A["prior_lilly_accepted"],5338)
  self.assertEqual(A["new_documentary_records"],75)
  self.assertEqual(A["lilly_if_published"],5413)
  self.assertEqual(A["combined_if_published"],6479)
  self.assertEqual(A["next_chapter"],"XCIV")
  self.assertEqual(A["next_printed_chapter"],"XCIII")
  self.assertEqual(A["following_heading_pdf"],501)
  self.assertEqual(len(U["issues"]),28)
  self.assertFalse(A["remote_canonical_published"])
 def test_supernatural_treatment_claims_unverified(self):
  self.assertEqual(A["independent_occult_causes_verified"],0)
  self.assertEqual(A["independent_diagnoses"],0)
  self.assertEqual(A["independent_remedy_successes"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_model_promotions"],0)
  self.assertEqual(len([r for r in R if r["role"]=="authorial_outcome_claim"]),1)
 def test_mutant_unsupported_causation(self):
  changed=copy.deepcopy(R);changed[45]["independently_authenticated_occult_causation"]=True
  with self.assertRaises(AssertionError):check(changed)
 def test_mutant_unsupported_treatment(self):
  changed=copy.deepcopy(R);changed[60]["independently_authenticated_treatment_success"]=True
  with self.assertRaises(AssertionError):check(changed)
 def test_mutant_following_chapter_leak(self):
  changed=copy.deepcopy(R);changed[-1]["chapter"]="XCIII"
  with self.assertRaises(AssertionError):check(changed)
if __name__=="__main__":unittest.main(verbosity=2)
