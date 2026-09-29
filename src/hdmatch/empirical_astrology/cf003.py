"""Dormant development-only helpers for CF-003 adjusted planetary dominance.

This module reconstructs only the seven published predictor contributions that
can be stated exactly from the source articles. It does not reproduce the
chart-conditioned biographical target pipeline, does not implement the original
Mastro corpus, and is not part of LiteratureModelV1.

Scientific status:
- development/source-replay utility only;
- no production or prospective coefficient;
- no claim that the published null is valid;
- no activation without a new Pro decision.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

CF003_CANDIDATE_BODIES: Final[tuple[str, ...]] = (
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
)

CF003_PUBLISHED_WEIGHTS: Final[Mapping[str, float]] = MappingProxyType(
    {
        "major_aspect_to_moon": 8.3,
        "five_or_more_major_aspects": 8.2,
        "modern_ascendant_ruler": 7.6,
        "placidus_house_12": 5.3,
        "modern_descendant_ruler": 5.2,
        "major_aspect_to_ascendant": 4.7,
        "within_5deg_placidus_house_9_center": 1.9,
    }
)


@dataclass(frozen=True, slots=True)
class CF003FactorFlags:
    """Published binary predictor flags for one candidate planet."""

    major_aspect_to_moon: bool
    five_or_more_major_aspects: bool
    modern_ascendant_ruler: bool
    placidus_house_12: bool
    modern_descendant_ruler: bool
    major_aspect_to_ascendant: bool
    within_5deg_placidus_house_9_center: bool

    def __post_init__(self) -> None:
        for field_name, value in (
            ("major_aspect_to_moon", self.major_aspect_to_moon),
            ("five_or_more_major_aspects", self.five_or_more_major_aspects),
            ("modern_ascendant_ruler", self.modern_ascendant_ruler),
            ("placidus_house_12", self.placidus_house_12),
            ("modern_descendant_ruler", self.modern_descendant_ruler),
            ("major_aspect_to_ascendant", self.major_aspect_to_ascendant),
            ("within_5deg_placidus_house_9_center", self.within_5deg_placidus_house_9_center),
        ):
            if not isinstance(value, bool):
                raise TypeError(f"{field_name} must be bool")


@dataclass(frozen=True, slots=True)
class CF003PlanetScore:
    """Raw published-weight score for one candidate planet."""

    body: str
    total: float
    contributions: tuple[tuple[str, float], ...]


def score_cf003_planet(body: str, flags: CF003FactorFlags) -> CF003PlanetScore:
    """Return the raw seven-factor score without imposing a tie rule."""

    normalized = body.strip().lower()
    if normalized not in CF003_CANDIDATE_BODIES:
        raise ValueError(f"body must be one of {CF003_CANDIDATE_BODIES!r}")

    contributions: list[tuple[str, float]] = []
    total_tenths = 0
    for feature_name, weight in CF003_PUBLISHED_WEIGHTS.items():
        if getattr(flags, feature_name):
            contributions.append((feature_name, weight))
            total_tenths += int(round(weight * 10))

    return CF003PlanetScore(
        body=normalized,
        total=total_tenths / 10.0,
        contributions=tuple(contributions),
    )


def rank_cf003_planet_scores(
    scores: Mapping[str, float],
) -> tuple[tuple[str, ...], ...]:
    """Rank all ten candidate bodies while preserving unresolved ties."""

    normalized: dict[str, int] = {}
    for body, value in scores.items():
        key = body.strip().lower()
        if key in normalized:
            raise ValueError(f"duplicate candidate body after normalization: {key}")
        if key not in CF003_CANDIDATE_BODIES:
            raise ValueError(f"unexpected candidate body: {body}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"score for {body} must be finite")
        scaled = number * 10.0
        nearest = round(scaled)
        if not math.isclose(scaled, nearest, abs_tol=1e-7):
            raise ValueError(f"score for {body} must resolve to the published 0.1-point grid")
        normalized[key] = int(nearest)

    if set(normalized) != set(CF003_CANDIDATE_BODIES):
        missing = sorted(set(CF003_CANDIDATE_BODIES) - set(normalized))
        extra = sorted(set(normalized) - set(CF003_CANDIDATE_BODIES))
        raise ValueError(
            f"scores must contain all ten candidate bodies; missing={missing}, extra={extra}"
        )

    ordered = sorted(
        normalized.items(),
        key=lambda item: (-item[1], CF003_CANDIDATE_BODIES.index(item[0])),
    )
    groups: list[tuple[str, ...]] = []
    current_value: int | None = None
    current_group: list[str] = []

    for body, value in ordered:
        if current_value is None or value == current_value:
            current_group.append(body)
            current_value = value
            continue
        groups.append(tuple(current_group))
        current_group = [body]
        current_value = value

    groups.append(tuple(current_group))
    return tuple(groups)
