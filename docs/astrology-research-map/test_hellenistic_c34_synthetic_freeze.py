"""C34 synthetic-only seal / response-order / score integrity regressions.

These tests DO NOT claim external timestamping, real consent, true blind
humans or successful historical astrology.
"""
from pathlib import Path
import copy
import hashlib
import json
import tempfile
import unittest

from hellenistic_c34_synthetic_blind_freeze import (
    SOURCE_SHA256, MOCK_SEED, QUESTION,
    canonical, digest, wrap, verify, file_read, new_file,
    freeze_from_c33, deterministic_mock_outcomes,
    score_mock, _statistic,
    verify_source_locked_freeze, mock_outcome_from_synthetic_id,
)

HERE=Path(__file__).resolve().parent
SOURCE=HERE/"HELLENISTIC_C33_UTC_2020_SYNTHETIC_CLASSIFIER_V1.json"
FREEZE=HERE/"HELLENISTIC_C34_SYNTHETIC_PREANSWER_FREEZE_V1.json"
ANSWERS=HERE/"HELLENISTIC_C34_SYNTHETIC_MOCK_OUTCOMES_V1.json"
SCORE=HERE/"HELLENISTIC_C34_SYNTHETIC_STRATIFIED_SCORE_V1.json"


class TestC34SyntheticFreeze(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.freeze=file_read(FREEZE)
        cls.answers=file_read(ANSWERS)
        cls.score=file_read(SCORE)
        cls.freeze_body=verify(
            cls.freeze,expected_schema="C34_SYNTHETIC_PREANSWER_PREDICTIONS_V1")
        cls.outcome_body=verify(
            cls.answers,expected_schema="C34_SYNTHETIC_MOCK_OUTCOMES_V1")

    def test_full_source_freeze_replay_exact(self):
        self.assertEqual(
            hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA256)
        self.assertEqual(freeze_from_c33(SOURCE),self.freeze)
        self.assertEqual(self.freeze["sha256"],
                         "d6405eca803e5fdb6d990266e0290d1de9ba980cee996886654f9257c3c49216")

    def test_phase_order_and_unchanged_response_replay(self):
        self.assertEqual(deterministic_mock_outcomes(self.freeze),self.answers)
        self.assertEqual(score_mock(self.freeze,self.answers),self.score)
        self.assertEqual(self.score["body"]["freeze_sha256"],self.freeze["sha256"])
        self.assertEqual(self.score["body"]["mock_response_sha256"],self.answers["sha256"])
        self.assertTrue(self.outcome_body["generated_after_frozen_prediction_packet"])
        self.assertTrue(self.score["body"]["source_pre_answer_freeze_preceded_mock_outcome_generation"])

    def test_no_outcomes_in_frozen_packet_and_no_private_inputs(self):
        b=self.freeze_body
        self.assertEqual(b["cohort_size"],366)
        self.assertEqual(len(b["frozen_cohort"]),366)
        self.assertTrue(b["synthetic_only"])
        self.assertFalse(b["real_person_births_used"])
        self.assertFalse(b["real_human_outcomes_available"])
        self.assertTrue(b["rehearsal_not_a_trusted_timestamped_preregistration"])
        self.assertNotIn("observations",b)
        self.assertNotIn("marriage_outcome",canonical(b).decode())
        self.assertTrue(all(r["synthetic_id"].startswith("MOCK-C34-")
                            for r in b["frozen_cohort"]))
        self.assertEqual(
            len(set(r["synthetic_id"] for r in b["frozen_cohort"])),366)
        self.assertEqual(digest([r["synthetic_id"] for r in b["frozen_cohort"]]),
                         b["participant_set_sha256"])

    def test_ancient_clause_does_not_predict_exactly_one_if_not_exposed(self):
        b=self.freeze_body
        self.assertTrue(b["nonpositive_sign_is_not_a_source_prediction_of_one_marriage"])
        self.assertIn("analyst_inference_not_literal_Ptolemy",b["analysis_contract"])
        counts={True:0,False:0,None:0}
        for row in b["frozen_cohort"]:
            counts[row["indicated_source_subclause"]]+=1
        self.assertEqual(counts,{True:55,False:186,None:125})

    def test_score_is_declared_mock_not_human_astrology_efficacy(self):
        b=self.score["body"]
        self.assertTrue(b["synthetic_only"])
        self.assertTrue(b["not_a_human_astrology_validation"])
        self.assertFalse(b["any_source_effect_measured_in_real_population"])
        self.assertEqual(b["actual_human_predictions"],0)
        self.assertEqual(b["scored_conditional_known"],241)
        self.assertEqual(b["birth_sign_condition_indeterminate"],125)
        self.assertEqual(b["response_unknowns"],0)
        self.assertEqual(b["predeclared_permutations"],1999)
        self.assertEqual(b["month_stratified_risk_difference_mock"],
                         -0.06010717511815876)
        self.assertEqual(b["month_stratified_one_sided_permutation_p_MOCK_ONLY"],
                         .862)

    def test_outcome_generation_invariant_when_signs_mutated_in_isolated_copy(self):
        changed=copy.deepcopy(self.freeze)
        for row in changed["body"]["frozen_cohort"]:
            value=row["indicated_source_subclause"]
            if value is not None:
                row["indicated_source_subclause"]=not value
        changed["sha256"]=digest(changed["body"])
        # Recomputed SHA is NOT permission to retune source exposures.
        with self.assertRaises(ValueError):
            deterministic_mock_outcomes(changed)
        with self.assertRaises(ValueError):
            score_mock(changed,self.answers)
        # Yet the separately scoped outcome generator uses NO source sign.
        before = [mock_outcome_from_synthetic_id(r["synthetic_id"],
                  r["birth_month_stratum"]) for r in self.freeze_body["frozen_cohort"]]
        after = [mock_outcome_from_synthetic_id(r["synthetic_id"],
                 r["birth_month_stratum"]) for r in changed["body"]["frozen_cohort"]]
        self.assertEqual(before,after)
        self.assertNotEqual(changed["sha256"],self.freeze["sha256"])

    def test_even_rehashed_analysis_seed_change_rejected(self):
        altered=copy.deepcopy(self.freeze)
        altered["body"]["analysis_contract"]["permutation_seed"]+=1
        altered["sha256"]=digest(altered["body"])
        with self.assertRaises(ValueError):
            verify_source_locked_freeze(altered)
        with self.assertRaises(ValueError):
            score_mock(altered,self.answers)

    def test_scorer_enforces_exact_preanswer_source_hash_and_cohort(self):
        verify_source_locked_freeze(self.freeze)
        altered=copy.deepcopy(self.freeze)
        altered["body"]["source_snapshot_sha256"]="0"*64
        altered["sha256"]=digest(altered["body"])
        with self.assertRaises(ValueError):
            verify_source_locked_freeze(altered)

    def test_source_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/"tampered.json"
            src.write_bytes(SOURCE.read_bytes()+b" ")
            with self.assertRaises(ValueError):
                freeze_from_c33(src)

    def test_packet_freeze_hash_tamper_rejected(self):
        packet=copy.deepcopy(self.freeze)
        packet["body"]["frozen_cohort"][0]["indicated_source_subclause"]=True
        with self.assertRaises(ValueError):
            verify(packet,expected_schema="C34_SYNTHETIC_PREANSWER_PREDICTIONS_V1")
        with self.assertRaises(ValueError):
            score_mock(packet,self.answers)

    def test_mock_outcome_hash_tamper_rejected(self):
        packet=copy.deepcopy(self.answers)
        packet["body"]["observations"][0]["simulated_binary_marriage_outcome"]="unknown"
        with self.assertRaises(ValueError):
            score_mock(self.freeze,packet)

    def test_outcome_from_different_freeze_rejected_even_with_valid_hash(self):
        packet=copy.deepcopy(self.answers)
        packet["body"]["freeze_sha256"]="0"*64
        packet["sha256"]=digest(packet["body"])
        with self.assertRaises(ValueError):
            score_mock(self.freeze,packet)

    def test_duplicate_or_missing_response_rejected(self):
        changed=copy.deepcopy(self.answers)
        changed["body"]["observations"][-1]["synthetic_id"]=changed["body"]["observations"][0]["synthetic_id"]
        changed["sha256"]=digest(changed["body"])
        with self.assertRaises(ValueError):
            score_mock(self.freeze,changed)
        missing=copy.deepcopy(self.answers)
        missing["body"]["observations"].pop()
        missing["sha256"]=digest(missing["body"])
        with self.assertRaises(ValueError):
            score_mock(self.freeze,missing)

    def test_unknowns_retained_but_unscored_no_relabel(self):
        packet=copy.deepcopy(self.answers)
        packet["body"]["observations"][0]["simulated_binary_marriage_outcome"]="unknown"
        packet["sha256"]=digest(packet["body"])
        result=score_mock(self.freeze,packet)
        self.assertEqual(result["body"]["response_unknowns"],1)
        self.assertEqual(result["body"]["scored_conditional_known"],241)

    def test_invalid_value_rejected_even_with_matching_sha(self):
        packet=copy.deepcopy(self.answers)
        packet["body"]["observations"][0]["simulated_binary_marriage_outcome"]="seven"
        packet["sha256"]=digest(packet["body"])
        with self.assertRaises(ValueError):
            score_mock(self.freeze,packet)
        packet["body"]["observations"][0]["this_is_not_a_real_marriage_history"]=False
        packet["sha256"]=digest(packet["body"])
        with self.assertRaises(ValueError):
            score_mock(self.freeze,packet)

    def test_exclusive_write_refuses_overwriting_existing_freeze(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"freeze.json"
            new_file(p,self.freeze)
            once=p.read_bytes()
            with self.assertRaises(FileExistsError):
                new_file(p,self.freeze)
            self.assertEqual(once,p.read_bytes())

    def test_mismatched_frozen_schema_not_accepted(self):
        p=copy.deepcopy(self.freeze)
        p["body"]["schema"]="OTHER_SCHEMA"
        p["sha256"]=digest(p["body"])
        with self.assertRaises(ValueError):
            score_mock(p,self.answers)

    def test_month_strata_are_same_prospectively_declared_population(self):
        rows=self.freeze_body["frozen_cohort"]
        self.assertEqual(sorted(set(x["birth_month_stratum"] for x in rows)),
                         [f"2020-{m:02d}" for m in range(1,13)])
        y={x["synthetic_id"]:int(x["simulated_binary_marriage_outcome"]=="two_plus")
           for x in self.outcome_body["observations"]}
        _,details=_statistic(rows,y)
        self.assertEqual(len(details),12)
        self.assertEqual(sum(v["scored"] for v in details),241)
        self.assertTrue(all(x["source_positive_count"]>0
                            and x["source_comparator_count"]>0 for x in details))

class TestC34RealHumanStudyBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gates=json.loads((HERE/"HELLENISTIC_C34_REAL_STUDY_READINESS_GATES_V1.json").read_text(encoding="utf8"))

    def test_every_actual_human_launch_gate_explicitly_unmet(self):
        g=self.gates
        self.assertEqual(g["root_status"],"OPEN")
        self.assertEqual(g["C34_status"],"SYNTHETIC_DRY_RUN_COMPLETED_NO_HUMAN_DATA")
        f=g["all_study_status_flags"]
        for key in ("real_recruitment_authorized","real_participant_consent_obtained",
                    "any_real_birth_tuples_received","any_real_marriage_history_responses_received",
                    "real_untouched_person_cohort_generated",
                    "live_predictions_timestamped_in_external_immutable_store",
                    "live_concealed_questionnaire_administered",
                    "human_research_ethics_and_data_handling_reviewed",
                    "predeclared_nonastrology_controls_and_sample_plan_approved"):
            self.assertIs(f[key],False,key)
        self.assertEqual(f["real_human_predictive_validations"],0)
        self.assertEqual(f["production_model_promotions"],0)

    def test_real_gate_mock_sha_tied_to_reproduced_artifacts(self):
        s=self.gates["synthetic_output"]
        self.assertEqual(s["synthetic_pre_answer_packet_sha256"],self.freeze["sha256"]
                         if hasattr(self,"freeze") else file_read(FREEZE)["sha256"])
        self.assertEqual(s["synthetic_mock_response_sha256"],file_read(ANSWERS)["sha256"])
        self.assertEqual(s["synthetic_score_sha256"],file_read(SCORE)["sha256"])
        self.assertFalse(self.gates["minimum_future_owner_decision"]
                         ["currently_required_in_this_synthetic_turn"])
        self.assertTrue(self.gates["minimum_future_owner_decision"]
                        ["no_public_repo_storage_of_real_birth_or_marital_data"])

if __name__=="__main__":
    unittest.main()
