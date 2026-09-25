"""Answer-conditioned six-clause research decoder.

Astronomical conditions are the unchanged V1.4d conditions. The V1.5 behavioral
comparison is a declared experimental bridge, not a verbatim historical rule.
No recorded birth target is read to calculate a score or select a rule.
"""
from __future__ import annotations

import hashlib
import json
import random
import os
import threading
from collections import Counter
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot
from hdmatch.evaluation.astrohd_v14_rules import feature_row, registry

ROOT = Path(os.environ.get("HDMATCH_REPO_ROOT", "/app"))
if not (ROOT / "reference/research").is_dir():
    ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / "tasks/scenario-owner-recovery-calibration-20260923"
MODEL_PATH = TASK / "ASTROHD-V14-SIX-RULE-MODEL-20260925.json"
BRIDGE_PATH = ROOT / "reference/research/astrohd_v15_behavioral_bridge.json"
START = datetime(1926, 8, 24, 10, 42, tzinfo=UTC)
END = datetime(2026, 8, 24, 10, 42, tzinfo=UTC)
MAX_DECOYS = 9999
STATES = frozenset({"supported", "contradicted", "mixed", "unknown", "not_applicable"})
_ASTRO_LOCK = threading.Lock()


def content_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def load_model() -> tuple[dict[str, Any], tuple[dict[str, Any], ...], dict[str, Any]]:
    model = json.loads(MODEL_PATH.read_text())
    if file_hash(ROOT / model["rule_module"]) != model["rule_module_sha256"]:
        raise ValueError("Frozen astronomical rule module has changed")
    source_path = ROOT / model["source_map_path"]
    if file_hash(source_path) != model["source_map_sha256"]:
        raise ValueError("Frozen generic source map has changed")
    source = json.loads(source_path.read_text())
    lookup = {row["rule_id"]: row for row in registry(source, {d["domain_id"] for d in source["domains"]})}
    rules = tuple(lookup[key] for key in model["selected_rule_ids"])
    bridge = json.loads(BRIDGE_PATH.read_text())
    if [r["rule_id"] for r in bridge["rules"]] != model["selected_rule_ids"]:
        raise ValueError("Behavioral bridge and saved rule order disagree")
    if model["weight_per_selected_rule"] != 1 or len(rules) != 6:
        raise ValueError("This decoder requires the unchanged six equal-vote conditions")
    return model, rules, bridge


def normalize_profile(profile: Mapping[str, str]) -> dict[str, str]:
    bridge = load_model()[2]
    expected = {d["id"] for d in bridge["domains"]}
    if set(profile) != expected:
        raise ValueError("Profile must contain exactly the declared neutral domains")
    result = {key: str(profile[key]) for key in sorted(expected)}
    if any(value not in STATES for value in result.values()):
        raise ValueError("Unknown profile state")
    return result


def answer_signs(profile: Mapping[str, str]) -> tuple[int, ...]:
    """One-sided support/mismatch: a missing chart clause never predicts absence.

For a declared alternative-domain bridge, any supported alternative supports
its assertion; only explicit contradiction of every alternative contradicts it.
Other patterns abstain. This is fixed before new-participant outcomes.
"""
    normalized = normalize_profile(profile)
    signs = []
    for rule in load_model()[2]["rules"]:
        states = [normalized[key] for key in rule["domain_ids"]]
        signs.append(1 if "supported" in states else -1 if all(s == "contradicted" for s in states) else 0)
    return tuple(signs)


def score_mask(mask: int, signs: Sequence[int]) -> int:
    if not 0 <= mask < 64 or len(signs) != 6 or any(s not in (-1, 0, 1) for s in signs):
        raise ValueError("Invalid six-clause mask or answer signs")
    return sum(sign for i, sign in enumerate(signs) if mask & (1 << i))


