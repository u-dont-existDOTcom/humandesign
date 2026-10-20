"""Source uncertainty-aware ZiWei/TianFu lookup for given lunar day & bureau only."""
import json,unittest
from pathlib import Path
from ziwei_original_bureau_candidate import candidate_given_bureau_day,sample_source_decisions,BUREAUS
from ziwei_tianfu_relative import tianfu_from_ziwei
HERE=Path(__file__).resolve().parent
class ZiWeiGivenBureauSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.saved=json.loads((HERE/'ZIWEI_SOURCE_CONDITIONAL_150_DAY_PLACEMENTS_20261020.json').read_text())
 def test_01_exact_five_source_bureaus(self):self.assertEqual(BUREAUS,{'水二局':2,'木三局':3,'金四局':4,'土五局':5,'火六局':6})
 def test_02_all_150_conditions_retained(self):
  self.assertEqual(self.saved['source_lookup_decisions'],150)
  self.assertEqual(len(self.saved['all_150_source_conditional_lookup_records']),150)
 def test_03_unknown_source_bureau_fail_closed(self):
  for b in ('','Water Two','Ming',None):
   with self.assertRaises(ValueError):candidate_given_bureau_day(b,1)
 def test_04_invalid_lunar_days_fail_closed(self):
  for d in (0,31,-2,'5',5.0,True,False,None):
   with self.assertRaises(ValueError):candidate_given_bureau_day('水二局',d)
 def test_05_single_source_cell_status_is_not_chart_parity(self):
  v=candidate_given_bureau_day('水二局',1)
  self.assertEqual(v.source_literal_status,'SINGLE_TRANSMITTED_SOURCE_LABEL_NOT_VALIDATED_BIRTH_CHART')
  self.assertIsNotNone(v.literal_ziwei_branch_if_single_source_label)
  self.assertEqual(v.derived_tianfu_branch_if_single_ziwei_label,tianfu_from_ziwei(v.literal_ziwei_branch_if_single_source_label))
  self.assertFalse(v.independently_confirmed_ziwei_14_star_birthday_chart)
 def test_06_wood_source_duplicate_day9_has_no_guessed_star(self):
  v=candidate_given_bureau_day('木三局',9)
  self.assertEqual(v.source_literal_status,'AMBIGUOUS_SOURCE_DUPLICATE')
  self.assertEqual(v.printed_duplicate_ziwei_candidate_branches,('Chen','Yin'))
  self.assertIsNone(v.literal_ziwei_branch_if_single_source_label)
  self.assertIsNone(v.derived_tianfu_branch_if_single_ziwei_label)
 def test_07_wood_source_day5_missing_not_guessed(self):
  v=candidate_given_bureau_day('木三局',5)
  self.assertEqual(v.source_literal_status,'UNRESOLVED_SOURCE_MISSING_DAY')
  self.assertIsNone(v.literal_ziwei_branch_if_single_source_label)
 def test_08_metal_source_day30_missing_not_guessed(self):
  v=candidate_given_bureau_day('金四局',30)
  self.assertEqual(v.source_literal_status,'UNRESOLVED_SOURCE_MISSING_DAY')
  self.assertIsNone(v.derived_tianfu_branch_if_single_ziwei_label)
 def test_09_three_bureaus_complete_30_lunar_days_in_transcription(self):
  for b in ('水二局','土五局','火六局'):
   for d in range(1,31):
    self.assertEqual(candidate_given_bureau_day(b,d).source_literal_status,'SINGLE_TRANSMITTED_SOURCE_LABEL_NOT_VALIDATED_BIRTH_CHART')
 def test_10_147_unique_1_duplicate_2_missing(self):
  self.assertEqual(self.saved['status_counts'],{'AMBIGUOUS_SOURCE_DUPLICATE':1,'SINGLE_TRANSMITTED_SOURCE_LABEL_NOT_VALIDATED_BIRTH_CHART':147,'UNRESOLVED_SOURCE_MISSING_DAY':2})
 def test_11_exact_saved_report_reproduces(self):
  self.assertEqual(self.saved,json.loads(json.dumps(sample_source_decisions(),ensure_ascii=False)))
 def test_12_no_human_validation_from_source_grid_match(self):
  self.assertEqual(self.saved['actual_person_predictions_validated'],0)
  self.assertEqual(self.saved['runtime_promotions'],0)
 def test_13_unverified_ancient_print_and_bureau_derivation(self):
  self.assertFalse(self.saved['original_Ming_print_verified'])
  self.assertFalse(self.saved['birth_year_and_life_palace_to_elemental_bureau_verified'])
  self.assertFalse(self.saved['independent_14_star_chart_parity_verified'])
 def test_14_source_occurrences_same_1963110(self):
  self.assertEqual({r['source_original_full_document_revision'] for r in self.saved['all_150_source_conditional_lookup_records']},{1963110})
if __name__=='__main__':unittest.main()
