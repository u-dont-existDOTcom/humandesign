import hashlib,json,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED.json')
def validate(rs):
 assert len(rs)==40
 assert [r['record_number'] for r in rs]==list(range(3631,3671))
 assert [r['id'] for r in rs]==[f'R{i}' for i in range(3631,3671)]
 assert all(r['historically_admitted'] and not r['source_case_independently_authenticated']
   and not r['empirical_astrological_prediction_validated']
   and not r['runtime_rule_promoted'] for r in rs)
 assert all(r['chapter']=='LXV' for r in rs[:-1])
 assert rs[-1]['chapter']=='LXVI_NAVIGATION_ONLY'
class Admission(unittest.TestCase):
 def test_contiguous_documentary_units(self):validate(R)
 def test_original_source_text_not_changed(self):
  for d,r in zip(D,R,strict=True):
   for k in ('local_id','role','original_pdf_pages','historical_author_claim_paraphrase',
    'source_conditions_and_limitations'):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d['global_record_number'])
 def test_source_to_documentary_map(self):
  ids=[i for sp in M['source_spans'] for i in sp['canonical_record_ids']]
  self.assertEqual(len(ids),40)
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],10)
 def test_original_source_page_hashes(self):
  for im in W['original_page_images']:
   raw=(B/im['path']).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),im['sha256'])
   self.assertEqual(len(raw),im['bytes'])
 def test_source_receipt_hashes(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_map_sha256')]:
   self.assertEqual(H(f),A[k])
 def test_historical_timing_cannot_be_scored(self):
  self.assertEqual(A['historical_favorable_battle_reported_cases'],1)
  self.assertEqual(A['independent_letter_arrival_time_evidence'],0)
  self.assertEqual(A['independently_authenticated_battle_outcomes'],0)
  self.assertFalse(A['eleven_to_twelve_hour_claim_empirically_verified'])
  self.assertTrue(A['complete_victory_not_unqualified'])
 def test_new_source_boundary(self):
  self.assertEqual(A['previous_lilly_accepted'],3630)
  self.assertEqual(A['new_documentary_records'],40)
  self.assertEqual(A['lilly_if_published'],3670)
  self.assertEqual(A['combined_if_published'],4736)
  self.assertEqual(len(U['issues']),18)
  self.assertFalse(A['remote_published'])
 def test_mutations_rejected(self):
  bad=copy.deepcopy(R);bad[5]['empirical_astrological_prediction_validated']=True
  with self.assertRaises(AssertionError):validate(bad)
  bad=copy.deepcopy(R);bad[-1]['chapter']='LXV'
  with self.assertRaises(AssertionError):validate(bad)
  bad=copy.deepcopy(R);bad[3]['record_number']=0
  with self.assertRaises(AssertionError):validate(bad)
if __name__=='__main__':unittest.main(verbosity=2)
