#!/usr/bin/env python3
"""Exact-time static partner-identification benchmark V1.

Frozen spec: reference/research/adb_static_partner_identification_freeze_v1.md
Development/model discovery only. Verified SWIEPH; no Joel/Bee data are used.
"""
from __future__ import annotations

import json
import math
import random
import re
import statistics
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import swisseph as swe
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

import adb_pair_timing_model_search_v1 as base
import partner_hd_timing_pilot as hd

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
FREEZE = REPO / "reference" / "research" / "adb_static_partner_identification_freeze_v1.md"
OUT = REPO / "reference" / "research" / "adb_static_partner_identification_results_v1.json"
URL = base.URL
HIGH_RR = {"AA", "A"}
ROMANTIC_REL_IDS = {843, 858, 859}
C_GRID = (0.001, 0.01, 0.1, 1.0)
RNG_SEED = 202608261432
N_DECOYS = 50
ASPECTS = (0, 60, 90, 120, 180)
SIGMA = 3.0
BODY_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}
BODY_NAMES = tuple(BODY_IDS) + ("ASC", "MC")
MODELS = ("M0S", "MWS", "MHDS", "MCOMB")


def sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_coord(s: str | None, is_lat: bool) -> float | None:
    if not s:
        return None
    m = re.fullmatch(r"(\d{1,3})([nsew])(\d{1,2})", s.strip().lower())
    if not m:
        return None
    deg = int(m.group(1)); hemi = m.group(2); minute = int(m.group(3))
    if deg > (90 if is_lat else 180) or minute >= 60:
        return None
    v = deg + minute / 60.0
    return -v if hemi in {"s", "w"} else v


