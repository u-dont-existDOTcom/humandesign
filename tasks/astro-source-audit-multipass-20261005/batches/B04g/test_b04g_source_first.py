import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')['source_spans']
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json');C=J('CLAIM_LEDGER.json')
def check(rs,ss):
 assert len(rs)==33 and len(ss)==6
 assert [r['source_local_id'] for r in rs]==[f'LXXXVII-C{i:03}' for i in range(1,34)]
 ids=[x for s in ss for x in s['mapped_local_ids']]
 assert len(ids)==len(set(ids))==33 and set(ids)==set(r['source_local_id'] for r in rs)
 assert all(r['chapter']=='LXXXVII' and r['original_printed_chapter_numeral']=='LXXXVI' for r in rs[:-2])
 assert all(r['chapter']=='LXXXVIII_NAVIGATION_ONLY' and r['original_printed_chapter_numeral']=='LXXXVII' for r in rs[-2:])
 assert all(r['global_record_number'] is None and not r['historical_documentary_accepted'] and not r['independently_authenticated_preferment_outcome'] and not r['empirically_validated_prediction'] for r in rs)
class Source(unittest.TestCase):
 def test_all_source_rows(self):check(D,M)
 def test_image_witnesses(self):
  self.assertEqual([x['original_pdf_page'] for x in W['original_images']],[490,491])
  for x in W['original_images']:
   p=B/x['path'];self.assertEqual(p.stat().st_size,x['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['sha256'])
 def test_index_bridge(self):
  self.assertEqual(W['previous_accepted_lilly'],5080)
  self.assertEqual(W['source_editorial_chapter'],'LXXXVII')
  self.assertEqual(W['source_original_printed_chapter'],'LXXXVI')
  self.assertEqual(W['next_original_printed_chapter'],'LXXXVII')
 def test_predicted_and_retrospective_not_conflated(self):
  self.assertEqual(len([r for r in D if r['role']=='authorial_outcome_claim']),5)
  self.assertEqual(C['independent_verified_office_grants'],0)
  self.assertEqual(len(U['issues']),18)
 def test_duplicate_mutant(self):
  g=copy.deepcopy(M);g[0]['mapped_local_ids'].append(g[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D,g)
 def test_printed_numeral_mutant(self):
  d=copy.deepcopy(D);d[0]['original_printed_chapter_numeral']='LXXXVII'
  with self.assertRaises(AssertionError):check(d,M)
 def test_next_leak_mutant(self):
  d=copy.deepcopy(D);d[-1]['chapter']='LXXXVII'
  with self.assertRaises(AssertionError):check(d,M)
 def test_fake_empirical_mutant(self):
  d=copy.deepcopy(D);d[20]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(d,M)
if __name__=='__main__':unittest.main(verbosity=2)
