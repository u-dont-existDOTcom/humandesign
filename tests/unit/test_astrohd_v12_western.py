from __future__ import annotations

import numpy as np
import pytest

from hdmatch.evaluation.astrohd_v12_western import (
    angular_separation,
    aspect_mask,
    assign_houses,
    score_western_candidate,
    score_western_universe,
    sign_mask,
)


def test_aspect_mask_uses_inclusive_three_degree_boundary() -> None:
    a = np.asarray([0.0, 0.0, 0.0])
    b = np.asarray([57.0, 56.999, 63.001])
    result = aspect_mask(a, b, angles=(60.0,), max_orb=3.0)
    assert result.tolist() == [True, False, False]


def test_angular_separation_wraps_at_zero() -> None:
    result = angular_separation(np.asarray([359.0]), np.asarray([1.0]))
    assert result.tolist() == [2.0]


def test_sign_mask_is_lower_inclusive_upper_exclusive() -> None:
    values = np.asarray([29.9999, 30.0, 59.9999, 60.0])
    assert sign_mask(values, 1).tolist() == [False, True, True, False]


def test_assign_houses_handles_wraparound_twelfth_house() -> None:
    cusps = np.asarray(
        [[0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0]]
    )
    assert assign_houses(np.asarray([345.0]), cusps).tolist() == [12]


def test_western_cluster_scoring_uses_best_path_not_sum() -> None:
    clusters = [
        {
            "id": "c",
            "wa": [
                ["a", 1.0, 1.0],
                ["b", 0.5, 1.0],
            ],
        }
    ]
    total, breakdown = score_western_candidate(
        feature_matches={"a": True, "b": True},
        feature_prevalence={"a": 0.25, "b": 0.125},
        clusters=clusters,
        behavioral_confidence={"c": 0.5},
    )
    assert total == pytest.approx(1.0)
    assert breakdown == {"c": pytest.approx(1.0)}


def test_universe_scoring_matches_scalar_candidates() -> None:
    clusters = [{"id": "c", "wa": [["a", 1.0, 1.0], ["b", 0.5, 1.0]]}]
    prevalence = {"a": 0.25, "b": 0.125}
    masks = {
        "a": np.asarray([True, False, True]),
        "b": np.asarray([False, True, True]),
    }
    vector = score_western_universe(
        feature_masks=masks,
        feature_prevalence=prevalence,
        clusters=clusters,
        behavioral_confidence={"c": 0.5},
    )
    scalar = []
    for index in range(3):
        total, _ = score_western_candidate(
            feature_matches={key: bool(mask[index]) for key, mask in masks.items()},
            feature_prevalence=prevalence,
            clusters=clusters,
            behavioral_confidence={"c": 0.5},
        )
        scalar.append(total)
    assert vector.tolist() == pytest.approx(scalar)
