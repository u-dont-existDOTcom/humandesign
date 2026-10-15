"""Source witness and prohibited-promotion gates, not semantic full-text certification."""
import unittest,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
M=J('SOURCE_WINDOW_MANIFEST.json')
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
O=J('SOURCE_ORDER_DRAFT.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
R=D['rows']
by={x['source_local_id']:x for x in R}

class OriginalFirstPartnership(unittest.TestCase):
 def test_original_image_sha_and_pdf_identity(self):
  self.assertEqual(M['complete_original_pdf_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
  self.assertEqual([p['original_pdf_page'] for p in M['original_images']],[411,412,413])
  for item in M['original_images']:
   p=B/item['relative_path']
   self.assertEqual(p.stat().st_size,item['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),item['sha256'])
  self.assertTrue(M['original_image_pixels_parity_to_full_pdf_not_claimed'])

 def test_physical_heading_and_next_chapter_exclusion(self):
  self.assertEqual(M['physical_start']['pdf_page'],411)
  self.assertIn('BELOW',M['physical_start']['position'])
  self.assertEqual(M['physical_end']['pdf_page'],413)
  self.assertIn('ABOVE',M['physical_end']['position'])
  self.assertEqual(R[0]['role'],'heading')
  self.assertEqual(R[-1]['role'],'boundary')
  self.assertIn('Chapter LVI',R[-1]['conditional_statement_author_claim_not_empirical'])
  self.assertTrue(all('LVI' not in x['chapter'] for x in R[:-1]))

 def test_numbering_and_index_not_premature(self):
  self.assertEqual(len(R),D['source_units'])
  self.assertEqual(len(R),32)
  self.assertEqual(O['ordered_ids'],[f'LV-C{i:03}' for i in range(1,33)])
  self.assertEqual(O['ordered_ids'],[r['source_local_id'] for r in R])
  self.assertEqual(len(by),32)
  self.assertTrue(all(x['global_record_number'] is None for x in R))
  self.assertEqual(M['last_accepted_lilly_at_source_snapshot'],3071)
  self.assertEqual(M['prerequisites_before_global_numbering'],['LIII acceptance','LIV acceptance and frozen R range'])

 def test_cross_page_clauses_are_real(self):
  self.assertEqual([r['source_local_id'] for r in R if len(r['original_pdf_pages'])>1],O['cross_page_ids'])
  self.assertEqual([by[z]['original_pdf_pages'] for z in O['cross_page_ids']],[[411,412],[411,412],[412,413]])

 def test_reverse_source_coverage_is_total_and_single(self):
  self.assertEqual(C['span_count'],17)
  self.assertEqual(C['draft_record_count'],32)
  ids=[i for s in C['visual_source_spans'] for i in s['mapped_source_ids']]
  self.assertEqual(ids,[r['source_local_id'] for r in R])
  for s in C['visual_source_spans']:
   for i in s['mapped_source_ids']:
    self.assertEqual(s['pdf_pages'],by[i]['original_pdf_pages'])
  self.assertFalse(C['complete_independent_diplomatic_transcription_claimed'])

 def test_partnership_actors_not_conflated(self):
  self.assertIn('querent',by['LV-C002']['conditional_statement_author_claim_not_empirical'])
  self.assertIn('intended partner',by['LV-C003']['conditional_statement_author_claim_not_empirical'])
  self.assertIn('neer the cusp',by['LV-C004']['anchor_editorially_shortened_not_diplomatic'])
  self.assertIn('Moon',by['LV-C005']['conditional_statement_author_claim_not_empirical'])

 def test_movable_fixed_common_and_reception_preserved(self):
  self.assertIn('both first lord and Moon movable',by['LV-C008']['preconditions_and_disjunctions'])
  self.assertIn('reconcili',by['LV-C009']['conditional_statement_author_claim_not_empirical'].lower())
  self.assertIn('both relevant significators in fixed signs',by['LV-C010']['preconditions_and_disjunctions'])
  self.assertIn('fixed signs AND no reception',by['LV-C011']['preconditions_and_disjunctions'])
  self.assertIn('both relevant significators in common signs',by['LV-C013']['preconditions_and_disjunctions'])

 def test_moon_separation_application_direction(self):
  self.assertIn('benefic A AND applies benefic B',by['LV-C019']['preconditions_and_disjunctions'])
  self.assertIn('benefic AND applies malefic',by['LV-C020']['preconditions_and_disjunctions'])
  self.assertIn('does not print a full inverse',by['LV-C021']['conditional_statement_author_claim_not_empirical'])
  self.assertIn('quality unspecified',by['LV-C022']['preconditions_and_disjunctions'])

 def test_benefic_and_malefic_economic_houses(self):
  self.assertIn('second benefic -> querent',by['LV-C024']['preconditions_and_disjunctions'])
  self.assertIn('seventh benefic -> partner',by['LV-C024']['preconditions_and_disjunctions'])
  self.assertIn('second-house malefic OR source glyph',by['LV-C025']['preconditions_and_disjunctions'])
  self.assertIn('seventh OR eighth lord',by['LV-C031']['preconditions_and_disjunctions'])
  self.assertIn('square OR opposition',by['LV-C031']['preconditions_and_disjunctions'])

 def test_no_empirical_validation_or_runtime_promotion(self):
  self.assertTrue(all(x['new_independent_real_world_cases']==0 for x in R))
  self.assertTrue(all(x['validated_predictive_results']==0 for x in R))
  self.assertTrue(all(not x['historical_documentary_admitted'] and not x['runtime_promoted'] for x in R))
  self.assertEqual(len(U['issues']),16)
  self.assertEqual(U['empirical_validation_count'],0)

 def test_simple_mutation_counterexamples(self):
  def accepted_safe(rows):
   b={x['source_local_id']:x for x in rows}
   return all(x['global_record_number'] is None for x in rows) and 'quality unspecified' in b['LV-C022']['preconditions_and_disjunctions'] and 'no reception' in b['LV-C011']['preconditions_and_disjunctions']
  self.assertTrue(accepted_safe(R))
  mut=[dict(v) for v in R];mut[21]['preconditions_and_disjunctions']='Moon applies another malefic'
  self.assertFalse(accepted_safe(mut))
  mut=[dict(v) for v in R];mut[10]['preconditions_and_disjunctions']='fixed signs'
  self.assertFalse(accepted_safe(mut))
  mut=[dict(v) for v in R];mut[0]['global_record_number']=3090
  self.assertFalse(accepted_safe(mut))

if __name__=='__main__':
 unittest.main()
