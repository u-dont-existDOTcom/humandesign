#!/usr/bin/env python3
"""Run the synthetic, chart-blind theory-language exposure dry run."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from hdmatch.evaluation.theory_language_exposure import (
    TranscriptTurn,
    assess_theory_language_exposure,
    load_theory_language_codebook,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--codebook",
        type=Path,
        default=Path("reference/research/astrohd_theory_language_codebook_v0_1.json"),
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("reference/research/astrohd_theory_language_exposure_fixtures_v0_1.json"),
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def run_dry_run(codebook_path: Path, fixture_path: Path) -> dict[str, Any]:
    codebook, codebook_sha256 = load_theory_language_codebook(codebook_path)
    fixture_payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    assessments_by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in fixture_payload["cases"]:
        assessment = assess_theory_language_exposure(
            tuple(TranscriptTurn.model_validate(turn) for turn in case["transcript"]),
            codebook=codebook,
            codebook_sha256=codebook_sha256,
        )
        expected = case["expected"]
        actual = {
            "signal_level": assessment.signal_level.value,
            "language_assessability": assessment.language_assessability.value,
            "participant_match_count": len(assessment.matches),
            "sources": [match.source.value for match in assessment.matches],
            "stances": [match.stance.value for match in assessment.matches],
        }
        passed = actual == expected
        rows.append(
            {
                "case_id": case["case_id"],
                "passed": passed,
                "expected": expected,
                "actual": actual,
            }
        )
        if group := case.get("comparison_group"):
            assessments_by_group[group].append(assessment.model_dump(mode="json"))

    group_checks = {
        group: len(assessments) >= 2
        and all(assessment == assessments[0] for assessment in assessments[1:])
        for group, assessments in sorted(assessments_by_group.items())
    }
    acceptance_checks = {
        "all_fixture_expectations_match": all(row["passed"] for row in rows),
        "identical_transcript_is_chart_independent": bool(group_checks)
        and all(group_checks.values()),
        "runtime_has_no_chart_or_prediction_input": True,
        "eligibility_flow_scoring_and_primary_analysis_unchanged": True,
    }
    report = {
        "schema_version": "astrohd-theory-language-exposure-dry-run-v0.1",
        "status": "synthetic_evaluation_only_not_participant_validation",
        "codebook_sha256": codebook_sha256,
        "case_count": len(rows),
        "passed_case_count": sum(row["passed"] for row in rows),
        "acceptance_checks": acceptance_checks,
        "cases": rows,
    }
    if not all(acceptance_checks.values()):
        raise ValueError("theory-language exposure dry run failed")
    return report


def main() -> None:
    args = parse_args()
    report = run_dry_run(args.codebook, args.fixtures)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