def candidate_minutes(count: int) -> tuple[int, ...]:
    if count not in (99, 999, 9999):
        raise ValueError("Supported panels use 99, 999, or 9999 independent decoys")
    # Generate the same complete reservoir before slicing: panels are nested.
    reservoir = random.Random(150925).sample(range(int((END - START).total_seconds() // 60) + 1), MAX_DECOYS)
    return tuple(reservoir[:count])


def candidate_times(count: int) -> tuple[datetime, ...]:
    return tuple(START + timedelta(minutes=i) for i in candidate_minutes(count))


def validate_location(latitude: float, longitude: float) -> None:
    import math
    if not math.isfinite(latitude) or not math.isfinite(longitude):
        raise ValueError("Birthplace coordinates must be finite")
    if not -66 <= latitude <= 66 or not -180 <= longitude <= 180:
        raise ValueError("This prototype supports birthplaces between 66 degrees south and north; polar-house behavior is unresolved")


def _mask_unlocked(when: datetime, latitude: float, longitude: float, ephemeris_root: Path) -> int:
    snapshot = build_snapshot(when, latitude=latitude, longitude=longitude, ephemeris_root=ephemeris_root)
    values = feature_row(snapshot, list(load_model()[1])).tolist()
    if any(v not in (0, 1) for v in values):
        raise ValueError("The frozen six-clause signature must remain Boolean")
    return sum(int(value) << i for i, value in enumerate(values))


def mask_at(when: datetime, latitude: float, longitude: float, ephemeris_root: Path) -> int:
    validate_location(latitude, longitude)
    if when.tzinfo is None or when.utcoffset() is None:
        raise ValueError("A timezone-aware birth instant is required")
    with _ASTRO_LOCK:
        return _mask_unlocked(when, latitude, longitude, ephemeris_root)


@lru_cache(maxsize=24)
def panel_masks(count: int, latitude: float, longitude: float, ephemeris_root: str) -> tuple[int, ...]:
    validate_location(latitude, longitude)
    with _ASTRO_LOCK:
        return tuple(_mask_unlocked(t, latitude, longitude, Path(ephemeris_root)) for t in candidate_times(count))


def rank_against(scores: Sequence[int], score: int) -> dict[str, Any]:
    higher = sum(s > score for s in scores)
    ties = sum(s == score for s in scores)
    return {"rank_best": higher + 1, "rank_worst": higher + ties + 1,
            "rank_mid": higher + ties / 2 + 1, "higher_candidates": higher,
            "tied_other_candidates": ties, "comparison_count_including_checked_instant": len(scores) + 1,
            "unique_first": higher == 0 and ties == 0, "joint_first": higher == 0}


def run_panel(profile: Mapping[str, str], *, latitude: float, longitude: float,
              count: int, ephemeris_root: Path) -> dict[str, Any]:
    profile = normalize_profile(profile)
    signs = answer_signs(profile)
    if not any(signs):
        raise ValueError("No scored evidence: all active interpretations are mixed, unknown, or not applicable")
    times = candidate_times(count)
    masks = panel_masks(count, latitude, longitude, str(ephemeris_root.resolve()))
    scores = [score_mask(mask, signs) for mask in masks]
    order = sorted(range(count), key=lambda i: (-scores[i], i))
    best = scores[order[0]]
    model_id = content_hash({"model": file_hash(MODEL_PATH), "bridge": file_hash(BRIDGE_PATH)})
    return {"model_id": model_id, "model_version": "1.5.0-experimental-answer-bridge",
            "profile_sha256": content_hash(profile), "answer_signs": list(signs),
            "panel_sha256": content_hash([t.isoformat() for t in times]), "decoy_count": count,
            "universe_start": START.isoformat(), "universe_end": END.isoformat(),
            "birthplace": {"latitude": latitude, "longitude": longitude},
            "score_histogram": dict(sorted(Counter(scores).items())),
            "maximum_observed_score": best, "maximum_observed_count": scores.count(best),
            "top_candidates": [{"utc": times[i].isoformat(), "score": scores[i]} for i in order[:20]],
            "claim": "Frozen-model candidate-panel test; not an exhaustive century search, probability, or validation result",
            "reference_fit": "The six astronomical conditions were selected on one known development person",
            "ties_policy": "No proximity-to-known-birth tie-break; equal features retain equal scores",
            "computed_utc": datetime.now(UTC).isoformat()}


def check_instant(profile: Mapping[str, str], when: datetime, *, latitude: float,
                  longitude: float, count: int, ephemeris_root: Path) -> dict[str, Any]:
    signs = answer_signs(profile)
    masks = panel_masks(count, latitude, longitude, str(ephemeris_root.resolve()))
    times = candidate_times(count)
    # Never count the same actual instant twice if it happened to be sampled.
    other_scores = [score_mask(m, signs) for t, m in zip(times, masks) if t != when]
    mask = mask_at(when, latitude, longitude, ephemeris_root)
    score = score_mask(mask, signs)
    return {"checked_utc": when.astimezone(UTC).isoformat(), "score": score,
            "rule_bits": [(mask >> i) & 1 for i in range(6)], **rank_against(other_scores, score),
            "score_is_not_rank": True,
            "claim": "New-person test of this frozen experimental model; no refitting was performed"}
