from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from hdmatch.util import sha256_json
from scripts.audit_natal_time_preinference_feasibility import (
    build_feasibility_report,
    build_methods_decision_ledger,
    build_public_ledger_schema,
    build_unresolved_decision_register,
    calibration_error_interval,
    hoeffding_half_width,
    paired_required_sample_size,
    validate_public_aggregate_semantics,
    wilson_interval,
)

PROJECT_ROOT = Path(__file__).parents[2]


def _assert_self_hash(payload: dict[str, Any], field: str) -> None:
    unhashed = deepcopy(payload)
    expected = unhashed.pop(field)
    assert expected == sha256_json(unhashed)


def _load(name: str) -> dict[str, Any]:
    value = json.loads((PROJECT_ROOT / "state" / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in _all_keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in _all_keys(item)}
    return set()


def test_feasibility_formulas_are_deterministic_and_bounded() -> None:
    assert wilson_interval(100, 0.5) == {
        "lower": 0.403832,
        "upper": 0.596168,
        "half_width": 0.096168,
    }
    assert hoeffding_half_width(100) == 0.13581
    assert paired_required_sample_size(0.05, 0.3) > paired_required_sample_size(0.1, 0.3)
    assert calibration_error_interval(100, 0.5, 0.1) == {
        "assumed_observed_rate": 0.6,
        "signed_error_lower": 0.002003,
        "signed_error_upper": 0.190599,
        "sampling_half_width": 0.094298,
    }


def test_feasibility_report_is_synthetic_nonselecting_and_complete() -> None:
    report = build_feasibility_report("1" * 40)
    _assert_self_hash(report, "artifact_sha256")

    assert report["synthetic_only"] is True
    assert report["human_observations_used"] == 0
    assert not any(report["non_selections"].values())
    assert report["global_assumptions"]["synthetic_chart_oracle_is_not_a_human_effect_estimate"]
    assert len(report["binary_rate_precision"]["rows"]) == 45
    assert len(report["width_and_state_count_precision"]["rows"]) == 10
    assert len(report["paired_baseline_sensitivity"]["rows"]) == 9
    paired = report["paired_baseline_sensitivity"]
    assert paired["target_power_selected"] is False
    assert any("-1, 0, or +1" in assumption for assumption in paired["assumptions"])
    assert any("Wald-normal" in assumption for assumption in paired["assumptions"])
    calibration = report["potential_future_calibration_error_sensitivity"]
    assert calibration["all_predicted_rates_and_deviations_are_hypothetical"] is True
    assert calibration["signed_error_definition"] == (
        "observed event rate minus hypothetical predicted rate"
    )
    assert len(calibration["rows"]) == 36
    assert {row["hypothetical_predicted_rate"] for row in calibration["rows"]} == {
        0.2,
        0.5,
        0.8,
    }
    assert {row["hypothetical_signed_calibration_deviation"] for row in calibration["rows"]} == {
        -0.1,
        0.0,
        0.1,
    }
    assert len(report["subgroup_and_source_quality_sensitivity"]["rows"]) == 24


def test_public_ledger_schema_is_release_disabled_and_aggregate_only() -> None:
    artifact = build_public_ledger_schema("2" * 40)
    _assert_self_hash(artifact, "artifact_sha256")

    assert artifact["default_granularity"] == "cohort_aggregate_only"
    assert artifact["public_release_authorized"] is False
    assert artifact["synthetic_example"]["release_authorized"] is False
    assert artifact["record_schema"]["additionalProperties"] is False
    assert artifact["record_schema"]["x-semantic-validator"]["required"] is True
    assert artifact["semantic_validation"]["synthetic_example_status"] == "passed"
    assert validate_public_aggregate_semantics(artifact["synthetic_example"]) == ()
    aggregate_schema = artifact["record_schema"]["properties"]["cohort_aggregate"]
    assert aggregate_schema["additionalProperties"] is False
    aggregate = artifact["synthetic_example"]["cohort_aggregate"]
    assert aggregate["included_count"] == (
        aggregate["abstention_count"] + aggregate["non_abstaining_evaluable_count"]
    )
    assert (
        aggregate["temporal_width_retained_ratio_summary"]["eligible_count"]
        == (aggregate["non_abstaining_evaluable_count"])
    )
    assert (
        aggregate["full_state_count_retained_ratio_summary"]["eligible_count"]
        == (aggregate["non_abstaining_evaluable_count"])
    )
    keys = _all_keys(artifact["record_schema"])
    assert keys.isdisjoint(
        {
            "participant_id",
            "birth_date",
            "birth_time",
            "birth_place",
            "timezone",
            "relationship_id",
            "personal_data_hash",
            "free_text",
            "chart_intervals",
        }
    )
    assert {
        "participant_level_rows",
        "exact_birth_dates",
        "relationship_identifiers",
        "personal_data_hashes",
        "free_text",
    }.issubset(set(artifact["prohibited_public_fields"]))


def test_public_aggregate_semantics_reject_cross_field_mutants_and_zero_is_explicit() -> None:
    example = build_public_ledger_schema("2" * 40)["synthetic_example"]
    mutants: list[tuple[dict[str, Any], str]] = []

    included_too_large = deepcopy(example)
    included_too_large["cohort_aggregate"]["included_count"] = 201
    mutants.append((included_too_large, "included_count_exceeds_eligible_count"))

    broken_partition = deepcopy(example)
    broken_partition["cohort_aggregate"]["non_abstaining_evaluable_count"] = 136
    mutants.append(
        (
            broken_partition,
            "included_count_not_abstention_plus_non_abstaining_evaluable",
        )
    )

    too_many_intersections = deepcopy(example)
    too_many_intersections["cohort_aggregate"]["coverage_intersection_count"] = 136
    mutants.append((too_many_intersections, "coverage_intersection_count_exceeds_evaluable_count"))

    bad_date_denominator = deepcopy(example)
    bad_date_denominator["cohort_aggregate"]["date_coverage_evaluable_count"] = 41
    mutants.append(
        (
            bad_date_denominator,
            "date_coverage_evaluable_count_exceeds_eligible_count",
        )
    )

    bad_ratio_denominator = deepcopy(example)
    bad_ratio_denominator["cohort_aggregate"]["temporal_width_retained_ratio_summary"][
        "eligible_count"
    ] = 180
    mutants.append(
        (
            bad_ratio_denominator,
            (
                "temporal_width_retained_ratio_summary_eligible_count_not_"
                "non_abstaining_evaluable_count"
            ),
        )
    )

    for mutant, expected_error in mutants:
        assert expected_error in validate_public_aggregate_semantics(mutant)

    all_abstain = deepcopy(example)
    aggregate = all_abstain["cohort_aggregate"]
    aggregate.update(
        {
            "eligible_count": 10,
            "included_count": 10,
            "non_abstaining_evaluable_count": 0,
            "coverage_intersection_count": 0,
            "abstention_count": 10,
            "date_coverage_eligible_count": 0,
            "date_coverage_evaluable_count": 0,
            "date_coverage_intersection_count": 0,
        }
    )
    for summary_name in (
        "temporal_width_retained_ratio_summary",
        "full_state_count_retained_ratio_summary",
    ):
        aggregate[summary_name] = {"eligible_count": 0, "mean": None, "median": None}
    assert validate_public_aggregate_semantics(all_abstain) == ()

    fabricated_zero_summary = deepcopy(all_abstain)
    fabricated_zero_summary["cohort_aggregate"]["temporal_width_retained_ratio_summary"]["mean"] = (
        0.0
    )
    assert (
        "temporal_width_retained_ratio_summary_mean_must_be_null_when_count_is_zero"
        in validate_public_aggregate_semantics(fabricated_zero_summary)
    )


def test_public_schema_string_values_are_controlled_not_free_text() -> None:
    schema = build_public_ledger_schema("2" * 40)["record_schema"]

    def string_schemas(value: object) -> list[dict[str, Any]]:
        if isinstance(value, dict):
            own = [value] if value.get("type") == "string" else []
            return own + [node for nested in value.values() for node in string_schemas(nested)]
        if isinstance(value, list):
            return [node for nested in value for node in string_schemas(nested)]
        return []

    nodes = string_schemas(schema)
    assert nodes
    assert all({"const", "enum", "pattern"} & node.keys() for node in nodes)

    provenance = schema["properties"]["nonpersonal_provenance"]["properties"]
    assert re.fullmatch(provenance["protocol_version"]["pattern"], "NT-PROTOCOL-20260830-V1")
    assert not re.fullmatch(provenance["protocol_version"]["pattern"], "participant narrative here")
    control_codes = set(
        schema["properties"]["disclosure_review"]["properties"]["unresolved_controls"]["items"][
            "enum"
        ]
    )
    assert "participant narrative here" not in control_codes


def test_methods_ledger_covers_required_families_without_estimator_choice() -> None:
    ledger = build_methods_decision_ledger("3" * 40)
    _assert_self_hash(ledger, "ledger_sha256")

    assert ledger["estimator_selected"] is False
    by_family = {entry["method_family"]: entry for entry in ledger["entries"]}
    assert {
        "interval_censored_reference_data",
        "prior_sensitivity",
        "probability_calibration",
        "abstention_rejection",
        "conformal_set_valued",
        "measurement_reliability",
        "participant_connected_component_splitting",
        "nested_adaptation",
        "permutation_and_negative_controls",
        "selective_post_selection_inference",
        "disclosure_control",
    }.issubset(by_family)
    assert set(entry["classification"] for entry in ledger["entries"]) == set(
        ledger["allowed_classifications"]
    )
    assert all(entry["reason"] for entry in ledger["entries"])
    assert all(entry["evidence_required_before_use"] for entry in ledger["entries"])


def test_unresolved_register_selects_nothing_and_preserves_owner_boundaries() -> None:
    register = build_unresolved_decision_register("4" * 40)
    _assert_self_hash(register, "register_sha256")

    assert register["owner_decision_required_now"] is False
    assert len(register["decisions"]) == 12
    assert all(item["status"] == "unresolved" for item in register["decisions"])
    assert all(item["selected_value"] is None for item in register["decisions"])
    assert all(item["implementation_blocked"] is True for item in register["decisions"])
    by_decision = {item["decision"]: item for item in register["decisions"]}
    participant_facing = by_decision["participant_facing_use_case_and_output"]
    assert "explicit owner choice" in participant_facing["evidence_or_authority_required"]
    assert "new Pro checkpoint" in participant_facing["evidence_or_authority_required"]


def test_committed_machine_artifacts_match_their_builders() -> None:
    artifacts: tuple[tuple[str, Any, str], ...] = (
        (
            "NATAL-TIME-PREINFERENCE-FEASIBILITY.json",
            build_feasibility_report,
            "artifact_sha256",
        ),
        (
            "NATAL-TIME-PUBLIC-LEDGER-SYNTHETIC-SCHEMA.json",
            build_public_ledger_schema,
            "artifact_sha256",
        ),
        (
            "NATAL-TIME-METHODS-DECISION-LEDGER.json",
            build_methods_decision_ledger,
            "ledger_sha256",
        ),
        (
            "NATAL-TIME-UNRESOLVED-DECISIONS.json",
            build_unresolved_decision_register,
            "register_sha256",
        ),
    )
    for name, builder, hash_field in artifacts:
        payload = _load(name)
        assert payload == builder(payload["repository_commit"])
        _assert_self_hash(payload, hash_field)


def test_threat_model_addresses_every_checkpoint_threat_without_policy_selection() -> None:
    text = (PROJECT_ROOT / "docs/NATAL_TIME_PUBLIC_LEDGER_THREAT_MODEL_20260830.md").read_text(
        encoding="utf-8"
    )
    required_phrases = (
        "Exact birth linkage",
        "Sparse state fingerprints",
        "Membership inference",
        "Rare candidate sets",
        "Repeated-release differencing",
        "Relationship-network linkage",
        "Deterministic personal-data hashes",
        "Small cells",
        "Free text",
        "Withdrawal and deletion",
        "Versioned corrections",
        "cohort-aggregate",
        "No small-cell suppression threshold, privacy budget, release cadence",
    )
    assert all(phrase in text for phrase in required_phrases)
