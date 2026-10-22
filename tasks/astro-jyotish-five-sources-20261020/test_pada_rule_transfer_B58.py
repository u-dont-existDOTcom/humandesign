import unittest
from pada_rule_transfer_B58 import (SOURCE_TRANSFERS,transferred_condition,
  economic_source_kind,relationship_a7_position,social_king_claim,mixed_means_result)


class B58Transfer(unittest.TestCase):
    def test_four_source_transfers_only(self):
        self.assertEqual(len(SOURCE_TRANSFERS),4)
    def test_12_to_11_changes_relative_house(self):
        t=transferred_condition(parent_rule_id='BPHS29.22',original_house=12,synthetic=True)
        self.assertEqual((t['origin_relative_house'],t['derived_relative_house']),(12,11))
        self.assertFalse(t['separate_score_credit'])
    def test_7_to_2_changes_relative_house(self):
        t=transferred_condition(parent_rule_id='BPHS29.27',original_house=7,synthetic=True)
        self.assertEqual((t['origin_relative_house'],t['derived_relative_house']),(7,2))
    def test_karakamsha_transfer_has_bandhava_exclusion(self):
        t=transferred_condition(parent_rule_id='BPHS29.29',original_house=None,synthetic=True)
        self.assertIn('RELATIVES_OR_BANDHAVA',t['exclusions'])
        self.assertEqual(t['derived_frame'],'KARAKAMSHA')
    def test_other_pada_transfer_not_independent(self):
        t=transferred_condition(parent_rule_id='BPHS29.35',original_house=None,synthetic=True)
        self.assertFalse(t['independently_evidenced_prediction'])
    def test_wrong_house_fails(self):
        with self.assertRaises(ValueError):
            transferred_condition(parent_rule_id='BPHS29.22',original_house=11,synthetic=True)
    def test_unknown_transfer_fails(self):
        with self.assertRaises(ValueError):
            transferred_condition(parent_rule_id='FLEXIBLE_RETROACTIVE_HIT',original_house=12,synthetic=True)
    def test_synthetic_gate(self):
        with self.assertRaises(ValueError):
            transferred_condition(parent_rule_id='BPHS29.27',original_house=7)
    def test_house_adverse_partition(self):
        actual={n for n in range(1,13) if relationship_a7_position(n,synthetic=True)['claim']=='ENMITY_CLAIM_SOURCE_ONLY'}
        self.assertEqual(actual,{6,8,12})
    def test_house_positive_partition(self):
        actual={n for n in range(1,13) if relationship_a7_position(n,synthetic=True)['claim']=='FRIENDSHIP_CLAIM_SOURCE_ONLY'}
        self.assertEqual(actual,{1,4,5,7,9,10})
    def test_three_unspecified_houses(self):
        actual={n for n in range(1,13) if relationship_a7_position(n,synthetic=True)['claim']=='NO_BINARY_29_34_CLAIM'}
        self.assertEqual(actual,{2,3,11})
    def test_king_claim_distinct_ruling_scope(self):
        self.assertTrue(social_king_claim(3,synthetic=True)['29_36_rulership_antecedent'])
        self.assertEqual(relationship_a7_position(3,synthetic=True)['claim'],'NO_BINARY_29_34_CLAIM')
    def test_moral_means_excluded(self):
        self.assertTrue(economic_source_kind('PROFIT_METHOD_MORAL',synthetic=True)['ethically_excluded'])
    def test_spending_not_income_amount(self):
        a=economic_source_kind('EXPENDITURE_CAUSE',synthetic=True)
        b=economic_source_kind('PROFIT_VOLUME',synthetic=True)
        self.assertNotEqual(a['observational_domain'],b['observational_domain'])
        self.assertFalse(a['score_allowed'] or b['score_allowed'])
    def test_mixed_source_one_category(self):
        a=mixed_means_result(('BENEFIC','MALEFIC'),synthetic=True)
        self.assertEqual(a['source_moral_category'],'MIXED')
        self.assertEqual(a['multiple_independent_outcome_counts'],0)
    def test_no_criminal_inferences(self):
        for xs in [('BENEFIC',),('MALEFIC',),('BENEFIC','MALEFIC')]:
            r=mixed_means_result(xs,synthetic=True)
            self.assertFalse(r['person_specific_inference_allowed'] or r['score_allowed'])
    def test_relative_house_bounds(self):
        for x in [-1,0,13,True,1.5]:
            with self.assertRaises(ValueError):relationship_a7_position(x,synthetic=True)
    def test_unknown_moral_category_fails(self):
        with self.assertRaises(ValueError):mixed_means_result(('VERY_GOOD',),synthetic=True)
    def test_source_outcome_must_stay_unscored(self):
        for n in range(1,13):
            self.assertFalse(relationship_a7_position(n,synthetic=True)['score_allowed'])
            self.assertFalse(social_king_claim(n,synthetic=True)['score_allowed'])

if __name__=='__main__':unittest.main()
