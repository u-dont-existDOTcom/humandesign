"""Modern JPL vs Swiss SAME TT; preserve nominal pre-UTC anomaly, no human prediction."""
import json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from jpl_swiss_planetary_parity import build_result,verify_binaries,JPL_KERNEL_BYTES,JPL_KERNEL_SHA256
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;EPHE=ROOT/'data/ephemeris';KERNEL=EPHE/'de440s.bsp'
class TwoAstronomyImplementationParity(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.report=json.loads((HERE/'PLANETARY_JPL_VS_SWISS_20261020.json').read_text());c.rows=c.report['planetary_comparison_records']
 def test_original_NASA_DE440s_exact_SHA_bytes(self):
  self.assertTrue(KERNEL.is_file());self.assertEqual(KERNEL.stat().st_size,JPL_KERNEL_BYTES)
  self.assertEqual(self.report['JPL_original_DE440s_SHA256'],JPL_KERNEL_SHA256)
  verify_binaries(EPHE,KERNEL)
 def test_no_fake_JPL_file_allowed(self):
  with TemporaryDirectory() as p:
   with self.assertRaisesRegex(ValueError,'JPL DE440s'):
    verify_binaries(EPHE,Path(p)/'de440s.bsp')
 def test_original_Swiss_18_files_exact(self):
  self.assertEqual(set(self.report['Swiss_ephemeris_1900_plus_files_SHA_and_bytes']),{'sepl_18.se1','semo_18.se1'})
  self.assertTrue(all(len(x['sha256'])==64 for x in self.report['Swiss_ephemeris_1900_plus_files_SHA_and_bytes'].values()))
 def test_five_UTC_sample_labels_seven_planets(self):
  self.assertEqual(self.report['total_independent_planet_comparisons'],35)
  self.assertEqual(len(self.report['sample_nominal_UT1_dates_labeled_UTC_for_modern_software']),5)
  self.assertEqual({r['planet'] for r in self.rows},{'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn'})
 def test_same_TT_geocentric_apparent_tropical_agreement_sub_arcsec(self):
  self.assertLess(self.report['max_absolute_matched_TT_longitude_difference_arcseconds'],0.01)
  self.assertLess(self.report['median_absolute_matched_TT_longitude_difference_arcseconds'],0.005)
  self.assertEqual(self.report['matched_TT_disagreements_over_one_arcsecond'],[])
 def test_all_comparisons_use_actual_Swiss_ephemeris_files(self):
  self.assertTrue(all((r['Swiss_returned_ephemeris_flags'] & 7)==2 for r in self.rows))
  self.assertTrue(all(r['Swiss_returned_mode']=='SWIEPH' for r in self.rows))
 def test_1900_UTC_vs_UT1_comparison_ambiguity_explicit(self):
  moon=next(r for r in self.rows if r['utc_timestamp'].startswith('1900') and r['planet']=='Moon')
  self.assertGreater(moon['abs_naive_UTC_comparison_arcseconds'],26)
  self.assertLess(moon['abs_matched_TT_longitude_difference_arcseconds'],0.01)
  self.assertGreater(moon['skyfield_nominal_UTC_TT_minus_Swiss_UT1_TT_seconds'],40)
  self.assertLess(moon['skyfield_nominal_UTC_TT_minus_Swiss_UT1_TT_seconds'],50)
 def test_naive_UTC_mismatches_preserved_not_hidden(self):
  bad=self.report['naive_UTC_vs_UT1_disagreements_over_one_arcsecond']
  self.assertEqual(len(bad),5)
  self.assertTrue(all(x['utc_timestamp'].startswith('1900') for x in bad))
  self.assertGreater(self.report['max_naive_UTC_vs_Swiss_UT1_mismatch_arcseconds'],26)
 def test_1985_Moon_same_TT_better_than_nominal_UTC(self):
  m=next(r for r in self.rows if r['utc_timestamp'].startswith('1985') and r['planet']=='Moon')
  self.assertLess(m['abs_matched_TT_longitude_difference_arcseconds'],m['abs_naive_UTC_comparison_arcseconds'])
 def test_mars_jupiter_saturn_barycenter_not_mislabeled_planet_center(self):
  for r in self.rows:
   self.assertEqual(r['JPL_target_type'],'barycenter' if r['planet'] in ('Mars','Jupiter','Saturn') else 'center')
 def test_kernel_range_excludes_1616_historical_case(self):
  self.assertIn('EXCLUDES 1616',self.report['JPL_DE440s_coverage'])
  self.assertFalse(self.report['historical_1616_original_natal_ephemeris_independently_parity_verified'])
 def test_report_recomputes_exact_with_same_versions_binaries(self):
  self.assertEqual(self.report,build_result(EPHE,KERNEL))
 def test_no_chart_events_or_actual_person_validation(self):
  self.assertFalse(self.report['Regiomontanus_houses_lunar_calendar_14_stars_and_timing_full_parity_verified'])
  self.assertEqual(self.report['prospective_blinded_human_predictive_results'],0)
  self.assertEqual(self.report['runtime_model_promotions'],0)
if __name__=='__main__':unittest.main()
