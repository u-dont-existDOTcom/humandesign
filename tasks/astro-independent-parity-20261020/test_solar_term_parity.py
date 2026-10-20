"""SXTWL-vs-Swiss term timing independent implementation, retaining ancient misses."""
import json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from solar_term_parity import build_result,verify_ephe,SOURCE_YEARS
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;EPHE=ROOT/'data/ephemeris'
class TwoEphemerisSolarTerms(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.report=json.loads((HERE/'SOLAR_TERMS_TWO_ALGORITHMS_20261020.json').read_text())
 def test_source_four_Swiss_files_verified(self):verify_ephe(EPHE)
 def test_missing_Swiss_not_silent_Moshier_fallback(self):
  with TemporaryDirectory() as tmp:
   with self.assertRaisesRegex(ValueError,'refusing ephemeris fallback'):verify_ephe(tmp)
 def test_two_implementation_event_count_and_years(self):
  self.assertEqual(self.report['comparison_events'],250)
  self.assertEqual(tuple(self.report['years']),SOURCE_YEARS)
  self.assertEqual(self.report['events_per_year'],25)
 def test_every_event_explicitly_kept_in_source_order(self):
  rows=self.report['individual_source_versus_swiss_term_results']
  self.assertEqual(len(rows),250)
  for year in SOURCE_YEARS:
   yearrows=[r for r in rows if r['source_year_input']==year]
   self.assertEqual([r['term_index_in_25'] for r in yearrows],list(range(25)))
 def test_solar_term_longitudes_360_circular(self):
  for row in self.report['individual_source_versus_swiss_term_results']:
   self.assertEqual(row['expected_tropical_sun_longitude_deg'],(row['jieqi_index']*15+270)%360)
 def test_correct_Swiss_ephe_mode_returned_each_event(self):
  self.assertTrue(all(r['swisseph_flags_at_sxtwl'] & 7==2 and r['swisseph_flags_at_swiss_cross'] & 7==2 for r in self.report['individual_source_versus_swiss_term_results']))
 def test_modern_comparison_later_1700_onward_within_20_seconds(self):
  rows=self.report['individual_source_versus_swiss_term_results']
  modern=[r for r in rows if r['source_year_input']>=1700]
  self.assertEqual(len(modern),150)
  self.assertLess(max(abs(r['sxtwl_minus_swiss_solar_term_seconds']) for r in modern),20)
 def test_2024_LiChun_China_clock_UTC8_is_explicit(self):
  row=next(r for r in self.report['individual_source_versus_swiss_term_results'] if r['source_year_input']==2024 and r['term_index_in_25']==0)
  self.assertEqual(row['expected_tropical_sun_longitude_deg'],315)
  self.assertEqual(row['sxtwl_local_CST_UTC_plus_8'][:5],[2024,2,4,16,26])
  self.assertAlmostEqual(row['sxtwl_instant_utc_jd'],row['sxtwl_jd_encoded_in_china_civil_UTC_plus_8']-8/24,places=9)
 def test_ancient_1615_1618_source_anomalies_are_not_hidden(self):
  rows=self.report['anomalies_exceed_60_seconds_all_kept']
  self.assertEqual(len(rows),9)
  self.assertEqual(self.report['anomalies_exceed_60_seconds_count'],9)
  self.assertTrue(all(r['source_year_input'] in (1615,1616,1617,1618) for r in rows))
  self.assertTrue(any(abs(r['sxtwl_minus_swiss_solar_term_seconds'])>170000 for r in rows))
 def test_1616_nextyear_LiChun_source_two_day_internal_disagreement(self):
  source=self.report['cross_year_duplicate_LiChun_consistency_checks']
  a=next(r for r in source if r['first_year']==1616)
  self.assertEqual(a['sxtwl_next_LiChun_inconsistent_duplicate_seconds'],172800)
  self.assertFalse(a['duplicate_source_entries_identical'])
 def test_1615_1617_one_day_internal_disagreements(self):
  source=self.report['cross_year_duplicate_LiChun_consistency_checks']
  for yr in (1615,1617):
   a=next(r for r in source if r['first_year']==yr)
   self.assertEqual(a['sxtwl_next_LiChun_inconsistent_duplicate_seconds'],86400)
 def test_Swiss_solar_cross_nearest_not_next_year(self):
  r=next(r for r in self.report['individual_source_versus_swiss_term_results'] if r['source_year_input']==1616 and r['term_index_in_25']==24)
  self.assertGreater(r['sxtwl_minus_swiss_solar_term_seconds'],172000)
  self.assertLess(r['sxtwl_minus_swiss_solar_term_seconds'],173000)
 def test_pre_1700_not_full_historical_calendar_parity(self):
  self.assertFalse(self.report['original_traditional_time_zone_and_LiChun_hidden_stem_rules_verified'])
  self.assertFalse(self.report['independent_computed_Chinese_birth_four_pillars_or_14_star_palaces_verified'])
 def test_exact_replay_full_report(self):
  self.assertEqual(self.report,build_result(EPHE))
 def test_no_human_predictive_claim_from_250_astro_events(self):
  self.assertEqual(self.report['independent_real_human_predictions_validated'],0)
  self.assertEqual(self.report['runtime_rules_promoted'],0)
if __name__=='__main__':unittest.main()
