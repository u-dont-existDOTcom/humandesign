#!/usr/bin/env python3
"""Run the frozen AstroHD V1.3b source-native direct regression."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from hdmatch.evaluation.astrohd_v13_traditions import (
    behavior_weight_variants,
    build_snapshot,
)
from hdmatch.evaluation.astrohd_v13b_native import (
    score_lilly_native,
    score_parashari_native,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--consensus-map", required=True, type=Path)
    parser.add_argument("--behavior", required=True, type=Path)
    parser.add_argument("--crosswalk", required=True, type=Path)
    parser.add_argument("--pyjhora-oracle", required=True, type=Path)
    parser.add_argument("--ephemeris-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    freeze = _load(args.freeze)
    consensus = _load(args.consensus_map)
    behavior = _load(args.behavior)
    crosswalk = _load(args.crosswalk)
    oracle = _load(args.pyjhora_oracle)

    freeze_sha = _sha256(args.freeze)
    if oracle["freeze_sha256"] != freeze_sha:
        raise ValueError("PyJHora oracle was not generated from this exact V1.3b freeze")
    expected_commit = freeze["source_native_models"]["parashari_shadbala"]["engine_commit"]
    if oracle["engine_commit"] != expected_commit:
        raise ValueError("PyJHora oracle engine commit does not match the frozen V1.3b engine")

    weights = behavior_weight_variants(behavior, crosswalk)
    queries = _query_rows(freeze)
    oracle_by_label = {row["label"]: row for row in oracle["results"]}
    if set(oracle_by_label) != {label for label, _ in queries}:
        raise ValueError("PyJHora oracle labels do not match the frozen direct-query set")

    location = freeze.get("location", {"latitude": 39.9526, "longitude": -75.1652})
    latitude = float(location.get("latitude", 39.9526))
    longitude = float(location.get("longitude", -75.1652))

    scored: dict[str, Any] = {}
    for label, raw_timestamp in queries:
        when = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
        snapshot = build_snapshot(
            when,
            latitude=latitude,
            longitude=longitude,
            ephemeris_root=args.ephemeris_root,
        )
        shadbala = oracle_by_label[label]["normalized_shadbala_strength"]
        traditions: dict[str, Any] = {
            "lilly_core_fortitude": {},
            "parashari_shadbala": {},
        }
        for weight_name, domain_weights in weights.items():
            traditions["lilly_core_fortitude"][weight_name] = {
                aggregation: score_lilly_native(
                    snapshot,
                    consensus_map=consensus,
                    behavior_weights=domain_weights,
                    aggregation=aggregation,
                )
                for aggregation in ("domain_mean_nonstack", "significator_stack")
            }
            traditions["parashari_shadbala"][weight_name] = {
                aggregation: score_parashari_native(
                    snapshot,
                    consensus_map=consensus,
                    behavior_weights=domain_weights,
                    shadbala_strengths=shadbala,
                    aggregation=aggregation,
                )
                for aggregation in ("domain_mean_nonstack", "significator_stack")
            }
        scored[label] = {
            "timestamp": raw_timestamp,
            "traditions": traditions,
        }

    verdict = _direct_verdict(scored)
    report = {
        "schema": "astrohd-v1.3b-source-native-direct-regression-v1",
        "claim_scope": "owner_post_result_development_not_validation",
        "freeze_sha256": freeze_sha,
        "consensus_map_sha256": _sha256(args.consensus_map),
        "behavior_sha256": _sha256(args.behavior),
        "crosswalk_sha256": _sha256(args.crosswalk),
        "pyjhora_oracle_sha256": _sha256(args.pyjhora_oracle),
        "queries": scored,
        "direct_verdict": verdict,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _direct_verdict(scored: dict[str, Any]) -> dict[str, Any]:
    traditions = ("lilly_core_fortitude", "parashari_shadbala")
    weight_variants = ("equal_domain", "frozen_measurement_confidence")
    aggregations = ("domain_mean_nonstack", "significator_stack")
    result: dict[str, Any] = {}

    for tradition in traditions:
        aggregation_rows: dict[str, Any] = {}
        for aggregation in aggregations:
            variants: dict[str, Any] = {}
            for weight_name in weight_variants:
                target = _score(scored, "target", tradition, weight_name, aggregation)
                comp = _score(
                    scored,
                    "persistent_competitor",
                    tradition,
                    weight_name,
                    aggregation,
                )
                same = [
                    _score(scored, label, tradition, weight_name, aggregation)
                    for label in scored
                    if label.startswith("same_date_")
                ]
                strongest = max([comp, *same])
                variants[weight_name] = {
                    "target": target,
                    "persistent_competitor": comp,
                    "strongest_same_date": max(same),
                    "strongest_any_competitor": strongest,
                    "target_margin_vs_strongest": target - strongest,
                    "pass": target > comp and all(value <= target for value in same),
                }
            aggregation_rows[aggregation] = {
                "variants": variants,
                "passes_both_behavioral_weight_variants": all(
                    row["pass"] for row in variants.values()
                ),
            }
        tradition_pass = any(
            row["passes_both_behavioral_weight_variants"]
            for row in aggregation_rows.values()
        )
        result[tradition] = {
            "aggregations": aggregation_rows,
            "tradition_pass": tradition_pass,
        }

    convergence = all(result[name]["tradition_pass"] for name in traditions)
    return {
        "traditions": result,
        "convergence_pass": convergence,
        "century_rank_admitted": convergence,
        "label": "CONVERGENCE_PASS" if convergence else "DIRECT_FAIL",
    }


def _score(
    scored: dict[str, Any],
    label: str,
    tradition: str,
    weight_name: str,
    aggregation: str,
) -> float:
    return float(
        scored[label]["traditions"][tradition][weight_name][aggregation]["total"]
    )


def _query_rows(freeze: dict[str, Any]) -> list[tuple[str, str]]:
    direct = freeze["direct_queries"]
    return [
        ("target", direct["target"]),
        ("persistent_competitor", direct["persistent_competitor"]),
        *[
            (f"same_date_{index}", value)
            for index, value in enumerate(direct["same_date_alternative_midpoints"])
        ],
    ]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    main()
