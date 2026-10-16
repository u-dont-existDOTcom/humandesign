import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows'];M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')['source_spans']
W=J('SOURCE_WINDOW_MANIFEST.json');C=J('CLAIM_LEDGER.json');U=J('UNRESOLVED_SOURCE_LIMITS.json')
def valid(rs,spans):
 assert len(rs)==48 and len(spans)==7
 assert [r['source_local_id'] for r in rs]==[f'LXXXVIII-C{i:03}' for i in range(1,49)]
 ids=[id for g in spans for id in g['mapped_local_ids']]
 assert len(ids)==len(set(ids))==48 and set(ids)==set(r['source_local_id'] for r in rs)
 assert all(r['chapter']=='LXXXVIII' and r['original_printed_chapter_numeral']=='LXXXVII' for r in rs[:-2])
 assert all(r['chapter']=='LXXXIX_NAVIGATION_ONLY' and r['original_printed_chapter_numeral']=='LXXXVIII' for r in rs[-2:])
 assert all(not r['historical_documentary_accepted'] and r['global_record_number'] is None and not r['empirically_validated_prediction'] for r in rs)
class Source(unittest.TestCase):
 def test_full_one_to_one_source_order(self):valid(D,M)
 def test_original_page_hashes(self):
  self.assertEqual([x['original_pdf_page'] for x in W['original_images']],[491,492,493])
  for x in W['original_images']:
   p=B/x['path'];self.assertEqual(p.stat().st_size,x['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['sha256'])
 def test_prev_and_next_literal_headings(self):
  self.assertEqual(W['previous_accepted_lilly'],5113)
  self.assertEqual(W['chapter_editorial'],'LXXXVIII')
  self.assertEqual(W['chapter_original_printed'],'LXXXVII')
  self.assertEqual(W['following_original_printed'],'LXXXVIII')
 def test_partial_whole_probable_not_conflated(self):
  text=' '.join(r['historical_author_paraphrase'].lower() for r in D)
  for s in ('only part','probability','whole','suffer harm','feasible and possible','even when'):
   self.assertIn(s,text)
 def test_case_not_prospectively_validated(self):
  self.assertEqual(len(U['issues']),21)
  self.assertEqual(C['independent_verified_hope_outcomes'],0)
  self.assertEqual(C['new_empirical_validations'],0)
 def test_source_page_seam(self):
  self.assertEqual([x['original_pdf_pages'] for x in M if len(x['original_pdf_pages'])>1],[[491,492]])
 def test_duplicate_source_mutant(self):
  x=copy.deepcopy(M);x[0]['mapped_local_ids'].append(x[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D,x)
 def test_heading_leak_mutant(self):
  x=copy.deepcopy(D);x[-1]['chapter']='LXXXVIII'
  with self.assertRaises(AssertionError):valid(x,M)
 def test_empirical_promotion_mutant(self):
  x=copy.deepcopy(D);x[23]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):valid(x,M)
if __name__=='__main__':unittest.main(verbosity=2)
