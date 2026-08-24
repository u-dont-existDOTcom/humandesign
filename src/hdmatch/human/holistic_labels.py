"""Dependency-aware weighting for observed positive behavior labels."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
import math


def cluster_normalized_evidence_weights(
    observed_labels: Sequence[str],
    *,
    label_clusters: Mapping[str, str],
    reliability_weights: Mapping[str, float] | None = None,
) -> dict[str, float]:
    """Return per-label weights capped to one unit per dependency cluster.

    Closely related observations may all be retained for specificity, but their
    total possible contribution is normalized by the number of observed labels
    in that cluster.  Optional reliability weights then reduce (never increase)
    individual contributions.

    A label absent from ``label_clusters`` forms its own singleton cluster.
    """

    labels = tuple(dict.fromkeys(label.strip() for label in observed_labels if label.strip()))
    reliabilities = reliability_weights or {}
    unknown = set(reliabilities) - set(labels)
    if unknown:
        raise ValueError(f"reliability supplied for unobserved labels: {sorted(unknown)}")
    invalid = sorted(
        label
        for label, value in reliabilities.items()
        if not math.isfinite(value) or not 0.0 <= value <= 1.0
    )
    if invalid:
        raise ValueError(f"reliability weights must be within [0, 1]: {invalid}")

    clusters = {
        label: str(label_clusters.get(label, label))
        for label in labels
    }
    counts = Counter(clusters.values())
    return {
        label: float(reliabilities.get(label, 1.0)) / counts[clusters[label]]
        for label in labels
    }
