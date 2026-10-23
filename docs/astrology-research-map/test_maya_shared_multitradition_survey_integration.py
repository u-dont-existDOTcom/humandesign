#!/usr/bin/env python3
"""Cross-tradition Maya / shared survey integration acceptance checks.

Human validation is deliberately absent: tests verify metadata links,
coverage, provenance and fail-closed protection of existing survey banks.
"""
from __future__ import annotations
import unittest,json,hashlib
from copy import deepcopy
from pathlib import Path
from compile_maya_shared_survey_bridge import (
  compile_bridge,BridgeInvariantError,load
)
from build_maya_complete_source_coverage import create as make_source_index
from maya_calendar_reference import YUCATEC_DAYS,KICHE_DAY_NAMES_BY_YUCATEC

ROOT=Path(__file__).resolve().parent
S=load("MAYA_SHARED_SURVEY_EXISTING_INSTRUMENT_SNAPSHOT_V1.json")
SOURCE=load("MAYA_COMBINED_SOURCE_DAYNAME_SURVEY_INDEX_V1.json")
M=load("MAYA_SHARED_CROSS_TRADITION_SURVEY_INTEGRATION_V1.json")
COMPILED=load("MAYA_SHARED_SURVEY_COMPILED_NONDEPLOYED_PLAN_V1.json")

