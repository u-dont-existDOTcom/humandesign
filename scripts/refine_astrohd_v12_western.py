#!/usr/bin/env python3
"""Minute-refine the frozen top hourly AstroHD V1.2 Western neighborhoods."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from score_astrohd_v12_western_regression import (
    _direct_snapshot,
    _load,
    _parse_iso,
)

from hdmatch.evaluation.astrohd_v12_western import (
    feature_mask,
    score_western_candidate,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ranking", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--behavior", required=True, type=Path)
    parser.add_argument("--ephemeris-root", required=True, type=Path)
    parser.add_argument("--top-hours", type=int, default=10)
    parser.add_argument("--window-hours", type=int, default=12)
    parser.add_argument("--recorded-time", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ranking = _load(args.ranking)
    registry = _load(args.registry)
    model = _load(args.model)
    behavior = _load(args.behavior)
    prevalence = ranking["feature_prevalence"]
    behavioral_confidence = {
        row["historical_cluster"]: (
            float(row["behavioral_confidence"]) if row["relation"] == "supported" else 0.0
        )
        for row in behavior["translations"]
    }
    top = ranking["universe_ranking"]["top_candidates"][: args.top_hours]
    windows = _merge_windows(
        [
            (
                _parse_iso(row["timestamp"]) - timedelta(hours=args.window_hours),
                _parse_iso(row["timestamp"]) + timedelta(hours=args.window_hours),
            )
            for row in top
        ]
    )
    latitude = float(registry["astronomy"]["owner_development_location"]["latitude"])
    longitude = float(registry["astronomy"]["owner_development_location"]["longitude"])
    recorded = _parse_iso(args.recorded_time)

    rows: list[dict[str, Any]] = []
    for start, end in windows:
        current = start
        while current <= end:
            snapshot = _direct_snapshot(
                current,
                registry=registry,
                latitude=latitude,
                longitude=longitude,
                ephemeris_root=args.ephemeris_root,
            )
            matches = {
                feature_id: bool(
                    feature_mask(
                        feature_id,
                        registry=registry,
                        longitudes=snapshot["longitudes"],
                        houses=snapshot["houses"],
                        ascendant=snapshot["ascendant"],
                        midheaven=snapshot["midheaven"],
                    )[0]
                )
                for feature_id in registry["features"]
            }
            score, _ = score_western_candidate(
                feature_matches=matches,
                feature_prevalence=prevalence,
                clusters=model["clusters"],
                behavioral_confidence=behavioral_confidence,
            )
            rows.append(
                {
                    "timestamp": current,
                    "score": float(score),
                    "matched_features": tuple(
                        sorted(key for key, value in matches.items() if value)
                    ),
                }
            )
            current += timedelta(minutes=1)

    plateaus = _plateaus(rows)
    max_score = max(row["score"] for row in rows)
    best = [row for row in rows if row["score"] == max_score]
    recorded_row = next(row for row in rows if row["timestamp"] == recorded)
    recorded_score = recorded_row["score"]
    recorded_plateau = next(
        plateau
        for plateau in plateaus
        if plateau["start"] <= recorded <= plateau["end"]
    )
    local_zone_name = "America/New_York"
    local_zone = ZoneInfo(local_zone_name)
    recorded_local_date = recorded.astimezone(local_zone).date()
    jan29 = [
        row
        for row in rows
        if row["timestamp"].astimezone(local_zone).date() == recorded_local_date
    ]
    jan29_max = max(row["score"] for row in jan29)
    jan29_best = [row for row in jan29 if row["score"] == jan29_max]

    report = {
        "schema": "astrohd-v1.2-western-minute-refinement-v1",
        "claim_scope": "post_result_development_not_validation",
        "ranking_sha256": _sha256(args.ranking),
        "registry_sha256": _sha256(args.registry),
        "model_sha256": _sha256(args.model),
        "behavior_sha256": _sha256(args.behavior),
        "top_hours_refined": args.top_hours,
        "window_hours_each_side": args.window_hours,
        "merged_windows": [
            {"start": start.isoformat(), "end": end.isoformat()}
            for start, end in windows
        ],
        "minute_count": len(rows),
        "global_refined_max_score": max_score,
        "global_refined_best_minutes": [
            row["timestamp"].isoformat() for row in best
        ],
        "recorded": {
            "timestamp": recorded.isoformat(),
            "score": recorded_score,
            "best_rank": 1 + sum(row["score"] > recorded_score for row in rows),
            "worst_rank": sum(row["score"] >= recorded_score for row in rows),
            "plateau_start": recorded_plateau["start"].isoformat(),
            "plateau_end": recorded_plateau["end"].isoformat(),
            "plateau_score": recorded_plateau["score"],
            "in_global_best_plateau": recorded_score == max_score,
        },
        "jan29": {
            "local_timezone": local_zone_name,
            "local_date": recorded_local_date.isoformat(),
            "max_score": jan29_max,
            "best_minutes": [row["timestamp"].isoformat() for row in jan29_best],
            "recorded_is_best": recorded_score == jan29_max,
        },
        "top_plateaus": [
            {
                "start": plateau["start"].isoformat(),
                "end": plateau["end"].isoformat(),
                "score": plateau["score"],
            }
            for plateau in sorted(
                plateaus,
                key=lambda row: (-row["score"], row["start"]),
            )[:30]
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _merge_windows(windows):
    ordered = sorted(windows)
    merged = []
    for start, end in ordered:
        if not merged or start > merged[-1][1] + timedelta(minutes=1):
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return [(start, end) for start, end in merged]


def _plateaus(rows):
    ordered = sorted(rows, key=lambda row: row["timestamp"])
    plateaus = []
    start = ordered[0]["timestamp"]
    previous = ordered[0]
    score = ordered[0]["score"]
    for row in ordered[1:]:
        contiguous = row["timestamp"] == previous["timestamp"] + timedelta(minutes=1)
        if not contiguous or row["score"] != score:
            plateaus.append({"start": start, "end": previous["timestamp"], "score": score})
            start = row["timestamp"]
            score = row["score"]
        previous = row
    plateaus.append({"start": start, "end": previous["timestamp"], "score": score})
    return plateaus


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    main()
