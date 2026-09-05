from __future__ import annotations

import json

import pytest

from hdmatch.evaluation.structured_annotation_normalization import (
    normalize_structured_annotation_responses_jsonl_v2,
)
from hdmatch.evaluation.structured_annotation_v2 import StructuredAnnotationResponseV2
from hdmatch.experiments.canonical import canonical_json_bytes


def _payload(*, observable_id: str = "STRUCTURED_ALPHA") -> dict[str, object]:
    return {
        "schema_version": "life-patterns-structured-annotation-response-v2",
        "task_id": "TASK-A",
        "freeze_id": "BPF-0123456789ABCDEF0123",
        "freeze_sha256": "0" * 64,
        "ontology_artifact_id": "LPO-0123456789ABCDEF0123",
        "ontology_sha256": "1" * 64,
        "procedure_id": "LPSP-0123456789ABCDEF0123",
        "procedure_sha256": "2" * 64,
        "episode_id": "EP-A",
        "observable_id": observable_id,
        "state": "observed",
        "coded_values": ["VALUE_ONE"],
        "value_relation": "single",
        "asserts_non_action": False,
        "non_action_gate": None,
        "supporting_source_turn_ids": ["TURN-A"],
        "counterevidence_source_turn_ids": [],
        "context_qualifiers": [],
        "life_phase_qualifier": None,
        "language": "en",
        "influence_relation": "none_reported",
        "influence_source_turn_ids": [],
        "theory_exposure": "none_detected",
        "annotation_note": None,
        "person_level_contradiction_or_mixed_not_encoded_here": True,
    }


def test_noncanonical_but_schema_valid_raw_json_is_normalized_deterministically() -> None:
    payload = _payload()
    raw = (json.dumps(payload, indent=2) + "\n").encode()
    normalized = normalize_structured_annotation_responses_jsonl_v2(raw)
    response = StructuredAnnotationResponseV2.model_validate(payload)
    assert normalized == canonical_json_bytes(response) + b"\n"
    assert normalized != raw


def test_normalization_refuses_substantive_schema_repairs() -> None:
    payload = _payload()
    payload["coded_values"] = []
    raw = (json.dumps(payload) + "\n").encode()
    with pytest.raises(ValueError, match="observed structured annotations require coded values"):
        normalize_structured_annotation_responses_jsonl_v2(raw)


def test_normalization_refuses_duplicate_units() -> None:
    raw_line = json.dumps(_payload())
    raw = f"{raw_line}\n{raw_line}\n".encode()
    with pytest.raises(ValueError, match="repeats task/episode/observable unit"):
        normalize_structured_annotation_responses_jsonl_v2(raw)
