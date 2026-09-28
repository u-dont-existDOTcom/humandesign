#!/usr/bin/env python3
"""Descriptive comparison of Life Patterns collection modes.

This is measurement instrumentation, not a validity test. It compares source
richness/burden proxies, clarification burden and inference usage while keeping
collection mode explicit. No LLM or network call is made.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

MODES = {"railway_text", "chatgpt_voice", "chatgpt_text", "mixed", "unknown"}


def words(value: str | None) -> int:
    return len((value or "").split())


def percentile(values: list[int], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    location = (len(ordered) - 1) * fraction
    lower = int(location)
    upper = min(lower + 1, len(ordered) - 1)
    weight = location - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def mode(record: dict[str, Any]) -> str:
    value = record.get("collection_mode")
    if value in MODES:
        return value
    modes = {
        source.get("source_mode")
        for source in record.get("source_records", [])
        if isinstance(source, dict) and source.get("source_mode") in MODES
    }
    modes.discard("unknown")
    return next(iter(modes)) if len(modes) == 1 else "mixed" if len(modes) > 1 else "unknown"


def source_kind(turn: dict[str, Any]) -> str:
    source = str(turn.get("turn_source") or "")
    if source.startswith("import-"):
        return "imported"
    if source == "railway_participant":
        return "railway"
    return "other"


def summarize(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    turns = [turn for turn in record.get("turns", []) if isinstance(turn, dict)]
    behavioral_turns = [
        turn for turn in turns if turn.get("turn_role", "behavioral") == "behavioral"
    ]
    answered = [turn for turn in behavioral_turns if isinstance(turn.get("answer_text"), str)]
    answer_words = [words(turn.get("answer_text")) for turn in answered]
    imported = [turn for turn in behavioral_turns if source_kind(turn) == "imported"]
    railway = [turn for turn in behavioral_turns if source_kind(turn) == "railway"]
    evidence_authority = str(record.get("evidence_authority") or "unknown")
    evidence = [
        item
        for item in record.get("neutral_evidence", [])
        if isinstance(item, dict)
        and item.get("review_status") != "superseded_by_participant_correction"
    ]
    facets = {
        facet
        for item in evidence
        for facet in item.get("candidate_facet_ids", [])
        if isinstance(facet, str)
    }
    routes = {
        turn.get("canonical_question_id")
        for turn in behavioral_turns
        if isinstance(turn.get("canonical_question_id"), str)
    }
    conditions = sum(
        len(item.get("conditions") or [])
        for item in evidence
        if isinstance(item.get("conditions"), list)
    )
    corrections = sum(
        len(turn.get("corrections") or [])
        for turn in turns
        if isinstance(turn.get("corrections"), list)
    )
    calls = [call for call in record.get("model_call_telemetry", []) if isinstance(call, dict)]
    prompt_tokens = sum(
        int(call.get("prompt_tokens") or 0)
        for call in calls
        if isinstance(call.get("prompt_tokens"), (int, float))
    )
    completion_tokens = sum(
        int(call.get("completion_tokens") or 0)
        for call in calls
        if isinstance(call.get("completion_tokens"), (int, float))
    )
    request_chars = sum(
        int(call.get("request_chars") or 0)
        for call in calls
        if isinstance(call.get("request_chars"), (int, float))
    )
    return {
        "file": path.name,
        "session_id": record.get("session_id"),
        "collection_mode": mode(record),
        "turns_total": len(behavioral_turns),
        "metadata_turns": len(turns) - len(behavioral_turns),
        "answered_turns": len(answered),
        "imported_turns": len(imported),
        "railway_clarification_turns": len(railway),
        "participant_words_total": sum(answer_words),
        "answer_words_mean": round(statistics.mean(answer_words), 2) if answer_words else None,
        "answer_words_median": round(statistics.median(answer_words), 2) if answer_words else None,
        "answer_words_p25": round(percentile(answer_words, 0.25), 2) if answer_words else None,
        "answer_words_p75": round(percentile(answer_words, 0.75), 2) if answer_words else None,
        "evidence_authority": evidence_authority,
        "neutral_evidence_items": len(evidence),
        "railway_admitted_evidence_items": (
            len(evidence)
            if evidence_authority == "railway_independent_semantic_admission"
            else None
        ),
        "collector_unverified_evidence_items": (
            len(evidence) if evidence_authority == "chatgpt_collector_unverified" else None
        ),
        "unique_facets": len(facets),
        "canonical_routes_answered_or_presented": len(routes),
        "structured_conditions": conditions,
        "correction_links": corrections,
        "participant_review_confirmed": bool(record.get("participant_review", {}).get("confirmed")),
        "model_calls": len(calls),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "request_chars": request_chars,
        "review_status": record.get("review_status"),
        "interview_status": record.get("interview_status"),
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["collection_mode"]].append(row)

    output = {}
    metrics = (
        "participant_words_total",
        "answer_words_median",
        "railway_clarification_turns",
        "railway_admitted_evidence_items",
        "collector_unverified_evidence_items",
        "unique_facets",
        "correction_links",
        "model_calls",
        "prompt_tokens",
        "completion_tokens",
    )
    for group, members in sorted(groups.items()):
        output[group] = {"sessions": len(members)}
        for metric in metrics:
            values = [
                float(row[metric]) for row in members if isinstance(row.get(metric), (int, float))
            ]
            output[group][f"{metric}_mean"] = round(statistics.mean(values), 2) if values else None
            output[group][f"{metric}_median"] = (
                round(statistics.median(values), 2) if values else None
            )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exports", type=Path, nargs="+")
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    args = parser.parse_args()

    if (args.input_usd_per_million is None) != (args.output_usd_per_million is None):
        parser.error("Provide both token prices or neither.")

    rows = []
    for path in args.exports:
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise SystemExit(f"{path}: expected one JSON object")
        row = summarize(path, record)
        if args.input_usd_per_million is not None:
            row["estimated_model_usd"] = round(
                row["prompt_tokens"] * args.input_usd_per_million / 1_000_000
                + row["completion_tokens"] * args.output_usd_per_million / 1_000_000,
                6,
            )
        rows.append(row)

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted({key for row in rows for key in row}))
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "schema": "life-patterns-collection-mode-comparison-v1",
        "purpose": (
            "Descriptive whole-pipeline development comparison only. Collection mode can be "
            "confounded with participant/order/context and is not randomized evidence of equivalence. "
            "ChatGPT collector evidence is reported separately from Railway-admitted evidence."
        ),
        "sessions": rows,
        "by_collection_mode": aggregate(rows),
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sessions": len(rows), "csv": str(args.csv), "json": str(args.json)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
