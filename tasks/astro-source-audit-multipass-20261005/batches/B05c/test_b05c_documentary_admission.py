import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];A=J("ACCEPTANCE.json")
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
def valid(rs):
 assert len(rs)==74
 assert [r["record_number"] for r in rs]==list(range(6310,6384))
 assert [r["id"] for r in rs]==[f"R{k}" for k in range(6310,6384)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_authenticated_death_or_survival"] and
  not r["medical_longevity_prediction_validated"] and
  not r["empirically_validated_prediction"] and
  not r["runtime_model_promoted"] for r in rs)
 assert all(r["chapter"]=="CV" for r in rs[:-3])
 assert all(r["chapter"]=="CVI_NAVIGATION_ONLY" for r in rs[-3:])
class Admission(unittest.TestCase):
 def test_contiguous_source_only_global_records(self):valid(R)
 def test_draft_language_and_source_pages_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","printed_chapter","role",
    "original_pdf_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_original_passage_reverse_map_bijection(self):
  ids=[k for s in M["source_spans"] for k in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],7)
 def test_exact_source_hashes(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
   self.assertEqual(H(f),A[k])
 def test_count_acceptance_and_following_lord_geniture(self):
  self.assertEqual(A["prior_lilly"],6309)
  self.assertEqual(A["added_documentary_records"],74)
  self.assertEqual(A["lilly_if_published"],6383)
  self.assertEqual(A["combined_if_published"],7449)
  self.assertEqual(A["following_heading_pdf_page"],565)
  self.assertEqual(A["following_printed_chapter"],"CV")
 def test_preserve_explicit_historical_uncertainty(self):
  self.assertTrue(A["original_author_skepticism_explicit"])
  self.assertFalse(A["original_Alcochodon_years_independent_accuracy"])
  self.assertEqual(A["independently_verified_death_survival"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
 def test_mutant_false_mortality_validation_rejected(self):
  q=copy.deepcopy(R);q[36]["medical_longevity_prediction_validated"]=True
  with self.assertRaises(AssertionError):valid(q)
 def test_mutant_chapter_merger_rejected(self):
  q=copy.deepcopy(R);q[-1]["chapter"]="CV"
  with self.assertRaises(AssertionError):valid(q)
if __name__=="__main__":unittest.main(verbosity=2)
