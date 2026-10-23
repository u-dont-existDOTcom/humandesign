#!/usr/bin/env python3
"""Build final-stage *candidate* shared interview from the original V3 instrument.

No participant data. No live questionnaire deployment. Every pre-existing
question and microprobe is preserved verbatim, with exact object digests.
Maya's single possible *source-neutral* clarification lives in a separate
non-active future proposal slot and DOES NOT change the 23+7 source bank.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from build_maya_shared_survey_snapshot import BRANCH,SOURCE,_git
from compile_maya_shared_survey_bridge import load,compile_bridge

ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/"MAYA_SHARED_LIFE_PATTERNS_V3_FINAL_STAGE_CANDIDATE_V1.json"

def canonical_digest(x)->str:
    return hashlib.sha256(json.dumps(
      x,sort_keys=True,ensure_ascii=False,separators=(",",":")
    ).encode("utf-8")).hexdigest()

def build()->dict:
    snap=load("MAYA_SHARED_SURVEY_EXISTING_INSTRUMENT_SNAPSHOT_V1.json")
    survey_root=ROOT.parents[1]
    raw=_git(survey_root,BRANCH,SOURCE)
    digest=hashlib.sha256(raw).hexdigest()
    if snap["survey_v3"]["sha256_original_bytes"]!=digest:
        raise ValueError("Original V3 source has changed; halt integration instead of rewriting existing questions")
    src=json.loads(raw)
    q=src["questions"];micro=src["optional_microprobes"]
    if len(q)!=23 or len(micro)!=7:
        raise ValueError("Expected original V3 full 23 + 7 instrument, no changes")
    digest_map={x["id"]:canonical_digest(x) for x in q}
    probe_map={x["id"]:canonical_digest(x) for x in micro}
    if (digest_map!=snap["survey_v3"]["all_existing_question_object_sha256"] or
        probe_map!=snap["survey_v3"]["all_existing_microprobe_object_sha256"]):
        raise ValueError("Original questionnaire content changed")
    bridge=load("MAYA_SHARED_CROSS_TRADITION_SURVEY_INTEGRATION_V1.json")
    compiled=compile_bridge()
    if len(bridge["one_proposed_conditional_shared_probes"])!=1:
        raise ValueError("No standalone Maya survey or extra mandatory questions allowed")
    suggestion=bridge["one_proposed_conditional_shared_probes"][0]
    return {
      "schema":"MAYA_EXISTING_SHARED_V3_FULL_QUESTIONNAIRE_WITH_NONACTIVE_SOURCE_OVERLAY_V1",
      "status":"OFFLINE_RESEARCH_DESIGN_CANDIDATE_NOT_FROZEN_NOT_DEPLOYED",
      "prepared_utc_date":"2026-10-23",
      "exact_original_survey_source":{
        "commit":BRANCH,"file":SOURCE,"source_sha256":digest,
        "existing_question_count":23,
        "existing_conditional_microprobes_count":7,
        "all_original_question_objects_unmodified":True,
        "all_original_probe_objects_unmodified":True,
        "opt_in_topics_not_mandatory":True,
        "max_base_optional_topics_per_session":src["max_base_optional_topics_per_session"],
        "max_additional_conditional_probes_per_session":src["max_additional_conditional_probes_per_session"]
      },
      "original_v3_all_23_questions_verbatim":q,
      "original_v3_all_7_conditional_probes_verbatim":micro,
      "additional_nonactive_future_shared_gap_probe":suggestion,
      "existing_shared_survey_question_ids_linked_to_Maya": [
         x["question_id"] for x in compiled["source_pinned_behavioral_question_reuses"]
      ],
      "Maya_claim_count_mapped_source_only":compiled["separate_unscored_claims"],
      "Maya_full_source_day_counts":{"colonial_Yucatec":20,"Kiche_community_pairs":20},
      "does_not_reorder_or_require_questions":True,
      "chart_features_cannot_select_questions":True,
      "prior_answers_may_inform_development_but_not_validate_final_cohort":True,
      "requires_new_consenting_untouched_people_to_validate":True,
      "existing_live_Life_Patterns_app_modified":False,
      "existing_HD_V43_or_survey_V2_modified":False,
      "future_question_selection_and_per_tradition_model_freeze_outstanding":True,
      "source_natal_claims_behaviorally_validated":0,
      "test_started":False
    }

if __name__=="__main__":
    payload=build()
    OUTPUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(OUTPUT,len(payload["original_v3_all_23_questions_verbatim"]),
          len(payload["original_v3_all_7_conditional_probes_verbatim"]))
