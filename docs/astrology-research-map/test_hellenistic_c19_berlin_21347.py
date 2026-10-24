"""C19: papyrus witness audit, not personal predictive validation."""
import json
import unittest
from pathlib import Path
from paulus_trigon_narrative_c05 import TRIGON_DAY_NIGHT

SOURCE=Path(__file__).with_name("BERLIN_C19_P_BEROL_21347_SOURCE_WITNESS_V1.json")

class BerlinPapyrusC19(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.claims={x["id"]:x for x in cls.s["transmitted_source_claims"]}

    def test_identity_and_distinct_ancient_document(self):
        r=self.s["object"]
        self.assertEqual((r["shelfmark"],r["record_id"]),("P. Berol. 21347","04530"))
        self.assertTrue(r["not_equivalent_to_P_Berol_9825"])
        self.assertIn("second century",r["catalogued_date"])

    def test_primary_recto_integrity(self):
        x=self.s["object"]["recto"]
        self.assertEqual(x["dimensions"],[2245,4827])
        self.assertEqual(x["bytes"],834379)
        self.assertEqual(x["sha256"],"4ae8bf6dcbf6f46fcb3f48cfd9b9a9d16711489abe3879c85b222872e888ad70")
        self.assertTrue(x["visually_inspected"])

    def test_verso_file_visually_checked(self):
        x=self.s["object"]["verso"]
        self.assertEqual(x["bytes"],821227)
        self.assertTrue(x["visually_inspected"])

    def test_metadata_xml_not_fake_greek_transcription(self):
        x=self.s["object"]["metadata"]
        self.assertEqual(x["bytes"],12394)
        self.assertFalse(x["greek_line_transcription_present"])

    def test_nocturnal_airy_trigon_inferred_from_editorial_reading(self):
        x=self.claims["C19-01"]
        self.assertEqual(x["reading"],"τριγώνω Ἑρμοῦ")
        self.assertEqual(TRIGON_DAY_NIGHT["air"],("Saturn","Mercury"))
        self.assertEqual(self.s["method_limits"]["night_trigon_lord"],"Mercury")
        self.assertTrue(self.s["method_limits"]["editor_inferrs_nocturnal_birth_from_Mercury"])

    def test_moon_monomoiria_restoration_is_not_source_certified(self):
        x=self.claims["C19-02"]
        self.assertEqual(x["reading"],"[μονομοι]ρία Σε[λ]ήνης")
        self.assertIn("RESTORATION",x["source_status"])
        self.assertEqual(self.s["method_limits"]["independent_monomoiria_calculations_new_this_batch"],0)
        self.assertFalse(self.s["method_limits"]["single_degree_natal_longitude_available_for_Moon_check"])

    def test_Libra_sign_not_exact_Ascendant_longitude(self):
        x=self.claims["C19-03"]
        self.assertIn("Libra",x["reading"])
        self.assertFalse(self.s["method_limits"]["single_degree_natal_longitude_available_for_Moon_check"])

    def test_scholarly_source_indexed_not_full_pdf_read(self):
        p=self.s["new_critical_publication"]
        self.assertEqual(p["doi"],"10.1515/apf-2024-0019")
        self.assertTrue(p["not_full_pdf_reviewed"])

    def test_prior_4277_negative_cases_not_pooled(self):
        x=self.s["method_limits"]
        self.assertEqual(x["P_Oxy_4277_three_preexisting_comparisons_unchanged"],
                         {"agree":1,"disagree":2})
        self.assertTrue(x["comparisons_should_not_pool_across_documents"])

    def test_no_new_model_or_human_validation(self):
        x=self.s["open"]
        self.assertEqual(x["human_predictive_validations"],0)
        self.assertFalse(x["production_scorer_changed"])
        self.assertFalse(x["two_glyphs_independently_palaeographically_certified"])
        self.assertFalse(x["gansten_purchased_ebook_extracted"])

if __name__=="__main__":
    unittest.main()
