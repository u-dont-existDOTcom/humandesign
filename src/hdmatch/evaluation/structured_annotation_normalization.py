"""Deterministic normalization for raw structured-annotation model output.

Raw LLM output should be retained and hashed separately. This module only parses schema-valid
JSON objects and emits the canonical JSONL bytes used by downstream immutable artifacts.
It performs no substantive recoding, repair, inference, or target-theory-aware transformation.
"""

from __future__ import annotations

import json
from typing import Any, cast

from hdmatch.experiments.canonical import canonical_json_bytes

from .structured_annotation_v2 import StructuredAnnotationResponseV2


def _decode_json_object_stream(data: bytes) -> tuple[dict[str, Any], ...]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("raw structured annotation output is not UTF-8") from exc

    decoder = json.JSONDecoder()
    position = 0
    values: list[dict[str, Any]] = []
    while position < len(text):
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            break
        try:
            value, end = decoder.raw_decode(text, position)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"raw structured annotation contains invalid JSON near character {position}"
            ) from exc
        if not isinstance(value, dict):
            raise ValueError("raw structured annotation entries must be JSON objects")
        values.append(cast(dict[str, Any], value))
        position = end
    return tuple(values)


def normalize_structured_annotation_responses_jsonl_v2(data: bytes) -> bytes:
    """Parse raw JSON-object output and emit canonical schema-valid V2 response JSONL.

    Objects may be compact JSONL or pretty-printed/whitespace-separated JSON objects. The
    function refuses malformed objects and duplicate episode/observable units. It does not fix
    invalid substantive values or fill missing fields; Pydantic validation must succeed as-is.
    """

    responses: list[StructuredAnnotationResponseV2] = []
    unit_keys: set[tuple[str, str, str]] = set()
    for object_number, value in enumerate(_decode_json_object_stream(data), start=1):
        response = StructuredAnnotationResponseV2.model_validate(value)
        key = (response.task_id, response.episode_id, response.observable_id)
        if key in unit_keys:
            raise ValueError(
                "raw structured annotation repeats task/episode/observable unit "
                f"at object {object_number}"
            )
        unit_keys.add(key)
        responses.append(response)
    return b"\n".join(canonical_json_bytes(response) for response in responses) + (
        b"\n" if responses else b""
    )
