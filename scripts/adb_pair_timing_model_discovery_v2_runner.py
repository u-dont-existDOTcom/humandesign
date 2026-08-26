#!/usr/bin/env python3
"""Engineering runner for frozen V2 model discovery.

scikit-learn requires random_state <= 2**32-1. The frozen reproducibility seed
remains unchanged for Python permutation generation; only the estimator receives
a deterministic 32-bit projection of that seed.
"""
from __future__ import annotations

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


if __name__ == "__main__":
    v2.fit_l1 = fit_l1_32bit
    v2.main()
