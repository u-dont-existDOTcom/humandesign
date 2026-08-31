from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from hdmatch.natal_time.preinference_validation import (
    ContaminationEvent,
    DataRole,
    ReferenceAccessEvent,
    ReferenceActor,
    ReferencePurpose,
    RoleAssignment,
    reference_access_violations,
    validate_synthetic_case,
)
from hdmatch.util import sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
CONTRACT_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"


def _contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for nested in value.values() for key in _all_keys(nested)}
    if isinstance(value, list):
        return {key for nested in value for key in _all_keys(nested)}
    return set()


def test_contract_is_canonical_self_hashed_and_synthetic_only() -> None:
    contract = _contract()

    assert contract["schema_version"] == "natal-time-preinference-design-contract-v1"
    assert contract["authorization"] == {
        "checkpoint": "docs/PRO_SUPERVISION_CHECKPOINT_3_20260830.md",
        "authorized_slice": (
            "pre-inference study-design, falsification, and disclosure contract only"
        ),
        "local_commits_only": True,
        "participant_inference_authorized": False,
        "synthetic_only": True,
    }
    canonicalization = contract["canonicalization"]
    assert canonicalization["algorithm"] == "sha256"
    assert canonicalization["implementation"] == "hdmatch.util.sha256_json"
    assert "contract_sha256" in canonicalization["hash_scope"]

    unhashed = deepcopy(contract)
    expected = unhashed.pop("contract_sha256")
    assert expected == sha256_json(unhashed)


def test_formal_objects_preserve_complete_candidates_hidden_reference_and_set_output() -> None:
    objects = _contract()["formal_objects"]

    assert set(objects) == {"C_i", "T_i", "S_i"}
    assert objects["C_i"]["ordering_semantics"] == "none"
    assert "complete unordered set" in objects["C_i"]["definition"]
    assert "before any inferential response" in objects["C_i"]["freeze_rule"]
    assert "T_i is unavailable" in objects["C_i"]["reference_independence"]
    assert "any source class accepted" in objects["C_i"]["candidate_evidence_rule"]
    assert "isolated" in objects["C_i"]["candidate_evidence_rule"]

    assert "independently sourced documentary" in objects["T_i"]["definition"]
    assert objects["T_i"]["point_promotion_prohibited"] is True
    assert "ineligible for calibration or validation" in objects["T_i"]["absence_rule"]
    assert "previously committed S_i" in objects["T_i"]["evaluation_rule"]

    assert "subset of C_i" in objects["S_i"]["definition"]
    assert "unchanged member of the frozen C_i" in objects["S_i"]["subset_rule"]
    assert "neither success nor error" in objects["S_i"]["abstention_rule"]
    assert "a single best minute" in objects["S_i"]["prohibited_forms"]


def test_estimand_keeps_coverage_width_state_count_date_and_abstention_separate() -> None:
    estimand = _contract()["non_scalar_estimand"]
    components = estimand["participant_level_components"]

    assert estimand["primary_target"] == (
        "joint coverage-temporal-width-state-count-abstention frontier"
    )
    assert set(components) == {
        "reference_intersection",
        "temporal_width_retained",
        "full_state_interval_count_retained",
        "abstention",
        "date_coverage",
    }
    assert components["temporal_width_retained"]["separate_from_state_count"] is True
    assert components["full_state_interval_count_retained"]["separate_from_temporal_width"] is True
    assert "not_applicable_due_to_abstention" in components["reference_intersection"]["values"]
    assert "neither success nor error" in components["abstention"]["definition"].lower()
    assert "more than one civil date" in components["date_coverage"]["applies_when"]
    assert "Do not combine" in estimand["aggregation_rule"]
    assert set(estimand["not_selected"]) == {
        "operating threshold",
        "coverage target",
        "temporal-width target",
        "state-count target",
        "abstention threshold",
        "preferred frontier point",
    }


