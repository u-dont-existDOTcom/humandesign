"""Project the pinned development bank without its researcher-only mappings.

No question wording is authored here. Source JSON and object hashes remain in
this task directory; only the explicit whitelist reaches the participant app.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
SOURCE = TASK / "source/adaptive-v3-original.json"
OUTPUT = ROOT / "apps/life-patterns-participant/participant/static/shared-life-topics-v3.json"
MANIFEST = TASK / "SHARED-EVIDENCE-PROJECTION.json"
SOURCE_SHA256 = "fec3d0d18b9463d29842e65c4759fd7ed900a019889531896f89c1b3764e0084"
VERSION = "shared-life-topics-v3-20261026"
TOPIC_KEYS = (
    "id",
    "label",
    "question",
    "optional_followup",
    "conditional_new_probe_ids",
    "eligibility",
    "followup_gate",
    "response_state_options",
    "answer_capture",
)
PROBE_KEYS = ("id", "question", "followup", "related_topics")


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def object_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def contents() -> tuple[dict, dict]:
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("The pinned shared question source changed.")
    source = json.loads(raw)
    if len(source["questions"]) != 23 or len(source["optional_microprobes"]) != 7:
        raise ValueError("The original 23 topics and seven probes must be preserved.")
    result = {
        "schema": "life-patterns-shared-evidence-instrument-v1",
        "version": VERSION,
        "status": "development_optional_unscored",
        **{
            key: source[key]
            for key in (
                "consent_rule",
                "max_base_optional_topics_per_session",
                "max_additional_conditional_probes_per_session",
                "decline_all_allowed",
                "evidence_state_codes",
            )
        },
        "questions": [{key: item[key] for key in TOPIC_KEYS} for item in source["questions"]],
        "optional_microprobes": [
            {key: item[key] for key in PROBE_KEYS} for item in source["optional_microprobes"]
        ],
    }
    provenance = {
        "schema": "life-patterns-shared-evidence-projection-provenance-v1",
        "source_commit": "7971b3c1564d9c38bce17abe4c4575affcba2c76",
        "source_path": (
            "tasks/life-patterns-external-questionnaire-merge-20261021/"
            "LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json"
        ),
        "source_sha256": SOURCE_SHA256,
        "projection_sha256": hashlib.sha256(encoded(result)).hexdigest(),
        "projection_version": VERSION,
        "source_status": source["status"],
        "participant_wording_changed": False,
        "topic_whitelist": list(TOPIC_KEYS),
        "probe_whitelist": list(PROBE_KEYS),
        "objects": [
            {
                "id": item["id"],
                "kind": kind,
                "source_object_sha256": object_hash(item),
                "question_sha256": hashlib.sha256(item["question"].encode("utf-8")).hexdigest(),
                "followup_sha256": hashlib.sha256(item[followup].encode("utf-8")).hexdigest(),
            }
            for kind, rows, followup in (
                ("topic", source["questions"], "optional_followup"),
                ("probe", source["optional_microprobes"], "followup"),
            )
            for item in rows
        ],
        "limits": [
            "Projection is an engineering preservation check, not neutral measurement validation.",
            "Source mappings and object hashes are researcher-side provenance, "
            "never interview input.",
            "The existing optional development candidate remains unscored.",
        ],
    }
    return result, provenance


def main() -> None:
    result, provenance = contents()
    OUTPUT.write_bytes(encoded(result))
    MANIFEST.write_bytes(encoded(provenance))


if __name__ == "__main__":
    main()
