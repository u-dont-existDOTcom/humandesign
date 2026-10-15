"""Check original-case source mapping and evidence status."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
L=J('CLAIM_LEDGER.json')
def valid(rows,spans):
 assert len(rows)==58 and len(spans)==25
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LIX-C{i:03}' for i in range(1,59)]
 mapped=[k for s in spans for k in s['mapped_source_local_ids']]
 assert sorted(mapped)==sorted(ids) and len(mapped)==len(ids)
 by={r['source_local_id']:r for r in rows}
 assert all(by[k]['original_pdf_pages']==s['original_pdf_pages']
  for s in spans for k in s['mapped_source_local_ids'])
 assert all(r['global_record_number'] is None
  and not r['historical_documentation_admitted']
  and not r['real_outcome_independently_authenticated']
  and not r['empirical_astrology_prediction_validated']
  and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LIX' for r in rows[:-1])
 assert rows[-1]['chapter']=='LX_HEADING_ONLY'
 return True
class SourceTest(unittest.TestCase):
 def test_full_source_map(self):self.assertTrue(valid(D['rows'],M['source_spans']))
 def test_image_sha256(self):
  self.assertEqual([i['pdf_page'] for i in W['images']],[419,420,421,422,423])
  for im in W['images']:
   b=(B/im['path']).read_bytes()
   self.assertEqual(hashlib.sha256(b).hexdigest(),im['sha256'])
 def test_separate_charts(self):
  text=' '.join(r['historical_author_report_paraphrase']+' '+r['conditions_source_limits_or_chronology'] for r in D['rows']).lower()
  self.assertIn('16 june 1646',text)
  self.assertIn('11 june 1646',text)
 def test_outcome_not_authenticated(self):
  self.assertEqual(L['independently_confirmed_1646_marriage'],0)
  self.assertEqual(L['frozen_pre_outcome_horoscope_forecasts'],0)
  self.assertEqual(len(U['issues']),18)
 def test_original_source_types(self):
  self.assertEqual(sum(r['role']=='figure' for r in D['rows']),1)
  self.assertGreaterEqual(sum(r['role']=='counterfactual' for r in D['rows']),4)
 def test_mutants_rejected(self):
  altered=copy.deepcopy(D['rows'])
  altered[-1]['chapter']='LIX'
  with self.assertRaises(AssertionError):valid(altered,M['source_spans'])
  altered=copy.deepcopy(D['rows'])
  altered[5]['real_outcome_independently_authenticated']=True
  with self.assertRaises(AssertionError):valid(altered,M['source_spans'])
  altered=copy.deepcopy(M['source_spans'])
  altered[0]['mapped_source_local_ids'].append(altered[1]['mapped_source_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D['rows'],altered)
if __name__=='__main__':unittest.main(verbosity=2)
