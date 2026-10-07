"""Value-free API diagnostics: never return input values, unknown keys, or Pydantic ctx."""

from __future__ import annotations

import secrets
from typing import Any

# Only server-declared protocol identifiers may appear in a diagnostic path.
SAFE_FIELDS = frozenset(
    {
        "body",
        "path",
        "query",
        "header",
        "research_use_consented",
        "request_id",
        "candidate_record",
        "review_id",
        "primary_record",
        "cf003_record",
        "primary_record_json",
        "cf003_record_json",
        "answer_text",
        "clarification_id",
        "operation_id",
        "skipped",
        "action",
        "claim_id",
        "candidate_sha256",
        "status",
        "worker_state",
        "receipt",
        "clarification",
        "error",
        "schema",
        "turns",
        "turn_id",
        "question_text",
        "canonical_question_id",
        "turn_role",
        "consent",
        "freeze",
        "record_state",
        "frozen_before_birth_or_chart_reveal",
        "collection_mode",
        "participant_review",
        "summary_shown",
        "confirmed",
    }
)
HINTS = {
    "model_attributes_type": "Send the request as a JSON object with Content-Type: application/json, not a string or raw non-JSON body.",
    "model_type": "Send a JSON object for this request, not a string or list.",
    "missing": "Required field is missing.",
    "extra_forbidden": "An undeclared request field was supplied. Keep the source backup; check the published request envelope.",
    "string_type": "This protocol field must be a string.",
    "string_too_short": "Identifier must contain at least 16 characters; generate uuid.uuid4().hex for a new operation.",
    "string_too_long": "Field exceeds its published maximum length; never truncate a participant answer to repair it.",
    "string_pattern_mismatch": "Use the identifier format in the schema. New request/operation IDs allow only letters, digits, underscore and hyphen.",
    "dict_type": "Send a JSON object here, not a JSON-encoded string or list.",
    "list_type": "Send a JSON array here.",
    "bool_type": "Use a JSON boolean, not a consent sentence.",
    "literal_error": "Value must match the published choices. Never invent consent or review completion to satisfy validation.",
    "json_invalid": "The request is not valid JSON. Preserve the original record and repair serialization only.",
}


def safe_validation_diagnostic(errors: list[dict[str, Any]]) -> dict[str, Any]:
    fields = []
    for item in errors[:12]:
        path = []
        for part in item.get("loc", ()):
            if isinstance(part, int):
                path.append("[]")  # offsets and user-controlled dictionary keys are not echoed
            elif part in SAFE_FIELDS:
                path.append(part)
            else:
                path.append("<unrecognized-field>")
        code = item.get("type", "invalid_field")
        if code not in HINTS:
            code = "invalid_field"
        json_record_transport = any(
            part in {"primary_record_json", "cf003_record_json"} for part in path
        )
        hint = HINTS.get(code, "Check this field against the published schema.")
        if json_record_transport:
            hint = {
                "missing": (
                    "The exact frozen record JSON string is missing. Use the corresponding "
                    "saved record; never reconstruct or summarize it."
                ),
                "json_invalid": (
                    "This field must contain one valid raw JSON object string, without "
                    "markdown fences or truncation. Preserve all source words."
                ),
                "dict_type": (
                    "This string must decode to one complete JSON object, not a list or "
                    "scalar. Preserve the exact frozen record."
                ),
                "string_too_long": (
                    "The exact record exceeds the published transport limit. Never truncate "
                    "it; keep the file intact and report the diagnostic."
                ),
            }.get(code, hint)
        fields.append(
            {
                "path": ".".join(path),
                "code": code,
                "hint": hint,
            }
        )
    summary = "; ".join(f"{field['path']}: {field['code']}" for field in fields[:3])
    return {
        "detail": f"Invalid request fields ({summary}). Rejected before storage; no existing record was changed.",
        "code": "request_validation_failed",
        "diagnostic_id": "V-" + secrets.token_hex(12),
        "errors": fields,
        "additional_errors": max(0, len(errors) - len(fields)),
        "request_accepted": False,
        "next_action": "Keep the exact candidate backup and give the participant this diagnostic. Correct only the listed envelope/serialization fields, preserve all source words, and retry with genuine recorded consent.",
    }
