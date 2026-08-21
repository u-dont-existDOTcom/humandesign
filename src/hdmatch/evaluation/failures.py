"""Evidence-based oracle failure labels required by the acceptance protocol."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FailureClassification(StrEnum):
    STRUCTURALLY_INDISTINGUISHABLE = "structurally_indistinguishable"
    MISSING_MAPPING = "missing_mapping"
    SEARCH_BUG = "search_bug"
    SCORING_BUG = "scoring_bug"
    AGGREGATION_AMBIGUITY = "aggregation_ambiguity"


class FailureRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    classification: FailureClassification
    explanation: str = Field(min_length=1)
    evidence: dict[str, Any]


def classify_oracle_failure(
    *,
    case_id: str,
    true_candidate_present: bool,
    unresolved_mapping_ids: tuple[str, ...] = (),
    structurally_identical_top_candidate: bool = False,
    state_winner_but_date_loser: bool = False,
    scoring_reference_disagreement: bool = False,
    evidence: dict[str, Any] | None = None,
) -> FailureRecord:
    """Classify by explicit diagnostic evidence, using protocol-defined labels only."""

    details = dict(evidence or {})
    if not true_candidate_present:
        classification = FailureClassification.SEARCH_BUG
        explanation = (
            "The candidate universe or search output omitted the concealed true date/state."
        )
    elif unresolved_mapping_ids:
        classification = FailureClassification.MISSING_MAPPING
        explanation = "One or more required symbolic mappings were explicitly unresolved."
        details["unresolved_mapping_ids"] = sorted(unresolved_mapping_ids)
    elif structurally_identical_top_candidate:
        classification = FailureClassification.STRUCTURALLY_INDISTINGUISHABLE
        explanation = "The winning alternative is identical under all frozen scored features."
    elif state_winner_but_date_loser:
        classification = FailureClassification.AGGREGATION_AMBIGUITY
        explanation = (
            "State-level evidence recovered the truth but the frozen date aggregation did not."
        )
    else:
        classification = FailureClassification.SCORING_BUG
        explanation = (
            "No search, missing-mapping, structural-tie, or aggregation explanation was "
            "established; "
            "the remaining protocol category is scoring behavior requiring investigation."
        )
        details["scoring_reference_disagreement"] = scoring_reference_disagreement
    return FailureRecord(
        case_id=case_id,
        classification=classification,
        explanation=explanation,
        evidence=details,
    )
