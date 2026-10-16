import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')['source_spans']
W=J('SOURCE_WINDOW_MANIFEST.json');C=J('CLAIM_LEDGER.json')
def check(r,s):
 assert len(r)==54 and len(s)==10
 assert [x['source_local_id'] for x in r]==[f'LXXXVI-C{i:03}' for i in range(1,55)]
 ids=[k for g in s for k in g['mapped_local_ids']]
 assert len(ids)==len(set(ids))==54
 assert set(ids)==set(x['source_local_id'] for x in r)
 assert all(x['chapter']=='LXXXVI' for x in r[:-2])
 assert all(x['chapter']=='LXXXVII_NAVIGATION_ONLY' for x in r[-2:])
 assert all(x['global_record_number'] is None and not x['historical_documentary_accepted']
 and not x['empirically_validated_prediction'] and not x['runtime_model_promoted'] for x in r)
class Source(unittest.TestCase):
 def test_exact_mapping(self):check(D,M)
 def test_original_hashes(self):
  self.assertEqual([z['original_pdf_page'] for z in W['original_images']],[489,490])
  for z in W['original_images']:
   p=B/z['path'];self.assertEqual(p.stat().st_size,z['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),z['sha256'])
 def test_boundary(self):
  self.assertEqual(W['previous_accepted_lilly'],5026)
  self.assertEqual(W['next_numbered_chapter'],'LXXXVII')
  self.assertEqual([g['original_pdf_pages'] for g in M if len(g['original_pdf_pages'])>1],[[489,490]])
 def test_uncertain_figure_date(self):self.assertTrue(W['source_figure_absolute_date_unresolved'])
 def test_partial_failure(self):
  text=' '.join(x['historical_author_paraphrase'].lower() for x in D)
  self.assertIn('lost some of her forces',text)
  self.assertIn('essentially destroying',text)
  self.assertTrue(W['Queen_army_not_totally_destroyed_in_author_account'])
 def test_science_separation(self):
  self.assertEqual(C['independently_verified_royal_military_outcomes'],0)
  self.assertEqual(C['new_empirical_validations'],0)
 def test_duplicate_mutant(self):
  q=copy.deepcopy(M);q[0]['mapped_local_ids'].append(q[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D,q)
 def test_wrong_chapter_mutant(self):
  q=copy.deepcopy(D);q[-1]['chapter']='LXXXVI'
  with self.assertRaises(AssertionError):check(q,M)
 def test_fake_empirical_mutant(self):
  q=copy.deepcopy(D);q[25]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(q,M)
if __name__=='__main__':unittest.main(verbosity=2)
