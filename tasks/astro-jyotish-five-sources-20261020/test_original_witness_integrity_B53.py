import unittest
from original_witness_integrity_B53 import (
    PDF_SHA256, adverse_work_planets, source_witnesses, source_scope,
    sun_orders, eleventh_conflict, reputation_versions, VerseWitness,
)

class B53PrintedWitnessTests(unittest.TestCase):
    def test_sha_fingerprint_formed(self):
        self.assertEqual(len(PDF_SHA256),64)
        int(PDF_SHA256,16)
    def test_all_five_loci_mapped_and_visually_read(self):
        w=source_witnesses()
        self.assertEqual(len(w),5)
        self.assertTrue(all(v.visual_read for v in w))
    def test_same_print_family_not_independent_manuscripts(self):
        self.assertEqual(len({v.source_family for v in source_witnesses()}),1)
        self.assertTrue(all(not v.independent_manuscript for v in source_witnesses()))
    def test_page_number_mapping(self):
        self.assertEqual(source_witnesses()[2].printed_pages,(151,))
        self.assertEqual(source_witnesses()[-1].physical_pdf_pages,(172,))
    def test_invalid_page_map_rejected(self):
        with self.assertRaises(ValueError):
            VerseWitness('X',(10,11),(3,),"SANSKRIT","A",True)
        with self.assertRaises(ValueError):
            VerseWitness('X',(10,),(3,),"OCR_ONLY","A",False)
    def test_v3_source_planet_discrepancy(self):
        a=adverse_work_planets('Saturn')
        self.assertNotEqual(a['bhasin_english_v3'],a['printed_sanskrit_v3'])
        self.assertEqual(a['printed_sanskrit_v3'],['Jupiter','Mercury','Venus'])
    def test_v3_conditional_coincidence(self):
        self.assertEqual(adverse_work_planets('Venus')['bhasin_english_v3'],adverse_work_planets('Venus')['printed_sanskrit_v3'])
    def test_v3_invalid_lord(self):
        with self.assertRaises(ValueError): adverse_work_planets('Rahu')
    def test_v16_sun_only_candidate(self):
        r=sun_orders(True,False,True)
        self.assertFalse(r['bhasin_english_and'])
        self.assertTrue(r['sanskrit_va_candidate'])
        self.assertFalse(r['sanskrit_grammar_arbitrated'])
    def test_v16_mars_only_candidate(self):
        r=sun_orders(False,True,True)
        self.assertFalse(r['bhasin_english_and'])
        self.assertTrue(r['sanskrit_va_candidate'])
    def test_v16_both_conditions(self):
        r=sun_orders(True,True,True)
        self.assertTrue(r['bhasin_english_and'] and r['sanskrit_va_candidate'])
    def test_v16_angular_required_in_both_diagnostic_versions(self):
        r=sun_orders(True,True,False)
        self.assertFalse(r['bhasin_english_and'] or r['sanskrit_va_candidate'])
    def test_v16_requires_boolean_inputs(self):
        with self.assertRaises(TypeError):sun_orders(1,True,True)
    def test_eleventh_positive_negative_same_antecedent(self):
        r=eleventh_conflict(True,False)
        self.assertTrue(r['v2_gain'] and r['v10_loss'] and r['overlap'])
        self.assertFalse(r['precedence_known'] or r['score_allowed'])
    def test_eleventh_without_malefic_not_collision(self):
        self.assertFalse(eleventh_conflict(False,True)['overlap'])
    def test_eleventh_requires_boolean_inputs(self):
        with self.assertRaises(TypeError):eleventh_conflict('true',False)
    def test_reputation_polarity_opposed_without_emendation(self):
        r=reputation_versions(True)
        self.assertEqual(r['printed_1929'],'FAVORABLE')
        self.assertEqual(r['bhasin_english'],'UNFAVORABLE')
        self.assertIsNone(r['canonical_conjectural_emendation'])
    def test_reputation_no_false_trigger(self):
        self.assertEqual(reputation_versions(False)['printed_1929'],'NOT_TRIGGERED')
    def test_no_production_or_human_validation(self):
        s=source_scope()
        self.assertEqual(s['human_predictions_tested'],0)
        self.assertEqual(s['production_rules_promoted'],0)
        self.assertFalse(s['model_scoring_allowed'])

if __name__ == '__main__':unittest.main()
