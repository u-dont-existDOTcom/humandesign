#!/usr/bin/env python3
"""Independent CF-003 printed-table arithmetic, not a source-target replay.

Numbers below are transcribed from Godbout and Coron, Correlation 35(2) (2023),
Table 10, and 36(1) (2023), Tables 2--4. No person-level records are inferred.
Run: python scripts/empirical_astrology/reproduce_cf003_20260929.py
"""
from __future__ import annotations

import json
import math


# n, top biographical ranks, prediction tries, successes, printed p0,
# printed Z, printed one-sided normal-tail p.
REPLICATION = (
    (61, 1, 1, 13, .107, 2.68, .00372),
    (61, 1, 2, 24, .206, 3.61, .000152),
    (61, 1, 3, 29, .311, 2.78, .00274),
    (61, 2, 1, 23, .214, 3.10, .000961),
    (61, 2, 2, 39, .390, 4.00, .0000317),
    (61, 2, 3, 43, .546, 2.50, .00624),
    (61, 3, 1, 29, .319, 2.63, .00432),
    (61, 3, 2, 42, .548, 2.21, .0135),
    (61, 3, 3, 47, .718, .91, .182),
)
TRAINING = (
    (189, 3, 1, 92, .319, 4.96, 3.56e-7),
    (189, 3, 2, 135, .548, 4.60, 2.08e-6),
    (189, 3, 3, 158, .718, 3.60, 1.61e-4),
)


def check_cell(cell: tuple[int, int, int, int, float, float, float]) -> dict:
    n, rank_max, tries, successes, p0, printed_z, printed_p = cell
    assert 0 <= successes <= n and 0 < p0 < 1
    z = (successes / n - p0) / math.sqrt(p0 * (1 - p0) / n)
    p = math.erfc(z / math.sqrt(2)) / 2
    effect_size = (successes / n - p0) / math.sqrt(p0 * (1 - p0))
    # Rounded p0 (one decimal percent) prevents exact agreement with the
    # unpublished baseline; this tolerance is a sensitivity check, not a fit.
    assert abs(z - printed_z) < .02, (cell, z)
    assert abs(p / printed_p - 1) < .06, (cell, p)
    return {
        "n": n,
        "rank_max": rank_max,
        "tries": tries,
        "successes_printed": successes,
        "printed_p0_rounded": p0,
        "expected_from_rounded_p0": round(n * p0, 3),
        "printed_z": printed_z,
        "z_from_rounded_p0": round(z, 6),
        "printed_one_sided_p": printed_p,
        "one_sided_normal_p_from_rounded_p0": p,
        "effect_size_from_rounded_p0": round(effect_size, 6),
    }


def results() -> dict:
    rep = [check_cell(row) for row in REPLICATION]
    train = [check_cell(row) for row in TRAINING]
    assert [(r["rank_max"], r["tries"], r["successes_printed"])
            for r in rep] == [
                (1, 1, 13), (1, 2, 24), (1, 3, 29),
                (2, 1, 23), (2, 2, 39), (2, 3, 43),
                (3, 1, 29), (3, 2, 42), (3, 3, 47),
            ]
    assert round(train[-1]["expected_from_rounded_p0"], 1) == 135.7
    assert round(rep[-1]["expected_from_rounded_p0"], 1) == 43.8
    return {
        "schema_version": 1,
        "scope": "Independent arithmetic replay of printed aggregates only; no targets, per-person vectors, or assignment-respecting null.",
        "source_sha256": {
            "training_2023_35_2": "780b8422d77059892b57c395d9cf3c2b40f828706b0c2ed51a7bcabb0b03aac6",
            "replication_2023_36_1": "a4c0da056639aa0833dd96229a4efc3817395729b26c361875f24322f5092f44",
        },
        "training_table_10": train,
        "replication_tables_2_to_4": rep,
        "reported_text_table_disagreements": [
            {
                "source": "35(2) p.25 prose versus Table 10 p.24",
                "prose": "Third training condition: 158 successes, expected 151.6.",
                "table": "158 successes, expected 135.8.",
                "expected_from_printed_rounded_p0": 135.702,
            },
            {
                "source": "36(1) p.53 prose versus Table 4 p.52",
                "prose": "Third replication condition: 43.8 successes, expected 33.3.",
                "table": "47 successes, expected 43.8.",
                "expected_from_printed_rounded_p0": 43.798,
            },
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), ensure_ascii=False, indent=2, allow_nan=False))
