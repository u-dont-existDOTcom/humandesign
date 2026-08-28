"""Human Design partnership/connection mechanics.

This package is intentionally separate from natal reverse-matching scoring.
"""

from .analysis import (
    CardinalActivation,
    CenterConfigurationKeynote,
    ConnectionChannel,
    ConnectionKind,
    PartnershipAnalysis,
    PartnershipSnapshot,
    SunEarthNodeAlignment,
    analyze_partnership,
    snapshot_from_chart,
)
from .questionnaire import (
    RelationshipQuestion,
    RelationshipQuestionnaireSpec,
    load_relationship_questionnaire,
    question_by_id,
    select_next_capture_question,
    select_next_validation_question,
)
from .uncertain_time import (
    AnalyzedPartnershipInterval,
    PartnerTimeCandidate,
    UncertainPartnerTimeSummary,
    summarize_uncertain_partner_time,
)

__all__ = [
    "AnalyzedPartnershipInterval",
    "CardinalActivation",
    "CenterConfigurationKeynote",
    "ConnectionChannel",
    "ConnectionKind",
    "PartnerTimeCandidate",
    "PartnershipAnalysis",
    "PartnershipSnapshot",
    "RelationshipQuestion",
    "RelationshipQuestionnaireSpec",
    "SunEarthNodeAlignment",
    "UncertainPartnerTimeSummary",
    "analyze_partnership",
    "load_relationship_questionnaire",
    "question_by_id",
    "select_next_capture_question",
    "select_next_validation_question",
    "snapshot_from_chart",
    "summarize_uncertain_partner_time",
]
