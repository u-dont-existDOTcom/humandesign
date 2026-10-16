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
 assert len(rs)==46
 assert [r["record_number"] for r in rs]==list(range(4830,4876))
 assert [r["id"] for r in rs]==[f"R{i}" for i in range(4830,4876)]
 assert all(r["historical_documentary_accepted"] and
  not r["independently_authenticated_restoration_outcome"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="LXXXIII" for r in rs[:-2])
 assert all(r["chapter"]=="LXXXIV_NAVIGATION_ONLY" for r in rs[-2:])
class Admission(unittest.TestCase):
 def test_contiguous_ids_and_nonvalidation(self):valid(R)
 def test_source_to_record_content_unchanged(self):
  for old,new in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","role","original_pdf_pages","historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(old[k],new[k])
 def test_reverse_span_bijection(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
 def test_byte_hashes(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
  ("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
  ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_prior_index_and_outcome_isolation(self):
  self.assertEqual(A["prior_lilly_accepted"],4829)
  self.assertEqual(A["new_documentary_records"],46)
  self.assertEqual(A["lilly_if_published"],4875)
  self.assertEqual(A["combined_if_published"],5941)
  self.assertEqual(A["next_chapter"],"LXXXIV")
  self.assertEqual(A["independently_verified_restoration_outcomes"],0)
  self.assertEqual(A["empirically_validated_predictions"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_false_prediction_mutant(self):
  rs=copy.deepcopy(R);rs[15]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(rs)
if __name__=="__main__":unittest.main(verbosity=2)
