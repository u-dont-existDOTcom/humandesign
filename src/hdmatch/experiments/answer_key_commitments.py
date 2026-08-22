"""Canonical public commitments derived during authenticated answer-key reveal."""

from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import UTC, date, datetime
from typing import Any

from .canonical import sha256_json
from .manifest import SHA256_PATTERN


def generation_seed_commitment(secret_seed: int) -> str:
    """Commit to a synthetic generation seed without publishing the seed."""

    if isinstance(secret_seed, bool) or not isinstance(secret_seed, int) or secret_seed < 0:
        raise ValueError("synthetic generation seed must be a non-negative integer")
    return sha256_json(
        {
            "schema_version": "synthetic-generation-seed-commitment-v1",
            "generation_seed": secret_seed,
        }
    )


def revealed_local_date_set_hash(
    keyed_cases: Mapping[str, Mapping[str, Any]],
) -> str:
    """Hash the case/date truth already exposed by known-month evaluation reports."""

    targets: list[tuple[str, str]] = []
    for case_id in sorted(keyed_cases):
        raw_date = keyed_cases[case_id].get("true_local_date")
        if not isinstance(raw_date, str):
            raise ValueError(f"answer key case {case_id} lacks true_local_date")
        try:
            parsed = date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ValueError(f"answer key case {case_id} true_local_date is invalid") from exc
        if parsed.isoformat() != raw_date:
            raise ValueError(f"answer key case {case_id} true_local_date is not canonical")
        targets.append((case_id, raw_date))
    if not targets:
        raise ValueError("answer key contains no cases")
    return sha256_json(
        {
            "schema_version": "revealed-local-date-set-v1",
            "targets": targets,
        }
    )


def revealed_target_set_hash(
    keyed_cases: Mapping[str, Mapping[str, Any]],
) -> str | None:
    """Hash exact concealed targets while excluding experiment/model identity."""

    extended = [
        "true_utc" in item or "true_chart_features_hash" in item for item in keyed_cases.values()
    ]
    if not any(extended):
        return None
    if not all(
        "true_utc" in item and "true_chart_features_hash" in item for item in keyed_cases.values()
    ):
        raise ValueError("answer key cases must all include true_utc and true_chart_features_hash")
    targets: list[tuple[str, str, str, str]] = []
    for case_id in sorted(keyed_cases):
        item = keyed_cases[case_id]
        raw_utc = item.get("true_utc")
        if not isinstance(raw_utc, str):
            raise ValueError(f"answer key case {case_id} true_utc is invalid")
        try:
            parsed_utc = datetime.fromisoformat(raw_utc.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"answer key case {case_id} true_utc is invalid") from exc
        if parsed_utc.tzinfo is None or parsed_utc.utcoffset() is None:
            raise ValueError(f"answer key case {case_id} true_utc must be timezone-aware")
        canonical_utc = parsed_utc.astimezone(UTC).isoformat().replace("+00:00", "Z")
        if canonical_utc != raw_utc:
            raise ValueError(f"answer key case {case_id} true_utc is not canonical UTC")

        raw_date = item.get("true_local_date")
        if not isinstance(raw_date, str):
            raise ValueError(f"answer key case {case_id} true_local_date is invalid")
        try:
            parsed_date = date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ValueError(f"answer key case {case_id} true_local_date is invalid") from exc
        if parsed_date.isoformat() != raw_date:
            raise ValueError(f"answer key case {case_id} true_local_date is not canonical")

        chart_hash = item.get("true_chart_features_hash")
        if not isinstance(chart_hash, str) or re.fullmatch(SHA256_PATTERN, chart_hash) is None:
            raise ValueError(f"answer key case {case_id} true_chart_features_hash must be SHA-256")
        targets.append((case_id, canonical_utc, raw_date, chart_hash))
    return sha256_json(
        {
            "schema_version": "revealed-target-set-v1",
            "targets": targets,
        }
    )


def answer_key_case_mapping(answer_key: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Return a duplicate-free case map suitable for commitment derivation."""

    raw_cases = answer_key.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("answer key must contain a non-empty case list")
    cases: dict[str, Mapping[str, Any]] = {}
    for item in raw_cases:
        if not isinstance(item, Mapping):
            raise ValueError("answer key cases must be objects")
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("answer key case_id must be a non-empty string")
        if case_id in cases:
            raise ValueError(f"answer key contains duplicate case_id {case_id!r}")
        cases[case_id] = item
    return cases
