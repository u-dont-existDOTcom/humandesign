from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from hdmatch.util import canonical_json_bytes, sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
LINEAGE_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-CHECKPOINT4-LINEAGE-ATTESTATION.json"
SOURCE_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json"


def _load_audit_module() -> ModuleType:
    path = PROJECT_ROOT / "scripts" / "audit_natal_time_checkpoint4_phase0.py"
    spec = importlib.util.spec_from_file_location("audit_natal_time_checkpoint4_phase0", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = _load_audit_module()
BASELINE = AUDIT.BASELINE
CHECKPOINT3_RULING_COMMIT = AUDIT.CHECKPOINT3_RULING_COMMIT
EVALUATED_HEAD = AUDIT.EVALUATED_HEAD
EXPECTED_REPLAY_AGGREGATE_SHA256 = AUDIT.EXPECTED_REPLAY_AGGREGATE_SHA256
EXPECTED_REPLAY_INDEX_SHA256 = AUDIT.EXPECTED_REPLAY_INDEX_SHA256
REPLAY_SOURCE = AUDIT.REPLAY_SOURCE
REVIEWED_CHECKPOINT3_HEAD = AUDIT.REVIEWED_CHECKPOINT3_HEAD
AttestationError = AUDIT.AttestationError
build_lineage_attestation = AUDIT.build_lineage_attestation
build_replay_source_manifest = AUDIT.build_replay_source_manifest
validate_lineage_attestation = AUDIT.validate_lineage_attestation
validate_replay_source_manifest = AUDIT.validate_replay_source_manifest


@pytest.fixture(scope="module")
def attestations() -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        build_lineage_attestation(PROJECT_ROOT),
        build_replay_source_manifest(PROJECT_ROOT),
    )


