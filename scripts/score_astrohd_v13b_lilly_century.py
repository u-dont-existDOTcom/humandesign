#!/usr/bin/env python3
"""Run the owner-requested post-selection Lilly-only century scan."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import numpy as np
import swisseph as swe

from hdmatch.evaluation.astrohd_v12_western import assign_houses
from hdmatch.evaluation.astrohd_v13_traditions import (
    BODY_IDS,
    behavior_weight_variants,
    build_snapshot,
)
from hdmatch.evaluation.astrohd_v13b_lilly_century import (
    lilly_strength_arrays,
    lilly_universe_scores,
)
from hdmatch.evaluation.astrohd_v13b_native import PLANETS, score_lilly_native

BODY_ID_ORDER = tuple(BODY_IDS[planet] for planet in PLANETS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--consensus-map", required=True, type=Path)
    parser.add_argument("--behavior", required=True, type=Path)
    parser.add_argument("--crosswalk", required=True, type=Path)
    parser.add_argument("--ephemeris-root", required=True, type=Path)
    parser.add_argument("--universe-start", required=True)
    parser.add_argument("--universe-end", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--persistent-competitor", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--top", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    freeze_text = args.freeze.read_text()
    consensus = _load(args.consensus_map)
    behavior = _load(args.behavior)
    crosswalk = _load(args.crosswalk)
    weights = behavior_weight_variants(behavior, crosswalk)

    start = _parse_iso(args.universe_start)
    end = _parse_iso(args.universe_end)
    jds = _hourly_jds(start, end)
    n = len(jds)
    if n != 876_601:
        raise ValueError(f"unexpected frozen century candidate count: {n}")

    latitude = 39.9526
    longitude = -75.1652
    longitudes, speeds, cusps = _exact_century_arrays(
        jds,
        latitude=latitude,
        longitude=longitude,
        ephemeris_root=args.ephemeris_root,
    )
    houses = np.empty((len(PLANETS), n), dtype=np.int16)
    for planet_index in range(len(PLANETS)):
        houses[planet_index] = assign_houses(
            longitudes[planet_index],
            cusps,
        ).astype(np.int16)
    day_chart = np.isin(houses[0], np.asarray((7, 8, 9, 10, 11, 12), dtype=np.int16))
    strengths = lilly_strength_arrays(
        longitudes=longitudes,
        speeds=speeds,
        houses=houses,
        day_chart=day_chart,
    )

    exact_times = {
        "target": _parse_iso(args.target),
        "persistent_competitor": _parse_iso(args.persistent_competitor),
    }
    exact_snapshots = {
        label: build_snapshot(
            when,
            latitude=latitude,
            longitude=longitude,
            ephemeris_root=args.ephemeris_root,
        )
        for label, when in exact_times.items()
    }

    specs: dict[str, Any] = {}
    for aggregation in ("domain_mean_nonstack", "significator_stack"):
        for weight_name, domain_weights in weights.items():
            spec_id = f"{aggregation}__{weight_name}"
            universe_scores = lilly_universe_scores(
                strengths=strengths,
                cusp_longitudes=cusps,
                consensus_map=consensus,
                behavior_weights=domain_weights,
                aggregation=aggregation,
            )
            exact_scores = {
                label: float(
                    score_lilly_native(
                        snapshot,
                        consensus_map=consensus,
                        behavior_weights=domain_weights,
                        aggregation=aggregation,
                    )["total"]
                )
                for label, snapshot in exact_snapshots.items()
            }
            specs[spec_id] = _summarize_spec(
                universe_scores=universe_scores,
                exact_scores=exact_scores,
                start=start,
                top=args.top,
            )

    report = {
        "schema": "astrohd-v1.3b-lilly-century-descriptive-v1",
        "classification": "owner_requested_post_selection_descriptive_not_validation",
        "freeze_sha256": hashlib.sha256(freeze_text.encode()).hexdigest(),
        "consensus_map_sha256": _sha256(args.consensus_map),
        "behavior_sha256": _sha256(args.behavior),
        "crosswalk_sha256": _sha256(args.crosswalk),
        "universe": {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "candidate_count": n,
            "cadence_hours": 1,
            "location": {
                "name": "Philadelphia",
                "latitude": latitude,
                "longitude": longitude,
            },
            "ephemeris": "Swiss Ephemeris local-file SWIEPH exact hourly positions/speeds",
            "houses": "Regiomontanus exact hourly cusps",
        },
        "exact_queries": {
            label: when.isoformat() for label, when in exact_times.items()
        },
        "specifications": specs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _exact_century_arrays(
    jds: np.ndarray,
    *,
    latitude: float,
    longitude: float,
    ephemeris_root: Path,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(jds)
    longitudes = np.empty((len(PLANETS), n), dtype=np.float64)
    speeds = np.empty((len(PLANETS), n), dtype=np.float64)
    cusps = np.empty((n, 12), dtype=np.float64)
    flags = int(swe.FLG_SWIEPH) | int(swe.FLG_SPEED)
    swe.set_ephe_path(str(ephemeris_root))

    for candidate_index, jd in enumerate(jds):
        for planet_index, body_id in enumerate(BODY_ID_ORDER):
            values, returned = swe.calc_ut(float(jd), body_id, flags)
            if returned & int(swe.FLG_MOSEPH) or not returned & int(swe.FLG_SWIEPH):
                raise RuntimeError(
                    "Swiss Ephemeris fallback during Lilly century scan: "
                    f"candidate_index={candidate_index} planet={PLANETS[planet_index]} "
                    f"returned_flags={returned}"
                )
            longitudes[planet_index, candidate_index] = float(values[0]) % 360.0
            speeds[planet_index, candidate_index] = float(values[3])
        raw_cusps, _ascmc = swe.houses_ex(
            float(jd),
            latitude,
            longitude,
            b"R",
            0,
        )
        cusps[candidate_index, :] = raw_cusps[:12]

    return longitudes, speeds, cusps


def _summarize_spec(
    *,
    universe_scores: np.ndarray,
    exact_scores: dict[str, float],
    start: datetime,
    top: int,
) -> dict[str, Any]:
    exact_summary = {}
    for label, score in exact_scores.items():
        exact_summary[label] = {
            "score": score,
            "best_rank_vs_hourly": int(np.count_nonzero(universe_scores > score) + 1),
            "worst_rank_vs_hourly": int(np.count_nonzero(universe_scores >= score)),
            "hourly_strictly_above_count": int(np.count_nonzero(universe_scores > score)),
            "hourly_equal_count": int(np.count_nonzero(universe_scores == score)),
        }

    top_count = min(top, len(universe_scores))
    top_indices = np.argpartition(universe_scores, -top_count)[-top_count:]
    top_indices = top_indices[np.argsort(universe_scores[top_indices])[::-1]]

    local_zone = ZoneInfo("America/New_York")
    local_day = date(1985, 1, 29)
    local_start = datetime(1985, 1, 29, 0, 0, tzinfo=local_zone).astimezone(UTC)
    local_end = datetime(1985, 1, 30, 0, 0, tzinfo=local_zone).astimezone(UTC)
    first = max(0, int(np.ceil((local_start - start).total_seconds() / 3600.0)))
    stop = min(
        len(universe_scores),
        int(np.ceil((local_end - start).total_seconds() / 3600.0)),
    )
    local_indices = np.arange(first, stop, dtype=int)
    local_timestamps = [start + timedelta(hours=int(index)) for index in local_indices]
    local_mask = np.asarray(
        [timestamp.astimezone(local_zone).date() == local_day for timestamp in local_timestamps]
    )
    local_indices = local_indices[local_mask]
    if len(local_indices) == 0:
        raise RuntimeError("no hourly candidates found on Philadelphia-local date 1985-01-29")
    local_scores = universe_scores[local_indices]
    local_max = float(np.max(local_scores))
    local_best_indices = local_indices[local_scores == local_max]

    return {
        "exact_queries": exact_summary,
        "distinct_score_count": int(len(np.unique(universe_scores))),
        "global_max_score": float(np.max(universe_scores)),
        "top_candidates": [
            {
                "timestamp": (start + timedelta(hours=int(index))).isoformat(),
                "score": float(universe_scores[index]),
            }
            for index in top_indices
        ],
        "best_recorded_local_date_hourly": {
            "local_date": "1985-01-29",
            "score": local_max,
            "timestamps": [
                (start + timedelta(hours=int(index))).isoformat()
                for index in local_best_indices
            ],
        },
    }


def _hourly_jds(start: datetime, end: datetime) -> np.ndarray:
    start_jd = _datetime_to_jd(start)
    end_jd = _datetime_to_jd(end)
    count = round((end_jd - start_jd) * 24.0) + 1
    values = start_jd + np.arange(count, dtype=np.float64) / 24.0
    if abs(values[-1] - end_jd) > 1e-7:
        raise ValueError("hourly universe endpoints are not integral hours apart")
    return values


def _datetime_to_jd(value: datetime) -> float:
    utc = value.astimezone(UTC)
    hour = (
        utc.hour
        + utc.minute / 60.0
        + utc.second / 3600.0
        + utc.microsecond / 3.6e9
    )
    return float(swe.julday(utc.year, utc.month, utc.day, hour, swe.GREG_CAL))


def _parse_iso(raw: str) -> datetime:
    value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must include timezone")
    return value


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    main()
