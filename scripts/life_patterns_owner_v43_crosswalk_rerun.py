#!/usr/bin/env python3
"""Run a frozen Life Patterns neutral profile through the clean V4.3 crosswalk.

Development-only post-freeze adapter. The participant-specific translated behavioral
input stays private and is supplied with OWNER_V43_TRANSLATION. No participant text is
stored here.
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
from typing import Any

import swisseph as swe

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import swieph_ab_rerun as base  # noqa: E402
import v43_profile_netinfo_rerun as runner  # noqa: E402
import v43_profile_netinfo_rerun_v2 as overlay_runner  # noqa: E402

REPO = SCRIPT_DIR.parent
CROSSWALK_PATH = REPO / "reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observable_id(mapping: dict[str, Any]) -> str:
    """Match the pre-existing holistic-audit observable partition."""

    if mapping["cluster"] == "PROFILE_STRUCTURE":
        return str(mapping["id"])
    return str(mapping["cluster"])


def cap_confidence(frozen: float, translated: float) -> float:
    """Apply the pre-search frozen CAP rule."""

    if not 0.0 <= frozen <= 1.0 or not 0.0 <= translated <= 1.0:
        raise ValueError("confidence must be in [0, 1]")
    return min(frozen, translated)


def translated_model(translation_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Instantiate only crosswalked, supported, candidate-unexposed mappings."""

    model, base_path, overlay_path = overlay_runner.load_frozen_model()
    translation = json.loads(translation_path.read_text(encoding="utf-8"))
    rows = translation.get("translations")
    if not isinstance(rows, list):
        raise RuntimeError("translation must contain a translations list")

    crosswalk = json.loads(CROSSWALK_PATH.read_text(encoding="utf-8"))
    expected = {str(row["observable"]) for row in crosswalk["clean_v36_information_crosswalk"]}
    observed = {str(row["observable"]) for row in rows}
    if observed != expected:
        raise RuntimeError(
            f"translation observable set mismatch: missing={sorted(expected-observed)} extra={sorted(observed-expected)}"
        )

    active_mapping_by_id = {
        str(item["id"]): item
        for item in model["mappings"]
        if not item.get("post_selection", False)
    }
    active_by_observable: dict[str, list[dict[str, Any]]] = {}
    for item in active_mapping_by_id.values():
        active_by_observable.setdefault(observable_id(item), []).append(item)

    selected_mapping_ids: dict[str, float] = {}
    selected_rows: dict[str, list[str]] = {}
    contradiction_confidence: dict[str, float] = {}

    for row in rows:
        obs = str(row["observable"])
        confidence = float(row["behavioral_confidence"])
        relation = str(row["relation"])
        if confidence not in {0.0, 0.25, 0.5, 0.75, 1.0}:
            raise RuntimeError(f"unexpected translated confidence for {obs}: {confidence}")
        if relation not in {"supported", "not_established"}:
            raise RuntimeError(f"unexpected relation for {obs}: {relation}")
        if (confidence == 0.0) != (relation == "not_established"):
            raise RuntimeError(f"relation/confidence mismatch for {obs}")

        if obs.startswith("CONTRADICTION:"):
            cluster = obs.split(":", 1)[1]
            matches = [item for item in model.get("contradictions", []) if item["cluster"] == cluster]
            if not matches:
                raise RuntimeError(f"unknown contradiction selector: {obs}")
            if confidence > 0.0:
                contradiction_confidence[cluster] = confidence
            continue

        mappings = active_by_observable.get(obs)
        if not mappings:
            raise RuntimeError(f"unknown positive selector: {obs}")
        ids = sorted(str(item["id"]) for item in mappings)
        selected_rows[obs] = ids
        if confidence == 0.0:
            continue
        for mapping_id in ids:
            selected_mapping_ids[mapping_id] = confidence

    mappings: list[dict[str, Any]] = []
    derivation_rows: list[dict[str, Any]] = []
    for mapping_id in sorted(selected_mapping_ids):
        source = active_mapping_by_id[mapping_id]
        item = copy.deepcopy(source)
        translated_confidence = selected_mapping_ids[mapping_id]
        frozen_confidence = float(item["confidence"])
        derived = cap_confidence(frozen_confidence, translated_confidence)
        item["historical_confidence"] = frozen_confidence
        item["translation_confidence"] = translated_confidence
        item["confidence"] = derived
        mappings.append(item)
        derivation_rows.append(
            {
                "observable": observable_id(item),
                "mapping_id": mapping_id,
                "historical_confidence": frozen_confidence,
                "translation_confidence": translated_confidence,
                "derived_confidence": derived,
            }
        )

    contradictions: list[dict[str, Any]] = []
    for source in model.get("contradictions", []):
        cluster = str(source["cluster"])
        if cluster not in contradiction_confidence:
            continue
        item = copy.deepcopy(source)
        translated_confidence = contradiction_confidence[cluster]
        frozen_confidence = float(item["confidence"])
        item["historical_confidence"] = frozen_confidence
        item["translation_confidence"] = translated_confidence
        item["confidence"] = cap_confidence(frozen_confidence, translated_confidence)
        contradictions.append(item)

    adapted = copy.deepcopy(model)
    adapted["mappings"] = mappings
    adapted["contradictions"] = contradictions
    adapted["survey_crosswalk_adapter"] = {
        "schema": "life-patterns-owner-v43-crosswalk-adapter-v1",
        "translation_sha256": sha256_path(translation_path),
        "source_neutral_profile_sha256": translation["source_final_neutral_profile_sha256"],
        "crosswalk_sha256": sha256_path(CROSSWALK_PATH),
        "base_mapping_sha256": sha256_path(base_path),
        "overlay_sha256": sha256_path(overlay_path),
        "confidence_rule": "min(frozen_pathway_confidence, translated_behavioral_confidence)",
        "zero_confidence_policy": "omit_before_matching_and_signature",
        "post_selection_mappings_included": False,
        "core_fit_policy": "constant_zero_not_instantiated_by_owner_crosswalk",
        "selected_rows": selected_rows,
        "selected_mapping_ids": sorted(selected_mapping_ids),
        "selected_contradiction_clusters": sorted(contradiction_confidence),
        "derivation_rows": derivation_rows,
    }
    return adapted, translation


