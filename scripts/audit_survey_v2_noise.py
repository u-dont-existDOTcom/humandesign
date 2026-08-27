#!/usr/bin/env python3
"""Run the frozen full-universe survey-v2 answer-noise audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_capacity import TARGET_FEATURES, _clean_observable_patterns
from hdmatch.evaluation.survey_v2_noise import (
    DEFAULT_NOISE_SCENARIOS,
    simulate_noise_case,
    summarize_noise_cases,
)
from hdmatch.evaluation.survey_v2_recoverability import (
    DEFAULT_TIE_BREAKERS,
    _tie_breaker_vector,
    _value_vector,
)
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states
from hdmatch.schemas import StructuralChartFeatures
from hdmatch.util.canonical import sha256_file, sha256_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--case-start", type=int, default=0)
    parser.add_argument("--case-stop", type=int)
    parser.add_argument(
        "--candidate-limit",
        type=int,
        help="Smoke-test only: truncate the candidate universe and mark the report non-century.",
    )
    parser.add_argument(
        "--base-mapping",
        type=Path,
        default=Path("reference/core/profile_v3_6_v43_mapping_frozen_2026_08_22.json"),
    )
    parser.add_argument(
        "--overlay",
        type=Path,
        default=Path("reference/core/profile_v3_6_v43_mapping_overlay_v2_2026_08_22.json"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest_path = args.cache / "manifest.json"
    manifest = CenturyCacheManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    if args.candidate_limit is not None:
        if args.candidate_limit < 2:
            raise ValueError("candidate-limit must be at least two")
        states = states[: args.candidate_limit]
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    structural = tuple(_structural(state.chart_features) for state in states)
    base = _clean_observable_patterns(structural, model)
    target_vectors = tuple(_value_vector(structural, feature) for feature in TARGET_FEATURES)
    tie_vectors = tuple(
        _tie_breaker_vector(structural, feature) for feature in DEFAULT_TIE_BREAKERS
    )
    rows = tuple(
        tuple(base[index])
        + tuple(vector[index] for vector in target_vectors)
        + tuple(vector[index] for vector in tie_vectors)
        for index in range(len(states))
    )
    base_feature_count = len(base[0]) + len(TARGET_FEATURES)
    stop = len(states) if args.case_stop is None else min(args.case_stop, len(states))
    if not 0 <= args.case_start < stop:
        raise ValueError("case range must be a non-empty subset of the universe")

    summaries = []
    for scenario in DEFAULT_NOISE_SCENARIOS:
        cases = tuple(
            simulate_noise_case(
                rows,
                base_feature_count=base_feature_count,
                true_index=true_index,
                scenario=scenario,
            )
            for true_index in range(args.case_start, stop)
        )
        summaries.append(summarize_noise_cases(cases).model_dump(mode="json"))

    report: dict[str, Any] = {
        "schema_version": "survey-v2-century-noise-audit-v1",
        "claim_scope": "synthetic_oracle_robustness_only_not_demonstrated_human_accuracy",
        "candidate_count": len(states),
        "case_start": args.case_start,
        "case_stop": stop,
        "covers_complete_universe": (
            args.candidate_limit is None and args.case_start == 0 and stop == len(states)
        ),
        "base_answer_count": base_feature_count,
        "adaptive_tie_breakers": list(DEFAULT_TIE_BREAKERS),
        "scenario_definitions": [
            scenario.model_dump(mode="json") for scenario in DEFAULT_NOISE_SCENARIOS
        ],
        "scenario_summaries": summaries,
        "candidate_universe_manifest_sha256": sha256_file(manifest_path),
        "base_mapping_sha256": sha256_file(args.base_mapping),
        "overlay_sha256": sha256_file(args.overlay),
        "candidate_blind_selection": True,
        "target_blind_stopping": True,
        "post_reveal_excluded_from_headline_science": True,
    }
    report["report_content_sha256"] = sha256_json(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)


def _structural(value: object) -> StructuralChartFeatures:
    if not isinstance(value, StructuralChartFeatures):
        raise ValueError("noise audit requires structural chart features")
    return value


if __name__ == "__main__":
    main()
