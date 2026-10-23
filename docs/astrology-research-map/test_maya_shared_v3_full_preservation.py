#!/usr/bin/env python3
"""Full original V3 optional bank unchanged inside the nondeployed joint-test candidate.

The standalone builder reads the pinned old Git commit when regenerating;
these tests deliberately run offline with the saved original-object hashes.
"""
import copy,hashlib,json
import unittest
from pathlib import Path
ROOT=Path(__file__).parent
def read(f):return json.loads((ROOT/f).read_text(encoding="utf-8"))
S=read("MAYA_SHARED_SURVEY_EXISTING_INSTRUMENT_SNAPSHOT_V1.json")
C=read("MAYA_SHARED_LIFE_PATTERNS_V3_FINAL_STAGE_CANDIDATE_V1.json")
B=read("MAYA_SHARED_CROSS_TRADITION_SURVEY_INTEGRATION_V1.json")
def hash_item(x):
    return hashlib.sha256(json.dumps(
      x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

class JointSurveyV3NoChanges(unittest.TestCase):
    def test_complete_original_23_questions_preserved_in_same_order(self):
        q=C["original_v3_all_23_questions_verbatim"]
        self.assertEqual(len(q),23)
        self.assertEqual([x["id"] for x in q],S["survey_v3"]["question_ids"])
        self.assertEqual({x["id"]:hash_item(x) for x in q},
                         S["survey_v3"]["all_existing_question_object_sha256"])
        self.assertTrue(C["exact_original_survey_source"]["all_original_question_objects_unmodified"])

    def test_complete_original_7_optional_probes_preserved_in_same_order(self):
        q=C["original_v3_all_7_conditional_probes_verbatim"]
        self.assertEqual(len(q),7)
        self.assertEqual([x["id"] for x in q],S["survey_v3"]["microprobe_ids"])
        self.assertEqual({x["id"]:hash_item(x) for x in q},
                         S["survey_v3"]["all_existing_microprobe_object_sha256"])
        self.assertTrue(C["exact_original_survey_source"]["all_original_probe_objects_unmodified"])

    def test_maya_question_is_only_proposed_and_never_inserted_into_live_bank(self):
        x=C["additional_nonactive_future_shared_gap_probe"]
        self.assertEqual(x,B["one_proposed_conditional_shared_probes"][0])
        self.assertNotIn(x["id"],[q["id"] for q in C["original_v3_all_23_questions_verbatim"]])
        self.assertNotIn(x["id"],[q["id"] for q in C["original_v3_all_7_conditional_probes_verbatim"]])
        self.assertFalse(C["existing_live_Life_Patterns_app_modified"])
        self.assertFalse(C["existing_HD_V43_or_survey_V2_modified"])
        self.assertFalse(C["test_started"])

    def test_preserved_source_hash_and_no_auto_promotion(self):
        o=C["exact_original_survey_source"]
        self.assertEqual(o["source_sha256"],S["survey_v3"]["sha256_original_bytes"])
        self.assertEqual(o["commit"],S["survey_v3"]["git_commit"])
        self.assertEqual(C["status"],"OFFLINE_RESEARCH_DESIGN_CANDIDATE_NOT_FROZEN_NOT_DEPLOYED")
        self.assertTrue(C["future_question_selection_and_per_tradition_model_freeze_outstanding"])
        self.assertTrue(C["prior_answers_may_inform_development_but_not_validate_final_cohort"])
        self.assertEqual(C["source_natal_claims_behaviorally_validated"],0)

    def test_a_mutated_respondent_question_text_would_fail_original_content_hash(self):
        q=copy.deepcopy(C["original_v3_all_23_questions_verbatim"])
        q[0]["question"]="Modified after seeing the answers"
        self.assertNotEqual({x["id"]:hash_item(x) for x in q},
                            S["survey_v3"]["all_existing_question_object_sha256"])

if __name__=="__main__":
    unittest.main()
