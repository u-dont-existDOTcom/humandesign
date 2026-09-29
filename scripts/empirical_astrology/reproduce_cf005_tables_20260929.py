#!/usr/bin/env python3
"""Replay printed CF-005 arithmetic, conditional on its published event counts.

This checks Tables 3–6 and the combined birth-third tables C.2/D.2 of
Daigno, Correlation 38(2), 2026, pp.16–18,25–27. It is not a person-level
reanalysis, a valid exchangeability test, or an astrology-model decision.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


SOURCE_SHA256 = "5d6a87dc0e5aff058d007a66b2104035a27b639a566fa078ab1e0539d7af1024"
ASPECTS = (
    "MO 0 MA", "MO 180 MA", "ME 0 MA", "ME 180 MA",
    "VE 0 MA", "VE 180 MA", "SO 0 MA", "SO 180 MA",
)
# Each row: observed aspect events, observed aspect opportunities, control
# events, control opportunities, source-reported one-sided binomial p.
FRENCH = (
    (7, 60, 450, 4148, .47948), (12, 66, 443, 4107, .04845),
    (21, 105, 772, 7472, .00231), (0, 40, 138, 2694, 1.0),
    (7, 82, 614, 6195, .71507), (6, 35, 235, 2853, .06409),
    (15, 97, 747, 7269, .07067), (5, 32, 156, 2687, .03581),
)
SERIAL = (
    (8, 85, 776, 7124, .71996), (12, 60, 749, 7014, .02334),
    (27, 122, 1329, 12891, .00010), (5, 41, 255, 4569, .07664),
    (21, 99, 1221, 10844, .00309), (2, 47, 351, 4869, .86183),
    (21, 129, 1291, 12524, .02362), (5, 47, 269, 4661, .13312),
)
# Aggregate event/opportunity sums as printed in Tables 3/5 and C.2/D.2.
COMBINED = (
    ("french_all", 73, 517, 3555, 37425, 3.5485, .000194),
    ("serial_all", 101, 630, 6241, 64496, 5.3543, 4.30e-8),
    ("french_1819_1874", 25, 154, 3089, 31652, 2.697, .0035),
    ("french_1875_1893", 25, 166, 2894, 31077, 2.5378, .0056),
    ("french_1894_1930", 23, 197, 3034, 30506, .8081, .210),
    ("serial_1803_1945", 32, 203, 2753, 29526, 3.138, .000851),
    ("serial_1946_1962", 29, 215, 2968, 32206, 2.1558, .0155),
    ("serial_1963_1995", 40, 212, 3274, 30495, 3.8027, .0000716),
)


def upper_binomial(k: int, n: int, p: float) -> float:
    return math.fsum(math.comb(n, j) * p**j * (1 - p)**(n - j) for j in range(k, n + 1))


def aspects(rows: tuple[tuple[int, int, int, int, float], ...]) -> list[dict]:
    out = []
    for name, (observed, trials, control, control_trials, published_p) in zip(ASPECTS, rows, strict=True):
        p0 = control / control_trials
        p = upper_binomial(observed, trials, p0)
        assert abs(p - published_p) <= 1e-5, (name, p, published_p)
        out.append({"aspect": name, "observed_events": observed,
                    "observed_event_opportunities": trials, "control_events": control,
                    "control_event_opportunities": control_trials,
                    "conditional_control_fraction": p0,
                    "conditional_exact_binomial_p": p, "printed_p": published_p,
                    "below_authors_eight_test_threshold": p < .00625})
    return out


def combined() -> list[dict]:
    out = []
    for label, observed, trials, control, control_trials, printed_z, printed_p in COMBINED:
        p1 = observed / trials
        p0 = control / control_trials
        pooled = (observed + control) / (trials + control_trials)
        z = (p1 - p0) / math.sqrt(pooled * (1 - pooled) * (1 / trials + 1 / control_trials))
        p = .5 * math.erfc(z / math.sqrt(2))
        h = 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p0)))
        assert abs(z - printed_z) <= 6e-5, (label, z, printed_z)
        # The period tables print between two and eight significant figures.
        assert abs(p - printed_p) <= 5.1e-4, (label, p, printed_p)
        out.append({"cohort_and_period": label, "observed_events": observed,
                    "observed_event_opportunities": trials, "control_events": control,
                    "control_event_opportunities": control_trials,
                    "conditional_two_proportions_z": z, "conditional_one_sided_p": p,
                    "conditional_cohen_h": h, "printed_z": printed_z, "printed_p": printed_p})
    return out


def result() -> dict:
    french = aspects(FRENCH)
    serial = aspects(SERIAL)
    assert [(x["aspect"]) for x in french if x["below_authors_eight_test_threshold"]] == ["ME 0 MA"]
    assert [(x["aspect"]) for x in serial if x["below_authors_eight_test_threshold"]] == ["ME 0 MA", "VE 0 MA"]
    totals = combined()
    assert [sum(row[j] for row in FRENCH) for j in range(4)] == [73, 517, 3555, 37425]
    assert [sum(row[j] for row in SERIAL) for j in range(4)] == [101, 630, 6241, 64496]
    assert [sum(row[j] for row in COMBINED[2:5]) for j in range(1, 5)] == [73, 517, 9017, 93235]
    assert [sum(row[j] for row in COMBINED[5:8]) for j in range(1, 5)] == [101, 630, 8995, 92227]
    return {
        "schema_version": 1,
        "source": "Daigno 2026, Correlation 38(2), 13–28; Tables 3–6, C.2 and D.2",
        "source_complete_issue_sha256": SOURCE_SHA256,
        "scope": "Conditional arithmetic checks of source-published counts, not a corrected person-level inference",
        "authors_threshold": .00625,
        "french_individual_aspects": french,
        "serial_individual_aspects": serial,
        "combined_event_tables": totals,
        "reported_temporal_mercury_conjunction_p_without_extractable_cell_counts": {
            "french": [.00062, .15124, .44856],
            "serial": [.05906, .76209, .01503],
        },
        "limitations": [
            "Aspect events and opportunities can share people; the table denominators are not independent persons.",
            "Calendar-day ephemerides and shuffled component controls do not constitute matched-person controls.",
            "The per-person event vectors, source-year rosters and control-generator software are absent from the issue; no cluster-adjusted uncertainty or fresh null is estimated.",
            "The C.3/D.3 temporal Mercury-conjunction p-values lack text-extractable per-cell counts, so they remain reported rather than reproduced here.",
            "A time-varying Wikidata query is not the same as the author's frozen 2026 person roster.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(result(), indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end="")
