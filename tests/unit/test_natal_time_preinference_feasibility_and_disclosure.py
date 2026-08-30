from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from hdmatch.util import sha256_json
from scripts.audit_natal_time_preinference_feasibility import (
    build_feasibility_report,
    build_methods_decision_ledger,
    build_public_ledger_schema,
    build_unresolved_decision_register,
    hoeffding_half_width,
    paired_required_sample_size,
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
    assert len(report["potential_future_calibration_precision"]["rows"]) == 24
    assert len(report["subgroup_and_source_quality_sensitivity"]["rows"]) == 24


def test_public_ledger_schema_is_release_disabled_and_aggregate_only() -> None:
    artifact = build_public_ledger_schema("2" * 40)
    _assert_self_hash(artifact, "artifact_sha256")

    assert artifact["default_granularity"] == "cohort_aggregate_only"
    assert artifact["public_release_authorized"] is False
    assert artifact["synthetic_example"]["release_authorized"] is False
    assert artifact["record_schema"]["additionalProperties"] is False
    aggregate_schema = artifact["record_schema"]["properties"]["cohort_aggregate"]
    assert aggregate_schema["additionalProperties"] is False
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
    assert len(register["decisions"]) == 11
    assert all(item["status"] == "unresolved" for item in register["decisions"])
    assert all(item["selected_value"] is None for item in register["decisions"])
    assert all(item["implementation_blocked"] is True for item in register["decisions"])


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
    text = (
        PROJECT_ROOT / "docs/NATAL_TIME_PUBLIC_LEDGER_THREAT_MODEL_20260830.md"
    ).read_text(encoding="utf-8")
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
