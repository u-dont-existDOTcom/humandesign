#!/usr/bin/env python3
"""Run the frozen 1,000-partner future-concordance null benchmark.

Specification: reference/research/partner_null_1000_freeze_v1.md

This is development/exploratory research, not a soulmate probability. Production
astronomy is verified SWIEPH and fails closed on Moshier fallback.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

import partner_future_pilot as west
import partner_hd_timing_pilot as hd

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
OUT = REPO / "reference" / "research" / "partner_null_1000_results_v1.json"
SEED = 202608252037
N = 1000
TROPICAL_YEAR = 365.2422
ASPECTS = (0, 60, 90, 120, 180)
DOMAINS = {
    "relationship": ("Moon", "Venus", "Mars"),
    "resources": ("Venus", "Jupiter", "Saturn"),
    "identity": ("Sun", "Saturn", "Uranus"),
    "purpose": ("Sun", "Mercury", "Mars", "Saturn"),
}
TRANSIT_ORBS = {
    "Jupiter": 2.5,
    "Saturn": 2.0,
    "Uranus": 1.5,
    "Neptune": 1.5,
    "Pluto": 1.5,
}
PROG_ORBS = {
    "Sun": 1.0,
    "Moon": 1.5,
    "Mercury": 1.0,
    "Venus": 1.0,
    "Mars": 1.0,
}
TRANSIT_WEIGHT = 0.60
PROGRESSION_WEIGHT = 1.00


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def months() -> list[datetime]:
    out = []
    for y in range(2026, 2041):
        for m in range(1, 13):
            out.append(datetime(y, m, 15, 12, 0, tzinfo=timezone.utc))
    return out


def random_births(start: datetime, end: datetime, n: int, rng: random.Random) -> list[datetime]:
    span = (end - start).total_seconds()
    return [start + __import__("datetime").timedelta(seconds=rng.random() * span) for _ in range(n)]


def kernel(residual_deg: float, sigma: float) -> float:
    return math.exp(-0.5 * (residual_deg / sigma) ** 2)


def natal_planets(dt: datetime) -> dict[str, float]:
    return {
        name: west.calc(west.jd(dt), body)[0]
        for name, body in west.NATAL_PLANETS.items()
        if name in {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus"}
    }


def precompute_transits(ds: list[datetime]) -> list[dict[str, float]]:
    return [
        {name: west.calc(west.jd(d), body)[0] for name, body in west.TRANSIT_PLANETS.items()}
        for d in ds
    ]


def progressed_positions(birth: datetime, ds: list[datetime]) -> list[dict[str, float]]:
    nj = west.jd(birth)
    rows = []
    for d in ds:
        age_years = (d - birth).total_seconds() / 86400.0 / TROPICAL_YEAR
        pj = nj + age_years
        rows.append({name: west.calc(pj, body)[0] for name, body in west.PROGRESSED_PLANETS.items()})
    return rows


def western_vector(
    birth: datetime,
    ds: list[datetime],
    transit_positions: list[dict[str, float]],
) -> list[float]:
    natal = natal_planets(birth)
    prog = progressed_positions(birth, ds)
    vec: list[float] = []
    for i, _d in enumerate(ds):
        for domain_targets in DOMAINS.values():
            targets = [natal[t] for t in domain_targets]
            for asp in ASPECTS:
                values = []
                for moving, mlon in transit_positions[i].items():
                    sigma = TRANSIT_ORBS[moving]
                    for tlon in targets:
                        resid = abs(west.aspect_residual(mlon, tlon, asp))
                        values.append(kernel(resid, sigma))
                vec.append(TRANSIT_WEIGHT * (sum(values) / len(values)))
            for asp in ASPECTS:
                values = []
                for moving, mlon in prog[i].items():
                    sigma = PROG_ORBS[moving]
                    for tlon in targets:
                        resid = abs(west.aspect_residual(mlon, tlon, asp))
                        values.append(kernel(resid, sigma))
                vec.append(PROGRESSION_WEIGHT * (sum(values) / len(values)))
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def precompute_hd_transits(ds: list[datetime]) -> list[set[int]]:
    out = []
    for d in ds:
        _by, gates = hd.transit_gate_state(d)
        out.append(gates)
    return out


def hd_metrics(a_gates: set[int], b_gates: set[int], transit_gates: list[set[int]]) -> dict[str, float]:
    single = eight = both = 0
    static = a_gates | b_gates
    for tg in transit_gates:
        fp = hd.fingerprint(static | tg)
        is_single = fp["definition_components"] == 1
        is_eight = fp["defined_center_count"] == 8
        single += int(is_single)
        eight += int(is_eight)
        both += int(is_single and is_eight)
    den = len(transit_gates)
    return {
        "single_definition_fraction": single / den,
        "eight_plus_one_fraction": eight / den,
        "single_and_eight_plus_one_fraction": both / den,
    }


def mean_sd(xs: list[float]) -> tuple[float, float]:
    m = statistics.fmean(xs)
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.0
    return m, sd


def z(x: float, m: float, sd: float) -> float:
    return 0.0 if sd == 0 else (x - m) / sd


def rank_desc(real: float, nulls: list[float]) -> tuple[int, float, int]:
    exceeding = sum(v > real + 1e-15 for v in nulls)
    rank = exceeding + 1
    percentile = 100.0 * (1.0 - exceeding / len(nulls))
    return rank, percentile, exceeding


def score_pool(
    focal_birth: datetime,
    real_partner_states: dict[str, datetime],
    null_births: list[datetime],
    ds: list[datetime],
    transits_w: list[dict[str, float]],
    transits_hd: list[set[int]],
) -> dict:
    focal_vec = western_vector(focal_birth, ds, transits_w)
    focal_gates = hd.natal_gates(focal_birth)

    null_w = []
    null_h = []
    for idx, dt in enumerate(null_births, 1):
        pv = western_vector(dt, ds, transits_w)
        pg = hd.natal_gates(dt)
        null_w.append(cosine(focal_vec, pv))
        null_h.append(hd_metrics(focal_gates, pg, transits_hd)["single_and_eight_plus_one_fraction"])
        if idx % 100 == 0:
            print(f"scored {idx}/{len(null_births)} null partners", flush=True)

    mw, sw = mean_sd(null_w)
    mh, sh = mean_sd(null_h)
    null_joint = [z(w, mw, sw) + z(h, mh, sh) for w, h in zip(null_w, null_h)]

    real = {}
    for label, dt in real_partner_states.items():
        pv = western_vector(dt, ds, transits_w)
        pg = hd.natal_gates(dt)
        rw = cosine(focal_vec, pv)
        hm = hd_metrics(focal_gates, pg, transits_hd)
        rh = hm["single_and_eight_plus_one_fraction"]
        rj = z(rw, mw, sw) + z(rh, mh, sh)
        wr, wp, we = rank_desc(rw, null_w)
        hr, hp, he = rank_desc(rh, null_h)
        jr, jp, je = rank_desc(rj, null_joint)
        real[label] = {
            "western_timing_similarity": rw,
            "western_rank": wr,
            "western_percentile": wp,
            "western_null_exceeding": we,
            **hm,
            "hd_primary_rank": hr,
            "hd_primary_percentile": hp,
            "hd_null_exceeding": he,
            "joint_z": rj,
            "joint_rank": jr,
            "joint_percentile": jp,
            "joint_null_exceeding": je,
        }

    return {
        "null_summary": {
            "western_mean": mw,
            "western_sd": sw,
            "hd_primary_mean": mh,
            "hd_primary_sd": sh,
            "joint_mean": statistics.fmean(null_joint),
            "joint_sd": statistics.stdev(null_joint),
        },
        "real_states": real,
        "null_top_joint": sorted(null_joint, reverse=True)[:10],
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

    ds = months()
    transits_w = precompute_transits(ds)
    transits_hd = precompute_hd_transits(ds)
    rng = random.Random(SEED)

    joel = datetime(1985, 1, 29, 10, 25, tzinfo=timezone.utc)
    bee = {
        "B_early": datetime(1989, 6, 19, 5, 0, tzinfo=timezone.utc),
        "B_mid": datetime(1989, 6, 19, 12, 0, tzinfo=timezone.utc),
        "B_late": datetime(1989, 6, 19, 17, 0, tzinfo=timezone.utc),
    }

    women = random_births(
        datetime(1984, 6, 19, tzinfo=timezone.utc),
        datetime(1994, 6, 19, tzinfo=timezone.utc),
        N,
        rng,
    )
    men = random_births(
        datetime(1980, 1, 29, tzinfo=timezone.utc),
        datetime(1990, 1, 29, tzinfo=timezone.utc),
        N,
        rng,
    )

    print("Joel -> 1000 women", flush=True)
    j_to_w = score_pool(joel, bee, women, ds, transits_w, transits_hd)

    print("Bee -> 1000 men", flush=True)
    b_to_m = {}
    for blabel, bdt in bee.items():
        print("focal", blabel, flush=True)
        rec = score_pool(bdt, {"Joel": joel}, men, ds, transits_w, transits_hd)
        b_to_m[blabel] = {
            "null_summary": rec["null_summary"],
            "Joel": rec["real_states"]["Joel"],
            "null_top_joint": rec["null_top_joint"],
        }

    data = {
        "status": "development_exploratory",
        "freeze_spec": "reference/research/partner_null_1000_freeze_v1.md",
        "seed": SEED,
        "n_per_direction": N,
        "months": [ds[0].isoformat(), ds[-1].isoformat()],
        "ephemeris": {
            "requested": "SWIEPH",
            "returned": "SWIEPH or abort",
            "sepl_18_sha256": sha256(EPHE / "sepl_18.se1"),
            "semo_18_sha256": sha256(EPHE / "semo_18.se1"),
        },
        "joel_to_random_women": j_to_w,
        "bee_to_random_men": b_to_m,
        "limitations": [
            "No houses, angles, progressed angles, or astrocartography are used in this null benchmark.",
            "The Western score is raw activation-timing similarity, not a calibrated life-outcome likelihood.",
            "The HD score is the predeclared joint single-definition + 8+1 fraction, not a validated compatibility probability.",
            "Bee is reported for all three representative unknown-time states; no state is selected from fit.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", OUT, "sha256", sha256(OUT), flush=True)
    print(json.dumps({
        "joel_to_women": j_to_w["real_states"],
        "bee_to_men": {k: v["Joel"] for k, v in b_to_m.items()},
    }, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
