#!/usr/bin/env python3
"""Engineering runner for frozen V2 model discovery.

Two implementation adapters leave the frozen astrology/model specification
unchanged:
1. sklearn receives a deterministic 32-bit projection of the frozen seed;
2. event-rank ties receive neutral average rank instead of stable-sort priority.
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

import adb_pair_timing_model_discovery_v2 as v2
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def fit_l1_32bit(X_train, y_train, X_test, c):
    scaler = StandardScaler().fit(X_train)
    xt = scaler.transform(X_train)
    xv = scaler.transform(X_test)
    clf = LogisticRegression(
        C=c,
        penalty="l1",
        solver="liblinear",
        class_weight="balanced",
        max_iter=5000,
        random_state=v2.RNG_SEED % (2**32),
    ).fit(xt, y_train)
    return clf, clf.decision_function(xv)


def metric_scores_neutral_ties(rows, scores):
    by_event = defaultdict(list)
    for row, score in zip(rows, scores):
        by_event[row["event_key"]].append((float(score), int(row["actual"])))

    average_ranks = []
    percentiles = []
    losses = []
    tol = 1e-12

    for vals in by_event.values():
        true_scores = [s for s, y in vals if y == 1]
        if len(true_scores) != 1:
            raise RuntimeError(f"expected exactly one true candidate, got {len(true_scores)}")
        true_score = true_scores[0]
        controls = [s for s, y in vals if y == 0]
        higher = sum(s > true_score + tol for s in controls)
        lower = sum(s < true_score - tol for s in controls)
        tied = len(controls) - higher - lower
        rank_avg = 1.0 + higher + 0.5 * tied
        pct = 50.0 if not controls else 100.0 * (lower + 0.5 * tied) / len(controls)
        average_ranks.append(rank_avg)
        percentiles.append(pct)

        arr = np.array([s for s, _ in vals], dtype=float)
        actual_index = next(i for i, (_, y) in enumerate(vals) if y == 1)
        arr -= arr.max()
        probs = np.exp(arr)
        probs /= probs.sum()
        losses.append(-math.log(max(float(probs[actual_index]), 1e-15)))

    return {
        "events": len(average_ranks),
        "mean_true_date_percentile": float(np.mean(percentiles)),
        "median_true_date_percentile": float(np.median(percentiles)),
        "top1_rate": float(np.mean([r <= 1.0 + tol for r in average_ranks])),
        "top3_rate": float(np.mean([r <= 3.0 + tol for r in average_ranks])),
        "mean_reciprocal_rank": float(np.mean([1.0 / r for r in average_ranks])),
        "softmax_log_loss": float(np.mean(losses)),
        "tie_handling": "neutral_average_rank",
    }


if __name__ == "__main__":
    v2.fit_l1 = fit_l1_32bit
    v2.metric_scores = metric_scores_neutral_ties
    v2.main()
