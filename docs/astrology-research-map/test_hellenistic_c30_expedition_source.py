"""C30 first Hellenistic falsifiable life-outcome claim: source fidelity only."""
import inspect
import json
from decimal import Decimal
from pathlib import Path
import unittest

from hellenistic_c30_dorotheus_expedition_lot import (
    CAMPAIGN_INDICATOR_SIGNS, ZODIAC, documentary_claim,
    lot_of_expedition, lot_sign, sampled_birth_uncertainty,
)

DIR=Path(__file__).resolve().parent
SRC=DIR/"HELLENISTIC_C30_DOROTHEUS_EXPEDITION_SOURCE_V1.json"
DESIGN=DIR/"HELLENISTIC_C30_EXPEDITION_BLIND_TEST_DESIGN_DRAFT_V1.json"


class TestC30DorotheusExpeditionLot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(SRC.read_text(encoding="utf-8"))
        cls.design=json.loads(DESIGN.read_text(encoding="utf-8"))

    def test_source_locus_and_english_rendered_page(self):
        w=self.src["witness"]
        self.assertIn("chapter 19",w["locus"])
        self.assertEqual((w["english_pdf_page_one_based"],
                          w["english_printed_page"]),(40,68))
        self.assertEqual(len(w["local_owner_pdf_sha256"]),64)
        self.assertEqual(len(w["greek_source_sha256"]),64)
        self.assertTrue(w["source_scan_rendered_and_visually_read"])
        self.assertFalse(w["original_pingree_Greek_critical_apparatus_inspected"])

    def test_literal_planet_from_and_to_labels(self):
        x=self.src["greek_source_anchors"]
        self.assertIn("Φαίνοντος",x["arithmetic_phrase"])
        self.assertIn("Σελήνης",x["arithmetic_phrase"])
        self.assertIn("ὥρης",x["ascendant_phrase"])
        self.assertIn("στρατίῃσιν",x["purported_outcome"])
        self.assertTrue(x["no_night_reversal_written_in_this_fragment"])

    def test_no_fabricated_biconditional(self):
        self.assertIn("ONE_WAY",self.src["greek_source_anchors"]["direct_source_characterization"])
        x=documentary_claim(ascendant=30,saturn=0,moon=0)
        self.assertFalse(x["source_positive_condition"])
        self.assertEqual(x["source_claim_status"],
                         "NO_POSITIVE_CLAIM_FROM_THIS_CONDITION")
        self.assertTrue(x["not_source_claiming_no_campaign_when_false"])
        self.assertTrue(self.src["separate_following_greek_passage"]
                        ["does_not_change_four_sign_positive_conditional"])

    def test_exact_four_sign_indicator_with_12_sign_coverage(self):
        self.assertEqual(CAMPAIGN_INDICATOR_SIGNS,
                         {"Aries","Scorpio","Capricorn","Aquarius"})
        self.assertEqual(len(ZODIAC),12)
        self.assertEqual(sum(documentary_claim(ascendant=i*30,saturn=0,moon=0)
                             ["source_positive_condition"] for i in range(12)),4)
        self.assertEqual(self.src["mathematical_interpretation"]
                         ["exposed_fraction_under_uniform_lot_null"],"1/3")

    def test_full_circle_boundary_conditions(self):
        cases=[
            ("0","Aries",True),("29.999999","Aries",True),
            ("30","Taurus",False),("209.999999","Libra",False),
            ("210","Scorpio",True),("239.999","Scorpio",True),
            ("240","Sagittarius",False),("270","Capricorn",True),
            ("299.999","Capricorn",True),("300","Aquarius",True),
            ("329.9999","Aquarius",True),("330","Pisces",False),
            ("359.9999","Pisces",False),
        ]
        for asc,sign,indicated in cases:
            with self.subTest(asc=asc):
                x=documentary_claim(ascendant=asc,saturn=0,moon=0)
                self.assertEqual((x["lot_sign"],x["source_positive_condition"]),
                                 (sign,indicated))

    def test_synthetic_wraparound_when_moon_precedes_saturn(self):
        self.assertEqual(lot_of_expedition(ascendant=345,saturn=350,moon=10),
                         Decimal("5"))
        self.assertEqual(lot_sign(lot_of_expedition(ascendant=35,saturn=10,moon=350)),
                         "Aries")
        self.assertEqual(lot_of_expedition(ascendant="359.9",
                                            saturn="359.8",moon="0.2"),
                         Decimal("0.3"))

    def test_invalid_or_nan_rejected_without_implicit_wrap(self):
        invalids=[-1,360,True,None,"", " ", "nan","Infinity",object()]
        for v in invalids:
            with self.subTest(value=repr(v)):
                with self.assertRaises(ValueError):
                    lot_of_expedition(ascendant=v,saturn=0,moon=0)
        with self.assertRaises(ValueError):
            lot_sign("360")
        with self.assertRaises(ValueError):
            lot_of_expedition(ascendant=0,saturn=1,moon=float("nan"))

    def test_no_sect_argument_to_hallucinate_reversal(self):
        self.assertNotIn("sect",inspect.signature(lot_of_expedition).parameters)
        self.assertFalse(self.src["mathematical_interpretation"]
                         ["sect_reversal_applied"])

    def test_sampling_birth_uncertainty_is_never_certification(self):
        x=sampled_birth_uncertainty([(0,0,0),(0.1,0,0),(0.2,0,0)])
        self.assertTrue(x["sampled_condition_consistent"])
        self.assertFalse(x["certified_full_birth_interval_stability"])
        self.assertFalse(x["unobserved_intermediate_crossings_excluded"])
        self.assertFalse(x["eligible_for_prospective_claim_freeze"])
        y=sampled_birth_uncertainty([(29.8,0,0),(30.1,0,0)])
        self.assertFalse(y["sampled_condition_consistent"])
        self.assertEqual(y["sampled_condition_values"],[False,True])
        with self.assertRaises(ValueError):
            sampled_birth_uncertainty([])

    def test_translated_modern_war_proxy_not_source(self):
        o=self.design["human_outcome_variable"]
        self.assertIn("military",o["potential_measure"].lower())
        self.assertIn("PARTIAL_MODERN_PROXY",o["equivalence_to_ancient_term"])
        self.assertTrue(self.design["outcome_measurement"]["unscored_unknown"])
        self.assertTrue(self.design["primary_test_proposed"]["no_claim_if_events_missing"])

    def test_no_recruitment_outcomes_or_person_fit(self):
        x=self.design["status_checks"]
        self.assertFalse(x["applicant_enrollment_started"])
        self.assertFalse(x["outcome_records_loaded"])
        self.assertFalse(x["predictions_precommitted_for_actual_people"])
        self.assertEqual(x["blinded_human_validations"],0)
        self.assertFalse(x["production_rules_changed"])
        self.assertFalse(self.src["mathematical_interpretation"]
                         ["own_birth_or_known_life_data_used"])

    def test_parent_open_with_strong_nonastrology_control(self):
        self.assertEqual(self.src["main_owner_outcome"]["status"],"OPEN")
        self.assertEqual(self.design["status"],
                         "UNREGISTERED_STUDY_DESIGN_DRAFT_NOT_A_HUMAN_PREDICTION_FREEZE")
        self.assertIn("cohort",self.design["primary_test_proposed"]["baseline"])
        self.assertIn("conditional",self.design["primary_test_proposed"]["method"])
        self.assertTrue(self.design["other_models"]["no_tuning_on_owner_history"])

    def test_secondary_Taurus_example_not_exact_word_of_verse(self):
        q=self.src["separate_following_greek_passage"]
        self.assertEqual(q["references_lot_in"],"Taurus")
        self.assertTrue(q["not_in_checked_Schmidt_excerpt"])
        self.assertFalse(q["independent_manuscript_glyph_authentication"])
        self.assertIn("NOT_A_BINARY_CONVERSE",q["status"])


if __name__=="__main__":
    unittest.main()
