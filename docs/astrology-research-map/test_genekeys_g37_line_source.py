"""G37 official six-Line communication-response source and ethical test scope."""
import hashlib,json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
F=HERE/"GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json"
TEMP=Path("/tmp/g37-gene-keys-official-profile-guidance.html")


class TestG37SixLineSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(F.read_text(encoding="utf8"))

    def test_six_lines_all_present_and_single_source(self):
        x=self.data
        self.assertEqual(x["direct_publisher_source"],
                         "https://genekeys.com/how-to-read-your-profile/")
        self.assertEqual(len(x["verified_six_line_interpersonal_styles"]),6)
        self.assertEqual([v["line"] for v in x["verified_six_line_interpersonal_styles"]],
                         [1,2,3,4,5,6])
        self.assertEqual(len({v["experimental_style_category"]
                              for v in x["verified_six_line_interpersonal_styles"]}),6)

    def test_correct_short_publisher_response_descriptors(self):
        exact=[
          "Full Information and Heartfelt Directness",
          "High Frequency with No Agenda",
          "Absolutely no pressure",
          "Integrity, Honesty, Softness & Romance",
          "Simple & Practical Solutions",
          "Patience"
        ]
        self.assertEqual([x["brief_official_responds_best_to"] for x
                          in self.data["verified_six_line_interpersonal_styles"]],
                         exact)

    def test_line_interpretation_is_not_a_source_frozen_predictive_model(self):
        s=self.data["source_to_behavior_status"]
        self.assertTrue(s["six_line_styles_are_original_publishers_source"])
        self.assertTrue(s["scientific_behavioral_questionnaire_not_supplied_by_Rudd"])
        self.assertFalse(s["prospective_line_classification_mapping_frozen"])
        self.assertFalse(s["experimental_stimuli_permutations_published"])
        self.assertEqual(s["actual_volunteers_or_blind_results"],0)
        self.assertFalse(s["source_6_lines_do_not_prove_behavioural_validity"] is False)

    def test_no_predetermined_biological_frequency_or_clinical_interpretation(self):
        s=self.data["source_to_behavior_status"]
        self.assertFalse(s["biologically_measured_emotional_frequency_claim"])
        self.assertTrue(s["human_design_line_baseline_required_if_claiming_incremental_inference"])
        self.assertFalse(self.data["current_parent_status"]
                         ["production_behavioral_scorer_changed"])
        self.assertEqual(self.data["current_parent_status"]
                         ["real_people_and_human_outcomes_tested"],0)

    def test_childhood_relationship_spheres_cannot_be_diagnosed(self):
        obs=self.data["other_strong_source_scope"]
        self.assertEqual([v["sphere"] for v in obs],
                         ["EQ","IQ","Attraction","Life's Work","repeated_same_key"])
        self.assertTrue(obs[0]["no_emotional_defence_diagnoses_generated"])
        self.assertTrue(obs[2]["no_unconsenting_partner_or_owner_relationships_examined"])
        self.assertTrue(obs[3]["no_income_or_career_prediction_generated"])
        self.assertTrue(obs[4]["no_personal_ideas_fitted"])

    def test_choose_specific_chart_sphere_is_analyst_not_original(self):
        s=self.data["source_to_behavior_status"]
        self.assertTrue(s["author_did_not_specify_primary_sphere_for_behavior_test"])
        self.assertTrue(s["choose_Lifes_Work_line_as_primary_would_be_analyst_added_not_source_rule"])
        self.assertFalse(s["full_64_line_by_gene_key_interpretive_corpus_not_read"] is False)
        self.assertFalse(s["prospective_line_classification_mapping_frozen"])

    def test_prereg_design_marked_future_and_HD_not_independent(self):
        p=self.data["proposed_bounded_question_if_later_authorized"]
        self.assertIn("ANALYST_DERIVED",p["model_type"])
        self.assertEqual(p["source_style_count"],6)
        self.assertTrue(p["validity_warning"].startswith("Cannot claim independent"))
        self.assertFalse(p["current_source_claim_to_research_outcome_frozen"])
        self.assertTrue(p["children_and_relationship_diagnostics_out_of_scope"])

    @unittest.skipUnless(TEMP.is_file(),
                         "original publicly fetched official HTML not mounted on this host")
    def test_original_public_page_byte_identity_if_present(self):
        self.assertEqual(hashlib.sha256(TEMP.read_bytes()).hexdigest(),
                         self.data["directly_fetched_public_page_sha256"])
        # HTML mixes adjacent tags; rendered text still has all short descriptors.
        from html import unescape
        import re
        raw=unescape(TEMP.read_text(encoding="utf8"))
        flattened=re.sub(r"<[^>]+>"," ",raw)
        flattened=" ".join(flattened.split())
        for line in self.data["verified_six_line_interpersonal_styles"]:
            self.assertIn(line["brief_official_responds_best_to"],flattened)

if __name__=="__main__":
    unittest.main()
