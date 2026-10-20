"""Only reproducible modern CST historical-source chart fragments; keep policy ambiguity."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from partial_chinese_chart_candidates import CHINA_CIVIL_FIXED_UTC_PLUS8
from ziwei_nayin_bureau_source import conditional_source_bureau
from ziwei_partial_source_pipeline import one_sample,build_result,TEST_CASES
from ziwei_original_bureau_candidate import candidate_given_bureau_day
HERE=Path(__file__).resolve().parent
class ZiWeiPartialSourcePipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved=json.loads((HERE/'ZIWEI_PARTIAL_END_TO_END_10_SYNTHETIC_CHARTS_20261020.json').read_text())
        cls.cases={c['synthetic_calendar_case_label']:c for c in cls.saved['scenarios']}
    def test_01_source_only_10_cases(self):
        self.assertEqual(self.saved['sample_count'],10)
        self.assertEqual(len(self.saved['scenarios']),10)
        self.assertEqual(len(set(self.cases)),10)
        self.assertEqual(len(TEST_CASES),10)
    def test_02_both_year_selection_policies_present(self):
        for case in self.saved['scenarios']:
            self.assertEqual(set(case['two_unmerged_natal_year_conventions']),
              {'natal_lunar_new_year_convention','natal_LiChun_convention'})
    def test_03_three_explicit_calendar_year_ambiguous_examples(self):
        self.assertEqual(self.saved['year_policy_ambiguity_sample_count'],3)
        titles={k for k,v in self.cases.items() if v['different_source_year_policy_or_star_position']}
        self.assertEqual(titles,{
           'LiChun_2024_after_term_minutes',
           'LiChun_2024_next_day_before_lunar_newyear',
           'late_Zi_2024_unresolved_day_change'})
    def test_04_before_LiChun_year_conventions_agree(self):
        example=self.cases['LiChun_2024_before_solar_term_noon']
        self.assertFalse(example['different_source_year_policy_or_star_position'])
    def test_05_lunar_year_not_silently_replaced_with_LiChun(self):
        case=self.cases['LiChun_2024_next_day_before_lunar_newyear']
        lunar=case['two_unmerged_natal_year_conventions']['natal_lunar_new_year_convention']
        term=case['two_unmerged_natal_year_conventions']['natal_LiChun_convention']
        self.assertNotEqual(lunar['source_birth_year_stem_as_provided_under_this_convention'],
            term['source_birth_year_stem_as_provided_under_this_convention'])
        self.assertNotEqual(lunar['source_NaYin_bureau']['derived_source_palace_sexagenary_name'],
            term['source_NaYin_bureau']['derived_source_palace_sexagenary_name'])
    def test_06_after_2024_newyear_same_yearpolicy_again(self):
        example=self.cases['after_2024_lunar_newyear']
        self.assertFalse(example['different_source_year_policy_or_star_position'])
    def test_07_leap_month_source_leap_month_policy_explicit(self):
        c=self.cases['intercalary_second_month_2023']['calendar_candidate']
        self.assertTrue(c['source_lunar_leap_month'])
        self.assertEqual(c['ziwei_month_for_palace_rule'],3)
        self.assertEqual(c['lunar_ymd'],[2023,2,1])
    def test_08_source_bureau_pipeline_can_be_independently_reproduced(self):
        for case in self.saved['scenarios']:
            cal=case['calendar_candidate']
            for policy,x in case['two_unmerged_natal_year_conventions'].items():
                r=conditional_source_bureau(x['source_birth_year_stem_as_provided_under_this_convention'],
                                            cal['ziwei_life_palace_partial'])
                self.assertEqual(x['source_NaYin_bureau']['source_conditional_bureau_Chinese'],r.source_conditional_bureau_Chinese)
                if r.source_conditional_bureau_Chinese:
                    got=candidate_given_bureau_day(r.source_conditional_bureau_Chinese,cal['lunar_ymd'][2])
                    self.assertEqual(got.literal_ziwei_branch_if_single_source_label,
                           x['possible_ziwei_palace_as_original_transmitted_source_only'])
                    self.assertEqual(got.derived_tianfu_branch_if_single_ziwei_label,
                           x['possible_tianfu_palace_as_original_transmitted_source_only'])
    def test_09_strict_unresolved_glyph_in_non_demo_case_is_not_filled(self):
        x=conditional_source_bureau('Jia','Xu')
        self.assertIsNone(x.source_conditional_bureau_Chinese)
    def test_10_original_claimed_birthhour_bureau_parity_not_overstated(self):
        self.assertFalse(self.saved['full_natal_14_star_chart_and_timing_computation_verified'])
        self.assertFalse(self.saved['birth_place_and_historical_time_zone_normalization_verified'])
        self.assertFalse(self.saved['full_original_LiChun_calendar_source_policy_expert_validated'])
    def test_11_1616_historical_date_rejected_as_modern_CST(self):
        with self.assertRaisesRegex(ValueError,'scoped to post-1970'):
            one_sample('not_admissible_1616',1616,9,29,12,0)
    def test_12_no_human_posterior_fit_or_runtime_rule_promotion(self):
        self.assertEqual(self.saved['personal_life_or_illness_predictions_made'],0)
        self.assertEqual(self.saved['independent_real_human_predictions_validated'],0)
        self.assertEqual(self.saved['runtime_model_promotions'],0)
    def test_13_exact_saved_result_recomputes(self):
        self.assertEqual(self.saved,json.loads(json.dumps(build_result(),ensure_ascii=False)))
if __name__=='__main__':
    unittest.main()
