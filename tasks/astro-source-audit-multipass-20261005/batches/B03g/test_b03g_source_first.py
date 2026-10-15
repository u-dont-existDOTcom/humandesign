import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
O=J('SOURCE_ORDER_DRAFT.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
def inspect(rows,spans):
 assert len(rows)==35 and len(spans)==15
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LXI-C{i:03}' for i in range(1,36)]
 mapped=[id for s in spans for id in s['mapped_source_local_ids']]
 assert sorted(mapped)==sorted(ids) and len(mapped)==35
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages']
    for s in spans for k in s['mapped_source_local_ids'])
 assert all(r['global_record_number'] is None and
            not r['historical_documentation_admitted'] and
            not r['real_outcome_independently_authenticated'] and
            not r['empirical_astrology_prediction_validated'] and
            not r['runtime_model_promoted'] for r in rows)
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(set(r['original_pdf_pages']).issubset({424,425,426}) for r in rows)
 assert all(r['chapter']=='LXI' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXII_NAVIGATION_ONLY'
 assert sum(r['role']=='source_internal_reported_outcome' for r in rows)==1
 assert sum(r['role']=='limitation' for r in rows)>=1
 return True
class SourceFirst(unittest.TestCase):
 def test_source_record_bidirectional_mapping(self):
  self.assertTrue(inspect(D['rows'],M['source_spans']))
  self.assertEqual(O['ordered_local_ids'],[r['source_local_id'] for r in D['rows']])
 def test_document_full_identity(self):
  self.assertEqual(W['source_full_pdf_sha256'],
   '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
  self.assertEqual(W['source_body_pdf_pages'],[424,425,426])
 def test_every_original_image_hash(self):
  for x in W['original_images']:
   b=(B/x['path']).read_bytes()
   self.assertEqual(len(b),x['bytes'])
   self.assertEqual(hashlib.sha256(b).hexdigest(),x['sha256'])
 def test_original_chapter_boundary(self):
  self.assertIn('BELOW',W['opening'])
  self.assertIn('ABOVE',W['closing'])
  self.assertEqual(D['rows'][-1]['original_pdf_pages'],[426])
  self.assertEqual(D['rows'][-1]['chapter'],'LXII_NAVIGATION_ONLY')
 def test_figure_semantic_directions(self):
  t=' '.join(r['historical_author_report_paraphrase'] for r in D['rows']).lower()
  for term in ['mars','mercury','moon','gemini','aquarius','west',
   'trine','second house','kingston','friday','cancer']:
   self.assertIn(term,t,term)
 def test_author_uncertainty_and_distance_preserved(self):
  t=' '.join(r['historical_author_report_paraphrase'] for r in D['rows']).lower()
  self.assertIn('which if true',t)
  self.assertIn('three or four houses',t)
  self.assertIn('one or two days',t)
  self.assertIn('consultation date',' '.join(r['conditions_source_limits_or_chronology'] for r in D['rows']).lower())
 def test_author_report_never_empirical(self):
  self.assertFalse(W['source_outcome_independently_authenticated'])
  self.assertEqual(C['source_internal_servant_return_reports'],1)
  self.assertEqual(C['empirical_predictions_validated'],0)
  self.assertEqual(C['independently_verified_return_cases'],0)
  self.assertEqual(C['globally_accepted_new_source_units'],0)
 def test_uncertainty_count(self):
  self.assertEqual(len(U['issues']),16)
  self.assertEqual(M['span_count'],15)
  self.assertEqual(len(O['cross_page_ids']),2)
 def test_mutant_duplicate_mapping(self):
  bad=copy.deepcopy(M['source_spans'])
  bad[0]['mapped_source_local_ids'].append(bad[1]['mapped_source_local_ids'][0])
  with self.assertRaises(AssertionError):inspect(D['rows'],bad)
 def test_mutant_wrong_page(self):
  bad=copy.deepcopy(D['rows']);bad[5]['original_pdf_pages']=[426]
  with self.assertRaises(AssertionError):inspect(bad,M['source_spans'])
 def test_mutant_false_validation(self):
  bad=copy.deepcopy(D['rows']);bad[15]['real_outcome_independently_authenticated']=True
  with self.assertRaises(AssertionError):inspect(bad,M['source_spans'])
 def test_mutant_different_chapter(self):
  bad=copy.deepcopy(D['rows']);bad[-1]['chapter']='LXI'
  with self.assertRaises(AssertionError):inspect(bad,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
