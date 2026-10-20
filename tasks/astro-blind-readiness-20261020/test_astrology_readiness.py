"""Negative-control tests for astrology prereg readiness, NOT psychology accuracy."""
from __future__ import annotations

import copy
import unittest
from pathlib import Path

from check_astrology_readiness import load, validate

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
class ReadinessAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good=load()

    def test_01_original_source_sha_and_all_ten_gates_enforced(self):
        result=validate(self.good,ROOT)
        self.assertEqual(result["status"],"NOT_READY_SOURCE_AND_ENGINEERING_ONLY")
        self.assertEqual(result["gate_count"],10)
        self.assertEqual(len(result["blocking_gate_ids"]),10)
        self.assertEqual(result["real_human_predictive_validations"],0)

    def test_02_source_history_is_documentary_count_not_people(self):
        result=validate(self.good,ROOT)
        self.assertEqual(result["historical_documentary_annotations_across_distinct_branches"],15098)
        self.assertEqual(self.good["source_provenance"]["chinese_ziwei_source_annotations"],586)
        self.assertEqual(self.good["source_provenance"]["chinese_bazi_source_annotations"],210)
        self.assertFalse(self.good["source_provenance"]["cross_branch_registry_integrated"])

    def test_03_do_not_mark_pilot_ready_before_all_ten_gates(self):
        tampered=copy.deepcopy(self.good)
        tampered["pilot_eligibility"]["candidate_pilot_ready"]=True
        with self.assertRaisesRegex(ValueError,"candidate ready"):
            validate(tampered,ROOT)

    def test_04_do_not_overrule_important_gate_as_nonblocking(self):
        tampered=copy.deepcopy(self.good)
        tampered["candidate_pilot_gates"][3]["blocking"]=False
        with self.assertRaisesRegex(ValueError,"nonblocking"):
            validate(tampered,ROOT)

    def test_05_do_not_mark_gate_verified_without_evidence_receipt(self):
        tampered=copy.deepcopy(self.good)
        tampered["candidate_pilot_gates"][0]["status"]="verified"
        with self.assertRaisesRegex(ValueError,"pinned receipt"):
            validate(tampered,ROOT)

    def test_06_do_not_invent_or_discard_gates(self):
        tampered=copy.deepcopy(self.good)
        tampered["candidate_pilot_gates"].pop()
        with self.assertRaisesRegex(ValueError,"gates missing"):
            validate(tampered,ROOT)

    def test_07_source_index_is_immutably_sha_bound(self):
        tampered=copy.deepcopy(self.good)
        tampered["source_provenance"]["chinese_accepted_index_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"source index SHA"):
            validate(tampered,ROOT)

    def test_08_cannot_say_past_synthetic_study_validates_humans(self):
        tampered=copy.deepcopy(self.good)
        tampered["source_provenance"]["independent_real_human_predictive_validations"]=1
        with self.assertRaisesRegex(ValueError,"real people"):
            validate(tampered,ROOT)

    def test_09_cannot_turn_unregistered_design_into_scored_questionnaire(self):
        tampered=copy.deepcopy(self.good)
        tampered["pilot_eligibility"]["scored_human_questionnaire_authorized"]=True
        with self.assertRaisesRegex(ValueError,"falsely readied"):
            validate(tampered,ROOT)

    def test_10_discriminatory_historical_health_claims_excluded(self):
        tampered=copy.deepcopy(self.good)
        tampered["pilot_eligibility"]["historical_gender_disease_longevity_and_moral_claims_excluded_from_medicine_and_human_stereotyping"]=False
        with self.assertRaisesRegex(ValueError,"pseudo-clinical"):
            validate(tampered,ROOT)

    def test_11_owner_and_Hale_not_called_untouched_final_cases(self):
        tampered=copy.deepcopy(self.good)
        tampered["pilot_eligibility"]["already_inspected_owner_Hale_ineligible_as_untouched_final_test"]=False
        with self.assertRaisesRegex(ValueError,"known/exploratory"):
            validate(tampered,ROOT)

    def test_12_missing_local_original_source_evidence_fails(self):
        tampered=copy.deepcopy(self.good)
        tampered["source_and_engine_evidence"][0]["evidence_local"]="does/not/exist.json"
        with self.assertRaisesRegex(ValueError,"local path"):
            validate(tampered,ROOT)

if __name__ == "__main__":
    unittest.main()
