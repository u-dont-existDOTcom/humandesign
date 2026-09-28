"""Unweighted calculation of the retrieved Oshop--Foss karaka-kendra rule.

Inputs must already be sidereal longitudes in the caller's frozen ayanamsa and
node convention.  This module does not select the seven bodies, calculate an
ayanamsa, resolve exact ties, or decide whether the rule belongs in a model.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass

NAVAMSA_WIDTH_DEGREES = 360.0 / 108.0
KENDRA_OFFSETS = frozenset({0, 3, 6, 9})


@dataclass(frozen=True, slots=True)
class KarakaKendraResult:
    """Transparent intermediate state for one unweighted binary rule."""

    atmakaraka_body: str
    putrakaraka_body: str
    atmakaraka_rasi_sign: int
    putrakaraka_rasi_sign: int
    atmakaraka_navamsa_sign: int
    putrakaraka_navamsa_sign: int
    kendra_in_rasi: bool
    kendra_in_navamsa: bool
    kendra_in_either: bool


def _longitude(value: float) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("longitude must be finite")
    return result % 360.0


def within_sign_degree(sidereal_longitude: float) -> float:
    """Return a sidereal body's degree within its 30-degree rāśi sign."""

    return _longitude(sidereal_longitude) % 30.0


def rasi_sign_index(sidereal_longitude: float) -> int:
    """Return zero-based rāśi index: Aries=0 through Pisces=11."""

    return int(_longitude(sidereal_longitude) // 30.0)


def navamsa_sign_index(sidereal_longitude: float) -> int:
    """Return zero-based D9 navāṃśa sign index from sidereal longitude."""

    # Multiplication avoids floor-division rounding just below exact 30/60/etc.
    # boundaries when the repeating 3 1/3-degree width is represented as float.
    division = int(_longitude(sidereal_longitude) * 108.0 / 360.0)
    return division % 12


def rank_seven_karakas(
    sidereal_longitudes: Mapping[str, float],
    *,
    tie_tolerance_degrees: float = 1e-12,
) -> tuple[str, ...]:
    """Rank exactly seven caller-selected bodies by descending within-sign degree.

    Exact/near ties fail closed because the retrieved evidence did not establish
    a transportable tie policy.  The returned first body is AtmaKaraka and the
    sixth is PutraKaraka for the tested rule.
    """

    if len(sidereal_longitudes) != 7:
        raise ValueError("exactly seven distinct bodies are required")
    tolerance = float(tie_tolerance_degrees)
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tie_tolerance_degrees must be finite and non-negative")
    degrees = {
        str(body): within_sign_degree(longitude)
        for body, longitude in sidereal_longitudes.items()
    }
    if any(not body.strip() for body in degrees):
        raise ValueError("body names must be non-empty")
    ordered = sorted(degrees, key=lambda body: (-degrees[body], body))
    for left, right in zip(ordered, ordered[1:], strict=False):
        if abs(degrees[left] - degrees[right]) <= tolerance:
            raise ValueError(
                "karaka rank is unresolved because within-sign degrees tie: "
                f"{left!r} and {right!r}"
            )
    return tuple(ordered)


def _is_kendra(sign_a: int, sign_b: int) -> bool:
    return (sign_b - sign_a) % 12 in KENDRA_OFFSETS


def karaka_kendra_feature(
    sidereal_longitudes: Mapping[str, float],
    *,
    tie_tolerance_degrees: float = 1e-12,
) -> KarakaKendraResult:
    """Calculate the unweighted D1-or-D9 AtmaKaraka/PutraKaraka kendra rule."""

    ranked = rank_seven_karakas(
        sidereal_longitudes,
        tie_tolerance_degrees=tie_tolerance_degrees,
    )
    atmakaraka = ranked[0]
    putrakaraka = ranked[5]
    atma_rasi = rasi_sign_index(sidereal_longitudes[atmakaraka])
    putra_rasi = rasi_sign_index(sidereal_longitudes[putrakaraka])
    atma_navamsa = navamsa_sign_index(sidereal_longitudes[atmakaraka])
    putra_navamsa = navamsa_sign_index(sidereal_longitudes[putrakaraka])
    rasi_match = _is_kendra(atma_rasi, putra_rasi)
    navamsa_match = _is_kendra(atma_navamsa, putra_navamsa)
    return KarakaKendraResult(
        atmakaraka_body=atmakaraka,
        putrakaraka_body=putrakaraka,
        atmakaraka_rasi_sign=atma_rasi,
        putrakaraka_rasi_sign=putra_rasi,
        atmakaraka_navamsa_sign=atma_navamsa,
        putrakaraka_navamsa_sign=putra_navamsa,
        kendra_in_rasi=rasi_match,
        kendra_in_navamsa=navamsa_match,
        kendra_in_either=rasi_match or navamsa_match,
    )
