#!/usr/bin/env python3
"""Measure the secondary nodal environment/perspective layer on the century cache."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hdmatch.evaluation.holistic_profile_information import load_legacy_v36_model
from hdmatch.evaluation.nodal_environment_v2 import (
    audit_nodal_environment_v2,
    load_nodal_environment_v2_items,
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
        "--gate-catalog",
        type=Path,
        default=Path("reference/core/mapping_v2_gate_catalog.json"),
    )
    parser.add_argument(
        "--nodal-roles",
        type=Path,
        default=Path("reference/core/mapping_v2_nodal_environment_roles.json"),
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
    items = load_nodal_environment_v2_items(
        gate_catalog_path=args.gate_catalog,
        nodal_roles_path=args.nodal_roles,
    )
    report = audit_nodal_environment_v2(states, manifest, model, items)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "items=",
        report.generated_item_count,
        " primary_bits=",
        f"{report.primary.uniform_information_bits:.6f}",
        " combined_bits=",
        f"{report.primary_plus_nodes.uniform_information_bits:.6f}",
        " unique=",
        report.primary_plus_nodes.unique_fingerprints,
        "/",
        report.cache_interval_count,
        " exact=",
        report.exact_interval_identity_reached,
        sep="",
    )
    print("family_metrics")
    for item in sorted(
        report.family_metrics,
        key=lambda value: -value.incremental_uniform_bits,
    ):
        print(item.model_dump(mode="json"))
    print(args.output)


if __name__ == "__main__":
    main()
