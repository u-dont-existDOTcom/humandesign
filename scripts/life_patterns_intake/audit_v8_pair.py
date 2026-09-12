"""Read-only structural audit of v8 transfers and v8.1 repair supplements.

Uses only Python's standard library. This is not a corpus importer, a label
normalizer, a source-authenticity check, or authorization for research scoring.
Reports contain structural identifiers/counts, never participant narrative.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

BASE_SCHEMA = "life-patterns-pattern-first-longitudinal-interview-v8"
REPAIR_SCHEMA = "life-patterns-v8-repair-supplement-v8.1"


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _constant(_: str) -> Any:
    raise ValueError("non-finite JSON constant")


def load(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                       parse_constant=_constant)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value, {"filename": path.name, "bytes": len(raw),
                   "sha256": hashlib.sha256(raw).hexdigest()}


def audit(base: dict[str, Any], repair: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    def check(condition: bool, label: str) -> None:
        if not condition:
            errors.append(label)

    def index(parent: dict[str, Any], field: str, key: str) -> dict[str, Any]:
        rows = parent.get(field)
        if not isinstance(rows, list):
            errors.append(f"{field}: expected array")
            return {}
        out: dict[str, Any] = {}
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get(key), str):
                errors.append(f"{field}: missing string ID")
                continue
            ident = row[key]
            if not ident or ident in out:
                errors.append(f"{field}: empty or duplicate ID")
            out[ident] = row
        return out

    def refs(row: dict[str, Any], field: str, target: dict[str, Any], label: str) -> None:
        values = row.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{label}/{field}: expected reference array")
            return
        check(all(isinstance(v, str) and v in target for v in values),
              f"{label}/{field}: unresolved reference")

    check(base.get("schema_version") == BASE_SCHEMA, "unsupported base schema")
    check(repair.get("schema_version") == REPAIR_SCHEMA, "unsupported repair schema")
    check(repair.get("original_schema_version") == base.get("schema_version"),
          "original schema reference mismatch")
    check(repair.get("original_record_status") == base.get("record_status"),
          "original status reference mismatch")
    patterns = index(base, "pattern_claims", "pattern_id")
    series = index(base, "series_reports", "series_id")
    episodes = index(base, "episodes", "episode_id")
    provenance = base.get("transcript_source_provenance", {})
    turns = provenance.get("source_turn_index", {}) if isinstance(provenance, dict) else {}
    if not isinstance(turns, dict):
        errors.append("source turn index: expected object")
        turns = {}
    for ident, row in patterns.items():
        refs(row, "supporting_episode_ids", episodes, ident)
        refs(row, "counterexample_episode_ids", episodes, ident)
        refs(row, "supporting_series_report_ids", series, ident)
        refs(row, "source_turn_ids", turns, ident)
    for ident, row in {**series, **episodes}.items():
        refs(row, "source_turn_ids", turns, ident)
        refs(row, "linked_pattern_ids", patterns, ident)

    questions = index(repair, "question_log", "question_id")
    responses = index(repair, "repair_responses", "response_id")
    recovered = index(repair, "recovered_transcript_turns", "recovered_turn_id")
    changes = index(repair, "participant_confirmed_account_changes", "target_pattern_id")
    additions = index(repair, "post_review_added_evidence", "added_evidence_id")
    metadata = index(repair, "proposed_metadata_corrections", "target_pattern_id")
    outstanding = index(repair, "outstanding_issues", "issue_id")
    review = repair.get("review_record", {})
    if not isinstance(review, dict):
        errors.append("review record: expected object")
        review = {}
    check(len(questions) <= 4, "repair question budget exceeded")
    for ident, row in questions.items():
        check(row.get("target_pattern_id") in patterns, f"{ident}: unknown pattern")
        check(row.get("response_reference") in responses, f"{ident}: missing response")
    for ident, row in recovered.items():
        if "original_local_id" in row:
            check(row["original_local_id"] in turns, f"{ident}: missing original turn")
        if "pattern_id" in row:
            check(row["pattern_id"] in patterns, f"{ident}: unknown pattern")
    for ident, row in changes.items():
        check(ident in patterns, f"{ident}: changed pattern absent from original")
        check(row.get("review_reference") == review.get("review_id"),
              f"{ident}: missing review reference")
        check(row.get("approval_reference") in responses, f"{ident}: missing approval")
    approval_id = review.get("participant_response_reference")
    check(approval_id in responses, "review approval response missing")
    if approval_id in responses:
        check(review.get("participant_response") == responses[approval_id].get("exact_text"),
              "review approval text disagrees with referenced response")
    for ident, row in additions.items():
        check(row.get("target_pattern_id") in patterns, f"{ident}: unknown pattern")
        check(row.get("source_reference") in responses, f"{ident}: missing source response")
    all_base_ids = set(patterns) | set(series) | set(episodes)
    for ident, row in metadata.items():
        check(ident in patterns, f"{ident}: metadata target absent")
        if ident in patterns:
            check(row.get("original_value") == patterns[ident].get(row.get("field")),
                  f"{ident}: metadata original value mismatch")
        for ref in row.get("source_references", []):
            check(isinstance(ref, str) and ref.startswith("original:")
                  and ref.partition(":")[2] in all_base_ids,
                  f"{ident}: unknown metadata source")

    label_findings = []
    for ident, row in patterns.items():
        n_ep = len(row.get("supporting_episode_ids", []))
        n_ser = len(row.get("supporting_series_report_ids", []))
        label = row.get("support_state")
        mismatch = ((label == "anchored_series" and (n_ep < 1 or n_ser < 1))
                    or (label == "multiple_episodes" and n_ep < 2))
        if mismatch:
            label_findings.append({"pattern_id": ident, "original_label": label,
                                   "episode_links": n_ep, "series_links": n_ser,
                                   "disposition": "retain_original_and_flag; no_automatic_relabel"})
    return {
        "audit_kind": "structural_pair_check_only",
        "structural_check_passed": not errors,
        "structural_errors": errors,
        "original_counts": {"patterns": len(patterns), "series": len(series),
                            "episodes": len(episodes), "indexed_participant_turns": len(turns)},
        "supplement_counts": {"questions": len(questions), "responses": len(responses),
                              "recovered_turns": len(recovered), "account_changes": len(changes),
                              "added_evidence_records": len(additions),
                              "outstanding_issues": len(outstanding)},
        "added_evidence_types": dict(sorted(Counter(
            row.get("evidence_type", "unspecified") for row in additions.values()).items())),
        "changed_pattern_ids": sorted(changes),
        "original_support_label_findings": label_findings,
        "limitations": [
            "Schema/status matches and resolvable IDs do not prove supplement lineage; uploaded bytes are separately hashed.",
            "Recovered text is an assertion in the supplied file; the original platform transcript was not independently checked.",
            "No episode segmentation, substantive labels, participant account, or support state is rewritten.",
            "Counts do not establish truth, comparability, independent recurrence, or participant-wide generality.",
            "No corpus importer, automatic research freeze, blinded coding, validation promotion, or model scoring is performed."
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("supplement", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        original, original_info = load(args.original)
        supplement, supplement_info = load(args.supplement)
        result = audit(original, supplement)
        result["input_files"] = {"original": original_info, "supplement": supplement_info}
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        print(f"Audit failed ({type(exc).__name__}); no successful audit claimed.")
        return 2
    print("Structural check:", "PASS" if result["structural_check_passed"] else "FAIL")
    return 0 if result["structural_check_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
