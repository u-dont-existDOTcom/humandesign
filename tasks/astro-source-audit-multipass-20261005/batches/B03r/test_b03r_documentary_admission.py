import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
def check(rs):
 assert len(rs)==43
 assert [r['record_number'] for r in rs]==list(range(4094,4137))
 assert [r['id'] for r in rs]==[f'R{i}' for i in range(4094,4137)]
 assert all(r['historical_documentary_accepted'] and
  not r['prospective_astrology_prediction_validated'] and not r['runtime_rule_promoted'] for r in rs)
 assert all(r['chapter']=='LXXII' for r in rs[:-1])
 assert rs[-1]['chapter']=='LXXIII_NAVIGATION_ONLY'
class Admission(unittest.TestCase):
 def test_source_global_ids(self):check(R)
 def test_original_source_transformation_preserves_meaning(self):
  for orig,accepted in zip(D,R,strict=True):
   for k in ('source_local_id','role','original_pdf_pages',
    'historical_author_paraphrase','limits_and_attribution'):
    self.assertEqual(orig[k],accepted[k])
   self.assertIsNone(orig['global_record_number'])
 def test_reverse_map_unique(self):
  ids=[x for s in M['source_spans'] for x in s['accepted_record_ids']]
  self.assertEqual(len(ids),43)
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],11)
 def test_accepted_hash_receipts(self):
  for n,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
   ('UNRESOLVED.json','limits_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','audit_sha256')]:
   self.assertEqual(H(n),A[k])
 def test_historical_event_not_independent_prediction(self):
  self.assertTrue(A['independent_event_confirmed'])
  self.assertFalse(A['independent_forecast_confirmed'])
  self.assertEqual(A['empirically_validated_predictions'],0)
  self.assertEqual(A['previous_lilly'],4093)
  self.assertEqual(A['new_documentary_records'],43)
  self.assertEqual(A['combined_if_published'],5202)
 def test_mutants(self):
  rs=copy.deepcopy(R);rs[5]['prospective_astrology_prediction_validated']=True
  with self.assertRaises(AssertionError):check(rs)
  rs=copy.deepcopy(R);rs[-1]['chapter']='LXXII'
  with self.assertRaises(AssertionError):check(rs)
if __name__=='__main__':unittest.main(verbosity=2)
