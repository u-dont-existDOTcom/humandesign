"""Replay the CF-004 arithmetic that is actually printed in Correlation 38(1).

The source publishes only three of the 141 paired global scores. This program
does not infer the other 138 decisions or simulate a biography-assignment null.
All numeric inputs below are transcribed from the 2026 issue's pp. 47-50.
"""

from __future__ import annotations

from decimal import Decimal
import json
from math import asin, comb, erfc, sqrt


EXAMPLES = {
    "Allende": ("0.9989", "0.9425", "0.0456", "Table 1, p. 47"),
    "Anitta": ("0.3616", "0.9617", "0.0201", "Table 1, p. 47"),
    "Musk": ("0.3170", "0.3329", "0.1108", "Table 4, p. 50"),
}


def upper_binomial_tail(k: int, n: int) -> float:
    """Exact one-sided P[X >= k] for X ~ Binomial(n, 1/2)."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2**n


def replay() -> dict:
    south_wins, south_n = 48, 68
    north_wins, north_n = 26, 73
    p_south = south_wins / south_n
    p_north = north_wins / north_n
    pooled = (south_wins + north_wins) / (south_n + north_n)
    standard_error = sqrt(pooled * (1 - pooled) * (1 / south_n + 1 / north_n))
    z = (p_south - p_north) / standard_error
    rows = []
    for person, (original, inverted, printed, source) in EXAMPLES.items():
        corrected = Decimal(inverted) - Decimal(original)
        rows.append(
            {
                "person": person,
                "source": source,
                "printed_non_inverted": original,
                "printed_inverted": inverted,
                "printed_difference": printed,
                "computed_inverted_minus_non_inverted": str(corrected),
                "difference_matches_print": corrected == Decimal(printed),
                "inversion_wins_according_to_printed_pair": corrected > 0,
            }
        )
    return {
        "scope": "aggregate arithmetic and three printed paired-score examples only",
        "published_total_people": south_n + north_n,
        "individual_pairs_printed": len(rows),
        "individual_pairs_unprinted": south_n + north_n - len(rows),
        "aggregate": {
            "south_inversion_wins": south_wins,
            "south_n": south_n,
            "north_inversion_wins": north_wins,
            "north_n": north_n,
            "south_inversion_rate": p_south,
            "north_inversion_rate": p_north,
            "pooled_z": z,
            "one_sided_p": erfc(z / sqrt(2)) / 2,
            "cohen_h": 2 * (asin(sqrt(p_south)) - asin(sqrt(p_north))),
            "south_binomial_one_sided_p_assuming_half": upper_binomial_tail(48, 68),
            "north_noninversion_binomial_one_sided_p_assuming_half": upper_binomial_tail(47, 73),
        },
        "examples": rows,
        "other_printed_inconsistencies": {
            "figure_6_p49": "Non-inverted Sun Capricorn / inverted Cancer in columns; p. 50 prose describes Capricorn as inverted, and p. 51 treats Sun Cancer as non-inverted.",
            "musk_authority_pp50_51": "Table 4 inverted authority word score 7.9; Table 5 inverted Autority score 7.0.",
            "p48_risk_ratio_arithmetic": "Printed 0.705/0.365=1.98; printed fractions yield 1.932, whereas unrounded south/north rates yield 1.982.",
        },
        "person_level_reproduction": "blocked: 138 score pairs and complete chart/profile/word-score exports not published in examined PDF",
        "assignment_respecting_null": "not run: requires complete paired score generation and fixed profiles/scoring pipeline",
    }


if __name__ == "__main__":
    result = replay()
    assert all(not row["difference_matches_print"] for row in result["examples"])
    assert result["individual_pairs_printed"] == 3
    assert abs(result["aggregate"]["pooled_z"] - 4.155) < 0.002
    assert abs(result["aggregate"]["cohen_h"] - 0.716) < 0.002
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
