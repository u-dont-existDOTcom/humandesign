"""Source-to-human bridge C29: calculation does not make prediction."""
import json
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
SRC=HERE/"HELLENISTIC_C29_SOURCE_TO_HUMAN_TEST_DISPOSITION_V1.json"

class TestC29HumanOutcomeBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SRC.read_text(encoding="utf-8"))

    def test_checked_greek_passage_is_sect_light_and_ascendant_math(self):
        s=self.d["source_read"]
        self.assertIn("αἱρετικοῦ φωτὸς",s["exact_ch32_excerpt"])
        self.assertIn("ὡροσκόπου",s["exact_ch33_excerpt"])
        self.assertTrue(s["modern_digitization_not_boer_critical_apparatus"])
        self.assertTrue(s["critical_editorial_variants_unresolved"])

    def test_all_feature_rows_retain_unmapped_person_outcome(self):
        v=self.d["features"]
        self.assertEqual(len(v),4)
        self.assertTrue(all(x["human_behavioral_outcome_attested_in_checked_passage"] is False for x in v))
        self.assertTrue(all(x["status"] in ("SOURCE_CALCULATION_ONLY",
                                          "NO_PERSON_OUTCOME_MAPPING_FROZEN",
                                          "SOURCE_COMPARISON_ONLY") for x in v))

    def test_ascendant_reconstruction_is_not_behavior_validation(self):
        q=self.d["distinct_possible_technical_question"]
        self.assertEqual(q["type"],"CHART_RECTIFICATION_OR_ASTRONOMICAL_PARITY")
        self.assertTrue(q["not_a_personality_or_life_event_prediction"])
        self.assertFalse(q["actual_birth_data_checked"])
        self.assertFalse(q["blinded_verification_protocol_frozen"])
        self.assertFalse(q["method_fully_source_disambiguated"])

    def test_source_photography_never_upgrades_human_outcomes(self):
        x=self.d["nonpromotion"]
        self.assertFalse(x["behavioral_questionnaire_predictions_frozen"])
        self.assertFalse(x["consenting_untouched_human_tested"])
        self.assertEqual(x["human_predictive_validations"],0)
        self.assertFalse(x["production_model_promoted"])
        self.assertTrue(x["calculation_parity_does_not_prove_astrology"])
        self.assertEqual(self.d["root_objective_status"],"OPEN")

if __name__=="__main__":
    unittest.main()
