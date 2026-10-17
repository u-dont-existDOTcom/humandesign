import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];A=J("ACCEPTANCE.json")
class Admission(unittest.TestCase):
 def test_ids(self):
  self.assertEqual([r["record_number"] for r in R],list(range(5553,5587)))
  self.assertEqual(len(R),34)
 def test_source_unchanged(self):
  for x,y in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","historical_author_paraphrase","original_source_qualifications"):self.assertEqual(x[k],y[k])
 def test_no_false_science(self):
  self.assertTrue(all(not r["empirically_validated_prediction"] and not r["independently_verified_prior_garrison_capture"] for r in R))
  self.assertEqual(A["empirical_validations"],0)
 def test_navigation(self):
  self.assertTrue(all(r["chapter"]=="POST_XCVI_NAVIGATION_ONLY" for r in R[-4:]))
  self.assertEqual(A["next"],"UNNUMBERED_ESSEX_AND_TABLES")
 def test_source_hash(self):
  for file,key in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256")]:self.assertEqual(H(file),A[key])
 def test_reverse_bijection(self):
  m=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[x for s in m["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
 def test_original_chronology(self):
  self.assertTrue(R and A["combined_if_published"]==6652)
  self.assertTrue(any("before the question" in r["historical_author_paraphrase"] for r in R))
if __name__=="__main__":unittest.main(verbosity=2)
