#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_completion import audit_survey_v2_completion
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
    report = audit_survey_v2_completion(states, model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("survey_v2_bits", f"{report.survey_v2_baseline.uniform_information_bits:.6f}")
    print("full_structure_bits", f"{report.full_cached_structure.uniform_information_bits:.6f}")
    print("full_structure_unique", report.cached_structure_can_uniquely_identify_all_states)
    print("greedy_completion")
    for step in report.greedy_completion:
        print(step.model_dump(mode="json"))
    print(args.output)


if __name__ == "__main__":
    main()
