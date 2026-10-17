import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(rows):
 assert len(rows)==29
 assert [r["record_number"] for r in rows]==list(range(6216,6245))
 assert [r["id"] for r in rows]==[f"R{k}" for k in range(6216,6245)]
 assert all(r["historical_documentary_accepted"] and
 r["global_record_number"]==r["record_number"] and
 not r["independently_verified_natal_outcome"] and
 not r["empirically_validated_prediction"] and
 not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="CIII" for r in rows[:-3])
 assert all(r["chapter"]=="CIV_NAVIGATION_ONLY" for r in rows[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_documentary_records_only(self):check(R)
 def test_original_semantics_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","printed_chapter","role",
      "original_pdf_pages","short_original_anchor_not_diplomatic",
      "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_forward_reverse_coverage(self):
  ids=[i for s in M["source_spans"] for i in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],4)
 def test_exact_hashed_inputs(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
    ("UNRESOLVED.json","unresolved_sha256"),
    ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
    ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_cumulative_and_following_chapter(self):
  self.assertEqual(A["prior_lilly"],6215)
  self.assertEqual(A["new_documentary_records"],29)
  self.assertEqual(A["lilly_if_published"],6244)
  self.assertEqual(A["combined_if_published"],7310)
  self.assertEqual(A["following_heading_pdf"],559)
  self.assertEqual(A["next_printed_chapter"],"CIII")
 def test_no_invented_numerical_orb(self):
  self.assertTrue(A["source_antiscia_and_fixed_star_numeric_thresholds_unspecified"])
  self.assertEqual(A["actual_person_outcomes_verified"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
 def test_mutant_false_human_outcome_rejected(self):
  x=copy.deepcopy(R);x[15]["independently_verified_natal_outcome"]=True
  with self.assertRaises(AssertionError):check(x)
 def test_mutant_next_chapter_merger_rejected(self):
  x=copy.deepcopy(R);x[-1]["chapter"]="CIII"
  with self.assertRaises(AssertionError):check(x)
if __name__=="__main__":unittest.main(verbosity=2)
