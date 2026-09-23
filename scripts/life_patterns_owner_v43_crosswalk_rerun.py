#!/usr/bin/env python3
"""Run the frozen Life Patterns owner profile through the clean V4.3 crosswalk.

This is a development-only, post-freeze adapter. It does not modify the historical
V4.3 audit. The private translated profile is supplied with OWNER_V43_TRANSLATION.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import swieph_ab_rerun as base  # noqa: E402
import v43_profile_netinfo_rerun as runner  # noqa: E402
import v43_profile_netinfo_rerun_v2 as overlay_runner  # noqa: E402

REPO = SCRIPT_DIR.parent
TRANSLATION = Path(os.environ["OWNER_V43_TRANSLATION"]).resolve()
OUT = Path(os.environ.get("OWNER_V43_OUTPUT", "owner-v43-crosswalk-result.json")).resolve()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def translated_model() -> tuple[dict, dict]:
    model, base_path, overlay_path = overlay_runner.load_frozen_model()
    translation = json.loads(TRANSLATION.read_text(encoding="utf-8"))
    mapping_by_id = {item["id"]: item for item in model["mappings"] if not item.get("post_selection", False)}
    cluster_to_ids: dict[str, list[str]] = {}
    for item in mapping_by_id.values():
        cluster_to_ids.setdefault(item["cluster"], []).append(item["id"])

    selected_confidence: dict[str, float] = {}
    selected_rows: dict[str, list[str]] = {}
    contradiction_confidence: dict[str, float] = {}

    for row in translation["rows"]:
        observable = str(row["observable"])
        confidence = float(row["behavioral_confidence"])
        relation = str(row["relation"])
        if observable.startswith("CONTRADICTION:"):
            cluster = observable.split(":", 1)[1]
            matches = [item for item in model.get("contradictions", []) if item["cluster"] == cluster]
            if not matches:
                raise RuntimeError(f"unknown contradiction selector: {observable}")
            if relation == "supported" and confidence > 0:
                contradiction_confidence[cluster] = confidence
            continue
        if observable in mapping_by_id:
            ids = [observable]
        elif observable in cluster_to_ids:
            ids = sorted(cluster_to_ids[observable])
        else:
            raise RuntimeError(f"unknown positive selector: {observable}")
        selected_rows[observable] = ids
        if relation != "supported" or confidence <= 0:
            continue
        for mapping_id in ids:
            selected_confidence[mapping_id] = max(selected_confidence.get(mapping_id, 0.0), confidence)

    mappings: list[dict] = []
    for mapping_id in sorted(selected_confidence):
        item = copy.deepcopy(mapping_by_id[mapping_id])
        item["confidence"] = min(float(item["confidence"]), selected_confidence[mapping_id])
        item["translation_confidence"] = selected_confidence[mapping_id]
        mappings.append(item)

    contradictions: list[dict] = []
    for item0 in model.get("contradictions", []):
        cluster = item0["cluster"]
        if cluster not in contradiction_confidence:
            continue
        item = copy.deepcopy(item0)
        item["confidence"] = min(float(item["confidence"]), contradiction_confidence[cluster])
        item["translation_confidence"] = contradiction_confidence[cluster]
        contradictions.append(item)

    adapted = copy.deepcopy(model)
    adapted["mappings"] = mappings
    adapted["contradictions"] = contradictions
    adapted["survey_crosswalk_adapter"] = {
        "translation_sha256": sha256_path(TRANSLATION),
        "base_mapping_sha256": sha256_path(base_path),
        "overlay_sha256": sha256_path(overlay_path),
        "selected_rows": selected_rows,
        "selected_mapping_ids": sorted(selected_confidence),
        "selected_contradiction_clusters": sorted(contradiction_confidence),
        "core_fit_policy": "constant_zero_not_instantiated_by_owner_crosswalk",
    }
    return adapted, translation


def merge_scored_without_historical_core(scored: list[dict]) -> list[dict]:
    """Merge adjacent states using only score-relevant translated evidence.

    The historical V3.6 core fields are not instantiated by this survey crosswalk, so
    Type/Authority/Profile/center changes must not split otherwise score-identical
    intervals and thereby leak into the duration tie-break.
    """

    merged: list[dict] = []
    for item in scored:
        state = item["state"]
        score = item["score"]
        signature = (score["matches"], score["contra_matches"])
        if merged and merged[-1]["signature"] == signature:
            merged[-1]["state"]["end"] = state["end"]
            merged[-1]["state"]["dur"] += state["dur"]
        else:
            merged.append({"state": dict(state), "score": score, "signature": signature})
    return merged


def ranked_rows(states: list[dict], model: dict, prevalence: dict) -> list[dict]:
    # The crosswalk does not instantiate the historical target's core block. Keep the
    # documented ranking slot but make it candidate-independent for this survey run.
    original_core_fit = runner.core_fit
    runner.core_fit = lambda _state, _model: 0.0
    try:
        scored = [
            {"state": state, "score": runner.score_one(state, model, prevalence, False)}
            for state in states
        ]
    finally:
        runner.core_fit = original_core_fit
    return runner.sort_and_rank(merge_scored_without_historical_core(scored))


def result_row(item: dict) -> dict:
    state = item["state"]
    score = item["score"]
    return {
        "order": item["order"],
        "rank": item["rank"],
        "start": base.dt_from_jd(state["start"]).isoformat(),
        "end": base.dt_from_jd(state["end"]).isoformat(),
        "duration_hours": round(state["dur"] * 24.0, 6),
        "net": round(score["net"], 6),
        "evidence": round(score["evidence"], 6),
        "contradiction": round(score["contra"], 6),
        "meaningful_contradictions": score["meaningful"],
        "detail": round(score["detail"], 3),
        "core": 0.0,
        "winning_mappings": score["winner_by_cluster"],
        "winning_contradictions": score["contra_winners"],
    }


def best_intersecting(ranked: list[dict], start_jd: float, end_jd: float) -> dict | None:
    hits = [item for item in ranked if item["state"]["end"] > start_jd and item["state"]["start"] < end_jd]
    return hits[0] if hits else None


def main() -> None:
    model, translation = translated_model()
    ephe = (REPO / os.environ.get("EPHE_PATH", "data/ephemeris")).resolve()
    swe.set_ephe_path(str(ephe))
    for filename in ["sepl_18.se1", "semo_18.se1"]:
        path = ephe / filename
        if not path.exists():
            raise RuntimeError(f"missing {path}")

    t0 = time.time()
    states = runner.build_exact_states()
    prevalence, min_parent_duration = runner.build_prevalence(states, model)
    ranked = ranked_rows(states, model, prevalence)

    recorded_dt = datetime(1985, 1, 29, 10, 25, tzinfo=timezone.utc)
    recorded_jd = base.jd_from_dt(recorded_dt)
    recorded = next(item for item in ranked if item["state"]["start"] <= recorded_jd < item["state"]["end"])
    # Philadelphia local calendar date 1985-01-29 was EST (UTC-5).
    correct_date_start = base.jd_from_dt(datetime(1985, 1, 29, 5, 0, tzinfo=timezone.utc))
    correct_date_end = base.jd_from_dt(datetime(1985, 1, 30, 5, 0, tzinfo=timezone.utc))
    best_date = best_intersecting(ranked, correct_date_start, correct_date_end)

    result = {
        "schema": "life-patterns-owner-v43-crosswalk-result-v1",
        "label": "survey-instantiated clean V4.3/NetInformation crosswalk run",
        "translation_sha256": sha256_path(TRANSLATION),
        "source_neutral_profile_sha256": translation["source_final_neutral_profile_sha256"],
        "base_mapping_sha256": model["survey_crosswalk_adapter"]["base_mapping_sha256"],
        "overlay_sha256": model["survey_crosswalk_adapter"]["overlay_sha256"],
        "selected_mapping_ids": model["survey_crosswalk_adapter"]["selected_mapping_ids"],
        "selected_contradiction_clusters": model["survey_crosswalk_adapter"]["selected_contradiction_clusters"],
        "core_fit_policy": model["survey_crosswalk_adapter"]["core_fit_policy"],
        "post_selection_mappings_included": False,
        "raw_state_count": len(states),
        "merged_ranked_count": len(ranked),
        "prevalence_policy": {
            "median_state_hours": statistics.median(state["dur"] for state in states) * 24.0,
            "minimum_parent_duration_days": min_parent_duration,
        },
        "top20": [result_row(item) for item in ranked[:20]],
        "recorded_moment": result_row(recorded),
        "best_interval_intersecting_recorded_local_date": result_row(best_date) if best_date else None,
        "elapsed_seconds": time.time() - t0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT),
        "translation_sha256": result["translation_sha256"],
        "selected_mapping_count": len(result["selected_mapping_ids"]),
        "top1": result["top20"][0],
        "recorded_moment": result["recorded_moment"],
        "best_interval_intersecting_recorded_local_date": result["best_interval_intersecting_recorded_local_date"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
