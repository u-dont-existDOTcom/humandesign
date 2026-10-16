import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
O=J('SOURCE_ORDER_DRAFT.json')
def check(rows,spans):
 assert len(rows)==153 and len(spans)==28
 ids=[r['local_id'] for r in rows]
 assert ids==[f'LXXIV-C{i:03}' for i in range(1,154)]
 mapped=[k for s in spans for k in s['mapped_local_ids']]
 assert len(mapped)==153 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages']
  for s in spans for k in s['mapped_local_ids'])
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['global_record_number'] is None and not r['historical_documentary_accepted']
   and not r['independently_authenticated_case_outcome']
   and not r['empirically_validated_prediction']
   and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXIV' for r in rows[:-2])
 assert all(r['chapter']=='LXXV_NAVIGATION_ONLY' for r in rows[-2:])
 assert set(p for s in spans for p in s['original_pdf_pages'])==set(range(456,464))
 assert [s['original_pdf_pages'][0] for s in spans]==sorted(s['original_pdf_pages'][0] for s in spans)
 return True
class SourceFirst(unittest.TestCase):
 def test_original_to_source_bijection(self):
  self.assertTrue(check(D['rows'],M['source_spans']))
  self.assertEqual(O['ordered_local_ids'],[r['local_id'] for r in D['rows']])
 def test_all_primary_image_hashes(self):
  self.assertEqual(len(W['original_images']),8)
  for x in W['original_images']:
   body=(B/x['path']).read_bytes()
   self.assertEqual(len(body),x['bytes'])
   self.assertEqual(hashlib.sha256(body).hexdigest(),x['sha256'])
 def test_original_source_and_boundary(self):
  self.assertEqual(W['previous_accepted_lilly'],4170)
  self.assertEqual(W['original_body_pdf_pages'],list(range(456,464)))
  self.assertEqual(W['next_chapter'],'LXXV')
  self.assertEqual(W['next_chapter_pdf_page'],463)
  self.assertEqual(W['source_original_full_pdf_sha256'],
    '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_six_original_page_seams(self):
  crosses=[s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1]
  self.assertEqual(crosses,[[456,457],[457,458],[458,459],[459,460],[460,461],[462,463]])
 def test_preserve_subsections(self):
  heads=[r['short_anchor_not_diplomatic'].lower() for r in D['rows'] if r['role']=='subheading']
  for topic in ('voyage','wind','return','journey','length','letter'):
   t=' '.join(r['historical_author_paraphrase']+' '+r['short_anchor_not_diplomatic']
     for r in D['rows']).lower()
   self.assertIn(topic,t)
 def test_no_verified_real_outcome(self):
  self.assertEqual(C['source_author_reported_concrete_journey_cases'],0)
  self.assertEqual(C['independently_authenticated_journey_cases'],0)
  self.assertEqual(C['independently_authenticated_wind_or_weather_cases'],0)
  self.assertEqual(C['new_empirically_validated_predictions'],0)
  self.assertEqual(len(U['issues']),32)
 def test_mutant_wrong_source_page(self):
  rs=copy.deepcopy(D['rows']);rs[10]['original_pdf_pages']=[457]
  with self.assertRaises(AssertionError):check(rs,M['source_spans'])
 def test_mutant_duplicate_source_map(self):
  sp=copy.deepcopy(M['source_spans']);sp[0]['mapped_local_ids'].append(sp[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],sp)
 def test_mutant_false_independent_forecast(self):
  rs=copy.deepcopy(D['rows']);rs[41]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(rs,M['source_spans'])
 def test_mutant_next_chapter_swallowed(self):
  rs=copy.deepcopy(D['rows']);rs[-1]['chapter']='LXXIV'
  with self.assertRaises(AssertionError):check(rs,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
