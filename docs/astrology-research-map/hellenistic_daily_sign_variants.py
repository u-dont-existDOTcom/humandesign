"""Source-only arithmetic contrast for ancient daily sign-allocation descriptions.

This is NOT a natal chart calculator, accepted timing rule, or evidence of
prediction. It computes only how different reported days-per-sign rates would
partition consecutive days after a hypothetical shared sign origin.

Source witnesses:
* Paulus, Introductory Matters ch. 31, Greenbaum p. 65: one day/sign
* Hephaistio II ch. 28, Schmidt p. 82: two and a half days/sign
* Ptolemy, Tetrabiblos IV.10, Robbins p. 453: two and a third days/sign
* Robbins note 3 p. 453: two and a half days/sign in two manuscript witnesses
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class SourceDailyRate:
    name: str
    days_per_sign: Fraction
    locator: str
    calendar_note: str


RATES = {
    "PAULUS_1D": SourceDailyRate(
        "PAULUS_1D", Fraction(1, 1), "Paulus ch31, Greenbaum p65",
        "One sign per month for monthly rulers; this demonstration fixes a shared origin artificially.",
    ),
    "HEPH_5_OVER_2": SourceDailyRate(
        "HEPH_5_OVER_2", Fraction(5, 2), "Hephaistio II.28, Schmidt p82",
        "Two and a half days per sign; 30-day 12-sign coverage is arithmetic, not a complete calendar policy.",
    ),
    "PTOLEMY_ROBBINS_7_OVER_3": SourceDailyRate(
        "PTOLEMY_ROBBINS_7_OVER_3", Fraction(7, 3), "Tetrabiblos IV.10, Robbins p453",
        "Main English critical text also specifies 28 days per sign for months.",
    ),
    "PTOLEMY_MSS_5_OVER_2": SourceDailyRate(
        "PTOLEMY_MSS_5_OVER_2", Fraction(5, 2), "Tetrabiblos IV.10, Robbins p453 note3",
        "Separate two-manuscript days-per-sign reading; do not assume linked to 30-day month variant.",
    ),
}


def relative_sign(elapsed_whole_days: int, variant: str, origin_sign: int = 0) -> int:
    """Relative 0..11 sign, NOT a historical date or natal sign prediction.

    Day 1 = elapsed_whole_days=0. Fractions give exact floor boundaries
    without binary floating rounding or implicit local timezone.
    """
    if not isinstance(elapsed_whole_days, int) or elapsed_whole_days < 0:
        raise ValueError("elapsed_whole_days must be a non-negative integer")
    if not isinstance(origin_sign, int) or not (0 <= origin_sign < 12):
        raise ValueError("origin_sign must be an integer between 0 and 11")
    if variant not in RATES:
        raise ValueError("unknown named historical witness")
    days_per_sign = RATES[variant].days_per_sign
    sign_offset = elapsed_whole_days // days_per_sign
    return (origin_sign + sign_offset) % 12


def discrepancy_counts(days: int = 28) -> dict[str, int]:
    """Compare named source rate descriptions over toy consecutive days."""
    if not isinstance(days, int) or days <= 0:
        raise ValueError("days must be a positive integer")
    p = "PAULUS_1D"
    h = "HEPH_5_OVER_2"
    t = "PTOLEMY_ROBBINS_7_OVER_3"
    vals = [(relative_sign(k, p), relative_sign(k, h), relative_sign(k, t))
            for k in range(days)]
    return {
        "toy_days": days,
        "paulus_vs_hephaistio_different": sum(a != b for a, b, c in vals),
        "paulus_vs_ptolemy_different": sum(a != c for a, b, c in vals),
        "hephaistio_vs_ptolemy_different": sum(b != c for a, b, c in vals),
        "all_three_identical": sum(a == b == c for a, b, c in vals),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(discrepancy_counts(), indent=2))
