from __future__ import annotations

import hashlib
import json
import math
import os
import statistics
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

import swieph_ab_rerun as base

MAPPING_PATH = Path(
    os.environ.get(
        "HD_MAPPING",
        "reference/core/profile_v3_6_v43_mapping_frozen_2026_08_22.json",
    )
)
TARGET_PATH = Path(
    os.environ.get("HD_TARGET", "reference/core/behavioral_target_combined_v3_6.md")
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def channel_pair(text: str) -> tuple[int, int]:
    a, b = (int(x) for x in text.split("-"))
    return tuple(sorted((a, b)))


def match_predicate(state: dict, predicate: dict) -> bool:
    feature = predicate["feature"]
    if feature == "type":
        return state["type"] == predicate["equals"]
    if feature == "authority":
        return state["auth"] == predicate["equals"]
    if feature == "center":
        present = predicate["name"] in state["centers"]
        return present is bool(predicate["defined"])
    if feature == "profile":
        return state["profile"] == predicate["equals"]
    if feature == "profile_has_line":
        return int(predicate["line"]) in (state["pl"], state["dl"])
    if feature == "channel":
        return channel_pair(predicate["equals"]) in state["channels"]
    if feature == "gate":
        return int(predicate["equals"]) in state["gates"]
    if feature == "activation":
        side = predicate["side"]
        body = predicate["body"]
        gate = int(predicate["gate"])
        return state.get(f"{side}_{body}_gate") == gate
    raise ValueError(f"unknown predicate feature: {feature}")


def match_conditions(state: dict, conditions: list[dict]) -> bool:
    return all(match_predicate(state, item) for item in conditions)


def profile_core_points(pl: int, dl: int) -> float:
    if (pl, dl) == (2, 4):
        return 15.0
    if pl == 2 or dl == 4:
        return 7.5
    if pl == 4 or dl == 2:
        return 5.0
    return 0.0


def core_fit(state: dict, model: dict) -> float:
    core = model["core"]
    earned = 0.0
    if state["type"] == core["type"]:
        earned += 30.0
    if state["auth"] == core["authority"]:
        earned += 30.0
    center_preds = core["diagnostic_centers"]
    per_center = 25.0 / len(center_preds)
    for name, defined in center_preds.items():
        if ((name in state["centers"]) is bool(defined)):
            earned += per_center
    earned += profile_core_points(state["pl"], state["dl"])
    return earned


def build_exact_states() -> list[dict]:
    t0 = time.time()
    raw: dict[tuple[str, str], list[float]] = {}
    for name, bid in base.BODY_IDS.items():
        st = time.time()
        raw[(name, "gate")] = base.generate(name, bid, "gate")
        print("EVENTS", name, len(raw[(name, "gate")]), "sec", round(time.time() - st, 2), flush=True)
    raw[("sun", "line")] = base.generate("sun", swe.SUN, "line")
    print("EVENTS sun_lines", len(raw[("sun", "line")]), flush=True)

    events = []
    eps = 2 / 86400.0
    for (name, kind), evs in raw.items():
        bid = base.BODY_IDS[name]
        for event_jd in evs:
            lon_after, _ = base.lon_speed(event_jd + eps, bid)
            after_gate, after_line = base.gate_line(lon_after)
            if base.START < event_jd < base.END:
                events.append((event_jd, "p", name, kind, after_gate, after_line))
            if base.START - 95 < event_jd < base.END - 80:
                birth_jd = base.forward_birth(event_jd)
                if base.START < birth_jd < base.END:
                    events.append((birth_jd, "d", name, kind, after_gate, after_line))

    events.sort(key=lambda item: item[0])
    groups: list[list[tuple]] = []
    for event in events:
        if groups and abs(event[0] - groups[-1][0][0]) * 86400 <= 0.5:
            groups[-1].append(event)
        else:
            groups.append([event])
    bounds = [base.START] + [sum(e[0] for e in group) / len(group) for group in groups] + [base.END]
    print("BOUNDARIES", len(bounds), "elapsed", round(time.time() - t0, 1), flush=True)

    acts = base.initial_state((bounds[0] + bounds[1]) / 2)
    counter = base.gate_counter(acts)
    states: list[dict] = []
    for idx in range(len(bounds) - 1):
        a, b = bounds[idx], bounds[idx + 1]
        if idx > 0:
            for _, side, name, kind, after_gate, after_line in groups[idx - 1]:
                base.apply_event(acts, counter, side, name, kind, after_gate, after_line)
        gates = frozenset(counter)
        channels, centers, typ, auth, definition = base.arch_from_gates(gates)
        pl = acts["p"]["sun"][1]
        dl = acts["d"]["sun"][1]
        states.append(
            {
                "start": a,
                "end": b,
                "dur": b - a,
                "gates": gates,
                "channels": frozenset(channels),
                "centers": frozenset(centers),
                "type": typ,
                "auth": auth,
                "definition": definition,
                "pl": pl,
                "dl": dl,
                "profile": f"{pl}/{dl}",
                "personality_moon_gate": acts["p"]["moon"][0],
                "design_mars_gate": acts["d"]["mars"][0],
            }
        )
    print("RAW_STATES", len(states), "elapsed", round(time.time() - t0, 1), flush=True)
    return states


def duration_prevalence(states: list[dict], mapping: dict, min_parent_duration: float) -> dict:
    full_parents = list(mapping.get("parents", []))
    parents = full_parents[:]
    total = sum(state["dur"] for state in states)
    while True:
        denom = sum(state["dur"] for state in states if match_conditions(state, parents))
        if denom >= min_parent_duration or not parents:
            break
        parents = parents[:-1]
    if denom <= 0:
        denom = total
        parents = []
    numer = sum(
        state["dur"]
        for state in states
        if match_conditions(state, parents) and match_predicate(state, mapping["predicate"])
    )
    prevalence = numer / denom if denom else 0.0
    return {
        "prevalence": prevalence,
        "numerator_days": numer,
        "denominator_days": denom,
        "parents_requested": full_parents,
        "parents_used": parents,
        "backoff_steps": len(full_parents) - len(parents),
    }


def information_bits(prevalence: float, cap: float) -> float:
    if prevalence <= 0:
        return cap
    return min(cap, -math.log2(prevalence))


def build_prevalence(states: list[dict], model: dict) -> tuple[dict, float]:
    median_duration = statistics.median(state["dur"] for state in states)
    min_equiv = model["constants"]["minimum_parent_state_equivalents"]
    min_parent_duration = median_duration * min_equiv
    info = {}
    for mapping in model["mappings"]:
        info[mapping["id"]] = duration_prevalence(states, mapping, min_parent_duration)
    for contradiction in model.get("contradictions", []):
        temp = {"predicate": contradiction["predicate"], "parents": contradiction.get("parents", [])}
        info[contradiction["id"]] = duration_prevalence(states, temp, min_parent_duration)
    return info, min_parent_duration


def active_mappings(model: dict, include_post_selection: bool) -> list[dict]:
    if include_post_selection:
        return list(model["mappings"])
    return [mapping for mapping in model["mappings"] if not mapping.get("post_selection", False)]


def score_one(state: dict, model: dict, prevalence: dict, include_post_selection: bool) -> dict:
    cap = model["constants"]["information_cap_bits"]
    mappings = active_mappings(model, include_post_selection)
    by_cluster: dict[str, list[dict]] = defaultdict(list)
    cluster_max_conf: dict[str, float] = defaultdict(float)

    for mapping in mappings:
        cluster = mapping["cluster"]
        cluster_max_conf[cluster] = max(cluster_max_conf[cluster], float(mapping["confidence"]))
        if not match_predicate(state, mapping["predicate"]):
            continue
        pinfo = prevalence[mapping["id"]]
        bits = information_bits(float(pinfo["prevalence"]), cap)
        support = float(mapping["salience"]) * float(mapping["directness"])
        evidence = float(mapping["confidence"]) * support * float(mapping["flexibility"]) * bits
        by_cluster[cluster].append(
            {
                "mapping_id": mapping["id"],
                "evidence": evidence,
                "weighted_support": float(mapping["confidence"]) * support,
                "support": support,
                "bits": bits,
            }
        )

    evidence_by_cluster: dict[str, float] = {}
    support_by_cluster: dict[str, float] = {}
    winner_by_cluster: dict[str, str] = {}
    for cluster in cluster_max_conf:
        options = by_cluster.get(cluster, [])
        if options:
            winner = max(options, key=lambda x: (x["evidence"], x["weighted_support"], x["mapping_id"]))
            evidence_by_cluster[cluster] = winner["evidence"]
            support_by_cluster[cluster] = winner["weighted_support"]
            winner_by_cluster[cluster] = winner["mapping_id"]
        else:
            evidence_by_cluster[cluster] = 0.0
            support_by_cluster[cluster] = 0.0

    contradiction_by_cluster: dict[str, float] = {}
    meaningful = 0
    contra_winners: dict[str, str] = {}
    grouped_contra: dict[str, list[tuple[float, str, float]]] = defaultdict(list)
    for contradiction in model.get("contradictions", []):
        if match_predicate(state, contradiction["predicate"]):
            penalty = float(contradiction["confidence"]) * float(contradiction["severity"]) * float(model["constants"]["contradiction_cap_bits"])
            grouped_contra[contradiction["cluster"]].append((penalty, contradiction["id"], float(contradiction["severity"])))
    for cluster, options in grouped_contra.items():
        penalty, cid, severity = max(options)
        contradiction_by_cluster[cluster] = penalty
        contra_winners[cluster] = cid
        if severity >= 0.50:
            meaningful += 1

    evidence_total = sum(evidence_by_cluster.values())
    contradiction_total = sum(contradiction_by_cluster.values())
    denom = sum(cluster_max_conf.values())
    detail = 100.0 * sum(support_by_cluster.values()) / denom if denom else 0.0
    return {
        "net": evidence_total - contradiction_total,
        "evidence": evidence_total,
        "contra": contradiction_total,
        "meaningful": meaningful,
        "detail": detail,
        "core": core_fit(state, model),
        "evidence_by_cluster": evidence_by_cluster,
        "contra_by_cluster": contradiction_by_cluster,
        "winner_by_cluster": winner_by_cluster,
        "contra_winners": contra_winners,
        "matches": tuple(sorted(winner_by_cluster.items())),
        "contra_matches": tuple(sorted(contra_winners.items())),
    }


def merge_scored(scored: list[dict], model: dict) -> list[dict]:
    center_names = tuple(model["core"]["diagnostic_centers"].keys())
    merged: list[dict] = []
    for item in scored:
        state = item["state"]
        score = item["score"]
        signature = (
            score["matches"],
            score["contra_matches"],
            state["type"],
            state["auth"],
            state["profile"],
            tuple((name, name in state["centers"]) for name in center_names),
        )
        if merged and merged[-1]["signature"] == signature:
            merged[-1]["state"]["end"] = state["end"]
            merged[-1]["state"]["dur"] += state["dur"]
        else:
            merged.append({"state": dict(state), "score": score, "signature": signature})
    return merged


def sort_and_rank(rows: list[dict]) -> list[dict]:
    rows.sort(
        key=lambda item: (
            -item["score"]["net"],
            item["score"]["meaningful"],
            -item["score"]["detail"],
            -item["score"]["core"],
            -item["state"]["dur"],
            item["state"]["start"],
        )
    )
    rank = 0
    previous = None
    for pos, item in enumerate(rows, 1):
        key = (
            round(item["score"]["net"], 12),
            item["score"]["meaningful"],
            round(item["score"]["detail"], 12),
            round(item["score"]["core"], 12),
            round(item["state"]["dur"], 12),
        )
        if key != previous:
            rank = pos
            previous = key
        item["rank"] = rank
        item["order"] = pos
    return rows


def row_json(item: dict) -> dict:
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
        "core": round(score["core"], 3),
        "type": state["type"],
        "authority": state["auth"],
        "profile": state["profile"],
        "definition": state["definition"],
        "personality_moon_gate": state["personality_moon_gate"],
        "design_mars_gate": state["design_mars_gate"],
        "channels": ["-".join(map(str, pair)) for pair in sorted(state["channels"])],
        "winning_mappings": score["winner_by_cluster"],
    }


