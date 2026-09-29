#!/usr/bin/env python3
"""Compare a frozen CF-003 behavioral target with separately frozen predictor scores."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from hdmatch.empirical_astrology.cf003 import CF003_CANDIDATE_BODIES
from hdmatch.empirical_astrology.cf003_target import compare_cf003_rankings


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def predictor_scores(value: dict[str, Any]) -> dict[str, float]:
    raw = value.get("planet_scores", value.get("scores"))
    if not isinstance(raw, dict):
        raise ValueError("predictor file must contain planet_scores or scores mapping")
    out = {str(key).lower(): float(score) for key, score in raw.items()}
    if set(out) != set(CF003_CANDIDATE_BODIES):
        raise ValueError("predictor score mapping must contain all ten candidate bodies")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--predictor", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    target = load_object(args.target)
    if target.get("prediction_opened") is not False:
        raise ValueError("behavioral target does not prove prediction remained unopened")
    if target.get("behavioral_target_complete") is not True:
        raise ValueError("behavioral target is incomplete; primary comparison unavailable")
    behavior = target.get("planet_scores")
    if not isinstance(behavior, dict):
        raise ValueError("frozen behavioral target lacks mapped planet scores")

    predictor_file = load_object(args.predictor)
    prediction = predictor_scores(predictor_file)
    comparison = compare_cf003_rankings(prediction, behavior)

    result = {
        "schema_version": "cf003-target-predictor-comparison-v0",
        "behavioral_target_sha256": sha256(args.target),
        "predictor_file_sha256": sha256(args.predictor),
        "prediction_opened_after_target_freeze": True,
        "comparison": asdict(comparison),
        "primary_endpoint": {
            "name": "predicted_top_set_mean_behavioral_midrank",
            "value": comparison.primary_top_set_mean_behavioral_midrank,
            "direction": "lower_is_better",
        },
        "secondary_endpoints": {
            "spearman_rho": comparison.spearman_rho,
            "top3_overlap_count": comparison.top3_overlap_count,
            "top3_jaccard": comparison.top3_jaccard,
        },
        "scientific_status": "development_or_prospective_as_declared_by_study_manifest",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote CF-003 comparison to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
