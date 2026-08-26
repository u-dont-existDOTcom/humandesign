#!/usr/bin/env python3
"""Engineering adapter for frozen Castille static-synastry V1.

Pre-run review found that alternate-time sensitivity positions were cached only
for the final binary pairs, while the frozen sensitivity analysis also scores
the 20k final risk sets. This adapter records those already-frozen risk tasks
and includes their DOBs in the 00:00/23:59 position cache. No split, negative,
feature, model, hyperparameter, threshold, or primary result rule is changed.
"""
from __future__ import annotations

import castille_static_synastry_v1 as v1

_RISK_TASKS = []
_orig_make_risk_tasks = v1.make_risk_tasks


def make_risk_tasks_recording(records):
    tasks, drop = _orig_make_risk_tasks(records)
    _RISK_TASKS[:] = tasks
    return tasks, drop


def final_features_with_full_sensitivity_cache(pairs, hour, include_syn=True):
    dates = set()
    for r, sf in pairs:
        dates.add(r.mother)
        dates.add(r.father)
        dates.add(sf)
    for r, decoys in _RISK_TASKS:
        dates.add(r.mother)
        dates.add(r.father)
        dates.update(decoys)
    pos = v1.planet_positions(dates, hour)
    X, y, _ = v1.build_binary_matrix(pairs, pos, include_syn)
    return X, y, pos


v1.make_risk_tasks = make_risk_tasks_recording
v1.final_features_at_hour = final_features_with_full_sensitivity_cache

if __name__ == "__main__":
    v1.main()
