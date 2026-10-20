#!/usr/bin/env python3
"""Fail-closed astrology pilot readiness and original source provenance audit.

No personal participant inputs, no claimed ability to run astrology human
forecasts before model/chart/instrument/consent freeze. Pure offline checks.
"""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = HERE / "READINESS_GATES_V1.json"
SCHEMA = "HUMANDESIGN_ASTROLOGY_BLIND_TEST_READINESS_V1"
ALLOWED_SOURCE_STATUS = {
    "source_text_verified",
    "mechanical_synthetic",
    "limited_engine_partial",
    "unresolved",
    "owner_gate",
    "prospective_validation",
}
ALLOWED_GATE_STATUS = {"unresolved", "owner_gate", "verified"}
EXPECTED_GATE_IDS = {
    "G01_bounded_birth_population",
    "G02_single_named_model_and_rule_version",
    "G03_birth_chart_withheld_and_reproducible",
    "G04_questionnaire_mapping_freeze",
    "G05_calibrated_prediction_and_predeclared_score",
    "G06_decoy_and_nonastrological_controls",
    "G07_data_protection_and_participant_consent",
    "G08_immutable_pre_response_package",
    "G09_untouched_cohort_and_power_plan",
    "G10_permutation_null_and_negative_disclosure",
}

def load(path: Path = MATRIX) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def fail(reason: str) -> None:
    raise ValueError("Readiness audit rejected: " + reason)

def validate(data: dict[str, Any], repo: Path = ROOT) -> dict[str, Any]:
    if data.get("schema") != SCHEMA:
        fail("unrecognized schema/version")
    if data.get("status") != "PROTOCOL_REVIEW_ONLY_NOT_PREREGISTERED_OR_RECRUITING":
        fail("cannot present unregistered draft as a registered protocol")
    source = data.get("source_provenance", {})
    if (source.get("chinese_bazi_source_annotations"),
        source.get("chinese_ziwei_source_annotations"),
        source.get("western_lilly_source_annotations_in_other_branch"),
        source.get("western_ptolemy_source_annotations_in_other_branch")) != (
        210, 586, 13236, 1066
    ):
        fail("documentary source annotation counts altered or confused across branches")
    if sum((
        source["chinese_bazi_source_annotations"],
        source["chinese_ziwei_source_annotations"],
        source["western_lilly_source_annotations_in_other_branch"],
        source["western_ptolemy_source_annotations_in_other_branch"],
    )) != source.get("cross_branch_historical_documentary_total_not_empirical_results", -1):
        fail("cross-branch source count not consistent")
    if source.get("cross_branch_registry_integrated") is not False or (
        source.get("western_current_parent_snapshot_is_older_B07bc") is not True
    ):
        fail("distinct West/Chinese original source histories must not be implicitly merged")
    local_index = repo / source.get("chinese_accepted_index", "")
    if not local_index.is_file() or (
        sha256(local_index.read_bytes()).hexdigest()
        != source.get("chinese_accepted_index_sha256")
    ):
        fail("accepted Chinese historical source index SHA not verified locally")
    local_json = json.loads(local_index.read_text(encoding="utf-8"))
    if (
        local_json.get("sum_source_annotations") != 796
        or [x["accepted_source_annotations"] for x in local_json.get("systems", [])]
        != [210,586]
        or local_json.get("independently_validated_real_human_claims") != 0
    ):
        fail("source index not pinned exact current source without human claims")
    for k in (
        "independent_real_human_predictive_validations",
        "real_human_participant_birth_records_in_this_artifact",
        "participant_scored_responses_in_this_artifact",
        "astrology_production_rules_promoted",
    ):
        if source.get(k) != 0:
            fail("audit draft improperly contains real people or predictive validation")
    evidence = data.get("source_and_engine_evidence", [])
    if not evidence or len({x.get("id") for x in evidence}) != len(evidence):
        fail("evidence source identities absent or duplicated")
    for item in evidence:
        if item.get("status") not in ALLOWED_SOURCE_STATUS:
            fail("evidence status outside allowed categories")
        if "evidence_local" in item:
            filepath = repo / item["evidence_local"]
            if not filepath.is_file() or not filepath.is_relative_to(repo):
                fail("source evidence local path unavailable")
        if item.get("id") == "empirical_human_results" and (
            item.get("independent_human_tests") != 0
            or item.get("results_available_for_accuracy_claim") is not False
        ):
            fail("unsupported real-human empirical success asserted")
    gates = data.get("candidate_pilot_gates", [])
    ids = [gate.get("id") for gate in gates]
    if set(ids) != EXPECTED_GATE_IDS or len(ids) != len(EXPECTED_GATE_IDS):
        fail("pilot readiness gates missing or duplicated")
    if any(gate.get("status") not in ALLOWED_GATE_STATUS for gate in gates):
        fail("gate contains unrecognized status")
    for gate in gates:
        if gate.get("blocking") is not True:
            fail("a scientific gate silently marked nonblocking")
        if gate["status"] == "verified":
            if not gate.get("independent_verification_receipt_sha256"):
                fail("cannot mark a gate verified without independent pinned receipt")
        elif gate.get("independent_verification_receipt_sha256"):
            fail("a nonverified gate has an inconsistent validation receipt")
    eligibility = data.get("pilot_eligibility", {})
    required_false = (
        "this_version_is_a_preregistration",
        "scored_human_recruitment_authorized",
        "scored_human_questionnaire_authorized",
        "full_traditional_western_and_chinese_model_ready",
        "full_human_prospective_or_reverse_model_validated",
    )
    if any(eligibility.get(x) is not False for x in required_false):
        fail("unregistered incomplete astrology model falsely readied")
    is_ready = all(g["status"] == "verified" for g in gates)
    if eligibility.get("candidate_pilot_ready") is not is_ready:
        fail("candidate ready field inconsistent with immutable blocked gates")
    safe_historical = (
        "historical_gender_disease_longevity_and_moral_claims_"
        "excluded_from_medicine_and_human_stereotyping"
    )
    if eligibility.get(safe_historical) is not True:
        fail("no historical pseudo-clinical or discriminatory outcome model")
    if eligibility.get("development_only_synthetic_chart_tests_may_continue") is not True:
        fail("synthetic calculation checks must remain independent from scored human study")
    if (
        eligibility.get("already_inspected_owner_Hale_ineligible_as_untouched_final_test")
        is not True
    ):
        fail("known/exploratory profiles cannot be reused as untouched validation people")
    if data.get("not_done") is None or len(data["not_done"]) < 5:
        fail("missing known incompleteness and uncertainty disclosures")
    return {
        "status": "READY_FOR_RECRUITMENT" if is_ready else "NOT_READY_SOURCE_AND_ENGINEERING_ONLY",
        "gate_count": len(gates),
        "blocking_gate_ids": [g["id"] for g in gates if g["status"] != "verified"],
        "historical_documentary_annotations_across_distinct_branches": source[
            "cross_branch_historical_documentary_total_not_empirical_results"
        ],
        "real_human_predictive_validations": 0,
        "astrology_runtime_promotions": 0,
        "has_public_private_participant_records": False,
    }

if __name__ == "__main__":
    print(json.dumps(validate(load()), indent=2, ensure_ascii=False))
