"""G36 external publisher seven-key language and prenatal method uncertainty.

Source-only logic, six SYNTHETIC comparisons. No gene frequency measurements,
publisher calculator result, confidential people or human outcome scores.
"""
from __future__ import annotations

import copy
from pathlib import Path
import json
import unittest

from genekeys_g35_source_crosswalk import (
    CORE_11,SUPPLEMENTARY_3, wheel_programming_partner, digest
)
from genekeys_g36_source_difference_matrix import (
    ROOT, PARENT, REGISTRY, OUT, build
)


class TestG36OfficialSourceScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=json.loads(REGISTRY.read_text(encoding="utf8"))
        cls.dataset=json.loads(OUT.read_text(encoding="utf8"))

    def test_computational_dataset_reproducible_from_frozen_G35(self):
        self.assertEqual(build(),self.dataset)
        body={k:v for k,v in self.dataset.items()
              if k!="replay_source_digest_sha256"}
        self.assertEqual(self.dataset["replay_source_digest_sha256"],digest(body))
        self.assertEqual(len(self.dataset["replay_source_digest_sha256"]),64)

    def test_source_seven_keys_selected_without_known_life_events(self):
        keys=self.registry["source_sampled_7_keys"]
        self.assertEqual([x["number"] for x in keys],[5,28,32,50,54,55,64])
        self.assertTrue(self.dataset["six_source_times_are_synthetic_not_personal_births"])
        self.assertTrue(self.dataset["no_owner_chart_or_participant_responses_used"])
        self.assertEqual(self.dataset["actual_real_human_behavioral_predictions_or_outcomes"],0)

    def test_official_public_seven_programming_partners_independently_parity(self):
        partners={x["number"]:x["official_programming_partner"]
                  for x in self.registry["source_sampled_7_keys"]}
        self.assertEqual(partners,
                         {5:35,28:27,32:42,50:3,54:53,55:59,64:63})
        for key,partner in partners.items():
            self.assertEqual(wheel_programming_partner(key),partner)
            self.assertEqual(wheel_programming_partner(partner),key)

    def test_all_seven_source_headings_exact_public_short_titles(self):
        expect={
          5:("Impatience","Patience","Timelessness"),
          28:("Purposelessness","Totality","Immortality"),
          32:("Failure","Preservation","Veneration"),
          50:("Corruption","Equilibrium","Harmony"),
          54:("Greed","Aspiration","Ascension"),
          55:("Victimisation","Freedom","Freedom"),
          64:("Confusion","Imagination","Illumination")
        }
        for x in self.registry["source_sampled_7_keys"]:
            self.assertEqual((x["shadow"],x["gift"],x["siddhi"]),
                             expect[x["number"]])
            self.assertEqual(x["official_url"],
                             f"https://genekeys.com/gene-key-{x['number']}/")
            self.assertTrue(x["primary_page_concept_summary"])
            self.assertFalse(x["natal_person_trait_proportional_claim"])
            self.assertFalse(x["behavioral_threshold_or_outcome_frequency_stated"])

    def test_not_a_fixed_personality_diagnosis_or_measured_DNA_frequency(self):
        x=self.registry
        self.assertIn("not a fixed",x["official_public_cited_works"]
                      ["not_fixed_personality_profile"]["claimed_scope"])
        self.assertTrue(x["source_ethics"]["never_impute_defect_or_diagnosis_from_shadow"])
        self.assertTrue(x["source_ethics"]["never_assign_spiritual_rank_from_siddhi"])
        self.assertTrue(x["source_ethics"]["never_claim_measured_DNA_frequency"])
        self.assertFalse(x["interpretative_authority"]
                         ["source_conditional_predictions_formally_frozen"])

    def test_speculative_gene55_mutation_not_supposed_as_current_science(self):
        key=next(x for x in self.registry["source_sampled_7_keys"] if x["number"]==55)
        self.assertIn("LACKS_PREDEFINED",key["collective_genetic_change_claim_status"])
        self.assertIn("genekeys.com/resource/the-55/",key["speculative_distinct_source_url"])
        self.assertFalse(key["natal_person_trait_proportional_claim"])

    def test_source_not_accessible_completed_publisher_profile(self):
        a=self.registry["official_public_cited_works"]
        self.assertIn("under construction",a["free_profile_url"]["literal_current_notice"])
        self.assertEqual(a["free_profile_url"]["actual_completed_synthetic_profile_result"],"NONE")
        self.assertFalse(a["alternate_profiler_url"]["verified_interactive_birth_calculation_completed"])
        self.assertFalse(a["free_profile_url"]["private_api_access_attempted"])
        self.assertFalse(a["free_profile_url"]["registered_account_created"])

    def test_full_88degree_versus_day_method_still_unknown(self):
        self.assertFalse(self.dataset
                         ["official_real_profile_88_day_vs_88_degree_method_certified"])
        self.assertTrue(self.dataset
                        ["this_is_two_candidate_methods_not_two_real_GeneKeys_profiles"])
        self.assertEqual(self.dataset["synthetic_chart_count"],6)
        self.assertEqual(self.dataset["pre_natal_core_sphere_count"],6)
        self.assertEqual(self.dataset["prenatal_supplementary_spheres"],2)

    def test_exact_six_synthetic_prenatal_sphere_sensitivity_counts(self):
        self.assertEqual(self.dataset["core_prenatal_sphere_total_gate_changes"],12)
        self.assertEqual(self.dataset["core_prenatal_sphere_total_line_changes"],26)
        self.assertEqual(self.dataset["all_prenatal_sphere_total_gate_changes"],12)
        self.assertEqual(self.dataset["all_prenatal_sphere_total_line_changes"],28)
        self.assertEqual(len(self.dataset["synthetic_sphere_comparisons"]),6)
        self.assertTrue(all(len(c["reconstructed_spheres"])==8
                            for c in self.dataset["synthetic_sphere_comparisons"]))

    def test_prenatal_attraction_design_moon_changes_gene_key_all_six(self):
        by={x["sphere"]:x for x in self.dataset["by_prenatal_sphere"]}
        self.assertEqual(by["attraction"]["body"],"moon")
        self.assertTrue(by["attraction"]["core"])
        self.assertEqual(by["attraction"]["changed_key_cases"],6)
        self.assertEqual(by["attraction"]["changed_line_cases"],6)

    def test_sun_and_earth_geometric_coupling_not_independent_evidence(self):
        rows=self.dataset["synthetic_sphere_comparisons"]
        for row in rows:
            s={x["sphere"]:x for x in row["reconstructed_spheres"]}
            self.assertEqual(s["radiance"]["change_key"],s["purpose"]["change_key"])
            self.assertEqual(s["radiance"]["change_line"],s["purpose"]["change_line"])
        self.assertTrue(self.dataset["cannot_count_Human_Design_as_independent_confirmation"])

    def test_sources_do_not_suddenly_claim_probabilistic_behavior(self):
        sample=self.dataset["official_7_public_partner_and_triads"]
        self.assertEqual(len(sample),7)
        self.assertTrue(all(s["not_source_specified_natal_behavioral_probability"]
                            for s in sample))
        self.assertTrue(self.dataset
                        ["source_pages_do_not_state_natal_specific_numeric_trait_predictions"])
        self.assertEqual(self.registry["administrative_boundary"]
                         if "administrative_boundary" in self.registry else
                         self.registry["source_ethics"]["real_people_processed"],0)

    def test_two_different_research_questions_remain_distinct(self):
        q=self.registry["research_compatible_but_separate_hypotheses"]
        self.assertEqual([v["id"] for v in q],
                         ["G36_PERSON_PROFILE_IMPRESSIONS","G36_CONTEMPLATIVE_PROGRAM_EFFECT"])
        self.assertEqual(q[0]["type"],
                         "EXPLORATORY_ANALYST_DERIVED_NOT_ORIGINAL_SOURCE_PREDICTION")
        self.assertEqual(q[1]["type"],
                         "INTERVENTION_NOT_NATAL_PREDICTIVITY")
        self.assertTrue(q[1]["no_actual_randomization_or_outcomes"])
        self.assertFalse(self.registry["source_ethics"]
                         ["official_Profile_calculation_still_UNVERIFIED"] is False)

    def test_research_input_hashes_source_artifact_bytes(self):
        import hashlib
        self.assertEqual(hashlib.sha256(PARENT.read_bytes()).hexdigest(),
                         self.dataset["source_parent_G35_file_sha256"])
        self.assertEqual(hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
                         self.dataset["source_G36_interpretive_register_sha256"])


if __name__=="__main__":
    unittest.main()
