import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding="utf-8"))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json");U=J("UNRESOLVED.json")
def check(rows):
 assert len(rows)==141
 assert [r["record_number"] for r in rows]==list(range(4689,4830))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(4689,4830)]
 assert all(r["historical_documentary_accepted"]
  and r["global_record_number"]==r["record_number"]
  and not r["independently_authenticated_office_outcome"]
  and not r["empirically_validated_prediction"]
  and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="LXXXII" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXIII_NAVIGATION_ONLY" for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_contiguous_global_records(self):check(R)
 def test_no_change_to_original_draft(self):
  for before,after in zip(D,R,strict=True):
   for key in ("source_local_id","source_span_id","chapter","role",
     "original_pdf_pages","short_original_anchor_not_diplomatic",
     "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(before[key],after[key])
   self.assertIsNone(before["global_record_number"])
 def test_bidirectional_span_mapping(self):
  ids=[i for s in M["source_spans"] for i in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(len(ids),141)
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],21)
 def test_exact_hash_receipts(self):
  for name,key in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
   self.assertEqual(H(name),A[key],name)
 def test_documentary_scope_and_count(self):
  self.assertEqual(A["prior_lilly_accepted"],4688)
  self.assertEqual(A["new_documentary_records"],141)
  self.assertEqual(A["lilly_if_published"],4829)
  self.assertEqual(A["combined_if_published"],5895)
  self.assertEqual(A["next_chapter"],"LXXXIII")
  self.assertTrue(A["office_acquisition_distinct_from_office_retention"])
  self.assertEqual(A["independently_verified_office_outcomes"],0)
  self.assertEqual(A["new_empirically_validated_predictions"],0)
  self.assertEqual(A["runtime_model_promotions"],0)
  self.assertEqual(len(U["issues"]),26)
  self.assertFalse(A["remote_canonical_published"])
 def test_false_empirical_result_mutant(self):
  changed=copy.deepcopy(R);changed[80]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(changed)
if __name__=="__main__":unittest.main(verbosity=2)
