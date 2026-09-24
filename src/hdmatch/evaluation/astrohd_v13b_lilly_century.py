"""Vectorized William Lilly source-native century scoring for AstroHD V1.3b."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np
from numpy.typing import NDArray

from hdmatch.evaluation.astrohd_v13_traditions import EXALTATIONS, FALLS, RULERS, SIGNS
from hdmatch.evaluation.astrohd_v13b_native import (
    LILLY_FACES,
    LILLY_HOUSE_POINTS,
    LILLY_TERMS,
    LILLY_TRIPLICITY,
    PLANETS,
    SIGN_ELEMENT,
)

PLANET_INDEX = {planet: index for index, planet in enumerate(PLANETS)}
SIGN_INDEX = {sign: index for index, sign in enumerate(SIGNS)}
SIGN_RULER_INDEX = np.asarray([PLANET_INDEX[RULERS[sign]] for sign in SIGNS], dtype=np.int8)
EXALTATION_SIGN_INDEX = {
    planet: SIGN_INDEX[EXALTATIONS[planet]] for planet in PLANETS
}
FALL_SIGN_INDEX = {planet: SIGN_INDEX[FALLS[planet]] for planet in PLANETS}
DETRIMENT_SIGN_INDICES = {
    planet: frozenset(
        (SIGN_INDEX[sign] + 6) % 12 for sign, ruler in RULERS.items() if ruler == planet
    )
    for planet in PLANETS
}
HOUSE_POINTS = np.asarray(
    [0.0] + [float(LILLY_HOUSE_POINTS.get(house, 0)) for house in range(1, 13)],
    dtype=np.float64,
)
NONLUMINARY_INDICES = frozenset(
    PLANET_INDEX[planet] for planet in ("mercury", "venus", "mars", "jupiter", "saturn")
)


def lilly_strength_arrays(
    *,
    longitudes: NDArray[np.float64],
    speeds: NDArray[np.float64],
    houses: NDArray[np.int16],
    day_chart: NDArray[np.bool_],
) -> NDArray[np.float64]:
    """Return Lilly core fortitude totals as shape (7, n)."""
    _validate_planet_arrays(longitudes, speeds, houses, day_chart)
    n = longitudes.shape[1]
    strengths = np.zeros((len(PLANETS), n), dtype=np.float64)

    sign_indices = np.floor((longitudes % 360.0) / 30.0).astype(np.int8)
    degrees = longitudes % 30.0
    term_rulers = _term_ruler_indices(sign_indices, degrees)
    face_rulers = _face_ruler_indices(sign_indices, degrees)
    triplicity_rulers = _triplicity_ruler_indices(sign_indices, day_chart)

    for planet_index, planet in enumerate(PLANETS):
        signs = sign_indices[planet_index]
        own = SIGN_RULER_INDEX[signs] == planet_index
        exalted = signs == EXALTATION_SIGN_INDEX[planet]
        triplicity = triplicity_rulers[planet_index] == planet_index
        term = term_rulers[planet_index] == planet_index
        face = face_rulers[planet_index] == planet_index
        dignified = own | exalted | triplicity | term | face

        strengths[planet_index] += own * 5.0
        strengths[planet_index] += exalted * 4.0
        strengths[planet_index] += triplicity * 3.0
        strengths[planet_index] += term * 2.0
        strengths[planet_index] += face * 1.0

        detriment = np.zeros(n, dtype=bool)
        for sign_index in DETRIMENT_SIGN_INDICES[planet]:
            detriment |= signs == sign_index
        strengths[planet_index] += detriment * -5.0
        strengths[planet_index] += (signs == FALL_SIGN_INDEX[planet]) * -4.0
        strengths[planet_index] += (~dignified) * -5.0
        strengths[planet_index] += HOUSE_POINTS[houses[planet_index]]

        if planet_index in NONLUMINARY_INDICES:
            strengths[planet_index] += np.where(
                speeds[planet_index] >= 0.0,
                4.0,
                -5.0,
            )

    return strengths


def lilly_universe_scores(
    *,
    strengths: NDArray[np.float64],
    cusp_longitudes: NDArray[np.float64],
    consensus_map: Mapping[str, Any],
    behavior_weights: Mapping[str, float],
    aggregation: str,
) -> NDArray[np.float64]:
    """Score all candidates for one frozen Lilly aggregation/behavior variant."""
    if strengths.ndim != 2 or strengths.shape[0] != len(PLANETS):
        raise ValueError("strengths must have shape (7, n)")
    if cusp_longitudes.shape != (strengths.shape[1], 12):
        raise ValueError("cusp_longitudes must have shape (n, 12)")
    if aggregation not in {"domain_mean_nonstack", "significator_stack"}:
        raise ValueError(f"unsupported aggregation: {aggregation}")

    n = strengths.shape[1]
    candidate_indices = np.arange(n)
    cusp_sign_indices = np.floor((cusp_longitudes % 360.0) / 30.0).astype(np.int8)
    house_lord_indices = SIGN_RULER_INDEX[cusp_sign_indices]
    total = np.zeros(n, dtype=np.float64)

    for domain in consensus_map["domains"]:
        domain_id = str(domain["domain_id"])
        weight = float(behavior_weights.get(domain_id, 0.0))
        if weight <= 0.0:
            continue
        mapping = next(
            row
            for row in domain["traditions"]
            if row["tradition"] == "lilly_traditional_western"
        )
        selected = np.zeros((len(PLANETS), n), dtype=bool)
        for row in mapping.get("planets", ()):
            selected[PLANET_INDEX[str(row["id"])], :] = True
        for row in mapping.get("houses", ()):
            house = int(row["id"])
            rulers = house_lord_indices[:, house - 1]
            selected[rulers, candidate_indices] = True

        counts = np.count_nonzero(selected, axis=0)
        mapped = counts > 0
        if not np.any(mapped):
            continue
        sums = np.sum(strengths * selected, axis=0)
        if aggregation == "domain_mean_nonstack":
            raw = np.zeros(n, dtype=np.float64)
            raw[mapped] = sums[mapped] / counts[mapped]
        else:
            raw = sums
        total += weight * raw

    return total


def _term_ruler_indices(
    sign_indices: NDArray[np.int8],
    degrees: NDArray[np.float64],
) -> NDArray[np.int8]:
    result = np.empty_like(sign_indices, dtype=np.int8)
    for sign_index, sign in enumerate(SIGNS):
        sign_mask = sign_indices == sign_index
        if not np.any(sign_mask):
            continue
        assigned = np.zeros(sign_indices.shape, dtype=bool)
        lower = 0.0
        for upper, ruler in LILLY_TERMS[sign]:
            mask = sign_mask & (degrees >= lower) & (degrees < upper)
            result[mask] = PLANET_INDEX[ruler]
            assigned |= mask
            lower = float(upper)
        if not np.all(assigned[sign_mask]):
            raise RuntimeError(f"unassigned Lilly term degrees for {sign}")
    return result


def _face_ruler_indices(
    sign_indices: NDArray[np.int8],
    degrees: NDArray[np.float64],
) -> NDArray[np.int8]:
    result = np.empty_like(sign_indices, dtype=np.int8)
    decan = np.minimum(2, np.floor(degrees / 10.0).astype(np.int8))
    for sign_index, sign in enumerate(SIGNS):
        for face_index, ruler in enumerate(LILLY_FACES[sign]):
            mask = (sign_indices == sign_index) & (decan == face_index)
            result[mask] = PLANET_INDEX[ruler]
    return result


def _triplicity_ruler_indices(
    sign_indices: NDArray[np.int8],
    day_chart: NDArray[np.bool_],
) -> NDArray[np.int8]:
    result = np.empty_like(sign_indices, dtype=np.int8)
    for sign_index, sign in enumerate(SIGNS):
        element = SIGN_ELEMENT[sign]
        day_ruler = PLANET_INDEX[LILLY_TRIPLICITY[element]["day"]]
        night_ruler = PLANET_INDEX[LILLY_TRIPLICITY[element]["night"]]
        for planet_index in range(len(PLANETS)):
            mask = sign_indices[planet_index] == sign_index
            result[planet_index, mask] = np.where(
                day_chart[mask],
                day_ruler,
                night_ruler,
            )
    return result


def _validate_planet_arrays(
    longitudes: NDArray[np.float64],
    speeds: NDArray[np.float64],
    houses: NDArray[np.int16],
    day_chart: NDArray[np.bool_],
) -> None:
    if longitudes.ndim != 2 or longitudes.shape[0] != len(PLANETS):
        raise ValueError("longitudes must have shape (7, n)")
    if speeds.shape != longitudes.shape:
        raise ValueError("speeds shape must match longitudes")
    if houses.shape != longitudes.shape:
        raise ValueError("houses shape must match longitudes")
    if day_chart.shape != (longitudes.shape[1],):
        raise ValueError("day_chart must have shape (n,)")
