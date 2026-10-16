import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
O=J('SOURCE_ORDER_DRAFT.json')
FOLIO={463:429,464:431,465:430,466:432}
def valid(rows,spans):
 assert len(rows)==61 and len(spans)==16
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LXXV-C{i:03}' for i in range(1,62)]
 mapping=[x for s in spans for x in s['mapped_local_ids']]
 assert len(mapping)==61 and sorted(mapping)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages']
  for s in spans for k in s['mapped_local_ids'])
 assert all(s['printed_page_numerals_as_imprinted']==[FOLIO[n] for n in s['original_pdf_pages']] for s in spans)
 assert all(r['printed_page_numerals_as_physically_imprinted']==[FOLIO[n] for n in r['original_pdf_pages']] for r in rows)
 assert all(r['global_record_number'] is None and
   not r['historical_documentary_accepted'] and
   not r['individual_case_independently_verified'] and
   not r['empirical_forecast_validated'] and
   not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXV' for r in rows[:-2])
 assert all(r['chapter']=='LXXVI_NAVIGATION_ONLY' for r in rows[-2:])
 assert [s['original_pdf_pages'][0] for s in spans]==sorted(s['original_pdf_pages'][0] for s in spans)
 return True
class OriginalSource(unittest.TestCase):
 def test_bijective_reverse_source_map(self):
  self.assertTrue(valid(D['rows'],M['source_spans']))
  self.assertEqual(O['ordered_local_ids'],[r['source_local_id'] for r in D['rows']])
 def test_exact_historical_original_images(self):
  self.assertEqual(W['original_scan_order'],[463,464,465,466])
  for i in W['original_images']:
   raw=(B/i['path']).read_bytes()
   self.assertEqual(len(raw),i['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256'])
 def test_folio_misnumbering_not_scan_misorder(self):
  self.assertEqual(W['original_imprinted_page_numerals'],[429,431,430,432])
  self.assertEqual(W['original_scan_order'],[463,464,465,466])
  self.assertEqual(D['original_scan_text_order'],[463,464,465,466])
  self.assertIn('Do not reorder scans',W['imprinted_folio_transposition'])
 def test_original_scope_and_next_boundary(self):
  self.assertEqual(W['previous_lilly_accepted'],4323)
  self.assertEqual(W['next_chapter'],'LXXVI')
  self.assertEqual(W['next_chapter_pdf'],466)
  self.assertEqual(D['source_original_full_pdf_sha256'],
    '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_unnumbered_sections_not_omitted(self):
  anchors=[r['short_source_anchor_not_diplomatic'].lower() for r in D['rows'] if r['role']=='subheading']
  for s in ('science cunning','persons absent','part of heaven'):
   self.assertTrue(any(s in a for a in anchors),anchors)
 def test_cross_page_seams(self):
  pairs=[s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1]
  self.assertEqual(pairs,[[463,464],[464,465],[465,466]])
  self.assertEqual(len(O['page_crossing_local_ids']),len([r for r in D['rows'] if len(r['original_pdf_pages'])>1]))
 def test_historical_only_no_person_cases(self):
  self.assertEqual(C['separately_verified_competency_cases'],0)
  self.assertEqual(C['separately_verified_traveler_cases'],0)
  self.assertEqual(C['separately_verified_economic_outcomes'],0)
  self.assertEqual(C['empirically_validated_astrology_predictions'],0)
  self.assertEqual(len(U['issues']),20)
 def test_differentiates_skill_gain_travel(self):
  t=' '.join(r['historical_author_paraphrase']+' '+r['source_conditions_uncertainty'] for r in D['rows']).lower()
  for s in ('useful','knowledge','second','eighth','west','moon','person'):
   self.assertIn(s,t)
 def test_mutation_duplicate_source_rejected(self):
  sp=copy.deepcopy(M['source_spans']);sp[0]['mapped_local_ids'].append(sp[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D['rows'],sp)
 def test_mutation_false_pagination_rejected(self):
  rs=copy.deepcopy(D['rows']);rs[20]['printed_page_numerals_as_physically_imprinted']=[430]
  with self.assertRaises(AssertionError):valid(rs,M['source_spans'])
 def test_mutation_false_forecast_rejected(self):
  rs=copy.deepcopy(D['rows']);rs[33]['empirical_forecast_validated']=True
  with self.assertRaises(AssertionError):valid(rs,M['source_spans'])
 def test_mutation_next_chapter_swallowed_rejected(self):
  rs=copy.deepcopy(D['rows']);rs[-1]['chapter']='LXXV'
  with self.assertRaises(AssertionError):valid(rs,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
