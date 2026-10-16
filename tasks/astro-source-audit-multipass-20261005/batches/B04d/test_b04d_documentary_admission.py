import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(rs):
 assert len(rs)==79
 assert [r["record_number"] for r in rs]==list(range(4876,4955))
 assert [r["id"] for r in rs]==[f"R{i}" for i in range(4876,4955)]
 assert all(r["historical_documentary_accepted"]
  and not r["independently_authenticated_vocational_outcome"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="LXXXIV" for r in rs[:-2])
 assert all(r["chapter"]=="LXXXV_NAVIGATION_ONLY" for r in rs[-2:])
class Admission(unittest.TestCase):
 def test_ids_and_epistemic_separation(self):check(R)
 def test_source_first_fields_immutable(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter","original_pdf_pages","historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
 def test_bidirectional_passage_map(self):
  ids=[r for s in M["source_spans"] for r in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],15)
 def test_original_accepted_hashes(self):
  for n,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
    ("UNRESOLVED.json","unresolved_sha256"),
    ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
    ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
   self.assertEqual(H(n),A[k])
 def test_count_next_chapter_and_mars_venus(self):
  self.assertEqual(A["prior_lilly_accepted"],4875)
  self.assertEqual(A["new_documentary_records"],79)
  self.assertEqual(A["lilly_if_published"],4954)
  self.assertEqual(A["combined_if_published"],6020)
  self.assertEqual(A["next_chapter"],"LXXXV")
  self.assertTrue(A["Mars_Venus_glyph_original_verified"])
  self.assertEqual(A["independently_verified_vocational_outcomes"],0)
  self.assertEqual(A["empirically_validated_predictions"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_mutant_empirical_promotion_rejected(self):
  changed=copy.deepcopy(R);changed[30]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(changed)
if __name__=="__main__":unittest.main(verbosity=2)