class IntegratedMayaSurveyNoNewStandaloneTest(unittest.TestCase):
    def test_all_original_research_survey_ids_source_anchored(self):
        v3=S["survey_v3"]
        self.assertEqual(v3["git_commit"],"7971b3c1564d9c38bce17abe4c4575affcba2c76")
        self.assertEqual(v3["sha256_original_bytes"],
                         "fec3d0d18b9463d29842e65c4759fd7ed900a019889531896f89c1b3764e0084")
        self.assertEqual(len(v3["question_ids"]),23)
        self.assertEqual(len(v3["microprobe_ids"]),7)
        self.assertEqual(len(S["human_design_survey_bank"]["question_ids"]),81)
        self.assertEqual(len(S["tendency_first"]["question_ids"]),25)
        self.assertEqual(len(S["experience_meaning"]["question_ids"]),8)
        self.assertEqual(v3["max_base_optional_topics_per_session"],5)
        self.assertEqual(v3["max_additional_conditional_probes_per_session"],2)
        self.assertTrue(v3["decline_all_allowed"])
        self.assertEqual(v3["source_status"],"DEVELOPMENT_OPT_IN_NO_LIVE_OR_CHART_SCORING")
        self.assertTrue(all(not i["already_live"] for i in v3["selected_existing_question_definitions"]))

    def test_source_selected_questions_have_exact_text_hashes(self):
        for q in S["survey_v3"]["selected_existing_question_definitions"]:
            self.assertEqual(hashlib.sha256(q["question"].encode()).hexdigest(),q["question_sha256"])
            self.assertIn(q["id"],S["survey_v3"]["question_ids"])

    def test_20_Yucatec_and_20_highland_day_variants_are_held_without_copying_meanings(self):
        self.assertEqual(SOURCE,make_source_index())
        y=SOURCE["Yucatec_colonial_named_days"]
        h=SOURCE["Highland_Kiche_two_community_named_day_pairs"]
        self.assertEqual(len(y),20)
        self.assertEqual(len(h),20)
        self.assertEqual({v["canonical_Yucatec_day_name"] for v in y},set(YUCATEC_DAYS))
        self.assertEqual({v["Kiche_day_name"] for v in h},set(KICHE_DAY_NAMES_BY_YUCATEC))
        self.assertEqual(len([v for v in y if v["source_claim_disposition"]=="QUARANTINE"]),15)
        self.assertTrue(all(not v["automatically_scored"] for v in y+h))
        self.assertTrue(SOURCE["identity_matching_is_not_source_prediction_equivalence"])

    def test_cross_tradition_name_borrowing_not_mistaken_as_same_prediction(self):
        a=next(v for v in SOURCE["Yucatec_colonial_named_days"] if v["canonical_Yucatec_day_name"]=="CHUWEN")
        b=next(v for v in SOURCE["Highland_Kiche_two_community_named_day_pairs"] if v["Kiche_day_name"]=="B’ATZ’")
        self.assertEqual(a["Kiche_linguistic_crosswalk_not_same_natal_predicate"],"B’ATZ’")
        self.assertEqual(b["Yucatec_linguistic_crosswalk_not_same_natal_predicate"],"CHUWEN")
        self.assertNotEqual("B’ATZ’","CHUWEN")
        self.assertFalse(b["same_community_or_source"])

    def test_deployed_survey_untouched_and_single_shared_future_interview(self):
        self.assertTrue(M["final_test_integration"]["one_common_behavioral_interview_for_all_eligible_natal_systems"])
        self.assertTrue(M["final_test_integration"]["original_Life_Patterns_v19_live_question_bank_unchanged"])
        self.assertTrue(M["final_test_integration"]["existing_Human_Design_V2_frozen_model_unchanged"])
        self.assertFalse(M["readiness"]["live_app_modified"])
        self.assertFalse(M["readiness"]["standalone_Maya_questionnaire_created"])
        self.assertFalse(M["readiness"]["joint_human_test_commenced"])
        self.assertFalse(M["readiness"]["final_questionnaire_frozen"])
        self.assertEqual(M["readiness"]["scored_participants"],0)

    def test_shared_domain_coverage_not_falsely_direct(self):
        self.assertEqual(len(M["common_observables"]),8)
        self.assertTrue(all(not d["direct_measure_exists"] for d in M["common_observables"]))
        claims=M["source_claim_bindings"]
        self.assertEqual(len(claims),11)
        self.assertTrue(all(not v["individual_predictive_accuracy_verified"] for v in claims))
        d=next(v for v in M["common_observables"] if v["id"]=="CRAFT_SKILLED_WORK")
        self.assertEqual(d["existing_question_ids"],["VOCATION","LEARNING_HISTORY","ART"])
        self.assertEqual(d["existing_question_coverage"],"PROXY_ONLY")

    def test_one_neutral_optional_probe_not_a_new_maya_questionnaire(self):
        p=M["one_proposed_conditional_shared_probes"]
        self.assertEqual(len(p),1)
        x=p[0]
        self.assertNotIn("Chuen",x["neutral_prompt"])
        self.assertNotIn("Maya",x["neutral_prompt"])
        self.assertIn("irrespective of predicted day sign",x["trigger_rule"])
        self.assertTrue(x["must_not_ask_based_on_natal_chart"])
        self.assertEqual(x["no_change_to_existing_v3_question_count"],23)
        self.assertEqual(x["stage"],"FUTURE_FINAL_SHARED_SURVEY_RESEARCH_CANDIDATE_NOT_ADDED_TO_LIVE_APP")

    def test_existing_ART_VOCATION_LEARNING_TRAVEL_RECIPROCITY_remain_one_each(self):
        output=compile_bridge()
        q={x["question_id"]:x for x in output["source_pinned_behavioral_question_reuses"]}
        for key in ["ART","VOCATION","LEARNING_HISTORY","TRAVEL","RECIPROCITY","TF1-G01"]:
            self.assertIn(key,q)
            self.assertFalse(q[key]["actual_existing_question_modified"])
        c={x["facet_id"]:x for x in output["single_shared_answer_facets"]}
        self.assertGreaterEqual(len(c["CRAFT_SKILLED_WORK"]["claim_ids_reusing_same_facet"]),3)
        self.assertFalse(c["CRAFT_SKILLED_WORK"]["counts_as_independent_duplicate_responses"])
        self.assertEqual(output["future_conditional_probe_ids"],["SHARED-PHYSICAL-MAKING-CONTEXT-v1"])

    def test_reproducible_compiled_output_exact(self):
        self.assertEqual(compile_bridge(),COMPILED)
        self.assertEqual(COMPILED["separate_unscored_claims"],11)
        self.assertEqual(COMPILED["maya_source_system_count"],5)
        self.assertEqual(COMPILED["preexisting_shared_v3_optional_questions"],23)
        self.assertEqual(COMPILED["source_predictions_all_separately_unfrozen"],True)
        self.assertEqual(COMPILED["real_participant_records_read_or_emitted"],0)
        self.assertEqual(COMPILED["scoring_or_runtime_changes"],0)

    def test_matched_safe_evidence_never_scores_ancient_ritual_or_dreamspell_as_natal(self):
        docs={x["id"]:x for x in M["maya_source_systems"]}
        self.assertFalse(docs["MAYA-ANCIENT-CODICES"]["eligible_for_shared_respondent_evidence_if_eventually_frozen"])
        self.assertFalse(docs["MAYA-MODERN-DREAMSPELL"]["eligible_for_shared_respondent_evidence_if_eventually_frozen"])
        self.assertEqual(SOURCE["historical_maya_codex_astronomy"],"EXCLUDED_FROM_NATAL_SURVEY_CLAIMS")
        self.assertEqual(SOURCE["new_surveys_or_scoring_rules_deployed"],0)

    def test_adversarial_nonexistent_survey_item_fails(self):
        mutant=deepcopy(M)
        mutant["source_claim_bindings"][0]["survey_question_ids"].append("INVENTED-NEW-MAYA-SURVEY")
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(bridge=mutant)

    def test_adversarial_quick_promotion_of_source_prediction_fails(self):
        mutant=deepcopy(M)
        mutant["source_claim_bindings"][0]["status"]="VALIDATED_HUMAN"
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(bridge=mutant)

    def test_adversarial_cross_culture_day_sign_swap_fails(self):
        mutant=deepcopy(M)
        mutant["source_claim_bindings"][0]["source_day_name"]="B’ATZ’"
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(bridge=mutant)

    def test_adversarial_chart_based_question_selection_fails(self):
        mutant=deepcopy(M)
        mutant["one_proposed_conditional_shared_probes"][0]["must_not_ask_based_on_natal_chart"]=False
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(bridge=mutant)

    def test_adversarial_duplicate_source_claim_fails(self):
        mutant=deepcopy(M)
        mutant["source_claim_bindings"].append(deepcopy(mutant["source_claim_bindings"][0]))
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(bridge=mutant)

    def test_adversarial_silent_live_app_deployment_fails(self):
        mutant=deepcopy(M)
        mutant["readiness"]["live_app_modified"]=True
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(bridge=mutant)

    def test_adversarial_missing_source_or_instrument_bank_detected(self):
        source=deepcopy(SOURCE)
        source["Yucatec_colonial_named_days"].pop()
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(source=source)
        snap=deepcopy(S)
        snap["survey_v3"]["question_ids"].pop()
        with self.assertRaises(BridgeInvariantError):
            compile_bridge(snapshot=snap)

    def test_shared_survey_map_connected_to_existing_root_architecture(self):
        overview=(ROOT/"WORKFLOW.mmd").read_text()
        drill=(ROOT/"SHARED_SURVEY_INTEGRATION.mmd").read_text()
        gates=(ROOT/"SOURCE_TO_TEST_GATES.mmd").read_text()
        arch=(ROOT.parents[1]/"ARCHITECTURE.md").read_text()
        readme=(ROOT/"README.md").read_text()
        self.assertIn("SHARED --> OVERLAP --> FREEZE",overview)
        self.assertIn("READY --> SHARED --> FREEZE",gates)
        self.assertIn("MULTI --> END",drill)
        self.assertIn("SHARED_SURVEY_INTEGRATION.mmd",readme)
        self.assertIn("MAYA_SHARED_CROSS_TRADITION_SURVEY_INTEGRATION_V1.json",arch)

    def test_focused_shared_survey_diagram_has_no_undefined_nodes(self):
        import re
        text=(ROOT/"SHARED_SURVEY_INTEGRATION.mmd").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("flowchart "))
        declared=set(re.findall(r'(?m)^\s*([A-Z][A-Z0-9_]*)\s*(?:\[|\{)',text))
        self.assertGreaterEqual(len(declared),12)
        for line in text.splitlines()[1:]:
            if "-->" not in line:continue
            bare=re.sub(r'"[^"]*"',"",line)
            used=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',bare))
            self.assertFalse(used-declared,f"Undefined map node: {used-declared}")
        self.assertIn("ANSWERS --> MULTI --> END",text)

if __name__=="__main__":
    unittest.main()
