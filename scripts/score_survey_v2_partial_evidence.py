#!/usr/bin/env python3
"""Score a century candidate universe from partial Survey-v2 evidence."""

from __future__ import annotations

import argparse
import heapq
import json
from collections import Counter
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_partial_evidence import (
    compile_partial_evidence,
    score_candidate,
)
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states
from hdmatch.schemas import StructuralChartFeatures
from hdmatch.util.canonical import sha256_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
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
    manifest_path = args.cache / "manifest.json"
    manifest = CenturyCacheManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    field_map = json.loads(args.field_map.read_text(encoding="utf-8"))
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    compiled = compile_partial_evidence(
        evidence=evidence,
        field_dependency_map=field_map,
        model=model,
    )
    query_times = _parse_queries(args.query_time)
    query_hits: dict[str, tuple[Any, Fraction] | None] = {
        label: None for label in query_times
    }
    histogram: Counter[Fraction] = Counter()
    top_heap: list[tuple[Fraction, int]] = []
    scored_states: dict[int, Any] = {}

    for index, state in enumerate(states):
        features = state.chart_features
        if not isinstance(features, StructuralChartFeatures):
            raise ValueError("partial-evidence scorer requires structural chart features")
        score = score_candidate(features, compiled)
        histogram[score] += 1
        if len(top_heap) < args.top:
            heapq.heappush(top_heap, (score, index))
            scored_states[index] = state
        elif score > top_heap[0][0]:
            _, dropped = heapq.heapreplace(top_heap, (score, index))
            scored_states.pop(dropped, None)
            scored_states[index] = state
        for label, timestamp in query_times.items():
            if query_hits[label] is None and state.start_utc <= timestamp < state.end_utc:
                query_hits[label] = (state, score)

    queries = []
    for label, timestamp in query_times.items():
        hit = query_hits[label]
        if hit is None:
            raise ValueError(f"query timestamp not present in candidate universe: {label}")
        state, score = hit
        best_rank, worst_rank = _rank_from_histogram(histogram, score)
        queries.append(
            {
                "label": label,
                "timestamp": timestamp.isoformat(),
                "interval_start_utc": state.start_utc.isoformat(),
                "interval_end_utc": state.end_utc.isoformat(),
                "profile": _structural(state.chart_features).profile,
                "raw_score": _fraction_json(score),
                "best_rank": best_rank,
                "worst_rank": worst_rank,
                "tie_size": worst_rank - best_rank + 1,
            }
        )
    top_candidates = []
    for score, index in sorted(top_heap, reverse=True):
        state = scored_states[index]
        top_candidates.append(
            {
                "interval_start_utc": state.start_utc.isoformat(),
                "interval_end_utc": state.end_utc.isoformat(),
                "profile": _structural(state.chart_features).profile,
                "raw_score": _fraction_json(score),
            }
        )

    report = {
        "schema_version": "survey-v2-partial-evidence-century-score-v1",
        "claim_scope": "development_partial_evidence_only_not_validation",
        "candidate_count": len(states),
        "evidence_selection_classification": evidence.get(
            "development_classification", "unspecified"
        ),
        "eligible_field_count": len(compiled.fields),
        "eligible_cluster_count": len({field.cluster_id for field in compiled.fields}),
        "field_ids": [field.field_id for field in compiled.fields],
        "candidate_blind_scoring": True,
        "hidden_structural_rarity_bonus": False,
        "dependency_cluster_macro_average": True,
        "queries": queries,
        "top_candidates": top_candidates,
        "distinct_score_count": len(histogram),
        "candidate_universe_manifest_sha256": sha256_file(manifest_path),
        "field_map_sha256": sha256_file(args.field_map),
        "base_mapping_sha256": sha256_file(args.base_mapping),
        "overlay_sha256": sha256_file(args.overlay),
        "evidence_sha256": sha256_file(args.evidence),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)


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



def _rank_from_histogram(histogram: Counter[Fraction], score: Fraction) -> tuple[int, int]:
    higher = sum(count for value, count in histogram.items() if value > score)
    tied = histogram[score]
    return higher + 1, higher + tied


def _fraction_json(value: Fraction) -> dict[str, float | int]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def _structural(value: object) -> StructuralChartFeatures:
    if not isinstance(value, StructuralChartFeatures):
        raise ValueError("expected structural chart features")
    return value


if __name__ == "__main__":
    main()
