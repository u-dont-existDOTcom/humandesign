#!/usr/bin/env python3
"""Engineering runner for frozen static partner-identification V1.

The first execution aborted before fitting because an A/AA decoy birth moment
fell outside the pinned .se1 coverage and Swiss Ephemeris correctly returned
MOSEPH. The frozen specification requires SWIEPH-only astronomy. This adapter
therefore excludes people who cannot produce both natal Western positions and
an exact HD natal gate set under the pinned SWIEPH files *before* pair/risk-set
construction. No scoring feature, decoy matching rule, model, threshold, or
hyperparameter is changed.
"""
from __future__ import annotations

from collections import Counter

import adb_static_partner_identification_v1 as v1


def swieph_eligible(person: dict) -> bool:
    jd = person.get("jd")
    if jd is None:
        return False
    try:
        for body in v1.BODY_IDS.values():
            v1.base.calc(jd, body)
        # HD design moment reaches ~88 solar degrees before birth; this call
        # verifies that the full natal HD calculation also remains SWIEPH-only.
        v1.hd.natal_gates(v1.hd.dt_from_jd(jd))
        return True
    except Exception:
        return False


def build_tasks_swieph_only(people, neighbors, pair_types):
    initially_high = {
        pid: p for pid, p in people.items()
        if p["rr"] in v1.HIGH_RR and p["jd"] is not None
    }
    high = {pid: p for pid, p in initially_high.items() if swieph_eligible(p)}
    dropped = Counter()
    dropped["exact_A_AA_people_outside_pinned_SWIEPH_coverage"] = len(initially_high) - len(high)

    positive_pairs = []
    positive_before_coverage = 0
    for (a, b), _types in sorted(pair_types.items()):
        if a in initially_high and b in initially_high:
            positive_before_coverage += 1
        if a in high and b in high:
            positive_pairs.append((a, b))
    dropped["positive_pairs_lost_to_SWIEPH_coverage"] = positive_before_coverage - len(positive_pairs)

    tasks = []
    for a, b in positive_pairs:
        for focal_id, true_id in ((a, b), (b, a)):
            focal = high[focal_id]
            true = high[true_id]
            gender = true["gender"]
            pool = []
            for pid, p in high.items():
                if pid in {focal_id, true_id} or pid in neighbors.get(focal_id, set()):
                    continue
                if p["gender"] != gender:
                    continue
                pool.append(p)
            pool.sort(key=lambda p: (abs(p["jd"] - true["jd"]), p["id"]))
            if len(pool) < v1.N_DECOYS:
                dropped["fewer_than_50_same_gender_decoys"] += 1
                continue
            decoys = pool[:v1.N_DECOYS]
            tasks.append({
                "task_key": f"{focal_id}->{true_id}",
                "group_key": f"{min(a,b)}:{max(a,b)}",
                "focal": focal,
                "true": true,
                "decoys": decoys,
                "max_decoy_birth_jd_distance_days": max(abs(p["jd"] - true["jd"]) for p in decoys),
            })
    return high, positive_pairs, tasks, dict(dropped)


if __name__ == "__main__":
    v1.build_tasks = build_tasks_swieph_only
    v1.main()
