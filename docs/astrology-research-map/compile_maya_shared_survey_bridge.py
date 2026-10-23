#!/usr/bin/env python3
"""Compile Maya source claims into EXISTING Life Patterns survey references.

This is a *metadata-only* integration: does not load birth dates, answers,
answer keys, questionnaire respondent records, live plugins or HD scorers.
It does not create a dedicated Maya questionnaire or conduct a human test.

Source identities are distinct. A K'iche' day-name translation is never
substituted for a colonial Yucatec birth rule. Multiple traditions can point
to the same future response without becoming independent evidence.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SNAPSHOT="MAYA_SHARED_SURVEY_EXISTING_INSTRUMENT_SNAPSHOT_V1.json"
SOURCE_COVERAGE="MAYA_COMBINED_SOURCE_DAYNAME_SURVEY_INDEX_V1.json"
CONFIG="MAYA_SHARED_CROSS_TRADITION_SURVEY_INTEGRATION_V1.json"
OUTPUT="MAYA_SHARED_SURVEY_COMPILED_NONDEPLOYED_PLAN_V1.json"

class BridgeInvariantError(ValueError): pass

def load(name:str)->dict:
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def compile_bridge(snapshot:dict|None=None,source:dict|None=None,bridge:dict|None=None)->dict:
    snap=snapshot if snapshot is not None else load(SNAPSHOT)
    src=source if source is not None else load(SOURCE_COVERAGE)
    cfg=bridge if bridge is not None else load(CONFIG)
    if len(src["Yucatec_colonial_named_days"])!=20 or len(src["Highland_Kiche_two_community_named_day_pairs"])!=20:
        raise BridgeInvariantError("20+20 source identity audit is a prerequisite for this source overlay")
    if len(snap["survey_v3"]["question_ids"])!=23 or len(snap["survey_v3"]["microprobe_ids"])!=7:
        raise BridgeInvariantError("Source-pinned V3 optional bank was not the audited one")
    if len(snap["tendency_first"]["question_ids"])!=25 or len(snap["human_design_survey_bank"]["question_ids"])!=81:
        raise BridgeInvariantError("Another instrument changed; do not silently retrofit it")
    if len(snap["experience_meaning"]["question_ids"])!=8:
        raise BridgeInvariantError("Existing separate experience-source IDs changed")
    if snap["survey_v3"]["source_status"]!="DEVELOPMENT_OPT_IN_NO_LIVE_OR_CHART_SCORING":
        raise BridgeInvariantError("Source V3 was not the nonlive research candidate")
    yuc_names={v["canonical_Yucatec_day_name"] for v in src["Yucatec_colonial_named_days"]}
    high_names={v["Kiche_day_name"] for v in src["Highland_Kiche_two_community_named_day_pairs"]}
    if len(yuc_names)!=20 or len(high_names)!=20:raise BridgeInvariantError("Duplicate original tradition day name")
    known_v3=set(snap["survey_v3"]["question_ids"])
    known_tf=set(snap["tendency_first"]["question_ids"])
    known=known_v3|known_tf
    domain_ids={v["id"] for v in cfg["common_observables"]}
    if len(domain_ids)!=len(cfg["common_observables"]):raise BridgeInvariantError("Duplicate shared behavioral facet")
    claim_ids=[v["id"] for v in cfg["source_claim_bindings"]]
    if len(claim_ids)!=len(set(claim_ids)):raise BridgeInvariantError("Duplicate source claim IDs")
    systems={v["id"]:v for v in cfg["maya_source_systems"]}
    reused_question_to_claims=defaultdict(set)
    shared_facet_to_claims=defaultdict(set)
    for claim in cfg["source_claim_bindings"]:
        system=systems.get(claim["system_id"])
        if system is None:raise BridgeInvariantError("Claim source tradition not registered")
        allowed=yuc_names if system["id"]=="MAYA-YUCATEC-COLONIAL-NATAL" else high_names
        if claim["source_day_name"] not in allowed:
            raise BridgeInvariantError("Yucatec/K'iche' source-day name equivalence silently corrupted")
        if not claim["status"].startswith(("SOURCE_ONLY","EXPLORATORY")):
            raise BridgeInvariantError("Source-only claims may not be silently promoted to scoring")
        if claim["individual_predictive_accuracy_verified"]:
            raise BridgeInvariantError("No empirical human validations recorded in source materials")
        for facet in claim["observable_ids"]:
            if facet not in domain_ids:raise BridgeInvariantError("Unknown shared behavioral construct")
            shared_facet_to_claims[facet].add(claim["id"])
        for question_id in claim["survey_question_ids"]:
            if question_id not in known:
                raise BridgeInvariantError("Claim refers to a question absent from the existing banks")
            reused_question_to_claims[question_id].add(claim["id"])
    optional=cfg["one_proposed_conditional_shared_probes"]
    if len(optional)>1:raise BridgeInvariantError("One optional missing-domain clarification maximum")
    for probe in optional:
        if probe["id"] in known:
            raise BridgeInvariantError("Conditional probe collides with an actual survey question")
        if not probe["must_not_ask_based_on_natal_chart"] or not probe["source_neutral_no_astrology_day_name_in_prompt"]:
            raise BridgeInvariantError("Chart-directed or astrological cue questions cannot enter shared interview")
        if probe["stage"]!="FUTURE_FINAL_SHARED_SURVEY_RESEARCH_CANDIDATE_NOT_ADDED_TO_LIVE_APP":
            raise BridgeInvariantError("Unfrozen research question accidentally represented as deployed")
        if probe["no_change_to_existing_v3_question_count"]!=23:
            raise BridgeInvariantError("V3 existing questions cannot be modified by adding a source-specific probe")
    if not cfg["final_test_integration"]["one_common_behavioral_interview_for_all_eligible_natal_systems"]:
        raise BridgeInvariantError("Owner selected a single shared interview, not a Maya-only follow-up")
    if cfg["readiness"]["live_app_modified"] or cfg["readiness"]["joint_human_test_commenced"]:
        raise BridgeInvariantError("Research-only overlay must never claim deployment or human testing")
    # Stable, no observable response content; sums are catalog entries, not effects.
    return {
        "schema":"COMPILED_MAYA_TO_SHARED_SURVEY_RESEARCH_OVERLAY_V1",
        "status":"COMPILED_METADATA_ONLY_NOT_FROZEN_NOT_DEPLOYED",
        "source_snapshots":[SNAPSHOT,SOURCE_COVERAGE,CONFIG],
        "maya_source_system_count":len(systems),
        "yucatec_source_day_names":len(yuc_names),
        "Kiche_source_day_name_pairs":len(high_names),
        "separate_unscored_claims":len(claim_ids),
        "preexisting_shared_v3_optional_questions":len(known_v3),
        "source_pinned_behavioral_question_reuses":[
          {"question_id":key,
           "source_bank":"V3_CANDIDATE" if key in known_v3 else "TENDENCY_FIRST",
           "source_claim_ids":sorted(reused_question_to_claims[key]),
           "actual_existing_question_modified":False}
          for key in sorted(reused_question_to_claims)
        ],
        "single_shared_answer_facets":[
          {"facet_id":key, "claim_ids_reusing_same_facet":sorted(shared_facet_to_claims[key]),
           "counts_as_independent_duplicate_responses":False}
          for key in sorted(shared_facet_to_claims)
        ],
        "future_conditional_probe_ids":[v["id"] for v in optional],
        "conditional_probes_added_to_existing_live_app":False,
        "final_survey_questionnaire_source_frozen":False,
        "source_predictions_all_separately_unfrozen":True,
        "real_participant_records_read_or_emitted":0,
        "real_human_natal_results":0,
        "scoring_or_runtime_changes":0
    }

if __name__=="__main__":
    output=compile_bridge()
    dest=ROOT/OUTPUT
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(dest.name,output["separate_unscored_claims"],
          len(output["source_pinned_behavioral_question_reuses"]),
          len(output["single_shared_answer_facets"]))
