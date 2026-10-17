"""Create an exact-source, LOCAL-ONLY owner survey packet for the offline pilot.

No responses or personal source data belong in the git repository.
All input paths are supplied explicitly; originals are never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

SCHEMA = "life-patterns-owner-source-packet-v1"
SOURCES: dict[str, tuple[str, str]] = {
    "latest_v33": ("local_life_patterns_v3_3_pilot_unsubmitted", "v3.3 response export"),
    "primary_84": (
        "life-patterns-full-survey-participant-export-v2",
        "historical primary interview",
    ),
    "secondary_cf003": ("life-patterns-cf003-secondary-v0", "separately frozen follow-ups"),
}


def load_source(source_id: str, path: Path) -> dict[str, Any]:
    expected, label = SOURCES[source_id]
    raw = path.read_bytes()
    decoded = raw.decode("utf-8")
    data = json.loads(decoded)
    if not isinstance(data, dict) or data.get("schema") != expected:
        raise ValueError(f"Unexpected source schema for {source_id}")
    if source_id == "latest_v33" and (
        not isinstance(data.get("answers"), dict)
        or not isinstance(data.get("unique_behaviors"), list)
    ):
        raise ValueError("Incomplete V3.3 source structure")
    if source_id in ("primary_84", "secondary_cf003") and not isinstance(
        data.get("turns"), list
    ):
        raise ValueError(f"Missing original turns for {source_id}")
    return {
        "source_id": source_id,
        "label": label,
        "filename": path.name,
        "original_schema": expected,
        "byte_count": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "text": decoded,
    }


def build(
    *,
    latest_v33: Path,
    primary: Path,
    secondary: Path,
    output: Path,
) -> dict[str, Any]:
    sources = [
        load_source("latest_v33", latest_v33),
        load_source("primary_84", primary),
        load_source("secondary_cf003", secondary),
    ]
    packet = {
        "schema": SCHEMA,
        "status": "PRIVATE_LOCAL_ONLY_NOT_SUBMITTED_NOT_SCORED",
        "source_relation": "Separate original instruments preserved verbatim; do not deduplicate.",
        "usage": (
            "Import into the updated offline Experience and Meaning pilot "
            "as prior-source context."
        ),
        "no_new_experience_answers_imputed": True,
        "sources": sources,
    }
    assert all(
        hashlib.sha256(src["text"].encode("utf-8")).hexdigest() == src["sha256"]
        for src in sources
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    blob = (json.dumps(packet, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "wb") as dest:
            dest.write(blob)
    except BaseException:
        output.unlink(missing_ok=True)
        raise
    if json.loads(output.read_text(encoding="utf-8")) != packet:
        raise RuntimeError("Source packet serialization round trip failed")
    return {
        "sources": len(sources),
        "size": output.stat().st_size,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "source_counts": {
            "v33_answers": len(json.loads(sources[0]["text"])["answers"]),
            "unusual_behaviors": len(json.loads(sources[0]["text"])["unique_behaviors"]),
            "primary_turns": len(json.loads(sources[1]["text"])["turns"]),
            "secondary_turns": len(json.loads(sources[2]["text"])["turns"]),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latest-v33", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--secondary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(
        latest_v33=args.latest_v33,
        primary=args.primary,
        secondary=args.secondary,
        output=args.output,
    )
    print(json.dumps(result, sort_keys=True))
