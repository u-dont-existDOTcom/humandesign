#!/usr/bin/env python3
"""Compare a frozen independent CF-003 behavioral target with its committed predictor."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from hdmatch.empirical_astrology.cf003 import CF003_CANDIDATE_BODIES
from hdmatch.empirical_astrology.cf003_target import compare_cf003_rankings

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
    ROOT / "reference/empirical_astrology/cf003_independent_behavioral_target_manifest_v0.json"
)


def _duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(), object_pairs_hook=_duplicate_guard)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def predictor_scores(value: dict[str, Any]) -> dict[str, float]:
    if value.get("schema_version") != "cf003-predictor-scores-v0":
        raise ValueError("predictor file must use cf003-predictor-scores-v0")
    if value.get("candidate_id") != "CF-003":
        raise ValueError("predictor file candidate_id must be CF-003")
    raw = value.get("planet_scores")
    if not isinstance(raw, dict):
        raise ValueError("predictor file must contain planet_scores mapping")
    out = {str(key).lower(): float(score) for key, score in raw.items()}
    if set(out) != set(CF003_CANDIDATE_BODIES):
        raise ValueError("predictor score mapping must contain all ten candidate bodies")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--predictor", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    target = load_object(args.target)
    manifest = load_object(args.manifest)
    if target.get("schema_version") != "cf003-frozen-behavioral-target-v0":
        raise ValueError("unexpected behavioral target schema")
    if target.get("behavioral_target_complete") is not True:
        raise ValueError("behavioral target is incomplete; primary comparison unavailable")
    if target.get("manifest_sha256") != sha256(args.manifest):
        raise ValueError("behavioral target was not frozen against this manifest")

    commitment = target.get("predictor_commitment_sha256")
    if not isinstance(commitment, str):
        raise ValueError("behavioral target lacks a preclassification predictor commitment")
    actual_predictor_hash = sha256(args.predictor)
    if actual_predictor_hash != commitment:
        raise ValueError("predictor file does not match the preclassification commitment")

    behavior = target.get("planet_scores")
    if not isinstance(behavior, dict):
        raise ValueError("frozen behavioral target lacks mapped planet scores")

    predictor_file = load_object(args.predictor)
    expected_spec_hash = manifest["files"]["predictor_spec"]["sha256"]
    if predictor_file.get("predictor_spec_sha256") != expected_spec_hash:
        raise ValueError("predictor file does not use the manifest-pinned predictor spec")
    prediction = predictor_scores(predictor_file)
    comparison = compare_cf003_rankings(prediction, behavior)

    result = {
        "schema_version": "cf003-target-predictor-comparison-v0",
        "behavioral_target_sha256": sha256(args.target),
        "predictor_file_sha256": actual_predictor_hash,
        "predictor_commitment_verified": True,
        "comparison": asdict(comparison),
        "primary_endpoint": {
            "name": "predicted_top_set_mean_behavioral_midrank",
            "value": comparison.primary_top_set_mean_behavioral_midrank,
            "direction": "lower_is_better",
        },
        "secondary_endpoints": {
            "spearman_rho": comparison.spearman_rho,
            "top3_fractional_overlap": comparison.top3_fractional_overlap,
            "top3_fractional_jaccard": comparison.top3_fractional_jaccard,
            "spearman_undefined_rule": (
                "Per-person undefined rho remains null; cohort summaries must report "
                "the number defined rather than imputing a value."
            ),
        },
        "scientific_status": "development_comparison_not_validation",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote CF-003 comparison to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
