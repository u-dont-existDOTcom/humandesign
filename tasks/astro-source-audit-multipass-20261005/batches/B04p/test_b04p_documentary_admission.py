import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(rs):
 assert len(rs)==42
 assert [r["record_number"] for r in rs]==list(range(5511,5553))
 assert [r["id"] for r in rs]==[f"R{i}" for i in range(5511,5553)]
 assert all(r["historical_documentary_accepted"]
   and r["global_record_number"]==r["record_number"]
   and not r["independently_verified_escaped_prisoner_identity"]
   and not r["independently_authenticated_fugitive_recapture"]
   and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="XCVI" for r in rs[:-3])
 assert all(r["chapter"]=="XCVII_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_global_ids_and_no_retrospective_empirical_validation(self):check(R)
 def test_source_first_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","role",
    "original_pdf_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_reverse_passage_bijection(self):
  ids=[k for s in M["source_spans"] for k in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],7)
 def test_exact_admission_hashes(self):
  for f,k in [("RULES.json","rules_sha256"),
   ("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_corpus_totals_and_next_chapter(self):
  self.assertEqual(A["prior_lilly_accepted"],5510)
  self.assertEqual(A["new_documentary_records"],42)
  self.assertEqual(A["lilly_if_published"],5552)
  self.assertEqual(A["combined_if_published"],6618)
  self.assertEqual(A["next_editorial_chapter"],"XCVII")
  self.assertEqual(A["next_printed_chapter"],"XCVI")
  self.assertEqual(A["following_heading_pdf"],505)
 def test_no_independent_letter_custody_or_time_outcome(self):
  self.assertEqual(A["independent_recaptures_verified"],0)
  self.assertEqual(A["independent_direction_outcomes_verified"],0)
  self.assertEqual(A["independent_prisoner_identity"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_model_promotions"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_mutant_false_recapture_proof(self):
  bad=copy.deepcopy(R);bad[29]["independently_authenticated_fugitive_recapture"]=True
  with self.assertRaises(AssertionError):check(bad)
 def test_mutant_wrong_chapter_scope(self):
  bad=copy.deepcopy(R);bad[-1]["chapter"]="XCVI"
  with self.assertRaises(AssertionError):check(bad)
if __name__=="__main__":unittest.main(verbosity=2)
