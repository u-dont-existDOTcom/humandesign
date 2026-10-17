import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];R=J("RULES.json")["rules"]
M=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
A=J("ACCEPTANCE.json")
def check(records):
 assert len(records)==59
 assert [r["record_number"] for r in records]==list(range(6416,6475))
 assert [r["id"] for r in records]==[f"R{i}" for i in range(6416,6475)]
 assert all(r["historical_documentary_accepted"] and
 r["global_record_number"]==r["record_number"] and
 not r["independently_validated_temperament_or_health"] and
 not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in records)
 assert all(r["chapter"]=="CVII" for r in records[:-3])
 assert all(r["chapter"]=="CVIII_NAVIGATION_ONLY" for r in records[-3:])
class Admission(unittest.TestCase):
 def test_source_only_global_record_integrity(self):check(R)
 def test_source_claim_fields_not_changed(self):
  for d,r in zip(D,R,strict=True):
   for f in ("source_local_id","source_span_id","chapter","printed_chapter","role",
    "original_pdf_pages","short_original_anchor_not_diplomatic",
    "historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[f],r[f])
 def test_original_to_record_bijection(self):
  ids=[i for x in M["source_spans"] for i in x["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],9)
 def test_original_source_hashes_immutable(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
   self.assertEqual(H(f),A[k])
 def test_prior_and_next_chapter(self):
  self.assertEqual(A["prior_lilly_accepted"],6415)
  self.assertEqual(A["new_documentary_records"],59)
  self.assertEqual(A["lilly_if_published"],6474)
  self.assertEqual(A["combined_if_published"],7540)
  self.assertEqual(A["following_heading_pdf"],568)
  self.assertEqual(A["next_printed_chapter"],"CVII")
 def test_tally_disposition_and_no_human_predictions(self):
  self.assertTrue(A["equal_opposed_hot_cold_testimony_cancellation"])
  self.assertTrue(A["conditional_triple_lord_geniture_ascendant"])
  self.assertTrue(A["conditional_double_moon_ascendant"])
  self.assertEqual(A["out_of_sample_human_temperament_matches"],0)
  self.assertEqual(A["empirical_predictions_validated"],0)
  self.assertFalse(A["remote_published"])
 def test_mutant_false_clinical_success(self):
  x=copy.deepcopy(R);x[32]["independently_validated_temperament_or_health"]=True
  with self.assertRaises(AssertionError):check(x)
 def test_mutant_next_manners_leak(self):
  x=copy.deepcopy(R);x[-1]["chapter"]="CVII"
  with self.assertRaises(AssertionError):check(x)
if __name__=="__main__":unittest.main(verbosity=2)
