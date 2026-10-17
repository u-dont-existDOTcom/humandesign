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
 assert len(rs)==34
 assert [r["record_number"] for r in rs]==list(range(5924,5958))
 assert [r["id"] for r in rs]==[f"R{k}" for k in range(5924,5958)]
 assert all(r["historical_documentary_accepted"] and
 r["global_record_number"]==r["record_number"] and
 not r["independently_authenticated_birth_time"] and
 not r["independently_validated_Animodar_accuracy"] and
 not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="C" for r in rs[:-3])
 assert all(r["chapter"]=="CI_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_record_numbers(self):valid(R)
 def test_source_preserved_without_rewrites(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","printed_chapter","role","original_pdf_pages",
    "short_original_anchor_not_diplomatic","historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_source_to_record_bijection(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],5)
 def test_frozen_input_sha256(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_science_and_source_qualifications(self):
  self.assertTrue(A["source_says_Animodar_weaker_than_accidents"])
  self.assertTrue(A["preexisting_accident_rectification_used_as_target"])
  self.assertEqual(A["independent_birth_time_accuracies"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
 def test_counts_and_next_boundaries(self):
  self.assertEqual(A["prior_lilly"],5923)
  self.assertEqual(A["lilly_if_published"],5957)
  self.assertEqual(A["combined_if_published"],7023)
  self.assertEqual(A["next_editorial_chapter"],"CI")
  self.assertEqual(A["next_heading_pdf"],541)
 def test_false_verified_birth_time_mutant(self):
  z=copy.deepcopy(R);z[23]["independently_authenticated_birth_time"]=True
  with self.assertRaises(AssertionError):valid(z)
 def test_false_animodar_accuracy_mutant(self):
  z=copy.deepcopy(R);z[16]["independently_validated_Animodar_accuracy"]=True
  with self.assertRaises(AssertionError):valid(z)
 def test_next_chapter_merge_mutant(self):
  z=copy.deepcopy(R);z[-1]["chapter"]="C"
  with self.assertRaises(AssertionError):valid(z)
if __name__=="__main__":unittest.main(verbosity=2)
