#!/usr/bin/env python3
"""Independent literature scope controls and unlaunched historical natal pilot."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).parent
S=json.loads((ROOT/"MAYA_B08_CONTEMPORARY_COUNT_SOURCE_AND_HYPOTHESIS_LEDGER.json").read_text(encoding="utf-8"))
P=json.loads((ROOT/"MAYA_B08_CHUWEN_HISTORIC_RECONSTRUCTION_PILOT_V1.json").read_text(encoding="utf-8"))
B07=json.loads((ROOT/"MAYA_B07_ARTISAN_BLIND_STUDY_DRAFT_V1.json").read_text(encoding="utf-8"))

class LivingVsHistoricMayaScope(unittest.TestCase):
    def test_modern_yucatec_source_is_limited_to_actual_field_sites(self):
        s=S["sources"][0]
        self.assertEqual(set(s["field_communities"]),{"Kopchen","Chemax"})
        self.assertEqual(s["doi"],"10.3389/fpsyg.2012.00271")
        self.assertIn("Villa Rojas (1945)",s["source_restriction"])
        self.assertIn("not",s["exact_short_claim"])
        self.assertTrue(any("Do not make a negative statement about all living" in i for i in S["outside_scope"]))

    def test_ancient_inscription_clock_hypothesis_not_modern_policy(self):
        v=S["sources"][1]
        self.assertTrue(v["consensus_not_asserted"])
        self.assertTrue(v["commenter_2026_noon_to_noon_claim_rejected_as_unverified"])
        self.assertIn("not a current local Yucatec natal date policy",v["provenance"])

    def test_living_and_historical_reconstruction_are_distinct_claims(self):
        live,historical,other=S["separate_testable_claims"]
        self.assertEqual(live["status"],"NOT_ESTABLISHED")
        self.assertTrue(live["id"].endswith("UNBROKEN"))
        self.assertTrue(historical["can_test_if_declared_before_answers"])
        self.assertIn("UNFROZEN",historical["status"])
        self.assertFalse(live["natal_engine_eligible"])
        self.assertFalse(historical["natal_engine_eligible"])
        self.assertEqual(other["status"],"MUST_REPORT_NOT_POSTHOC_PRIMARY")

    def test_timebound_and_reconstruction_not_automatic_birth_scoring(self):
        self.assertFalse(S["method_protocol_status"]["live_yucatec_calendar_clock_still_unverified"] is False)
        self.assertFalse(S["method_protocol_status"]["exact_birth_date_policy_not_frozen"] is False)
        self.assertEqual(S["method_protocol_status"]["actual_human_predictions"],0)
        self.assertEqual(S["method_protocol_status"]["empirical_validated_effects"],0)

    def test_manuscript_claim_and_three_sign_composite_prohibited_as_one(self):
        self.assertEqual(P["prediction"]["target_canonical_yucatec_day"],"CHUWEN")
        self.assertTrue(P["prediction"]["one_primary_contrast"])
        self.assertTrue(B07["exploratory_not_primary"]["is_investigator_generated_group_not_in_original_source"])
        self.assertFalse(P["distinction"]["test_type"].startswith("live"))

    def test_craft_outcome_includes_paid_without_double_score(self):
        q=P["questionnaire_candidate"]
        self.assertIn("both paid work and unpaid activity",q["wordings"]["english"])
        self.assertIn("rémunérées",q["wordings"]["french"])
        self.assertIn("NOT_TRANSLATED",q["wordings"]["yucatec"])
        self.assertEqual(q["ordinal_scores"],list(range(6)))
        self.assertEqual(len(q["missing_answers"]),2)
        self.assertTrue(q["independent_content_validity_check_pending"])
        self.assertEqual(q["score_status"],"NOT_FROZEN")

    def test_inference_not_claimed_as_calibrated_probability(self):
        p=P["statistical_plan_unfrozen"]
        self.assertIn("permutation",p["primary_inference"])
        self.assertFalse(p["full_preregistration_frozen"])
        self.assertFalse(p["human_prediction_release"])
        self.assertIn("One-sided",p["primary_inference"])
        self.assertTrue(P["prediction"]["no_graded_trait_probability_claimed"])

    def test_no_human_validation_or_runtime_promotion_in_new_protocol(self):
        self.assertEqual(set(P["outcomes"].values()),{0})
        self.assertEqual(S["method_protocol_status"]["runtime_rule_promotions"],0)
        self.assertEqual(S["method_protocol_status"]["pilot_participants"],0)
        self.assertEqual(B07["counters"]["scored_untouched_participants"],0)

if __name__=="__main__":
    unittest.main()
