#!/usr/bin/env python3
"""Run the frozen full-universe survey-v2 answer-noise audit."""

from __future__ import annotations

import argparse
import gc
import json
import resource
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_capacity import TARGET_FEATURES, _clean_observable_patterns
from hdmatch.evaluation.survey_v2_noise import (
    DEFAULT_NOISE_SCENARIOS,
    summarize_noise_cases,
)
from hdmatch.evaluation.survey_v2_noise_indexed import (
    IndexedSurveyScorer,
    simulate_noise_case_indexed,
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
    audit_started = time.perf_counter()
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
    candidate_count = len(rows)
    feature_ids = (
        tuple(f"baseline_observable:{index}" for index in range(len(base[0])))
        + tuple(TARGET_FEATURES)
        + tuple(DEFAULT_TIE_BREAKERS)
    )
    base_feature_count = len(base[0]) + len(TARGET_FEATURES)
    stop = len(states) if args.case_stop is None else min(args.case_stop, len(states))
    if not 0 <= args.case_start < stop:
        raise ValueError("case range must be a non-empty subset of the universe")

    scorer = IndexedSurveyScorer.build(rows)
    del states, structural, base, target_vectors, tie_vectors
    gc.collect()
    summaries = []
    diagnostics: dict[str, Any] = {}
    for scenario in DEFAULT_NOISE_SCENARIOS:
        scenario_started = time.perf_counter()
        cases = tuple(
            simulate_noise_case_indexed(
                scorer,
                base_feature_count=base_feature_count,
                true_index=true_index,
                scenario=scenario,
            )
            for true_index in range(args.case_start, stop)
        )
        summaries.append(summarize_noise_cases(cases).model_dump(mode="json"))
        diagnostics[scenario.scenario_id] = _failure_diagnostics(cases, feature_ids)
        summaries[-1]["runtime_seconds"] = time.perf_counter() - scenario_started
        summaries[-1]["unique_observed_signature_count"] = _signature_count(
            scorer,
            base_feature_count,
            scenario,
            args.case_start,
            stop,
        )

    report: dict[str, Any] = {
        "schema_version": "survey-v2-century-noise-audit-v1",
        "claim_scope": "synthetic_oracle_robustness_only_not_demonstrated_human_accuracy",
        "candidate_count": candidate_count,
        "case_start": args.case_start,
        "case_stop": stop,
        "covers_complete_universe": (
            args.candidate_limit is None and args.case_start == 0 and stop == candidate_count
        ),
        "base_answer_count": base_feature_count,
        "adaptive_tie_breakers": list(DEFAULT_TIE_BREAKERS),
        "feature_ids": list(feature_ids),
        "scenario_definitions": [
            scenario.model_dump(mode="json") for scenario in DEFAULT_NOISE_SCENARIOS
        ],
        "scenario_summaries": summaries,
        "failure_diagnostics": diagnostics,
        "candidate_universe_manifest_sha256": sha256_file(manifest_path),
        "base_mapping_sha256": sha256_file(args.base_mapping),
        "overlay_sha256": sha256_file(args.overlay),
        "candidate_blind_selection": True,
        "target_blind_stopping": True,
        "post_reveal_excluded_from_headline_science": True,
        "optimized_scorer": "python-int-inverted-bitsets-bit-sliced-exact-v1",
        "reference_equivalence_status": "required_by_test_suite",
        "git_commit_sha": _git_commit(),
        "runtime_seconds": time.perf_counter() - audit_started,
        "peak_memory_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
    }
    report["report_content_sha256"] = sha256_json(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)


def _structural(value: object) -> StructuralChartFeatures:
    if not isinstance(value, StructuralChartFeatures):
        raise ValueError("noise audit requires structural chart features")
    return value


def _failure_diagnostics(cases: tuple[Any, ...], feature_ids: tuple[str, ...]) -> dict[str, Any]:
    failures = [case for case in cases if case.best_rank != 1 or case.worst_rank != 1]
    by_perturbed: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"case_count": 0, "failure_count": 0, "rank_damage_sum": 0.0, "top10_sum": 0.0}
    )
    leading_differences: Counter[str] = Counter()
    for case in cases:
        for feature in case.perturbed_feature_indices:
            row = by_perturbed[feature_ids[feature]]
            row["case_count"] += 1
            row["failure_count"] += int(case.best_rank != 1 or case.worst_rank != 1)
            row["rank_damage_sum"] += case.midrank - 1
            row["top10_sum"] += case.top10_credit
    for case in failures:
        leading_differences.update(
            feature_ids[feature] for feature in case.leading_competitor_difference_indices
        )
    normalized = {}
    for feature, row in sorted(by_perturbed.items()):
        count = int(row["case_count"])
        normalized[feature] = {
            "case_count": count,
            "failure_rate": float(row["failure_count"]) / count,
            "mean_rank_damage": float(row["rank_damage_sum"]) / count,
            "top10": float(row["top10_sum"]) / count,
        }
    return {
        "failure_count": len(failures),
        "true_candidate_eliminated_count": sum(not case.true_candidate_survived for case in cases),
        "outscored_but_not_eliminated_count": sum(
            case.overtaking_candidate_count > 0 and case.true_candidate_survived for case in cases
        ),
        "median_overtaking_candidates_on_failure": (
            sorted(case.overtaking_candidate_count for case in failures)[len(failures) // 2]
            if failures
            else 0
        ),
        "by_perturbed_feature": normalized,
        "leading_competitor_difference_counts": dict(leading_differences.most_common()),
    }


def _signature_count(
    scorer: IndexedSurveyScorer,
    base_feature_count: int,
    scenario: Any,
    start: int,
    stop: int,
) -> int:
    # The source-index-seeded corruption rule can make otherwise identical rows
    # follow different paths. Count the conservative exact memoization key.
    from hdmatch.evaluation.survey_v2_noise import _selected_positions

    signatures = set()
    for true_index in range(start, stop):
        count = max(
            scenario.minimum_perturbed_answers,
            __import__("math").ceil(base_feature_count * scenario.fraction),
        )
        selected = _selected_positions(base_feature_count, count, scenario, true_index)
        truth = scorer.rows[true_index]
        observations = tuple(
            scorer.perturb(feature, truth[feature], scenario, true_index)
            if feature in selected
            else (truth[feature],)
            for feature in range(base_feature_count)
        )
        signatures.add(observations)
    return len(signatures)


def _git_commit() -> str:
    return subprocess.check_output(
        ("git", "rev-parse", "HEAD"), text=True, encoding="utf-8"
    ).strip()


if __name__ == "__main__":
    main()
