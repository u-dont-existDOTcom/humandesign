import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_FIRST_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
def check(rows,spans):
 assert len(rows)==44 and len(spans)==15
 keys=[r['local_id'] for r in rows]
 assert keys==[f'LXIII-C{i:03}' for i in range(1,45)]
 mapped=[k for x in spans for k in x['mapped_local_ids']]
 assert len(mapped)==44 and sorted(mapped)==sorted(keys)
 assert all(x['original_pdf_pages']==rows[keys.index(k)]['original_pdf_pages']
   for x in spans for k in x['mapped_local_ids'])
 assert all(r['global_record_number'] is None and not r['historical_documentary_admitted'] and
   not r['empirically_validated_thief_or_case'] for r in rows)
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter']=='LXIII' for r in rows[:-1])
 assert rows[-1]['chapter']=='NEXT_PRINTED_LIV_FISH_STOLEN_NAVIGATION_ONLY'
class SourceFirst(unittest.TestCase):
 def test_image_to_draft_bijection(self):check(D['rows'],M['source_spans'])
 def test_primary_source(self):
  self.assertEqual(W['original_pdf_body_pages'],[428,429,430])
  self.assertEqual(W['prior_accepted_lilly'],3527)
  self.assertEqual(W['next_heading_exact_original_roman'],'LIV')
  self.assertEqual(W['next_heading_logical_chapter'],'LXIV')
 def test_frozen_image_sha(self):
  for im in W['original_page_images']:
   raw=(B/im['path']).read_bytes()
   self.assertEqual(len(raw),im['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),im['sha256'])
 def test_worked_money_case(self):
  text=' '.join(r['historical_author_paraphrase'] for r in D['rows']).lower()
  self.assertIn('24 may 1647',text)
  self.assertIn('returned within three days',text)
 def test_competing_planets(self):
  text=' '.join(r['historical_author_paraphrase'] for r in D['rows']).lower()
  self.assertIn('saturn',text)
  self.assertIn('mercury',text)
  self.assertIn('mars',text)
 def test_claim_separation(self):
  self.assertEqual(C['new_empirical_predictions'],0)
  self.assertEqual(C['globally_accepted_new_units'],0)
  self.assertEqual(C['independently_authenticated_thief_cases'],0)
 def test_uncertainties(self):
  self.assertEqual(len(U['issues']),16)
 def test_navigational_marker(self):
  self.assertEqual(D['rows'][-1]['original_pdf_pages'],[431])
  self.assertIn('LIV',D['rows'][-1]['source_conditions_and_uncertainty'])
 def test_mutant_double_map(self):
  r=copy.deepcopy(M['source_spans'])
  r[0]['mapped_local_ids'].append(r[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],r)
 def test_mutant_empirical_flag(self):
  r=copy.deepcopy(D['rows'])
  r[4]['empirically_validated_thief_or_case']=True
  with self.assertRaises(AssertionError):check(r,M['source_spans'])
 def test_mutant_boundary(self):
  r=copy.deepcopy(D['rows']);r[-1]['chapter']='LXIII'
  with self.assertRaises(AssertionError):check(r,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
