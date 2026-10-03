#!/usr/bin/env python3
"""Reproduce the 2026-10-03 murderer birth-pattern pilot.

Input: paired_cohort.csv next to this script.
Output: printed metrics. This is exploratory research, not an individual-risk tool.
"""
from __future__ import annotations

import calendar
import math
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import swisseph as swe
from dateutil import parser
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, log_loss, roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 20261003
MASTERS = {11, 22, 33}
PLANETS = [swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]
PNAMES = ["sun", "mercury", "venus", "mars", "jupiter", "saturn"]


def reduce_num(n: int, preserve_master: bool = True) -> int:
    n = int(n)
    while n > 9 and not (preserve_master and n in MASTERS):
        n = sum(map(int, str(n)))
    return n


def numerology(d: date) -> dict[str, float]:
    m = reduce_num(d.month)
    day = reduce_num(d.day)
    yr = reduce_num(sum(map(int, str(d.year))))
    lp = reduce_num(m + day + yr)
    att = reduce_num(d.month + d.day)
    return {
        "lp": lp,
        "day": day,
        "att": att,
        "month": d.month,
        "yearroot": yr,
        "lp_master": int(lp in MASTERS),
        "day_master": int(day in MASTERS),
        "att_master": int(att in MASTERS),
        "digit_sum": sum(map(int, f"{d.year:04d}{d.month:02d}{d.day:02d}")),
    }


def longitude(d: date, planet: int) -> float:
    jd = swe.julday(d.year, d.month, d.day, 12.0)
    return float(swe.calc_ut(jd, planet)[0][0] % 360.0)


def astrology(d: date) -> dict[str, float]:
    out: dict[str, float] = {}
    signs: list[int] = []
    for p, name in zip(PLANETS, PNAMES):
        lon = longitude(d, p)
        rad = math.radians(lon)
        out[f"{name}_sin"] = math.sin(rad)
        out[f"{name}_cos"] = math.cos(rad)
        signs.append(int(lon // 30))
    out["mutable_count"] = sum(sign % 3 == 2 for sign in signs)
    for k in range(3):
        out[f"modality_{k}_count"] = sum(sign % 3 == k for sign in signs)
    for k in range(4):
        out[f"element_{k}_count"] = sum(sign % 4 == k for sign in signs)
    return out


def calendar_features(d: date) -> dict[str, float]:
    theta = 2.0 * math.pi * (d.timetuple().tm_yday - 1) / 365.2425
    return {
        "doy_sin": math.sin(theta),
        "doy_cos": math.cos(theta),
        "year": d.year,
        "year2": ((d.year - 1960) ** 2) / 100.0,
    }


def features(d: date, family: str) -> dict[str, float]:
    out: dict[str, float] = {}
    if family == "calendar":
        out.update(calendar_features(d))
    if family in {"numerology", "combined"}:
        nf = numerology(d)
        for key in ["lp", "day", "att", "month", "yearroot"]:
            value = nf[key]
            values = range(1, 13) if key == "month" else [*range(1, 10), 11, 22, 33]
            for v in values:
                out[f"{key}_{v}"] = int(value == v)
        for key in ["lp_master", "day_master", "att_master", "digit_sum"]:
            out[key] = nf[key]
    if family in {"astrology", "combined"}:
        out.update(astrology(d))
    return out


def matrix(rows: list[dict], family: str):
    dicts = [features(row["date"], family) for row in rows]
    cols = sorted({key for d in dicts for key in d})
    x = np.array([[d.get(col, 0.0) for col in cols] for d in dicts], dtype=float)
    y = np.array([row["y"] for row in rows], dtype=int)
    groups = np.array([row["pair"] for row in rows])
    return x, y, groups


def grouped_cv(rows: list[dict], family: str) -> dict[str, float]:
    x, y, groups = matrix(rows, family)
    pred = np.zeros(len(y))
    cv = GroupKFold(n_splits=5)
    for train, test in cv.split(x, y, groups):
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(C=0.25, max_iter=3000, solver="liblinear"),
        )
        model.fit(x[train], y[train])
        pred[test] = model.predict_proba(x[test])[:, 1]
    return {
        "auc": float(roc_auc_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred >= 0.5)),
        "log_loss": float(log_loss(y, pred)),
    }


def parse_date(value: str) -> date:
    return parser.parse(str(value)).date()


def rows_from_pairs(df: pd.DataFrame, max_year_gap: int | None = None) -> list[dict]:
    rows: list[dict] = []
    for _, r in df.iterrows():
        od = parse_date(r["offender_dob"])
        cd = parse_date(r["control_dob"])
        if max_year_gap is not None and abs(od.year - cd.year) > max_year_gap:
            continue
        pair = int(r["pair_id"])
        rows.extend(
            [
                {"pair": pair, "date": od, "y": 1},
                {"pair": pair, "date": cd, "y": 0},
            ]
        )
    return rows


def random_same_year(d: date, rng: np.random.Generator) -> date:
    ndays = 366 if calendar.isleap(d.year) else 365
    return date(d.year, 1, 1) + timedelta(days=int(rng.integers(0, ndays)))


def same_year_auc_distribution(df: pd.DataFrame, family: str, draws: int = 100) -> np.ndarray:
    offender_dates = [parse_date(x) for x in df["offender_dob"]]
    vals = []
    for j in range(draws):
        rng = np.random.default_rng(SEED + j)
        rows = []
        for pair, od in enumerate(offender_dates):
            rows.extend(
                [
                    {"pair": pair, "date": od, "y": 1},
                    {"pair": pair, "date": random_same_year(od, rng), "y": 0},
                ]
            )
        vals.append(grouped_cv(rows, family)["auc"])
    return np.asarray(vals)


def main() -> None:
    path = Path(__file__).with_name("paired_cohort.csv")
    df = pd.read_csv(path)
    print(f"pairs={len(df)}")

    print("\nNobel high-achievement proxy, year gap <= 5")
    matched = rows_from_pairs(df, max_year_gap=5)
    print(f"pairs={len(matched)//2}")
    for family in ["calendar", "numerology", "astrology", "combined"]:
        print(family, grouped_cv(matched, family))

    print("\nSame-year random-date control, 100 redraws")
    for family in ["calendar", "numerology", "astrology", "combined"]:
        aucs = same_year_auc_distribution(df, family, draws=100)
        print(
            family,
            {
                "mean_auc": float(aucs.mean()),
                "median_auc": float(np.median(aucs)),
                "q025": float(np.quantile(aucs, 0.025)),
                "q975": float(np.quantile(aucs, 0.975)),
            },
        )

    offender_dates = [parse_date(x) for x in df["offender_dob"]]
    print("\nObserved Life Path counts")
    print(dict(sorted(Counter(numerology(d)["lp"] for d in offender_dates).items())))


if __name__ == "__main__":
    main()
