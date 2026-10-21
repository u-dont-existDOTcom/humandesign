"""Standalone, *non-production* source-variant fixtures for Jyotish text study.

Two variants of Ekadhipatya (shared-lord) Ashtakavarga reduction.  They are
not empirical forecasting algorithms, and this file does NOT select a default
or claim to implement all Sanskrit/edition exceptions.

Original Sanskrit locations: BPHS Chapter 68 vv1–6, Hora Sara shared-lord
section, Phaladipika Chapter 24 vv18–22.  Variant 'difference' appears in
later paraphrases and a worked example; source pedigree is unsettled.
"""
from __future__ import annotations

from typing import Literal, Sequence

Method = Literal["equalize", "difference"]
SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
DUAL_LORD_PAIRS = ((0, 7), (1, 6), (2, 5), (8, 11), (9, 10))
TRINES = ((0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11))


def _validate_value(value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"Counts must be nonnegative integers, got {value!r}")


def _method(method: str) -> None:
    if method not in ("equalize", "difference"):
        raise ValueError("Choose an explicit source variant: equalize or difference")


def reduce_same_lord_pair(
    first: int,
    second: int,
    *,
    first_occupied: bool,
    second_occupied: bool,
    method: Method,
) -> tuple[int, int]:
    """Reduce a single same-lord sign pair after Trikona.

    Assumes occupancy flags are supplied independently of computed outcomes.
    This *does not* determine birth-chart positions or astrological accuracy.
    """
    _validate_value(first)
    _validate_value(second)
    _method(method)
    if type(first_occupied) is not bool or type(second_occupied) is not bool:
        raise TypeError("Occupancy flags must be boolean")
    if first == 0 or second == 0 or (first_occupied and second_occupied):
        return first, second
    if not first_occupied and not second_occupied:
        if first == second:
            return 0, 0
        if method == "equalize":
            minimum = min(first, second)
            return minimum, minimum
        minimum = min(first, second)
        return first - minimum, second - minimum
    if first_occupied:
        return first, (0 if second <= first else first if method == "equalize" else second - first)
    return (0 if first <= second else second if method == "equalize" else first - second), second


def reduce_trines(counts: Sequence[int]) -> tuple[int, ...]:
    """Trikona stage, BPHS Ch67: skip any trine with a zero."""
    if len(counts) != 12:
        raise ValueError("Exactly twelve sign counts required")
    result = list(counts)
    for value in result:
        _validate_value(value)
    for a, b, c in TRINES:
        values = [result[a], result[b], result[c]]
        least = min(values)
        if least == 0:
            continue
        for idx in (a, b, c):
            result[idx] -= least
    return tuple(result)


def reduce_same_lord_signs(
    counts: Sequence[int],
    *,
    occupied_sign_indices: Sequence[int],
    method: Method,
) -> tuple[int, ...]:
    """Ekadhipatya stage only, intended on *post-Trikona* counts.

    Cancer/Leo (the single-lord signs) stay unchanged. Occupancy excludes
    non-classical bodies unless a separate source-version is declared.
    """
    if len(counts) != 12:
        raise ValueError("Exactly twelve sign counts required")
    for value in counts:
        _validate_value(value)
    _method(method)
    if any(type(idx) is not int or not 0 <= idx < 12 for idx in occupied_sign_indices):
        raise ValueError("Occupied indices must be 0..11 integers")
    occupied = set(occupied_sign_indices)
    result = list(counts)
    for left, right in DUAL_LORD_PAIRS:
        result[left], result[right] = reduce_same_lord_pair(
            result[left], result[right],
            first_occupied=(left in occupied),
            second_occupied=(right in occupied),
            method=method,
        )
    return tuple(result)
