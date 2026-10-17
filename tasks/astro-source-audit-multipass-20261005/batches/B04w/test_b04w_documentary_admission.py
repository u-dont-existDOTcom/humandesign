import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=j("RULES.json")["rules"];A=j("ACCEPTANCE.json")
def valid(rows):
 assert len(rows)==99
 assert [r["record_number"] for r in rows]==list(range(5825,5924))
 assert [r["id"] for r in rows]==[f"R{i}" for i in range(5825,5924)]
 assert all(r["historical_documentary_accepted"] and
 r["global_record_number"]==r["record_number"] and not r["independently_verified_conception_event"]
 and not r["independently_verified_natal_birth_time"] and not r["empirically_validated_prediction"]
 and not r["runtime_model_promoted"] for r in rows)
 assert all(r["section"]=="TRUTINE_AND_OTHER_RECTIFICATION_METHODS" for r in rows[:-3])
 assert all(r["section"]=="NEXT_ANIMODAR_NAV_ONLY" for r in rows[-3:])
class Admission(unittest.TestCase):
 def test_record_sequence_and_source_only(self):valid(R)
 def test_source_preservation(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","section","original_pdf_pages","historical_author_paraphrase","original_source_qualifications"):self.assertEqual(d[k],r[k])
 def test_reverse_map(self):
  z=j("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[i for g in z["source_spans"] for i in g["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
 def test_hashes(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
   ("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
   ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):self.assertEqual(h(f),A[k])
 def test_corpus_and_next_Animodar(self):
  self.assertEqual(A["prior_lilly"],5824)
  self.assertEqual(A["lilly_if_published"],5923)
  self.assertEqual(A["combined_if_published"],6989)
  self.assertEqual(A["next_printed_chapter"],"XCIX")
  self.assertEqual(A["next_editorial_chapter"],"C")
 def test_source_negative_qualification(self):
  self.assertTrue(A["Trutine_exact_degree_failure_admitted"])
  self.assertTrue(A["source_life_events_method_preferred"])
  self.assertTrue(A["source_conception_hour_method_not_credited"])
  self.assertEqual(A["independent_birth_time_successes"],0)
 def test_no_empirical_credit(self):
  self.assertEqual(A["new_empirical_validations"],0)
  self.assertEqual(A["runtime_promotions"],0)
 def test_mutant_false_precision_rejected(self):
  x=copy.deepcopy(R);x[51]["independently_verified_natal_birth_time"]=True
  with self.assertRaises(AssertionError):valid(x)
if __name__=="__main__":unittest.main(verbosity=2)
