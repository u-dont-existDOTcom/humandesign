"""Candidate-blind classifier reliability records and agreement summaries."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


ClassificationStatus = Literal[
    "classified", "mixed", "other", "insufficient_evidence", "unclassifiable"
]
RaterKind = Literal["same_model_repeat", "cross_model", "blinded_human"]


class ReliabilityRating(_FrozenModel):
    """One sealed classification; candidate/chart fields are intentionally absent."""

    evidence_id: str = Field(min_length=1)
    domain_id: str = Field(min_length=1)
    replicate_id: str = Field(min_length=1)
    rater_id: str = Field(min_length=1)
    rater_kind: RaterKind
    classifier_version: str = Field(min_length=1)
    prompt_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    evidence_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    status: ClassificationStatus
    primary_archetype: str | None = None
    secondary_archetypes: tuple[str, ...] = ()
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_spans: tuple[str, ...] = ()
    counterevidence_spans: tuple[str, ...] = ()
    context_notes: str = ""
    blinded_to_candidate: Literal[True] = True
    confirmatory_score_frozen: Literal[True] = True
    post_reveal: bool = False


class AgreementSummary(_FrozenModel):
    schema_version: str = "survey-v2-classifier-reliability-v1"
    rating_count: int = Field(ge=0)
    item_count: int = Field(ge=0)
    pair_count: int = Field(ge=0)
    exact_status_label_agreement: float | None = Field(default=None, ge=0.0, le=1.0)
    status_agreement: float | None = Field(default=None, ge=0.0, le=1.0)
    fleiss_kappa: float | None = Field(default=None, ge=-1.0, le=1.0)
    excluded_post_reveal_count: int = Field(ge=0)
    confirmatory_scoring_changed: Literal[False] = False


def summarize_classifier_agreement(
    ratings: Sequence[ReliabilityRating],
) -> AgreementSummary:
    """Summarize repeated ratings without feeding agreement back into scoring."""
    included = [rating for rating in ratings if not rating.post_reveal]
    groups: dict[tuple[str, str], list[ReliabilityRating]] = defaultdict(list)
    for rating in included:
        groups[(rating.evidence_id, rating.domain_id)].append(rating)
    pairs = 0
    exact = 0
    status = 0
    for group in groups.values():
        for left_index, left in enumerate(group):
            for right in group[left_index + 1 :]:
                pairs += 1
                status += int(left.status == right.status)
                exact += int(_category(left) == _category(right))
    kappa = _fleiss_kappa(tuple(groups.values()))
    return AgreementSummary(
        rating_count=len(included),
        item_count=len(groups),
        pair_count=pairs,
        exact_status_label_agreement=(exact / pairs if pairs else None),
        status_agreement=(status / pairs if pairs else None),
        fleiss_kappa=kappa,
        excluded_post_reveal_count=len(ratings) - len(included),
    )


def _category(rating: ReliabilityRating) -> str:
    label = rating.primary_archetype if rating.status in {"classified", "mixed"} else None
    return f"{rating.status}:{label or '-'}"


def _fleiss_kappa(groups: Sequence[Sequence[ReliabilityRating]]) -> float | None:
    eligible = [group for group in groups if len(group) >= 2]
    if not eligible or len({len(group) for group in eligible}) != 1:
        return None
    n = len(eligible[0])
    categories = sorted({_category(rating) for group in eligible for rating in group})
    observed = 0.0
    totals: Counter[str] = Counter()
    for group in eligible:
        counts = Counter(_category(rating) for rating in group)
        observed += sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))
        totals.update(counts)
    observed /= len(eligible)
    denominator = len(eligible) * n
    expected = sum((totals[category] / denominator) ** 2 for category in categories)
    if expected == 1.0:
        return 1.0 if observed == 1.0 else None
    return (observed - expected) / (1.0 - expected)
