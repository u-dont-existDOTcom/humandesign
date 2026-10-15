import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
SHA=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def check(rs):
 assert len(rs)==24
 assert [r['record_number'] for r in rs]==list(range(3148,3172))
 assert [r['id'] for r in rs]==[f'R{i}' for i in range(3148,3172)]
 assert [r['local_id'] for r in rs]==[f'LIV-C{i:03}' for i in range(1,25)]
 assert all(r['accepted_historical_documentary'] and not r['is_provisional']
  and not r['empirically_verified_case'] and not r['safe_for_real_person_prognosis']
  and not r['model_runtime_promotion'] for r in rs)
 assert all(x['chapter']=='LIV' for x in rs[:-1])
 assert rs[-1]['chapter']=='LV_HEADING_NAVIGATION_ONLY'
 return True
class Acceptance(unittest.TestCase):
 def test_contiguous_source_units(self):
  self.assertTrue(check(R['rules']))
  self.assertEqual(R['record_count'],24)
  self.assertEqual(R['source_reverse_passages'],16)
 def test_earlier_draft_preserved(self):
  for a,b in zip(D['rows'],R['rules'],strict=True):
   for k in ('local_id','source_statement_paraphrase',
       'source_anchor_editorial_abbreviation',
       'source_predicates_and_qualifiers',
       'original_pdf_pages','record_role'):
    self.assertEqual(a[k],b[k])
  self.assertEqual(D['rows'][-1]['global_record_number'],None)
 def test_reverse_source_to_rule_mapping(self):
  ids=[i for s in M['source_spans'] for i in s['canonical_record_ids']]
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R['rules']))
  self.assertEqual(len(ids),24)
  self.assertEqual(M['span_count'],16)
 def test_witness_and_record_hash(self):
  self.assertEqual(len(W['images']),2)
  for x in W['images']:
   self.assertEqual(SHA(x['path']),x['sha256'])
   self.assertEqual((B/x['path']).stat().st_size,x['size_bytes'])
  for n,k in [('RULES.json','rules_sha256'),
   ('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','original_to_record_source_map_sha256')]:
   self.assertEqual(SHA(n),A[k],n)
 def test_high_risk_exception_preserved(self):
  t=' '.join(x['source_predicates_and_qualifiers'] for x in R['rules']).lower()
  for k in ['not corporally','no evil aspect','no strong','from misfortune','seller','receiver']:
   if k!='receiver':self.assertIn(k,t)
  self.assertEqual(len(U['issues']),14)
  self.assertEqual(A['new_empirical_astro_validations'],0)
  self.assertEqual(A['runtime_promotions'],0)
 def test_baseline_and_no_cross_chapter(self):
  self.assertEqual(A['previous_accepted_lilly'],3147)
  self.assertEqual(A['lilly_if_published'],3171)
  self.assertEqual(A['combined_if_published'],4237)
  self.assertFalse(A['canonical_published'])
  self.assertEqual([r['original_pdf_pages'] for r in R['rules'] if r['record_role']=='boundary'],[[411]])
 def test_semantic_mutants_rejected(self):
  r=copy.deepcopy(R['rules']);r[0]['accepted_historical_documentary']=False
  with self.assertRaises(AssertionError):check(r)
  r=copy.deepcopy(R['rules']);r[-1]['chapter']='LIV'
  with self.assertRaises(AssertionError):check(r)
  r=copy.deepcopy(R['rules']);r[1]['empirically_verified_case']=True
  with self.assertRaises(AssertionError):check(r)
if __name__=='__main__':unittest.main(verbosity=2)