def download_people():
    req = urllib.request.Request(URL, headers={"User-Agent": "humandesign-static-partner-id/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    root = ET.fromstring(raw)
    people = {}
    neighbors: dict[int, set[int]] = defaultdict(set)
    pair_types: dict[tuple[int, int], set[int]] = defaultdict(set)
    for e in root.findall("adb_entry"):
        aid = int(e.attrib["adb_id"])
        pub = e.find("public_data")
        if pub is None:
            continue
        rr = (pub.findtext("roddenrating") or "").strip()
        gender_el = pub.find("gender")
        gender = gender_el.attrib.get("csex", "") if gender_el is not None else ""
        bt = pub.find("./bdata/sbtime")
        bd = pub.find("./bdata/sbdate")
        exact_jd = None
        if bt is not None and bt.attrib.get("jd_ut") and (bt.text or "").strip():
            try:
                exact_jd = float(bt.attrib["jd_ut"])
            except ValueError:
                pass
        birth_year = None
        if bd is not None:
            try:
                birth_year = int(bd.attrib.get("iyear", "0")) or None
            except ValueError:
                pass
        place = pub.find("./bdata/place")
        coord = None
        if place is not None:
            lat = parse_coord(place.attrib.get("slati"), True)
            lon = parse_coord(place.attrib.get("slong"), False)
            if lat is not None and lon is not None:
                coord = (lat, lon)
        people[aid] = {
            "id": aid, "rr": rr, "gender": gender, "jd": exact_jd,
            "birth_year": birth_year, "coord": coord,
        }
        research = e.find("research_data")
        if research is not None:
            rp = research.find("relationships")
            if rp is not None:
                for rel in rp.findall("relationship"):
                    try:
                        rid = int(rel.attrib.get("rel_id", "0"))
                        other = int(rel.attrib.get("rel_adb_id", "0"))
                    except ValueError:
                        continue
                    if rid in ROMANTIC_REL_IDS:
                        neighbors[aid].add(other)
                        neighbors[other].add(aid)
                        pair_types[tuple(sorted((aid, other)))].add(rid)
    return people, neighbors, pair_types, len(raw)


def aspect_kernel(a: float, b: float, asp: int) -> float:
    r = base.aspect_residual(a, b, asp)
    return math.exp(-0.5 * (r / SIGMA) ** 2)


def natal_west(person: dict, cache: dict[int, dict[str, float | None]]) -> dict[str, float | None]:
    pid = person["id"]
    if pid in cache:
        return cache[pid]
    jd = person["jd"]
    assert jd is not None
    out: dict[str, float | None] = {n: base.calc(jd, body)[0] for n, body in BODY_IDS.items()}
    out["ASC"] = None; out["MC"] = None
    if person["coord"] is not None:
        lat, lon = person["coord"]
        try:
            _cusps, ascmc = swe.houses_ex(jd, lat, lon, b"P", 0)
            out["ASC"] = float(ascmc[0] % 360.0)
            out["MC"] = float(ascmc[1] % 360.0)
        except Exception:
            pass
    cache[pid] = out
    return out


def natal_gates(person: dict, cache: dict[int, set[int]]) -> set[int]:
    pid = person["id"]
    if pid not in cache:
        cache[pid] = hd.natal_gates(hd.dt_from_jd(person["jd"]))
    return cache[pid]


def hd_mechanics(a_g: set[int], b_g: set[int]) -> dict[str, float]:
    fp = hd.fingerprint(a_g | b_g)
    em = comp = dom_a = dom_b = compr_a = compr_b = 0
    for x, y in hd.CHANNELS:
        aset = int(x in a_g) + int(y in a_g)
        bset = int(x in b_g) + int(y in b_g)
        a_full = aset == 2; b_full = bset == 2
        if a_full and b_full:
            comp += 1
        elif a_full and bset == 0:
            dom_a += 1
        elif b_full and aset == 0:
            dom_b += 1
        elif a_full and bset == 1:
            compr_a += 1
        elif b_full and aset == 1:
            compr_b += 1
        elif aset == 1 and bset == 1:
            ag = x if x in a_g else y
            bg = x if x in b_g else y
            if ag != bg:
                em += 1
    ncenters = int(fp["defined_center_count"])
    out = {
        "hd_defined_centers": float(ncenters),
        "hd_definition_components": float(fp["definition_components"]),
        "hd_electromagnetic": float(em),
        "hd_companionship": float(comp),
        "hd_dominance_focal": float(dom_a),
        "hd_dominance_candidate": float(dom_b),
        "hd_compromise_focal": float(compr_a),
        "hd_compromise_candidate": float(compr_b),
        "hd_shared_gates": float(len(a_g & b_g)),
        "hd_combined_channels": float(len(fp["channels"])),
    }
    for n in (9, 8, 7, 6, 5):
        out[f"hd_centers_{n}"] = 1.0 if ncenters == n else 0.0
    return out


def feature_row(focal: dict, cand: dict, west_cache, gate_cache) -> dict[str, float]:
    year = base.TROPICAL_YEAR
    signed = (cand["jd"] - focal["jd"]) / year
    f = {
        "m0_signed_age_diff": signed,
        "m0_abs_age_diff": abs(signed),
        "m0_focal_year": ((focal["birth_year"] or 1950) - 1950.0) / 50.0,
        "m0_candidate_year": ((cand["birth_year"] or 1950) - 1950.0) / 50.0,
    }
    wa = natal_west(focal, west_cache); wb = natal_west(cand, west_cache)
    f["w_focal_angles_available"] = 1.0 if wa["ASC"] is not None and wa["MC"] is not None else 0.0
    f["w_candidate_angles_available"] = 1.0 if wb["ASC"] is not None and wb["MC"] is not None else 0.0
    for an in BODY_NAMES:
        av = wa[an]
        for bn in BODY_NAMES:
            bv = wb[bn]
            for asp in ASPECTS:
                key = f"w_{an}_{bn}_a{asp}"
                f[key] = 0.0 if av is None or bv is None else aspect_kernel(float(av), float(bv), asp)
    f.update(hd_mechanics(natal_gates(focal, gate_cache), natal_gates(cand, gate_cache)))
    return f


def build_tasks(people, neighbors, pair_types):
    high = {pid: p for pid, p in people.items() if p["rr"] in HIGH_RR and p["jd"] is not None}
    positive_pairs = []
    for (a, b), _types in sorted(pair_types.items()):
        if a in high and b in high:
            positive_pairs.append((a, b))
    tasks = []
    dropped = Counter()
    for a, b in positive_pairs:
        for focal_id, true_id in ((a, b), (b, a)):
            focal = high[focal_id]; true = high[true_id]
            gender = true["gender"]
            pool = []
            for pid, p in high.items():
                if pid in {focal_id, true_id} or pid in neighbors.get(focal_id, set()):
                    continue
                if p["gender"] != gender:
                    continue
                pool.append(p)
            pool.sort(key=lambda p: (abs(p["jd"] - true["jd"]), p["id"]))
            if len(pool) < N_DECOYS:
                dropped["fewer_than_50_same_gender_decoys"] += 1
                continue
            decoys = pool[:N_DECOYS]
            tasks.append({
                "task_key": f"{focal_id}->{true_id}",
                "group_key": f"{min(a,b)}:{max(a,b)}",
                "focal": focal,
                "true": true,
                "decoys": decoys,
                "max_decoy_birth_jd_distance_days": max(abs(p["jd"] - true["jd"]) for p in decoys),
            })
    return high, positive_pairs, tasks, dict(dropped)


def build_rows(tasks):
    west_cache = {}; gate_cache = {}
    rows = []
    for idx, task in enumerate(tasks, 1):
        candidates = [task["true"]] + task["decoys"]
        for cand in candidates:
            rows.append({
                "task_key": task["task_key"],
                "group_key": task["group_key"],
                "actual": int(cand["id"] == task["true"]["id"]),
                "features": feature_row(task["focal"], cand, west_cache, gate_cache),
            })
        if idx % 10 == 0:
            print(f"built features for {idx}/{len(tasks)} directed tasks", flush=True)
    return rows, len(west_cache), len(gate_cache)


def feature_names(model: str, all_names: list[str]) -> list[str]:
    out = []
    for n in all_names:
        if n.startswith("m0_"):
            out.append(n)
        elif model in {"MWS", "MCOMB"} and n.startswith("w_"):
            out.append(n)
        elif model in {"MHDS", "MCOMB"} and n.startswith("hd_"):
            out.append(n)
    return out


def neutral_metrics(rows, scores) -> dict[str, float]:
    by_task: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for r, s in zip(rows, scores):
        by_task[r["task_key"]].append((float(s), int(r["actual"])))
    ranks = []; pcts = []; losses = []
    for vals in by_task.values():
        actual_score = next(s for s, y in vals if y == 1)
        controls = [s for s, y in vals if y == 0]
        higher = sum(s > actual_score + 1e-12 for s in controls)
        tied = sum(abs(s - actual_score) <= 1e-12 for s in controls)
        rank = 1.0 + higher + 0.5 * tied
        pct = 100.0 * (len(controls) - higher - 0.5 * tied) / len(controls)
        ranks.append(rank); pcts.append(pct)
        arr = np.array([s for s, _ in vals], dtype=float)
        arr -= arr.max(); probs = np.exp(arr); probs /= probs.sum()
        idx = next(i for i, (_s, y) in enumerate(vals) if y == 1)
        losses.append(-math.log(max(float(probs[idx]), 1e-15)))
    return {
        "tasks": len(ranks),
        "mean_true_partner_percentile": float(np.mean(pcts)),
        "median_true_partner_percentile": float(np.median(pcts)),
        "top1_rate": float(np.mean([r <= 1.0 + 1e-12 for r in ranks])),
        "top5_rate": float(np.mean([r <= 5.0 + 1e-12 for r in ranks])),
        "mean_reciprocal_rank": float(np.mean([1.0 / r for r in ranks])),
        "softmax_log_loss": float(np.mean(losses)),
    }


def fit_model(Xt, yt, Xv, model, c):
    scaler = StandardScaler().fit(Xt)
    penalty = "l1" if model in {"MWS", "MCOMB"} else "l2"
    clf = LogisticRegression(
        C=c, penalty=penalty, solver="liblinear", class_weight="balanced",
        max_iter=5000, random_state=RNG_SEED % (2**32),
    ).fit(scaler.transform(Xt), yt)
    return clf, clf.decision_function(scaler.transform(Xv))


def choose_c(train_rows, names, model):
    groups = np.array([r["group_key"] for r in train_rows])
    uniq = sorted(set(groups))
    nfold = min(3, max(2, len(uniq) // 5))
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in train_rows], dtype=float)
    y = np.array([r["actual"] for r in train_rows], dtype=int)
    gkf = GroupKFold(n_splits=nfold)
    best = None
    for c in C_GRID:
        vals = []
        for ti, vi in gkf.split(X, y, groups):
            _clf, pred = fit_model(X[ti], y[ti], X[vi], model, c)
            vals.append(neutral_metrics([train_rows[i] for i in vi], pred)["mean_true_partner_percentile"])
        mean = statistics.fmean(vals)
        if best is None or mean > best[0] + 1e-12 or (abs(mean-best[0]) <= 1e-12 and c < best[1]):
            best = (mean, c)
    return best[1]


def evaluate(rows, model, fixed_c=None):
    all_names = sorted(rows[0]["features"])
    names = feature_names(model, all_names)
    groups = np.array([r["group_key"] for r in rows])
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in rows], dtype=float)
    y = np.array([r["actual"] for r in rows], dtype=int)
    gkf = GroupKFold(n_splits=5)
    oof = np.full(len(rows), np.nan)
    cs = []; folds = []; nonzero = []
    for ti, vi in gkf.split(X, y, groups):
        tr = [rows[i] for i in ti]
        c = fixed_c if fixed_c is not None else choose_c(tr, names, model)
        clf, pred = fit_model(X[ti], y[ti], X[vi], model, c)
        oof[vi] = pred
        cs.append(float(c))
        folds.append(neutral_metrics([rows[i] for i in vi], pred)["mean_true_partner_percentile"])
        nonzero.append(int(np.sum(np.abs(clf.coef_[0]) > 1e-10)))
    met = neutral_metrics(rows, oof)
    met.update({
        "model": model, "feature_count": len(names), "outer_folds": 5,
        "selected_C_by_fold": cs, "mean_true_partner_percentile_by_fold": folds,
        "nonzero_feature_count_by_fold": nonzero,
    })
    return met


