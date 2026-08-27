#!/usr/bin/env python3
"""Merge verified exact century-cache segments into one canonical global cache."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.runtime.century_cache import (
    GlobalCandidateState,
    _load_verified_global_states,
    verify_century_cache,
    write_verified_century_cache,
)
from hdmatch.runtime.chart_adapter import ExactChartAdapter
from hdmatch.util import sha256_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris", required=True)
    parser.add_argument("--inputs-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--generation-commit", required=True)
    return parser.parse_args()


def _state_id(start: datetime, end: datetime, stable_hash: str) -> str:
    return "STATE-" + sha256_json(
        {
            "start_utc": start.isoformat(),
            "end_utc": end.isoformat(),
            "stable_feature_sha256": stable_hash,
        }
    )[:24].upper()


def _merged_state(
    adapter: ExactChartAdapter,
    left: GlobalCandidateState,
    right: GlobalCandidateState,
) -> GlobalCandidateState:
    if left.end_utc != right.start_utc:
        raise ValueError("cannot merge non-contiguous exact states")
    if left.chart_features_hash != right.chart_features_hash:
        raise ValueError("cannot merge states with different stable features")
    start = left.start_utc
    end = right.end_utc
    representative = start + (end - start) / 2
    chart = adapter.calculate(representative)
    stable_hash = left.chart_features_hash
    observed_hash = chart.engine_metadata.get("stable_feature_sha256")
    if observed_hash != stable_hash:
        raise ValueError(
            "merged representative chart does not reproduce the stable feature hash"
        )
    return GlobalCandidateState(
        state_id=_state_id(start, end, stable_hash),
        start_utc=start,
        end_utc=end,
        chart_features_hash=stable_hash,
        chart_features=chart,
        boundary_events=left.boundary_events + right.boundary_events,
    )


def main() -> None:
    args = parse_args()
    adapter = ExactChartAdapter(args.ephemeris)
    manifest_paths = sorted(args.inputs_root.glob("*/manifest.json"))
    if not manifest_paths:
        raise SystemExit(f"no verified shard manifests found under {args.inputs_root}")

    parts: list[tuple[datetime, Path, tuple[GlobalCandidateState, ...]]] = []
    for manifest_path in manifest_paths:
        cache_dir = manifest_path.parent
        manifest = verify_century_cache(
            cache_dir,
            expected_engine_fingerprint=adapter.fingerprint,
        )
        states = _load_verified_global_states(cache_dir, manifest)
        parts.append((manifest.utc_start, cache_dir, states))
        print(
            "verified_segment",
            cache_dir.name,
            manifest.utc_start.isoformat(),
            manifest.utc_end_exclusive.isoformat(),
            manifest.interval_count,
            manifest.canonical_rows_sha256,
            flush=True,
        )

    parts.sort(key=lambda item: item[0])
    merged: list[GlobalCandidateState] = []
    for _, cache_dir, states in parts:
        if not merged:
            merged.extend(states)
            continue
        if merged[-1].end_utc != states[0].start_utc:
            raise ValueError(
                f"segment gap/overlap before {cache_dir}: "
                f"{merged[-1].end_utc.isoformat()} != {states[0].start_utc.isoformat()}"
            )
        if merged[-1].chart_features_hash == states[0].chart_features_hash:
            merged[-1] = _merged_state(adapter, merged[-1], states[0])
            merged.extend(states[1:])
        else:
            merged.extend(states)

    final_states = tuple(merged)
    manifest = write_verified_century_cache(
        args.output,
        final_states,
        engine_fingerprint=adapter.fingerprint,
        generation_commit=args.generation_commit,
        created_at_utc=datetime.now(UTC),
        shard_years=10,
    )
    print("final_interval_count", manifest.interval_count, flush=True)
    print("final_range", manifest.utc_start.isoformat(), manifest.utc_end_exclusive.isoformat())
    print("final_canonical_rows_sha256", manifest.canonical_rows_sha256, flush=True)
    print("final_manifest", args.output / "manifest.json", flush=True)


if __name__ == "__main__":
    main()
