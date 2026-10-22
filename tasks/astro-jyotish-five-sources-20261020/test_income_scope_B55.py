import unittest
from income_scope_B55 import (printed_gain_loss_premises, printed_income_means,
                              source_lord_vs_occupant, compare_event_targets,
                              target_types, Witness, verse_locator_binding)

class IncomeScopeB55(unittest.TestCase):
    def _wealth(self, a=False, b=False, c=False):
        return printed_gain_loss_premises(lord11_kendra_or_trikona=a,
                                         malefic_in_11th=b,
                                         lord11_favorable_sign_or_amsa=c,
                                         synthetic=True)
    def test_malefic_eleventh_activates_opposites_in_sarvartha(self):
        r=self._wealth(b=True)
        self.assertTrue(r['SC_11_v2_gain'] and r['SC_11_v10_loss'] and r['source_collision_SC'])
        self.assertFalse(r['score_allowed'])
    def test_jataka_gain_does_not_resolve_sarvartha_conflict(self):
        r=self._wealth(b=True)
        self.assertTrue(r['JP_XV_v72_gain'] and r['source_collision_SC'])
        self.assertIsNone(r['canon_rule'])
    def test_unique_jataka_dignity_alternative(self):
        r=self._wealth(c=True)
        self.assertTrue(r['JP_XV_v72_gain'])
        self.assertFalse(r['SC_11_v2_gain'] or r['SC_11_v10_loss'])
    def test_jataka_semantic_parallel_not_identical_witness(self):
        self.assertTrue(self._wealth(a=True)['parallel_predicate_not_verbatim_sanskrit'])
    def test_wealth_argument_validation(self):
        with self.assertRaises(TypeError):
            printed_gain_loss_premises(lord11_kendra_or_trikona=False,
                                       malefic_in_11th=1, lord11_favorable_sign_or_amsa=False,
                                       synthetic=True)
    def test_synthetic_gate(self):
        with self.assertRaises(ValueError):
            printed_gain_loss_premises(lord11_kendra_or_trikona=True,
                                       malefic_in_11th=False,lord11_favorable_sign_or_amsa=False)
    def test_11th_moral_class_favorable(self):
        x=printed_income_means(benefic_occupants=1,malefic_occupants=0,synthetic=True)
        self.assertEqual(x['archival_evaluative_class'],'FAVORABLE_MEANS')
        self.assertIsNone(x['quantitative_wealth_prediction'])
    def test_11th_moral_class_unfavorable(self):
        x=printed_income_means(benefic_occupants=0,malefic_occupants=1,synthetic=True)
        self.assertEqual(x['archival_evaluative_class'],'UNFAVORABLE_MEANS')
        self.assertFalse(x['personal_moral_allegation_allowed'])
    def test_11th_moral_class_explicit_mixed_case(self):
        x=printed_income_means(benefic_occupants=1,malefic_occupants=1,synthetic=True)
        self.assertEqual(x['archival_evaluative_class'],'MIXED_MEANS')
        self.assertFalse(x['score_allowed'])
    def test_no_occupants_and_invalid(self):
        self.assertEqual(printed_income_means(benefic_occupants=0,malefic_occupants=0,synthetic=True)['archival_evaluative_class'],'NO_OCCUPANTS')
        with self.assertRaises(ValueError):
            printed_income_means(benefic_occupants=-1,malefic_occupants=0,synthetic=True)
        with self.assertRaises(ValueError):
            printed_income_means(benefic_occupants=0,malefic_occupants=True,synthetic=True)
    def test_11th_house_owner_not_occupant(self):
        x=source_lord_vs_occupant(eleventh_lord='Sun',eleventh_occupants=('Saturn',),synthetic=True)
        self.assertEqual(x['JP_XV_v71_lord_indicator'],'Sun')
        self.assertEqual(x['JP_XV_v67_v68_occupant_indicators'],['Saturn'])
        self.assertFalse(x['indicators_have_same_role_by_definition'])
    def test_same_planet_still_distinct_indicatory_roles(self):
        x=source_lord_vs_occupant(eleventh_lord='Sun',eleventh_occupants=('Sun',),synthetic=True)
        self.assertTrue(x['lord_equals_every_occupant'])
        self.assertFalse(x['indicators_have_same_role_by_definition'])
    def test_occupant_validation(self):
        with self.assertRaises(ValueError):
            source_lord_vs_occupant(eleventh_lord='Uranus',eleventh_occupants=('Saturn',),synthetic=True)
        with self.assertRaises(ValueError):
            source_lord_vs_occupant(eleventh_lord='Venus',eleventh_occupants=('Sun','Sun'),synthetic=True)
    def test_foreign_trade_and_residence_are_different(self):
        x=compare_event_targets('FOREIGN_TRADE_ACTIVITY','FOREIGN_RESIDENCE',synthetic=True)
        self.assertFalse(x['same_observable'])
    def test_itinerant_wandering_and_foreign_trade_different(self):
        x=compare_event_targets('ITINERANT_WANDERING','FOREIGN_TRADE_ACTIVITY',synthetic=True)
        self.assertFalse(x['same_observable'])
    def test_income_amount_not_income_means(self):
        x=compare_event_targets('INCOME_AMOUNT','INCOME_MEANS_MORAL_CLAIM',synthetic=True)
        self.assertFalse(x['same_observable'])
    def test_donation_not_deprivation(self):
        x=compare_event_targets('DISTRIBUTION_DONATION','DOCUMENTED_DEPRIVATION',synthetic=True)
        self.assertFalse(x['same_observable'])
    def test_all_targets_enumerated(self):
        self.assertEqual(len(target_types()),9)
        self.assertTrue(compare_event_targets('INCOME_AMOUNT','INCOME_AMOUNT',synthetic=True)['same_observable'])
    def test_locator_requires_edition_and_page(self):
        w=Witness('Sastri DLI 2015.312156','XV.72',928,'JYOT-JP')
        self.assertIn('XV.72|p928',verse_locator_binding(w,synthetic=True)['citation_key'])
        self.assertIsNone(verse_locator_binding(w,synthetic=True)['global_numbering_offset'])
    def test_locator_fails_without_provenance(self):
        with self.assertRaises(ValueError):
            verse_locator_binding(Witness('', 'XV.72', 928,'JYOT-JP'), synthetic=True)
        with self.assertRaises(ValueError):
            verse_locator_binding(Witness('Sastri','XV.72',0,'JYOT-JP'),synthetic=True)
    def test_no_real_person_model_admission(self):
        with self.assertRaises(ValueError):
            source_lord_vs_occupant(eleventh_lord='Sun',eleventh_occupants=())
        with self.assertRaises(ValueError):
            compare_event_targets('INCOME_AMOUNT','INCOME_AMOUNT')

if __name__=='__main__':
    unittest.main()
