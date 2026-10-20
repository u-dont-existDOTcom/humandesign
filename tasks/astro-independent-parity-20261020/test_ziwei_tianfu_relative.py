"""Conditioned source map is not natal birth calculation or outcome evidence."""
import json,unittest
from pathlib import Path
from ziwei_tianfu_relative import (source_witness,source_conditional_map,tianfu_from_ziwei,BRANCHES)
HERE=Path(__file__).resolve().parent
class ZiWeiTianFuSourceConditional(unittest.TestCase):
 def test_original_transmitted_source_sha_recovered(self):
  r=source_witness();self.assertEqual(r['original_oldid'],1963110)
  self.assertEqual(len(r['original_Chinese_excerpt_sha256']),64)
 def test_source_original_not_authenticated_physical(self):self.assertFalse(source_witness()['independent_physical_early_edition_authenticated'])
 def test_tianfu_ziweigiven_chou_corresponds_mao(self):self.assertEqual(tianfu_from_ziwei('Chou'),'Mao')
 def test_tianfu_in_yin_same_palace(self):self.assertEqual(tianfu_from_ziwei('Yin'),'Yin')
 def test_tianfu_in_shen_same_palace(self):self.assertEqual(tianfu_from_ziwei('Shen'),'Shen')
 def test_reflection_has_exactly_two_fixed_points(self):self.assertEqual({b for b in BRANCHES if tianfu_from_ziwei(b)==b},{'Yin','Shen'})
 def test_reflection_is_involution(self):
  for b in BRANCHES:self.assertEqual(tianfu_from_ziwei(tianfu_from_ziwei(b)),b)
 def test_reflection_is_permutation_of_twelve(self):self.assertEqual(set(tianfu_from_ziwei(b) for b in BRANCHES),set(BRANCHES))
 def test_all_twelve_map_explicit(self):
  expected={'Zi':'Chen','Chou':'Mao','Yin':'Yin','Mao':'Chou','Chen':'Zi','Si':'Hai','Wu':'Xu','Wei':'You','Shen':'Shen','You':'Wei','Xu':'Wu','Hai':'Si'}
  self.assertEqual({b:tianfu_from_ziwei(b) for b in BRANCHES},expected)
 def test_unknown_branch_not_silently_defaulted(self):
  for x in ('',None,'Capricorn','寅'):
   with self.assertRaises(ValueError):tianfu_from_ziwei(x)
 def test_exact_report_matches_recomputed(self):
  report=json.loads((HERE/'ZIWEI_TIANFU_CONDITIONAL_MAP_20261020.json').read_text())
  self.assertEqual(report,source_conditional_map())
 def test_no_full_birth_ZiWei_star_engine(self):
  x=source_conditional_map();self.assertFalse(x['ziwei_principal_star_birth_palace_known_from_calendar']);self.assertFalse(x['can_generate_fourteen_principal_stars'])
 def test_no_human_data_or_runtime_promotions(self):
  r=source_conditional_map();self.assertEqual(r['human_outcomes_and_predictions_validated'],0);self.assertEqual(r['runtime_astrology_promotions'],0)
if __name__=='__main__':unittest.main()
