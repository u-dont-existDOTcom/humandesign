import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json");U=J("UNRESOLVED.json")
def check(rs):
 assert len(rs)==53
 assert [r["record_number"] for r in rs]==list(range(5458,5511))
 assert [r["id"] for r in rs]==[f"R{i}" for i in range(5458,5511)]
 assert all(r["historical_documentary_accepted"]
  and r["global_record_number"]==r["record_number"]
  and not r["independently_authenticated_occult_cause"]
  and not r["independently_authenticated_medical_diagnosis"]
  and not r["independently_verified_medical_recovery"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="XCV" for r in rs[:-3])
 assert all(r["chapter"]=="XCVI_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_all_contiguous_ordinals_and_historical_evidence_only(self):check(R)
 def test_draft_source_fields_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter",
      "original_pdf_pages","short_original_anchor_not_diplomatic",
      "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_to_record_reverse_coverage(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],10)
 def test_provenance_hash_frozen_inputs(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_documentary_count_and_next_chapter(self):
  self.assertEqual(A["prior_lilly_accepted"],5457)
  self.assertEqual(A["new_documentary_records"],53)
  self.assertEqual(A["lilly_if_published"],5510)
  self.assertEqual(A["combined_if_published"],6576)
  self.assertEqual(A["next_editorial_chapter"],"XCVI")
  self.assertEqual(A["next_printed_chapter"],"XCV")
  self.assertEqual(A["following_heading_pdf"],504)
  self.assertEqual(len(U["issues"]),22)
 def test_medical_etiology_and_outcome_not_accepted_facts(self):
  self.assertTrue(A["author_final_witchcraft_verdict_negative"])
  self.assertTrue(A["author_never_confirmed_syphilis"])
  self.assertTrue(A["author_recovery_is_only_authorial_outcome_claim"])
  self.assertEqual(A["independent_medical_diagnoses"],0)
  self.assertEqual(A["independent_treatment_outcomes"],0)
  self.assertEqual(A["independent_occult_causes"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_mutant_false_medical_diagnosis_rejected(self):
  changed=copy.deepcopy(R);changed[33]["independently_authenticated_medical_diagnosis"]=True
  with self.assertRaises(AssertionError):check(changed)
 def test_mutant_false_treatment_success_rejected(self):
  changed=copy.deepcopy(R);changed[49]["independently_verified_medical_recovery"]=True
  with self.assertRaises(AssertionError):check(changed)
 def test_mutant_later_chapter_import_rejected(self):
  changed=copy.deepcopy(R);changed[-1]["chapter"]="XCV"
  with self.assertRaises(AssertionError):check(changed)
if __name__=="__main__":unittest.main(verbosity=2)
