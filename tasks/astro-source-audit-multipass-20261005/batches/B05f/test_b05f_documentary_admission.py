import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json");A=J("ACCEPTANCE.json")
def check(rs):
 assert len(rs)==86
 assert [r["record_number"] for r in rs]==list(range(6475,6561))
 assert [r["id"] for r in rs]==[f"R{k}" for k in range(6475,6561)]
 assert all(r["historical_documentary_accepted"]
   and r["global_record_number"]==r["record_number"]
   and not r["independently_validated_human_personality"]
   and not r["independently_validated_criminal_or_medical_prognosis"]
   and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="CVIII" for r in rs[:-3])
 assert all(r["chapter"]=="CIX_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_documentary_records(self):check(R)
 def test_full_source_claims_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","role","printed_chapter",
   "original_pdf_pages","short_original_anchor_not_diplomatic","historical_author_paraphrase",
   "original_source_qualifications"):self.assertEqual(d[k],r[k])
 def test_reverse_map_onto_all_accepted_ids(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],14)
 def test_original_input_hashes(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_prior_total_and_next_heading(self):
  self.assertEqual(A["prior_lilly"],6474)
  self.assertEqual(A["lilly_if_published"],6560)
  self.assertEqual(A["combined_if_published"],7626)
  self.assertEqual(A["following_heading_pdf"],573)
  self.assertEqual(A["next_printed_chapter"],"CVIII")
 def test_source_skepticism_and_no_human_targets(self):
  self.assertTrue(A["no_independently_verified_mental_or_forensic_traits"])
  self.assertTrue(A["source_rejected_fine_degree_personality_scheme"])
  self.assertEqual(A["actual_blinded_human_personality_matches"],0)
  self.assertEqual(A["runtime_promotions"],0)
 def test_false_criminal_prediction_mutant_rejected(self):
  x=copy.deepcopy(R);x[62]["independently_validated_criminal_or_medical_prognosis"]=True
  with self.assertRaises(AssertionError):check(x)
 def test_next_chapter_contamination_mutant_rejected(self):
  x=copy.deepcopy(R);x[-1]["chapter"]="CVIII"
  with self.assertRaises(AssertionError):check(x)
if __name__=="__main__":unittest.main(verbosity=2)