def modal_c(cs):
    c = Counter(cs); mx = max(c.values())
    return min(k for k, v in c.items() if v == mx)


def permutation(rows, model, observed, cs, n=200):
    rng = random.Random(RNG_SEED)
    fixed_c = modal_c(cs)
    by_task: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows): by_task[r["task_key"]].append(i)
    vals = []
    for p in range(n):
        perm = [dict(r) for r in rows]
        for idxs in by_task.values():
            chosen = rng.choice(idxs)
            for i in idxs: perm[i]["actual"] = int(i == chosen)
        vals.append(evaluate(perm, model, fixed_c=fixed_c)["mean_true_partner_percentile"])
        if (p+1) % 20 == 0: print(f"permutation {p+1}/{n}", flush=True)
    ge = sum(v >= observed - 1e-12 for v in vals)
    return {
        "n": n, "fixed_C": fixed_c, "observed": observed,
        "null_mean": statistics.fmean(vals), "null_sd": statistics.stdev(vals),
        "null_ge_observed": ge, "empirical_p_ge_observed": (ge+1)/(n+1),
    }


def main():
    for p in (EPHE/"sepl_18.se1", EPHE/"semo_18.se1"):
        if not p.is_file(): raise SystemExit("Missing Swiss ephemeris file: "+str(p))
    swe.set_ephe_path(str(EPHE))
    people, neighbors, pair_types, raw_bytes = download_people()
    high, positive_pairs, tasks, dropped = build_tasks(people, neighbors, pair_types)
    if len(positive_pairs) < 25 or len(tasks) < 50:
        raise RuntimeError(f"Unexpectedly too few exact positive pairs/tasks: {len(positive_pairs)} / {len(tasks)}")
    rows, west_cached, gate_cached = build_rows(tasks)
    results = {m: evaluate(rows, m) for m in MODELS}
    m0 = results["M0S"]
    candidates = ("MWS", "MHDS", "MCOMB")
    for m in candidates:
        results[m]["delta_vs_M0S"] = results[m]["mean_true_partner_percentile"] - m0["mean_true_partner_percentile"]
        results[m]["positive_improvement_folds_vs_M0S"] = sum(
            a > b + 1e-12 for a,b in zip(results[m]["mean_true_partner_percentile_by_fold"], m0["mean_true_partner_percentile_by_fold"])
        )
        results[m]["clears_promising_threshold"] = (
            results[m]["mean_true_partner_percentile"] >= 60.0
            and results[m]["delta_vs_M0S"] >= 5.0
            and results[m]["positive_improvement_folds_vs_M0S"] >= 4
            and results[m]["softmax_log_loss"] <= m0["softmax_log_loss"] + 0.05
        )
    best = max(candidates, key=lambda m: results[m]["delta_vs_M0S"])
    perm = permutation(rows, best, results[best]["mean_true_partner_percentile"], results[best]["selected_C_by_fold"], 200)
    max_decoy = [t["max_decoy_birth_jd_distance_days"] for t in tasks]
    out = {
        "status": "development_model_discovery",
        "freeze_spec": str(FREEZE.relative_to(REPO)), "freeze_sha256": sha256(FREEZE),
        "source": URL, "source_raw_bytes": raw_bytes,
        "dataset": {
            "high_quality_exact_people": len(high),
            "positive_unordered_pairs": len(positive_pairs),
            "directed_identification_tasks": len(tasks),
            "decoys_per_task": N_DECOYS,
            "candidate_rows": len(rows),
            "dropped_tasks": dropped,
            "median_farthest_decoy_birth_distance_days": float(np.median(max_decoy)),
            "max_farthest_decoy_birth_distance_days": float(np.max(max_decoy)),
            "western_natal_cache_people": west_cached,
            "hd_gate_cache_people": gate_cached,
        },
        "results": results,
        "best_pair_family": best,
        "any_pair_family_clears_frozen_threshold": any(results[m]["clears_promising_threshold"] for m in candidates),
        "permutation_diagnostic_for_selected_family": perm,
        "limitations": [
            "Development on the public C-sample; independent validation is still required.",
            "Hard decoys match recorded gender and birth generation, but not real-world exposure/social network.",
            "Recorded romantic linkage establishes partnership, not relationship quality or mutual benefit.",
            "The C-sample is a non-random public-figure-heavy subset of Astro-Databank.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True), flush=True)
    print("wrote", OUT, "sha256", sha256(OUT), flush=True)


if __name__ == "__main__":
    main()
