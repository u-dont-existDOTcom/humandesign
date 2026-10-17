import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(records):
 assert len(records)==32
 assert [r["record_number"] for r in records]==list(range(6384,6416))
 assert [r["id"] for r in records]==[f"R{k}" for k in range(6384,6416)]
 assert all(r["historical_documentary_accepted"] and r["global_record_number"]==r["record_number"]
 and not r["independently_verified_lord_geniture_personality"]
 and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in records)
 assert all(r["chapter"]=="CVI" for r in records[:-3])
 assert all(r["chapter"]=="CVII_NAVIGATION_ONLY" for r in records[-3:])
class Admission(unittest.TestCase):
 def test_record_continuity_and_no_predictive_credit(self):check(R)
 def test_original_source_claims_preserved(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","printed_chapter","role","original_pdf_pages",
    "short_original_anchor_not_diplomatic","historical_author_paraphrase",
    "original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_reverse_map_bijection(self):
  ids=[x for s in M["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],6)
 def test_exact_input_hashes(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","audit_sha256")]:
   self.assertEqual(H(f),A[k])
 def test_prior_and_next(self):
  self.assertEqual(A["prior_lilly"],6383)
  self.assertEqual(A["new_historical_annotations"],32)
  self.assertEqual(A["lilly_if_published"],6415)
  self.assertEqual(A["combined_if_published"],7481)
  self.assertEqual(A["following_heading_pdf"],566)
  self.assertEqual(A["next_printed_chapter"],"CVI")
 def test_multiple_planets_not_hidden(self):
  self.assertTrue(A["runnerup_and_nearequal_planet_allowed"])
  self.assertTrue(A["no_frozen_numeric_weights_or_thresholds"])
  self.assertEqual(A["independent_human_personality_validations"],0)
  self.assertFalse(A["remote_published"])
 def test_false_personality_match_mutant_rejected(self):
  r=copy.deepcopy(R);r[15]["independently_verified_lord_geniture_personality"]=True
  with self.assertRaises(AssertionError):check(r)
 def test_next_chapter_merge_mutant_rejected(self):
  r=copy.deepcopy(R);r[-1]["chapter"]="CVI"
  with self.assertRaises(AssertionError):check(r)
if __name__=="__main__":unittest.main(verbosity=2)
