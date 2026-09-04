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


def normalize_structured_annotation_responses_jsonl_v2(data: bytes) -> bytes:
    """Parse raw JSONL and emit canonical schema-valid V2 response JSONL.

    The function refuses malformed objects and duplicate episode/observable units. It does not
    fix invalid substantive values or fill missing fields; Pydantic validation must succeed as-is.
    """

    responses: list[StructuredAnnotationResponseV2] = []
    unit_keys: set[tuple[str, str, str]] = set()
    for line_number, raw_line in enumerate(data.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value: Any = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"raw structured annotation line {line_number} is invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"raw structured annotation line {line_number} is not a JSON object")
        response = StructuredAnnotationResponseV2.model_validate(cast(dict[str, Any], value))
        key = (response.task_id, response.episode_id, response.observable_id)
        if key in unit_keys:
            raise ValueError(
                f"raw structured annotation repeats task/episode/observable unit on line {line_number}"
            )
        unit_keys.add(key)
        responses.append(response)
    return b"\n".join(canonical_json_bytes(response) for response in responses) + (
        b"\n" if responses else b""
    )
