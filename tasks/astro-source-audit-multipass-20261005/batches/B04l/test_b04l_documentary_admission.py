import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(r):
 assert len(r)==31
 assert [x["record_number"] for x in r]==list(range(5308,5339))
 assert [x["id"] for x in r]==[f"R{i}" for i in range(5308,5339)]
 assert all(x["historical_documentary_accepted"] and
   x["global_record_number"]==x["record_number"] and
   not x["independently_authenticated_captive_outcome"] and
   not x["empirically_validated_prediction"] and not x["runtime_model_promoted"] for x in r)
 assert all(x["chapter"]=="XCII" for x in r[:-2])
 assert all(x["chapter"]=="XCIII_NAVIGATION_ONLY" for x in r[-2:])
class Admission(unittest.TestCase):
 def test_record_continuity_and_false_validation(self):check(R)
 def test_first_source_content_not_rewritten(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","chapter","original_pdf_pages",
      "printed_pages","short_original_anchor_not_diplomatic",
      "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_to_record_mapping(self):
  ids=[id for s in M["source_spans"] for id in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],5)
 def test_exact_admission_input_hashes(self):
  for name,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
    ("UNRESOLVED.json","unresolved_sha256"),
    ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
    ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
   self.assertEqual(H(name),A[k],name)
 def test_documentary_counts_and_next_heading(self):
  self.assertEqual(A["prior_lilly_accepted"],5307)
  self.assertEqual(A["new_documentary_records"],31)
  self.assertEqual(A["lilly_if_published"],5338)
  self.assertEqual(A["combined_if_published"],6404)
  self.assertEqual(A["next_printed_chapter"],"XCII")
  self.assertEqual(A["next_editorial_chapter"],"XCIII")
  self.assertEqual(A["following_heading_pdf"],498)
  self.assertEqual(A["independent_captive_outcomes"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_falsified_promotion_mutant(self):
  broken=copy.deepcopy(R);broken[15]["runtime_model_promoted"]=True
  with self.assertRaises(AssertionError):check(broken)
 def test_falsified_next_chapter_mutant(self):
  broken=copy.deepcopy(R);broken[-1]["chapter"]="XCII"
  with self.assertRaises(AssertionError):check(broken)
if __name__=="__main__":unittest.main(verbosity=2)
