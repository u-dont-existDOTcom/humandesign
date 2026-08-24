from __future__ import annotations

import pytest

from hdmatch.human.holistic_labels import cluster_normalized_evidence_weights


def test_correlated_labels_share_one_cluster_unit() -> None:
    weights = cluster_normalized_evidence_weights(
        ("actor", "tv_actor", "writer"),
        label_clusters={
            "actor": "entertainment",
            "tv_actor": "entertainment",
            "writer": "writing",
        },
    )
    assert weights["actor"] == pytest.approx(0.5)
    assert weights["tv_actor"] == pytest.approx(0.5)
    assert weights["writer"] == pytest.approx(1.0)


def test_reliability_can_reduce_but_not_inflate_cluster_weight() -> None:
    weights = cluster_normalized_evidence_weights(
        ("a", "b"),
        label_clusters={"a": "same", "b": "same"},
        reliability_weights={"a": 0.8, "b": 0.4},
    )
    assert weights == pytest.approx({"a": 0.4, "b": 0.2})
    assert sum(weights.values()) <= 1.0


def test_unknown_reliability_label_is_rejected() -> None:
    with pytest.raises(ValueError, match="unobserved"):
        cluster_normalized_evidence_weights(
            ("a",),
            label_clusters={},
            reliability_weights={"b": 1.0},
        )
