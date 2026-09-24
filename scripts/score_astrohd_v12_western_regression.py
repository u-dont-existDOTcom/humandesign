#!/usr/bin/env python3
"""Compute frozen AstroHD V1.2 Western prevalence and direct regression scores."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import struct
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import swisseph as swe

from hdmatch.evaluation.astrohd_v12_western import (
    assign_houses,
    feature_mask,
    score_western_candidate,
    score_western_universe,
)

BODY_IDS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--behavior", required=True, type=Path)
    parser.add_argument("--cache-dir", required=True, type=Path)
    parser.add_argument("--universe-start", required=True)
    parser.add_argument("--universe-end", required=True)
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--rank-universe", action="store_true")
    parser.add_argument("--top", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registry = _load(args.registry)
    model = _load(args.model)
    behavior = _load(args.behavior)
    manifest = _load(args.cache_dir / "manifest.json")
    _validate_cache_manifest(manifest)
    start = _parse_iso(args.universe_start)
    end = _parse_iso(args.universe_end)
    jds = _hourly_jds(start, end)
    longitudes = {
        body: _interpolate_cache(
            args.cache_dir / f"{body}.d2xz",
            cache_start_jd=float(manifest["start_jd"]),
            target_jds=jds,
        )
        for body in BODY_IDS
    }
    latitude = float(registry["astronomy"]["owner_development_location"]["latitude"])
    longitude = float(registry["astronomy"]["owner_development_location"]["longitude"])
    ephemeris_root = args.cache_dir.parent
    cusps, ascendant, midheaven = _house_arrays(jds, latitude=latitude, longitude=longitude)
    needed_house_bodies = {
        spec["body"]
        for spec in registry["features"].values()
        if spec["type"] in {"house", "angular_house"}
    }
    houses = {
        body: assign_houses(longitudes[body], cusps)
        for body in sorted(needed_house_bodies)
    }

    feature_masks: dict[str, np.ndarray] = {}
    prevalence: dict[str, float] = {}
    for feature_id in registry["features"]:
        mask = feature_mask(
            feature_id,
            registry=registry,
            longitudes=longitudes,
            houses=houses,
            ascendant=ascendant,
            midheaven=midheaven,
        )
        feature_masks[feature_id] = mask
        prevalence[feature_id] = float(np.count_nonzero(mask) / len(mask))

    behavioral_confidence = {
        row["historical_cluster"]: (
            float(row["behavioral_confidence"]) if row["relation"] == "supported" else 0.0
        )
        for row in behavior["translations"]
    }
    queries = []
    for raw in args.query:
        label, sep, timestamp = raw.partition("=")
        if not sep:
            raise ValueError("--query must use LABEL=ISO_TIMESTAMP")
        query_dt = _parse_iso(timestamp)
        snapshot = _direct_snapshot(
            query_dt,
            registry=registry,
            latitude=latitude,
            longitude=longitude,
            ephemeris_root=ephemeris_root,
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
        total, breakdown = score_western_candidate(
            feature_matches=matches,
            feature_prevalence=prevalence,
            clusters=model["clusters"],
            behavioral_confidence=behavioral_confidence,
        )
        queries.append(
            {
                "label": label,
                "timestamp": query_dt.isoformat(),
                "score": total,
                "breakdown": breakdown,
                "matched_features": sorted(key for key, value in matches.items() if value),
            }
        )

    universe_ranking = None
    if args.rank_universe:
        universe_scores = score_western_universe(
            feature_masks=feature_masks,
            feature_prevalence=prevalence,
            clusters=model["clusters"],
            behavioral_confidence=behavioral_confidence,
        )
        for query in queries:
            query_score = float(query["score"])
            query["best_rank_vs_hourly"] = int(np.count_nonzero(universe_scores > query_score) + 1)
            query["worst_rank_vs_hourly"] = int(np.count_nonzero(universe_scores >= query_score))
        top_count = min(args.top, len(universe_scores))
        top_indices = np.argpartition(universe_scores, -top_count)[-top_count:]
        top_indices = top_indices[np.argsort(universe_scores[top_indices])[::-1]]
        universe_ranking = {
            "top_candidates": [
                {
                    "timestamp": (start + timedelta(hours=int(index))).isoformat(),
                    "score": float(universe_scores[index]),
                }
                for index in top_indices
            ],
            "distinct_score_count": int(len(np.unique(universe_scores))),
        }

    report = {
        "schema": "astrohd-v1.2-western-direct-regression-v1",
        "claim_scope": "post_result_development_not_validation",
        "universe": {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "hourly_candidate_count": len(jds),
        },
        "registry_sha256": _sha256(args.registry),
        "model_sha256": _sha256(args.model),
        "behavior_sha256": _sha256(args.behavior),
        "cache_manifest_sha256": _sha256(args.cache_dir / "manifest.json"),
        "feature_prevalence": prevalence,
        "queries": queries,
        "universe_ranking": universe_ranking,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _direct_snapshot(
    when: datetime,
    *,
    registry: dict[str, Any],
    latitude: float,
    longitude: float,
    ephemeris_root: Path,
) -> dict[str, Any]:
    jd = _datetime_to_jd(when)
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    swe.set_ephe_path(str(ephemeris_root))
    direct_longitudes: dict[str, float] = {}
    for body, body_id in BODY_IDS.items():
        values, returned_flags = swe.calc_ut(jd, body_id, flags)
        if returned_flags & swe.FLG_MOSEPH or not returned_flags & swe.FLG_SWIEPH:
            raise RuntimeError(
                f"Swiss Ephemeris fallback for {body} at {when.isoformat()}: "
                f"returned_flags={returned_flags}"
            )
        direct_longitudes[body] = float(values[0]) % 360.0
    longitudes = {
        body: np.asarray([value])
        for body, value in direct_longitudes.items()
    }
    raw_cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b"P", 0)
    cusps = np.asarray([raw_cusps[:12]], dtype=float)
    houses = {
        body: assign_houses(values, cusps)
        for body, values in longitudes.items()
    }
    return {
        "longitudes": longitudes,
        "houses": houses,
        "ascendant": np.asarray([float(ascmc[0]) % 360.0]),
        "midheaven": np.asarray([float(ascmc[1]) % 360.0]),
    }


def _house_arrays(
    jds: np.ndarray,
    *,
    latitude: float,
    longitude: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cusps = np.empty((len(jds), 12), dtype=np.float64)
    asc = np.empty(len(jds), dtype=np.float64)
    mc = np.empty(len(jds), dtype=np.float64)
    for index, jd in enumerate(jds):
        raw_cusps, ascmc = swe.houses_ex(float(jd), latitude, longitude, b"P", 0)
        cusps[index, :] = raw_cusps[:12]
        asc[index] = float(ascmc[0]) % 360.0
        mc[index] = float(ascmc[1]) % 360.0
    return cusps, asc, mc


def _hourly_jds(start: datetime, end: datetime) -> np.ndarray:
    start_jd = _datetime_to_jd(start)
    end_jd = _datetime_to_jd(end)
    count = round((end_jd - start_jd) * 24.0) + 1
    values = start_jd + np.arange(count, dtype=np.float64) / 24.0
    if abs(values[-1] - end_jd) > 1e-7:
        raise ValueError("hourly universe endpoints are not integral hours apart")
    return values


def _datetime_to_jd(value: datetime) -> float:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    utc = value.astimezone(UTC).replace(tzinfo=None)
    hour = (
        utc.hour
        + utc.minute / 60.0
        + utc.second / 3600.0
        + utc.microsecond / 3.6e9
    )
    return float(swe.julday(utc.year, utc.month, utc.day, hour, swe.GREG_CAL))


def _interpolate_cache(
    path: Path,
    *,
    cache_start_jd: float,
    target_jds: np.ndarray,
) -> np.ndarray:
    raw = lzma.decompress(path.read_bytes())
    q0, d1, n, step = struct.unpack("<qiId", raw[:24])
    dd = np.frombuffer(raw[24:], dtype="<i4").astype(np.int64)
    d = np.empty(n - 1, dtype=np.int64)
    d[0] = d1
    if n > 2:
        d[1:] = d1 + np.cumsum(dd)
    q = np.empty(n, dtype=np.int64)
    q[0] = q0
    q[1:] = q0 + np.cumsum(d)
    series = ((q / 1e5) % 360).astype(np.float64)
    x = (target_jds - cache_start_jd) * 24.0 / step
    index = np.floor(x).astype(int)
    fraction = x - index
    endpoint = np.isclose(x, len(series) - 1, atol=1e-9)
    invalid = (index < 0) | ((index >= len(series) - 1) & ~endpoint)
    if np.any(invalid):
        raise ValueError(f"requested universe exceeds cache bounds for {path.name}")
    safe_index = np.minimum(index, len(series) - 2)
    left = series[safe_index]
    right = series[safe_index + 1]
    delta = ((right - left + 180.0) % 360.0) - 180.0
    result = (left + fraction * delta) % 360.0
    result[endpoint] = series[-1]
    return result


def _validate_cache_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("ephemeris_returned") != "SWIEPH":
        raise ValueError("V1.2 requires a Swiss-file ephemeris cache")
    flags = int(manifest.get("flags", 0))
    if flags & int(swe.FLG_MOSEPH) or not flags & int(swe.FLG_SWIEPH):
        raise ValueError(f"V1.2 cache flags are not Swiss-file backed: {flags}")


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
