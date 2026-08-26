#!/usr/bin/env python3
"""High-resolution ADB pair-timing model discovery V2.

Frozen spec: reference/research/adb_pair_timing_model_discovery_freeze_v2.md
Development/model-discovery only. Uses verified SWIEPH via the V1 helpers and
fails closed on ephemeris fallback.
"""
from __future__ import annotations

import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

import adb_pair_timing_model_search_v1 as base

REPO = Path(__file__).resolve().parents[1]
FREEZE = REPO / "reference" / "research" / "adb_pair_timing_model_discovery_freeze_v2.md"
OUT = REPO / "reference" / "research" / "adb_pair_timing_model_discovery_results_v2.json"
C_GRID = (0.001, 0.01, 0.1, 1.0)
RNG_SEED = 202608261311
MODELS = ("M0HR", "M1HR", "XPROGHR", "NCOMPHR", "PCOMPHR", "ALLHR")


def aspect_kernel(moving: float, target: float, aspect: int, sigma: float) -> float:
    r = base.aspect_residual(moving, target, aspect)
    return math.exp(-0.5 * (r / sigma) ** 2)


def raw_features(ev: base.EventRecord, y: int, m: int, d: int) -> dict[str, float]:
    cj = base.date_jd(y, m, d, 12.0)
    a_birth = ev.focal.exact_jd
    b_birth = ev.partner.parity_birth_jd()
    assert a_birth is not None and b_birth is not None

    na = base.natal_positions(a_birth)
    nb = base.natal_positions(b_birth)
    pa = base.progressed_positions(a_birth, cj)
    pb = base.progressed_positions(b_birth, cj)
    tr = {n: base.calc(cj, b)[0] for n, b in base.TRANSIT_BODIES.items()}

    f: dict[str, float] = {
        "m0_age_a": (cj - a_birth) / base.TROPICAL_YEAR,
        "m0_age_b": (cj - b_birth) / base.TROPICAL_YEAR,
        "m0_year_scaled": (y - 1950.0) / 50.0,
    }

    # Individual timing: every explicit mover -> own natal target -> aspect.
    for side, natal, prog in (("a", na, pa), ("b", nb, pb)):
        for mover, mlon in tr.items():
            for target, tlon in natal.items():
                for asp in base.ASPECTS:
                    f[f"m1_{side}_tr_{mover}_{target}_a{asp}"] = aspect_kernel(mlon, tlon, asp, 1.5)
        for mover, mlon in prog.items():
            for target, tlon in natal.items():
                for asp in base.ASPECTS:
                    f[f"m1_{side}_pr_{mover}_{target}_a{asp}"] = aspect_kernel(mlon, tlon, asp, 1.0)

    # Cross-progressions.
    for mover, mlon in pa.items():
        for target, tlon in nb.items():
            for asp in base.ASPECTS:
                f[f"xp_pa_nb_{mover}_{target}_a{asp}"] = aspect_kernel(mlon, tlon, asp, 1.0)
    for mover, mlon in pb.items():
        for target, tlon in na.items():
            for asp in base.ASPECTS:
                f[f"xp_pb_na_{mover}_{target}_a{asp}"] = aspect_kernel(mlon, tlon, asp, 1.0)
    for mover_a, lon_a in pa.items():
        for mover_b, lon_b in pb.items():
            for asp in base.ASPECTS:
                f[f"xp_pa_pb_{mover_a}_{mover_b}_a{asp}"] = aspect_kernel(lon_a, lon_b, asp, 1.0)

    # Natal midpoint-composite transits.
    ncomp = {n: base.midpoint(na[n], nb[n]) for n in base.NATAL_BODIES}
    for mover, mlon in tr.items():
        for target, tlon in ncomp.items():
            for asp in base.ASPECTS:
                f[f"nc_tr_{mover}_{target}_a{asp}"] = aspect_kernel(mlon, tlon, asp, 1.5)

    # Progressed midpoint-composite transits.
    pcomp = {n: base.midpoint(pa[n], pb[n]) for n in base.PROG_BODIES}
    for mover, mlon in tr.items():
        for target, tlon in pcomp.items():
            for asp in base.ASPECTS:
                f[f"pc_tr_{mover}_{target}_a{asp}"] = aspect_kernel(mlon, tlon, asp, 1.5)
    return f


