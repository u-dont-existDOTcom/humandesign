#!/usr/bin/env python3
"""Generate independent raw Western/HD timing inputs for a partner future-concordance pilot.

This is intentionally an event generator, not a relationship-story generator.
It calculates A and B independently first and writes raw events that can later be
compared under docs/19_partner_future_concordance.md.

Production astronomy is verified Swiss Ephemeris (.se1) and fails closed on
Moshier fallback.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import swisseph as swe

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
OUT = REPO / "reference" / "research" / "partner_future_joel_bee_2026_2040_raw.json"

FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
EPH_MASK = swe.FLG_JPLEPH | swe.FLG_SWIEPH | swe.FLG_MOSEPH
TROPICAL_YEAR = 365.2422
ASPECTS = (0, 60, 90, 120, 180)
TRANSIT_PLANETS = {
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}
NATAL_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "TrueNode": swe.TRUE_NODE,
}
PROGRESSED_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
}

START = datetime(2026, 1, 1, tzinfo=timezone.utc)
END = datetime(2041, 1, 1, tzinfo=timezone.utc)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def jd(dt: datetime) -> float:
    dt = dt.astimezone(timezone.utc)
    hour = dt.hour + dt.minute / 60 + dt.second / 3600 + dt.microsecond / 3.6e9
    return swe.julday(dt.year, dt.month, dt.day, hour, swe.GREG_CAL)


def dt_from_jd(x: float) -> datetime:
    y, m, d, hh = swe.revjul(x, swe.GREG_CAL)
    h = int(hh)
    mmf = (hh - h) * 60
    mi = int(mmf)
    ssf = (mmf - mi) * 60
    s = int(ssf)
    us = int(round((ssf - s) * 1e6))
    if us >= 1_000_000:
        s += 1
        us -= 1_000_000
    return datetime(y, m, d, h, mi, s, us, tzinfo=timezone.utc)


def calc(jd_ut: float, body: int) -> tuple[float, float]:
    xx, ret = swe.calc_ut(jd_ut, body, FLAGS)
    used = ret & EPH_MASK
    if used != swe.FLG_SWIEPH:
        raise RuntimeError(
            f"EPHEMERIS_FALLBACK body={body} jd={jd_ut} used={used} ret={ret}"
        )
    return xx[0] % 360.0, xx[3]


def wrap180(x: float) -> float:
    return (x + 180.0) % 360.0 - 180.0


def angle_distance(a: float, b: float) -> float:
    return abs(wrap180(a - b))


def aspect_residual(moving: float, natal: float, aspect: int) -> float:
    # For non-180 aspects, either +aspect or -aspect can be the exact geometry.
    if aspect == 0:
        return wrap180(moving - natal)
    if aspect == 180:
        return wrap180(moving - natal - 180.0)
    r1 = wrap180(moving - natal - aspect)
    r2 = wrap180(moving - natal + aspect)
    return r1 if abs(r1) <= abs(r2) else r2


def root_bisect(fn, a: float, b: float, fa: float, fb: float) -> float:
    for _ in range(60):
        if (b - a) * 86400 < 0.5:
            break
        m = (a + b) / 2
        fm = fn(m)
        if abs(fm) < 1e-10:
            return m
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2


def natal_snapshot(dt: datetime, lat: float | None, lon: float | None) -> dict:
    x = jd(dt)
    planets = {name: calc(x, body)[0] for name, body in NATAL_PLANETS.items()}
    out: dict[str, object] = {
        "utc": dt.astimezone(timezone.utc).isoformat(),
        "planets": planets,
    }
    if lat is not None and lon is not None:
        cusps, ascmc = swe.houses_ex(x, lat, lon, b"P", 0)
        out["asc"] = float(ascmc[0] % 360)
        out["mc"] = float(ascmc[1] % 360)
        out["houses"] = [float(v % 360) for v in cusps]
    return out


def transit_events(natal: dict, include_angles: bool) -> list[dict]:
    targets: dict[str, float] = {
        k: float(v)
        for k, v in natal["planets"].items()
        if k in {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus"}
    }
    if include_angles:
        targets["ASC"] = float(natal["asc"])
        targets["MC"] = float(natal["mc"])

    out: list[dict] = []
    start_jd, end_jd = jd(START), jd(END)
    step = 1.0
    for mp_name, mp_id in TRANSIT_PLANETS.items():
        for target_name, target_lon in targets.items():
            for asp in ASPECTS:
                def f(t: float) -> float:
                    return aspect_residual(calc(t, mp_id)[0], target_lon, asp)

                t0 = start_jd
                f0 = f(t0)
                while t0 < end_jd:
                    t1 = min(t0 + step, end_jd)
                    f1 = f(t1)
                    # Avoid wrap-discontinuity false roots. Slow planets cannot move 90 deg/day.
                    if f0 == 0 or (f0 * f1 < 0 and abs(f0 - f1) < 30):
                        r = t0 if f0 == 0 else root_bisect(f, t0, t1, f0, f1)
                        rdt = dt_from_jd(r)
                        if not out or not (
                            out[-1].get("moving") == mp_name
                            and out[-1].get("target") == target_name
                            and out[-1].get("aspect") == asp
                            and abs((rdt - datetime.fromisoformat(out[-1]["utc"])).total_seconds()) < 36 * 3600
                        ):
                            out.append({
                                "utc": rdt.isoformat(),
                                "moving": mp_name,
                                "aspect": asp,
                                "target": target_name,
                                "natal_target_lon": target_lon,
                            })
                    t0, f0 = t1, f1
    out.sort(key=lambda e: e["utc"])
    return out


def progressed_jd(natal_jd: float, birth_dt: datetime, target_dt: datetime) -> float:
    age_years = (target_dt - birth_dt).total_seconds() / 86400.0 / TROPICAL_YEAR
    return natal_jd + age_years


def progression_events(birth_dt: datetime, natal: dict, include_angles: bool) -> list[dict]:
    nj = jd(birth_dt)
    targets: dict[str, float] = {
        k: float(v)
        for k, v in natal["planets"].items()
        if k in {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"}
    }
    if include_angles:
        targets["ASC"] = float(natal["asc"])
        targets["MC"] = float(natal["mc"])

    def p_lon(calendar_jd: float, body: int) -> float:
        target_dt = dt_from_jd(calendar_jd)
        return calc(progressed_jd(nj, birth_dt, target_dt), body)[0]

    out: list[dict] = []
    sj, ej = jd(START), jd(END)
    step = 7.0
    for pp_name, pp_id in PROGRESSED_PLANETS.items():
        for target_name, target_lon in targets.items():
            for asp in ASPECTS:
                def f(t: float) -> float:
                    return aspect_residual(p_lon(t, pp_id), target_lon, asp)

                t0, f0 = sj, f(sj)
                while t0 < ej:
                    t1 = min(t0 + step, ej)
                    f1 = f(t1)
                    if f0 == 0 or (f0 * f1 < 0 and abs(f0 - f1) < 30):
                        r = t0 if f0 == 0 else root_bisect(f, t0, t1, f0, f1)
                        rdt = dt_from_jd(r)
                        if not out or not (
                            out[-1].get("moving") == f"p{pp_name}"
                            and out[-1].get("target") == target_name
                            and out[-1].get("aspect") == asp
                            and abs((rdt - datetime.fromisoformat(out[-1]["utc"])).total_seconds()) < 15 * 86400
                        ):
                            out.append({
                                "utc": rdt.isoformat(),
                                "moving": f"p{pp_name}",
                                "aspect": asp,
                                "target": target_name,
                                "natal_target_lon": target_lon,
                            })
                    t0, f0 = t1, f1
    out.sort(key=lambda e: e["utc"])
    return out


def half_year_progressed_snapshots(birth_dt: datetime, natal: dict) -> list[dict]:
    nj = jd(birth_dt)
    rows = []
    for year in range(2026, 2041):
        for month in (1, 7):
            d = datetime(year, month, 1, tzinfo=timezone.utc)
            pj = progressed_jd(nj, birth_dt, d)
            rows.append({
                "utc": d.isoformat(),
                "progressed_planets": {
                    n: calc(pj, b)[0] for n, b in PROGRESSED_PLANETS.items()
                },
            })
    return rows


def subject_record(
    label: str,
    birth_dt: datetime,
    lat: float | None,
    lon: float | None,
    exact_time: bool,
) -> dict:
    natal = natal_snapshot(birth_dt, lat if exact_time else None, lon if exact_time else None)
    return {
        "label": label,
        "birth_utc": birth_dt.astimezone(timezone.utc).isoformat(),
        "exact_birth_time": exact_time,
        "natal": natal,
        "transit_events": transit_events(natal, include_angles=exact_time),
        "progression_events": progression_events(birth_dt, natal, include_angles=exact_time),
        "progressed_snapshots": half_year_progressed_snapshots(birth_dt, natal),
    }


def main() -> None:
    required = (EPHE / "sepl_18.se1", EPHE / "semo_18.se1")
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise SystemExit("Missing Swiss ephemeris files: " + ", ".join(missing))
    swe.set_ephe_path(str(EPHE))

    # Fail-closed probes over natal and forecast span.
    for d in (
        datetime(1985, 1, 29, 10, 25, tzinfo=timezone.utc),
        datetime(1989, 6, 19, 12, tzinfo=timezone.utc),
        START,
        datetime(2033, 1, 1, tzinfo=timezone.utc),
        END - timedelta(days=1),
    ):
        for body in NATAL_PLANETS.values():
            calc(jd(d), body)

    # Known exact record.
    joel = subject_record(
        "A",
        datetime(1985, 1, 29, 10, 25, tzinfo=timezone.utc),
        39.9526,
        -75.1652,
        True,
    )

    # Bee: date + Cameroon are known, clock time is not. Carry representative
    # early/mid/late states independently; do not choose among them from pair fit.
    douala = ZoneInfo("Africa/Douala")
    bee_local_times = {
        "B_early": datetime(1989, 6, 19, 6, 0, tzinfo=douala),
        "B_mid": datetime(1989, 6, 19, 13, 0, tzinfo=douala),
        "B_late": datetime(1989, 6, 19, 18, 0, tzinfo=douala),
    }
    bee = {
        label: subject_record(label, local.astimezone(timezone.utc), None, None, False)
        for label, local in bee_local_times.items()
    }

    manifest = {
        "protocol": "partner-future-concordance-v1-exploratory",
        "status": "raw_independent_timeline_inputs_no_pair_scoring",
        "forecast_horizon": [START.isoformat(), END.isoformat()],
        "known_prior_suspected_window": "2030-2032 was discussed before this pilot; do not treat rediscovery as blind confirmation",
        "ephemeris": {
            "requested": "SWIEPH",
            "returned": "SWIEPH or run aborts",
            "sepl_18_sha256": sha256(EPHE / "sepl_18.se1"),
            "semo_18_sha256": sha256(EPHE / "semo_18.se1"),
        },
        "progression_convention": "secondary progression: one ephemeris day per tropical year of life (365.2422 d)",
        "aspects": list(ASPECTS),
        "person_A": joel,
        "person_B_time_states": bee,
        "limitations": [
            "Bee birth time unknown: no natal houses/angles/progressed angles/astrocartography are treated as robust.",
            "Three representative Bee times are for planetary robustness, not a completed exact-state time rectification.",
            "This file contains raw timing events; life-state interpretation and pair comparison must be frozen separately.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"sha256={sha256(OUT)}")
    print(f"A transit events={len(joel['transit_events'])} progressions={len(joel['progression_events'])}")
    for label, rec in bee.items():
        print(label, "transits", len(rec["transit_events"]), "progressions", len(rec["progression_events"]))


if __name__ == "__main__":
    main()