def test_documentary_reference_eligibility_preserves_coarse_precision() -> None:
    reference = _contract()["reference_standard"]
    requirements = reference["eligibility_requirements"]
    ineligible = reference["ineligible_as_accuracy_ground_truth"]
    precision = reference["precision_rules"]

    assert len(requirements) == 5
    assert any("documentary rather than memory-only" in rule for rule in requirements)
    assert any("independently" in rule for rule in requirements)
    assert "memory-only time or date" in ineligible
    assert any("rectification" in source for source in ineligible)
    assert "never promote" in precision["general"]
    assert "all source-compatible interpretations" in precision["unknown_rounding_convention"]
    assert precision["examples_of_coarse_precision"] == [
        "five-minute precision remains a five-minute-scale reference interval",
        "fifteen-minute precision remains a fifteen-minute-scale reference interval",
        "hour precision remains an hour-scale reference interval",
    ]
    assert "never define T_i" in precision["memory_only"]
    assert "invalid for calibration or validation" in reference["leakage_invalidation_rule"]
    assert "independent calibration evaluator" in reference[
        "authorized_calibration_comparison_rule"
    ]
    assert "methodological revision" in reference["authorized_calibration_comparison_rule"]


def test_baseline_falsification_matrix_is_complete_and_keeps_random_controls_distinct() -> None:
    contract = _contract()
    rows = contract["baseline_falsification_matrix"]
    by_id = {row["id"]: row for row in rows}

    assert len(by_id) == len(rows)
    assert set(by_id) == {
        "complete-unordered-candidate-set",
        "no-pruning-after-responses",
        "random-subset-temporal-width-matched",
        "random-subset-state-count-matched",
        "calendar-only",
        "season-only",
        "birthplace-only",
        "timezone-only",
        "cohort-only",
        "source-quality-only",
        "response-style-only",
        "participant-chart-label-permutation",
        "plausible-mismatched-chart",
        "blinded-matching",
        "strongest-ordinary-non-hd",
    }
    assert (
        "without matching on state count"
        in by_id["random-subset-temporal-width-matched"]["definition"]
    )
    assert (
        "without matching on temporal width"
        in by_id["random-subset-state-count-matched"]["definition"]
    )
    assert (
        "not a probability model"
        in by_id["random-subset-temporal-width-matched"]["falsification_role"]
    )
    assert (
        "not a probability model"
        in by_id["random-subset-state-count-matched"]["falsification_role"]
    )
    assert "beating random assignment alone is insufficient" in contract["baseline_claim_rule"]


def test_roles_withhold_raw_reference_and_fail_closed_after_contamination() -> None:
    contract = _contract()
    roles = contract["data_roles"]
    access = contract["actor_access_matrix"]

    assert roles["assignment_unit"] == "connected_component"
    assert roles["development"]["raw_T_i_access"] is False
    assert roles["calibration"]["raw_T_i_access"] is False
    assert roles["locked_validation"]["raw_T_i_access"] is False
    assert "fresh unexposed calibration cohort" in roles["calibration"]["contamination_rule"]
    assert "new untouched validation cohort" in roles["locked_validation"]["contamination_rule"]
    assert set(roles["development"]["adaptive_choices"]) == {
        "concepts and wording",
        "features and coding",
        "missingness handling",
        "model family",
        "priors",
        "hyperparameters",
        "operating and abstention rules",
        "baselines",
        "subgroup definitions",
        "outcome transformations",
    }

    assert access["candidate_constructor"]["raw_T_i"] is False
    assert access["measurement_developer"]["raw_T_i"] is False
    assert access["inference_procedure"]["raw_T_i"] is False
    assert access["reference_custodian"]["raw_T_i"] is True
    assert access["independent_calibration_evaluator"]["raw_T_i"] is True
    assert access["independent_validation_evaluator"]["raw_T_i"] is True
    assert access["reference_custodian"]["committed_S_i"] is False
    assert access["independent_calibration_evaluator"]["committed_S_i"] is True
    assert access["independent_validation_evaluator"]["committed_S_i"] is True
    assert "method and output frozen" in access["independent_calibration_evaluator"][
        "access_condition"
    ]


def test_connected_component_rules_cover_identity_relationship_household_and_source() -> None:
    split = _contract()["connected_component_split"]

    assert "undirected graph" in split["graph_definition"]
    assert "Assign entire connected components" in split["graph_definition"]
    assert set(split["edge_classes"]) == {
        "same participant or repeated identity under any alias",
        "partners or members of the same relationship pair",
        "members of the same household",
        "participants connected through any relationship chain",
        "participants linked to the same label-transmitting record source or record custodian",
    }
    assert "may cross" in split["cross_role_rule"]
    assert set(split["freeze_evidence"]) == {
        "pseudonymous vertex manifest digest",
        "edge manifest digest with reason codes",
        "connected-component assignment digest",
        "data-role manifest digest",
    }
    assert "permanently disqualifies" in split["relationship_rule"]


