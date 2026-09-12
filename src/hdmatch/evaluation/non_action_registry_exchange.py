"""Deterministic import/normalization for theory-blind non-action classification output."""

from __future__ import annotations

import json
from typing import Any

from hdmatch.experiments.canonical import canonical_json_bytes

from .non_action_registry import NonActionClassificationDecision


def parse_non_action_classification_output(
    data: bytes,
) -> tuple[NonActionClassificationDecision, ...]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("non-action classification output is not UTF-8") from exc

    decoder = json.JSONDecoder()
    position = 0
    decisions: list[NonActionClassificationDecision] = []
    keys: set[tuple[str, str]] = set()
    while position < len(text):
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            break
        try:
            value: Any
            value, end = decoder.raw_decode(text, position)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"non-action classification output contains invalid JSON near character {position}"
            ) from exc
        if not isinstance(value, dict):
            raise ValueError("non-action classification entries must be JSON objects")
        decision = NonActionClassificationDecision.model_validate(value)
        key = (decision.observable_id, decision.subcode_id)
        if key in keys:
            raise ValueError(f"non-action classification output repeats decision: {key}")
        keys.add(key)
        decisions.append(decision)
        position = end
    return tuple(decisions)


def normalize_non_action_classification_jsonl(data: bytes) -> bytes:
    decisions = parse_non_action_classification_output(data)
    return b"\n".join(canonical_json_bytes(row) for row in decisions) + (
        b"\n" if decisions else b""
    )