def build_rows(events: list[base.EventRecord]) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    counts = Counter()
    for ev in events:
        if ev.transition != "formation":
            continue
        candidates = [(ev.year, ev.month, ev.day, True, False)]
        for dy in base.SHIFT_YEARS:
            shifted = base.safe_shift(ev.year, ev.month, ev.day, dy)
            if not shifted:
                continue
            y, m, d, adjusted = shifted
            a_jd = ev.focal.exact_jd
            b_jd = ev.partner.parity_birth_jd()
            assert a_jd is not None and b_jd is not None
            cj = base.date_jd(y, m, d, 12.0)
            age_a = (cj - a_jd) / base.TROPICAL_YEAR
            age_b = (cj - b_jd) / base.TROPICAL_YEAR
            if not (16 <= age_a <= 85 and 16 <= age_b <= 85):
                counts["control_age_excluded"] += 1
                continue
            candidates.append((y, m, d, False, adjusted))
        if len(candidates) < 6:
            counts["event_too_few_controls"] += 1
            continue
        event_key = f"{ev.pair_key}|{ev.event_id}|{ev.year:04d}-{ev.month:02d}-{ev.day:02d}"
        for y, m, d, actual, adjusted in candidates:
            rows.append({
                "event_key": event_key,
                "pair_key": ev.pair_key,
                "actual": int(actual),
                "candidate_date": f"{y:04d}-{m:02d}-{d:02d}",
                "leap_adjusted": adjusted,
                "features": raw_features(ev, y, m, d),
            })
    return rows, dict(counts)


def feature_names(model: str, all_names: list[str]) -> list[str]:
    out = []
    for n in all_names:
        if n.startswith("m0_"):
            out.append(n)
        elif model != "M0HR" and n.startswith("m1_"):
            out.append(n)
        elif model in {"XPROGHR", "ALLHR"} and n.startswith("xp_"):
            out.append(n)
        elif model in {"NCOMPHR", "ALLHR"} and n.startswith("nc_"):
            out.append(n)
        elif model in {"PCOMPHR", "ALLHR"} and n.startswith("pc_"):
            out.append(n)
    return out


def metric_scores(rows: list[dict], scores: np.ndarray) -> dict[str, float]:
    by_event: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for row, score in zip(rows, scores):
        by_event[row["event_key"]].append((float(score), int(row["actual"])))
    ranks: list[int] = []
    pct: list[float] = []
    losses: list[float] = []
    for vals in by_event.values():
        vals.sort(key=lambda x: x[0], reverse=True)
        rank = next(i + 1 for i, (_, y) in enumerate(vals) if y == 1)
        n = len(vals)
        ranks.append(rank)
        pct.append(100.0 if n == 1 else 100.0 * (n - rank) / (n - 1))
        arr = np.array([s for s, _ in vals], dtype=float)
        arr -= arr.max()
        probs = np.exp(arr); probs /= probs.sum()
        idx = next(i for i, (_, y) in enumerate(vals) if y == 1)
        losses.append(-math.log(max(float(probs[idx]), 1e-15)))
    return {
        "events": len(ranks),
        "mean_true_date_percentile": float(np.mean(pct)),
        "median_true_date_percentile": float(np.median(pct)),
        "top1_rate": float(np.mean([r == 1 for r in ranks])),
        "top3_rate": float(np.mean([r <= 3 for r in ranks])),
        "mean_reciprocal_rank": float(np.mean([1.0 / r for r in ranks])),
        "softmax_log_loss": float(np.mean(losses)),
    }


def fit_l1(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, c: float):
    scaler = StandardScaler().fit(X_train)
    xt = scaler.transform(X_train)
    xv = scaler.transform(X_test)
    clf = LogisticRegression(
        C=c,
        penalty="l1",
        solver="liblinear",
        class_weight="balanced",
        max_iter=5000,
        random_state=RNG_SEED,
    ).fit(xt, y_train)
    return clf, clf.decision_function(xv)


def choose_c(train_rows: list[dict], names: list[str]) -> float:
    groups = np.array([r["pair_key"] for r in train_rows])
    unique = sorted(set(groups))
    if len(unique) < 6:
        return 0.01
    nsplit = min(3, max(2, len(unique) // 5))
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in train_rows], dtype=float)
    y = np.array([r["actual"] for r in train_rows], dtype=int)
    gkf = GroupKFold(n_splits=nsplit)
    best: tuple[float, float] | None = None
    for c in C_GRID:
        fold_scores = []
        for ti, vi in gkf.split(X, y, groups):
            _, pred = fit_l1(X[ti], y[ti], X[vi], c)
            met = metric_scores([train_rows[i] for i in vi], pred)
            fold_scores.append(met["mean_true_date_percentile"])
        score = statistics.fmean(fold_scores)
        if best is None or score > best[0] + 1e-12 or (abs(score - best[0]) < 1e-12 and c < best[1]):
            best = (score, c)
    assert best is not None
    return best[1]


