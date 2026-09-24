#!/usr/bin/env python3
"""Score a century candidate universe from partial Survey-v2 evidence."""

from __future__ import annotations

import argparse
import heapq
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_partial_evidence import (
    compile_partial_evidence,
    score_candidate_scaled,
)
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states
from hdmatch.schemas import StructuralChartFeatures
from hdmatch.util.canonical import sha256_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument(
        "--evidence-variant",
        action="append",
        default=[],
        help="Additional LABEL=PATH evidence variant scored in the same universe traversal.",
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--query-time", action="append", default=[])
    parser.add_argument(
        "--field-map",
        type=Path,
        default=Path("reference/core/survey_v2_field_dependency_map_v1_0_0.json"),
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
    if args.top < 1:
        raise ValueError("--top must be positive")
    evidence_paths = _parse_evidence_variants(args.evidence, args.evidence_variant)
    manifest_path = args.cache / "manifest.json"
    manifest = CenturyCacheManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    field_map = json.loads(args.field_map.read_text(encoding="utf-8"))
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    evidence_by_variant = {
        label: json.loads(path.read_text(encoding="utf-8"))
        for label, path in evidence_paths.items()
    }
    compiled_by_variant = {
        label: compile_partial_evidence(
            evidence=evidence,
            field_dependency_map=field_map,
            model=model,
        )
        for label, evidence in evidence_by_variant.items()
    }
    query_times = _parse_queries(args.query_time)
    query_hits = {
        variant: {label: None for label in query_times}
        for variant in compiled_by_variant
    }
    histograms: dict[str, Counter[int]] = {
        variant: Counter() for variant in compiled_by_variant
    }
    top_heaps: dict[str, list[tuple[int, int]]] = {
        variant: [] for variant in compiled_by_variant
    }

    for index, state in enumerate(states):
        features = state.chart_features
        if not isinstance(features, StructuralChartFeatures):
            raise ValueError("partial-evidence scorer requires structural chart features")
        for variant, compiled in compiled_by_variant.items():
            score = score_candidate_scaled(features, compiled)
            histograms[variant][score] += 1
            heap = top_heaps[variant]
            if len(heap) < args.top:
                heapq.heappush(heap, (score, index))
            elif score > heap[0][0]:
                heapq.heapreplace(heap, (score, index))
            for label, timestamp in query_times.items():
                if (
                    query_hits[variant][label] is None
                    and state.start_utc <= timestamp < state.end_utc
                ):
                    query_hits[variant][label] = (index, score)

    variants: dict[str, Any] = {}
    for variant, compiled in compiled_by_variant.items():
        histogram = histograms[variant]
        queries = []
        for label, timestamp in query_times.items():
            hit = query_hits[variant][label]
            if hit is None:
                raise ValueError(
                    f"query timestamp not present in candidate universe: {label}"
                )
            index, score = hit
            state = states[index]
            best_rank, worst_rank = _rank_from_histogram(histogram, score)
            queries.append(
                {
                    "label": label,
                    "timestamp": timestamp.isoformat(),
                    "interval_start_utc": state.start_utc.isoformat(),
                    "interval_end_utc": state.end_utc.isoformat(),
                    "profile": _structural(state.chart_features).profile,
                    "raw_score": _scaled_score_json(score, compiled.score_scale),
                    "best_rank": best_rank,
                    "worst_rank": worst_rank,
                    "tie_size": worst_rank - best_rank + 1,
                }
            )
        top_candidates = []
        for score, index in sorted(top_heaps[variant], reverse=True):
            state = states[index]
            top_candidates.append(
                {
                    "interval_start_utc": state.start_utc.isoformat(),
                    "interval_end_utc": state.end_utc.isoformat(),
                    "profile": _structural(state.chart_features).profile,
                    "raw_score": _scaled_score_json(score, compiled.score_scale),
                }
            )
        evidence = evidence_by_variant[variant]
        variants[variant] = {
            "evidence_selection_classification": evidence.get(
                "development_classification", "unspecified"
            ),
            "evidence_sha256": sha256_file(evidence_paths[variant]),
            "eligible_field_count": len(compiled.fields),
            "eligible_cluster_count": len(
                {field.cluster_id for field in compiled.fields}
            ),
            "field_ids": [field.field_id for field in compiled.fields],
            "score_scale": compiled.score_scale,
            "queries": queries,
            "top_candidates": top_candidates,
            "distinct_score_count": len(histogram),
        }

    report = {
        "schema_version": "survey-v2-partial-evidence-century-score-v2",
        "claim_scope": "development_partial_evidence_only_not_validation",
        "candidate_count": len(states),
        "candidate_blind_scoring": True,
        "hidden_structural_rarity_bonus": False,
        "dependency_cluster_macro_average": True,
        "exact_integer_scaled_scoring": True,
        "candidate_universe_manifest_sha256": sha256_file(manifest_path),
        "field_map_sha256": sha256_file(args.field_map),
        "base_mapping_sha256": sha256_file(args.base_mapping),
        "overlay_sha256": sha256_file(args.overlay),
        "variants": variants,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)


def _parse_evidence_variants(
    main_path: Path,
    values: list[str],
) -> dict[str, Path]:
    parsed = {"main": main_path}
    for value in values:
        label, separator, raw = value.partition("=")
        if not separator or not label or not raw:
            raise ValueError("--evidence-variant must use LABEL=PATH")
        if label in parsed:
            raise ValueError(f"duplicate evidence variant: {label}")
        parsed[label] = Path(raw)
    return parsed


def _parse_queries(values: list[str]) -> dict[str, datetime]:
    parsed: dict[str, datetime] = {}
    for value in values:
        label, separator, raw = value.partition("=")
        if not separator or not label or not raw:
            raise ValueError("--query-time must use LABEL=ISO_TIMESTAMP")
        timestamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("--query-time timestamps must include an offset")
        if label in parsed:
            raise ValueError(f"duplicate query label: {label}")
        parsed[label] = timestamp
    return parsed



def _rank_from_histogram(histogram: Counter[int], score: int) -> tuple[int, int]:
    higher = sum(count for value, count in histogram.items() if value > score)
    tied = histogram[score]
    return higher + 1, higher + tied


def _scaled_score_json(value: int, scale: int) -> dict[str, float | int]:
    return {
        "numerator": value,
        "denominator": scale,
        "decimal": value / scale,
    }


def _structural(value: object) -> StructuralChartFeatures:
    if not isinstance(value, StructuralChartFeatures):
        raise ValueError("expected structural chart features")
    return value


if __name__ == "__main__":
    main()
