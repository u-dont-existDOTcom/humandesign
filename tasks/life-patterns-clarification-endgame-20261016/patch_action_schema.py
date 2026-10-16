"""Deterministic additive OpenAPI extension for honest review progress."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = (
    ROOT
    / "reference/custom_gpt/releases/Life-Patterns-GPT-completed-interview-update-2026-10-15.zip"
)
OUT = ROOT / "apps/life-patterns-participant/participant/static/action-openapi.yaml"
SCHEMA = "ACTION-life-patterns-submission-openapi.yaml"


def build() -> bytes:
    with zipfile.ZipFile(BASE) as archive:
        contract = json.loads(archive.read(SCHEMA))
    assert contract["info"]["version"] == "1.6.0"
    status = contract["components"]["schemas"]["ReviewStatus"]
    assert status.get("additionalProperties") is False
    props = status["properties"]
    assert "clarification_progress" not in props
    contract["info"]["version"] = "1.6.1"
    contract["info"]["description"] = (
        "Asynchronous independent review and exact-source submission. "
        "Clarification batch counts are not overall interview remaining counts."
    )
    props["clarification_progress"] = {
        "type": "object",
        "description": (
            "Authoritative stage and answered-count bookkeeping. A current batch "
            "of one is NOT the last question in the interview; the number of "
            "future reviewer-admitted questions is unknown until status ready."
        ),
        "additionalProperties": False,
        "properties": {
            "stage": {"type": "string"},
            "clarifications_answered_or_skipped_total": {"type": "integer", "minimum": 0},
            "current_batch_question_count": {"type": "integer", "minimum": 0},
            "current_batch_only": {"type": "boolean"},
            "overall_clarifications_remaining": {"type": ["integer", "null"], "minimum": 0},
            "overall_remaining_known": {"type": "boolean"},
            "full_evidence_review_ready": {"type": "boolean"},
            "remaining_after_ready": {"type": "array", "items": {"type": "string"}},
            "participant_message": {"type": "string"},
        },
        "required": [
            "stage",
            "clarifications_answered_or_skipped_total",
            "current_batch_question_count",
            "current_batch_only",
            "overall_clarifications_remaining",
            "overall_remaining_known",
            "full_evidence_review_ready",
            "remaining_after_ready",
            "participant_message",
        ],
    }
    return (json.dumps(contract, indent=2, ensure_ascii=False) + "\n").encode()


def main():
    import sys

    value = build()
    if "--check" in sys.argv:
        assert OUT.read_bytes() == value, "Generated Action schema changed"
    else:
        OUT.write_bytes(value)
    print("PROGRESS_OPENAPI", "CHECKED" if "--check" in sys.argv else "BUILT", len(value))


if __name__ == "__main__":
    main()
