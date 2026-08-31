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
ARTIFACT_PATH = (
    PROJECT_ROOT / "state" / "NATAL-TIME-CHECKPOINT5-REPLAY-DELTA-ATTESTATION.json"
)


def _load_audit_module() -> ModuleType:
    path = PROJECT_ROOT / "scripts" / "audit_natal_time_checkpoint5_replay_delta.py"
    spec = importlib.util.spec_from_file_location(
        "audit_natal_time_checkpoint5_replay_delta", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = _load_audit_module()


@pytest.fixture(scope="module")
def attestation() -> dict[str, Any]:
    return AUDIT.build_replay_delta_attestation(PROJECT_ROOT)


def test_route_a_is_established_by_the_only_replay_delta(
    attestation: dict[str, Any],
) -> None:
    assert attestation["route_decision"]["route"] == "A_equivalence_proof"
    assert attestation["route_decision"]["route_a_established"] is True
    assert attestation["route_decision"]["route_b_regeneration_required"] is False
    delta = attestation["replay_source_delta"]
    assert delta["changed_replay_affecting_paths"] == [AUDIT.REPLAY_PATH]
    assert [item["symbol"] for item in delta["changed_replay_definitions"]] == [
        "_load_json_object"
    ]
    changed = delta["changed_replay_definitions"][0]
    assert changed["category"] == "resumption_durability_orchestration_only"
    assert changed["successful_path_mechanically_equivalent"] is True
    assert changed["receipt_semantic_construction_changed"] is False


def test_every_semantic_surface_and_frozen_input_is_unchanged(
    attestation: dict[str, Any],
) -> None:
    categories = {
        item["category"] for item in attestation["receipt_semantic_surface_evidence"]
    }
    assert categories == {
        "scientific_engine_input",
        "fixture_definition",
        "event_interval_construction",
        "receipt_semantic_construction",
        "canonical_serialization",
        "digest_construction",
        "independent_verification",
    }
    assert all(
        item["ast_identical_across_all_sources"]
        for item in attestation["receipt_semantic_surface_evidence"]
    )
    assert all(item["byte_identical_across_all_sources"] for item in attestation["frozen_inputs"])
    changed_paths = [
        item
        for pair in attestation["pairwise_changed_path_classification"]
        for item in pair["changed_paths"]
    ]
    assert all(item["category"] in AUDIT.PRO_CATEGORIES for item in changed_paths)
    replay_changes = [item for item in changed_paths if item["path"] == AUDIT.REPLAY_PATH]
    assert len(replay_changes) == 1
    assert replay_changes[0]["category"] == "resumption_durability_orchestration_only"


def test_acceptance_validator_reproduces_receipts_index_and_mutation_failure(
    attestation: dict[str, Any],
) -> None:
    evidence = attestation["acceptance_source_validation"]
    assert evidence["receipt_count"] == 9
    assert evidence["all_nine_receipts_valid"] is True
    assert evidence["rebuilt_index_byte_equivalent"] is True
    assert evidence["acceptance_runtime_surface_matches_git_source"] is True
    assert evidence["index_byte_identical_evaluated_through_acceptance"] is True
    assert evidence["index_sha256"] == (
        "f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435"
    )
    assert evidence["aggregate_sha256"] == (
        "ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665"
    )
    mutation = evidence["semantic_input_mutation_probe"]
    assert mutation["receipt_self_hash_recomputed_after_mutation"] is True
    assert mutation["acceptance_validator_rejected"] is True
    assert mutation["failure"] == "replay receipt fixture input mismatch"


def test_saved_attestation_reproduces_and_rejects_rehashed_tamper(
    attestation: dict[str, Any],
) -> None:
    saved = json.loads(ARTIFACT_PATH.read_bytes())
    assert saved == attestation
    assert ARTIFACT_PATH.read_bytes() == canonical_json_bytes(attestation) + b"\n"
    AUDIT.validate_replay_delta_attestation(PROJECT_ROOT, saved)
    tampered = deepcopy(attestation)
    tampered["route_decision"]["route_b_regeneration_required"] = True
    tampered["attestation_sha256"] = sha256_json(
        {key: value for key, value in tampered.items() if key != "attestation_sha256"}
    )
    with pytest.raises(AUDIT.ReplayDeltaError, match="does not reproduce exactly"):
        AUDIT.validate_replay_delta_attestation(PROJECT_ROOT, tampered)