def run_variant(states: list[dict], model: dict, prevalence: dict, include_post_selection: bool, label: str) -> list[dict]:
    scored = [{"state": state, "score": score_one(state, model, prevalence, include_post_selection)} for state in states]
    ranked = sort_and_rank(merge_scored(scored, model))
    print("VARIANT", label, "RAW", len(states), "MERGED", len(ranked), flush=True)
    print("TOP20", label, flush=True)
    for item in ranked[:20]:
        print(json.dumps(row_json(item), sort_keys=True), flush=True)
    target_jd = base.jd_from_dt(datetime(1985, 1, 29, 0, 22, 30, tzinfo=timezone.utc))
    current = next(item for item in ranked if item["state"]["start"] <= target_jd < item["state"]["end"])
    print("CURRENT_1985", label, json.dumps(row_json(current), sort_keys=True), flush=True)
    print(
        "CURRENT_1985_CONTRIB",
        label,
        json.dumps(
            {
                "evidence_by_cluster": {k: round(v, 6) for k, v in current["score"]["evidence_by_cluster"].items() if v},
                "contra_by_cluster": {k: round(v, 6) for k, v in current["score"]["contra_by_cluster"].items() if v},
                "winner_by_cluster": current["score"]["winner_by_cluster"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return ranked


def main() -> None:
    mapping_path = MAPPING_PATH.resolve()
    target_path = TARGET_PATH.resolve()
    model = json.loads(mapping_path.read_text(encoding="utf-8"))
    print("MAPPING_SHA256", sha256_path(mapping_path), flush=True)
    print("TARGET_SHA256", sha256_path(target_path), flush=True)

    ephe = Path(os.environ.get("EPHE_PATH", "data/ephemeris")).resolve()
    swe.set_ephe_path(str(ephe))
    print("EPHE_PATH", ephe, flush=True)
    for filename in ["sepl_18.se1", "semo_18.se1"]:
        path = ephe / filename
        if not path.exists():
            raise RuntimeError(f"missing {path}")
        print("EPHE_FILE", filename, path.stat().st_size, sha256_path(path), flush=True)
    for dt in [base.START_DT, datetime(1985, 1, 29, tzinfo=timezone.utc), base.END_DT]:
        jd = base.jd_from_dt(dt)
        for name in ["sun", "moon", "mars", "pluto"]:
            base.lon_speed(jd, base.BODY_IDS[name])
        print("SWIEPH_PROBE_OK", dt.isoformat(), flush=True)

    t0 = time.time()
    states = build_exact_states()
    prevalence, min_parent_duration = build_prevalence(states, model)
    print(
        "PREVALENCE_POLICY",
        json.dumps(
            {
                "median_state_hours": round(statistics.median(s["dur"] for s in states) * 24, 6),
                "minimum_parent_state_equivalents": model["constants"]["minimum_parent_state_equivalents"],
                "minimum_parent_duration_days": round(min_parent_duration, 6),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    print("PREVALENCE_TABLE")
    for mid in sorted(prevalence):
        p = prevalence[mid]
        print(
            json.dumps(
                {
                    "id": mid,
                    "p": round(p["prevalence"], 9),
                    "bits": round(information_bits(p["prevalence"], model["constants"]["information_cap_bits"]), 6),
                    "denominator_days": round(p["denominator_days"], 6),
                    "backoff_steps": p["backoff_steps"],
                    "parents_used": p["parents_used"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    run_variant(states, model, prevalence, False, "NO_POST_SELECTION_CARRIERS")
    run_variant(states, model, prevalence, True, "BEST_CURRENT_V3_6")
    print("DONE", round(time.time() - t0, 1), flush=True)


if __name__ == "__main__":
    main()
