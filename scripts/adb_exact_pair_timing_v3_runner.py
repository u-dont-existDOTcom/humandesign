#!/usr/bin/env python3
"""Engineering runner for frozen exact-pair timing V3.

Adds the preflight exclusion required by the frozen inclusion rule and memoizes
repeated astronomical calculations. No feature/model rule is changed.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache

import adb_exact_pair_timing_v3 as v3

_original_make_events = v3.make_events
EXCLUSIONS = Counter()

# --- Pure computation caches (same inputs -> same frozen outputs) ---
_orig_natal = v3.natal
_orig_houses = v3.houses
_orig_progressed = v3.progressed
_orig_calc = v3.calc
_orig_hd_natal_gates = v3.hd.natal_gates
_orig_transit_gate_state = v3.hd.transit_gate_state

@lru_cache(maxsize=None)
def natal_cached(jd):
    return _orig_natal(jd)

@lru_cache(maxsize=None)
def houses_cached(jd, lat, lon):
    return _orig_houses(jd, lat, lon)

@lru_cache(maxsize=None)
def progressed_cached(birth_jd, event_jd):
    return _orig_progressed(birth_jd, event_jd)

@lru_cache(maxsize=None)
def calc_cached(jd, body):
    return _orig_calc(jd, body)

@lru_cache(maxsize=None)
def hd_natal_cached(jd):
    return _orig_hd_natal_gates(v3.hd.dt_from_jd(jd))

@lru_cache(maxsize=None)
def hd_transit_cached(jd):
    return _orig_transit_gate_state(v3.hd.dt_from_jd(jd))

v3.natal = natal_cached
v3.houses = houses_cached
v3.progressed = progressed_cached
v3.calc = calc_cached


def hd_features_cached(a, b, event_jd):
    ag = hd_natal_cached(a.jd)
    bg = hd_natal_cached(b.jd)
    _by, tg = hd_transit_cached(event_jd)
    fp = v3.hd.fingerprint(ag | bg | tg)
    n = fp["defined_center_count"]
    comp = fp["definition_components"]
    ch = len(fp["channels"])
    return {
        "hd_center_count": float(n),
        "hd_components": float(comp),
        "hd_single": float(comp == 1),
        "hd_8plus1": float(n == 8),
        "hd_9plus0": float(n == 9),
        "hd_channel_count": float(ch),
    }

v3.hd_features = hd_features_cached


def person_supported(person) -> bool:
    try:
        for body in v3.NATAL_IDS.values():
            v3.calc(person.jd, body)
        hd_natal_cached(person.jd)
        return True
    except Exception as exc:
        print(f"prefilter person {person.key}: {exc}", flush=True)
        return False


def make_events_prefilter(entries, recovered):
    events = _original_make_events(entries, recovered)
    support = {}
    kept = []
    for ev in events:
        if ev.a.key not in support:
            support[ev.a.key] = person_supported(ev.a)
        if ev.b.key not in support:
            support[ev.b.key] = person_supported(ev.b)
        if not (support[ev.a.key] and support[ev.b.key]):
            EXCLUSIONS["pair_birth_or_design_outside_swieph"] += 1
            continue
        kept.append(ev)
    print("preflight event exclusions", dict(EXCLUSIONS), flush=True)
    return kept


@lru_cache(maxsize=None)
def candidate_supported(jd) -> bool:
    try:
        for body in v3.TRANSIT_IDS.values():
            v3.calc(jd, body)
        return True
    except Exception:
        return False


def build_rows_prefilter(events, transition):
    rows = []
    counts = Counter()
    for ev in events:
        if ev.transition != transition:
            continue
        true_jd = v3.date_jd(ev.year, ev.month, ev.day)
        if not candidate_supported(true_jd):
            counts["true_event_date_outside_swieph"] += 1
            continue
        candidates = [(ev.year, ev.month, ev.day, 1)]
        for dy in v3.SHIFT_YEARS:
            sh = v3.safe_shift(ev.year, ev.month, ev.day, dy)
            if not sh:
                continue
            y, m, d, _ = sh
            cj = v3.date_jd(y, m, d)
            aa = (cj - ev.a.jd) / v3.TROPICAL_YEAR
            bb = (cj - ev.b.jd) / v3.TROPICAL_YEAR
            if not (16 <= aa <= 85 and 16 <= bb <= 85):
                counts["age_excluded"] += 1
                continue
            if not candidate_supported(cj):
                counts["candidate_date_outside_swieph"] += 1
                continue
            candidates.append((y, m, d, 0))
        if len(candidates) < 6:
            counts["too_few_controls"] += 1
            continue
        ek = f"{ev.pair_key}|{ev.event_id}|{ev.year:04d}-{ev.month:02d}-{ev.day:02d}"
        for y, m, d, actual in candidates:
            rows.append({
                "event_key": ek,
                "pair_key": ev.pair_key,
                "actual": actual,
                "features": v3.raw_features(ev, v3.date_jd(y, m, d)),
            })
    counts.update(EXCLUSIONS)
    return rows, dict(counts)


if __name__ == "__main__":
    v3.make_events = make_events_prefilter
    v3.build_rows = build_rows_prefilter
    v3.main()
