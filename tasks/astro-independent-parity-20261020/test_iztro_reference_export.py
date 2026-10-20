"""Independent JavaScript iztro reference data frozen before Python parity scoring."""
import hashlib,json,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
INPUT=HERE/'IZTRO_2_6_3_FROZEN_COMPARISON_INPUT_20261020.json'
OUTPUT=HERE/'IZTRO_2_6_3_EXTERNAL_REFERENCE_1354_CASES_20261020.json'
NAMES={'紫微','天机','太阳','武曲','天同','廉贞','天府','太阴','贪狼','巨门','天相','天梁','七杀','破军'}
class FrozenIndependentIztroReference(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.i=json.loads(INPUT.read_text());cls.o=json.loads(OUTPUT.read_text())
 def test_01_frozen_inputs_sha_identical(self):
  self.assertEqual(hashlib.sha256(INPUT.read_bytes()).hexdigest(),'cbad83855602700f6835b3ff48e2a27f4868575e6e2e8de46a3e1a80d73f8299')
  self.assertEqual(self.o['frozen_input_manifest_sha256'],hashlib.sha256(INPUT.read_bytes()).hexdigest())
 def test_02_reference_export_sha_and_version(self):
  self.assertEqual(hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'015cbd9f26679c7a1ccd60aa15d6491c38647f8e4af73dcca19f13e762079b21')
  self.assertEqual(self.o['independent_library_version'],'2.6.3')
  self.assertTrue(self.o['npm_package_tarball_integrity'].startswith('sha512-'))
 def test_03_all_1354_independent_calculator_outputs(self):
  self.assertEqual(self.o['synthetic_input_count'],1354)
  self.assertEqual(len(self.o['outputs']),len(self.i['cases']))
 def test_04_reference_cases_match_frozen_input_one_to_one(self):
  for idx,(a,b) in enumerate(zip(self.o['outputs'],self.i['cases'])):
   self.assertEqual(a['index'],idx)
   self.assertEqual(a['synthetic_label'],b['synthetic_label'])
   self.assertEqual(a['input_fixed_CST'],b['local_CST_fixed_timestamp'])
   self.assertEqual(a['input_solar_date'],b['solar_date_for_Iztro'])
   self.assertEqual(a['hour_index_used'],b['timeIndex_0_to_12'])
 def test_05_each_reference_contains_exact_fourteen_principal_stars(self):
  for r in self.o['outputs']:
   self.assertEqual(set(r['fourteen_major_star_original_chinese_name_to_palace']),NAMES)
 def test_06_all_source_earthly_branches_wellformed(self):
  branches=set('子丑寅卯辰巳午未申酉戌亥')
  for r in self.o['outputs']:
   self.assertEqual(len(r['reference_life_branch']),1)
   self.assertIn(r['reference_life_branch'],branches)
   self.assertIn(r['reference_body_branch'],branches)
   self.assertTrue(set(r['fourteen_major_star_original_chinese_name_to_palace'].values())<=branches)
 def test_07_calendar_leap_scenarios_all_retained(self):
  labels={r['synthetic_label'] for r in self.o['outputs']}
  self.assertIn('leap_second_month_2023',labels)
  self.assertIn('2024_lateZi_2330',labels)
  self.assertIn('2024_exact_LiChun_1626',labels)
  self.assertIn('2024_exact_LiChun_1630',labels)
 def test_08_no_real_participant_results(self):
  self.assertEqual(self.o['real_human_response_outcomes_scored'],0)
  self.assertEqual(self.o['runtime_astrological_rules_promoted'],0)
if __name__=='__main__':unittest.main()
