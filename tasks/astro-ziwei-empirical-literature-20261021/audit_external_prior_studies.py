#!/usr/bin/env python3
"""Fail-closed, ABSTRACT-ONLY prior-literature evidence gates; not human predictions."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = HERE / "EXTERNAL_ASTROLOGY_EMPIRICAL_EVIDENCE_REGISTRY_V1.json"
QUEUE = HERE / "FULL_TEXT_EXTRACTION_AND_REPLICATION_GATES_V1.json"
REVIEW = HERE / "RESEARCH_REVIEW_AND_DESIGN_CONSEQUENCES_20261021.md"
RECEIPT = HERE / "EMPIRICAL_PRIOR_LITERATURE_VERIFICATION_RECEIPT_20261021.json"
IDS = {
    "ZWDS-2018-TEO",
    "ZWDS-2020-CHEN",
    "WESTERN-1984-TYSON",
    "WESTERN-1985-CARLSON",
    "WESTERN-1992-FUZEAU",
    "WESTERN-1996-ERTEL-DEAN",
    "WESTERN-1996-FUZEAU-REPLY",
}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def reject(reason: str) -> None:
    raise ValueError("Prior empirical evidence audit rejected: " + reason)


def evaluate(reg: dict, queue: dict) -> dict:
    if reg.get("schema") != "HUMANDESIGN_INDEPENDENT_PREEXISTING_ASTROLOGY_HUMAN_STUDY_EVIDENCE_V1":
        reject("unexpected source registry schema")
    if reg.get("status") != "PRIMARY_METADATA_AND_ABSTRACT_RESEARCH_AUDIT_NOT_A_SYSTEMATIC_REVIEW":
        reject("abstract scan improperly described as systematic full-text review")
    if reg.get("root_project_persons_tested_in_independent_prospective_blind_astrology_study") != 0:
        reject("external thesis participants counted as project predictions")
    if reg.get("no_external_thesis_full_text_claimed_as_read") is not True:
        reject("unread full texts were falsely marked examined")
    studies = reg.get("external_human_studies", [])
    study = {x["study_id"]: x for x in studies}
    if len(studies) != 7 or set(study) != IDS:
        reject("missing or duplicated primary positive/negative/critique evidence")
    for item in studies:
        if not item.get("link", "").startswith("https://"):
            reject("primary metadata citation URL absent")
        if "ABSTRACT" not in item.get("source_observed_level", ""):
            reject("original full study access misrepresented")
        if item.get("prospective_out_of_sample_chart_prediction_demonstrated") is not False:
            reject("abstract reports falsely called independent prospective accuracy")
        if item.get("exact_p_values_available") not in (False, None):
            reject("original numerical p values not read")
        if item["tradition"] != "Zi Wei Dou Shu" and not item.get(
            "tradition_transferability_to_ZiWei"
        ):
            reject("Western studies mistaken as direct Chinese replication")
    a = study["ZWDS-2018-TEO"]
    if not (
        a["sample_n_reported"] == 243
        and a["astrology_analyst_n"] == 3
        and a["reported_question_items_given_to_astrologers"] == 7
        and a["overall_group_result_reported_null"] is True
        and a["positive_subgroup_finding_reported"] is True
        and a["effect_size_numeric_available"] is False
        and a["multiple_testing_adjustment_checked"] is False
    ):
        reject("2018 null plus subgroup exceptions/source uncertainties altered")
    b = study["ZWDS-2020-CHEN"]
    if not (
        b["sample_n_reported"] is None
        and b["positive_group_finding_reported"] is True
        and b["numeric_group_smoking_rates_verified"] is False
        and b["effect_size_numeric_available"] is False
        and b["cites_2018_ZWDS_TEO_thesis"] is True
        and b["covariate_age_sex_cohort_education_income_confounding_checked"] is False
    ):
        reject("2020 smoking association or unverified N/covariates misrepresented")
    sources = reg.get("source_access_audit", {})
    csmu = sources.get("CSMU_2018", {})
    tku = sources.get("TKU_2020", {})
    if not (
        csmu.get("institutional_access_control_seen") == "Request a copy"
        and csmu.get("full_original_thesis_file_downloaded") is False
        and tku.get("full_original_thesis_file_downloaded") is False
        and tku.get("full_numeric_tables_checked") is False
        and tku.get("download_button_observed_requires_institutional_proxy_authentication") is True
        and "ezproxy" in tku.get("tested_download_button_redirect_target", "")
    ):
        reject("thesis full-text access blocker or verification status erased")
    twins = study["WESTERN-1992-FUZEAU"]
    critique = study["WESTERN-1996-ERTEL-DEAN"]
    reply = study["WESTERN-1996-FUZEAU-REPLY"]
    if not (
        twins["responding_twin_pairs_reported"] == 238
        and twins["original_author_reported_replies"]
        == {"exact": 153, "reverse": 65, "no_difference": 20}
        and critique["critique_of_study"] == twins["study_id"]
        and critique["critique_not_uncontested"] is True
        and reply["response_to_study"] == critique["study_id"]
        and reply["claim_that_future_replication_actually_occurred"] is False
    ):
        reject("original twin claim, published reanalysis or author response omitted")
    carlson = study["WESTERN-1985-CARLSON"]
    if (
        carlson["outcome_direction"] != "NOT_VERIFIED_FROM_SHORT_PUBLISHER_ABSTRACT"
        or carlson["original_results_quantitatively_extracted"] is not False
    ):
        reject("Carlson publisher metadata mistaken for full results")
    synthesis = reg.get("cross_study_synthesis", {})
    if not (
        synthesis.get("ZiWei_direct_studies_verified_in_registry") == 2
        and synthesis.get("meta_analysis_on_comparable_ZiWei_estimands_possible_now") is False
        and synthesis.get(
            "causal_inference_or_preregistered_predictive_accuracy_from_theses_demonstrated"
        )
        is False
        and synthesis.get("external_original_author_claims_include_null_and_positive_reports")
        is True
    ):
        reject("incomparable prior Zi Wei results falsely pooled")
    request = queue.get("primary_missing_sources", [])
    if (
        len(request) != 2
        or {x["study_id"] for x in request} != {"ZWDS-2018-TEO", "ZWDS-2020-CHEN"}
        or any(x["full_text_available_to_current_research"] is not False for x in request)
        or any(x["full_text_methodology_verified"] is not False for x in request)
    ):
        reject("missing full-text acquisition unresolved gates erased")
    future = queue.get("pre_registration_only_after_missing_method_inputs", {})
    if not (
        future.get("human_study_frozen_and_authorized") is False
        and future.get("project_real_human_predictive_trials_completed") == 0
        and future.get(
            "do_not_choose_between_TEO_personality_and_CHEN_smoking_after_looking_at_any_new_answers"
        )
        is True
        and len(future.get("required_controls", [])) >= 5
    ):
        reject("unfrozen outcome/blind study falsely authorized")
    return {
        "source_status": "ORIGINAL_METADATA_AND_ABSTRACT_ONLY",
        "external_studies_screened": 7,
        "direct_ZiWei_studies": 2,
        "original_full_theses_read": 0,
        "2018_sample_N": 243,
        "2018_experienced_astrologers": 3,
        "2018_null_with_friendliness_subgroup_exceptions": True,
        "2020_author_reported_smoking_category_signal": True,
        "2020_numeric_coefficient_or_N_verified": False,
        "1992_twin_positive_and_1996_critique_and_author_response_kept": True,
        "HumanDesign_human_predictive_trials": 0,
        "actual_human_study_frozen": False,
    }


def emit_receipt() -> dict:
    result = evaluate(read(REG), read(QUEUE))
    if not REVIEW.is_file() or REVIEW.stat().st_size < 3000:
        reject("full source criticism/research-next-actions document missing")
    receipt = {
        "schema": "HUMANDESIGN_EXTERNAL_ASTROLOGY_EMPIRICAL_ABSTRACT_GATE_V1",
        "status": "VERIFIED_SOURCE_METADATA_ONLY_NOT_HUMAN_ACCURACY",
        "evidence": result,
        "source_registry_SHA256": hash_file(REG),
        "full_thesis_access_queue_SHA256": hash_file(QUEUE),
        "methods_review_SHA256": hash_file(REVIEW),
        "full_texts_authentically_obtained": False,
        "human_astrology_predictive_trials_completed_by_project": 0,
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    print(json.dumps(emit_receipt(), indent=2, ensure_ascii=False))
