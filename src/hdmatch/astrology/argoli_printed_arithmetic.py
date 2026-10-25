"""Literal historical degree-minute/second arithmetic, without silent repairs.

This pure arithmetic validates three matched examples in photographed original
Argoli 1610 and 1667 editions. It makes NO claim of full edition equivalence,
planetary forecast success, authentic Argolus timing key, or human validation.
"""

from __future__ import annotations

from collections.abc import Sequence


def subtract_degree_minutes(minuend: Sequence[int], subtrahend: Sequence[int]) -> tuple[int, int]:
    """Nonnegative angular subtraction in sexagesimal degrees and minutes."""
    if len(minuend) != 2 or len(subtrahend) != 2:
        raise ValueError("degree-minute operands require exactly two integers")
    vals = tuple(minuend) + tuple(subtrahend)
    if any(type(value) is not int for value in vals):
        raise ValueError("historical integer operands only")
    if not (0 <= minuend[0] <= 360 and 0 <= subtrahend[0] <= 360):
        raise ValueError("degrees must be in 0–360 range")
    if not (0 <= minuend[1] < 60 and 0 <= subtrahend[1] < 60):
        raise ValueError("minutes must be in 0–59 range")
    total = minuend[0] * 60 + minuend[1] - subtrahend[0] * 60 - subtrahend[1]
    if total < 0:
        raise ValueError("these source examples require nonnegative differences")
    return divmod(total, 60)


def subtract_degree_minute_seconds(
    minuend: Sequence[int], subtrahend: Sequence[int]
) -> tuple[int, int, int]:
    """Nonnegative angular subtraction in literal D° M′ S″."""
    if len(minuend) != 3 or len(subtrahend) != 3:
        raise ValueError("degree-minute-second operands require 3 integers")
    values = tuple(minuend) + tuple(subtrahend)
    if any(type(value) is not int for value in values):
        raise ValueError("historical integer operands only")
    if not (0 <= minuend[0] <= 360 and 0 <= subtrahend[0] <= 360):
        raise ValueError("degrees must be in 0–360 range")
    if any(not (0 <= v < 60) for v in (*minuend[1:], *subtrahend[1:])):
        raise ValueError("minutes and seconds must be in 0–59 range")
    value = ((minuend[0] * 60 + minuend[1]) * 60 + minuend[2]) - (
        (subtrahend[0] * 60 + subtrahend[1]) * 60 + subtrahend[2]
    )
    if value < 0:
        raise ValueError("these source examples require nonnegative differences")
    degrees, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return degrees, minutes, seconds


def printed_arc_discrepancy_minutes(computed: Sequence[int], observed: Sequence[int]) -> int:
    """Signed printing error, preserving *both* original historical readings."""
    if len(computed) != 2 or len(observed) != 2:
        raise ValueError("each historical angular reading is degree/minute")
    for sample in (computed, observed):
        if any(type(x) is not int for x in sample):
            raise ValueError("only exact printed integer readings supported")
        if not (0 <= sample[0] <= 360 and 0 <= sample[1] < 60):
            raise ValueError("invalid historical angle")
    return (observed[0] - computed[0]) * 60 + observed[1] - computed[1]
