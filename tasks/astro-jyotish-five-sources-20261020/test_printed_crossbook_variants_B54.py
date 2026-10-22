import unittest
from printed_crossbook_variants_B54 import (Wording, nonidentical_predicate_witnesses,
    edition_verse_alignment, occupational_disjunction, income_source_vs_occupation,
    textual_dependency)

class TestSourceScopeB54(unittest.TestCase):
    def test_conjunction_only(self):
        r=nonidentical_predicate_witnesses(synthetic=True,with_saturn=True,
             eighth_lord_conjoined=True,eighth_lord_aspects=False,cruel_varga_or_angle=True)
        self.assertTrue(r['sarvartha_1929_conjunction_version'])
        self.assertFalse(r['jataka_1922_aspect_version'])
    def test_aspect_only(self):
        r=nonidentical_predicate_witnesses(synthetic=True,with_saturn=True,
             eighth_lord_conjoined=False,eighth_lord_aspects=True,cruel_varga_or_angle=True)
        self.assertFalse(r['sarvartha_1929_conjunction_version'])
        self.assertTrue(r['jataka_1922_aspect_version'])
        self.assertFalse(r['score_allowed'])
    def test_both_and_neither(self):
        for conjunction,aspect in [(True,True),(False,False)]:
            r=nonidentical_predicate_witnesses(synthetic=True,with_saturn=True,
                eighth_lord_conjoined=conjunction,eighth_lord_aspects=aspect,
                cruel_varga_or_angle=True)
            self.assertEqual((r['sarvartha_1929_conjunction_version'],
                              r['jataka_1922_aspect_version']), (conjunction,aspect))
    def test_common_preconditions_gate(self):
        for saturn,qual in [(False,True),(True,False)]:
            r=nonidentical_predicate_witnesses(synthetic=True,with_saturn=saturn,
                eighth_lord_conjoined=True,eighth_lord_aspects=True,cruel_varga_or_angle=qual)
            self.assertFalse(r['sarvartha_1929_conjunction_version'] or r['jataka_1922_aspect_version'])
    def test_no_personal_chart_admission(self):
        with self.assertRaises(ValueError):
            nonidentical_predicate_witnesses(synthetic=False,with_saturn=True,
                eighth_lord_conjoined=True,eighth_lord_aspects=False,cruel_varga_or_angle=True)
    def test_reject_bool_coercion(self):
        with self.assertRaises(TypeError):
            nonidentical_predicate_witnesses(synthetic=True,with_saturn=1,
                eighth_lord_conjoined=True,eighth_lord_aspects=False,cruel_varga_or_angle=True)
    def test_1922_vs_2026_verse_numbers(self):
        d=edition_verse_alignment('JP-XV-61-1922','JP-XV-60-ELECTRONIC',same_sanskrit_lemma_verified=True)
        self.assertTrue(d['same_clause_recognized'])
        self.assertFalse(d['global_offset_assumed'] or d['score_allowed'])
    def test_no_global_offset_inference(self):
        d=edition_verse_alignment('JP-XV-43-1922','JP-XV-43-ELECTRONIC',same_sanskrit_lemma_verified=False)
        self.assertFalse(d['global_offset_assumed'])
    def test_empty_verse_block(self):
        with self.assertRaises(ValueError):
            edition_verse_alignment('', '60', same_sanskrit_lemma_verified=True)
    def test_disjunction_width(self):
        r=occupational_disjunction(('cosmetics','painting','commerce'),synthetic=True)
        self.assertEqual(r['distinct_possible_categories'],3)
        self.assertFalse(r['unique_occupation_prediction'] or r['probabilities_estimated'])
    def test_duplicate_categories_not_independent(self):
        r=occupational_disjunction(('trading','trading'),synthetic=True)
        self.assertEqual(r['distinct_possible_categories'],1)
        self.assertFalse(r['prediction_allowed'])
    def test_disjunction_gate(self):
        with self.assertRaises(ValueError):
            occupational_disjunction(('medicine',),synthetic=False)
        with self.assertRaises(ValueError):
            occupational_disjunction((),synthetic=True)
    def test_foreign_trade_not_residence(self):
        x=income_source_vs_occupation(wealth_provider='foreign customers',job_sector='overseas commerce')
        self.assertFalse(x['same_observable'])
        self.assertEqual(x['independent_prediction_confirmations'],0)
    def test_source_witnesses_not_independent_prediction(self):
        a=Wording('SC_JP_AUTHORITY', 'SC1929','8.1.17',None,'8th-lord conjunction','OFFICIAL_ORDERS')
        b=Wording('SC_JP_AUTHORITY', 'JP1922','15.61','15.60','8th-lord aspect','OFFICIAL_ORDERS')
        d=textual_dependency(a,b,shared_substantial_wording=True)
        self.assertTrue(d['shared_transmitted_pattern'])
        self.assertFalse(d['wording_identical'] or d['copying_direction_proven'] or d['score_allowed'])
    def test_families_not_forcibly_grouped(self):
        a=Wording('A','SC1929','8.1.17',None,'conjunction','OFFICIAL_ORDERS')
        b=Wording('B','JP1922','15.61',None,'aspect','OFFICIAL_ORDERS')
        with self.assertRaises(ValueError):
            textual_dependency(a,b,shared_substantial_wording=True)
    def test_no_promotion(self):
        with self.assertRaises(ValueError):
            Wording('A','SC1929','v17',None,'a','b','ALLOW_SCORE')

if __name__=='__main__':unittest.main()
