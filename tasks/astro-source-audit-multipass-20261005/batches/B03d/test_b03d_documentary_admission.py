"""Guarded source-to-documentary transformation checks."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED.json')
A=J('ACCEPTANCE.json')
def valid(rows):
 assert len(rows)==38
 assert [r['record_number'] for r in rows]==list(range(3323,3361))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3323,3361)]
 assert [r['source_local_id'] for r in rows]==[f'LVIII-C{i:03}' for i in range(1,39)]
 assert all(r['historical_documentation_accepted'] and not r['empirical_predictive_validation']
  and not r['active_personality_or_honesty_classifier'] and r['observed_real_adversary_cases']==0
  and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LVIII' for r in rows[:-1])
 assert rows[-1]['chapter']=='LIX_HEADING_ONLY'
 return True
class Admission(unittest.TestCase):
 def test_contiguous_source_numbering(self):self.assertTrue(valid(R['rules']))
 def test_original_draft_byte_meaning(self):
  for a,b in zip(D['rows'],R['rules'],strict=True):
   for key in ['source_local_id','role','source_short_anchor_not_diplomatic',
               'historical_claim_paraphrase','conditions_and_limits','original_pdf_pages']:
    self.assertEqual(a[key],b[key])
 def test_reverse_map_total_no_duplicate(self):
  ids=[i for s in M['source_spans'] for i in s['canonical_record_ids']]
  self.assertEqual(len(ids),38)
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R['rules']))
 def test_image_source_and_rules_hash(self):
  for v in W['images']:self.assertEqual(H(v['relative_path']),v['sha256'])
  for n,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
  ('UNRESOLVED.json','unresolved_sha256'),
  ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256')]:
   self.assertEqual(H(n),A[k])
 def test_predecessor_and_limits(self):
  self.assertEqual((A['previous_accepted_lilly'],A['lilly_if_published'],
                    A['combined_if_published']),(3322,3360,4426))
  self.assertEqual(len(U['issues']),14)
  self.assertFalse(A['canonical_publication_verified'])
 def test_no_model_or_behavior_prediction(self):
  self.assertEqual(R['authenticated_person_level_adversary_observations'],0)
  self.assertEqual(R['new_predictive_accuracy_validation'],0)
  self.assertEqual(R['runtime_model_promotions'],0)
 def test_mutant_invalidity(self):
  r=copy.deepcopy(R['rules']);r[0]['record_number']=0
  with self.assertRaises(AssertionError):valid(r)
  r=copy.deepcopy(R['rules']);r[10]['empirical_predictive_validation']=True
  with self.assertRaises(AssertionError):valid(r)
  r=copy.deepcopy(R['rules']);r[-1]['chapter']='LVIII'
  with self.assertRaises(AssertionError):valid(r)
if __name__=='__main__':unittest.main(verbosity=2)
