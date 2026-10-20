"""Partial source-chart mechanistic examples and explicit uncertainty; no human predictions."""
import json,unittest
from pathlib import Path
from datetime import datetime,timedelta,timezone
from partial_chinese_chart_candidates import (source_candidate,uncertainty_envelope,build_demo,CHINA_CIVIL_FIXED_UTC_PLUS8)
HERE=Path(__file__).resolve().parent
CST=CHINA_CIVIL_FIXED_UTC_PLUS8
class BoundedChineseChartCandidates(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.report=json.loads((HERE/'PARTIAL_CHINESE_CHART_BOUNDARY_CANDIDATES_20261020.json').read_text())
 def test_synthetic_date_1985_01_29_China_noon(self):
  a=source_candidate(datetime(1985,1,29,12,tzinfo=CST))
  self.assertEqual(a.lunar_ymd,(1984,12,9))
  self.assertEqual(a.bazi_four_pillars_if_policy_lunar_python_exact,('甲子','丁丑','戊辰','戊午'))
  self.assertEqual(a.source_sxtwl_four_pillars_date_convention,a.bazi_four_pillars_if_policy_lunar_python_exact)
 def test_leap_month_explicitly_uses_ZiWei_next_rule(self):
  a=source_candidate(datetime(2023,3,22,12,tzinfo=CST))
  self.assertEqual(a.lunar_ymd,(2023,2,1));self.assertTrue(a.source_lunar_leap_month)
  self.assertEqual(a.ziwei_month_for_palace_rule,3)
  self.assertEqual(a.ziwei_chosen_lunar_leap_policy,'quan_shu_as_next (source-specific, not universal)')
 def test_original_ZiWei_first_month_Zi_hour_life_body_Yin(self):
  a=source_candidate(datetime(2000,2,5,0,tzinfo=CST))
  self.assertEqual(a.lunar_ymd[1],1)
  self.assertTrue(a.bazi_hour_pillar.endswith('子'))
  self.assertEqual(a.ziwei_life_palace_partial,'Yin')
  self.assertEqual(a.ziwei_body_palace_partial,'Yin')
 def test_LiChun_china_clock_5minute_interval_two_states(self):
  start=datetime(2024,2,4,16,26,tzinfo=CST)
  q=uncertainty_envelope(start,5)
  self.assertEqual(q['unique_partial_states'],2)
  firsts={tuple(q['possible_distinct_variants'][i]['bazi_exact_four_pillars'][:2]) for i in range(2)}
  self.assertEqual(firsts,{('癸卯','乙丑'),('甲辰','丙寅')})
  self.assertEqual(q['evaluated_clock_minute_points'],11)
 def test_sxtwl_date_only_vs_exact_after_LiChun_not_misread(self):
  a=source_candidate(datetime(2024,2,4,16,26,tzinfo=CST))
  self.assertFalse(a.sxtwl_exact_year_month_conventions_agree)
  self.assertTrue(a.original_sxtwl_has_JieQi_on_date)
 def test_late_Zi_has_two_day_policies(self):
  a=source_candidate(datetime(2024,2,4,23,30,tzinfo=CST))
  self.assertTrue(a.bazi_day_unresolved_for_23h)
  self.assertEqual(a.bazi_calendar_day_pillar,'戊戌')
  self.assertEqual(a.bazi_day_23h_next_day_convention,'己亥')
  self.assertEqual(a.bazi_hour_pillar,'甲子')
 def test_reject_UTC_not_China_local(self):
  with self.assertRaisesRegex(ValueError,'explicit fixed China Standard'):
   source_candidate(datetime(2024,2,4,16,26,tzinfo=timezone.utc))
 def test_reject_naive_and_old_1616_history(self):
  with self.assertRaises(ValueError):source_candidate(datetime(1985,1,29,12))
  with self.assertRaisesRegex(ValueError,'scoped to post-1970'):
   source_candidate(datetime(1616,9,29,12,tzinfo=CST))
 def test_dont_accept_huge_uncertainty_as_exact_boundary(self):
  with self.assertRaises(ValueError):uncertainty_envelope(datetime(2024,2,4,12,tzinfo=CST),121)
 def test_zero_radius_deterministic(self):
  r=uncertainty_envelope(datetime(1985,1,29,12,tzinfo=CST),0)
  self.assertEqual(r['unique_partial_states'],1)
  self.assertEqual(r['evaluated_clock_minute_points'],1)
 def test_source_ziwei_engine_only_partial(self):
  a=source_candidate(datetime(1985,1,29,12,tzinfo=CST))
  self.assertTrue(a.no_full_ziwei_14_star_calculation)
  self.assertTrue(a.no_independent_original_calendar_policy_confirmation)
 def test_exact_report_recomputes(self):
  self.assertEqual(self.report,json.loads(json.dumps(build_demo(),ensure_ascii=False)))
 def test_no_human_predictions_or_runtime_promotion(self):
  self.assertFalse(self.report['full_natal_engine_validated'])
  self.assertEqual(self.report['human_predictions_validated'],0)
  self.assertFalse(self.report['runtime_model_promoted'])
if __name__=='__main__':unittest.main()
