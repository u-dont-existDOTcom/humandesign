import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json");U=J("UNRESOLVED.json")
def check(rows):
 assert len(rows)==57
 assert [r["record_number"] for r in rows]==list(range(4632,4689))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(4632,4689)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_authenticated_philosophers_stone_case"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="LXXXI" for r in rows[:-3])
 assert all(r["chapter"]=="LXXXII_NAVIGATION_ONLY" for r in rows[-3:])
class Admission(unittest.TestCase):
 def test_global_id_continuity_and_next_divider(self):check(R)
 def test_original_content_not_rewritten(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","role","chapter","source_span_id",
    "original_pdf_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_reverse_map_complete(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],11)
 def test_accepted_source_hash_integrity(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_documentary_only_and_historical_health_scope(self):
  self.assertEqual(A["prior_lilly_accepted"],4631)
  self.assertEqual(A["new_documentary_records"],57)
  self.assertEqual(A["lilly_if_published"],4688)
  self.assertEqual(A["combined_if_published"],5754)
  self.assertEqual(A["next_chapter"],"LXXXII")
  self.assertTrue(A["authorial_belief_is_not_validated_elixir"])
  self.assertTrue(A["medical_allegation_is_not_confirmed_diagnosis"])
  self.assertEqual(A["independently_verified_alchemical_successes"],0)
  self.assertEqual(A["independently_authenticated_medical_diagnoses"],0)
  self.assertEqual(A["new_empirically_validated_predictions"],0)
  self.assertEqual(len(U["issues"]),20)
  self.assertFalse(A["remote_canonical_published"])
 def test_false_predictive_credit_mutant_rejected(self):
  changed=copy.deepcopy(R);changed[30]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(changed)
if __name__=="__main__":unittest.main(verbosity=2)
