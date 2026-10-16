import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
U=J("UNRESOLVED.json")
def validate(rows):
 assert [r["record_number"] for r in rows]==list(range(3933,3977))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(3933,3977)]
 assert all(r["documentary_admitted"] and not r["independent_wealth_outcome_authenticated"]
   and not r["validated_predictive_case"] and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="LXVIII" for r in rows[:-1])
 assert rows[-1]["chapter"]=="LXIX_NAVIGATION_ONLY"
class Admission(unittest.TestCase):
 def test_contiguous_accepted(self):
  validate(R["rules"])
  self.assertEqual(R["record_count"],44)
  self.assertEqual(R["chapter_lxviii_source_units"],43)
 def test_draft_exact_survives(self):
  for a,b in zip(D,R["rules"],strict=True):
   for k in ("source_local_id","role","original_pdf_pages",
    "historical_author_paraphrase","conditions_scope_and_uncertainty"):
    self.assertEqual(a[k],b[k])
   self.assertIsNone(a["global_record_number"])
 def test_source_to_record_bijection(self):
  ids=[k for x in M["source_spans"] for k in x["canonical_record_ids"]]
  self.assertEqual(len(ids),44)
  self.assertEqual(sorted(ids),sorted(x["id"] for x in R["rules"]))
  self.assertEqual(M["span_count"],11)
 def test_source_hash_receipts(self):
  for n,k in [("RULES.json","rules_sha256"),
   ("SOURCE_ORDER.json","order_sha256"),("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_audit_sha256")]:
   self.assertEqual(H(n),A[k])
 def test_retained_negative_outcomes(self):
  txt=" ".join(r["historical_author_paraphrase"] for r in R["rules"]).lower()
  for t in ("difficulty","delayed","nonpayment","cheating","cannot always be certain"):
   self.assertIn(t,txt)
  self.assertEqual(R["independent_dowry_receipts_verified"],0)
  self.assertEqual(R["independent_fraud_cases_verified"],0)
 def test_baseline_and_next_chapter(self):
  self.assertEqual(A["previous_lilly_accepted"],3932)
  self.assertEqual(A["new_documentary_records"],44)
  self.assertEqual(A["lilly_if_published"],3976)
  self.assertEqual(A["combined_if_published"],5042)
  self.assertEqual(A["next_chapter"],"LXIX")
  self.assertEqual(len(U["issues"]),15)
  self.assertFalse(A["canonical_published"])
 def test_semantic_mutants(self):
  bad=copy.deepcopy(R["rules"]);bad[0]["validated_predictive_case"]=True
  with self.assertRaises(AssertionError):validate(bad)
  bad=copy.deepcopy(R["rules"]);bad[-1]["chapter"]="LXVIII"
  with self.assertRaises(AssertionError):validate(bad)
  bad=copy.deepcopy(R["rules"]);bad[1]["record_number"]=0
  with self.assertRaises(AssertionError):validate(bad)
if __name__=="__main__":unittest.main(verbosity=2)
