#!/usr/bin/env python3
"""Run the frozen AstroHD V1.3 tradition-grounded direct regression."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
from pathlib import Path
from typing import Any

from hdmatch.evaluation.astrohd_v13_traditions import (
    behavior_weight_variants,
    build_snapshot,
    score_snapshot,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--consensus-map", required=True, type=Path)
    parser.add_argument("--behavior", required=True, type=Path)
    parser.add_argument("--crosswalk", required=True, type=Path)
    parser.add_argument("--ephemeris-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    freeze = _load(args.freeze)
    consensus = _load(args.consensus_map)
    behavior = _load(args.behavior)
    crosswalk = _load(args.crosswalk)
    weights = behavior_weight_variants(behavior, crosswalk)
    direct = freeze["direct_queries"]
    query_values = [
        ("target", direct["target"]),
        ("persistent_competitor", direct["persistent_competitor"]),
        *[
            (f"same_date_{index}", value)
            for index, value in enumerate(direct["same_date_alternative_midpoints"])
        ],
    ]
    latitude = float(freeze["astronomy"]["location"]["latitude"])
    longitude = float(freeze["astronomy"]["location"]["longitude"])

    snapshots = {
        label: build_snapshot(
            _parse_iso(timestamp),
            latitude=latitude,
            longitude=longitude,
            ephemeris_root=args.ephemeris_root,
        )
        for label, timestamp in query_values
    }
    scores = _score_all(snapshots, consensus=consensus, weights=weights)
    verdict = _direct_verdict(scores)

    report: dict[str, Any] = {
        "schema": "astrohd-v1.3-tradition-grounded-direct-regression-v1",
        "claim_scope": "owner_post_result_development_not_validation",
        "freeze_sha256": _sha256(args.freeze),
        "consensus_map_sha256": _sha256(args.consensus_map),
        "behavior_sha256": _sha256(args.behavior),
        "crosswalk_sha256": _sha256(args.crosswalk),
        "queries": [
            {
                "label": label,
                "timestamp": timestamp,
                "scores": scores[label],
            }
            for label, timestamp in query_values
        ],
        "direct_verdict": verdict,
    }

    clean_equal_pass = (
        verdict["families"]["domain_collapse_nonstack"]["variants"]["equal_domain"]["pass"]
        or verdict["families"]["cross_tradition_convergence_stack"]["variants"]["equal_domain"][
            "pass"
        ]
    )
    neg = freeze.get("negative_control")
    if clean_equal_pass and neg and neg.get("status") == "FROZEN_BEFORE_ANY_V1_3_OWNER_SCORE":
        report["mapping_permutation_control"] = _permutation_control(
            snapshots=snapshots,
            consensus=consensus,
            weights=weights,
            observed_scores=scores,
            permutations=int(neg["permutations"]),
            seed=int(neg["random_seed"]),
        )
    else:
        report["mapping_permutation_control"] = {"status": "NOT_RUN_CLEAN_EQUAL_ARM_DID_NOT_PASS"}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _score_all(
    snapshots,
    *,
    consensus: dict[str, Any],
    weights: dict[str, dict[str, float]],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for label, snapshot in snapshots.items():
        per_variant = {}
        for variant, domain_weights in weights.items():
            per_variant[variant] = score_snapshot(
                snapshot,
                consensus_map=consensus,
                behavior_weights=domain_weights,
            )
        result[label] = per_variant
    return result


def _direct_verdict(scores: dict[str, dict[str, Any]]) -> dict[str, Any]:
    arms = (
        "domain_collapse_nonstack",
        "cross_tradition_convergence_stack",
        "raw_independent_testimony_stack",
    )
    variants = ("equal_domain", "frozen_measurement_confidence")
    families: dict[str, Any] = {}
    for arm in arms:
        row = {"variants": {}}
        for variant in variants:
            target = scores["target"][variant]["totals"][arm]
            comp = scores["persistent_competitor"][variant]["totals"][arm]
            same = [
                scores[label][variant]["totals"][arm]
                for label in scores
                if label.startswith("same_date_")
            ]
            strongest = max([comp, *same])
            passed = target > comp and all(value <= target for value in same)
            row["variants"][variant] = {
                "target": target,
                "persistent_competitor": comp,
                "strongest_same_date": max(same),
                "strongest_any_competitor": strongest,
                "target_margin_vs_strongest": target - strongest,
                "pass": passed,
            }
        row["family_pass_both_weight_variants"] = all(
            row["variants"][variant]["pass"] for variant in variants
        )
        families[arm] = row

    collapse = families["domain_collapse_nonstack"]["family_pass_both_weight_variants"]
    convergence = families["cross_tradition_convergence_stack"]["family_pass_both_weight_variants"]
    raw = families["raw_independent_testimony_stack"]["family_pass_both_weight_variants"]
    if collapse and convergence:
        label = "ROBUST_MULTI_FAMILY"
    elif convergence:
        label = "CONVERGENCE_SPECIFIC"
    elif collapse:
        label = "NONSTACK_SPECIFIC"
    elif raw:
        label = "RAW_STACK_ONLY_WARNING"
    else:
        label = "DIRECT_FAIL"
    return {
        "families": families,
        "robustness_label": label,
        "clean_century_rank_admitted": collapse or convergence,
    }


def _permutation_control(
    *,
    snapshots,
    consensus: dict[str, Any],
    weights: dict[str, dict[str, float]],
    observed_scores: dict[str, dict[str, Any]],
    permutations: int,
    seed: int,
) -> dict[str, Any]:
    rng = random.Random(seed)
    observed = _direct_verdict(observed_scores)
    spec_keys = [
        (arm, variant)
        for arm in (
            "domain_collapse_nonstack",
            "cross_tradition_convergence_stack",
            "raw_independent_testimony_stack",
        )
        for variant in ("equal_domain", "frozen_measurement_confidence")
    ]
    observed_margin = {
        key: observed["families"][key[0]]["variants"][key[1]]["target_margin_vs_strongest"]
        for key in spec_keys
    }
    exceed = {key: 0 for key in spec_keys}
    passed = {key: 0 for key in spec_keys}

    for _ in range(permutations):
        shuffled = _permute_map(consensus, rng)
        scores = _score_all(snapshots, consensus=shuffled, weights=weights)
        verdict = _direct_verdict(scores)
        for key in spec_keys:
            arm, variant = key
            row = verdict["families"][arm]["variants"][variant]
            if row["pass"]:
                passed[key] += 1
                if row["target_margin_vs_strongest"] >= observed_margin[key]:
                    exceed[key] += 1

    return {
        "status": "COMPLETED",
        "permutations": permutations,
        "random_seed": seed,
        "specifications": {
            f"{arm}::{variant}": {
                "observed_margin_vs_strongest": observed_margin[(arm, variant)],
                "permutation_direct_pass_count": passed[(arm, variant)],
                "permutation_meet_or_exceed_observed_count": exceed[(arm, variant)],
                "meet_or_exceed_fraction": exceed[(arm, variant)] / permutations,
            }
            for arm, variant in spec_keys
        },
    }


def _permute_map(consensus: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    out = copy.deepcopy(consensus)
    domains = out["domains"]
    traditions = [
        "hellenistic_western",
        "lilly_traditional_western",
        "parashari_jyotish",
    ]
    for tradition in traditions:
        entries = []
        for domain in domains:
            entry = next(row for row in domain["traditions"] if row["tradition"] == tradition)
            entries.append(
                {
                    "planets": copy.deepcopy(entry.get("planets", [])),
                    "houses": copy.deepcopy(entry.get("houses", [])),
                    "consensus_abstain": entry.get("consensus_abstain", False),
                }
            )
        rng.shuffle(entries)
        for domain, payload in zip(domains, entries, strict=True):
            entry = next(row for row in domain["traditions"] if row["tradition"] == tradition)
            entry["planets"] = payload["planets"]
            entry["houses"] = payload["houses"]
            entry["consensus_abstain"] = payload["consensus_abstain"]
    return out


def _parse_iso(raw: str):
    from datetime import datetime

    value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must include timezone")
    return value


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    main()
