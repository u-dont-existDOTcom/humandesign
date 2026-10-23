import unittest
from valens_zodiacal_place_c06 import WITNESSES, witnessed_assignment, cross_document_concordance

class TestHistoricalPlaces(unittest.TestCase):
    def test_attestations(self):
        self.assertEqual(len(WITNESSES), 3)
        self.assertEqual(witnessed_assignment('VALENS_VIII_7_LEO22'), 'Virgo')
        self.assertEqual(witnessed_assignment('POXY_4277_ASC_LEO22_11'), 'Virgo')
        self.assertEqual(witnessed_assignment('POXY_4277_MERC_CAP6_22'), 'Sagittarius')

    def test_no_inferred_values(self):
        with self.assertRaises(ValueError):
            witnessed_assignment('VALENS_CAPRICORN_6')
        stats=cross_document_concordance()
        self.assertTrue(stats['leo_place_overlap'])
        self.assertFalse(stats['papyrus_capricorn_entry_independently_reconstructed'])
        self.assertFalse(stats['same_degree_notation_proven'])
        self.assertFalse(stats['prediction_or_human_success'])
