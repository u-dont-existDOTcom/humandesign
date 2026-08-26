#!/usr/bin/env python3
"""Engineering adapter for the frozen Castille wedding-timing V1.

The pre-run audit of the implementation found that the draft combined the
frozen annual sine/cosine phase terms into one column. No result had been run.
This adapter restores the two separate frozen columns and corresponding feature
dimensions without changing any scientific rule.
"""
from __future__ import annotations

import math
import numpy as np

import castille_wedding_timing_v1 as v1

v1.P0 = 7
v1.P1 = v1.P0 + 2 * (5 * 6 * 5 + 4 * 6 * 5)
v1.P3 = v1.P1 + 2 * (4 * 6 * 5) + (4 * 4 * 5) + (5 * 6 * 5) + (5 * 4 * 5)
v1.MODEL_DIMS = {"M0T": v1.P0, "M1T": v1.P1, "M3T": v1.P3}


def frozen_base_features(r, cand):
    ma = v1.static.age_years(r.mother, cand)
    fa = v1.static.age_years(r.father, cand)
    signed = ma - fa
    phase = 2 * math.pi * ((cand[1] - 1) + (cand[2] - 1) / 31.0) / 12.0
    return np.asarray([
        ma,
        fa,
        signed,
        abs(signed),
        (cand[0] - 1985.0) / 20.0,
        math.sin(phase),
        math.cos(phase),
    ], dtype=np.float32)


v1.base_features = frozen_base_features

if __name__ == "__main__":
    v1.main()
