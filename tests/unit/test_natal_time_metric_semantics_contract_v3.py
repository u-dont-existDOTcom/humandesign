from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

from hdmatch.util import sha256_file, sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
V3_AUDIT_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3-AUDIT.json"
UNRESOLVED_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-UNRESOLVED-DECISIONS.json"
STUDY_DESIGN_PATH = PROJECT_ROOT / "docs" / "NATAL_TIME_PREINFERENCE_STUDY_DESIGN_20260830.md"


def _load_audit_module() -> ModuleType:
    path = PROJECT_ROOT / "scripts" / "audit_natal_time_metric_semantics_v3.py"
    spec = importlib.util.spec_from_file_location("audit_natal_time_metric_semantics_v3", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = _load_audit_module()
REFERENCE_EDGE_IDS = AUDIT.REFERENCE_EDGE_IDS
SUBSET_EDGE_IDS = AUDIT.SUBSET_EDGE_IDS
V1_CONTRACT_SHA256 = AUDIT.V1_CONTRACT_SHA256
V1_FILE_SHA256 = AUDIT.V1_FILE_SHA256
V1_PATH = AUDIT.V1_PATH
V2_CONTRACT_SHA256 = AUDIT.V2_CONTRACT_SHA256
V2_FILE_SHA256 = AUDIT.V2_FILE_SHA256
V2_PATH = AUDIT.V2_PATH
V3_CONTRACT_SHA256 = AUDIT.V3_CONTRACT_SHA256
V3_PATH = AUDIT.V3_PATH
build_audit_report = AUDIT.build_audit_report
validate_v3_contract = AUDIT.validate_v3_contract


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def _assert_contract_hash(payload: dict[str, Any], expected: str) -> None:
    unhashed = deepcopy(payload)
    assert unhashed.pop("contract_sha256") == expected
    assert sha256_json(unhashed) == expected


def test_v3_is_self_hashed_and_preserves_exact_v1_v2_bytes() -> None:
    v1 = _load(PROJECT_ROOT / V1_PATH)
    v2 = _load(PROJECT_ROOT / V2_PATH)
    v3 = validate_v3_contract(PROJECT_ROOT)

    assert sha256_file(PROJECT_ROOT / V1_PATH) == V1_FILE_SHA256
    assert sha256_file(PROJECT_ROOT / V2_PATH) == V2_FILE_SHA256
    _assert_contract_hash(v1, V1_CONTRACT_SHA256)
    _assert_contract_hash(v2, V2_CONTRACT_SHA256)
    _assert_contract_hash(v3, V3_CONTRACT_SHA256)
    assert v3["supersession"]["preserved_v1"]["unchanged"] is True
    assert v3["supersession"]["preserved_v2"]["unchanged"] is True
    assert v3["supersession"]["supersedes_scope"] == (
        "selected-subset adjacency and candidate-reference-domain compatibility semantics only"
    )


def test_C_i_partition_is_preserved_but_S_i_has_no_adjacency_requirement() -> None:
    semantics = _load(PROJECT_ROOT / V3_PATH)["set_semantics_v3"]
    candidate = semantics["C_i"]
    selected = semantics["S_i_candidate_subset"]

    assert "gap-free, non-overlapping partition" in candidate["partition_requirement"]
    assert "candidate construction, not" in candidate["partition_scope"]
    assert "any nonempty unordered subset" in selected["definition"]
    assert "nonadjacent intervals on the same civil date" in selected["allowed_geometry"]
    assert "are not validity conditions" in selected["adjacency_rule"]
    assert "does not require S_i" in selected["distinct_from_C_i_partition"]
    assert "canonical reordering" in selected["ordering_rule"]
    assert {
        "no duplicate interval ID or complete identity",
        "no changed endpoint or partial interval",
        "no manufactured union, split, interpolation, or spanning window",
    }.issubset(set(selected["validation_requirements"]))


def test_D_i_is_exact_union_and_reference_domain_has_exactly_three_states() -> None:
    contract = _load(PROJECT_ROOT / V3_PATH)
    domain = contract["set_semantics_v3"]["D_i"]
    compatibility = contract["reference_domain_compatibility_v3"]
    states = {item["status"]: item for item in compatibility["states"]}

    assert domain["formula"] == "D_i = union_{I in C_i} I"
    assert "not the convex hull" in domain["no_convex_hull_rule"]
    assert set(states) == {
        "reference_domain_compatible",
        "reference_domain_partially_incompatible",
        "reference_domain_incompatible",
    }
    assert "T_i is a subset of D_i" in states["reference_domain_compatible"]["condition"]
    assert (
        "overlap_width is positive"
        in states["reference_domain_partially_incompatible"]["condition"]
    )
    assert "overlap_width is zero" in states["reference_domain_incompatible"]["condition"]
    assert (
        states["reference_domain_compatible"]["valid_reference_evaluation_receipt_allowed"] is True
    )
    for status in (
        "reference_domain_partially_incompatible",
        "reference_domain_incompatible",
    ):
        assert states[status]["valid_reference_evaluation_receipt_allowed"] is False
        assert states[status]["reference_intersection_applicability"].startswith(
            "not_applicable_reference_domain_"
        )
    assert "neither credit nor error" in compatibility["partial_or_complete_incompatibility_rule"]
    assert "Never clip T_i" in compatibility["immutability_rule"]
    assert compatibility["diagnostics"]["permitted"] == [
        "reference_domain_status",
        "documentary_reference_width_microseconds",
    ]


def test_every_checkpoint5_subset_and_reference_edge_case_is_explicit() -> None:
    cases = {item["id"]: item for item in _load(PROJECT_ROOT / V3_PATH)["acceptance_edge_cases"]}

    assert set(cases) == REFERENCE_EDGE_IDS | SUBSET_EDGE_IDS
    disconnected = cases["s-i-disconnected-first-and-third-same-date"]
    assert disconnected["expected_status"] == "valid_candidate_subset"
    assert disconnected["expected_temporal_width"] == (
        "sum of first and third interval widths only"
    )
    assert disconnected["expected_interval_count_fraction"] == "2/4"
    assert cases["s-i-disconnected-reordered"]["expected_commitment"].startswith("identical")
    assert cases["s-i-disconnected-duplicate"]["expected_violation"] == (
        "duplicate_selected_interval"
    )
    assert cases["s-i-manufactured-spanning-window"]["expected_violation"] == (
        "manufactured_interval_not_allowed"
    )

    allowed = {
        case_id
        for case_id in REFERENCE_EDGE_IDS
        if cases[case_id]["valid_reference_evaluation_receipt_allowed"] is True
    }
    assert allowed == {
        "reference-contained-in-one-interval",
        "reference-contained-across-adjacent-intervals",
        "reference-multidate-included-date",
    }
    assert cases["reference-multidate-excluded-date"]["expected_status"] == (
        "reference_domain_incompatible"
    )
    assert cases["reference-endpoint-only-contact"]["expected_reference_intersection"] == (
        "not_applicable_reference_domain_incompatible"
    )


def test_v3_audit_artifact_reproduces_without_evaluator_execution() -> None:
    expected = build_audit_report(PROJECT_ROOT)
    committed = _load(V3_AUDIT_PATH)

    assert committed == expected
    unhashed = deepcopy(committed)
    assert unhashed.pop("audit_sha256") == sha256_json(unhashed)
    assert committed["status"] == "passed_contract_only_no_evaluator_execution"
    assert committed["human_records_accessed"] == 0
    assert committed["v3_contract_sha256"] == V3_CONTRACT_SHA256
    assert "no_evaluator_or_S_i_selector_implemented" in committed["checks"]


def test_v3_is_the_operating_reference_without_overwriting_v1_or_v2() -> None:
    register = _load(UNRESOLVED_PATH)
    references = register["metric_semantics_contract_references"]

    assert register["current_operative_metric_semantics_contract"] == "operative_v3"
    assert references["operative_v3"] == {
        "path": "state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json",
        "contract_sha256": V3_CONTRACT_SHA256,
        "status": "checkpoint_5_metric_reference_domain_contract",
    }
    assert references["operative_v2"]["contract_sha256"] == V2_CONTRACT_SHA256
    assert references["preserved_v1"]["contract_sha256"] == V1_CONTRACT_SHA256

    study = STUDY_DESIGN_PATH.read_text(encoding="utf-8")
    assert "NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json" in study
    assert V3_CONTRACT_SHA256 in study
    assert "any nonempty unordered subset" in study
    assert "reference_domain_partially_incompatible" in study
