from __future__ import annotations
import json, os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import swisseph as swe

BASE = Path(__file__).resolve().parent
YEAR = 2026
TZ = ZoneInfo("Europe/Istanbul")
EPHEM = os.environ["EPHEMERIS_ROOT"]
swe.set_ephe_path(EPHEM)
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED

timing = json.loads((BASE / "PROJECT_TIMING_2020_2041.json").read_text())["record"]
angles = {"ASC": 215.152487, "MC": 132.20992195252455}
aspects = (0, 60, 90, 120, 180)

slow = []
for event in timing["transit_events"]:
    t = datetime.fromisoformat(event["utc"])
    if t.year == YEAR and event["target"] in angles:
        slow.append((t, event))

progressions = []
for event in timing["progression_events"]:
    t = datetime.fromisoformat(event["utc"])
    if t.year == YEAR:
        progressions.append((t, event))

def jd(dt: datetime) -> float:
    hour = dt.hour + dt.minute / 60 + dt.second / 3600 + dt.microsecond / 3_600_000_000
    return swe.julday(dt.year, dt.month, dt.day, hour, swe.GREG_CAL)

def moon_lon(dt: datetime) -> float:
    xx, returned = swe.calc_ut(jd(dt), swe.MOON, FLAGS)
    if not (returned & swe.FLG_SWIEPH):
        raise RuntimeError(f"Swiss Ephemeris requested but returned flags={returned}")
    return xx[0] % 360.0

def adiff(a: float, b: float) -> float:
    return ((a - b + 180.0) % 360.0) - 180.0

def residual(dt: datetime, target: float, aspect: int) -> float:
    return adiff(moon_lon(dt) - target, aspect)

start = datetime(YEAR, 1, 1, tzinfo=timezone.utc)
end = datetime(YEAR + 1, 1, 1, tzinfo=timezone.utc)
step = timedelta(hours=1)
lunar = []
for target_name, target_lon in angles.items():
    for aspect in aspects:
        values = []
        t = start
        while t <= end:
            values.append((t, abs(residual(t, target_lon, aspect))))
            t += step
        for i in range(1, len(values) - 1):
            if values[i][1] <= values[i-1][1] and values[i][1] <= values[i+1][1] and values[i][1] < 0.6:
                lo, hi = values[i][0] - step, values[i][0] + step
                for _ in range(30):
                    m1 = lo + (hi - lo) / 3
                    m2 = hi - (hi - lo) / 3
                    if abs(residual(m1, target_lon, aspect)) < abs(residual(m2, target_lon, aspect)):
                        hi = m2
                    else:
                        lo = m1
                exact = lo + (hi - lo) / 2
                if start <= exact < end and abs(residual(exact, target_lon, aspect)) < 0.01:
                    if not any(
                        target_name == old[1]["target"]
                        and aspect == old[1]["aspect"]
                        and abs((exact - old[0]).total_seconds()) < 3600
                        for old in lunar
                    ):
                        lunar.append((exact, {"moving": "Moon", "aspect": aspect, "target": target_name}))
lunar.sort()

def nearest(mid: datetime, events):
    return min(events, key=lambda item: abs((item[0] - mid).total_seconds()))

rows = []
d = date(YEAR, 1, 1)
while d.year == YEAR:
    mid_local = datetime(d.year, d.month, d.day, 12, tzinfo=TZ)
    mid = mid_local.astimezone(timezone.utc)
    s = nearest(mid, slow)
    p = nearest(mid, progressions)
    m = nearest(mid, lunar)
    s_hours = abs((s[0] - mid).total_seconds()) / 3600
    p_hours = abs((p[0] - mid).total_seconds()) / 3600
    m_hours = abs((m[0] - mid).total_seconds()) / 3600
    families = int(s_hours <= 24) + int(p_hours <= 72) + int(m_hours <= 24)
    if families == 3:
        rows.append({
            "local_date": d.isoformat(),
            "slow_angle": {"distance_hours_from_local_noon": s_hours, "exact_local": s[0].astimezone(TZ).isoformat(), **s[1]},
            "progression": {"distance_hours_from_local_noon": p_hours, "exact_local": p[0].astimezone(TZ).isoformat(), **p[1]},
            "lunar_angle_trigger": {"distance_hours_from_local_noon": m_hours, "exact_local": m[0].astimezone(TZ).isoformat(), **m[1]},
        })
    d += timedelta(days=1)

out = {
    "schema": "hale-postoutcome-daily-timing-convergence-v1",
    "method_status": "POST_OUTCOME_DEVELOPMENT_NOT_VALIDATION",
    "year": YEAR,
    "timezone": "Europe/Istanbul",
    "rule": {
        "slow_outer_or_jupiter_saturn_exact_major_aspect_to_ASC_or_MC_within_hours_of_local_noon": 24,
        "any_frozen_secondary_progression_exact_major_aspect_within_hours_of_local_noon": 72,
        "transiting_moon_exact_major_aspect_to_ASC_or_MC_within_hours_of_local_noon": 24,
        "require_all_three_families": True,
    },
    "provenance": {
        "slow_transits_and_progressions": "PROJECT_TIMING_2020_2041.json; frozen before Hale outcome/history reveal in this clean-room sequence",
        "lunar_trigger_and_three_family_rule": "added after outcome exposure; discovery only",
    },
    "candidate_dates": rows,
    "candidate_count": len(rows),
}
path = BASE / "POSTHOC_DAILY_TIMING_CONVERGENCE_2026.json"
path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps(out, indent=2, sort_keys=True))
