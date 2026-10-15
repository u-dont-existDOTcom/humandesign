"""Reverse document/record coverage for original 1647 Chapter LII images.

This is documentary semantic collation, not validation of historical astrology.
"""
import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
D=json.loads((B/'SOURCE_FIRST_CLAUSES_DRAFT.json').read_text())
P=json.loads((B/'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json').read_text())
W=json.loads((B/'SOURCE_WINDOW_MANIFEST.json').read_text())
S=P['source_spans']
R={r['record_number']:r for r in D['rows']}
K={r['claim_kind']:r for r in D['rows']}
class ReverseLII(unittest.TestCase):
 def test_image_source_and_boundary_unchanged(self):
  self.assertEqual(P['original_pdf_pages'],[403,404,405])
  self.assertEqual(W['chapter_LIII_opens_pdf'],405)
  for x in W['original_source_scans']:
   self.assertEqual(hashlib.sha256((B/x['relative_path']).read_bytes()).hexdigest(),x['sha256'])
 def test_exact_once_reverse_all_55_records(self):
  actual=[n for s in S for n in s['corresponding_draft_record_numbers']]
  self.assertEqual(len(S),42)
  self.assertEqual(actual,list(range(3017,3072)))
  self.assertEqual(len(set(actual)),55)
  for s in S:
   for kind,n in zip(s['record_kinds'],s['corresponding_draft_record_numbers']):
    self.assertEqual(R[n]['claim_kind'],kind)
    self.assertEqual(R[n]['original_pdf_pages'],s['original_pdf_pages'])
 def test_cross_page_prose_and_heading_are_distinct(self):
  seams=[(s['record_kinds'],s['original_pdf_pages']) for s in S if len(s['original_pdf_pages'])>1]
  self.assertEqual(seams,[(['cadent_partner_worse'],[403,404]),(['two_businesses_heading_cross_page'],[404,405])])
 def test_no_hunting_body_or_later_lawsuit_in_lII(self):
  self.assertEqual(S[-1]['record_kinds'],['next_chapter_hunting_boundary'])
  self.assertEqual(S[-1]['physical_locator'],'405 below divider')
  self.assertEqual(R[3071]['chapter'],'LIII_BOUNDARY_NAVIGATION_ONLY')
  self.assertTrue(all(r['chapter']=='LII' for r in D['rows'][:-1]))
  self.assertFalse(any('hunting' in r['claim_kind'].lower() for r in D['rows'][:-1]))
 def test_litigation_complex_requirements_and_scopes(self):
  self.assertIn('AND noncadent',K['stronger_overcomes']['editorial_precondition_and_alternatives'])
  self.assertIn('Scope restricted',K['war_exaltation_precedence']['editorial_precondition_and_alternatives'])
  self.assertIn('other question',K['nonwar_house_precedence']['editorial_precondition_and_alternatives'])
  self.assertIn('does not prove',json.loads((B/'SECOND_PASS_SOURCE_SCOPE_RECEIPT_20261015.json').read_text())['correction'])
  self.assertIn('do not assume significator itself cadent',K['joined_party_overcome']['editorial_precondition_and_alternatives'])
 def test_partner_and_neighbor_differentiation(self):
  self.assertIn('querent versus companion',K['partner_finance_role_assignments']['editorial_precondition_and_alternatives'])
  self.assertIn('Which party',K['divergent_financial_results']['editorial_precondition_and_alternatives'])
  self.assertIn('Sign modality',K['friendship_duration_by_degree']['editorial_precondition_and_alternatives'])
 def test_relocation_direction_conditions(self):
  self.assertIn('Neither move NOR',K['first_lord_good_to_evil_do_not_go']['editorial_precondition_and_alternatives'])
  self.assertIn('AND',K['first_lord_evil_to_good_go']['editorial_precondition_and_alternatives'])
  self.assertIn('All explicit conjunctions',K['l4_seventh_benefic_l1_l7_good_abide']['editorial_precondition_and_alternatives'])
  self.assertIn('Compare',K['choose_stronger_destination']['editorial_precondition_and_alternatives'])
 def test_documentary_uncertainty_not_empirical(self):
  self.assertFalse(P['independently_blinded_source_reader'])
  self.assertFalse(P['empirical_prediction_validation'])
  self.assertFalse(P['accepted'])
  self.assertEqual(P['canonical_count_unmodified'],3016)
  self.assertTrue(all(not r['empirical_accuracy_verified'] and not r['runtime_promoted'] for r in R.values()))
if __name__=='__main__':
 unittest.main()
