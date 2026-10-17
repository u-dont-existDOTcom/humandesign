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
 assert len(rows)==44
 assert [r["record_number"] for r in rows]==list(range(5414,5458))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(5414,5458)]
 assert all(r["historical_documentary_accepted"] and
  r["global_record_number"]==r["record_number"] and
  not r["independently_authenticated_horse_recovery"] and
  not r["independently_authenticated_theft_or_riders"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
 assert all(r["chapter"]=="XCIV" for r in rows[:-2])
 assert all(r["chapter"]=="XCV_NAVIGATION_ONLY" for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_source_only_global_records(self):check(R)
 def test_no_edit_to_original_claims(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","chapter","role","original_pdf_pages",
      "short_original_anchor_not_diplomatic","historical_author_paraphrase",
      "original_source_qualifications"):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d["global_record_number"])
 def test_reverse_map_bijection(self):
  ids=[k for s in M["source_spans"] for k in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
  self.assertEqual(M["span_count"],7)
 def test_source_input_sha256(self):
  for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),
   ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
   self.assertEqual(H(f),A[k],f)
 def test_preserve_author_discrepancy_and_calendar_uncertainty(self):
  self.assertEqual(A["prior_lilly_accepted"],5413)
  self.assertEqual(A["new_documentary_records"],44)
  self.assertEqual(A["lilly_if_published"],5457)
  self.assertEqual(A["combined_if_published"],6523)
  self.assertTrue(A["source_author_timing_shortfall_preserved"])
  self.assertTrue(A["absolute_reported_actual_day_ambiguous"])
  self.assertEqual(A["next_chapter"],"XCV")
  self.assertEqual(A["next_printed_chapter"],"XCIV")
 def test_empirical_scoring_and_thief_not_promoted(self):
  self.assertEqual(A["independently_verified_recovered_horses"],0)
  self.assertEqual(A["independent_theft_confirmed"],0)
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_model_promotions"],0)
  self.assertFalse(A["remote_canonical_published"])
 def test_mutant_false_credibility(self):
  bad=copy.deepcopy(R);bad[30]["independently_authenticated_horse_recovery"]=True
  with self.assertRaises(AssertionError):check(bad)
 def test_mutant_next_chapter_leak(self):
  bad=copy.deepcopy(R);bad[-1]["chapter"]="XCIV"
  with self.assertRaises(AssertionError):check(bad)
if __name__=="__main__":unittest.main(verbosity=2)
