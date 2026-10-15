"""Reverse image-first Chapter LI source-to-record coverage and source-branch tests.
The independently authored anchors are MANUAL image readings, not proof that OCR,
a blind second transcription or empirical prediction validation occurred.
"""
import unittest,json,hashlib
from pathlib import Path
from collections import Counter

B=Path(__file__).resolve().parent
J=lambda p:json.loads((B/p).read_text(encoding='utf8'))
P=J('ORIGINAL_TO_RECORD_COVERAGE_V1.json')
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_DRAFT.json')
R={r['record_number']:r for r in D['rows']}
S=P['source_spans']

class ChapterLIReverseCoverage(unittest.TestCase):
 def test_all_original_spans_are_page_located_and_hash_grounded(self):
  self.assertEqual(len(S),P['source_span_count'])
  self.assertEqual(P['source_span_count'],35)
  self.assertEqual(P['reviewed_original_pdf_pages'],[400,401,402])
  self.assertEqual(P['boundary_only_pdf_page'],403)
  for item in W['source_images']:
   self.assertEqual(P['image_sha256s'][str(item['original_pdf_page'])],item['sha256'])
   self.assertEqual(hashlib.sha256((B/item['path']).read_bytes()).hexdigest(),item['sha256'])
  self.assertTrue(all(s['image_first_source_anchor_editorially_shortened'] for s in S))
  self.assertTrue(all(not s['anchor_is_diplomatic_quote'] for s in S))

 def test_reverse_map_exhaustively_reaches_each_draft_record_once(self):
  covered=[n for s in S for n in s['corresponding_record_numbers']]
  self.assertEqual(covered,list(range(2975,3017)))
  self.assertEqual(len(covered),len(set(covered)))
  self.assertEqual(set(covered),set(R))
  self.assertEqual(P['distinct_documentary_record_count'],42)
  for s in S:
   for n in s['corresponding_record_numbers']:
    self.assertEqual(s['original_pdf_pages'],R[n]['original_pdf_pages'])

 def test_page_seams_and_closed_chapter_boundaries(self):
  self.assertEqual([(s['corresponding_record_numbers'],s['original_pdf_pages']) for s in S if len(s['original_pdf_pages'])>1],
   [([2978],[400,401]),([2999],[401,402])])
  self.assertTrue(all('below divider' in s['printed_image_locator'] for s in S if s['original_pdf_pages']==[400]))
  self.assertEqual(S[-1]['corresponding_record_numbers'],[3016])
  self.assertEqual(S[-1]['original_pdf_pages'],[403])
  self.assertEqual(R[3016]['role'],'boundary')
  self.assertTrue(all(403 not in r['original_pdf_pages'] for r in D['rows'][:-1]))

 def test_five_literal_e_contra_plus_one_other_converse(self):
  rs=[r for r in D['rows'] if r['role']=='converse']
  self.assertEqual(len(rs),6)
  self.assertEqual(sum(r['source_anchor_editorial_normalization']=='& e contra' for r in rs),5)
  self.assertEqual(sum(r['source_anchor_editorial_normalization']=='the contrary noteth the contrary' for r in rs),1)
  self.assertTrue(all(not r['preconditions'] for r in rs))
  self.assertIn('five literal',U['issues'][2]['description'])
  self.assertIn('later war-outcome',U['issues'][1]['description'])

 def test_distinct_last_war_outcomes_and_marginal_house_lists(self):
  self.assertIn('victory OR',R[3008]['source_statement'])
  self.assertIn('reconciliation',R[3008]['source_statement'])
  self.assertIn('cusp',R[3007]['source_statement'].lower())
  self.assertIn('loss for both',R[3009]['source_statement'])
  self.assertIn('10/11/12/1/2/3',R[3012]['preconditions'][0])
  self.assertIn('9/8/7/6/5/4',R[3013]['preconditions'][0])
  self.assertIn('death of querent',R[3014]['source_statement'].lower())
  self.assertIn('death of adversary',R[3015]['source_statement'].lower())
  self.assertIn('OR',R[3015]['preconditions'][0])

 def test_documentary_source_is_not_empirical_truth(self):
  self.assertFalse(P['blind_independent_reviewer_claimed'])
  self.assertFalse(P['complete_diplomatic_transcription_claimed'])
  self.assertFalse(P['empirical_prediction_accuracy_tested'])
  self.assertTrue(P['not_counted_as_independent_real_world_cases'])
  self.assertTrue(all(not r['independently_authenticated_outcome'] and not r['prospective_blinded_prediction'] for r in D['rows']))
  self.assertTrue(all(not r['accepted'] for r in D['rows']))

if __name__=='__main__':
 unittest.main()
