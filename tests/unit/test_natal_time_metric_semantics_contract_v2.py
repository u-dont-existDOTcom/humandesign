from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from hdmatch.util import sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
V1_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json"
V2_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V2.json"
V1_SHA256 = "c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9"
V2_SHA256 = "067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _assert_self_hash(value: dict[str, Any]) -> None:
    unhashed = deepcopy(value)
    expected = unhashed.pop("contract_sha256")
    assert expected == sha256_json(unhashed)


def test_v2_is_self_hashed_and_supersedes_only_metric_semantics_without_overwriting_v1() -> None:
    v1 = _load(V1_PATH)
    v2 = _load(V2_PATH)

    _assert_self_hash(v1)
    _assert_self_hash(v2)
    assert v1["schema_version"] == "natal-time-preinference-design-contract-v1"
    assert v1["contract_sha256"] == V1_SHA256
    assert v2["schema_version"] == "natal-time-preinference-metric-semantics-contract-v2"
    assert v2["contract_sha256"] == V2_SHA256
    assert v2["supersession"] == {
        "supersedes_scope": "metric and reference semantics only",
        "preserved_v1_path": "state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json",
        "preserved_v1_contract_sha256": V1_SHA256,
        "preserved_v1_unchanged": True,
        "rule": (
            "This v2 contract supersedes v1 only where it gives more specific interval, "
            "reference, output-validity, or metric semantics. Every other v1 study-design, "
            "leakage, role, baseline, measurement, and prohibition rule remains in force."
        ),
    }


def test_canonical_interval_endpoints_and_rounding_are_explicit_and_fail_closed() -> None:
    canonical = _load(V2_PATH)["canonical_interval_model"]
    endpoints = canonical["endpoint_conversion"]
    rounding = canonical["rounding_canonicalization"]

    assert canonical["interval_form"] == "half-open [start_utc, end_utc)"
    assert canonical["positive_width_required"] is True
    assert canonical["successor_quantum_microseconds"] == 1
    assert set(canonical["candidate_interval_identity"]) == {
        "candidate_manifest_sha256",
        "candidate_set_sha256",
        "interval_id",
        "start_utc",
        "end_utc",
        "full_state_sha256",
    }
    assert (
        "every candidate_interval_identity field exactly equals"
        in canonical["candidate_membership_equality"]
    )
    assert "first representable microsecond" in endpoints["open_lower"]
    assert "first representable microsecond" in endpoints["closed_upper"]
    assert "strictly later" in endpoints["invalid_result"]
    assert rounding["floor_or_truncate"] == (
        "For recorded value v and declared quantum q, use [v, v+q)."
    )
    assert "[v-q/2, v+q/2)" in rounding["nearest"]
    assert "[successor(v-q), successor(v))" in rounding["ceiling"]
    assert "rounding_direction_unresolved" in rounding["known_quantum_unknown_direction"]
    assert "No eligible canonical T_i" in rounding["missing_quantum_or_unresolved_utc_mapping"]
    assert "never becomes a zero-width point" in rounding["point_promotion_prohibited"]


def test_output_contract_rejects_empty_duplicate_partial_manufactured_and_foreign_members() -> None:
    contract = _load(V2_PATH)["returned_output_contract"]
    subset = contract["candidate_subset"]
    abstention = contract["abstention"]
    cases = {case["id"]: case for case in _load(V2_PATH)["contract_rejection_cases"]}

    assert contract["allowed_output_kinds"] == ["candidate_subset", "abstention"]
    assert subset["non_empty_required"] is True
    assert "Never silently deduplicate" in subset["duplicate_policy"]
    assert "Reject any selected record" in subset["partial_interval_policy"]
    assert "unions, splits, interpolated windows" in subset["manufactured_interval_policy"]
    assert "another participant" in subset["foreign_interval_policy"]
    assert "never converted to abstention" in subset["empty_policy"]
    assert abstention["selected_intervals_required_value"] == []
    assert "neither success nor error" in abstention["interpretation"]

    assert {
        "empty-non-abstention",
        "duplicate-selected-interval",
        "partial-selected-interval",
        "manufactured-selected-interval",
        "foreign-selected-interval",
        "abstention-with-selected-interval",
        "conflicting-documentary-sources",
        "reference-outside-candidate-domain",
        "valid-explicit-abstention",
    } == cases.keys()
    for case_id in (
        "empty-non-abstention",
        "duplicate-selected-interval",
        "partial-selected-interval",
        "manufactured-selected-interval",
        "foreign-selected-interval",
        "abstention-with-selected-interval",
    ):
        assert cases[case_id]["expected_status"] == "not_computed_invalid_output"
        assert cases[case_id]["expected_violation"]


