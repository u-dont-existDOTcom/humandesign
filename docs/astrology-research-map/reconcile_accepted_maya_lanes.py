#!/usr/bin/env python3
"""Reconcile four accepted Maya research lanes without promoting chart/person claims.

This reads accepted sibling evidence copied byte-for-byte into the isolated
integration branch and emits a V2 descriptive coverage map and exact provenance
ledger. The existing canonical three Mermaid maps are reused, not duplicated.
"""
from pathlib import Path
from hashlib import sha256
import copy,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
COVER=HERE/"TRADITION_COVERAGE_V1.json"
MAYA_CATALOG=HERE/"MAYA_SOURCE_CATALOG_V1.json"
DAYKEEPER=HERE/"MAYA_FIRST_SOURCE_WITNESS_V1.json"
CLAIM=HERE/"CLAIM_TRACE_EXAMPLE_MAYA_E_V1.json"
INTAKE=ROOT/"tasks/astro-maya-comparative-map-20261022/MAYA_LOCAL_SOURCE_INVENTORY_V1.json"
INTAKE_REVIEW=ROOT/"tasks/astro-maya-comparative-map-20261022/MAYA_SOURCE_FIRST_READING_AND_PARALLEL_MAP_ALIGNMENT_20261022.md"
MULTI=ROOT/"tasks/astro-multitradition-source-coverage-20261022/TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json"
MULTI_BOOKS=ROOT/"tasks/astro-multitradition-source-coverage-20261022/MAYA_BOOKS_OTHER_SYSTEMS_AND_METHOD_20261022.md"
MULTI_MAYA=ROOT/"tasks/astro-multitradition-source-coverage-20261022/MAYA_RANKED_SOURCE_REGISTER_V1.json"
MULTI_OTHER=ROOT/"tasks/astro-multitradition-source-coverage-20261022/ADDITIONAL_TRADITIONS_PRIORITY_REGISTER_V1.json"
DRESDEN=ROOT/"tasks/astro-maya-dresden-facsimile-page24-20261022/DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json"
DRESDEN_DELTA=ROOT/"tasks/astro-maya-dresden-facsimile-page24-20261022/MAYA_SOURCE_TO_TEST_MAP_DELTA_V2.json"
DRESDEN_REVIEW=ROOT/"tasks/astro-maya-dresden-facsimile-page24-20261022/DRESDEN_FOLIOS24_46_SOURCE_CRITICAL_REVIEW_20261022.md"
OUT=HERE/"TRADITION_COVERAGE_RECONCILED_V2.json"
LEDGER=HERE/"RECONCILED_SOURCE_TO_TEST_EVIDENCE_V1.json"
PARENTS={
 "mesoamerica_source_map":"f3afeab41671ddf75978a3901f6f38d5620747a3",
 "independent_maya_books_crosswalk":"7b6b904266c69fa43fb0f5bffe1bdc4af16c984a",
 "owner_held_book_intake":"5ef97bd9a1cc684556f5da99fe5aa2ce27d23764",
 "dresden_folio_visual_reader":"a2c8a2ee1fb1897a9edaf145db88649af825d215",
}
ALL_PROVENANCE=(COVER,MAYA_CATALOG,DAYKEEPER,CLAIM,INTAKE,INTAKE_REVIEW,
                MULTI,MULTI_BOOKS,MULTI_MAYA,MULTI_OTHER,DRESDEN,DRESDEN_DELTA,DRESDEN_REVIEW)

def data(path):
 return json.loads(path.read_text(encoding="utf-8"))
def digest(path):
 return sha256(path.read_bytes()).hexdigest()
