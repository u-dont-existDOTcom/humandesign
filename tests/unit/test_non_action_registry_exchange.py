from __future__ import annotations

import json

import pytest

from hdmatch.evaluation.non_action_registry import NonActionClassificationDecision
from hdmatch.evaluation.non_action_registry_exchange import (
    normalize_non_action_classification_jsonl,
    parse_non_action_classification_output,
)
from hdmatch.experiments.canonical import canonical_json_bytes


def _decision() -> dict[str, str]:
    return {
        "observable_id": "NBM-R01",
        "subcode_id": "R01-a",
        "classification": "not_non_action",
        "rationale": "Synthetic structural rationale.",
    }


def test_pretty_json_object_is_parsed_and_normalized() -> None:
    raw = (json.dumps(_decision(), indent=2) + "\n").encode()
    decisions = parse_non_action_classification_output(raw)
    assert len(decisions) == 1
    expected = NonActionClassificationDecision.model_validate(_decision())
    assert decisions == (expected,)
    assert normalize_non_action_classification_jsonl(raw) == canonical_json_bytes(expected) + b"\n"


def test_duplicate_decision_is_rejected() -> None:
    line = json.dumps(_decision())
    with pytest.raises(ValueError, match="repeats decision"):
        parse_non_action_classification_output(f"{line}\n{line}\n".encode())


def test_extra_fields_are_not_silently_accepted() -> None:
    value = _decision()
    value["unexpected"] = "NOPE"
    with pytest.raises(ValueError):
        parse_non_action_classification_output(json.dumps(value).encode())
