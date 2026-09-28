"""Mechanically specified empirical-astrology calculation primitives.

This package contains no feature-selection, weighting, scoring, or scientific
adjudication.  A frozen Pro decision is required before these primitives may be
assembled into a literature-derived model.
"""

from .geometry import (
    AspectPhase,
    aspect_phase_from_forward_step,
    distance_to_aspect,
    minimum_axis_distance,
    near_time_distance_minutes,
    unsigned_angular_separation,
)
from .karaka import (
    KarakaKendraResult,
    karaka_kendra_feature,
    navamsa_sign_index,
    rank_seven_karakas,
    rasi_sign_index,
    within_sign_degree,
)

__all__ = [
    "AspectPhase",
    "KarakaKendraResult",
    "aspect_phase_from_forward_step",
    "distance_to_aspect",
    "karaka_kendra_feature",
    "minimum_axis_distance",
    "navamsa_sign_index",
    "near_time_distance_minutes",
    "rank_seven_karakas",
    "rasi_sign_index",
    "unsigned_angular_separation",
    "within_sign_degree",
]
