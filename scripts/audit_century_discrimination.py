#!/usr/bin/env python3
"""Audit the theoretical discrimination ceiling of the frozen symbolic model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.discrimination import audit_century_discrimination
from hdmatch.model.mapping_library import load_mapping_library
from hdmatch.runtime.century_cache import CenturyCacheManifest, load_century_candidate_states


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--mapping-library", required=True, type=Path)
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
    library = load_mapping_library(args.mapping_library)
    report = audit_century_discrimination(states, manifest, library)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "intervals=", report.cache_interval_count,
        " canonical_fingerprints=", report.canonical_answers.unique_fingerprints,
        " scoring_fingerprints=", report.scoring_rules.unique_fingerprints,
        " full_structures=", report.full_cached_structure.unique_fingerprints,
        sep="",
    )


if __name__ == "__main__":
    main()
