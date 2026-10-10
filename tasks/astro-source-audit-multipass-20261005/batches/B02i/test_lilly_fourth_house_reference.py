"""Check source-context boundaries and omission behavior, not predictions."""
import unittest

import lilly_fourth_house_reference as reference


class ContextTests(unittest.TestCase):
    def test_property_question_selects_the_tenth_house_meaning(self):
        frames = [reference.property_frame(s)['roles']['tenth']
                  for s in ('purchase', 'rental', 'land_quality')]
        self.assertIn('Price', frames[0])
        self.assertIn('Profit', frames[1])
        self.assertIn('Timber', frames[2])
        with self.assertRaises(ValueError): reference.property_frame('property')

    def test_goods_owner_examples_do_not_invent_unlisted_relations(self):
        self.assertEqual(reference.goods_house('father')['radical_house'], 5)
        self.assertEqual(reference.goods_house('mother')['radical_house'], 11)
        self.assertEqual(reference.goods_house('sibling')['radical_house'], 4)
        self.assertFalse(reference.goods_house('own')['later_second_lord_substitution_automated'])
        with self.assertRaises(ValueError): reference.goods_house('spouse')

    def test_direction_and_rain_lists_preserve_unusual_source_members(self):
        self.assertEqual(reference.sign_direction('Leo')['verbal_direction'], 'east by north')
        self.assertEqual(reference.sign_direction('Virgo')['verbal_direction'], 'south by west')
        self.assertIsNone(reference.sign_direction('Aries')['bearing_degrees'])
        self.assertIn('Leo', reference.RAIN_SIGNS)
        self.assertNotIn('Scorpio', reference.RAIN_SIGNS)


class TestimonyTests(unittest.TestCase):
    def slots(self):
        signs = ('Aries','Libra','Cancer','Capricorn')*2
        return {key:{'sign':sign} for key,sign in zip(reference.MISLAID_SLOTS,signs)}

    def test_four_way_tie_has_no_hidden_winner(self):
        result = reference.mislaid_direction_tally(self.slots())
        self.assertEqual(result['quarter_counts'], {'east':2,'west':2,'north':2,'south':2})
        self.assertTrue(result['unresolved_tie'])
        self.assertEqual(len(result['largest_count_quarters']), 4)
        self.assertIsNone(result['location_prediction'])

    def test_missing_or_extra_slot_rejected_instead_of_silent_rescaling(self):
        omitted = self.slots(); omitted.pop('PartOfFortune')
        extra = self.slots(); extra['TenthCusp'] = {'sign':'Aries'}
        for slots in (omitted,extra):
            with self.assertRaises(ValueError): reference.mislaid_direction_tally(slots)

    def test_repeated_body_roles_remain_visible_without_independence_claim(self):
        slots = self.slots()
        slots['AscendantLord'] = {'sign':'Cancer','body':'Moon'}
        slots['Moon'] = {'sign':'Cancer','body':'Moon'}
        result = reference.mislaid_direction_tally(slots)
        self.assertEqual(result['source_slots_counted'], 8)
        self.assertEqual(result['quarter_counts']['north'], 4)
        self.assertEqual(result['shared_body_slots']['Moon'], ['AscendantLord','Moon'])
        self.assertIsNone(result['independent_evidence_count'])

    def test_contradictory_positions_for_one_body_are_rejected(self):
        slots = self.slots()
        slots['AscendantLord'] = {'sign':'Cancer','body':'Moon'}
        slots['Moon'] = {'sign':'Virgo','body':'Moon'}
        with self.assertRaises(ValueError): reference.mislaid_direction_tally(slots)


class QualitativeBoundaryTests(unittest.TestCase):
    def test_depth_is_ordinal_without_physical_units_or_degree_bins(self):
        result = reference.depth_order(1,1799)
        self.assertEqual(result['ordinal_relation'], 'second deeper')
        self.assertIsNone(result['physical_depth'])
        self.assertIsNone(result['shallow_deep_threshold'])
        self.assertIsNone(result['units'])
        self.assertEqual(reference.depth_order(300,300)['ordinal_relation'], 'same sign progress')
        for bad in (1800,-1,True,None):
            with self.assertRaises(ValueError): reference.depth_order(bad,0)

    def test_ancient_hour_lord_gap_is_not_filled(self):
        data = reference.reference_inventory()['ancient_hour_lord_rule']
        self.assertEqual(data['source_first_branch_houses'], [10,11])
        self.assertIsNone(data['house_twelve_coverage'])
        self.assertIsNone(data['angular_endpoint_policy'])
        self.assertIsNone(data['complete_house_mapping'])


if __name__ == '__main__': unittest.main()
