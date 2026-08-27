from pathlib import Path

from hdmatch.model.evidence_registry import EvidenceClass, load_evidence_registry
from hdmatch.model.rich_predicate import ActivationGatePredicate, ChannelPredicate


def test_seed_evidence_registry_is_typed_and_hashable() -> None:
    registry = load_evidence_registry(
        Path("reference/core/mapping_v2_candidate_claims.json")
    )

    assert len(registry.candidates) == 4
    assert len(registry.sha256) == 64
    assert registry.sha256 == registry.sha256
    assert all(
        candidate.source.class_ is EvidenceClass.OFFICIAL_HD_PRIMARY
        for candidate in registry.candidates
    )

    moon = registry.candidates[0]
    assert isinstance(moon.predicate, ActivationGatePredicate)
    assert moon.predicate.gates == (53,)
    assert moon.predicate.bodies == ("moon",)

    channel = registry.candidates[1]
    assert isinstance(channel.predicate, ChannelPredicate)
    assert channel.predicate.channels == ("16-48",)
