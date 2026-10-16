import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
C=J('CLAIM_LEDGER.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
def check(rows,spans):
 assert len(rows)==41 and len(spans)==10
 keys=[r['source_local_id'] for r in rows]
 assert keys==[f'LXXI-C{i:03}' for i in range(1,42)]
 mapped=[k for s in spans for k in s['mapped_local_ids']]
 assert len(mapped)==41 and sorted(mapped)==sorted(keys)
 assert all(s['original_pdf_pages']==rows[keys.index(k)]['original_pdf_pages']
            for s in spans for k in s['mapped_local_ids'])
 assert all(r['global_record_number'] is None and not r['documentary_accepted']
            and not r['empirical_prediction_validated'] for r in rows)
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter']=='LXXI' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXXII_NAVIGATION_ONLY'
 return True
class SourceFirst(unittest.TestCase):
 def test_bijection(self):
  self.assertTrue(check(D['rows'],M['source_spans']))
 def test_images(self):
  for im in W['original_images']:
   b=(B/im['path']).read_bytes()
   self.assertEqual(len(b),im['bytes'])
   self.assertEqual(hashlib.sha256(b).hexdigest(),im['sha256'])
 def test_boundaries(self):
  self.assertEqual(W['previous_lilly_accepted'],4052)
  self.assertEqual(W['original_body_pages'],[451,452])
  self.assertEqual(W['next_heading_page'],453)
  self.assertEqual(W['original_figure_date'],'15 April 1645')
 def test_reported_segments(self):
  self.assertEqual(C['early_false_rumor_author_reports'],1)
  self.assertEqual(C['later_reliable_news_author_reports'],1)
  self.assertEqual(C['later_person_return_author_reports'],1)
