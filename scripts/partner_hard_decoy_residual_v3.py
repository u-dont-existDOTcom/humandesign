#!/usr/bin/env python3
"""Frozen hard-decoy pair-specific residual benchmark V3.

Specification: reference/research/partner_hard_decoy_residual_freeze_v3.md

Development/exploratory only. Verified SWIEPH; any Moshier fallback aborts.
This predicts pair-transition activation, not relationship quality.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

import swisseph as swe

import partner_multidomain_1000_v2 as v2
import partner_future_pilot as west
import partner_hd_timing_pilot as hd

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
FREEZE = REPO / "reference" / "research" / "partner_hard_decoy_residual_freeze_v3.md"
OUT = REPO / "reference" / "research" / "partner_hard_decoy_residual_results_v3.json"

SEED = 202608260043
POOL_N = 5000
HARD_N = 1000
MONTHS = v2.MONTHS
ASPECTS = (0, 60, 90, 120, 180)
PERSONAL = ("Sun", "Moon", "Venus", "Mars")
NATAL_TARGETS = ("Sun", "Moon", "Venus", "Mars", "Saturn")
SIGMA = {"Sun": 1.0, "Moon": 1.5, "Venus": 1.0, "Mars": 1.0}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def random_births(start: datetime, end: datetime, n: int, rng: random.Random) -> list[datetime]:
    span = (end - start).total_seconds()
    return [start + timedelta(seconds=rng.random() * span) for _ in range(n)]


def mean_sd(xs: list[float]) -> tuple[float, float]:
    return statistics.fmean(xs), statistics.stdev(xs) if len(xs) > 1 else 0.0


def z(x: float, m: float, sd: float) -> float:
    return 0.0 if sd == 0 else (x - m) / sd


def rank_desc(real: float, nulls: list[float]) -> dict[str, float | int]:
    exceeding = sum(v > real + 1e-15 for v in nulls)
    return {
        "rank": exceeding + 1,
        "percentile": 100.0 * (1.0 - exceeding / len(nulls)),
        "null_exceeding": exceeding,
    }


def hard_match_score(target_states: dict, candidate_states: dict) -> float:
    sims = v2.domain_similarity(target_states, candidate_states)
    return statistics.fmean(sims.values())


def build_hard_sets(
    pool: list[datetime],
    targets: dict[str, dict],
    transits: list[dict[str, float]],
    label: str,
) -> dict[str, list[tuple[float, datetime]]]:
    scored: dict[str, list[tuple[float, datetime]]] = {k: [] for k in targets}
    for idx, birth in enumerate(pool, 1):
        states = v2.individual_states(birth, transits)
        for target_label, target_states in targets.items():
            scored[target_label].append((hard_match_score(target_states, states), birth))
        if idx % 100 == 0:
            print(f"{label}: hard-match pool {idx}/{len(pool)}", flush=True)
    out = {}
    for target_label, rows in scored.items():
        rows.sort(key=lambda x: x[0], reverse=True)
        out[target_label] = rows[:HARD_N]
    return out


def natal_relationship_positions(birth: datetime) -> dict[str, float]:
    x = west.jd(birth)
    body_map = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Saturn": swe.SATURN,
    }
    return {name: west.calc(x, body)[0] for name, body in body_map.items()}


def subject_data(birth: datetime) -> dict:
    return {
        "birth": birth,
        "natal": natal_relationship_positions(birth),
        "progressed": v2.progressed_positions(birth),
        "gates": hd.natal_gates(birth),
    }


def family_p_to_n(prog: dict[str, float], natal: dict[str, float]) -> float:
    best = 0.0
    for moving in PERSONAL:
        mlon = prog[moving]
        sigma = SIGMA[moving]
        for target in NATAL_TARGETS:
            tlon = natal[target]
            for asp in ASPECTS:
                best = max(best, v2.aspect_activation(mlon, tlon, asp, sigma))
    return best


def family_p_to_p(prog_a: dict[str, float], prog_b: dict[str, float]) -> float:
    best = 0.0
    for moving in PERSONAL:
        mlon = prog_a[moving]
        sigma = SIGMA[moving]
        for target in PERSONAL:
            tlon = prog_b[target]
            for asp in ASPECTS:
                best = max(best, v2.aspect_activation(mlon, tlon, asp, sigma))
    return best


def rolling_peak(series: list[float], width: int) -> tuple[float, int]:
    if len(series) < width:
        raise ValueError("series shorter than rolling window")
    s = sum(series[:width])
    best = s / width
    best_i = 0
    for i in range(width, len(series)):
        s += series[i] - series[i - width]
        value = s / width
        if value > best:
            best = value
            best_i = i - width + 1
    return best, best_i


def temporal_score(series: list[float]) -> dict:
    p12, i12 = rolling_peak(series, 12)
    p24, i24 = rolling_peak(series, 24)
    return {
        "score": 0.60 * p12 + 0.40 * p24,
        "peak12": p12,
        "peak12_start": MONTHS[i12].isoformat(),
        "peak12_end": MONTHS[i12 + 11].isoformat(),
        "peak24": p24,
        "peak24_start": MONTHS[i24].isoformat(),
        "peak24_end": MONTHS[i24 + 23].isoformat(),
    }


def western_pair_dynamic(a: dict, b: dict) -> dict:
    monthly = []
    family_sums = {"pA_to_nB": 0.0, "pB_to_nA": 0.0, "pA_to_pB": 0.0}
    for i in range(len(MONTHS)):
        ab = family_p_to_n(a["progressed"][i], b["natal"])
        ba = family_p_to_n(b["progressed"][i], a["natal"])
        pp = family_p_to_p(a["progressed"][i], b["progressed"][i])
        family_sums["pA_to_nB"] += ab
        family_sums["pB_to_nA"] += ba
        family_sums["pA_to_pB"] += pp
        monthly.append(statistics.fmean((ab, ba, pp)))
    out = temporal_score(monthly)
    out["family_15y_means"] = {k: v / len(MONTHS) for k, v in family_sums.items()}
    return out


def hd_pair_dynamic(a: dict, b: dict, transits_hd: list[set[int]]) -> dict:
    static = a["gates"] | b["gates"]
    monthly = []
    for tg in transits_hd:
        fp = hd.fingerprint(static | tg)
        single = 1.0 if fp["definition_components"] == 1 else 0.0
        eight = 1.0 if fp["defined_center_count"] == 8 else 0.0
        monthly.append(0.5 * single + 0.5 * eight)
    return temporal_score(monthly)


def pair_scores(a: dict, b: dict, transits_hd: list[set[int]]) -> dict:
    w = western_pair_dynamic(a, b)
    h = hd_pair_dynamic(a, b, transits_hd)
    return {
        "western": w,
        "hd": h,
    }


def score_against_hard_decoys(
    focal_data: dict,
    real_partner_data: dict,
    hard_rows: list[tuple[float, datetime]],
    transits_hd: list[set[int]],
    cache: dict[str, dict],
    label: str,
) -> dict:
    real = pair_scores(focal_data, real_partner_data, transits_hd)
    null_w: list[float] = []
    null_h: list[float] = []
    for idx, (match_score, birth) in enumerate(hard_rows, 1):
        key = birth.isoformat()
        pdata = cache.get(key)
        if pdata is None:
            pdata = subject_data(birth)
            cache[key] = pdata
        s = pair_scores(focal_data, pdata, transits_hd)
        null_w.append(float(s["western"]["score"]))
        null_h.append(float(s["hd"]["score"]))
        if idx % 100 == 0:
            print(f"{label}: pair score {idx}/{len(hard_rows)}", flush=True)

    mw, sw = mean_sd(null_w)
    mh, sh = mean_sd(null_h)
    null_joint = [statistics.fmean((z(w, mw, sw), z(h, mh, sh))) for w, h in zip(null_w, null_h)]

    rw = float(real["western"]["score"])
    rh = float(real["hd"]["score"])
    rj = statistics.fmean((z(rw, mw, sw), z(rh, mh, sh)))

    hard_match_values = [m for m, _ in hard_rows]
    return {
        "real": {
            "western": real["western"],
            "hd": real["hd"],
            "western_rank": rank_desc(rw, null_w),
            "hd_rank": rank_desc(rh, null_h),
            "joint_residual_v3": rj,
            "joint_rank": rank_desc(rj, null_joint),
        },
        "hard_decoy_match": {
            "n": len(hard_rows),
            "min": min(hard_match_values),
            "mean": statistics.fmean(hard_match_values),
            "max": max(hard_match_values),
        },
        "null_summary": {
            "western_mean": mw,
            "western_sd": sw,
            "hd_mean": mh,
            "hd_sd": sh,
            "joint_mean": statistics.fmean(null_joint),
            "joint_sd": statistics.stdev(null_joint),
            "top10_joint": sorted(null_joint, reverse=True)[:10],
        },
    }


def main() -> None:
    for p in (EPHE / "sepl_18.se1", EPHE / "semo_18.se1"):
        if not p.is_file():
            raise SystemExit("Missing Swiss ephemeris file: " + str(p))
    swe.set_ephe_path(str(EPHE))

    # Fail-closed probes.
    for d in (
        datetime(1980, 1, 1, tzinfo=timezone.utc),
        datetime(1989, 6, 19, 12, tzinfo=timezone.utc),
        datetime(2033, 1, 1, tzinfo=timezone.utc),
        datetime(2040, 12, 15, tzinfo=timezone.utc),
    ):
        for body in west.NATAL_PLANETS.values():
            west.calc(west.jd(d), body)

    transits = v2.precompute_transits()
    transits_hd = v2.precompute_hd_transits()
    rng = random.Random(SEED)

    joel_birth = datetime(1985, 1, 29, 10, 25, tzinfo=timezone.utc)
    bee_births = {
        "B_early": datetime(1989, 6, 19, 5, 0, tzinfo=timezone.utc),
        "B_mid": datetime(1989, 6, 19, 12, 0, tzinfo=timezone.utc),
        "B_late": datetime(1989, 6, 19, 17, 0, tzinfo=timezone.utc),
    }

    joel_states = v2.individual_states(joel_birth, transits)
    bee_states = {k: v2.individual_states(dt, transits) for k, dt in bee_births.items()}

    women_pool = random_births(
        datetime(1984, 6, 19, tzinfo=timezone.utc),
        datetime(1994, 6, 19, tzinfo=timezone.utc),
        POOL_N,
        rng,
    )
    men_pool = random_births(
        datetime(1980, 1, 29, tzinfo=timezone.utc),
        datetime(1990, 1, 29, tzinfo=timezone.utc),
        POOL_N,
        rng,
    )

    print("Building A->B hard-decoy sets", flush=True)
    hard_women = build_hard_sets(women_pool, bee_states, transits, "women")
    print("Building B->A hard-decoy set", flush=True)
    hard_men = build_hard_sets(men_pool, {"Joel": joel_states}, transits, "men")["Joel"]

    joel_data = subject_data(joel_birth)
    bee_data = {k: subject_data(dt) for k, dt in bee_births.items()}
    subject_cache: dict[str, dict] = {joel_birth.isoformat(): joel_data}
    for k, dt in bee_births.items():
        subject_cache[dt.isoformat()] = bee_data[k]

    a_to_b = {}
    for blabel in bee_births:
        a_to_b[blabel] = score_against_hard_decoys(
            joel_data,
            bee_data[blabel],
            hard_women[blabel],
            transits_hd,
            subject_cache,
            f"A->{blabel}",
        )

    b_to_a = {}
    for blabel in bee_births:
        b_to_a[blabel] = score_against_hard_decoys(
            bee_data[blabel],
            joel_data,
            hard_men,
            transits_hd,
            subject_cache,
            f"{blabel}->A",
        )

    data = {
        "status": "development_exploratory",
        "model": "partner-hard-decoy-residual-v3",
        "research_target": "pair transition activation, not relationship quality",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "seed": SEED,
        "candidate_pool_per_direction": POOL_N,
        "hard_decoys_per_direction": HARD_N,
        "months": [MONTHS[0].isoformat(), MONTHS[-1].isoformat()],
        "ephemeris": {
            "requested": "SWIEPH",
            "returned": "SWIEPH or abort",
            "sepl_18_sha256": sha256(EPHE / "sepl_18.se1"),
            "semo_18_sha256": sha256(EPHE / "semo_18.se1"),
        },
        "joel_to_hard_matched_partners": a_to_b,
        "bee_to_hard_matched_partners": b_to_a,
        "limitations": [
            "Bee exact birth time remains unknown; all three representative states are reported.",
            "Static synastry is excluded from the primary score.",
            "The previously noticed 2030 window is not a blind timing discovery.",
            "The benchmark estimates symbolic pair-transition activation only; it says nothing about relationship quality.",
            "Hard decoys are synthetic age-matched birth moments, not documented real-world acquaintances/exposure sets.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", OUT, "sha256", sha256(OUT), flush=True)
    print(json.dumps({
        "A_to_B": {k: v["real"] for k, v in a_to_b.items()},
        "B_to_A": {k: v["real"] for k, v in b_to_a.items()},
    }, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
