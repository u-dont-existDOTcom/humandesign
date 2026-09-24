"""Transparent Western feature predicates for AstroHD V1.2 development experiments."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np


def angular_separation(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    raw = np.abs(np.mod(a - b, 360.0))
    return np.minimum(raw, 360.0 - raw)


def aspect_mask(
    a: np.ndarray,
    b: np.ndarray,
    *,
    angles: Sequence[float],
    max_orb: float,
) -> np.ndarray:
    sep = angular_separation(a, b)
    distance = np.minimum.reduce([np.abs(sep - angle) for angle in angles])
    return distance <= max_orb


def sign_mask(longitudes: np.ndarray, sign_index: int) -> np.ndarray:
    values = np.mod(longitudes, 360.0)
    lo = sign_index * 30.0
    hi = lo + 30.0
    return (values >= lo) & (values < hi)


def assign_houses(longitudes: np.ndarray, cusps: np.ndarray) -> np.ndarray:
    """Assign each longitude to one of 12 circular cusp intervals."""
    if cusps.ndim != 2 or cusps.shape[1] != 12:
        raise ValueError("cusps must have shape (N, 12)")
    if len(longitudes) != len(cusps):
        raise ValueError("longitude/cusp row counts differ")
    values = np.mod(longitudes, 360.0)
    houses = np.zeros(len(values), dtype=np.int8)
    for index in range(12):
        start = np.mod(cusps[:, index], 360.0)
        end = np.mod(cusps[:, (index + 1) % 12], 360.0)
        ordinary = start < end
        inside = np.where(
            ordinary,
            (values >= start) & (values < end),
            (values >= start) | (values < end),
        )
        houses[(houses == 0) & inside] = index + 1
    if np.any(houses == 0):
        raise RuntimeError("at least one longitude could not be assigned to a house")
    return houses


def feature_mask(
    feature_id: str,
    *,
    registry: Mapping[str, Any],
    longitudes: Mapping[str, np.ndarray],
    houses: Mapping[str, np.ndarray],
    ascendant: np.ndarray,
    midheaven: np.ndarray,
) -> np.ndarray:
    spec = registry["features"][feature_id]
    kind = spec["type"]
    orb = float(registry["aspects"]["max_orb_degrees"])
    aspect_angles = registry["aspects"]["allowed"]
    if kind == "pair_any_major":
        a, b = spec["bodies"]
        return aspect_mask(
            longitudes[a],
            longitudes[b],
            angles=tuple(float(value) for value in aspect_angles.values()),
            max_orb=orb,
        )
    if kind == "pair_hard":
        a, b = spec["bodies"]
        return aspect_mask(
            longitudes[a],
            longitudes[b],
            angles=(0.0, 90.0, 180.0),
            max_orb=orb,
        )
    if kind == "sign":
        return sign_mask(longitudes[spec["body"]], _sign_index(spec["sign"]))
    if kind == "asc_sign":
        return sign_mask(ascendant, _sign_index(spec["sign"]))
    if kind == "house":
        return houses[spec["body"]] == int(spec["house"])
    if kind == "angular_house":
        return np.isin(houses[spec["body"]], np.asarray((1, 4, 7, 10), dtype=np.int8))
    if kind == "mc_conjunction":
        return angular_separation(longitudes[spec["body"]], midheaven) <= orb
    if kind == "all_of":
        masks = [
            feature_mask(
                component,
                registry=registry,
                longitudes=longitudes,
                houses=houses,
                ascendant=ascendant,
                midheaven=midheaven,
            )
            for component in spec["predicates"]
        ]
        return np.logical_and.reduce(masks)
    raise ValueError(f"unsupported Western predicate type: {kind}")


def score_western_universe(
    *,
    feature_masks: Mapping[str, np.ndarray],
    feature_prevalence: Mapping[str, float],
    clusters: Sequence[Mapping[str, Any]],
    behavioral_confidence: Mapping[str, float],
) -> np.ndarray:
    if not feature_masks:
        raise ValueError("feature_masks must not be empty")
    lengths = {len(mask) for mask in feature_masks.values()}
    if len(lengths) != 1:
        raise ValueError("all feature masks must have equal length")
    scores = np.zeros(lengths.pop(), dtype=np.float64)
    for cluster in clusters:
        cluster_id = str(cluster["id"])
        confidence = float(behavioral_confidence.get(cluster_id, 0.0))
        if confidence <= 0.0:
            continue
        cluster_scores = np.zeros_like(scores)
        for feature_id, salience, directness in cluster.get("wa", ()):
            feature_id = str(feature_id)
            prevalence = float(feature_prevalence[feature_id])
            if not 0.0 < prevalence <= 1.0:
                raise ValueError(f"invalid prevalence for {feature_id}: {prevalence}")
            info_bits = min(6.0, -math.log2(prevalence))
            value = confidence * float(salience) * float(directness) * info_bits
            cluster_scores = np.maximum(
                cluster_scores,
                np.where(feature_masks[feature_id], value, 0.0),
            )
        scores += cluster_scores
    return scores


def score_western_candidate(
    *,
    feature_matches: Mapping[str, bool],
    feature_prevalence: Mapping[str, float],
    clusters: Sequence[Mapping[str, Any]],
    behavioral_confidence: Mapping[str, float],
) -> tuple[float, dict[str, float]]:
    breakdown: dict[str, float] = {}
    for cluster in clusters:
        cluster_id = str(cluster["id"])
        confidence = float(behavioral_confidence.get(cluster_id, 0.0))
        if confidence <= 0.0:
            breakdown[cluster_id] = 0.0
            continue
        best = 0.0
        for feature_id, salience, directness in cluster.get("wa", ()):
            if not feature_matches.get(str(feature_id), False):
                continue
            prevalence = float(feature_prevalence[str(feature_id)])
            if not 0.0 < prevalence <= 1.0:
                raise ValueError(f"invalid prevalence for {feature_id}: {prevalence}")
            info_bits = min(6.0, -math.log2(prevalence))
            best = max(
                best,
                confidence * float(salience) * float(directness) * info_bits,
            )
        breakdown[cluster_id] = best
    return sum(breakdown.values()), breakdown


def _sign_index(name: str) -> int:
    names = (
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "leo",
        "virgo",
        "libra",
        "scorpio",
        "sagittarius",
        "capricorn",
        "aquarius",
        "pisces",
    )
    try:
        return names.index(name)
    except ValueError as exc:
        raise ValueError(f"unknown zodiac sign: {name}") from exc
