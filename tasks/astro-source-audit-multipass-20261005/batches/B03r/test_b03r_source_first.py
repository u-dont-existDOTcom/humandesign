import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
C=J('CLAIM_LEDGER.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
def check(rows,spans):
 assert len(rows)==43 and len(spans)==11
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LXXII-C{i:03}' for i in range(1,44)]
 mapped=[id for s in spans for id in s['mapped_source_local_ids']]
 assert len(mapped)==43 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages']
  for s in spans for k in s['mapped_source_local_ids'])
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['global_record_number'] is None and not r['historical_documentary_accepted']
  and not r['prospective_astrology_prediction_validated'] and not r['runtime_rule_promoted']
  for r in rows)
 assert all(r['chapter']=='LXXII' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXXIII_NAVIGATION_ONLY'
class SourceFirst(unittest.TestCase):
 def test_exact_map(self):check(D['rows'],M['source_spans'])
 def test_original_image_hashes(self):
  for im in W['original_images']:
   raw=(B/im['path']).read_bytes()
   self.assertEqual(len(raw),im['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),im['sha256'])
 def test_dates_and_historical_event(self):
  self.assertEqual(W['chart_printed_date'],'3 December 1644')
  self.assertEqual(W['chart_printed_time'],'2:24 PM')
  self.assertEqual(W['external_confirmed_execution_date'],'10 January 1645')
  self.assertFalse(W['independent_prospective_forecast_freeze'])
 def test_true_source_window(self):
  self.assertEqual(W['previous_lilly_accepted'],4093)
  self.assertEqual(W['original_body_pdf_pages'],[453,454])
  self.assertEqual(W['next_heading_pdf'],455)
 def test_no_attributed_prediction_validation(self):
  self.assertEqual(C['independently_confirmed_historical_events'],1)
  self.assertEqual(C['independently_authenticated_prior_forecasts'],0)
  self.assertEqual(C['empirically_validated_astrology_predictions'],0)
  self.assertEqual(len(U['issues']),18)
 def test_negative_mutants(self):
  x=copy.deepcopy(M['source_spans']);x[0]['mapped_source_local_ids'].append(x[1]['mapped_source_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],x)
  r=copy.deepcopy(D['rows']);r[18]['prospective_astrology_prediction_validated']=True
  with self.assertRaises(AssertionError):check(r,M['source_spans'])
  r=copy.deepcopy(D['rows']);r[-1]['chapter']='LXXII'
  with self.assertRaises(AssertionError):check(r,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
