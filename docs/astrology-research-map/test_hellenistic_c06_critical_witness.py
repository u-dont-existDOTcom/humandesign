import json
import unittest
from pathlib import Path

class TestGreekEditorialWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).resolve().parent/'HEPHAISTIO_C06_PINGREE_CRITICAL_WITNESS_V1.json'
        cls.w=json.loads(path.read_text(encoding='utf-8'))
    def test_source_identified_and_not_promoted(self):
        r=self.w
        self.assertEqual(r['pdf_pages'],496)
        self.assertEqual(r['human_prediction_runs'],0)
        self.assertFalse(r['model_promotion'])
        self.assertEqual(len(r['inspected']),4)
        self.assertEqual(r['ch29']['saturn_to_mercury_greek'],150)
        self.assertEqual(r['ch29']['later_valens_addition'],140)
    def test_critical_edition_preserves_conflicting_totals(self):
        r=self.w['ch36']
        sums=[sum(r[k].values()) for k in ('first','finer_header_greek','finer_header_schmidt_english','finer_items')]
        self.assertEqual(sums,[360,365,375,365])
        self.assertEqual(r['critical_app_p225_l27'],'νβ desid.')
        self.assertEqual(r['first']['Mercury'],52)
        self.assertEqual(r['finer_header_greek']['Mercury'],57)
        self.assertEqual(r['finer_header_greek']['Moon'],71)
        self.assertEqual(r['finer_header_schmidt_english']['Moon'],81)