def _assignments(case: dict[str, Any]) -> tuple[RoleAssignment, ...]:
    return tuple(
        RoleAssignment(
            observation_id=item["observation_id"],
            participant_id=item["participant_id"],
            role=DataRole(item["role"]),
            alias_keys=tuple(item["alias_keys"]),
            household_keys=tuple(item["household_keys"]),
            relationship_keys=tuple(item["relationship_keys"]),
            shared_record_source_keys=tuple(item["shared_record_source_keys"]),
        )
        for item in case["assignments"]
    )


def _reference_events(case: dict[str, Any]) -> tuple[ReferenceAccessEvent, ...]:
    return tuple(
        ReferenceAccessEvent(
            participant_id=item["participant_id"],
            actor=ReferenceActor(item["actor"]),
            purpose=ReferencePurpose(item["purpose"]),
            method_frozen=item["method_frozen"],
            output_frozen=item["output_frozen"],
        )
        for item in case["reference_access_events"]
    )


def _contamination_events(case: dict[str, Any]) -> tuple[ContaminationEvent, ...]:
    return tuple(
        ContaminationEvent(
            role=DataRole(item["role"]),
            methodology_changed_after_outcome_access=item[
                "methodology_changed_after_outcome_access"
            ],
            relationship_evidence_used_for_natal_inference=item[
                "relationship_evidence_used_for_natal_inference"
            ],
        )
        for item in case["contamination_events"]
    )


def test_structured_synthetic_leakage_cases_execute_the_validator() -> None:
    cases = _contract()["synthetic_leakage_cases"]
    by_id = {case["id"]: case for case in cases}

    assert len(by_id) == len(cases)
    assert set(by_id) == {
        "clean-disjoint-components",
        "same-participant-cross-role",
        "alias-cross-role",
        "partners-cross-role",
        "household-cross-role",
        "relationship-chain-cross-role",
        "shared-record-source-cross-role",
        "reference-enters-candidate-construction",
        "reference-enters-measurement-development",
        "reference-enters-fitting",
        "reference-enters-stopping",
        "calibration-becomes-adaptive",
        "validation-peek-changes-method",
        "relationship-evidence-assisted-inference",
    }
    for case in cases:
        violations = validate_synthetic_case(
            _assignments(case),
            _reference_events(case),
            _contamination_events(case),
        )
        assert list(violations) == case["expected_violation_codes"], case["id"]
        assert (not violations) is case["expected_valid"], case["id"]
        assert case["expected_disposition"]

    assert not by_id["clean-disjoint-components"]["expected_violation_codes"]
    assert (
        "new untouched validation cohort"
        in by_id["validation-peek-changes-method"]["expected_disposition"]
    )
    assert (
        "permanently ineligible"
        in by_id["relationship-evidence-assisted-inference"]["expected_disposition"]
    )


def test_reference_access_requires_role_appropriate_post_freeze_comparison() -> None:
    authorized = ReferenceAccessEvent(
        participant_id="SYN-P-CAL",
        actor=ReferenceActor.INDEPENDENT_CALIBRATION_EVALUATOR,
        purpose=ReferencePurpose.POST_FREEZE_CALIBRATION_COMPARISON,
        method_frozen=True,
        output_frozen=True,
    )
    assert not reference_access_violations((authorized,))

    assert reference_access_violations(
        (
            ReferenceAccessEvent(
                participant_id="SYN-P-CAL",
                actor=ReferenceActor.INDEPENDENT_CALIBRATION_EVALUATOR,
                purpose=ReferencePurpose.POST_FREEZE_CALIBRATION_COMPARISON,
                method_frozen=False,
                output_frozen=True,
            ),
        )
    ) == ("calibration_method_not_frozen",)
    assert reference_access_violations(
        (
            ReferenceAccessEvent(
                participant_id="SYN-P-CAL",
                actor=ReferenceActor.MODEL_DEVELOPER,
                purpose=ReferencePurpose.MODEL_FITTING,
                method_frozen=False,
                output_frozen=False,
            ),
        )
    ) == ("reference_leakage",)

    wrong_role_violations = validate_synthetic_case(
        (
            RoleAssignment(
                observation_id="SYN-WRONG-ROLE",
                participant_id="SYN-P-WRONG-ROLE",
                role=DataRole.LOCKED_VALIDATION,
            ),
        ),
        (
            ReferenceAccessEvent(
                participant_id="SYN-P-WRONG-ROLE",
                actor=ReferenceActor.INDEPENDENT_CALIBRATION_EVALUATOR,
                purpose=ReferencePurpose.POST_FREEZE_CALIBRATION_COMPARISON,
                method_frozen=True,
                output_frozen=True,
            ),
        ),
    )
    assert wrong_role_violations == ("reference_role_mismatch",)


