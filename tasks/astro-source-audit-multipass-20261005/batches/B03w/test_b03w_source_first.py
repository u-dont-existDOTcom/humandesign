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
def valid(rows,spans):
 assert len(rows)==38 and len(spans)==8
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LXXVII-C{i:03}' for i in range(1,39)]
 mapped=[k for s in spans for k in s['mapped_local_ids']]
 assert len(mapped)==38 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages'] for s in spans for k in s['mapped_local_ids'])
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['global_record_number'] is None and not r['historical_documentary_accepted']
  and not r['independently_authenticated_dream_case']
  and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rows)
 assert 'Bonatus better than Haly' in rows[1]['historical_author_paraphrase']
 assert 'Al-Kindi' not in rows[1]['historical_author_paraphrase']
 assert all(r['chapter']=='LXXVII' for r in rows[:-2])
 assert all(r['chapter']=='LXXVIII_NAVIGATION_ONLY' for r in rows[-2:])
class OriginalSource(unittest.TestCase):
 def test_bidirectional_source_map(self):
  valid(D['rows'],M['source_spans'])
  self.assertEqual(O['ordered_ids'],[r['source_local_id'] for r in D['rows']])
 def test_original_witness_image_hashes(self):
  self.assertEqual(len(W['original_images']),3)
  for f in W['original_images']:
   raw=(B/f['path']).read_bytes()
   self.assertEqual(len(raw),f['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),f['sha256'])
 def test_original_boundary_and_previous_baseline(self):
  self.assertEqual(W['previous_accepted_lilly'],4446)
  self.assertEqual(W['original_body_pdf_pages'],[468,469])
  self.assertEqual(W['following_heading_pdf'],470)
  self.assertEqual(W['next_numbered_chapter'],'LXXVIII')
 def test_cross_page_mapping(self):
  self.assertEqual([s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1],[[468,469]])
  self.assertEqual(len(O['next_heading_navigation_only']),2)
 def test_house_specific_claims_separate(self):
  t=' '.join(r['historical_author_paraphrase']+' '+r['original_source_qualifications'] for r in D['rows']).lower()
  for s in ('ninth','first','second','tenth','saturn','dream','financial','harm'):
   self.assertIn(s,t,s)
 def test_limits_and_no_case_validation(self):
  self.assertEqual(len(U['issues']),15)
  self.assertEqual(C['independently_authenticated_dream_events'],0)
  self.assertEqual(C['independently_validated_predictive_outcomes'],0)
 def test_duplicate_mapping_mutant(self):
  sp=copy.deepcopy(M['source_spans']);sp[0]['mapped_local_ids'].append(sp[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D['rows'],sp)
 def test_false_prediction_mutant(self):
  rs=copy.deepcopy(D['rows']);rs[7]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):valid(rs,M['source_spans'])
 def test_next_chapter_leak_mutant(self):
  rs=copy.deepcopy(D['rows']);rs[-1]['chapter']='LXXVII'
  with self.assertRaises(AssertionError):valid(rs,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
