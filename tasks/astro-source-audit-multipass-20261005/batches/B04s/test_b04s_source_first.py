import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");E=J("EXTERNAL_HISTORICAL_EVENT_LEDGER_20261017.json")
def validate(rows,spans):
 assert len(rows)==43 and len(spans)==7
 assert [r["source_local_id"] for r in rows]==[f"ESSEX-C{i:03}" for i in range(1,44)]
 ids=[x for s in spans for x in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==43
 assert set(ids)=={r["source_local_id"] for r in rows}
 assert all(r["section"]=="UNNUMBERED_ESSEX" for r in rows[:-2])
 assert all(r["section"]=="PLANETARY_HOUR_TABLE_NAV_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_original_prediction"] and not r["empirically_validated_prediction"]
  and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_mapping(self):validate(D,M)
 def test_image_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],[507,508])
  for x in W["original_images"]:
   f=B/x["path"];self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),x["sha256"])
 def test_prior_baseline(self):
  self.assertEqual(W["previous_accepted_lilly"],5586)
  self.assertEqual(W["first_proposed_record"],5587)
  self.assertEqual(W["next_table_range"],[508,515])
 def test_author_forecast_vs_event(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for q in ("limited success","substantial losses","initially prospered","september 8","september 2"):self.assertIn(q,t)
 def test_external_history_distinction(self):
  x=E["external_authority"]
  self.assertTrue(x["military_event_externally_corroborated"])
  self.assertFalse(x["author_pre_event_astrology_prediction_independently_authenticated"])
  self.assertFalse(x["author_surrendered_himself_literally_supported"])
  self.assertEqual(len(x["separate_historical_events"]),2)
 def test_zero_validation(self):
  self.assertEqual(E["new_empirically_validated_predictions"],0)
  self.assertEqual(E["runtime_promotions"],0)
 def test_mutant_duplicate_source_fails(self):
  m=copy.deepcopy(M);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):validate(D,m)
 def test_mutant_false_prediction_credited_fails(self):
  d=copy.deepcopy(D);d[20]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):validate(d,M)
if __name__=="__main__":unittest.main(verbosity=2)
