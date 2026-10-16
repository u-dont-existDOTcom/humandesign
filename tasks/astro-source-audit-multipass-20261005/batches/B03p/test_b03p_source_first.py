import unittest
import json,hashlib,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
C=J('CLAIM_LEDGER.json')
def check(rows,spans):
 assert len(rows)==45 and len(spans)==14
 ids=[r['local_id'] for r in rows]
 assert ids==[f'LXX-C{i:03}' for i in range(1,46)]
 mapped=[k for s in spans for k in s['mapped_local_ids']]
 assert len(mapped)==45 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages'] for s in spans for k in s['mapped_local_ids'])
 assert all(r['global_record_number'] is None and not r['historical_documentary_admitted'] for r in rows)
 assert all(r['chapter']=='LXX' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXXI_NAVIGATION_ONLY'
class Source(unittest.TestCase):
 def test_exact_map(self):check(D['rows'],M['source_spans'])
 def test_primary_images(self):
  for im in W['original_images']:
   raw=(B/im['path']).read_bytes()
   self.assertEqual(len(raw),im['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),im['sha256'])
 def test_case_separation(self):
  self.assertEqual(W['printed_chart_date'],'6 February 1644')
  self.assertEqual(W['next_heading_pdf'],451)
  self.assertEqual(C['independently_authenticated_spouse_outcomes'],0)
  self.assertEqual(C['empirically_validated_predictive_cases'],0)
 def test_forecast_not_exact_october_day(self):
  self.assertEqual(C['forecast_time_window'],'late September or beginning October')
  self.assertEqual(C['forecast_outcome'],'death OR great danger')
 def test_original_uncertainties(self):
  self.assertEqual(len(J('UNRESOLVED_SOURCE_LIMITS.json')['issues']),18)
 def test_duplicate_mutant_rejected(self):
  bad=copy.deepcopy(M['source_spans'])
  bad[0]['mapped_local_ids'].append(bad[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],bad)
 def test_false_case_mutant_rejected(self):
  bad=copy.deepcopy(D['rows']);bad[-1]['chapter']='LXX'
  with self.assertRaises(AssertionError):check(bad,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
