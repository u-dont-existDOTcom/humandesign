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
 assert len(rows)==40 and len(spans)==10
 ids=[r['local_id'] for r in rows]
 assert ids==[f'LXV-C{i:03}' for i in range(1,41)]
 mapped=[id for sp in spans for id in sp['mapped_local_ids']]
 assert len(mapped)==40 and sorted(mapped)==sorted(ids)
 assert all(sp['original_pdf_pages']==rows[ids.index(i)]['original_pdf_pages'] for sp in spans for i in sp['mapped_local_ids'])
 assert all(r['global_record_number'] is None and not r['historically_admitted'] and
  not r['source_case_independently_authenticated'] and
  not r['empirical_astrological_prediction_validated'] and
  not r['runtime_rule_promoted'] for r in rows)
 assert all(r['original_printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter']=='LXV' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXVI_NAVIGATION_ONLY'
class SourceFirst(unittest.TestCase):
 def test_reverse_bijection(self):
  valid(D['rows'],M['source_spans'])
  self.assertEqual(O['ordered_local_ids'],[r['local_id'] for r in D['rows']])
 def test_original_images(self):
  self.assertEqual(W['source_body_pdf_pages'],[433,434])
  for x in W['original_page_images']:
   raw=(B/x['path']).read_bytes()
   self.assertEqual(len(raw),x['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x['sha256'])
 def test_original_chronology(self):
  self.assertEqual(W['chart_original_date'],'29 March 1644')
  self.assertEqual(W['chart_original_time'],'10:12 AM')
  self.assertEqual(W['prior_accepted_lilly'],3630)
 def test_claim_cannot_be_scored_as_hourly_accuracy(self):
  text=' '.join(r['historical_author_claim_paraphrase']+' '+r['source_conditions_and_limitations'] for r in D['rows']).lower()
  self.assertIn('11–12 hours',text)
  self.assertIn('exact arrival hour',text)
  self.assertEqual(C['independently_time_verified_11_to_12_hour_news_predictions'],0)
 def test_incomplete_victory_qualifier(self):
  t=' '.join(r['historical_author_claim_paraphrase'] for r in D['rows']).lower()
  self.assertIn('incomplete',t)
  self.assertIn('ammunition',t)
 def test_original_limits(self):
  self.assertEqual(len(U['issues']),18)
  self.assertEqual(C['new_empirically_validated_astrology_predictions'],0)
  self.assertEqual(C['new_accepted_historical_records'],0)
 def test_cross_page_and_next_heading(self):
  self.assertEqual([s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1],[[433,434]])
  self.assertEqual(D['rows'][-1]['chapter'],'LXVI_NAVIGATION_ONLY')
 def test_duplicate_mapping_mutant_rejected(self):
  sp=copy.deepcopy(M['source_spans'])
  sp[0]['mapped_local_ids'].append(sp[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D['rows'],sp)
 def test_false_empirical_label_mutant_rejected(self):
  r=copy.deepcopy(D['rows'])
  r[8]['empirical_astrological_prediction_validated']=True
  with self.assertRaises(AssertionError):valid(r,M['source_spans'])
 def test_wrong_navigation_mutant_rejected(self):
  r=copy.deepcopy(D['rows'])
  r[-1]['chapter']='LXV'
  with self.assertRaises(AssertionError):valid(r,M['source_spans'])
 def test_wrong_page_mutant_rejected(self):
  r=copy.deepcopy(D['rows'])
  r[4]['original_pdf_pages']=[434]
  with self.assertRaises(AssertionError):valid(r,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
