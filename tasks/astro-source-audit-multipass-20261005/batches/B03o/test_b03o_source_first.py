import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
def valid(rs,spans):
 assert len(rs)==31 and len(spans)==12
 ids=[r['local_id'] for r in rs]
 assert ids==[f'LXIX-C{i:03}' for i in range(1,32)]
 mapped=[x for s in spans for x in s['mapped_local_ids']]
 assert len(mapped)==31 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rs[ids.index(k)]['original_pdf_pages']
  for s in spans for k in s['mapped_local_ids'])
 assert all(r['printed_pages']==[n-34 for n in r['original_pdf_pages']] for r in rs)
 assert all(r['global_record_number'] is None and not r['historical_documentary_admitted']
  and not r['independent_danger_outcome_verified']
  and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rs)
 assert all(r['chapter']=='LXIX' and r['original_pdf_pages']==[448] for r in rs[:-1])
 assert rs[-1]['chapter']=='LXX_NAVIGATION_ONLY' and rs[-1]['original_pdf_pages']==[449]
class OriginalSource(unittest.TestCase):
 def test_bidirectional_map(self):valid(D['rows'],M['source_spans'])
 def test_original_scans(self):
  self.assertEqual(W['source_body_pdf_pages'],[448])
  for im in W['original_images']:
   raw=(B/im['path']).read_bytes()
   self.assertEqual(len(raw),im['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),im['sha256'])
 def test_original_identity_and_counts(self):
  self.assertEqual(W['previous_accepted_lilly'],3976)
  self.assertEqual(M['span_count'],12)
  self.assertEqual(len(U['issues']),14)
  self.assertEqual(C['empirically_validated_predictions'],0)
 def test_mutated_duplicate_rejected(self):
  x=copy.deepcopy(M['source_spans']);x[0]['mapped_local_ids'].append(x[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D['rows'],x)
 def test_mutated_wrong_page_rejected(self):
  x=copy.deepcopy(D['rows']);x[3]['original_pdf_pages']=[449]
  with self.assertRaises(AssertionError):valid(x,M['source_spans'])
 def test_mutated_empirical_label_rejected(self):
  x=copy.deepcopy(D['rows']);x[5]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):valid(x,M['source_spans'])
 def test_next_chapter_not_swallowed(self):
  x=copy.deepcopy(D['rows']);x[-1]['chapter']='LXIX'
  with self.assertRaises(AssertionError):valid(x,M['source_spans'])
 def test_important_semantic_separation(self):
  t=' '.join(r['historical_author_paraphrase']+' '+r['source_conditions_and_limits'] for r in D['rows']).lower()
  for q in ('accus','rumor','midheaven','reception','benefic','first lord'):
   self.assertIn(q,t)
 def test_source_authority_has_no_case(self):
  self.assertEqual(C['independently_verified_risk_outcomes'],0)
  self.assertEqual(C['globally_admitted_new_records'],0)
if __name__=='__main__':unittest.main(verbosity=2)
