#!/usr/bin/env python3
"""Run frozen multidomain 1,000-partner null benchmark V2.

Specification: reference/research/partner_multidomain_1000_freeze_v2.md

Development/exploratory only. Verified SWIEPH; any Moshier fallback aborts.
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

import partner_future_pilot as west
import partner_hd_timing_pilot as hd

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
FREEZE = REPO / "reference" / "research" / "partner_multidomain_1000_freeze_v2.md"
OUT = REPO / "reference" / "research" / "partner_multidomain_1000_results_v2.json"
SEED = 202608252052
N = 1000
TROPICAL_YEAR = 365.2422
MONTHS = [datetime(y, m, 15, 12, 0, tzinfo=timezone.utc) for y in range(2026, 2041) for m in range(1, 13)]
ASPECTS = (0, 60, 90, 120, 180)

DOMAIN_TARGETS = {
    "relationship": ("Moon", "Venus", "Mars"),
    "economy": ("Venus", "Jupiter", "Saturn", "Sun"),
    "home_community": ("Moon", "Venus", "Jupiter", "Saturn"),
    "work_purpose": ("Sun", "Mercury", "Mars", "Jupiter", "Saturn"),
}
PROG_BY_DOMAIN = {
    "relationship": ("Moon", "Venus", "Mars", "Sun"),
    "economy": ("Venus", "Mars", "Sun"),
    "home_community": ("Moon", "Venus", "Sun"),
    "work_purpose": ("Sun", "Mercury", "Mars"),
}
TRANSIT_SIGMA = {"Jupiter": 2.5, "Saturn": 2.0, "Uranus": 1.5, "Neptune": 1.5, "Pluto": 1.5}
PROG_SIGMA = {"Sun": 1.0, "Moon": 1.5, "Mercury": 1.0, "Venus": 1.0, "Mars": 1.0}
TRANSIT_FACTOR = 0.80
PROG_FACTOR = 1.00

# Frozen component weights by moving body and aspect.
SUPPORT_JUPITER = {0: 1.00, 60: 1.00, 90: 0.25, 120: 1.00, 180: 0.25}
STRUCTURE_SATURN = {0: 0.75, 60: 1.00, 120: 1.00}
CHANGE_OUTER = {
    "Uranus": {0: 1.00, 60: 0.60, 90: 0.90, 120: 0.60, 180: 0.90},
    "Neptune": {0: 0.90, 60: 0.55, 90: 0.80, 120: 0.55, 180: 0.80},
    "Pluto": {0: 1.00, 60: 0.60, 90: 0.90, 120: 0.60, 180: 0.90},
}
STRESS_OUTER = {
    "Saturn": {0: 0.35, 90: 1.00, 180: 1.00},
    "Uranus": {90: 0.90, 180: 0.90},
    "Neptune": {90: 0.80, 180: 0.80},
    "Pluto": {90: 0.90, 180: 0.90},
}
PROG_SUPPORT = {0: 0.75, 60: 0.75, 120: 0.75}
PROG_STRUCTURE = {0: 0.50, 60: 0.50, 120: 0.50}
PROG_CHANGE = {0: 0.75, 90: 0.60, 180: 0.60}
PROG_STRESS = {90: 0.50, 180: 0.50}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def random_births(start: datetime, end: datetime, n: int, rng: random.Random) -> list[datetime]:
    span = (end - start).total_seconds()
    return [start + timedelta(seconds=rng.random() * span) for _ in range(n)]


def kernel(residual: float, sigma: float) -> float:
    return math.exp(-0.5 * (residual / sigma) ** 2)


def natal_planets(dt: datetime) -> dict[str, float]:
    return {
        name: west.calc(west.jd(dt), body)[0]
        for name, body in west.NATAL_PLANETS.items()
        if name in {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus"}
    }


def precompute_transits() -> list[dict[str, float]]:
    return [
        {name: west.calc(west.jd(d), body)[0] for name, body in west.TRANSIT_PLANETS.items()}
        for d in MONTHS
    ]


def progressed_positions(birth: datetime) -> list[dict[str, float]]:
    nj = west.jd(birth)
    out = []
    for d in MONTHS:
        age_years = (d - birth).total_seconds() / 86400.0 / TROPICAL_YEAR
        pj = nj + age_years
        out.append({name: west.calc(pj, body)[0] for name, body in west.PROGRESSED_PLANETS.items()})
    return out


def aspect_activation(moving_lon: float, target_lon: float, aspect: int, sigma: float) -> float:
    residual = abs(west.aspect_residual(moving_lon, target_lon, aspect))
    return kernel(residual, sigma)


def max_weighted_aspect(
    moving_lon: float,
    target_lons: list[float],
    sigma: float,
    weights: dict[int, float],
    factor: float,
) -> float:
    best = 0.0
    for tlon in target_lons:
        for asp, weight in weights.items():
            best = max(best, factor * weight * aspect_activation(moving_lon, tlon, asp, sigma))
    return best


def individual_states(birth: datetime, transits: list[dict[str, float]]) -> dict[str, list[list[float]]]:
    natal = natal_planets(birth)
    prog = progressed_positions(birth)
    domains: dict[str, list[list[float]]] = {d: [] for d in DOMAIN_TARGETS}

    for i in range(len(MONTHS)):
        for domain, targets_names in DOMAIN_TARGETS.items():
            targets = [natal[n] for n in targets_names]
            support = max_weighted_aspect(
                transits[i]["Jupiter"], targets, TRANSIT_SIGMA["Jupiter"], SUPPORT_JUPITER, TRANSIT_FACTOR
            )
            structure = max_weighted_aspect(
                transits[i]["Saturn"], targets, TRANSIT_SIGMA["Saturn"], STRUCTURE_SATURN, TRANSIT_FACTOR
            )
            change = 0.0
            stress = 0.0
            for moving in ("Uranus", "Neptune", "Pluto"):
                change = max(
                    change,
                    max_weighted_aspect(
                        transits[i][moving], targets, TRANSIT_SIGMA[moving], CHANGE_OUTER[moving], TRANSIT_FACTOR
                    ),
                )
            for moving in ("Saturn", "Uranus", "Neptune", "Pluto"):
                stress = max(
                    stress,
                    max_weighted_aspect(
                        transits[i][moving], targets, TRANSIT_SIGMA[moving], STRESS_OUTER[moving], TRANSIT_FACTOR
                    ),
                )

            for p_name in PROG_BY_DOMAIN[domain]:
                p_lon = prog[i][p_name]
                sigma = PROG_SIGMA[p_name]
                support = max(
                    support,
                    max_weighted_aspect(p_lon, targets, sigma, PROG_SUPPORT, PROG_FACTOR),
                )
                structure = max(
                    structure,
                    max_weighted_aspect(p_lon, targets, sigma, PROG_STRUCTURE, PROG_FACTOR),
                )
                change = max(
                    change,
                    max_weighted_aspect(p_lon, targets, sigma, PROG_CHANGE, PROG_FACTOR),
                )
                stress = max(
                    stress,
                    max_weighted_aspect(p_lon, targets, sigma, PROG_STRESS, PROG_FACTOR),
                )
            domains[domain].append([support, structure, change, stress])
    return domains


def flatten(rows: list[list[float]]) -> list[float]:
    return [x for row in rows for x in row]


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def domain_similarity(a: dict[str, list[list[float]]], b: dict[str, list[list[float]]]) -> dict[str, float]:
    return {domain: cosine(flatten(a[domain]), flatten(b[domain])) for domain in DOMAIN_TARGETS}


def categorical_flags(states: dict[str, list[list[float]]]) -> dict[str, list[bool]]:
    rel = []
    econ = []
    home = []
    work = []
    for support, structure, change, stress in states["relationship"]:
        rel.append(support >= 0.40 and structure >= 0.30 and stress < 0.60)
    for support, structure, change, stress in states["economy"]:
        econ.append(change >= 0.50 and support >= 0.25 and stress < 0.75)
    for support, structure, change, stress in states["home_community"]:
        home.append(support >= 0.40 and structure >= 0.25 and stress < 0.60)
    for support, structure, change, stress in states["work_purpose"]:
        work.append(change >= 0.50)
    return {
        "relationship_stable_candidate": rel,
        "economic_independence_candidate": econ,
        "home_community_settlement_candidate": home,
        "work_purpose_reorientation_candidate": work,
    }


def categorical_overlap(a: dict[str, list[list[float]]], b: dict[str, list[list[float]]]) -> dict[str, dict[str, float]]:
    fa = categorical_flags(a)
    fb = categorical_flags(b)
    out = {}
    den = len(MONTHS)
    for k in fa:
        aa = sum(fa[k]) / den
        bb = sum(fb[k]) / den
        both = sum(x and y for x, y in zip(fa[k], fb[k])) / den
        union = sum(x or y for x, y in zip(fa[k], fb[k])) / den
        jacc = 0.0 if union == 0 else both / union
        out[k] = {
            "person_a_fraction": aa,
            "person_b_fraction": bb,
            "overlap_fraction": both,
            "jaccard": jacc,
        }
    return out


def precompute_hd_transits() -> list[set[int]]:
    return [hd.transit_gate_state(d)[1] for d in MONTHS]


def hd_pair_score(a_gates: set[int], b_gates: set[int], transits_hd: list[set[int]]) -> tuple[float, dict[str, float]]:
    single = eight = bridge = 0
    static = a_gates | b_gates
    for tg in transits_hd:
        fp = hd.fingerprint(static | tg)
        channels = set(fp["channels"])
        single += int(fp["definition_components"] == 1)
        eight += int(fp["defined_center_count"] == 8)
        bridge += int("21-45" in channels)
    den = len(transits_hd)
    components = {
        "single_definition_fraction": single / den,
        "eight_plus_one_fraction": eight / den,
        "material_bridge_21_45_fraction": bridge / den,
    }
    return statistics.fmean(components.values()), components


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


def score_pool(
    focal_birth: datetime,
    real_partner_states: dict[str, datetime],
    null_births: list[datetime],
    transits: list[dict[str, float]],
    transits_hd: list[set[int]],
) -> dict:
    focal_states = individual_states(focal_birth, transits)
    focal_gates = hd.natal_gates(focal_birth)

    null_domain: dict[str, list[float]] = {d: [] for d in DOMAIN_TARGETS}
    null_hd: list[float] = []

    for idx, dt in enumerate(null_births, 1):
        p_states = individual_states(dt, transits)
        sims = domain_similarity(focal_states, p_states)
        for d, v in sims.items():
            null_domain[d].append(v)
        p_gates = hd.natal_gates(dt)
        hscore, _ = hd_pair_score(focal_gates, p_gates, transits_hd)
        null_hd.append(hscore)
        if idx % 100 == 0:
            print(f"scored {idx}/{len(null_births)} null partners", flush=True)

    stats = {d: mean_sd(xs) for d, xs in null_domain.items()}
    hd_stats = mean_sd(null_hd)
    null_joint = []
    for i in range(len(null_births)):
        zs = [z(null_domain[d][i], *stats[d]) for d in DOMAIN_TARGETS]
        zs.append(z(null_hd[i], *hd_stats))
        null_joint.append(statistics.fmean(zs))

    real: dict[str, dict] = {}
    for label, dt in real_partner_states.items():
        p_states = individual_states(dt, transits)
        sims = domain_similarity(focal_states, p_states)
        p_gates = hd.natal_gates(dt)
        hscore, hcomp = hd_pair_score(focal_gates, p_gates, transits_hd)
        zs = [z(sims[d], *stats[d]) for d in DOMAIN_TARGETS]
        zs.append(z(hscore, *hd_stats))
        joint = statistics.fmean(zs)
        real[label] = {
            "domain_similarity": sims,
            "domain_ranks": {d: rank_desc(sims[d], null_domain[d]) for d in DOMAIN_TARGETS},
            "western_multidomain_mean": statistics.fmean(sims.values()),
            "hd_pair_score": hscore,
            "hd_components": hcomp,
            "hd_rank": rank_desc(hscore, null_hd),
            "joint_v2": joint,
            "joint_rank": rank_desc(joint, null_joint),
            "categorical_diagnostics": categorical_overlap(focal_states, p_states),
        }

    return {
        "null_summary": {
            "domains": {d: {"mean": stats[d][0], "sd": stats[d][1]} for d in DOMAIN_TARGETS},
            "hd_pair_score": {"mean": hd_stats[0], "sd": hd_stats[1]},
            "joint_v2": {"mean": statistics.fmean(null_joint), "sd": statistics.stdev(null_joint)},
            "top_joint_v2": sorted(null_joint, reverse=True)[:10],
        },
        "real_states": real,
    }


def main() -> None:
    for p in (EPHE / "sepl_18.se1", EPHE / "semo_18.se1"):
        if not p.is_file():
            raise SystemExit("Missing Swiss ephemeris file: " + str(p))
    swe.set_ephe_path(str(EPHE))

    # Fail-closed probes across natal and forecast span.
    for d in (
        datetime(1980, 1, 1, tzinfo=timezone.utc),
        datetime(1989, 6, 19, 12, tzinfo=timezone.utc),
        datetime(2033, 1, 1, tzinfo=timezone.utc),
        datetime(2040, 12, 15, tzinfo=timezone.utc),
    ):
        for body in west.NATAL_PLANETS.values():
            west.calc(west.jd(d), body)

    transits = precompute_transits()
    transits_hd = precompute_hd_transits()
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

    print("Joel -> 1000 age-matched comparison partners", flush=True)
    j_to_w = score_pool(joel, bee, women, transits, transits_hd)

    print("Bee -> 1000 age-matched comparison partners", flush=True)
    b_to_m = {}
    for blabel, bdt in bee.items():
        print("focal", blabel, flush=True)
        rec = score_pool(bdt, {"Joel": joel}, men, transits, transits_hd)
        b_to_m[blabel] = {
            "null_summary": rec["null_summary"],
            "Joel": rec["real_states"]["Joel"],
        }

    data = {
        "status": "development_exploratory",
        "model": "partner-multidomain-1000-v2",
        "freeze_spec": str(FREEZE.relative_to(REPO)),
        "freeze_sha256": sha256(FREEZE),
        "seed": SEED,
        "n_per_direction": N,
        "months": [MONTHS[0].isoformat(), MONTHS[-1].isoformat()],
        "domains": list(DOMAIN_TARGETS),
        "ephemeris": {
            "requested": "SWIEPH",
            "returned": "SWIEPH or abort",
            "sepl_18_sha256": sha256(EPHE / "sepl_18.se1"),
            "semo_18_sha256": sha256(EPHE / "semo_18.se1"),
        },
        "joel_to_random_partners": j_to_w,
        "bee_to_random_partners": b_to_m,
        "limitations": [
            "No geography score: Bee's exact time and exact Cameroon birthplace remain unresolved.",
            "No houses, angles, progressed angles, relocation charts, or astrocartography in V2 null ranking.",
            "Domain state vectors are frozen symbolic rubric features, not calibrated outcome probabilities.",
            "Economic-independence and community labels are exploratory diagnostics only and do not affect ranking.",
            "Bee remains three representative time states; no state is selected from fit.",
            "2030-2032 was known before this model; V2 is development evidence, not blind confirmation.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", OUT, "sha256", sha256(OUT), flush=True)
    print(json.dumps({
        "joel_to_partners": j_to_w["real_states"],
        "bee_to_partners": {k: v["Joel"] for k, v in b_to_m.items()},
    }, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
