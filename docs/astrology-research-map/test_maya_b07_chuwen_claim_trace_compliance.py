#!/usr/bin/env python3
"""Verify source-to-observable contract; not an empirical astrology test."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).parent
def read(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
S=read("CLAIM_TRACE_SCHEMA_V1.json")
C=read("MAYA_B07_CHUWEN_ARTISAN_SOURCE_TO_OBSERVABLE_TRACE.json")
D=read("MAYA_B07_ARTISAN_BLIND_STUDY_DRAFT_V1.json")
W=read("MAYA_B07_YUCATEC_ARTISAN_WITNESS_VARIANTS.json")

class SourceTraceTests(unittest.TestCase):
    def test_declared_schema_required_fields(self):
        self.assertEqual(set(C),set(S["required"]))
        for k in S["required"]:
            obj=S["properties"][k]
            if "required" in obj:
                self.assertTrue(set(obj["required"]).issubset(set(C[k])))

    def test_classification_and_original_sha(self):
        self.assertEqual(C["prediction_class"],"natal_trait")
        self.assertEqual(C["source_witness"]["original_source_hash_sha256"],W["source_english"]["original_pdf_sha256"])
        self.assertEqual(C["chart_feature"]["uncertainty_state"],"conflicted")
        self.assertIsNone(C["chart_feature"]["predicate"])

    def test_not_human_predictive_success_or_frozen(self):
        self.assertEqual(C["readiness"]["stage"],"source_only")
        self.assertFalse(C["readiness"]["frozen_before_outcomes"])
        self.assertEqual(C["human_evidence"]["untouched_test_participants"],0)
        self.assertEqual(C["human_evidence"]["validated_predictive_successes"],0)

    def test_paid_crafts_initially_missing_and_revision_unfrozen(self):
        a=D["source_construct_alignment_revision"]
        self.assertTrue(a["original_draft_item_excludes_paid_work"])
        self.assertTrue(a["historic_claim_includes_professional_making_roles"])
        self.assertFalse(a["independent_content_validity_review_complete"])
        self.assertFalse(a["promoted_to_primary_question"])
        self.assertFalse(a["revision_made_after_scored_human_outcomes"])
        self.assertIn("paid and unpaid",a["proposed_alternate_item_NOT_FROZEN"])

    def test_composite_not_allowed_to_rescue_chuen(self):
        self.assertEqual(D["primary"]["canonical_yucatec_day"],"CHUWEN")
        self.assertTrue(D["exploratory_not_primary"]["not_usable_to_rescue_failed_single_CHUWEN_result"])
        self.assertFalse(D["primary"]["source_construct_equivalence_established"])
        self.assertEqual(len(C["source_witness"]["alternate_witness_ids"]),5)

    def test_null_comparison_and_mismatch_reporting(self):
        self.assertIn("fails",C["observable"]["falsifier"])
        self.assertIn("age/trade/access",C["readiness"]["nonastrology_null_spec"])
        self.assertTrue(C["dependencies"]["source_lineage_ids"])
        self.assertTrue(C["readiness"]["exclusion_reason"])

    def test_small_n60_only_methodological(self):
        x=D["feasibility_interpretation"]
        self.assertEqual(x["random_cohort_60_expected_single_Chuen_birthdays_approx"],3.0)
        self.assertAlmostEqual(x["approx_probability_zero_Chuen_in_60_if_independent_uniform"],.95**60,places=3)
        self.assertTrue(x["methodological_pilot_not_significance_claim"])

if __name__=="__main__":
    unittest.main()
