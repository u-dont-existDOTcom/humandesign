"""Selected regressions for independently identified source fidelity defects."""
import unittest
from test_lilly_sick_doctor import load,record,body
class SourceFidelityRegressions(unittest.TestCase):
 def test_weekday_not_day_twentyfour(self):
  self.assertEqual(load('CHART_INSCRIPTION.json')['source_day_of_month'],8)
  self.assertIn('not numeral 24',body(1746))
 def test_julian_explicitly_inferred_not_printed(self):
  j=load('CHART_INSCRIPTION.json')
  self.assertIn('inferred_calendar',j)
  self.assertNotIn('source_calendar',j)
  self.assertTrue(load('CASE_EVIDENCE.json')['julian_question_date_inferred_not_printed_calendar'])
 def test_chart_center_includes_latin_connectives(self):
  s=body(1747)
  for w in ('a △','ad □','et ✶','uncertain'):self.assertIn(w,s)
 def test_stars_original_ligature_and_double_evil(self):
  s=body(1748)
  self.assertIn('chelæ',s)
  self.assertIn('evill position or presence',s)
 def test_sixth_house_source_backreference(self):
  self.assertIn('page 244',body(1749))
  self.assertIn('part or member',body(1749))
 def test_planet_in_sign_not_conjunction(self):
  self.assertIn('planet-in-sign',body(1751))
  self.assertNotIn('requires the conjunction',body(1751))
 def test_melancholy_term_vs_lunar_house_and_physician_deferral(self):
  s=body(1756)
  self.assertIn('own terms',s)
  self.assertIn('moon in saturn',s)
  self.assertIn('your physicians best know',s)
  self.assertIn('page244',s)
 def test_moon_out_of_terms_not_forced_negative(self):
  s=body(1757)
  self.assertIn('out of his termes',s)
  self.assertIn('unresolved',s)
  self.assertNotIn('moon outside his terms',s)
 def test_doctor_encounter_not_false_temporal_order(self):
  s=body(1758)
  self.assertIn('when i came to speak',s)
  self.assertIn('not established',s)
 def test_patient_complaint_vs_author_observations(self):
  q=record(1759)
  self.assertEqual({x['class'] for x in q['source_components']},{'AUTHOR_STATED_CONDITION','PATIENT_COMPLAINT_AS_RELAYED'})
  self.assertIn('dull',q['source_statement'].lower())
 def test_jaundice_is_hedged_not_diagnosed(self):
  self.assertIn('as if there was inclination',body(1760))
  self.assertFalse(record(1760)['source_components'][0]['confirmed_diagnosis'])
 def test_aquarius_moon_literal(self):
  s=body(1762)
  self.assertIn('aquarius',s)
  self.assertIn('&c.',s)
 def test_italic_author_report_not_independent(self):
  q=record(1765)
  kinds={x['class'] for x in q['source_components']}
  self.assertEqual(kinds,{'AUTHOR_ASTROLOGICAL_INFERENCE','AUTHOR_REPORTED_OUTCOME'})
  self.assertEqual(q['source_components'][1]['typography'],'italic in original print')
 def test_saturn_duration_separate_from_fixed_angles(self):
  s=body(1766)
  self.assertIn('page 248',s)
  self.assertIn('besides',s)
 def test_longitude_of_disease_not_person_lifespan(self):
  s=body(1767)
  self.assertIn('longitude of the disease',s)
  self.assertIn('out of angles',s)
  self.assertIn('unsettled',s)
 def test_duration_interpretation_after_reported_death(self):
  for i in (1766,1767,1768):self.assertIn('after',record(i)['not_prospective_order_note'].lower())
 def test_claims_have_separate_per_record_classes(self):
  self.assertEqual(record(1764)['claim_class'],'AUTHOR_THERAPEUTIC_SUGGESTION')
  self.assertEqual(record(1769)['claim_class'],'STRUCTURAL_BOUNDARY')
 def test_next_chapter_boundary_controller_only(self):
  x=load('SECTION_COVERAGE.json')['following_boundary']
  self.assertTrue(x['controller_image_checked'])
  self.assertFalse(x['independent_reviewer_image_checked'])
 def test_partial_chart_glyphs_retained_with_uncertainty(self):
  chart=load('CHART_GLYPH_OBSERVATIONS.json')
  self.assertTrue(any(v['confidence']=='MODERATE' for v in chart['observations']))
  self.assertGreater(len(chart['observations']),3)
 def test_one_historical_case_cannot_multiply_with_records(self):
  case=load('CASE_EVIDENCE.json')
  self.assertEqual(case['number_of_individuals_reported'],1)
  self.assertFalse(case['documented_prediction_freeze_before_outcome'])
if __name__=='__main__':unittest.main()
