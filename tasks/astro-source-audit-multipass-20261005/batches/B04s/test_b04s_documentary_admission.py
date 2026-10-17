import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];A=J("ACCEPTANCE.json")
class Admission(unittest.TestCase):
 def test_global_record_ids(self):
  self.assertEqual([r["record_number"] for r in R],list(range(5587,5630)))
  self.assertEqual([r["id"] for r in R],[f"R{i}" for i in range(5587,5630)])
 def test_preserve_source_text(self):
  for d,r in zip(D,R,strict=True):
   for k in ("source_local_id","source_span_id","role","section","historical_author_paraphrase","original_source_qualifications"):self.assertEqual(d[k],r[k])
 def test_reverse_map(self):
  m=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[x for s in m["source_spans"] for x in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r["id"] for r in R))
 def test_sha256(self):
  for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),("UNRESOLVED.json","unresolved_sha256"),("EXTERNAL_HISTORICAL_EVENT_LEDGER_20261017.json","external_evidence_sha256")):
   self.assertEqual(H(f),A[k])
 def test_external_corrob_does_not_equal_predictive_confirmation(self):
  self.assertTrue(A["historical_army_arms_surrender_independently_corroborated"])
  self.assertFalse(A["historical_essex_personally_surrendered"])
  self.assertFalse(A["independently_verified_original_astrology_forecast"])
  self.assertTrue(all(not r["empirically_validated_prediction"] for r in R))
 def test_next_table_and_totals(self):
  self.assertEqual(A["lilly_if_published"],5629)
  self.assertEqual(A["combined_if_published"],6695)
  self.assertEqual(A["next_original_pdf_page"],508)
  self.assertTrue(all(r["section"]=="PLANETARY_HOUR_TABLE_NAV_ONLY" for r in R[-2:]))
if __name__=="__main__":unittest.main(verbosity=2)
