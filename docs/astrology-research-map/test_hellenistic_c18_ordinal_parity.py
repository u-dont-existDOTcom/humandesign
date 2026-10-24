"""C18 regression: historical papyrus source comparisons only."""
import unittest
from poxy4277_ordinal_method_matrix_c18 import audit_ordinal_and_source_methods, load_witness

class C18OrdinalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=load_witness()
        cls.s=audit_ordinal_and_source_methods()

    def test_source_row_names(self):
        self.assertEqual([r['object'] for r in self.s['records']],
                         ['Mercury','Midheaven','Lower Midheaven'])

    def test_source_labeled_longitudes(self):
        self.assertEqual([(x['sign'],x['degree'],x['minutes']) for x in self.w['labels']],
                         [('Capricorn',6,22),('Taurus',27,8),('Scorpio',27,8)])

    def test_c05_ordinal_baseline_still_one_of_three(self):
        self.assertEqual(self.s['agreements']['C05_correct_ordinal'],1)
        self.assertEqual(self.s['agreements']['C05_completed_degree_ordinal'],0)
    def test_tolsa_valens_table_equals_truncated_indexing(self):
        self.assertEqual(self.s['Valens_truncated_equivalences'],3)
        self.assertEqual([r['variants']['Tolsa_ValensIV26'] for r in self.s['records']],
                         ['Mercury','Mars','Saturn'])

    def test_tolsa_trigonal_and_olympiodorus_none_match(self):
        counts=self.s['agreements']
        self.assertEqual(counts['Tolsa_Paulus32'],0)
        self.assertEqual(counts['Tolsa_Olymp34'],0)
        self.assertEqual(counts['Tolsa_ValensIV26'],0)
        self.assertEqual(counts['Tolsa_mixed'],1)
