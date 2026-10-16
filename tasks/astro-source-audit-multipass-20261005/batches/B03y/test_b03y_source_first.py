import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
def check(rows,spans):
 assert len(rows)==41 and len(spans)==7
 assert [r['source_local_id'] for r in rows]==[f'LXXIX-C{i:03}' for i in range(1,42)]
 m=[x for s in spans for x in s['mapped_local_ids']]
 assert len(m)==len(set(m))==41
 assert set(m)=={r['source_local_id'] for r in rows}
 by={r['source_local_id']:r for r in rows}
 assert all(s['original_pdf_pages']==by[k]['original_pdf_pages'] for s in spans for k in s['mapped_local_ids'])
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter']=='LXXIX' for r in rows[:-2])
 assert all(r['chapter']=='LXXX_NAVIGATION_ONLY' for r in rows[-2:])
 assert all(r['global_record_number'] is None and not r['historical_documentary_accepted']
   and not r['independently_authenticated_parsonage_case']
   and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rows)
class SourceFirst(unittest.TestCase):
 def test_unique_source_span_bijection(self):check(D['rows'],M['source_spans'])
 def test_original_page_witness_hashes(self):
  self.assertEqual([i['original_pdf_page'] for i in W['original_images']],[471,472,473])
  for i in W['original_images']:
   p=B/i['path'];self.assertEqual(p.stat().st_size,i['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),i['sha256'])
  self.assertEqual(W['original_images'][0]['sha256'],'1b836e7bec0aa96be01c47de14ecf158642de238d609038704158d38ad61f105')
 def test_previous_published_baseline(self):
  self.assertEqual(W['previous_accepted_lilly'],4508)
  self.assertEqual(W['next_numbered_chapter'],'LXXX')
  self.assertEqual(W['following_heading_pdf'],473)
  self.assertEqual(W['original_body_pdf_pages'],[471,472])
 def test_original_page_seam_and_navigation_isolated(self):
  self.assertEqual([s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1],[[471,472]])
  self.assertEqual(len([r for r in D['rows'] if r['chapter']=='LXXX_NAVIGATION_ONLY']),2)
  self.assertIn('1646/7',D['rows'][-1]['historical_author_paraphrase'])
 def test_six_original_denial_factors_not_pooled(self):
  t=' '.join(r['historical_author_paraphrase'] for r in D['rows'])
  for s in ('conjunction','Moon aspect','translates','collects','reception','Saturn','Mercury'):
   self.assertIn(s,t)
 def test_posthoc_outcomes_and_hidden_informer_unverified(self):
  self.assertEqual(C['source_author_self_reported_failure_outcome'],1)
  self.assertEqual(C['independent_authenticated_outcomes'],0)
  self.assertEqual(C['independent_predictions_validated'],0)
  t=' '.join(r['historical_author_paraphrase'] for r in D['rows'])
  self.assertIn('never discovered',t)
  self.assertIn('hypothetical culprit',t)
  self.assertEqual(len(U['issues']),17)
 def test_mutant_double_count_detected(self):
  s=copy.deepcopy(M['source_spans']);s[0]['mapped_local_ids'].append(s[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],s)
 def test_mutant_next_chapter_leak_detected(self):
  r=copy.deepcopy(D['rows']);r[-1]['chapter']='LXXIX'
  with self.assertRaises(AssertionError):check(r,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
