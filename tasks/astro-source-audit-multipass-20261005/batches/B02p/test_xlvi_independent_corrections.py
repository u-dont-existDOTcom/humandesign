"""Regressions from independent original 1647 source audit; not empirical validity."""
import unittest
from test_lilly_xlvi import rec,CASE,CHART,U,D,R
def val(n):return rec(n)['source_statement']+' '+' '.join(rec(n)['preconditions']+rec(n)['exceptions_and_evidence_limits'])
class SourceReviewCorrections(unittest.TestCase):
 def test_sixth_house_aquarius_14_not_first_virgo(self):
  x=rec(1792)
  self.assertIn('SIXTH',x['source_statement'])
  self.assertIn('14. of ♒',x['source_statement'])
  self.assertNotIn('first-house',x['source_statement'].lower())
  self.assertIn('Aquarius',next(q['description'] for q in U['limits'] if q['id']=='U18'))
 def test_report_after_outcome_class_not_predicted(self):
  for n in (1790,1791,1792):
   self.assertEqual(rec(n)['claim_class'],'AUTHOR_REPORTED_POST_OUTCOME_TIMING')
   self.assertFalse(rec(n)['blinded_prospective_prediction'])
 def test_one_case_one_chart_one_author_report(self):
  self.assertEqual((CASE['individuals_in_passage'],CASE['original_charts_in_passage']),(1,1))
  self.assertFalse(CASE['count_as_validated_prediction'])
 def test_editorial_arithmetic_not_historical_rule(self):
  self.assertEqual(rec(1789)['source_statement_type'],'EDITORIAL_DERIVED_ARITHMETIC')
  self.assertEqual(rec(1789)['source_locator']['pdf_pages'],[323,324])
  self.assertIn('spoken warning',val(1789))
 def test_possible_inclusive_date_count_retained(self):
  self.assertIn('inclusive',val(1789).lower())
  self.assertEqual(CASE['calendar_date_difference_days'],12)
  self.assertEqual(CASE['counting_convention'],'Exclusive subtraction 12; inclusive date count13')
 def test_source_glyph_qualifier_and_cauda_separate(self):
  self.assertIn('☋',val(1775))
  self.assertIn('orientation',val(1775))
  self.assertIn('Cauda Leonis',val(1786))
  self.assertIn('separate',val(1786))
 def test_moon_not_mars_is_afflicted(self):
  self.assertIn('Moon is afflicted by Mars',val(1786))
 def test_chart_center_distinct_from_planetary_hour(self):
  self.assertEqual(CHART['source_clock_time'],'7:22 AM:')
  self.assertEqual(CHART['source_planetary_hour_glyph'],'♄')
  self.assertTrue(CHART['timezone_unknown'])
 def test_no_synthetic_full_ephemeris(self):
  self.assertEqual(len(CHART['wheel_labels_provisional']),12)
  self.assertTrue(CHART['additional_wheel_glyph_uncertainties'])
  self.assertFalse(CHART['independent_ephemeris_parity'])
 def test_four_reasons_only_one_outcome(self):
  self.assertEqual(CASE['source_rationale_record_ids'],['R1784','R1785','R1786','R1787'])
  self.assertEqual(CASE['post_outcome_record_ids'],['R1790','R1791','R1792'])
 def test_question_sun_not_birth_natal(self):
  self.assertIn('QUESTION',val(1790))
  self.assertIn('not natal chart',val(1790))
 def test_source_latins_recover_and_glyph_qualification(self):
  self.assertIn('fons vitalis',val(1784))
  self.assertIn('both in fixed signs',val(1784))
  self.assertIn('imperfect',val(1788))
  self.assertTrue(any(t in val(1791).lower() for t in ('blotched','imperfect','blurred')))
if __name__=='__main__':unittest.main()