def merge_scored_neutral_core(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge adjacent states using only active survey-scoring signatures.

    The historical runner also split on its target-specific core Type/Authority/profile/
    center state. Those fields are not instantiated by this survey crosswalk and cannot
    affect the stable-duration tie-break here.
    """

    merged: list[dict[str, Any]] = []
    for item in scored:
        score = item["score"]
        signature = (score["matches"], score["contra_matches"])
        if merged and merged[-1]["signature"] == signature:
            merged[-1]["state"]["end"] = item["state"]["end"]
            merged[-1]["state"]["dur"] += item["state"]["dur"]
        else:
            merged.append(
                {"state": dict(item["state"]), "score": score, "signature": signature}
            )
    return merged


def score_and_rank(
    states: list[dict[str, Any]], model: dict[str, Any], prevalence: dict[str, Any]
) -> list[dict[str, Any]]:
    """Score with neutral CoreFit and rank score-equivalent stable neighborhoods."""

    original_core_fit = runner.core_fit
    runner.core_fit = lambda _state, _model: 0.0
    try:
        scored = [
            {"state": state, "score": runner.score_one(state, model, prevalence, False)}
            for state in states
        ]
    finally:
        runner.core_fit = original_core_fit
    return runner.sort_and_rank(merge_scored_neutral_core(scored))


def result_row(item: dict[str, Any]) -> dict[str, Any]:
    """Serialize only rank fields that remain homogeneous after neutral-core merging."""

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


def best_intersecting(
    ranked: list[dict[str, Any]], start_jd: float, end_jd: float
) -> dict[str, Any] | None:
    for item in ranked:
        if item["state"]["end"] > start_jd and item["state"]["start"] < end_jd:
            return item
    return None


def main() -> None:
    translation_path = Path(os.environ["OWNER_V43_TRANSLATION"]).resolve()
    output_path = Path(os.environ.get("OWNER_V43_OUTPUT", "owner-v43-crosswalk-result.json")).resolve()
    model, translation = translated_model(translation_path)

    ephe = (REPO / os.environ.get("EPHE_PATH", "data/ephemeris")).resolve()
    swe.set_ephe_path(str(ephe))
    for filename in ["sepl_18.se1", "semo_18.se1"]:
        path = ephe / filename
        if not path.exists():
            raise RuntimeError(f"missing {path}")

    t0 = time.time()
    states = runner.build_exact_states()
    prevalence, min_parent_duration = runner.build_prevalence(states, model)
    ranked = score_and_rank(states, model, prevalence)

    recorded_dt = datetime(1985, 1, 29, 10, 25, tzinfo=timezone.utc)
    recorded_jd = base.jd_from_dt(recorded_dt)
    recorded = next(
        item for item in ranked if item["state"]["start"] <= recorded_jd < item["state"]["end"]
    )
    # Philadelphia local calendar date 1985-01-29 was EST (UTC-5).
    date_start = base.jd_from_dt(datetime(1985, 1, 29, 5, 0, tzinfo=timezone.utc))
    date_end = base.jd_from_dt(datetime(1985, 1, 30, 5, 0, tzinfo=timezone.utc))
    best_date = best_intersecting(ranked, date_start, date_end)

    adapter = model["survey_crosswalk_adapter"]
    result = {
        "schema": "life-patterns-owner-v43-crosswalk-result-v1",
        "label": "survey-instantiated clean V4.3/NetInformation crosswalk run",
        "translation_sha256": adapter["translation_sha256"],
        "source_neutral_profile_sha256": adapter["source_neutral_profile_sha256"],
        "crosswalk_sha256": adapter["crosswalk_sha256"],
        "base_mapping_sha256": adapter["base_mapping_sha256"],
        "overlay_sha256": adapter["overlay_sha256"],
        "confidence_rule": adapter["confidence_rule"],
        "core_fit_policy": adapter["core_fit_policy"],
        "post_selection_mappings_included": False,
        "selected_mapping_ids": adapter["selected_mapping_ids"],
        "selected_contradiction_clusters": adapter["selected_contradiction_clusters"],
        "raw_state_count": len(states),
        "merged_scoring_neighborhood_count": len(ranked),
        "prevalence_policy": {
            "median_state_hours": statistics.median(state["dur"] for state in states) * 24.0,
            "minimum_parent_duration_days": min_parent_duration,
        },
        "top20": [result_row(item) for item in ranked[:20]],
        "recorded_moment": result_row(recorded),
        "best_interval_intersecting_recorded_local_date": (
            result_row(best_date) if best_date else None
        ),
        "elapsed_seconds": time.time() - t0,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output_path),
                "translation_sha256": result["translation_sha256"],
                "selected_mapping_count": len(result["selected_mapping_ids"]),
                "top1": result["top20"][0],
                "recorded_moment": result["recorded_moment"],
                "best_interval_intersecting_recorded_local_date": result[
                    "best_interval_intersecting_recorded_local_date"
                ],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
