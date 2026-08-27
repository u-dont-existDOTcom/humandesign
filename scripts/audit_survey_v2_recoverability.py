#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.survey_v2_recoverability import audit_perfect_match_recoverability
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
    manifest = CenturyCacheManifest.model_validate_json(
        (args.cache / "manifest.json").read_text(encoding="utf-8")
    )
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    model = load_legacy_v36_model(args.base_mapping, args.overlay)
    report = audit_perfect_match_recoverability(states, model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("candidate_count", report.candidate_count)
    print("rank1_count", report.recovered_rank1_count)
    print("all_unique", report.all_candidates_uniquely_recovered)
    print("maximum_questions", report.maximum_questions_asked)
    print(args.output)
    if not report.all_candidates_uniquely_recovered:
        raise SystemExit("perfect-match recoverability gate failed")


if __name__ == "__main__":
    main()
