"""Focused source-integrity tests for unaccepted, out-of-order Chapter LIV stage."""
import unittest,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
load=lambda name:json.loads((B/name).read_text())
M=load('SOURCE_WINDOW_MANIFEST.json')
D=load('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=load('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
U=load('UNRESOLVED_SOURCE_LIMITS.json')
S=load('SOURCE_ORDER_DRAFT.json')
R=D['rows']
BY={r['local_id']:r for r in R}

class OriginalSourceFirstProvisional(unittest.TestCase):
 def test_provenance_unmodified_image_hashes(self):
  self.assertEqual(M['original_full_pdf_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
  self.assertEqual(M['original_pages'],[410,411])
  self.assertEqual(M['original_printed_pages'],[376,377])
  for r in M['images']:
   f=B/r['path']; self.assertTrue(f.is_file())
   self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),r['sha256'])
   self.assertEqual(f.stat().st_size,r['size_bytes'])
  self.assertFalse(M['complete_full_diplomatic_second_transcription_claimed'])

 def test_order_and_id_provisional(self):
  self.assertEqual(D['record_count'],24)
  self.assertEqual(len(R),24)
  self.assertEqual(S['ordered_local_ids'],[f'LIV-C{i:03}' for i in range(1,25)])
  self.assertEqual([r['local_id'] for r in R],S['ordered_local_ids'])
  self.assertEqual(len(BY),24)
  self.assertEqual(S['chapter_LV_heading_boundary_only'],'LIV-C024')
  self.assertTrue(all(r['global_record_number'] is None for r in R))

 def test_substance_original_read_order(self):
  self.assertEqual([r['record_role'] for r in R[:3]],['heading','assignment','assignment'])
  self.assertEqual(R[-1]['record_role'],'boundary')
  self.assertTrue(R[-1]['source_statement_paraphrase'].startswith('Chapter LIV ends'))
  self.assertEqual(R[-1]['original_pdf_pages'],[411])
  self.assertEqual([r['original_pdf_pages'] for r in R if len(r['original_pdf_pages'])>1],[[410,411],[410,411]])
  self.assertEqual(S['cross_page_local_ids'],['LIV-C018','LIV-C019'])

 def test_original_visual_reverse_map_is_total(self):
  self.assertEqual(C['span_count'],16)
  self.assertEqual(C['draft_source_units'],24)
  ids=[i for span in C['source_spans'] for i in span['draft_local_ids']]
  self.assertEqual(ids,[r['local_id'] for r in R])
  for span in C['source_spans']:
   for id in span['draft_local_ids']:
    self.assertEqual(span['original_pdf_pages'],BY[id]['original_pdf_pages'])
  self.assertFalse(C['independent_diplomatic_transcription_claimed'])

 def test_actor_and_direction_not_conflated(self):
  self.assertIn('ascendant lord AND Moon',BY['LIV-C002']['source_statement_paraphrase'])
  self.assertIn('seventh-house lord',BY['LIV-C003']['source_statement_paraphrase'])
  self.assertIn('seller',BY['LIV-C013']['source_statement_paraphrase'])
  self.assertIn('querent',BY['LIV-C014']['source_statement_paraphrase'])
  self.assertIn('buyer',BY['LIV-C019']['source_statement_paraphrase'])
  self.assertIn('seller',BY['LIV-C020']['source_statement_paraphrase'])

 def test_branch_conditions_and_exceptions_retained(self):
  self.assertIn('not corporally',BY['LIV-C016']['source_predicates_and_qualifiers'])
  self.assertIn('no evil aspect',BY['LIV-C017']['source_predicates_and_qualifiers'])
  self.assertIn('no strong significator application',BY['LIV-C021']['source_predicates_and_qualifiers'])
  self.assertIn('no direct aspect',BY['LIV-C007']['source_predicates_and_qualifiers'].lower())
  self.assertIn('AND',BY['LIV-C023']['source_predicates_and_qualifiers'])

 def test_no_malefic_glyph_excess_confidence(self):
  self.assertIn('node-like',BY['LIV-C018']['source_statement_paraphrase'])
  self.assertIn('glyph interpretation retained',BY['LIV-C018']['source_predicates_and_qualifiers'])
  self.assertIn('before formalizing',U['issues'][4]['description'])

 def test_commodity_houses_match_stated_classes(self):
  self.assertIn('sixth house',BY['LIV-C009']['source_statement_paraphrase'])
  self.assertIn('twelfth house and ascendant',BY['LIV-C010']['source_statement_paraphrase'])
  self.assertIn('fourth house and its lord',BY['LIV-C011']['source_statement_paraphrase'])
  self.assertIn('no complete commodity list',BY['LIV-C012']['source_statement_paraphrase'])

 def test_early_modern_converse_not_executed(self):
  self.assertEqual(sum(r['record_role']=='converse' for r in R),1)
  self.assertIn('e contra',BY['LIV-C006']['source_anchor_editorial_abbreviation'])
  self.assertIn('without an independently enumerated',BY['LIV-C006']['source_statement_paraphrase'])

 def test_source_ambiguities_preserved(self):
  self.assertEqual(len(U['issues']),14)
  self.assertEqual([x['id'] for x in U['issues']],[f'Z-U{i:02}' for i in range(1,15)])
  self.assertTrue(any('strong-applying' in x['description'] for x in U['issues']))
  self.assertTrue(any('sign whose lord' in x['description'].lower() for x in U['issues']))

 def test_no_numbering_or_empirical_promotion(self):
  self.assertEqual(M['prior_accepted_lilly_at_frozen_start'],3071)
  self.assertEqual(M['last_accepted_chapter'],'LII')
  self.assertEqual(M['predecessor_still_open'],'LIII')
  self.assertTrue(all(not x['accepted_historical_documentary'] for x in R))
  self.assertTrue(all(not x['empirically_verified_case'] for x in R))
  self.assertTrue(all(not x['model_runtime_promotion'] for x in R))
  self.assertTrue(all(not x['safe_for_real_person_prognosis'] for x in R))
  self.assertEqual(U['outcome_validation_count'],0)

 def test_mutants_are_detected_by_semantic_invariant(self):
  def conditions_correct(rows):
   b={x['local_id']:x for x in rows}
   return 'not corporally' in b['LIV-C016']['source_predicates_and_qualifiers'] and 'no strong significator application' in b['LIV-C021']['source_predicates_and_qualifiers'] and all(x['global_record_number'] is None for x in rows)
  self.assertTrue(conditions_correct(R))
  fake=[dict(x) for x in R]
  fake[15]['source_predicates_and_qualifiers']='Sun in first' # lose exception
  self.assertFalse(conditions_correct(fake))
  fake=[dict(x) for x in R]
  fake[20]['source_predicates_and_qualifiers']='Moon VOC' # lose exclusion
  self.assertFalse(conditions_correct(fake))
  fake=[dict(x) for x in R]
  fake[0]['global_record_number']=3072 # premature global numbering
  self.assertFalse(conditions_correct(fake))

if __name__=='__main__':
 unittest.main()