def test_lineage_attestation_is_exact_content_hashed_and_unmerged(
    attestations: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    lineage, _source = attestations
    unhashed = deepcopy(lineage)
    embedded = unhashed.pop("attestation_sha256")
    assert embedded == sha256_json(unhashed)
    assert lineage["anchors"]["baseline"]["commit"] == BASELINE
    assert lineage["anchors"]["reviewed_checkpoint3_head"]["commit"] == (
        REVIEWED_CHECKPOINT3_HEAD
    )
    assert lineage["anchors"]["checkpoint3_ruling_commit"]["commit"] == (
        CHECKPOINT3_RULING_COMMIT
    )
    assert lineage["anchors"]["replay_source"]["commit"] == REPLAY_SOURCE
    assert lineage["anchors"]["evaluated_head"]["commit"] == EVALUATED_HEAD
    assert lineage["ordered_commits"][0]["commit"] == REVIEWED_CHECKPOINT3_HEAD
    assert lineage["ordered_commits"][-1]["commit"] == EVALUATED_HEAD
    assert lineage["assertions"]["ordered_commits_form_one_direct_first_parent_chain"]
    assert lineage["assertions"]["merge_commit_count_after_reviewed_checkpoint3"] == 0
    assert lineage["assertions"]["checkpoint3_ruling_commit_is_doc_only"]
    assert lineage["assertions"]["all_protected_files_byte_identical"]
    assert lineage["assertions"]["all_immutable_embedded_hashes_valid"]
    assert [item["pair_id"] for item in lineage["diffs"]] == [
        "baseline_to_evaluated_head",
        "reviewed_checkpoint3_to_ruling_commit",
        "ruling_commit_to_replay_source",
        "replay_source_to_evaluated_head",
    ]


def test_replay_source_manifest_is_fail_closed_and_current_aggregate_matches(
    attestations: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    _lineage, source = attestations
    unhashed = deepcopy(source)
    embedded = unhashed.pop("manifest_sha256")
    assert embedded == sha256_json(unhashed)
    assertions = source["assertions"]
    assert assertions == {
        "replay_source_is_ancestor_of_evaluated_head": True,
        "import_closure_identical": True,
        "all_replay_affecting_files_byte_identical": True,
        "all_replay_affecting_git_blobs_identical": True,
        "all_required_replay_surface_categories_bound": True,
        "all_differences_explicitly_allowed": True,
        "allowed_differences_overlap_replay_affecting_files": False,
        "current_evaluated_head_aggregate_only_match": True,
        "transition_recomputation_performed": False,
    }
    paths = {item["path"] for item in source["replay_affecting_files"]}
    assert "scripts/replay_natal_time_real_engine_fixtures.py" in paths
    assert "src/hdmatch/natal_time/replay.py" in paths
    assert "src/hdmatch/__init__.py" in paths
    assert "src/hdmatch/chart/boundaries.py" in paths
    assert "state/NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json" in paths
    assert {
        item["category"] for item in source["required_surface_coverage"]
    } == {
        "replay_orchestration",
        "receipt_schemas_and_canonicalization",
        "source_integrity_checks",
        "fixture_definitions",
        "engine_adapter_invocation",
        "independent_verifier_invocation",
        "coverage_and_result_digest_construction",
        "aggregate_index_construction_and_validation",
    }
    allowed = {item["path"] for item in source["allowed_differences"]}
    assert len(allowed) == source["allowed_difference_count"] == 12
    assert "tests/unit/test_natal_time_real_engine_replay.py" in allowed
    assert not paths.intersection(allowed)
    aggregate = source["aggregate_only_verification"]
    assert aggregate["evaluated_head"] == EVALUATED_HEAD
    assert aggregate["replay_source_commit"] == REPLAY_SOURCE
    assert aggregate["receipt_count"] == 9
    assert aggregate["successful_civil_day_count"] == 8
    assert aggregate["fail_closed_civil_day_count"] == 1
    assert aggregate["aggregate_rebuilt_from_receipt_hashes_only"] is True
    assert aggregate["transition_recomputation_performed"] is False
    assert aggregate["index_sha256"] == EXPECTED_REPLAY_INDEX_SHA256
    assert aggregate["aggregate_sha256"] == EXPECTED_REPLAY_AGGREGATE_SHA256
    assert aggregate["index_matches_checkpoint4_expected_sha256"] is True
    assert aggregate["aggregate_matches_checkpoint4_expected_sha256"] is True


def test_committed_phase0_artifacts_reproduce_exactly(
    attestations: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    lineage, source = attestations
    assert LINEAGE_PATH.read_bytes() == canonical_json_bytes(lineage) + b"\n"
    assert SOURCE_PATH.read_bytes() == canonical_json_bytes(source) + b"\n"
    validate_lineage_attestation(PROJECT_ROOT, json.loads(LINEAGE_PATH.read_bytes()))
    validate_replay_source_manifest(PROJECT_ROOT, json.loads(SOURCE_PATH.read_bytes()))


def test_phase0_validators_fail_closed_on_tamper(
    attestations: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    lineage, source = attestations
    bad_lineage = deepcopy(lineage)
    bad_lineage["assertions"]["merge_commit_count_after_reviewed_checkpoint3"] = 1
    with pytest.raises(AttestationError, match="content hash mismatch"):
        validate_lineage_attestation(PROJECT_ROOT, bad_lineage)
    bad_lineage["attestation_sha256"] = sha256_json(
        {key: value for key, value in bad_lineage.items() if key != "attestation_sha256"}
    )
    with pytest.raises(AttestationError, match="does not match exact Git objects"):
        validate_lineage_attestation(PROJECT_ROOT, bad_lineage)

    bad_source = deepcopy(source)
    bad_source["assertions"]["all_replay_affecting_files_byte_identical"] = False
    with pytest.raises(AttestationError, match="content hash mismatch"):
        validate_replay_source_manifest(PROJECT_ROOT, bad_source)
    bad_source["manifest_sha256"] = sha256_json(
        {key: value for key, value in bad_source.items() if key != "manifest_sha256"}
    )
    with pytest.raises(AttestationError, match="does not match exact Git objects"):
        validate_replay_source_manifest(PROJECT_ROOT, bad_source)
