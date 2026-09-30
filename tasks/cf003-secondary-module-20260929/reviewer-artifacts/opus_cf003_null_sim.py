#!/usr/bin/env python3
"""Calibration of the CF-003 global label-permutation null under chart/behaviour INDEPENDENCE.

Predictor: the repository's published seven-weight surface, fed by a crude random chart-flag
model in which ascendant sign is uniform and modern rulerships are used (so Venus and Mercury
each rule two signs). Behaviour: drawn independently of the predictor, with construct-specific
0..4 rating distributions. Any rejection is therefore a false positive.

Compares the repository's global construct-label permutation p-value with an across-participant
reassignment (pairing) permutation p-value. Read-only; writes nothing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path("/mnt/hdd/var/tmp/humandesign-cf003-module-20260929")
sys.path.insert(0, str(ROOT / "src"))

from hdmatch.empirical_astrology import cf003_target as T  # noqa: E402
from hdmatch.empirical_astrology.cf003 import (  # noqa: E402
    CF003_CANDIDATE_BODIES,
    CF003FactorFlags,
    score_cf003_planet,
)

BODIES = list(CF003_CANDIDATE_BODIES)
IDX = {b: i for i, b in enumerate(BODIES)}
SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]
MODERN_RULER = {
    "aries": "mars", "taurus": "venus", "gemini": "mercury", "cancer": "moon",
    "leo": "sun", "virgo": "mercury", "libra": "venus", "scorpio": "pluto",
    "sagittarius": "jupiter", "capricorn": "saturn", "aquarius": "uranus", "pisces": "neptune",
}


def draw_predictor(rng: np.random.Generator) -> dict[str, float]:
    asc = int(rng.integers(12))
    desc = (asc + 6) % 12
    out = {}
    for b in BODIES:
        flags = CF003FactorFlags(
            major_aspect_to_moon=bool(b != "moon" and rng.random() < 0.35),
            five_or_more_major_aspects=bool(rng.random() < 0.25),
            modern_ascendant_ruler=MODERN_RULER[SIGNS[asc]] == b,
            placidus_house_12=bool(rng.random() < 1 / 12),
            modern_descendant_ruler=MODERN_RULER[SIGNS[desc]] == b,
            major_aspect_to_ascendant=bool(rng.random() < 0.35),
            within_5deg_placidus_house_9_center=bool(rng.random() < 0.03),
        )
        out[b] = score_cf003_planet(b, flags).total
    return out


HIGH = np.array([0.02, 0.08, 0.25, 0.40, 0.25])
MID = np.array([0.10, 0.25, 0.35, 0.22, 0.08])
LOW = np.array([0.30, 0.35, 0.25, 0.08, 0.02])

SCENARIOS = {
    "A_equal_construct_marginals": {},
    "B_T01_T07_high": {"T01": HIGH, "T07": HIGH},
    "C_T01_T05_T07_high_T10_low": {"T01": HIGH, "T05": HIGH, "T07": HIGH, "T10": LOW},
    "D_T03_high_only": {"T03": HIGH},
}


def draw_behavior(rng: np.random.Generator, profile: dict) -> dict[str, float]:
    return {
        planet: float(rng.choice(5, p=profile.get(cid, MID)))
        for cid, planet in T.CF003_CONSTRUCT_TO_PLANET.items()
    }


def dataset(rng, n, profile):
    pairs = [
        T.CF003CohortPair(f"p{i}", draw_predictor(rng), draw_behavior(rng, profile))
        for i in range(n)
    ]
    R = np.empty((n, 10))
    Wt = np.zeros((n, 10))
    for i, pair in enumerate(pairs):
        mids = T.midranks_descending(pair.behavioral_scores)
        R[i] = [mids[b] for b in BODIES]
        top = T.rank_score_groups(pair.predictor_scores)[0]
        for b in top:
            Wt[i, IDX[b]] = 1.0 / len(top)
    return pairs, R, Wt


def p_global(R, Wt, rng, K):
    n = R.shape[0]
    M = Wt.T @ R
    obs = np.trace(M) / n
    P = np.argsort(rng.random((K, 10)), axis=1)
    stats = M[np.arange(10), P].sum(axis=1) / n
    return (1 + np.sum(stats <= obs + 1e-12)) / (K + 1)


def p_across(R, Wt, rng, K):
    n = R.shape[0]
    A = Wt @ R.T
    obs = np.trace(A) / n
    S = np.argsort(rng.random((K, n)), axis=1)
    stats = A[np.arange(n), S].sum(axis=1) / n
    return (1 + np.sum(stats <= obs + 1e-12)) / (K + 1)


rng = np.random.default_rng(20260929)

print("=== sanity: vectorised statistic == repository functions ===")
pairs, R, Wt = dataset(rng, 25, SCENARIOS["C_T01_T05_T07_high_T10_low"])
repo_obs = T.cohort_primary_statistic(pairs)
vec_obs = np.trace(Wt.T @ R) / 25
perms = [tuple(BODIES[j] for j in np.argsort(rng.random(10))) for _ in range(300)]
repo = T.permutation_test_from_global_label_maps(pairs, perms)
M = Wt.T @ R
vec_count = sum(1 for perm in perms if sum(M[l, IDX[perm[l]]] for l in range(10)) / 25 <= vec_obs + 1e-12)
print(f"observed repo={repo_obs!r} vec={vec_obs!r}; <=count repo={repo.equal_or_better_count} vec={vec_count}")

print("\n=== predictor top-set share per body (n=20000, independent draws) ===")
_, R_big, Wt_big = dataset(rng, 20000, {})
q = Wt_big.mean(axis=0)
print("  " + "  ".join(f"{b}={q[IDX[b]]:.3f}" for b in BODIES))
print("  share of charts whose predictor top set has >1 body:", float(np.mean((Wt_big > 0).sum(axis=1) > 1)))

for name in ("B_T01_T07_high", "C_T01_T05_T07_high_T10_low"):
    _, Rb, _ = dataset(rng, 20000, SCENARIOS[name])
    mu = Rb.mean(axis=0)
    print(f"  mean behavioural midrank per body under {name}: " + "  ".join(f"{b}={mu[IDX[b]]:.2f}" for b in BODIES))

print("\n=== type-I error at alpha=0.05 (400 datasets each, 999 permutations) ===")
K = 999
REPS = 400
for name, profile in SCENARIOS.items():
    ns = (30, 60, 120) if name != "D_T03_high_only" else (120,)
    for n in ns:
        pg, pa = [], []
        for _ in range(REPS):
            _, R, Wt = dataset(rng, n, profile)
            pg.append(p_global(R, Wt, rng, K))
            pa.append(p_across(R, Wt, rng, K))
        pg = np.array(pg)
        pa = np.array(pa)
        print(
            f"  {name:30s} n={n:4d} | global-label reject={np.mean(pg <= 0.05):.3f} "
            f"median p={np.median(pg):.3f} | across-participant reject={np.mean(pa <= 0.05):.3f} "
            f"median p={np.median(pa):.3f}"
        )

print("\n=== large-n behaviour (5 datasets, n=3000, 1999 permutations) ===")
for name in ("A_equal_construct_marginals", "B_T01_T07_high", "C_T01_T05_T07_high_T10_low", "D_T03_high_only"):
    gs, as_ = [], []
    for _ in range(5):
        _, R, Wt = dataset(rng, 3000, SCENARIOS[name])
        gs.append(round(float(p_global(R, Wt, rng, 1999)), 4))
        as_.append(round(float(p_across(R, Wt, rng, 1999)), 4))
    print(f"  {name:30s} global-label p={gs} | across-participant p={as_}")
