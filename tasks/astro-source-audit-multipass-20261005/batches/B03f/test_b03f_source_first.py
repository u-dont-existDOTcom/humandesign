import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
O=J('SOURCE_ORDER_DRAFT.json')
def check(rows,spans):
 assert len(rows)==31 and len(spans)==13
 keys=[x['source_local_id'] for x in rows]
 assert keys==[f'LX-C{i:03}' for i in range(1,32)]
 mapped=[k for x in spans for k in x['mapped_source_local_ids']]
 assert len(mapped)==31 and sorted(mapped)==sorted(keys)
 assert all(x['original_pdf_pages']==rows[keys.index(k)]['original_pdf_pages'] for x in spans for k in x['mapped_source_local_ids'])
 assert all(r['global_record_number'] is None and r['original_scan_is_authority'] and
  not r['historical_documentation_admitted'] and not r['empirical_astrology_prediction_validated'] and
  not r['is_independently_blinded_case'] and not r['real_outcome_independently_authenticated'] and
  not r['runtime_model_promoted'] for r in rows)
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(set(r['original_pdf_pages']).issubset({423,424}) for r in rows)
 assert all(x['chapter']=='LX' for x in rows[:-1])
 assert rows[-1]['chapter']=='LXI_NAVIGATION_ONLY'
class SourceFirst(unittest.TestCase):
 def test_bijection(self):
  check(D['rows'],M['source_spans'])
  self.assertEqual(O['ordered_local_ids'],[r['source_local_id'] for r in D['rows']])
 def test_historical_pdf_hash(self):
  self.assertEqual(W['source_full_pdf_sha256'],
   '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_original_images(self):
  for x in W['original_images']:
   p=B/x['path']
   self.assertEqual(p.stat().st_size,x['size_bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['sha256'])
 def test_page_boundary(self):
  self.assertEqual(W['source_body_pdf_pages'],[423,424])
  self.assertEqual(D['rows'][-1]['original_pdf_pages'],[424])
  self.assertEqual([r['chapter'] for r in D['rows'] if r['role']=='next_chapter_boundary'],['LXI_NAVIGATION_ONLY'])
 def test_case_chronology(self):
  t=' '.join(r['historical_author_report_paraphrase'] for r in D['rows'])
  self.assertIn('11 June 1646',t)
  self.assertIn('10:38 AM',t)
  self.assertIn('distinct worked horary',t)
 def test_conditional_aspect_polarity(self):
  t=' '.join(r['historical_author_report_paraphrase'] for r in D['rows'])
  for keyword in ['separating from a square','via a trine','semisextile','retrograde']:
   self.assertIn(keyword,t.lower())
 def test_non_empirical_limits(self):
  self.assertEqual(len(U['issues']),13)
  self.assertFalse(W['case_independently_authenticated'])
  self.assertEqual(C['new_empirically_validated_astrology_predictions'],0)
  self.assertEqual(C['source_internal_reported_positive_outcome_count'],1)
 def test_mutation_double_mapping(self):
  x=copy.deepcopy(M['source_spans'])
  x[0]['mapped_source_local_ids'].append(x[1]['mapped_source_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],x)
 def test_mutation_wrong_chapter(self):
  x=copy.deepcopy(D['rows']);x[-1]['chapter']='LX'
  with self.assertRaises(AssertionError):check(x,M['source_spans'])
 def test_mutation_empirical_claim(self):
  x=copy.deepcopy(D['rows']);x[4]['empirical_astrology_prediction_validated']=True
  with self.assertRaises(AssertionError):check(x,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
