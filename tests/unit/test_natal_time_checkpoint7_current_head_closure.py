from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

import pytest

from hdmatch.util import sha256_json
from scripts.audit_natal_time_checkpoint7_current_head_closure import (
    ACCEPTANCE_TEST_IDS,
    CHECKPOINT7_IMPLEMENTATION,
    EXPECTED_AGGREGATE_SHA256,
    EXPECTED_INDEX_SHA256,
    EXPECTED_ORACLE_VERSION_SHA256,
    EXPECTED_SUBMISSION_DELTA,
    IMPLEMENTATION_DELTA_CLASSIFICATION,
    OUTPUT_PATH,
    CurrentHeadClosureError,
    CurrentHeadRouteBRequired,
    _require_function_equal,
    _require_oracle_source,
    _require_replay_equal,
    validate_current_head_closure,
)

PROJECT_ROOT = Path(__file__).parents[2]


@pytest.fixture(scope="module")
def closure() -> dict[str, Any]:
    raw = json.loads((PROJECT_ROOT / OUTPUT_PATH).read_bytes())
    assert isinstance(raw, dict)
    payload = cast(dict[str, Any], raw)
    validate_current_head_closure(PROJECT_ROOT, payload, require_clean=True)
    assert payload["acceptance_test_count"] == 21
    assert payload["all_acceptance_tests_passed"] is True
    return payload


def _assert_acceptance(payload: dict[str, Any], index: int) -> None:
    results = cast(list[dict[str, Any]], payload["acceptance_tests"])
    assert results[index] == {
        "acceptance_test_id": ACCEPTANCE_TEST_IDS[index],
        "status": "passed",
    }


def test_checkpoint6_final_is_ancestor_of_implementation(
    closure: dict[str, Any],
) -> None:
    topology = cast(dict[str, Any], closure["topology_and_scope"])
    assert topology["checkpoint6_final_is_ancestor"] is True
    _assert_acceptance(closure, 0)


def test_oracle_source_is_ancestor_of_implementation(closure: dict[str, Any]) -> None:
    topology = cast(dict[str, Any], closure["topology_and_scope"])
    assert topology["oracle_source_is_ancestor"] is True
    _assert_acceptance(closure, 1)


def test_implementation_is_direct_parent_of_documentation_head(
    closure: dict[str, Any],
) -> None:
    topology = cast(dict[str, Any], closure["topology_and_scope"])
    submission = cast(dict[str, Any], topology["checkpoint7_submission"])
    assert submission["parents"] == [CHECKPOINT7_IMPLEMENTATION]
    assert topology["submission_direct_parent_verified"] is True
    _assert_acceptance(closure, 2)


def test_relevant_range_is_linear_and_merge_free(closure: dict[str, Any]) -> None:
    topology = cast(dict[str, Any], closure["topology_and_scope"])
    assert topology["no_merge_commit_or_alternate_parent_path"] is True
    _assert_acceptance(closure, 3)


def test_documentation_head_delta_is_exact(closure: dict[str, Any]) -> None:
    topology = cast(dict[str, Any], closure["topology_and_scope"])
    expected = [
        {"status": status, "path": path} for status, path in EXPECTED_SUBMISSION_DELTA
    ]
    assert topology["submission_delta"] == expected
    _assert_acceptance(closure, 4)


def test_all_58_replay_paths_are_compared(closure: dict[str, Any]) -> None:
    binding = cast(dict[str, Any], closure["replay_current_head_binding"])
    records = cast(list[dict[str, Any]], binding["replay_affecting_files"])
    assert binding["replay_affecting_file_count"] == len(records) == 58
    assert all(record["byte_identical"] is True for record in records)
    _assert_acceptance(closure, 5)