def stability_summary(fold_coefs: list[dict[str, float]], top_n: int = 30) -> list[dict]:
    agg: dict[str, list[float]] = defaultdict(list)
    for coefs in fold_coefs:
        for name, value in coefs.items():
            if abs(value) > 1e-10:
                agg[name].append(value)
    rows = []
    total_folds = len(fold_coefs)
    for name, vals in agg.items():
        pos = sum(v > 0 for v in vals); neg = sum(v < 0 for v in vals)
        rows.append({
            "feature": name,
            "selected_folds": len(vals),
            "total_folds": total_folds,
            "positive_folds": pos,
            "negative_folds": neg,
            "sign_consistent": pos == 0 or neg == 0,
            "mean_coef_when_selected": statistics.fmean(vals),
            "mean_abs_coef_when_selected": statistics.fmean(abs(v) for v in vals),
        })
    rows.sort(key=lambda r: (r["selected_folds"], r["sign_consistent"], r["mean_abs_coef_when_selected"]), reverse=True)
    return rows[:top_n]


def evaluate(rows: list[dict], model: str, fixed_c: float | None = None) -> tuple[dict, np.ndarray]:
    all_names = sorted(rows[0]["features"])
    names = feature_names(model, all_names)
    groups = np.array([r["pair_key"] for r in rows])
    unique = sorted(set(groups))
    nsplit = min(5, len(unique) // 5)
    if nsplit < 2:
        raise RuntimeError("too few grouped couples")
    X = np.array([[r["features"].get(n, 0.0) for n in names] for r in rows], dtype=float)
    y = np.array([r["actual"] for r in rows], dtype=int)
    gkf = GroupKFold(n_splits=nsplit)
    oof = np.full(len(rows), np.nan)
    selected_cs = []
    fold_metrics = []
    fold_coefs: list[dict[str, float]] = []
    for ti, vi in gkf.split(X, y, groups):
        train_rows = [rows[i] for i in ti]
        c = fixed_c if fixed_c is not None else choose_c(train_rows, names)
        selected_cs.append(float(c))
        clf, pred = fit_l1(X[ti], y[ti], X[vi], float(c))
        oof[vi] = pred
        fold_metrics.append(metric_scores([rows[i] for i in vi], pred)["mean_true_date_percentile"])
        fold_coefs.append({n: float(v) for n, v in zip(names, clf.coef_[0]) if abs(v) > 1e-10})
    met = metric_scores(rows, oof)
    met.update({
        "model": model,
        "feature_count": len(names),
        "outer_folds": nsplit,
        "selected_C_by_fold": selected_cs,
        "mean_true_date_percentile_by_fold": fold_metrics,
        "nonzero_feature_count_by_fold": [len(x) for x in fold_coefs],
        "stable_selected_features": stability_summary(fold_coefs),
    })
    return met, oof


def modal_c(cs: list[float]) -> float:
    counts = Counter(cs)
    mx = max(counts.values())
    return min(c for c, n in counts.items() if n == mx)


def permutation_diagnostic(rows: list[dict], model: str, observed: dict, n: int = 100) -> dict:
    rng = random.Random(RNG_SEED)
    fixed_c = modal_c([float(c) for c in observed["selected_C_by_fold"]])
    by_event: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        by_event[r["event_key"]].append(i)
    null = []
    for p in range(n):
        perm_rows = [dict(r) for r in rows]
        for idxs in by_event.values():
            chosen = rng.choice(idxs)
            for i in idxs:
                perm_rows[i]["actual"] = int(i == chosen)
        met, _ = evaluate(perm_rows, model, fixed_c=fixed_c)
        null.append(met["mean_true_date_percentile"])
        if (p + 1) % 10 == 0:
            print(f"permutation {p+1}/{n}", flush=True)
    obs = observed["mean_true_date_percentile"]
    ge = sum(x >= obs - 1e-12 for x in null)
    return {
        "n": n,
        "fixed_C": fixed_c,
        "observed_mean_true_date_percentile": obs,
        "null_mean_percentile": statistics.fmean(null),
        "null_sd_percentile": statistics.stdev(null),
        "null_ge_observed": ge,
        "empirical_p_ge_observed": (ge + 1) / (n + 1),
    }


def main() -> None:
    # V1 helper enforces the same pinned SWIEPH flag policy.
    for p in (base.EPHE / "sepl_18.se1", base.EPHE / "semo_18.se1"):
        if not p.is_file():
            raise SystemExit("Missing Swiss ephemeris file: " + str(p))
    base.swe.set_ephe_path(str(base.EPHE))
    for j in (base.date_jd(1800, 1, 2), base.date_jd(1950, 1, 1), base.date_jd(2026, 1, 1), base.date_jd(2398, 1, 1)):
        for body in list(base.NATAL_BODIES.values()) + list(base.TRANSIT_BODIES.values()):
            base.calc(j, body)

    persons, rels, events_raw, raw_bytes = base.download_parse()
    events, parser_exclusions = base.build_events(persons, rels, events_raw)
    formation = [e for e in events if e.transition == "formation"]
    rows, control_exclusions = build_rows(formation)
    dataset = {
        "formation_events_pre_controls": len(formation),
        "formation_pairs_pre_controls": len({e.pair_key for e in formation}),
        "precision": dict(Counter(e.precision for e in formation)),
        "event_types": dict(Counter(e.event_name for e in formation)),
        "usable_events": len({r["event_key"] for r in rows}),
        "usable_pairs": len({r["pair_key"] for r in rows}),
        "rows": len(rows),
        "parser_exclusions": parser_exclusions,
        "control_exclusions": control_exclusions,
    }
    print("dataset", json.dumps(dataset, indent=2), flush=True)

    results: dict[str, dict] = {}
    for model in MODELS:
        print("evaluating", model, flush=True)
        met, _ = evaluate(rows, model)
        results[model] = met
        print(model, met["mean_true_date_percentile"], met["softmax_log_loss"], flush=True)

    m1 = results["M1HR"]
    pair_models = ("XPROGHR", "NCOMPHR", "PCOMPHR", "ALLHR")
    best = max(pair_models, key=lambda m: results[m]["mean_true_date_percentile"] - m1["mean_true_date_percentile"])
    for m in pair_models:
        results[m]["delta_mean_percentile_vs_M1HR"] = results[m]["mean_true_date_percentile"] - m1["mean_true_date_percentile"]
        results[m]["delta_softmax_loss_vs_M1HR"] = results[m]["softmax_log_loss"] - m1["softmax_log_loss"]
        fold_deltas = [a - b for a, b in zip(results[m]["mean_true_date_percentile_by_fold"], m1["mean_true_date_percentile_by_fold"])]
        results[m]["fold_percentile_deltas_vs_M1HR"] = fold_deltas
        results[m]["positive_improvement_folds"] = sum(x > 0 for x in fold_deltas)
        results[m]["clears_frozen_promising_threshold"] = (
            results[m]["delta_mean_percentile_vs_M1HR"] >= 5.0
            and results[m]["delta_softmax_loss_vs_M1HR"] <= 0.05
            and results[m]["positive_improvement_folds"] >= 3
        )

    perm = permutation_diagnostic(rows, best, results[best], 100)
    data = {
        "status": "development_model_discovery",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": base.sha256(FREEZE),
        "source": base.URL,
        "source_raw_bytes": raw_bytes,
        "ephemeris": {
            "requested": "SWIEPH",
            "returned": "SWIEPH or abort",
            "sepl_18_sha256": base.sha256(base.EPHE / "sepl_18.se1"),
            "semo_18_sha256": base.sha256(base.EPHE / "semo_18.se1"),
        },
        "dataset": dataset,
        "results": results,
        "best_pair_family_by_mean_percentile_improvement": best,
        "permutation_diagnostic": perm,
        "any_pair_family_clears_frozen_threshold": any(results[m]["clears_frozen_promising_threshold"] for m in pair_models),
        "interpretation_rule": "If no pair family clears threshold, conclude this C-sample/date-only design has not found a useful pair-dynamic timing model; do not tune on coefficients.",
        "limitations": [
            "Openly developmental model discovery; not independent validation.",
            "Most linked partners are date-only, so Moon/houses/angles/HD are absent.",
            "Formation events are dominated by marriage events.",
            "True event date is compared with same month/day at +/-1..10 years, not with a full semi-Markov risk process.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "dataset": dataset,
        "summary": {m: {
            "pct": results[m]["mean_true_date_percentile"],
            "loss": results[m]["softmax_log_loss"],
            "delta_pct": results[m].get("delta_mean_percentile_vs_M1HR"),
            "delta_loss": results[m].get("delta_softmax_loss_vs_M1HR"),
            "clears": results[m].get("clears_frozen_promising_threshold"),
        } for m in MODELS},
        "best": best,
        "permutation": perm,
    }, indent=2), flush=True)
    print("wrote", OUT, "sha256", base.sha256(OUT), flush=True)


if __name__ == "__main__":
    main()