def save(path,obj):
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def build():
 base=data(COVER);book=data(INTAKE);cw=data(MULTI);native=data(DAYKEEPER)
 folios=data(DRESDEN);folio_changes=data(DRESDEN_DELTA)
 fields=base["traditional_systems"]
 assert len(fields)==16 and len({r["id"] for r in fields})==16
 assert len(base["documented_cross_source_links_not_confirmation"])==11
 assert len(cw["crosswalk"])==20
 assert len(cw["existing_Human_Design_domain_ids"])==6
 assert len([x for x in cw["crosswalk"] if x["id"].startswith("HD-EXISTING-")])==6
 assert cw["cross_tradition_hypotheses_active_in_runtime"]==0
 assert cw["validated_human_blind_predictions"]==0
 assert book["total_input_files"]==5 and book["research_sources_usable_for_next_reading"]==4
 assert book["fiction_omitted_from_original_sources"]==1
 assert book["books_fully_read_or_complete"]==0 and book["real_human_blinded_predictive_validations"]==0
 assert len(native["day_name_crosswalk_only"])==20
 assert len(native["observed_primary_claims_development_only"])==7
 assert native["real_human_blind_validations"]==0 and native["astrology_model_promotions"]==0
 assert len(folios["source_witnesses"])==2
 assert folios["independently_transcribed_Maya_hieroglyph_signs"]==0
 assert folios["independent_real_human_blind_predictions"]==0
 assert folio_changes["old_to_new_state"]["Maya_personal_phenotype_questionnaire_approved"] is False
 assert folio_changes["old_to_new_state"]["original_source_glyph_values_and_correlations_pinned"] is False
 assert folio_changes["old_to_new_state"]["birth_timing_or_local_calendar_birth_engine_independently_verified"] is False
 assert len(data(MULTI_MAYA)["source_records"])==15
 # Per-source physical/source availability claims are constrained to owner verified notes.
 sources={p.relative_to(ROOT).as_posix():{
  "sha256":digest(p),"bytes":p.stat().st_size,
  "evidence_layer":"SOURCE_OR_METHOD_DOCUMENTATION_NOT_HUMAN_SUCCESS"
 } for p in ALL_PROVENANCE}
 revised=copy.deepcopy(base)
 revised.update({
  "schema":"HUMANDESIGN_CROSS_TRADITION_COVERAGE_RECONCILED_V2",
  "date_utc":"2026-10-22",
  "status":"ACCEPTED_SIBLING_SOURCE_STATES_RECONCILED_IN_ISOLATED_BRANCH_NOT_RUNTIME",
  "prior_inventory_sha256":digest(COVER),
  "prior_inventory":"TRADITION_COVERAGE_V1.json",
  "source_lane_git_heads":PARENTS,
  "subject_level_inference_and_human_validation":"OPEN_UNTESTED"
 })
 updated={x["id"]:x for x in revised["traditional_systems"]}
 assert all(key in updated for key in ("MAYA-LIVING","MAYA-CODEX","NEWAGE-DREAMSPELL"))
 updated["MAYA-LIVING"]["state"]="Practitioner testimony original 3-page read; 20 day names plus 7 UNFROZEN source-only personal-day claims; Tedlock owned and excerpt-sampled; living K'iche' epoch and any calibrated real human prediction unresolved"
 updated["MAYA-LIVING"]["accepted_evidence"]={
  "practitioner_original_reference":"MAYA_FIRST_SOURCE_WITNESS_V1.json",
  "local_owner_Tedlock_source":"tasks/astro-maya-comparative-map-20261022/MAYA_LOCAL_SOURCE_INVENTORY_V1.json",
  "named_day_correspondences_only":20,
  "candidate_source_phenotype_claims_not_frozen":7,
  "Kiche_living_daycount_epoch_independently_verified":False,
  "personality_claims_in_runtime":0
 }
 updated["MAYA-CODEX"]["state"]="Two exact Dresden Codex 1892 Förstemann photo-facsimile folios (p24 and p46) visually inspected and byte/source SHA-pinned; original surviving SLUB physical codex and glyph decoding NOT independently read"
 updated["MAYA-CODEX"]["accepted_evidence"]={
  "source_visual_witness":"tasks/astro-maya-dresden-facsimile-page24-20261022/DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json",
  "historical_folio_pages_visualized":["Dresden 24","Dresden 46"],
  "visualized_facsimile_folio_count":2,
  "historical_original_glyph_values_independently_deciphered":0,
  "original_surviving_codex_pages_authenticated_against_facsimiles":False,
  "derived_person_specific_Maya_natal_predictions":0
 }
 updated["NEWAGE-DREAMSPELL"]["accepted_evidence"]={
  "state":"QUARANTINE_RECENT_MODERN_INVENTION_NOT_ANCIENT_MAYA_AUTHORITY",
  "ancient_Maya_original_rule_attributions":0,
  "scientific_human_validations":0
 }
 revised["current_claim_class_crosswalk"]={
  "source":"tasks/astro-multitradition-source-coverage-20261022/TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json",
  "existing_HumanDesign_survey_domains":6,
  "non_HD_candidate_only_categories":14,
  "cross_tradition_scored_claims_promoted":0,
  "source_claims_that_can_be_scored_in_confirmatory_Maya_humans_now":0,
 }
 revised["owner_maya_book_inventory"]={
  "source":"tasks/astro-maya-comparative-map-20261022/MAYA_LOCAL_SOURCE_INVENTORY_V1.json",
  "on_owner_machine_usable_research_books":4,
  "on_owner_machine_excluded_fiction_books":1,
  "fully_read_books":0,
  "Bricker_Astronomy_in_the_Maya_Codices_verified_owned":False
 }
 revised["historical_original_source_promotion"]={
  "merged_into_default_HD_model":False,
  "Maya_independently_calculated_natal_engine_verified":False,
  "Maya_original_person_trait_prediction_frozen":False,
  "untouched_real_human_forward_or_reverse_blind_results":0
 }
 revised["reconciled_source_files_sha256_and_bytes"]=sources
 assert revised["traditional_systems"][:9]==base["traditional_systems"][:9]
 assert revised["project_empirical_state"]["real_human_blind_pred_successes"]==0
 evidence={
  "schema":"ASTROLOGY_CROSS_LANE_SOURCE_ENGINE_QUESTION_HUMAN_RECONCILIATION_V1",
  "status":"SOURCE_ONLY_DESCRIPTIVE_INTEGRATION_NO_MODEL_PROMOTION",
  "source_lane_git_heads":PARENTS,
  "source_files_sha256_and_bytes":sources,
  "one_canonical_living_overview_diagram":"docs/astrology-research-map/WORKFLOW.mmd",
  "evaluation_gates_diagram":"docs/astrology-research-map/SOURCE_TO_TEST_GATES.mmd",
  "historical_dependency_map":"docs/astrology-research-map/TRADITION_DEPENDENCIES.mmd",
  "other_parallel_Mermaid_diagrams_copied_into_canonical_tree":False,
  "owner_available_usable_nonfiction_Maya_books":4,
  "owner_excluded_fiction":1,
  "owned_book_completely_read_count":0,
  "source_Maya_Dresden_original_1892_photo_facsimile_foils_inspected":2,
  "genuine_authentic_surviving_Maya_codex_glyphs_independently_deciphered":0,
  "Maya_tradition_region_layers":["Precontact_Lowland_codex_ritual_astronomy",
      "Colonial_Chilam_Balam_syncretic_text",
      "Living_Kiche_Chol_Qij_daykeeping",
      "Modern_Dreamspell_not_ancient_primary"],
  "living_Kiche_source_read_total_daynames":20,
  "living_Kiche_source_person_claims_held_as_exploratory":7,
  "Maya_lowland_calendar_GMT_correlation_choices":[584283,584285],
  "independent_Kiche_daycount_anchor_verified":False,
  "source_claim_crosswalk_existing_HD_domains":6,
  "source_claim_crosswalk_non_HD_candidate_only":14,
  "cross_tradition_runtime_chart_claims_scored":0,
  "uncertainty_states":["SOURCE_ONLY","CALENDAR_VARIANT_UNRESOLVED",
     "MAPPING_UNFROZEN","CONTEXTUAL_RITUAL_NOT_NATAL",
     "SYNTHETIC_ENGINEERING_ONLY","ABSTAIN","HUMAN_BLIND_UNTESTED"],
  "next_required_for_Maya_person_claim":["source_interpretation_regional_original_locus",
    "date_to_correct_regional_traditional_day_after_epoch_and_day_boundary",
    "calibrated_concealed_question_positive_opposite_base_rate",
    "freeze_rule_decoys_chart_and_prediction_before_untouched_humans"],
  "actual_independently_blinded_human_predictive_validations":0,
  "astrology_rule_promotions":0,
  "main_runtime_changes":False
 }
 save(OUT,revised)
 save(LEDGER,evidence)
 return {"traditions":len(revised["traditional_systems"]),
         "source_witnesses":len(sources),
         "Maya_person_claims_held":7,
         "owner_books_nonfiction":4,
         "original_1892_facsimile_folios":2,
         "human_predictive_validations":0,
         "coverage_sha256":digest(OUT),"ledger_sha256":digest(LEDGER)}

if __name__=="__main__":
 print(json.dumps(build(),ensure_ascii=False,indent=2))
