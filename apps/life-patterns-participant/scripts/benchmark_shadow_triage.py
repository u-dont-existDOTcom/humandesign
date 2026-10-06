#!/usr/bin/env python3
"""Benchmark the development-only clarification triage shadow pipeline.

Input records may contain private participant text. Persisted output and console
receipts deliberately contain only ordinal case IDs, counts, route IDs, bounded
failure codes, token counts, and timing. They never contain input paths, source
text, source-turn IDs, prompts, raw model output, or content-derived hashes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import statistics
import sys
import tempfile
from pathlib import Path
from typing import Literal

from participant.domain import (
    COLLECTION_MODES,
    StrictModel,
    import_record,
    load_instrument,
    new_state,
    strict_json,
)
from participant.shadow_triage import (
    privacy_safe_case_summary,
    privacy_safe_dry_run_summary,
    run_shadow_fast_spec_path,
    run_shadow_triage,
)
from participant.store import canonical
from pydantic import Field, ValidationError

REPO_ROOT = Path(__file__).resolve().parents[3]


class LegacyCase(StrictModel):
    case_id: str = Field(pattern=r"^case-[0-9]{4}$")
    decision: Literal["review_ready", "clarification_needed"]
    selected_route_ids: list[str] = Field(default_factory=list)
    semantic_duration_seconds: float = Field(ge=0)


class LegacyResults(StrictModel):
    schema_name: Literal["life-patterns-legacy-triage-benchmark-v1"] = Field(alias="schema")
    cases: list[LegacyCase]


def _instrument() -> dict:
    sources = {
        "INTERVIEW-PROTOCOL-v6.md": REPO_ROOT
        / "tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md",
        "interviewer-bank-v7.json": REPO_ROOT
        / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json",
        "EVIDENCE-GUIDE-v7.json": REPO_ROOT
        / "tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json",
        "INTERVIEW-CONTROLLER-v2.md": REPO_ROOT
        / "tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md",
    }
    with tempfile.TemporaryDirectory(prefix="life-patterns-shadow-authority-") as folder:
        root = Path(folder)
        for name, source in sources.items():
            shutil.copy2(source, root / name)
        return load_instrument(root)


def _state(record: dict, *, model: str, effort: str, instrument: dict) -> dict:
    state = new_state("shadow-gap-triage-v1", model, effort)
    mode = record.get("collection_mode", "unknown")
    if mode not in COLLECTION_MODES:
        mode = "unknown"
    import_record(state, record, "prior_json", instrument, str(mode))
    state["consent"] = True
    state["phase"] = "ready"
    return state


def _load_legacy(path: Path | None) -> dict[str, LegacyCase]:
    if path is None:
        return {}
    value = LegacyResults.model_validate(strict_json(path.read_text(encoding="utf-8")))
    rows = {item.case_id: item for item in value.cases}
    if len(rows) != len(value.cases):
        raise ValueError("Legacy benchmark case identifiers must be unique.")
    return rows


def _percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return round(ordered[max(0, math.ceil(fraction * len(ordered)) - 1)], 3)


def _legacy_comparison(row: dict, legacy: LegacyCase | None) -> dict | None:
    if legacy is None:
        return None
    selected_route = row["selected_route_id"]
    current_seconds = float(row["semantic_duration_seconds"])
    shadow_decision = {
        "review_ready": "review_ready",
        "clarification_recommended": "clarification_needed",
    }.get(row["shadow_outcome"])
    return {
        "decision_match": shadow_decision == legacy.decision,
        "legacy_clarification_needed": legacy.decision == "clarification_needed",
        "selected_route_match": (
            selected_route is not None
            and bool(legacy.selected_route_ids)
            and selected_route == legacy.selected_route_ids[0]
        ),
        "legacy_semantic_duration_seconds": round(legacy.semantic_duration_seconds, 3),
        "speedup_ratio": (
            round(legacy.semantic_duration_seconds / current_seconds, 3)
            if current_seconds > 0
            else None
        ),
    }


def _aggregate(cases: list[dict]) -> dict:
    durations = [float(row["semantic_duration_seconds"]) for row in cases]
    comparisons = [row["legacy_comparison"] for row in cases if row["legacy_comparison"]]
    clarification_comparisons = [
        comparison
        for row in cases
        if (comparison := row["legacy_comparison"])
        and (
            row["shadow_outcome"] == "clarification_recommended"
            or comparison["legacy_clarification_needed"]
        )
    ]
    return {
        "case_count": len(cases),
        "median_semantic_duration_seconds": (
            round(statistics.median(durations), 3) if durations else None
        ),
        "p90_semantic_duration_seconds": _percentile(durations, 0.9),
        "legacy_comparison_count": len(comparisons),
        "legacy_decision_match_rate": (
            round(sum(item["decision_match"] for item in comparisons) / len(comparisons), 4)
            if comparisons
            else None
        ),
        "clarification_selected_route_match_rate": (
            round(
                sum(item["selected_route_match"] for item in clarification_comparisons)
                / len(clarification_comparisons),
                4,
            )
            if clarification_comparisons
            else None
        ),
    }


def _write_private_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".shadow-triage-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_name, 0o600)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--legacy-results", type=Path)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--effort", default="xhigh")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--defer-match-audit",
        action="store_true",
        help="Return the first clarification batch without blocking on the broad match audit.",
    )
    parser.add_argument(
        "--fast-spec-path",
        action="store_true",
        help="Use spec-only triage/admission and deterministic canonical question rendering.",
    )
    args = parser.parse_args()

    try:
        instrument = _instrument()
        legacy = _load_legacy(args.legacy_results)
        cases = []
        provider = None
        if not args.dry_run:
            # Import only for a real run. Dry-run verification never inspects
            # owner authentication or launches a model process.
            from gpt_review_worker import CodexCliProvider

            provider = CodexCliProvider()

        for index, path in enumerate(args.records, 1):
            case_id = f"case-{index:04d}"
            record = strict_json(path.read_text(encoding="utf-8"))
            state = _state(record, model=args.model, effort=args.effort, instrument=instrument)
            if args.dry_run:
                cases.append(privacy_safe_dry_run_summary(case_id, state, instrument))
                continue
            assert provider is not None
            if args.fast_spec_path:
                result = run_shadow_fast_spec_path(
                    state,
                    instrument,
                    provider,
                    model=args.model,
                    effort=args.effort,
                )
            else:
                result = run_shadow_triage(
                    state,
                    instrument,
                    provider,
                    model=args.model,
                    effort=args.effort,
                    match_audit_mode="deferred" if args.defer_match_audit else "inline",
                )
            row = privacy_safe_case_summary(case_id, state, result)
            row["legacy_comparison"] = _legacy_comparison(row, legacy.get(case_id))
            cases.append(row)

        if legacy and set(legacy) != {f"case-{index:04d}" for index in range(1, len(cases) + 1)}:
            raise ValueError("Legacy results must match the current ordinal case set exactly.")

        if args.dry_run:
            report = {
                "schema": "life-patterns-shadow-triage-dry-run-v1",
                "shadow_only": True,
                "live_behavior_changed": False,
                "model_calls_executed": False,
                "case_count": len(cases),
                "cases": cases,
            }
        else:
            report = {
                "schema": "life-patterns-shadow-triage-benchmark-v1",
                "shadow_only": True,
                "live_behavior_changed": False,
                "model_calls_executed": True,
                "model": args.model,
                "effort": args.effort,
                "cases": cases,
                "aggregate": _aggregate(cases),
            }
        _write_private_json(args.output, report)
    except (AssertionError, OSError, RuntimeError, TypeError, ValueError, ValidationError) as exc:
        # Never echo exception text: parsing/model validators can include private
        # input fragments. The exception class and phase-independent code are enough
        # for a local operator to rerun under a debugger in an approved private path.
        print(
            canonical(
                {
                    "schema": "life-patterns-shadow-triage-cli-receipt-v1",
                    "status": "error",
                    "error_code": "shadow_benchmark_failed",
                    "error_type": type(exc).__name__,
                }
            ),
            file=sys.stderr,
        )
        return 1

    print(
        canonical(
            {
                "schema": "life-patterns-shadow-triage-cli-receipt-v1",
                "status": "ok",
                "mode": "dry_run" if args.dry_run else "semantic_benchmark",
                "case_count": len(cases),
                "output_written": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
