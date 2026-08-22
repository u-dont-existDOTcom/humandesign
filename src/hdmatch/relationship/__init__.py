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
    "SunEarthNodeAlignment",
    "UncertainPartnerTimeSummary",
    "analyze_partnership",
    "snapshot_from_chart",
    "summarize_uncertain_partner_time",
]
