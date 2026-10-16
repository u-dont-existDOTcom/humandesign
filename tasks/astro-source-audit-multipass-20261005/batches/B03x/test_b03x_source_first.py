import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json');M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json');C=J('CLAIM_LEDGER.json')
def check(rows,spans):
 assert len(rows)==24 and len(spans)==6
 assert [r['source_local_id'] for r in rows]==[f'LXXVIII-C{i:03}' for i in range(1,25)]
 m=[x for s in spans for x in s['mapped_local_ids']]
 assert len(m)==len(set(m))==24 and sorted(m)==sorted(r['source_local_id'] for r in rows)
 by={r['source_local_id']:r for r in rows}
 assert all(s['original_pdf_pages']==by[k]['original_pdf_pages'] for s in spans for k in s['mapped_local_ids'])
 assert all(r['printed_pages']==[n-34 for n in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter']=='LXXVIII' for r in rows[:-2])
 assert all(r['chapter']=='LXXIX_NAVIGATION_ONLY' for r in rows[-2:])
 assert all(not r['historical_documentary_accepted'] and r['global_record_number'] is None
            and not r['independently_authenticated_dream_case'] and not r['empirically_validated_prediction']
            and not r['runtime_model_promoted'] for r in rows)
class SourceFirst(unittest.TestCase):
 def test_bijective_original_span_map(self):check(D['rows'],M['source_spans'])
 def test_witness_hashes(self):
  self.assertEqual([x['original_pdf_page'] for x in W['original_images']],[470,471])
  for x in W['original_images']:
   p=B/x['path'];self.assertEqual(p.stat().st_size,x['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['sha256'])
  self.assertEqual(W['original_images'][0]['sha256'],'1ed7310724070b24699186824e43bf33875c51f5ba0af5e382cfc7a685b5c777')
  self.assertEqual(W['original_full_pdf_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_authored_case_and_following_boundary(self):
  self.assertEqual(W['previous_accepted_lilly'],4484)
  self.assertEqual(W['next_numbered_chapter'],'LXXIX')
  self.assertEqual(W['following_heading_pdf'],471)
  self.assertEqual(D['rows'][1]['role'],'chart_timestamp')
  self.assertIn('1648',D['rows'][1]['historical_author_paraphrase'])
  self.assertIn('1644',D['rows'][-1]['historical_author_paraphrase'])
 def test_forecast_endpoints_not_pooled(self):
  out=[r for r in D['rows'] if r['role']=='source_internal_forecast']
  self.assertEqual(len(out),2)
  self.assertIn('no peril',out[0]['historical_author_paraphrase'])
  self.assertIn('damage',out[1]['historical_author_paraphrase'])
 def test_success_assertion_separate_from_validation(self):
  self.assertEqual(len([r for r in D['rows'] if r['role']=='authorial_outcome_claim']),1)
  self.assertEqual(C['author_asserted_retrospective_confirmation'],1)
  self.assertEqual(C['independently_authenticated_case_outcomes'],0)
  self.assertEqual(C['independently_validated_predictions'],0)
  self.assertEqual(C['runtime_promotions'],0)
 def test_original_dates_and_uncertainty_preserved(self):
  self.assertEqual(len(U['issues']),14)
  self.assertTrue(any('chronology' in x['issue'] for x in U['issues']))
  self.assertTrue(any('office' in x['issue'] for x in U['issues']))
 def test_duplicate_mapping_mutant(self):
  s=copy.deepcopy(M['source_spans']);s[0]['mapped_local_ids'].append(s[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],s)
 def test_next_chapter_leak_mutant(self):
  r=copy.deepcopy(D['rows']);r[-1]['chapter']='LXXVIII'
  with self.assertRaises(AssertionError):check(r,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
