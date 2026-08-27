#!/usr/bin/env python3
"""Rank unused cached structural features by incremental discrimination capacity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.feature_capacity import audit_structural_feature_capacity
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = CenturyCacheManifest.model_validate(
        json.loads((args.cache / "manifest.json").read_text(encoding="utf-8"))
    )
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    report = audit_structural_feature_capacity(states, manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "intervals=",
        report.cache_interval_count,
        " baseline_bits=",
        f"{report.baseline.duration_weighted_information_bits:.6f}",
        " best_feature=",
        report.ranked_features[0].feature_id,
        " best_increment_bits=",
        f"{report.ranked_features[0].incremental_duration_weighted_bits:.6f}",
        sep="",
    )


if __name__ == "__main__":
    main()
