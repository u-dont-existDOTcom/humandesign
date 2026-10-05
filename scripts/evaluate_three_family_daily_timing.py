#!/usr/bin/env python3
"""Evaluate the frozen three-family daily timing candidate on one natal chart.

Candidate rule (frozen from Hale development):
- exact major aspect by Jupiter/Saturn/Uranus/Neptune/Pluto to natal ASC or MC
  within 24h of the candidate civil day's local noon;
- any exact major secondary progression by pSun/pMoon/pMercury/pVenus/pMars
  to natal Sun..Saturn, ASC, or MC within 72h of local noon;
- exact major transiting-Moon aspect to natal ASC or MC within 24h;
- require all three families.

This script evaluates the rule unchanged. It does not infer an event type.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import swisseph as swe

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
}
PROGRESSED_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
}
PROGRESSION_TARGETS = {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"}
TROPICAL_YEAR = 365.2422
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
EPH_MASK = swe.FLG_JPLEPH | swe.FLG_SWIEPH | swe.FLG_MOSEPH


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("birth UTC must include an offset")
    return dt.astimezone(timezone.utc)


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
        raise RuntimeError(f"EPHEMERIS_FALLBACK body={body} jd={jd_ut} used={used} ret={ret}")
    return xx[0] % 360.0, xx[3]


def wrap180(x: float) -> float:
    return (x + 180.0) % 360.0 - 180.0


def aspect_residual(moving: float, natal: float, aspect: int) -> float:
    if aspect == 0:
        return wrap180(moving - natal)
    if aspect == 180:
        return wrap180(moving - natal - 180.0)
    r1 = wrap180(moving - natal - aspect)
    r2 = wrap180(moving - natal + aspect)
    return r1 if abs(r1) <= abs(r2) else r2


def root_bisect(fn, a: float, b: float, fa: float, fb: float) -> float:
    for _ in range(70):
        if (b - a) * 86400 < 0.25:
            break
        m = (a + b) / 2
        fm = fn(m)
        if abs(fm) < 1e-12:
            return m
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2


def natal_snapshot(birth_dt: datetime, lat: float, lon: float) -> dict:
    x = jd(birth_dt)
    planets = {name: calc(x, body)[0] for name, body in NATAL_PLANETS.items()}
    cusps, ascmc = swe.houses_ex(x, lat, lon, b"P", 0)
    return {
        "utc": birth_dt.isoformat(),
        "lat": lat,
        "lon": lon,
        "planets": planets,
        "asc": float(ascmc[0] % 360.0),
        "mc": float(ascmc[1] % 360.0),
        "houses": [float(v % 360.0) for v in cusps],
    }


def exact_events(movers: dict[str, int], targets: dict[str, float], start: datetime, end: datetime, step_days: float, lon_fn) -> list[dict]:
    out: list[dict] = []
    sj, ej = jd(start), jd(end)
    for moving_name, moving_id in movers.items():
        for target_name, target_lon in targets.items():
            for aspect in ASPECTS:
                def f(t: float) -> float:
                    return aspect_residual(lon_fn(t, moving_id), target_lon, aspect)
                t0, f0 = sj, f(sj)
                while t0 < ej:
                    t1 = min(t0 + step_days, ej)
                    f1 = f(t1)
                    if f0 == 0 or (f0 * f1 < 0 and abs(f0 - f1) < 30):
                        r = t0 if f0 == 0 else root_bisect(f, t0, t1, f0, f1)
                        rdt = dt_from_jd(r)
                        candidate = {
                            "utc": rdt.isoformat(),
                            "moving": moving_name,
                            "aspect": aspect,
                            "target": target_name,
                            "natal_target_lon": target_lon,
                        }
                        if not any(
                            old["moving"] == moving_name
                            and old["target"] == target_name
                            and old["aspect"] == aspect
                            and abs((rdt - datetime.fromisoformat(old["utc"])).total_seconds()) < max(3600, step_days * 86400 * 0.5)
                            for old in out
                        ):
                            out.append(candidate)
                    t0, f0 = t1, f1
    return sorted(out, key=lambda e: e["utc"])


def transit_events(natal: dict, start: datetime, end: datetime) -> list[dict]:
    targets = {"ASC": natal["asc"], "MC": natal["mc"]}
    return exact_events(
        TRANSIT_PLANETS,
        targets,
        start,
        end,
        1.0,
        lambda t, body: calc(t, body)[0],
    )


def progressed_jd(natal_jd: float, birth_dt: datetime, target_dt: datetime) -> float:
    age_years = (target_dt - birth_dt).total_seconds() / 86400.0 / TROPICAL_YEAR
    return natal_jd + age_years


def progression_events(birth_dt: datetime, natal: dict, start: datetime, end: datetime) -> list[dict]:
    natal_jd = jd(birth_dt)
    targets = {k: v for k, v in natal["planets"].items() if k in PROGRESSION_TARGETS}
    targets["ASC"] = natal["asc"]
    targets["MC"] = natal["mc"]

    def p_lon(calendar_jd: float, body: int) -> float:
        target_dt = dt_from_jd(calendar_jd)
        return calc(progressed_jd(natal_jd, birth_dt, target_dt), body)[0]

    movers = {f"p{k}": v for k, v in PROGRESSED_PLANETS.items()}
    return exact_events(movers, targets, start, end, 7.0, p_lon)


def lunar_angle_events(natal: dict, start: datetime, end: datetime) -> list[dict]:
    targets = {"ASC": natal["asc"], "MC": natal["mc"]}
    return exact_events(
        {"Moon": swe.MOON},
        targets,
        start,
        end,
        0.05,
        lambda t, body: calc(t, body)[0],
    )


def nearest(mid: datetime, events: list[dict]) -> tuple[float, dict]:
    return min(
        (
            abs((datetime.fromisoformat(e["utc"]) - mid).total_seconds()) / 3600.0,
            e,
        )
        for e in events
    )


def evaluate(birth_dt: datetime, lat: float, lon: float, year: int, tz_name: str, event_date: str | None) -> dict:
    tz = ZoneInfo(tz_name)
    # Buffers ensure candidate days at year boundaries can see the frozen windows.
    start = datetime(year, 1, 1, tzinfo=timezone.utc) - timedelta(days=5)
    end = datetime(year + 1, 1, 1, tzinfo=timezone.utc) + timedelta(days=5)
    natal = natal_snapshot(birth_dt, lat, lon)
    slow = transit_events(natal, start, end)
    progressions = progression_events(birth_dt, natal, start, end)
    lunar = lunar_angle_events(natal, start, end)

    candidates = []
    d = date(year, 1, 1)
    while d.year == year:
        local_noon = datetime(d.year, d.month, d.day, 12, tzinfo=tz)
        mid = local_noon.astimezone(timezone.utc)
        sh, se = nearest(mid, slow)
        ph, pe = nearest(mid, progressions)
        mh, me = nearest(mid, lunar)
        if sh <= 24 and ph <= 72 and mh <= 24:
            candidates.append({
                "local_date": d.isoformat(),
                "slow_angle": {"distance_hours_from_local_noon": sh, **se},
                "progression": {"distance_hours_from_local_noon": ph, **pe},
                "lunar_angle_trigger": {"distance_hours_from_local_noon": mh, **me},
            })
        d += timedelta(days=1)

    event = None
    if event_date:
        event_day = date.fromisoformat(event_date)
        event_mid = datetime(event_day.year, event_day.month, event_day.day, 12, tzinfo=tz).astimezone(timezone.utc)
        esh, ese = nearest(event_mid, slow)
        eph, epe = nearest(event_mid, progressions)
        emh, eme = nearest(event_mid, lunar)
        match = next((x for x in candidates if x["local_date"] == event_date), None)
        event = {
            "reported_date": event_date,
            "matches_candidate_rule": match is not None,
            "matching_candidate": match,
            "nearest_families": {
                "slow_angle": {"distance_hours_from_local_noon": esh, **ese},
                "progression": {"distance_hours_from_local_noon": eph, **epe},
                "lunar_angle_trigger": {"distance_hours_from_local_noon": emh, **eme},
            },
            "thresholds_hours": {"slow_angle": 24, "progression": 72, "lunar_angle_trigger": 24},
        }

    return {
        "schema": "three-family-daily-timing-evaluation-v1",
        "rule_id": "daily_three_family_angle_activation_v1",
        "method_status": "fixed_candidate_rule_evaluation",
        "year": year,
        "civil_timezone": tz_name,
        "birth": natal,
        "rule": {
            "slow_major_aspect_to_ASC_or_MC_hours": 24,
            "progression_major_aspect_to_natal_planets_or_angles_hours": 72,
            "transiting_moon_major_aspect_to_ASC_or_MC_hours": 24,
            "major_aspects": list(ASPECTS),
            "slow_movers": list(TRANSIT_PLANETS),
            "progressed_movers": [f"p{k}" for k in PROGRESSED_PLANETS],
            "require_all_three_families": True,
        },
        "candidate_count": len(candidates),
        "candidate_dates": candidates,
        "event_evaluation": event,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--birth-utc", required=True)
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--timezone", required=True)
    ap.add_argument("--event-date")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    ephem_root = Path(os.environ.get("EPHEMERIS_ROOT", Path(__file__).resolve().parents[1] / "data" / "ephemeris"))
    required = (ephem_root / "sepl_18.se1", ephem_root / "semo_18.se1")
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise SystemExit("Missing Swiss ephemeris files: " + ", ".join(missing))
    swe.set_ephe_path(str(ephem_root))

    result = evaluate(parse_utc(args.birth_utc), args.lat, args.lon, args.year, args.timezone, args.event_date)
    result["ephemeris"] = {
        "root": str(ephem_root),
        "sepl_18_sha256": sha256(required[0]),
        "semo_18_sha256": sha256(required[1]),
        "version": swe.version,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "out": str(args.out),
        "candidate_count": result["candidate_count"],
        "candidate_dates": [x["local_date"] for x in result["candidate_dates"]],
        "event_evaluation": result["event_evaluation"],
        "asc": result["birth"]["asc"],
        "mc": result["birth"]["mc"],
    }, indent=2))


if __name__ == "__main__":
    main()
