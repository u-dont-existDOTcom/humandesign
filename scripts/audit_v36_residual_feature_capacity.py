#!/usr/bin/env python3
"""Rank unused structural features after the clean V3.6 observable profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.residual_feature_capacity import audit_v36_residual_feature_capacity
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
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
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    report = audit_v36_residual_feature_capacity(states, manifest, model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "baseline_bits=",
        f"{report.baseline.uniform_information_bits:.6f}",
        " reference_tie=",
        report.reference_baseline_tie_size,
        sep="",
    )
    print("top_global_features")
    for item in report.ranked_features[:12]:
        print(item.model_dump(mode="json"))
    print("best_reference_splitters")
    for item in sorted(
        report.ranked_features,
        key=lambda value: (
            value.reference_tie_size_after_feature,
            -value.incremental_uniform_bits,
            value.feature_id,
        ),
    )[:12]:
        print(item.model_dump(mode="json"))
    print(args.output)


if __name__ == "__main__":
    main()
