#!/usr/bin/env python3
"""Engineering runner for frozen exact-pair timing V3.

Adds the preflight exclusion required by the frozen inclusion rule: both natal
moments, their HD design roots, and candidate event/control dates must be
supported by the pinned Swiss ephemeris. No feature/model rule is changed.
"""
from __future__ import annotations

from collections import Counter

import adb_exact_pair_timing_v3 as v3


_original_make_events = v3.make_events
_original_build_rows = v3.build_rows
EXCLUSIONS = Counter()


def person_supported(person) -> bool:
    try:
        # Natal support.
        for body in v3.NATAL_IDS.values():
            v3.calc(person.jd, body)
        # HD support including exact Design-root calculation.
        v3.hd.natal_gates(v3.hd.dt_from_jd(person.jd))
        return True
    except Exception as exc:
        print(f"prefilter person {person.key}: {exc}", flush=True)
        return False


def make_events_prefilter(entries, recovered):
    events = _original_make_events(entries, recovered)
    cache = {}
    kept = []
    for ev in events:
        ok_a = cache.setdefault(ev.a.key, person_supported(ev.a))
        ok_b = cache.setdefault(ev.b.key, person_supported(ev.b))
        if not (ok_a and ok_b):
            EXCLUSIONS["pair_birth_or_design_outside_swieph"] += 1
            continue
        kept.append(ev)
    print("preflight event exclusions", dict(EXCLUSIONS), flush=True)
    return kept


def candidate_supported(jd) -> bool:
    try:
        for body in v3.TRANSIT_IDS.values():
            v3.calc(jd, body)
        return True
    except Exception:
        return False


def build_rows_prefilter(events, transition):
    # Mirror frozen candidate construction but remove unsupported event/control
    # dates before raw feature calculation.
    rows = []
    counts = Counter()
    for ev in events:
        if ev.transition != transition:
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
        # True event date itself must also be supported by the frozen rule.
        true_jd = v3.date_jd(ev.year, ev.month, ev.day)
        if not candidate_supported(true_jd):
            counts["true_event_date_outside_swieph"] += 1
            continue
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
