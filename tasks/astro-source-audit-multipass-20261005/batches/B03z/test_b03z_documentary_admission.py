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
 assert len(rows)==82
 assert [r["record_number"] for r in rows]==list(range(4550,4632))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(4550,4632)]
 assert all(r["historical_documentary_accepted"]
   and r["global_record_number"]==r["record_number"]
   and not r["independently_authenticated_religious_political_outcome"]
   and not r["empirically_validated_prediction"]
   and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="LXXX" for r in rows[:-2])
 assert all(r["chapter"]=="LXXXI_NAVIGATION_ONLY" for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_original_contiguous_global_ordinals(self):valid(R)
 def test_draft_field_identity_and_no_downgrade(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter","original_pdf_pages",
    "printed_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k],k)
   self.assertIsNone(d["global_record_number"])
 def test_all_original_passages_bidirectionally_covered(self):
  ids=[k for s in M["source_spans"] for k in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(len(ids),82)
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],13)
 def test_release_input_exact_byte_hashes(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
    ("UNRESOLVED.json","unresolved_sha256"),
    ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
    ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_historical_scope_and_qualified_timing(self):
  self.assertEqual(A["prior_lilly_accepted"],4549)
  self.assertEqual(A["new_documentary_records"],82)
  self.assertEqual(A["lilly_if_published"],4631)
  self.assertEqual(A["combined_if_published"],5697)
  self.assertEqual(A["next_chapter"],"LXXXI")
  self.assertTrue(A["status_quo_qualification_preserved"])
  self.assertIn("three whole years",A["source_predicted_window"])
  self.assertEqual(A["independently_verified_political_outcomes"],0)
  self.assertEqual(A["new_empirically_validated_predictions"],0)
  self.assertEqual(A["runtime_model_promotions"],0)
  self.assertEqual(len(U["issues"]),24)
  self.assertFalse(A["remote_canonical_published"])
 def test_cannot_promote_mutant_prediction(self):
  changed=copy.deepcopy(R)
  changed[60]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(changed)
 def test_cannot_import_following_chapter(self):
  changed=copy.deepcopy(R)
  changed[-1]["chapter"]="LXXX"
  with self.assertRaises(AssertionError):valid(changed)
if __name__=="__main__":unittest.main(verbosity=2)
