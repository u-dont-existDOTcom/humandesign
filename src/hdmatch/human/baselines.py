"""Non-HD baselines required before any human-validity claim."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from typing import Any

from hdmatch.human.dataset import HumanCase


def permute_chart_assignments(cases: Sequence[HumanCase], seed: int) -> dict[str, dict[str, Any]]:
    """Permute complete chart records across people without splitting a person."""

    identifiers = [case.participant_id for case in cases]
    features = [dict(case.chart_features) for case in cases]
    random.Random(seed).shuffle(features)
    return dict(zip(identifiers, features, strict=True))


def uniform_date_prior(candidate_dates: Sequence[str]) -> dict[str, float]:
    if not candidate_dates:
        raise ValueError("candidate date universe cannot be empty")
    probability = 1.0 / len(candidate_dates)
    return {candidate: probability for candidate in candidate_dates}


def calendar_features(year: int, month: int, day: int) -> Mapping[str, int]:
    """Raw calendar controls deliberately contain no HD chart features."""

    return {"year": year, "month": month, "day": day, "season_quarter": (month - 1) // 3 + 1}
