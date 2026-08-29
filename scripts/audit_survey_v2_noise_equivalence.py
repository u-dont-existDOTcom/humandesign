#!/usr/bin/env python3
"""Deterministically compare reference and indexed noise scorers on real-cache subsets."""

from __future__ import annotations

import argparse
import json
import random
import resource
import subprocess
import time
from pathlib import Path
from typing import Any

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_capacity import TARGET_FEATURES, _clean_observable_patterns
from hdmatch.evaluation.survey_v2_noise import (
    DEFAULT_NOISE_SCENARIOS,
    simulate_noise_case,
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
    parser.add_argument("--subset-sizes", default="32,128,512")
    parser.add_argument("--seed", type=int, default=20260827)
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
    started = time.perf_counter()
    manifest_path = args.cache / "manifest.json"
    manifest = CenturyCacheManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    structural = tuple(_structural(state.chart_features) for state in states)
    base = _clean_observable_patterns(structural, model)
    target_vectors = tuple(_value_vector(structural, feature) for feature in TARGET_FEATURES)
    tie_vectors = tuple(
        _tie_breaker_vector(structural, feature) for feature in DEFAULT_TIE_BREAKERS
    )
    full_rows = tuple(
        tuple(base[index])
        + tuple(vector[index] for vector in target_vectors)
        + tuple(vector[index] for vector in tie_vectors)
        for index in range(len(states))
    )
    base_feature_count = len(base[0]) + len(TARGET_FEATURES)
    subset_sizes = tuple(int(value) for value in args.subset_sizes.split(","))
    rng = random.Random(args.seed)
    scenario_variants = DEFAULT_NOISE_SCENARIOS + tuple(
        scenario.model_copy(update={"seed": seed})
        for scenario in DEFAULT_NOISE_SCENARIOS
        for seed in (20260828, 20260829)
        if scenario.fraction > 0 or scenario.minimum_perturbed_answers > 0
    )
    comparisons = 0
    subsets = []
    for size in subset_sizes:
        if not 2 <= size <= len(full_rows):
            raise ValueError(f"invalid subset size: {size}")
        source_indices = sorted(rng.sample(range(len(full_rows)), size))
        rows = tuple(full_rows[index] for index in source_indices)
        scorer = IndexedSurveyScorer.build(rows)
        for scenario in scenario_variants:
            for true_index in range(size):
                reference = simulate_noise_case(
                    rows,
                    base_feature_count=base_feature_count,
                    true_index=true_index,
                    scenario=scenario,
                )
                indexed = simulate_noise_case_indexed(
                    scorer,
                    base_feature_count=base_feature_count,
                    true_index=true_index,
                    scenario=scenario,
                )
                comparisons += 1
                if indexed != reference:
                    raise RuntimeError(
                        f"equivalence failure size={size} scenario={scenario.scenario_id} "
                        f"seed={scenario.seed} true_index={true_index}"
                    )
        subsets.append(
            {
                "size": size,
                "source_index_sha256": sha256_json(source_indices),
                "scenario_variant_count": len(scenario_variants),
            }
        )
    report: dict[str, Any] = {
        "schema_version": "survey-v2-noise-scorer-equivalence-v1",
        "status": "pass",
        "reference_scorer": "survey_v2_noise.simulate_noise_case",
        "optimized_scorer": "python-int-inverted-bitsets-bit-sliced-exact-v1",
        "candidate_universe_count": len(full_rows),
        "candidate_universe_manifest_sha256": sha256_file(manifest_path),
        "seed": args.seed,
        "subsets": subsets,
        "comparison_count": comparisons,
        "runtime_seconds": time.perf_counter() - started,
        "peak_memory_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
        "git_commit_sha": subprocess.check_output(
            ("git", "rev-parse", "HEAD"), text=True, encoding="utf-8"
        ).strip(),
    }
    report["report_content_sha256"] = sha256_json(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)


def _structural(value: object) -> StructuralChartFeatures:
    if not isinstance(value, StructuralChartFeatures):
        raise ValueError("equivalence audit requires structural chart features")
    return value


if __name__ == "__main__":
    main()
