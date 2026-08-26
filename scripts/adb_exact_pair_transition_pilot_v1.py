#!/usr/bin/env python3
"""Underpowered exact-time ADB pair transition pilot V1.

Frozen spec: reference/research/adb_exact_pair_transition_pilot_freeze_v1.md
Development/hypothesis generation only. Uses verified SWIEPH and the existing
HD timing engine; no Joel/Bee data enter model fitting.
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
OUT = REPO / "reference" / "research" / "adb_exact_pair_transition_pilot_results_v1.json"
FREEZE = REPO / "reference" / "research" / "adb_exact_pair_transition_pilot_freeze_v1.md"
URL = base.URL
C_FIXED = 0.1
RNG_SEED = 202608261432
ASPECTS = base.ASPECTS
SHIFT_YEARS = base.SHIFT_YEARS

NATAL_BODIES = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}
PROG_BODIES = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
}
TRANSIT_BODIES = base.TRANSIT_BODIES
MODELS = ("M0X", "M1X", "M3X", "M4X_HD", "M3X_HD")


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
    t = s.strip().lower()
    m = re.fullmatch(r"(\d{1,3})([nsew])(\d{1,2})", t)
    if not m:
        return None
    deg = int(m.group(1)); hemi = m.group(2); minute = int(m.group(3))
    limit = 90 if is_lat else 180
    if deg > limit or minute >= 60:
        return None
    val = deg + minute / 60.0
    if hemi in {"s", "w"}:
        val = -val
    return val


def download_coords() -> tuple[dict[int, tuple[float, float]], int]:
    req = urllib.request.Request(URL, headers={"User-Agent": "humandesign-exact-pair-pilot/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    root = ET.fromstring(raw)
    coords: dict[int, tuple[float, float]] = {}
    for e in root.findall("adb_entry"):
        aid = int(e.attrib["adb_id"])
        place = e.find("./public_data/bdata/place")
        if place is None:
            continue
        lat = parse_coord(place.attrib.get("slati"), True)
        lon = parse_coord(place.attrib.get("slong"), False)
        if lat is not None and lon is not None:
            coords[aid] = (lat, lon)
    return coords, len(raw)


def aspect_kernel(moving: float, target: float, sigma: float) -> float:
    r = min(base.aspect_residual(moving, target, a) for a in ASPECTS)
    return math.exp(-0.5 * (r / sigma) ** 2)


def max_activation(moving: float, targets: dict[str, float], sigma: float) -> float:
    if not targets:
        return 0.0
    return max(aspect_kernel(moving, t, sigma) for t in targets.values())


def natal_targets(birth_jd: float, coord: tuple[float, float] | None) -> dict[str, float]:
    out = {n: base.calc(birth_jd, b)[0] for n, b in NATAL_BODIES.items()}
    if coord is not None:
        lat, lon = coord
        try:
            _cusps, ascmc = swe.houses_ex(birth_jd, lat, lon, b"P", 0)
            out["ASC"] = float(ascmc[0] % 360.0)
            out["MC"] = float(ascmc[1] % 360.0)
        except Exception:
            pass
    return out


def progressed(birth_jd: float, candidate_jd: float) -> dict[str, float]:
    age_years = (candidate_jd - birth_jd) / base.TROPICAL_YEAR
    pj = birth_jd + age_years
    return {n: base.calc(pj, b)[0] for n, b in PROG_BODIES.items()}


def midpoint(a: float, b: float) -> float:
    return base.midpoint(a, b)


def western_features(ev: base.EventRecord, y: int, m: int, d: int, coords: dict[int, tuple[float, float]]) -> dict[str, float]:
    cj = base.date_jd(y, m, d, 12.0)
    a_birth = ev.focal.exact_jd
    b_birth = ev.partner.exact_jd
    assert a_birth is not None and b_birth is not None

    na = natal_targets(a_birth, coords.get(ev.focal.adb_id))
    nb = natal_targets(b_birth, coords.get(ev.partner.adb_id))
    pa = progressed(a_birth, cj)
    pb = progressed(b_birth, cj)
    tr = {n: base.calc(cj, body)[0] for n, body in TRANSIT_BODIES.items()}

    age_a = (cj - a_birth) / base.TROPICAL_YEAR
    age_b = (cj - b_birth) / base.TROPICAL_YEAR
    f: dict[str, float] = {
        "m0_age_a": age_a,
        "m0_age_b": age_b,
        "m0_abs_age_diff": abs(age_a - age_b),
        "m0_year_scaled": (y - 1950.0) / 50.0,
    }
    for eid in sorted(base.EVENTS):
        f[f"m0_event_{eid}"] = 1.0 if ev.event_id == eid else 0.0

    for side, natal, prog in (("a", na, pa), ("b", nb, pb)):
        for mover, mlon in tr.items():
            f[f"m1_{side}_tr_{mover}"] = max_activation(mlon, natal, 1.5)
        for mover, mlon in prog.items():
            sigma = 1.5 if mover == "Moon" else 1.0
            f[f"m1_{side}_pr_{mover}"] = max_activation(mlon, natal, sigma)

    for mover, mlon in pa.items():
        sigma = 1.5 if mover == "Moon" else 1.0
        f[f"m3_pa_nb_{mover}"] = max_activation(mlon, nb, sigma)
    for mover, mlon in pb.items():
        sigma = 1.5 if mover == "Moon" else 1.0
        f[f"m3_pb_na_{mover}"] = max_activation(mlon, na, sigma)
    for mover, mlon in pa.items():
        sigma = 1.5 if mover == "Moon" else 1.0
        f[f"m3_pa_pb_{mover}"] = max_activation(mlon, pb, sigma)

    common = [n for n in NATAL_BODIES if n in na and n in nb]
    ncomp = {n: midpoint(na[n], nb[n]) for n in common}
    for mover, mlon in tr.items():
        f[f"m3_ncomp_tr_{mover}"] = max_activation(mlon, ncomp, 1.5)
    return f


def hd_features(ev: base.EventRecord, y: int, m: int, d: int, gate_cache: dict[int, set[int]]) -> dict[str, float]:
    a_id = ev.focal.adb_id; b_id = ev.partner.adb_id
    if a_id not in gate_cache:
        gate_cache[a_id] = hd.natal_gates(hd.dt_from_jd(ev.focal.exact_jd))
    if b_id not in gate_cache:
        gate_cache[b_id] = hd.natal_gates(hd.dt_from_jd(ev.partner.exact_jd))
    dt = hd.dt_from_jd(base.date_jd(y, m, d, 12.0))
    _by, tg = hd.transit_gate_state(dt)
    fp = hd.fingerprint(gate_cache[a_id] | gate_cache[b_id] | tg)
    return {
        "hd_single": 1.0 if fp["definition_components"] == 1 else 0.0,
        "hd_eight": 1.0 if fp["defined_center_count"] == 8 else 0.0,
    }


def build_exact_events() -> tuple[list[base.EventRecord], dict, dict[int, tuple[float, float]], int]:
    persons, rels, events, _raw_bytes_base = base.download_parse()
    records, exclusions = base.build_events(persons, rels, events)
    exact = []
    seen = set()
    extra = Counter()
    for ev in records:
        if ev.partner.adb_id not in persons:
            continue
        partner = persons[ev.partner.adb_id]
        if not partner.high_timed:
            continue
        # build_events already requires focal high-timed.
        key = (ev.pair_key, ev.event_id, ev.year, ev.month, ev.day)
        if key in seen:
            extra["duplicate_after_exact_filter"] += 1
            continue
        seen.add(key)
        exact.append(ev)
    coords, raw_bytes = download_coords()
    return exact, {**exclusions, **extra}, coords, raw_bytes


def build_rows(events: list[base.EventRecord], coords: dict[int, tuple[float, float]]) -> tuple[list[dict], dict]:
    rows = []
    counts = Counter()
    gate_cache: dict[int, set[int]] = {}
    for ev in events:
        if ev.transition != "formation":
            continue
        candidates = [(ev.year, ev.month, ev.day, True)]
        for dy in SHIFT_YEARS:
            shifted = base.safe_shift(ev.year, ev.month, ev.day, dy)
            if not shifted:
                continue
            y, m, d, _adj = shifted
            cj = base.date_jd(y, m, d, 12.0)
            a_birth = ev.focal.exact_jd; b_birth = ev.partner.exact_jd
            assert a_birth is not None and b_birth is not None
            age_a = (cj - a_birth) / base.TROPICAL_YEAR
            age_b = (cj - b_birth) / base.TROPICAL_YEAR
            if not (16 <= age_a <= 85 and 16 <= age_b <= 85):
                counts["control_age_excluded"] += 1
                continue
            candidates.append((y, m, d, False))
        if len(candidates) < 6:
            counts["event_too_few_controls"] += 1
            continue
        event_key = f"{ev.pair_key}|{ev.event_id}|{ev.year:04d}-{ev.month:02d}-{ev.day:02d}"
        for y, m, d, actual in candidates:
            f = western_features(ev, y, m, d, coords)
            f.update(hd_features(ev, y, m, d, gate_cache))
            rows.append({
                "event_key": event_key,
                "pair_key": ev.pair_key,
                "actual": int(actual),
                "features": f,
            })
    return rows, dict(counts)


def names_for(model: str, all_names: list[str]) -> list[str]:
    names = []
    for n in all_names:
        if n.startswith("m0_"):
            names.append(n)
        elif model != "M0X" and n.startswith("m1_"):
            names.append(n)
        elif model in {"M3X", "M3X_HD"} and n.startswith("m3_"):
            names.append(n)
        elif model in {"M4X_HD", "M3X_HD"} and n.startswith("hd_"):
            names.append(n)
    return names


def metrics(rows: list[dict], scores: np.ndarray) -> dict[str, float]:
    by_event: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for r, s in zip(rows, scores):
        by_event[r["event_key"]].append((float(s), int(r["actual"])))
    ranks = []; pcts = []; losses = []
    for vals in by_event.values():
        actual_score = next(s for s, y in vals if y == 1)
        controls = [s for s, y in vals if y == 0]
        higher = sum(s > actual_score + 1e-12 for s in controls)
        tied = sum(abs(s - actual_score) <= 1e-12 for s in controls)
        avg_rank = 1.0 + higher + 0.5 * tied
        pct = 100.0 * (len(controls) - higher - 0.5 * tied) / len(controls)
        ranks.append(avg_rank); pcts.append(pct)
        arr = np.array([s for s, _ in vals], dtype=float)
        arr -= arr.max(); probs = np.exp(arr); probs /= probs.sum()
        idx = next(i for i, (_s, y) in enumerate(vals) if y == 1)
        losses.append(-math.log(max(float(probs[idx]), 1e-15)))
    return {
        "events": len(ranks),
        "mean_true_date_percentile": float(np.mean(pcts)),
        "median_true_date_percentile": float(np.median(pcts)),
        "top1_rate": float(np.mean([r <= 1.0 + 1e-12 for r in ranks])),
        "top3_rate": float(np.mean([r <= 3.0 + 1e-12 for r in ranks])),
        "mean_reciprocal_rank": float(np.mean([1.0 / r for r in ranks])),
        "softmax_log_loss": float(np.mean(losses)),
    }


def fit_predict(Xt, yt, Xv):
    scaler = StandardScaler().fit(Xt)
    clf = LogisticRegression(
        C=C_FIXED,
        penalty="l2",
        solver="liblinear",
        class_weight="balanced",
        max_iter=5000,
        random_state=RNG_SEED % (2**32),
    ).fit(scaler.transform(Xt), yt)
    return clf.decision_function(scaler.transform(Xv))


def evaluate(rows: list[dict], model: str) -> dict:
    all_names = sorted(rows[0]["features"])
    names = names_for(model, all_names)
    groups = np.array([r["pair_key"] for r in rows])
    unique_pairs = sorted(set(groups))
    nfold = min(4, max(2, len(unique_pairs) // 3))
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in rows], dtype=float)
    y = np.array([r["actual"] for r in rows], dtype=int)
    gkf = GroupKFold(n_splits=nfold)
    oof = np.full(len(rows), np.nan)
    fold_pcts = []
    for ti, vi in gkf.split(X, y, groups):
        pred = fit_predict(X[ti], y[ti], X[vi])
        oof[vi] = pred
        fold_pcts.append(metrics([rows[i] for i in vi], pred)["mean_true_date_percentile"])
    out = metrics(rows, oof)
    out.update({
        "model": model,
        "feature_count": len(names),
        "outer_folds": nfold,
        "mean_true_date_percentile_by_fold": fold_pcts,
    })
    return out


def permutation(rows: list[dict], model: str, observed: float, n: int = 200) -> dict:
    rng = random.Random(RNG_SEED)
    by_event: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        by_event[r["event_key"]].append(i)
    vals = []
    for _ in range(n):
        perm = [dict(r) for r in rows]
        for idxs in by_event.values():
            chosen = rng.choice(idxs)
            for i in idxs:
                perm[i]["actual"] = int(i == chosen)
        vals.append(evaluate(perm, model)["mean_true_date_percentile"])
    ge = sum(v >= observed - 1e-12 for v in vals)
    return {
        "n": n,
        "observed": observed,
        "null_mean": statistics.fmean(vals),
        "null_sd": statistics.stdev(vals),
        "null_ge_observed": ge,
        "empirical_p_ge_observed": (ge + 1) / (n + 1),
    }


def main() -> None:
    for p in (base.EPHE / "sepl_18.se1", base.EPHE / "semo_18.se1"):
        if not p.is_file():
            raise SystemExit("Missing Swiss ephemeris file: " + str(p))
    swe.set_ephe_path(str(base.EPHE))

    exact_events, parser_exclusions, coords, raw_bytes = build_exact_events()
    formation = [e for e in exact_events if e.transition == "formation"]
    dissolution = [e for e in exact_events if e.transition == "dissolution"]
    dataset = {
        "exact_events": len(exact_events),
        "exact_pairs": len(set(e.pair_key for e in exact_events)),
        "formation_events": len(formation),
        "formation_pairs": len(set(e.pair_key for e in formation)),
        "dissolution_events": len(dissolution),
        "dissolution_pairs": len(set(e.pair_key for e in dissolution)),
        "event_types": dict(Counter(e.event_name for e in exact_events)),
        "precision": dict(Counter(e.precision for e in exact_events)),
        "coordinate_records_parseable": len(coords),
        "parser_exclusions": parser_exclusions,
    }

    result = {
        "status": "underpowered_development_hypothesis_generation",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "source": URL,
        "source_raw_bytes": raw_bytes,
        "dataset": dataset,
        "models": {},
        "comparison": {},
        "permutation": None,
        "limitations": [
            "Fewer than the declared 50 exact high-quality pairs; no validation claim is allowed.",
            "C-sample is reused after date-only development work, so this is not independent replication.",
            "Formation events are likely dominated by marriage rather than first romantic contact.",
        ],
    }

    if len(set(e.pair_key for e in formation)) < 10 or len(formation) < 10:
        result["status"] = "insufficient_even_for_exact_pilot"
    else:
        rows, control_exclusions = build_rows(exact_events, coords)
        result["dataset"]["candidate_rows"] = len(rows)
        result["dataset"]["control_exclusions"] = control_exclusions
        for model in MODELS:
            result["models"][model] = evaluate(rows, model)
        m0 = result["models"]["M0X"]["mean_true_date_percentile"]
        m1 = result["models"]["M1X"]["mean_true_date_percentile"]
        for model in ("M3X", "M4X_HD", "M3X_HD"):
            met = result["models"][model]
            met["delta_vs_M1X"] = met["mean_true_date_percentile"] - m1
            met["positive_improvement_folds_vs_M1X"] = sum(
                a > b + 1e-12
                for a, b in zip(met["mean_true_date_percentile_by_fold"], result["models"]["M1X"]["mean_true_date_percentile_by_fold"])
            )
        result["comparison"] = {
            "M1X_minus_M0X": m1 - m0,
            "best_pair_family": max(("M3X", "M4X_HD", "M3X_HD"), key=lambda k: result["models"][k]["delta_vs_M1X"]),
        }
        best = result["comparison"]["best_pair_family"]
        best_delta = result["models"][best]["delta_vs_M1X"]
        result["comparison"]["best_delta_vs_M1X"] = best_delta
        if best_delta >= 5.0:
            result["permutation"] = permutation(rows, best, result["models"][best]["mean_true_date_percentile"], 200)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    print("wrote", OUT, "sha256", sha256(OUT), flush=True)


if __name__ == "__main__":
    main()
