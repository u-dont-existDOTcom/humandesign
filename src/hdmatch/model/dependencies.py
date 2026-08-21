"""Dependency controls preventing repeated symbolic evidence from multiplying."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from hdmatch.model.mapping_library import MappingLibrary


@dataclass(frozen=True, slots=True)
class ClusterContribution:
    cluster_id: str
    mapping_id: str
    anchor_id: str
    effective_confidence: float
    support: float
    evidence_rubric_bits: float
    contradiction_severity: float
    contradiction_rubric_bits: float


def validate_dependency_control(library: MappingLibrary) -> None:
    """Require every exact structural anchor to live in one dependency cluster.

    Repeated questions may reference an anchor, but they must collapse into the same
    cluster. A complete channel/gate implementation can extend this invariant later
    without changing the scoring contract.
    """

    clusters_by_anchor: dict[str, set[str]] = defaultdict(set)
    for mapping in library.frozen_mappings:
        clusters_by_anchor[mapping.anchor_id].add(mapping.dependency_cluster)
    violations = {
        anchor: sorted(clusters)
        for anchor, clusters in clusters_by_anchor.items()
        if len(clusters) > 1
    }
    if violations:
        raise ValueError(f"structural anchors reused across dependency clusters: {violations}")


def collapse_dependency_clusters(
    contributions: Iterable[ClusterContribution],
) -> tuple[ClusterContribution, ...]:
    """Keep one alternative pathway per cluster, deterministically.

    Support pathways compete. Contradictions are also capped to the strongest instance
    in a repeated cluster, preventing paraphrases from multiplying one conflict.
    """

    grouped: dict[str, list[ClusterContribution]] = defaultdict(list)
    for contribution in contributions:
        grouped[contribution.cluster_id].append(contribution)

    collapsed: list[ClusterContribution] = []
    for cluster_id in sorted(grouped):
        values = grouped[cluster_id]
        support_winner = min(
            values,
            key=lambda item: (-item.evidence_rubric_bits, -item.support, item.mapping_id),
        )
        contradiction_winner = min(
            values,
            key=lambda item: (
                -item.contradiction_rubric_bits,
                -item.contradiction_severity,
                item.mapping_id,
            ),
        )
        identity_winner = (
            support_winner if support_winner.evidence_rubric_bits > 0.0 else contradiction_winner
        )
        collapsed.append(
            ClusterContribution(
                cluster_id=cluster_id,
                mapping_id=identity_winner.mapping_id,
                anchor_id=identity_winner.anchor_id,
                effective_confidence=max(item.effective_confidence for item in values),
                support=support_winner.support,
                evidence_rubric_bits=support_winner.evidence_rubric_bits,
                contradiction_severity=contradiction_winner.contradiction_severity,
                contradiction_rubric_bits=contradiction_winner.contradiction_rubric_bits,
            )
        )
    return tuple(collapsed)
