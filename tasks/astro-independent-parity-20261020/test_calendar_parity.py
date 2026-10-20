"""Chinese independent implementer DATE/clock parity, not source or human validation."""
import json
import unittest
from pathlib import Path
from calendar_parity import compare_day, deterministic_sample, build_result
HERE=Path(__file__).resolve().parent
class CalendarComparisonTests(unittest.TestCase):
 def test_sample_is_deterministic_ordered_and_unique(self):
  sample=deterministic_sample()
  self.assertEqual(len(sample),2036)
  self.assertEqual(sample,sorted(set(sample)))
 def test_1985_01_29_calendar_and_lunar_new_year(self):
  r=compare_day(1985,1,29)
  self.assertEqual(r.sxtwl_lunar,(1984,12,9,False))
  self.assertEqual(r.lunar_python_lunar,r.sxtwl_lunar)
  self.assertEqual(r.sxtwl_date_based_pillars,('甲子','丁丑','戊辰','戊午'))
  self.assertEqual(r.sxtwl_date_based_pillars,r.lunar_python_clock_based_pillars)
 def test_2023_intercalary_second_month(self):
  r=compare_day(2023,3,22)
  self.assertEqual(r.sxtwl_lunar,(2023,2,1,True))
  self.assertEqual(r.lunar_python_lunar,r.sxtwl_lunar)
 def test_1616_proleptic_gregorian_date_not_historical_Julian_claim(self):
  a=compare_day(1616,9,19);b=compare_day(1616,9,29)
  self.assertNotEqual(a.sxtwl_lunar,b.sxtwl_lunar)
  self.assertTrue(a.same_lunar and b.same_lunar)
  self.assertEqual(b.sxtwl_lunar,(1616,8,19,False))
 def test_LiChun_calendar_date_vs_precise_term_clock_exception(self):
  r=compare_day(2024,2,4,hh=12)
  self.assertFalse(r.same_year_pillar_date_vs_exact_time)
  self.assertFalse(r.same_month_pillar_date_vs_exact_time)
  self.assertEqual(r.sxtwl_date_based_pillars[:2],('甲辰','丙寅'))
  self.assertEqual(r.lunar_python_clock_based_pillars[:2],('癸卯','乙丑'))
  self.assertTrue(r.same_lunar and r.same_lunar_new_year_pillar)
 def test_LiChun_after_instant_converges(self):
  r=compare_day(2024,2,4,hh=20)
  self.assertTrue(r.same_year_pillar_date_vs_exact_time and r.same_month_pillar_date_vs_exact_time)
 def test_23_hour_day_convention_explicitly_not_hidden(self):
  r=compare_day(2024,2,4,hh=23)
  self.assertFalse(r.same_day_pillar)
  self.assertTrue(r.same_hour_pillar)
  self.assertEqual(r.sxtwl_date_based_pillars[2],'戊戌')
  self.assertEqual(r.lunar_python_clock_based_pillars[2],'己亥')
 def test_calendar_year_Lichun_vs_newyear_are_distinct(self):
  r=compare_day(2024,2,5)
  self.assertEqual(r.sxtwl_lunar_year_pillar,'癸卯')
  self.assertEqual(r.lunar_python_lunar_year_pillar,'癸卯')
  self.assertEqual(r.sxtwl_date_based_pillars[0],'甲辰')
  self.assertEqual(r.lunar_python_clock_based_pillars[0],'甲辰')
 def test_invalid_clock_rejected(self):
  for hr in (-1,24):
   with self.assertRaises(ValueError):compare_day(2024,2,4,hh=hr)
 def test_whole_sample_mismatches_not_suppressed(self):
  result=build_result()
  self.assertEqual(result['sample_count'],2036)
  self.assertEqual(result['counts']['same_lunar']['mismatched'],0)
  self.assertEqual(result['counts']['same_lunar_new_year_pillar']['mismatched'],0)
  self.assertEqual(result['counts']['same_year_pillar_date_vs_exact_time']['mismatched'],5)
  self.assertEqual(result['counts']['same_month_pillar_date_vs_exact_time']['mismatched'],24)
  for col,stat in result['counts'].items():self.assertEqual(len(result['mismatches_all'][col]),stat['mismatched'])
 def test_committed_report_matches_recomputation(self):
  expected=json.loads((HERE/'CALENDAR_TWO_LIBRARY_COMPARISON_20261020.json').read_text())
  self.assertEqual(expected,json.loads(json.dumps(build_result(),ensure_ascii=False)))
 def test_never_claims_validation(self):
  data=build_result()
  self.assertFalse(data['whole_natal_calendar_chart_engine_verified'])
  self.assertEqual(data['independent_real_human_predictions_validated'],0)
if __name__=='__main__':unittest.main()
