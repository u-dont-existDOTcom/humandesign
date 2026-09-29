from __future__ import annotations

import math

import pytest

from hdmatch.empirical_astrology.cf003 import (
    CF003_CANDIDATE_BODIES,
    CF003_PUBLISHED_WEIGHTS,
    CF003FactorFlags,
    rank_cf003_planet_scores,
    score_cf003_planet,
)


def _flags(**overrides: bool) -> CF003FactorFlags:
    values = {name: False for name in CF003_PUBLISHED_WEIGHTS}
    values.update(overrides)
    return CF003FactorFlags(**values)


def test_cf003_published_weights_are_frozen() -> None:
    assert dict(CF003_PUBLISHED_WEIGHTS) == {
        "major_aspect_to_moon": 8.3,
        "five_or_more_major_aspects": 8.2,
        "modern_ascendant_ruler": 7.6,
        "placidus_house_12": 5.3,
        "modern_descendant_ruler": 5.2,
        "major_aspect_to_ascendant": 4.7,
        "within_5deg_placidus_house_9_center": 1.9,
    }
    assert math.isclose(sum(CF003_PUBLISHED_WEIGHTS.values()), 41.2)


@pytest.mark.parametrize("feature_name,weight", CF003_PUBLISHED_WEIGHTS.items())
def test_each_cf003_flag_contributes_only_its_published_weight(
    feature_name: str,
    weight: float,
) -> None:
    score = score_cf003_planet("mars", _flags(**{feature_name: True}))
    assert score.total == weight
    assert score.contributions == ((feature_name, weight),)


def test_cf003_all_flags_sum_without_extra_terms() -> None:
    score = score_cf003_planet(
        "jupiter",
        CF003FactorFlags(**{name: True for name in CF003_PUBLISHED_WEIGHTS}),
    )
    assert math.isclose(score.total, 41.2)
    assert len(score.contributions) == 7


def test_cf003_ranking_preserves_ties_instead_of_inventing_tiebreaker() -> None:
    scores = {body: float(index) for index, body in enumerate(CF003_CANDIDATE_BODIES)}
    scores["mars"] = 100.0
    scores["venus"] = 100.0
    ranked = rank_cf003_planet_scores(scores)
    assert ranked[0] == ("venus", "mars")


def test_cf003_ranking_requires_exact_ten_body_surface() -> None:
    with pytest.raises(ValueError, match="all ten"):
        rank_cf003_planet_scores({"mars": 1.0})


def test_cf003_rejects_non_boolean_feature_flags() -> None:
    with pytest.raises(TypeError, match="must be bool"):
        CF003FactorFlags(
            major_aspect_to_moon=1,  # type: ignore[arg-type]
            five_or_more_major_aspects=False,
            modern_ascendant_ruler=False,
            placidus_house_12=False,
            modern_descendant_ruler=False,
            major_aspect_to_ascendant=False,
            within_5deg_placidus_house_9_center=False,
        )