def test_all_28_semantic_functions_are_compared(closure: dict[str, Any]) -> None:
    binding = cast(dict[str, Any], closure["replay_current_head_binding"])
    records = cast(list[dict[str, Any]], binding["semantic_functions"])
    assert binding["semantic_function_count"] == len(records) == 28
    assert all(record["ast_identical"] is True for record in records)
    _assert_acceptance(closure, 6)


def test_all_required_replay_categories_are_identical(closure: dict[str, Any]) -> None:
    binding = cast(dict[str, Any], closure["replay_current_head_binding"])
    assert set(cast(list[str], binding["semantic_categories"])) == {
        "canonical_serialization",
        "digest_construction",
        "durable_write_resume",
        "engine_invocation",
        "event_interval_construction",
        "fixture_inputs",
        "independent_verification",
        "index_construction_validation",
        "receipt_semantic_fields",
    }
    _assert_acceptance(closure, 7)


def test_every_a7a_to_d2_change_is_explicitly_classified(
    closure: dict[str, Any],
) -> None:
    topology = cast(dict[str, Any], closure["topology_and_scope"])
    records = cast(list[dict[str, Any]], topology["implementation_delta_classification"])
    assert topology["implementation_delta_count"] == len(records) == 14
    assert {cast(str, item["path"]) for item in records} == set(
        IMPLEMENTATION_DELTA_CLASSIFICATION
    )
    _assert_acceptance(closure, 8)


def test_receipt_semantic_change_requires_route_b(closure: dict[str, Any]) -> None:
    with pytest.raises(CurrentHeadRouteBRequired, match="replay-affecting byte changed"):
        _require_replay_equal("synthetic/path", b"before", b"after")
    with pytest.raises(CurrentHeadRouteBRequired, match="replay function changed"):
        _require_function_equal("synthetic.py", "function", "a", "b")
    _assert_acceptance(closure, 9)


def test_d2_receipts_index_and_aggregate_reconstruct(closure: dict[str, Any]) -> None:
    validation = cast(dict[str, Any], closure["checkpoint7_receipt_validation"])
    assert validation["receipt_count"] == 9
    assert validation["all_nine_receipts_valid"] is True
    assert validation["index_byte_equivalent"] is True
    assert validation["index_sha256"] == EXPECTED_INDEX_SHA256
    assert validation["aggregate_sha256"] == EXPECTED_AGGREGATE_SHA256
    _assert_acceptance(closure, 10)


def test_every_replay_path_and_function_mutation_invalidates_closure(
    closure: dict[str, Any],
) -> None:
    binding = cast(dict[str, Any], closure["replay_current_head_binding"])
    file_probes = cast(list[dict[str, Any]], binding["file_mutation_probes"])
    function_probes = cast(list[dict[str, Any]], binding["function_mutation_probes"])
    assert binding["file_mutation_probe_count"] == len(file_probes) == 58
    assert binding["function_mutation_probe_count"] == len(function_probes) == 28
    assert all(item["route_b_required"] is True for item in file_probes)
    assert all(item["route_b_required"] is True for item in function_probes)
    _assert_acceptance(closure, 11)


def test_oracle_blob_matches_at_all_three_heads(closure: dict[str, Any]) -> None:
    oracle = cast(dict[str, Any], closure["oracle_current_head_binding"])
    records = cast(dict[str, dict[str, str]], oracle["source_records"])
    assert set(records) == {
        "oracle_source",
        "checkpoint7_implementation",
        "checkpoint7_submission",
    }
    assert len({record["git_blob_oid"] for record in records.values()}) == 1
    assert len({record["sha256"] for record in records.values()}) == 1
    _assert_acceptance(closure, 12)


def test_oracle_version_recomputes_exactly(closure: dict[str, Any]) -> None:
    oracle = cast(dict[str, Any], closure["oracle_current_head_binding"])
    assert oracle["version_sha256"] == EXPECTED_ORACLE_VERSION_SHA256
    version = cast(dict[str, Any], oracle["version"])
    assert version["oracle_version_sha256"] == EXPECTED_ORACLE_VERSION_SHA256
    _assert_acceptance(closure, 13)


