"""Original 1647 Lilly Chapter LVI source-first documentary checks; not efficacy tests."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
L=J('CLAIM_LEDGER.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
S=J('SOURCE_ORDER_DRAFT.json')
def validate(rows,spans):
 assert len(rows)==45 and len(spans)==19
 ids=[r['local_id'] for r in rows]
 assert ids==[f'LVI-C{i:03}' for i in range(1,46)]
 maps=[i for s in spans for i in s['local_source_ids']]
 assert sorted(maps)==sorted(ids) and len(maps)==len(ids)
 byid={r['local_id']:r for r in rows}
 assert all(byid[i]['original_pdf_pages']==s['original_pdf_pages']
            for s in spans for i in s['local_source_ids'])
 assert all(r['global_record_number'] is None and r['source_first_provisional']
            and not r['admitted_as_historical_documentation']
            and not r['validated_by_real_world_cases']
            and not r['runtime_predicate_active']
            and not r['real_world_military_use_authorized']
            and not r['complete_diplomatic_transcription'] for r in rows)
 assert all(r['original_pdf_pages'] in ([413],[414],[413,414]) for r in rows)
 assert all(r['original_printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter']=='LVI' for r in rows[:-1])
 assert rows[-1]['chapter']=='LVII_HEADING_NAVIGATION_ONLY'
 assert rows[-1]['role']=='next_heading_boundary'
 assert rows[0]['role']=='heading'
 assert len([r for r in rows if len(r['original_pdf_pages'])>1])>=5
 return True
class SourceFirst(unittest.TestCase):
 def test_source_order_bijection(self):
  self.assertTrue(validate(D['rows'],C['source_spans']))
  self.assertEqual(S['ordered_local_ids'],[r['local_id'] for r in D['rows']])
  self.assertEqual([s['span_id'] for s in C['source_spans']],
     [f'LVI-S{i:03}' for i in range(1,20)])
 def test_source_images_original(self):
  self.assertEqual([x['original_pdf_page'] for x in W['images']],[413,414])
  self.assertEqual([x['printed_page'] for x in W['images']],[379,380])
  for f in W['images']:
   p=B/f['path']
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),f['sha256'])
   self.assertEqual(p.stat().st_size,f['bytes'])
  self.assertEqual(W['complete_original_pdf_sha256'],
      '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_source_boundaries_and_no_runtime(self):
  self.assertEqual(W['prior_accepted_lilly'],3203)
  self.assertIn('below Chapter LV divider',W['first_position'])
  self.assertIn('above Chapter LVII divider',W['end_position'])
  self.assertFalse(W['full_original_pdf_repacked'])
  self.assertEqual(L['new_canonical_lilly'],0)
  self.assertEqual(L['new_empirical_siege_forecasts'],0)
  self.assertEqual(L['new_runtime_predicate_promotions'],0)
 def test_qualifier_integrity(self):
  txt=' '.join(' '.join([r['original_source_abbreviated_anchor_not_full_quote'],r['historical_author_assertion_paraphrase'],r['predicates_and_caveats']]) for r in D['rows']).lower()
  for needle in ['reception','twelve','twelfth','eighth','sixth','exception',
    'retrograde','combustion','fallback','cusp','orb','historic']:
   if needle!='twelve':self.assertIn(needle,txt)
  self.assertTrue(any('without reciprocal reception' in r['historical_author_assertion_paraphrase']
       for r in D['rows']))
  self.assertTrue(any('not be taken' in r['historical_author_assertion_paraphrase']
       for r in D['rows']))
  self.assertTrue(any('will not be taken' in r['historical_author_assertion_paraphrase']
       for r in D['rows']))
 def test_not_overinterpreted(self):
  self.assertEqual(len(U['issues']),17)
  self.assertFalse(D['independent_full_diplomatic_transcription_claimed'])
  self.assertEqual(sum(r['role']=='unresolved_symbol' for r in D['rows']),1)
  self.assertEqual(sum(r['role']=='margin' for r in D['rows']),1)
  self.assertEqual(sum(r['role']=='next_heading_boundary' for r in D['rows']),1)
  self.assertGreaterEqual(sum(r['role']=='exception' for r in D['rows']),2)
 def test_mutant_double_mapping_fails(self):
  spans=copy.deepcopy(C['source_spans'])
  spans[0]['local_source_ids'].append(spans[1]['local_source_ids'][0])
  with self.assertRaises(AssertionError):validate(D['rows'],spans)
 def test_mutant_wrong_chapter_fails(self):
  rows=copy.deepcopy(D['rows']);rows[-1]['chapter']='LVI'
  with self.assertRaises(AssertionError):validate(rows,C['source_spans'])
 def test_mutant_unsupported_empirical_promotion_fails(self):
  rows=copy.deepcopy(D['rows']);rows[15]['validated_by_real_world_cases']=True
  with self.assertRaises(AssertionError):validate(rows,C['source_spans'])
 def test_mutant_false_page_fails(self):
  rows=copy.deepcopy(D['rows']);rows[12]['original_pdf_pages']=[415]
  with self.assertRaises(AssertionError):validate(rows,C['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
