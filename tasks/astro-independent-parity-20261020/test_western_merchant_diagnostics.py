"""Original 1616 Lilly chart diagnostic, not a human/outcome/natal parity assertion."""
import json,sys,unittest
from pathlib import Path
from datetime import datetime,UTC
from tempfile import TemporaryDirectory
from western_merchant_diagnostics import verify_inputs, build_result, angular_signed_delta_deg
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
EPHE=ROOT/'data/ephemeris'
sys.path.insert(0,str(ROOT/'src'))
class Lilly1616SourceCalendarDiagnostic(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads((HERE/'LILLY_1616_DUAL_CALENDAR_SWIEPH_20261020.json').read_text())
  cls.jul=cls.report['julian_source_date_interpretation'];cls.greg=cls.report['literal_Gregorian_source_date_interpretation']
 def test_four_original_immutable_swiss_source_files(self):
  self.assertEqual(len(verify_inputs(EPHE)),4)
 def test_fail_closed_if_original_swiss_files_absent(self):
  with TemporaryDirectory() as tmp:
   with self.assertRaisesRegex(ValueError,'Swiss file missing/changed'):
    verify_inputs(tmp)
 def test_historical_printed_date_not_independently_confirmed(self):
  self.assertFalse(self.report['original_calendar_style_resolved'])
  self.assertFalse(self.report['original_place_longitude_verified'])
  self.assertFalse(self.report['LMT_to_UT_offset_known'])
 def test_julian_original_date_converts_to_gregorian_ten_days_ahead(self):
  self.assertEqual(self.report['julian_to_gregorian_1616_calendar_days_difference'],10)
  self.assertEqual(self.report['julian_1616_09_19_JD_UT'],self.report['gregorian_1616_09_29_same_JD_UT'])
  self.assertAlmostEqual(self.report['julian_1616_09_19_JD_UT']-self.report['literal_gregorian_1616_09_19_JD_UT'],10.0,places=6)
 def test_julian_sun_near_printed_but_not_exact(self):
  sun=next(row for row in self.jul['planet_rows'] if row['body']=='Sun')
  self.assertEqual(sun['printed_first_original_zodiac_sign'],'Libra')
  self.assertEqual((sun['printed_first_original_zodiac_degree'],sun['printed_first_original_zodiac_minute']),(6,37))
  self.assertGreater(sun['absolute_error_arcmin'],6)
  self.assertLess(sun['absolute_error_arcmin'],8)
 def test_gregorian_reading_sharply_worse_for_solar_source(self):
  gregsun=next(row for row in self.greg['planet_rows'] if row['body']=='Sun')
  julsun=next(row for row in self.jul['planet_rows'] if row['body']=='Sun')
  self.assertGreater(gregsun['absolute_error_arcmin'],500)
  self.assertLess(julsun['absolute_error_arcmin'],10)
 def test_seven_historical_planet_comparisons_preserve_misses(self):
  self.assertEqual(len(self.jul['planet_rows']),7)
  self.assertFalse(self.jul['printed_comparison_summary']['all_seven_printed_positions_agree_within_one_arcminute'])
  mercury=next(row for row in self.jul['planet_rows'] if row['body']=='Mercury')
  venus=next(row for row in self.jul['planet_rows'] if row['body']=='Venus')
  self.assertGreater(mercury['absolute_error_arcmin'],90)
  self.assertGreater(venus['absolute_error_arcmin'],60)
 def test_all_seven_swisseph_file_flags_returned_not_moshier(self):
  self.assertTrue(all(r['actual_returned_swiss_flags'] & 7==2 for r in self.jul['planet_rows']+self.greg['planet_rows']))
  self.assertTrue(all(r['returned_ephemeris_mode']=='SWIEPH' for r in self.jul['planet_rows']+self.greg['planet_rows']))
 def test_illustrative_regiomontanus_twelve_house_antisymmetry(self):
  h=self.jul['regiomontanus_assumed_0E_lat53'];c=h['cusp_longitudes_deg']
  self.assertEqual(len(c),12)
  self.assertEqual(h['house_system'],'Regiomontanus (R)')
  self.assertAlmostEqual(c[0],h['asc_longitude_deg'],places=7)
  self.assertAlmostEqual(c[9],h['mc_longitude_deg'],places=7)
  for i in range(6):self.assertAlmostEqual(abs(angular_signed_delta_deg(c[i],c[i+6])),180.0,places=6)
 def test_swe_houses_same_library_only(self):
  h=self.jul['regiomontanus_assumed_0E_lat53']
  self.assertTrue(h['Swiss_houses_ex_vs_houses_agree_same_library_only'])
  self.assertFalse(h['independently_verified_against_1616_printed_house_table'])
 def test_raw_Swiss_adapter_source_mode_consistency_not_external_parity(self):
  from hdmatch.chart.ephemeris import SwissEphemerisProvider,CelestialBody
  provider=SwissEphemerisProvider((EPHE/'sepl_12.se1',EPHE/'semo_12.se1'))
  pos=provider.position(CelestialBody.SUN,datetime(1616,9,29,14,24,39,tzinfo=UTC))
  raw=next(x['computed_tropical_geocentric_longitude_deg'] for x in self.jul['planet_rows'] if x['body']=='Sun')
  self.assertAlmostEqual(raw,pos.longitude,places=8)
 def test_report_recomputes_exactly(self):
  current=build_result(EPHE)
  self.assertEqual(self.report,current)
 def test_not_an_experiment_or_runtime_promotion(self):
  self.assertFalse(self.report['old_historical_source_year_natal_chart_parity_verified'])
  self.assertFalse(self.report['independent_second_astronomical_algorithm_compared'])
  self.assertEqual(self.report['empirical_human_outcomes_or_predictions_validated'],0)
  self.assertEqual(self.report['runtime_astro_rules_promoted'],0)
if __name__=='__main__':unittest.main()
