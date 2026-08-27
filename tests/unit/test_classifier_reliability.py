from __future__ import annotations

from hdmatch.evaluation.classifier_reliability import (
    ReliabilityRating,
    summarize_classifier_agreement,
)


def _rating(rater: str, label: str, *, post_reveal: bool = False) -> ReliabilityRating:
    return ReliabilityRating(
        evidence_id="e1",
        domain_id="profile",
        replicate_id=rater,
        rater_id=rater,
        rater_kind="blinded_human",
        classifier_version="codebook-v1",
        prompt_hash="0" * 64,
        evidence_hash="1" * 64,
        status="classified",
        primary_archetype=label,
        confidence=0.8,
        post_reveal=post_reveal,
    )


def test_agreement_excludes_post_reveal_and_never_changes_scoring() -> None:
    summary = summarize_classifier_agreement(
        (_rating("a", "1/3"), _rating("b", "1/3"), _rating("c", "2/4", post_reveal=True))
    )
    assert summary.rating_count == 2
    assert summary.pair_count == 1
    assert summary.exact_status_label_agreement == 1.0
    assert summary.fleiss_kappa == 1.0
    assert summary.excluded_post_reveal_count == 1
    assert not summary.confirmatory_scoring_changed
