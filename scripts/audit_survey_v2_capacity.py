#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_capacity import audit_survey_v2_capacity
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
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
    manifest = CenturyCacheManifest.model_validate(
        json.loads((args.cache / "manifest.json").read_text(encoding="utf-8"))
    )
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    report = audit_survey_v2_capacity(states, model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("baseline_bits", f"{report.baseline.uniform_information_bits:.6f}")
    print("joint_bits", f"{report.joint_target.uniform_information_bits:.6f}")
    print("incremental_bits", f"{report.incremental_uniform_bits:.6f}")
    print("remaining_gap", f"{report.remaining_identity_gap_bits:.6f}")
    print("top1_ceiling", f"{report.joint_target.uniform_top1_ceiling:.6f}")
    print("reference_tie", report.reference_1985_joint_tie_size)
    print("greedy")
    for step in report.greedy_target_sequence:
        print(step.model_dump(mode="json"))
    print(args.output)


if __name__ == "__main__":
    main()
