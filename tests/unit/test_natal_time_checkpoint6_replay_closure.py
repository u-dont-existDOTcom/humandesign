from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from hdmatch.util import sha256_json
from scripts.audit_natal_time_checkpoint6_replay_closure import (
    ACCEPTANCE_SOURCE,
    IMPLEMENTATION_SOURCE,
    SUBMISSION_DOC,
    SUBMISSION_SOURCE,
    RouteBRequiredError,
    _assert_unchanged_replay_bytes,
    build_replay_closure,
    validate_replay_closure,
)

PROJECT_ROOT = Path(__file__).parents[2]
ARTIFACT = PROJECT_ROOT / "state/NATAL-TIME-CHECKPOINT6-FINAL-REPLAY-SOURCE-CLOSURE.json"


@pytest.fixture(scope="module")
def closure_payload() -> dict[str, Any]:
    return build_replay_closure(PROJECT_ROOT)


def test_exact_anchor_chain_and_documentation_only_submission(
    closure_payload: dict[str, Any],
) -> None:
    payload = closure_payload

    assert payload["anchors"]["checkpoint5_acceptance_source"]["commit"] == ACCEPTANCE_SOURCE
    assert payload["anchors"]["checkpoint6_implementation_source"]["commit"] == (
        IMPLEMENTATION_SOURCE
    )
    assert payload["anchors"]["checkpoint6_submission_source"]["commit"] == (
        SUBMISSION_SOURCE
    )
    assert payload["anchors"]["checkpoint6_submission_source"]["parents"] == [
        IMPLEMENTATION_SOURCE
    ]
    assert payload["submission_documentation_only_delta"] == [
        {"status": "A", "path": SUBMISSION_DOC}
    ]


def test_all_replay_files_and_functions_close_at_implementation_head(
    closure_payload: dict[str, Any],
) -> None:
    payload = closure_payload

    assert payload["replay_affecting_file_count"] == 58
    assert payload["semantic_function_count"] == 28
    assert payload["acceptance_to_implementation_delta"][
        "replay_affecting_intersection"
    ] == []
    assert all(
        record["byte_identical_acceptance_implementation_submission"]
        for record in payload["replay_affecting_file_inventory"]
    )
    assert all(
        record["ast_identical_acceptance_implementation_submission"]
        for record in payload["semantic_function_inventory"]
    )


def test_every_replay_file_mutation_forces_route_b(
    closure_payload: dict[str, Any],
) -> None:
    payload = closure_payload

    assert payload["semantic_byte_mutation_probe_count"] == 58
    assert all(item["route_b_required"] for item in payload["semantic_byte_mutation_probes"])
    with pytest.raises(RouteBRequiredError, match="replay-affecting byte changed"):
        _assert_unchanged_replay_bytes("probe", b"accepted", b"changed")


def test_receipts_index_and_semantic_mutation_validate_at_implementation(
    closure_payload: dict[str, Any],
) -> None:
    validation = closure_payload["implementation_source_validation"]

    assert validation["receipt_count"] == 9
    assert validation["all_nine_receipts_valid"] is True
    assert validation["rebuilt_index_byte_equivalent"] is True
    assert validation["index_sha256"] == (
        "f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435"
    )
    assert validation["aggregate_sha256"] == (
        "ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665"
    )
    assert validation["semantic_input_mutation_probe"]["failure"] == (
        "replay receipt fixture input mismatch"
    )


def test_saved_closure_reproduces_and_rehashed_tamper_fails() -> None:
    saved = json.loads(ARTIFACT.read_bytes())

    validate_replay_closure(PROJECT_ROOT, saved)
    assert saved == build_replay_closure(PROJECT_ROOT)

    tampered = json.loads(ARTIFACT.read_bytes())
    tampered["assertions"]["no_replay_receipt_relabeling"] = False
    unhashed = dict(tampered)
    unhashed.pop("closure_sha256")
    tampered["closure_sha256"] = sha256_json(unhashed)
    with pytest.raises(ValueError, match="does not reproduce exactly"):
        validate_replay_closure(PROJECT_ROOT, tampered)


def test_prior_attestation_and_receipt_bytes_are_preserved(
    closure_payload: dict[str, Any],
) -> None:
    payload = closure_payload

    assert payload["prior_checkpoint5_attestation"]["preserved_not_overwritten"] is True
    assert payload["assertions"]["prior_attestation_and_receipts_preserved"] is True
    assert payload["assertions"]["no_replay_receipt_relabeling"] is True
