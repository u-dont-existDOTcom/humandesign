import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json");U=J("UNRESOLVED.json")
def valid(rows):
 assert len(rows)==72
 assert [r["record_number"] for r in rows]==list(range(4955,5027))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(4955,5027)]
 assert all(r["historical_documentary_accepted"] and r["global_record_number"]==r["record_number"] and
   not r["independently_authenticated_wartime_outcome"] and
   not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="LXXXV" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXVI_NAVIGATION_ONLY" for r in rows[-2:])
 assert len([r for r in rows if r["role"]=="authorial_error_admission"])==1
class Admission(unittest.TestCase):
 def test_original_contiguous_global_ids(self):valid(R)
 def test_original_clause_fields_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","role","chapter","source_span_id","original_pdf_pages",
             "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_reverse_span_bijection(self):
  ids=[r for s in M["source_spans"] for r in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],11)
 def test_source_exact_hashes(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_historical_provenance_never_claims_external_accuracy(self):
  self.assertEqual(A["prior_lilly_accepted"],4954)
  self.assertEqual(A["new_documentary_records"],72)
  self.assertEqual(A["lilly_if_published"],5026)
  self.assertEqual(A["combined_if_published"],6092)
  self.assertEqual(A["next_chapter"],"LXXXVI")
  self.assertTrue(A["edgehill_pre_question_not_forecast"])
  self.assertTrue(A["rupert_authorial_partial_error_must_remain"])
  self.assertEqual(len(U["issues"]),25)
  self.assertEqual(A["independently_verified_wartime_outcomes"],0)
  self.assertEqual(A["new_empirically_validated_predictions"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_false_empirical_success_mutant_rejected(self):
  r=copy.deepcopy(R);r[30]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(r)
 def test_following_chapter_contamination_rejected(self):
  r=copy.deepcopy(R);r[-1]["chapter"]="LXXXV"
  with self.assertRaises(AssertionError):valid(r)
if __name__=="__main__":unittest.main(verbosity=2)