def test_d2_oracle_ast_remains_structurally_independent(
    closure: dict[str, Any],
) -> None:
    oracle = cast(dict[str, Any], closure["oracle_current_head_binding"])
    audit = cast(dict[str, Any], oracle["independence_audit"])
    assert audit["standard_library_only"] is True
    assert audit["production_imports"] == []
    assert audit["repository_script_imports"] == []
    assert audit["dynamic_import_calls"] == []
    assert audit["subprocess_or_shell_calls"] == []
    assert audit["s_i_generation_or_optimization_definitions"] == []
    assert audit["constructs_or_chooses_s_i"] is False
    _assert_acceptance(closure, 14)


def test_four_oracle_artifacts_reproduce_from_d2(closure: dict[str, Any]) -> None:
    oracle = cast(dict[str, Any], closure["oracle_current_head_binding"])
    records = cast(list[dict[str, Any]], oracle["artifact_records"])
    assert oracle["artifact_count"] == len(records) == 4
    assert oracle["artifacts_reproduce_exactly"] is True
    _assert_acceptance(closure, 15)


def test_oracle_source_mutation_invalidates_version_and_closure(
    closure: dict[str, Any],
) -> None:
    oracle = cast(dict[str, Any], closure["oracle_current_head_binding"])
    probe = cast(dict[str, Any], oracle["source_mutation_probe"])
    assert probe["source_binding_invalidated"] is True
    assert probe["current_head_closure_invalidated"] is True
    with pytest.raises(CurrentHeadClosureError, match="oracle source hash changed"):
        _require_oracle_source(b"mutated oracle source")
    _assert_acceptance(closure, 16)


def test_all_48_protected_paths_remain_identical(closure: dict[str, Any]) -> None:
    protected = cast(dict[str, Any], closure["protected_core_binding"])
    assert protected["protected_path_count"] == 48
    assert protected["mismatch_count"] == 0
    _assert_acceptance(closure, 17)


def test_changed_scope_contains_no_prohibited_data_or_semantics(
    closure: dict[str, Any],
) -> None:
    scan = cast(dict[str, Any], closure["prohibited_scope_scan"])
    assert scan == {
        "implementation_delta_exactly_classified": True,
        "participant_or_live_data_introduced": False,
        "documentary_reference_data_introduced": False,
        "relationship_data_or_evidence_introduced": False,
        "questionnaire_content_introduced": False,
        "candidate_choice_or_inferential_semantics_introduced": False,
        "all_oracle_artifacts_synthetic_only": True,
    }
    _assert_acceptance(closure, 18)


def test_saved_closure_reproduces_and_rehashed_tamper_fails(
    closure: dict[str, Any],
) -> None:
    anchors = cast(dict[str, Any], closure["anchors"])
    assert set(anchors) == {
        "checkpoint6_final",
        "oracle_source",
        "checkpoint7_implementation",
        "checkpoint7_submission",
        "checkpoint7_submission_tree",
    }
    prior = cast(dict[str, Any], closure["prior_replay_closure"])
    assert prior["preserved_not_overwritten"] is True
    validate_current_head_closure(PROJECT_ROOT, closure, require_clean=True)
    mutant = deepcopy(closure)
    mutant["all_acceptance_tests_passed"] = False
    mutant.pop("current_head_closure_sha256")
    mutant["current_head_closure_sha256"] = sha256_json(mutant)
    with pytest.raises(CurrentHeadClosureError, match="does not reproduce exactly"):
        validate_current_head_closure(PROJECT_ROOT, mutant, require_clean=False)
    _assert_acceptance(closure, 19)


def test_worktree_and_index_are_clean(closure: dict[str, Any]) -> None:
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert status.stdout == ""
    assert closure["clean_worktree_and_index_required_for_generation_and_validation"] is True
    _assert_acceptance(closure, 20)