def test_reference_conflicts_domain_compatibility_and_documentary_width_fail_closed() -> None:
    reference = _load(V2_PATH)["reference_standard_v2"]
    adjudication = reference["multiple_source_adjudication"]
    compatibility = reference["reference_domain_compatibility"]
    width = reference["documentary_reference_width"]

    assert "exactly the same interval" in adjudication["identical_sources"]
    assert "does not infer consistency from overlap" in adjudication["conflicting_sources"]
    assert "Produce no operative T_i" in adjudication["conflicting_sources"]
    assert "compute no validation frontier metrics" in adjudication["conflicting_sources"]
    prohibition = adjudication["silent_combination_or_choice_prohibited"]
    assert "Do not average, intersect, union, clip" in prohibition
    assert "do not select" in prohibition
    assert "positive-width intersection with D_i" in compatibility["compatible_when"]
    assert "Endpoint touching alone is no intersection" in compatibility["set_condition"]
    assert (
        "Partial overlap does not produce reference_domain_incompatible"
        in compatibility["partial_overlap_rule"]
    )
    assert "do not clip T_i to D_i" in compatibility["partial_overlap_rule"]
    assert compatibility["incompatible_status"] == "reference_domain_incompatible"
    assert "no positive-width intersection with D_i" in compatibility["failure_rule"]
    assert "not_applicable_reference_domain_incompatible" in compatibility["failure_rule"]
    assert width["field"] == "documentary_reference_width_microseconds"
    assert "end_utc minus start_utc" in width["definition"]
    assert width["source_widths_preserved"] is True
    assert "not a procedure-performance metric" in width["interpretation"]
    assert "descriptively available on abstention" in width["availability"]


def test_abstention_metrics_are_na_and_interval_count_is_separate_from_unique_state_count() -> None:
    semantics = _load(V2_PATH)["metric_semantics"]
    components = semantics["components"]

    assert "not_applicable_abstention" in semantics["applicability_status_codes"]
    assert "all not_applicable_abstention" in semantics["abstention_rule"]
    assert "Never convert reference failure" in semantics["reference_failure_rule"]
    assert components["temporal_width_retained"]["separate_from_all_count_metrics"] is True
    interval_count = components["canonical_interval_count_retained"]
    state_count = components["unique_state_identity_count_retained"]
    assert interval_count["separate_from_unique_state_identity_count"] is True
    assert "duplicates are rejected" in interval_count["selected_interval_count"]
    assert "distinct full_state_sha256" in state_count["candidate_unique_state_identity_count"]
    assert (
        "multiple intervals but one unique state identity"
        in state_count["same_state_multiple_intervals_rule"]
    )
    assert state_count["reduced_signature_prohibited"] is True
    assert semantics["scalar_combination_prohibited"] is True
    assert "weighted utility" in semantics["prohibited_combination_forms"]
    assert (
        "implicit ordering produced by collapsing components"
        in semantics["prohibited_combination_forms"]
    )


def test_v2_remains_contract_only_with_every_inference_semantic_forbidden() -> None:
    contract = _load(V2_PATH)
    boundary = contract["implementation_boundary"]

    assert contract["status"]["metric_evaluator_implemented"] is False
    assert boundary["metric_or_evaluator_execution_present"] is False
    assert boundary["protected_deterministic_components_modified"] is False
    assert "contract, documentation, content hashing" in boundary["authorized_work"]
    assert "later separately authorized phase" in boundary["future_execution_gate"]
    assert all(contract["forbidden_semantics"].values())