def test_measurement_requirements_are_controls_only_and_prove_zero_item_content() -> None:
    measurement = _contract()["measurement_development_requirements"]
    requirement_ids = {item["id"] for item in measurement["required_future_evidence"]}
    proof = measurement["proof_no_measurement_content_written"]

    assert "requires a new ChatGPT Pro checkpoint" in measurement["checkpoint_gate"]
    assert requirement_ids == {
        "test-retest-reliability",
        "inter-rater-reliability",
        "missingness",
        "acquiescence-and-response-style",
        "social-desirability",
        "forer-barnum-susceptibility",
        "item-transparency-and-chart-cueing",
        "construct-overlap",
        "language-and-population-invariance",
        "blinded-authorship-and-evaluation",
        "item-generation-label-separation",
    }
    count_keys = {
        "questionnaire_items_authored",
        "response_choices_authored",
        "scoring_keys_authored",
        "chart_linked_interpretations_authored",
        "participant_semantics_selected",
        "estimator_formulas_selected",
        "operating_thresholds_selected",
        "participant_records_accessed",
    }
    assert count_keys <= proof.keys()
    assert all(proof[key] == 0 for key in count_keys)
    assert not (
        _all_keys(_contract())
        & {
            "questionnaire_items",
            "response_choices",
            "scoring_keys",
            "chart_linked_interpretations",
            "selected_estimator",
            "selected_operating_threshold",
            "participant_records",
        }
    )


def test_method_ledger_is_complete_without_selecting_an_estimator() -> None:
    ledger = _contract()["methods_decision_ledger"]
    by_family = {item["family"]: item for item in ledger}

    assert len(by_family) == len(ledger)
    assert {
        "interval-censored reference data",
        "prior sensitivity",
        "calibration",
        "abstention and rejection",
        "conformal and set-valued approaches",
        "measurement reliability",
        "participant and connected-component splitting",
        "nested adaptation",
        "permutation and negative controls",
        "selective and post-selection inference",
        "disclosure control",
        "traditional natal rectification heuristics",
    } <= by_family.keys()
    assert {item["classification"] for item in ledger} <= {
        "direct reuse",
        "adaptation",
        "baseline only",
        "incompatible",
        "unresolved/experimental",
    }
    assert all(item["reason"] for item in ledger)
    assert all(item["evidence_required_before_use"] for item in ledger)
    assert by_family["traditional natal rectification heuristics"]["classification"] == (
        "incompatible"
    )
    assert by_family["permutation and negative controls"]["classification"] == "baseline only"


def test_every_forbidden_semantic_is_fail_closed() -> None:
    flags = _contract()["forbidden_semantics"]

    assert set(flags) == {
        "prohibit_candidate_ranking_pruning_or_elimination",
        "prohibit_priors_weights_scores_probabilities_confidence_or_duration_mass",
        "prohibit_numeric_operating_or_abstention_thresholds",
        "prohibit_estimator_selection",
        "prohibit_questionnaire_items_choices_scoring_keys_or_chart_linked_interpretations",
        "prohibit_participant_semantics_and_participant_facing_output",
        "prohibit_relationship_evidence_or_inference",
        "prohibit_reference_leakage",
        "prohibit_live_records_recruitment_or_human_execution",
        "prohibit_final_cohort_size_burden_cost_or_expenditure_commitment",
        "prohibit_public_ledger_implementation_or_release",
        "prohibit_hd_validity_rectification_accuracy_or_human_calibration_claims",
    }
    assert all(value is True for value in flags.values())
