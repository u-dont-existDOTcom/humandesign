#!/usr/bin/env python3
"""Build the reusable exact-state century candidate cache.

This is intentionally a one-time/manual build. It uses the production exact chart
adapter, not the coarse broad-scan ephemeris cache, so every output row is a complete
stable CandidateState with exact 88-degree Design timing and pinned ephemeris
provenance. The generated cache is timezone-neutral; participant local-date overlaps
are attached when it is loaded.
"""

from __future__ import annotations

import argparse
import os
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.runtime.century_cache import GlobalCandidateState, write_verified_century_cache
from hdmatch.runtime.chart_adapter import ExactChartAdapter

DEFAULT_START = datetime(1926, 8, 22, tzinfo=UTC)
DEFAULT_END = datetime(2026, 8, 23, tzinfo=UTC)


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError("timestamps must include a UTC offset")
    return parsed.astimezone(UTC)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris", required=True, help="Pinned Swiss .se1 file/directory")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--start", type=_utc, default=DEFAULT_START)
    parser.add_argument("--end-exclusive", type=_utc, default=DEFAULT_END)
    parser.add_argument("--shard-years", type=int, default=10)
    parser.add_argument(
        "--generation-commit",
        default=os.environ.get("GITHUB_SHA", "unknown"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.end_exclusive <= args.start:
        raise SystemExit("--end-exclusive must be after --start")

    adapter = ExactChartAdapter(args.ephemeris)
    print("engine_fingerprint", adapter.fingerprint, flush=True)
    print("building_exact_states", args.start.isoformat(), args.end_exclusive.isoformat(), flush=True)
    candidates = adapter.candidate_states(args.start, args.end_exclusive, "UTC")
    print("exact_interval_count", len(candidates), flush=True)

    global_states = tuple(
        GlobalCandidateState(
            state_id=state.state_id,
            start_utc=state.start_utc,
            end_utc=state.end_utc,
            chart_features_hash=state.chart_features_hash,
            chart_features=state.chart_features,
            boundary_events=state.boundary_events,
        )
        for state in candidates
    )
    manifest = write_verified_century_cache(
        args.output,
        global_states,
        engine_fingerprint=adapter.fingerprint,
        generation_commit=args.generation_commit,
        created_at_utc=datetime.now(UTC),
        shard_years=args.shard_years,
    )
    print("cache_version", manifest.cache_version, flush=True)
    print("interval_count", manifest.interval_count, flush=True)
    print("canonical_rows_sha256", manifest.canonical_rows_sha256, flush=True)
    print("manifest", args.output / "manifest.json", flush=True)


if __name__ == "__main__":
    main()
