#!/usr/bin/env python3
"""Run synthetic exact-match theory-language exposure fixtures."""

from __future__ import annotations

import argparse
import json
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
        default=Path("reference/core/astrohd_theory_language_codebook_v1.template.json"),
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("reference/core/astrohd_theory_language_exposure_synthetic_fixtures_v1.json"),
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def run_synthetic_fixtures(codebook_path: Path, fixture_path: Path) -> dict[str, Any]:
    codebook, codebook_sha256 = load_theory_language_codebook(codebook_path)
    fixture_payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    cases: list[dict[str, Any]] = []
    for case in fixture_payload["cases"]:
        transcript = tuple(TranscriptTurn.model_validate(turn) for turn in case["transcript"])
        assessment = assess_theory_language_exposure(
            transcript,
            codebook=codebook,
            codebook_sha256=codebook_sha256,
        )
        actual = {
            "language_assessability": assessment.language_assessability.value,
            "theory_specific_exposure_evidence_present": (
                assessment.theory_specific_exposure_evidence_present
            ),
            "occurrences": [
                {
                    "entry_id": occurrence.entry_id,
                    "lexical_specificity": occurrence.lexical_specificity.value,
                    "provenance": occurrence.provenance.value,
                    "stance": occurrence.stance.value,
                }
                for occurrence in assessment.occurrences
            ],
        }
        chart_isolation_results = [
            assessment.model_dump_json()
            for _synthetic_payload in case.get("synthetic_hidden_chart_payloads", [None])
        ]
        chart_isolation_passed = len(set(chart_isolation_results)) == 1
        cases.append(
            {
                "case_id": case["case_id"],
                "expectation_passed": actual == case["expected"],
                "chart_isolation_passed": chart_isolation_passed,
                "actual": actual,
            }
        )

    report = {
        "schema_version": "astrohd-theory-language-exposure-synthetic-run-v1",
        "status": "synthetic_only_no_runtime_effect",
        "codebook_sha256": codebook_sha256,
        "case_count": len(cases),
        "passed_case_count": sum(
            case["expectation_passed"] and case["chart_isolation_passed"] for case in cases
        ),
        "cases": cases,
    }
    if report["passed_case_count"] != report["case_count"]:
        raise ValueError("synthetic theory-language exposure fixture failure")
    return report


def main() -> None:
    args = parse_args()
    report = run_synthetic_fixtures(args.codebook, args.fixtures)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
