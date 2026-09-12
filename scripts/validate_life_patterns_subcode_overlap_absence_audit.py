#!/usr/bin/env python3
"""Mechanically validate the theory-blind subcode overlap/absence audit artifacts.

This validator checks transport/schema/internal consistency only. It does not judge substantive
measurement conclusions and must not be used as a substitute for the fresh theory-blind audit.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

FINDING_KEYS = {
    "finding_id",
    "observable_id",
    "subcode_ids",
    "finding_type",
    "classification",
    "exact_issue",
    "human_coding_consequence",
    "recommended_disposition",
    "confidence",
}
SUMMARY_KEYS = {
    "schema_version",
    "observables_reviewed",
    "material_findings",
    "presentation_only_count",
    "response_contract_limitation_count",
    "substantive_codebook_overlap_count",
    "no_change_needed_count",
    "r05_disposition",
    "human_calibration_safe_to_start_without_revision",
    "blocking_findings",
    "notes",
}
FINDING_TYPES = {
    "semantic_relation",
    "facet_structure",
    "absence_structure",
    "response_contract",
    "double_count_risk",
}
SEMANTIC_RELATIONS = {
    "distinct_mutually_exclusive",
    "distinct_can_cooccur",
    "sequential_can_cooccur",
    "nested_or_subset",
    "partial_overlap",
    "near_duplicate",
    "boundary_unclear",
}
ABSENCE_STRUCTURES = {
    "pure_absence",
    "affirmative_plus_absence_condition",
    "resolved_hybrid",
    "classification_boundary_unclear",
}
CONSEQUENCE_CLASSES = {
    "presentation_only",
    "response_contract_limitation",
    "substantive_codebook_overlap",
    "no_change_needed",
}
DISPOSITIONS = {
    "presentation_only",
    "response_contract_change",
    "versioned_codebook_clarification",
    "no_change",
}
CONFIDENCE = {"high", "medium", "low"}
SUMMARY_DISPOSITIONS = {
    "presentation_only",
    "response_contract_change",
    "versioned_codebook_clarification",
    "no_change",
}
OBSERVABLE_IDS = {f"NBM-R{i:02d}" for i in range(1, 23)}
FINDING_ID_RE = re.compile(r"^OA-(\d{3})$")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: invalid JSON on line {line_number}: {exc}") from exc
        _require(isinstance(value, dict), f"{path}: line {line_number} must be one JSON object")
        rows.append(value)
    _require(rows, f"{path}: findings JSONL is empty")
    return rows


def _validate_finding(row: dict[str, Any], expected_index: int) -> None:
    _require(set(row) == FINDING_KEYS, f"finding {expected_index}: exact field set mismatch")
    match = FINDING_ID_RE.fullmatch(str(row["finding_id"]))
    _require(match is not None, f"finding {expected_index}: invalid finding_id")
    _require(int(match.group(1)) == expected_index, f"finding IDs must be sequential; expected OA-{expected_index:03d}")
    _require(row["observable_id"] in OBSERVABLE_IDS, f"{row['finding_id']}: invalid observable_id")
    _require(isinstance(row["subcode_ids"], list) and row["subcode_ids"], f"{row['finding_id']}: subcode_ids must be a nonempty list")
    _require(all(isinstance(v, str) and v for v in row["subcode_ids"]), f"{row['finding_id']}: invalid subcode_ids")
    _require(row["finding_type"] in FINDING_TYPES, f"{row['finding_id']}: invalid finding_type")
    allowed_classifications = (
        SEMANTIC_RELATIONS
        if row["finding_type"] == "semantic_relation"
        else ABSENCE_STRUCTURES
        if row["finding_type"] == "absence_structure"
        else CONSEQUENCE_CLASSES
    )
    _require(row["classification"] in allowed_classifications, f"{row['finding_id']}: invalid classification for finding_type")
    _require(row["recommended_disposition"] in DISPOSITIONS, f"{row['finding_id']}: invalid recommended_disposition")
    _require(row["confidence"] in CONFIDENCE, f"{row['finding_id']}: invalid confidence")
    for key in ("exact_issue", "human_coding_consequence"):
        _require(isinstance(row[key], str) and row[key].strip(), f"{row['finding_id']}: {key} must be nonempty")


def _validate_summary(summary: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    _require(set(summary) == SUMMARY_KEYS, "summary: exact field set mismatch")
    _require(summary["schema_version"] == "life-patterns-subcode-overlap-absence-audit-v1", "summary: wrong schema_version")
    _require(summary["observables_reviewed"] == 22, "summary: observables_reviewed must be 22")
    _require(summary["material_findings"] == len(findings), "summary: material_findings does not equal JSONL row count")
    _require(summary["r05_disposition"] in SUMMARY_DISPOSITIONS, "summary: invalid r05_disposition")
    _require(isinstance(summary["human_calibration_safe_to_start_without_revision"], bool), "summary: safety flag must be boolean")
    _require(isinstance(summary["blocking_findings"], list), "summary: blocking_findings must be a list")
    finding_ids = {row["finding_id"] for row in findings}
    _require(all(item in finding_ids for item in summary["blocking_findings"]), "summary: blocking_findings contains an unknown finding ID")
    _require(isinstance(summary["notes"], str) and summary["notes"].strip(), "summary: notes must be nonempty")

    disposition_counts = Counter(row["recommended_disposition"] for row in findings)
    expected = {
        "presentation_only_count": disposition_counts["presentation_only"],
        "response_contract_limitation_count": disposition_counts["response_contract_change"],
        "substantive_codebook_overlap_count": disposition_counts["versioned_codebook_clarification"],
        "no_change_needed_count": disposition_counts["no_change"],
    }
    for key, value in expected.items():
        _require(summary[key] == value, f"summary: {key} should be {value}, got {summary[key]!r}")
    _require(sum(expected.values()) == len(findings), "summary: disposition counts do not cover every material finding")

    reviewed = {row["observable_id"] for row in findings}
    _require(reviewed == OBSERVABLE_IDS, f"findings do not cover all 22 observables; missing={sorted(OBSERVABLE_IDS-reviewed)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    findings = _load_jsonl(args.findings)
    for index, row in enumerate(findings, start=1):
        _validate_finding(row, index)
    try:
        summary = json.loads(args.summary.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{args.summary}: invalid JSON: {exc}") from exc
    _require(isinstance(summary, dict), "summary must be one JSON object")
    _validate_summary(summary, findings)

    print(
        json.dumps(
            {
                "valid": True,
                "material_findings": len(findings),
                "observables_reviewed": 22,
                "first_finding_id": findings[0]["finding_id"],
                "last_finding_id": findings[-1]["finding_id"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
