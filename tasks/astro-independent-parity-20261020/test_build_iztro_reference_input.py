"""Fixed engineering parity input, no outcome-based exclusions or person labels."""
import json,unittest
from pathlib import Path
from build_iztro_reference_input import build,hour_index,RESEARCH_SAMPLES,YEARS,MONTHS,DAYS,HOURS
HERE=Path(__file__).resolve().parent
class IztroSyntheticGridFreeze(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.saved=json.loads((HERE/'IZTRO_2_6_3_FROZEN_COMPARISON_INPUT_20261020.json').read_text())
 def test_count(self):
  self.assertEqual(self.saved['development_fixture_count'],10)
  self.assertEqual(self.saved['predeclared_grid_case_count'],1344)
  self.assertEqual(self.saved['total_predeclared_cases'],1354)
  self.assertEqual(len(self.saved['cases']),1354)
 def test_grid_deterministic(self):self.assertEqual(self.saved,build())
 def test_hour_index_including_late_zi(self):
  self.assertEqual(hour_index(0),0)
  self.assertEqual(hour_index(12),6)
  self.assertEqual(hour_index(23),12)
  with self.assertRaises(ValueError):hour_index(24)
 def test_all_synthetic_labels_unique(self):self.assertEqual(len({q['synthetic_label'] for q in self.saved['cases']}),1354)
 def test_10_development_is_preexisting_cases(self):
  self.assertEqual([q['synthetic_label'] for q in self.saved['cases'][:10]],[q[0] for q in RESEARCH_SAMPLES])
 def test_grid_dates_each_year_month_day_hour(self):
  q=self.saved['cases'][10:]
  self.assertEqual(len(q),len(YEARS)*len(MONTHS)*len(DAYS)*len(HOURS))
  self.assertEqual(set(x['split'] for x in q),{'PREDECLARED_SYNTHETIC_GRID_PARITY'})
 def test_user_private_outcome_data_not_collected(self):
  self.assertTrue(self.saved['inputs_are_anonymous_synthetic_calendar_cases'])
  self.assertEqual(self.saved['synthetic_personal_predictive_results'],0)
 def test_minutes_cannot_be_inferred_by_iztro_reference(self):
  cs=self.saved['cases'][:10]
  self.assertTrue(cs[3]['calendar_clock_minutes_discarded_by_iztro_hour_branch_API'])
  self.assertTrue(cs[4]['calendar_clock_minutes_discarded_by_iztro_hour_branch_API'])
  self.assertTrue(cs[6]['calendar_clock_minutes_discarded_by_iztro_hour_branch_API'])
if __name__=='__main__':unittest.main()
