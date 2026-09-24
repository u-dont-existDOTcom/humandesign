#!/usr/bin/env python3
"""Run the frozen AstroHD V1.3 tradition-grounded direct regression."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import swisseph as swe

from hdmatch.evaluation.astrohd_v12_western import assign_houses
from hdmatch.evaluation.astrohd_v13_tradition import Snapshot, score_candidate_detailed

BODY_IDS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--consensus-map", required=True, type=Path)
    parser.add_argument("--behavior", required=True, type=Path)
    parser.add_argument("--crosswalk", required=True, type=Path)
    parser.add_argument("--ephemeris-root", required=True, type=Path)
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    freeze = _load(args.freeze)
    consensus = _load(args.consensus_map)
    behavior = _load(args.behavior)
    crosswalk = _load(args.crosswalk)

    behavioral_confidence = _behavioral_confidence(behavior, crosswalk)
    location = freeze["astronomy"]["location"]
    latitude = float(location["latitude"])
    longitude = float(location["longitude"])

    queries = []
    for raw in args.query:
        label, sep, timestamp = raw.partition("=")
        if not sep:
            raise ValueError("--query must use LABEL=ISO_TIMESTAMP")
        when = _parse_iso(timestamp)
        snapshot = _snapshot(
            when,
            ephemeris_root=args.ephemeris_root,
            latitude=latitude,
            longitude=longitude,
        )
        detailed = score_candidate_detailed(
            snapshot=snapshot,
            consensus_map=consensus,
            behavioral_confidence=behavioral_confidence,
        )
        queries.append(
            {
                "label": label,
                "timestamp": when.isoformat(),
                "scores": detailed["scores"],
                "domains": detailed["domains"],
                "chart_context": {
                    "is_day_chart": snapshot.is_day_chart,
                    "tropical_ascendant": snapshot.tropical_ascendant,
                    "sidereal_ascendant_lahiri": snapshot.sidereal_ascendant,
                },
            }
        )

    report = {
        "schema": "astrohd-v1.3-tradition-grounded-direct-regression-v1",
        "classification": "owner_post_result_development_not_validation",
        "freeze_sha256": _sha256(args.freeze),
        "consensus_map_sha256": _sha256(args.consensus_map),
        "behavior_sha256": _sha256(args.behavior),
        "crosswalk_sha256": _sha256(args.crosswalk),
        "ephemeris_manifest_sha256": _sha256(args.ephemeris_root / "manifest.json"),
        "behavioral_confidence": behavioral_confidence,
        "queries": queries,
        "direct_regression": _classify_direct_regression(queries),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)


def _snapshot(
    when: datetime,
    *,
    ephemeris_root: Path,
    latitude: float,
    longitude: float,
) -> Snapshot:
    jd = _datetime_to_jd(when)
    swe.set_ephe_path(str(ephemeris_root))
    tropical_flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    tropical_longitudes: dict[str, float] = {}
    tropical_speeds: dict[str, float] = {}
    for body, body_id in BODY_IDS.items():
        values, returned = swe.calc_ut(jd, body_id, tropical_flags)
        _require_swieph(returned, body, when)
        tropical_longitudes[body] = float(values[0]) % 360.0
        tropical_speeds[body] = float(values[3])

    regio_cusps_raw, regio_ascmc = swe.houses_ex(jd, latitude, longitude, b"R", 0)
    regio_cusps = tuple(float(value) % 360.0 for value in regio_cusps_raw[:12])
    cusp_array = np.asarray([regio_cusps], dtype=float)
    tropical_regio_houses = {
        body: int(
            assign_houses(
                np.asarray([longitude_value], dtype=float),
                cusp_array,
            )[0]
        )
        for body, longitude_value in tropical_longitudes.items()
    }
    is_day_chart = tropical_regio_houses["sun"] in {7, 8, 9, 10, 11, 12}

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    sidereal_flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
    sidereal_longitudes: dict[str, float] = {}
    sidereal_speeds: dict[str, float] = {}
    for body, body_id in BODY_IDS.items():
        values, returned = swe.calc_ut(jd, body_id, sidereal_flags)
        _require_swieph(returned, body, when)
        sidereal_longitudes[body] = float(values[0]) % 360.0
        sidereal_speeds[body] = float(values[3])

    _sid_cusps, sid_ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b"P",
        swe.FLG_SIDEREAL,
    )

    return Snapshot(
        tropical_longitudes=tropical_longitudes,
        tropical_speeds=tropical_speeds,
        tropical_regio_houses=tropical_regio_houses,
        tropical_regio_cusps=regio_cusps,
        tropical_ascendant=float(regio_ascmc[0]) % 360.0,
        sidereal_longitudes=sidereal_longitudes,
        sidereal_speeds=sidereal_speeds,
        sidereal_ascendant=float(sid_ascmc[0]) % 360.0,
        is_day_chart=is_day_chart,
    )


def _behavioral_confidence(
    behavior: dict[str, Any],
    crosswalk: dict[str, Any],
) -> dict[str, float]:
    cluster_to_domain = {
        row["historical_cluster"]: row["neutral_domain"]
        for row in crosswalk["historical_merged_cluster_crosswalk"]
    }
    result: dict[str, float] = {}
    for row in behavior["translations"]:
        cluster = row["historical_cluster"]
        domain = cluster_to_domain[cluster]
        confidence = (
            float(row["behavioral_confidence"])
            if row["relation"] == "supported"
            else 0.0
        )
        result[domain] = confidence
    return result


def _classify_direct_regression(queries: list[dict[str, Any]]) -> dict[str, Any]:
    by_label = {row["label"]: row for row in queries}
    target = by_label["target"]
    comparator = by_label["competitor2013"]
    alternatives = [row for row in queries if row["label"].startswith("same1985_")]

    families = (
        "domain_collapse_nonstack",
        "cross_tradition_convergence_stack",
        "raw_independent_testimony_stack",
    )
    family_results: dict[str, Any] = {}
    for family in families:
        variants = {}
        for weighting in ("equal", "confidence"):
            key = f"{family}__{weighting}"
            target_score = float(target["scores"][key])
            competitor_score = float(comparator["scores"][key])
            alt_scores = [float(row["scores"][key]) for row in alternatives]
            variants[weighting] = {
                "target_score": target_score,
                "competitor2013_score": competitor_score,
                "strongest_same_date_alternative_score": max(alt_scores),
                "target_strictly_beats_2013": target_score > competitor_score,
                "no_same_date_alternative_strictly_beats_target": max(alt_scores)
                <= target_score,
            }
        family_results[family] = {
            "variants": variants,
            "passes_both_weight_variants": all(
                row["target_strictly_beats_2013"]
                and row["no_same_date_alternative_strictly_beats_target"]
                for row in variants.values()
            ),
        }

    clean_passes = [
        name
        for name in ("domain_collapse_nonstack", "cross_tradition_convergence_stack")
        if family_results[name]["passes_both_weight_variants"]
    ]
    raw_pass = family_results["raw_independent_testimony_stack"][
        "passes_both_weight_variants"
    ]
    if len(clean_passes) >= 2:
        label = "robust_multi_family"
    elif clean_passes == ["cross_tradition_convergence_stack"]:
        label = "convergence_specific"
    elif clean_passes == ["domain_collapse_nonstack"]:
        label = "nonstack_specific"
    elif raw_pass:
        label = "raw_stack_only_warning"
    else:
        label = "direct_fail"

    return {
        "families": family_results,
        "clean_families_passing": clean_passes,
        "raw_family_passing": raw_pass,
        "robustness_label": label,
    }


def _require_swieph(returned_flags: int, body: str, when: datetime) -> None:
    if returned_flags & swe.FLG_MOSEPH or not returned_flags & swe.FLG_SWIEPH:
        raise RuntimeError(
            f"Swiss Ephemeris fallback for {body} at {when.isoformat()}: "
            f"returned_flags={returned_flags}"
        )


def _datetime_to_jd(value: datetime) -> float:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
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
