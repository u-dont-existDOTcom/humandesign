#!/usr/bin/env python3
"""Measure information capacity of the frozen V3.6 holistic profile model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from hdmatch.evaluation.holistic_profile_information import (
    audit_v36_holistic_profile_information,
    load_legacy_v36_model,
)
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
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("reference/core/behavioral_target_combined_v3_6.md"),
    )
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    report = audit_v36_holistic_profile_information(
        states,
        manifest,
        model,
        base_mapping_sha256=sha256_path(args.base_mapping),
        overlay_sha256=sha256_path(args.overlay),
        target_sha256=sha256_path(args.target),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for label, variant in (
        ("clean", report.clean_variant),
        ("best_current", report.best_current_variant),
    ):
        print(
            label,
            "observables=",
            variant.observable_count,
            "observable_bits=",
            f"{variant.observable_fingerprint.uniform_information_bits:.6f}",
            "observable_groups=",
            variant.observable_fingerprint.unique_fingerprints,
            "reference_1985_bits=",
            f"{variant.reference_1985_observable.uniform_information_bits:.6f}",
            "reference_1985_tie=",
            variant.reference_1985_observable.tie_size,
            "pathway_bits=",
            f"{variant.mapping_pathway_fingerprint.uniform_information_bits:.6f}",
        )
    print("greedy_clean_first_15")
    for step in report.clean_variant.greedy_observable_sequence[:15]:
        print(step.model_dump(mode="json"))
    print(args.output)


if __name__ == "__main__":
    main()
