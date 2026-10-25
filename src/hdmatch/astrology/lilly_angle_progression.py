"""Restricted original Lilly 1647 ascending-coordinate direction examples.

Page 515: MC directions computed as promissor RA minus RAMC.
Page 517: Ascendant progression computed from oblique ascensions.
This does NOT claim the entire Argolus method, full natal rotation
convention, or every possible converse/lunar-latitude case is known.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from enum import StrEnum


class AngularAxis(StrEnum):
    MC_RIGHT_ASCENSION = "mc_right_ascension"
    ASC_OBLIQUE_ASCENSION = "asc_oblique_ascension"


@dataclass(frozen=True, slots=True)
class ProgressionArc:
    axis: str
    significator_coordinate_deg: float
    promissor_coordinate_deg: float
    forward_source_arc_degrees: float
    original_printed_page: int
    semantic_status: str = "SOURCE_ASCENDING_COORDINATE_ARITHMETIC_ONLY"

    def to_dict(self) -> dict[str, str | float | int]:
        return asdict(self)


def source_forward_angular_arc(
    axis: AngularAxis,
    significator_coordinate_deg: float,
    promissor_coordinate_deg: float,
) -> ProgressionArc:
    """Forward succession of coordinate, exactly p.515 MC / p.517 Asc.

    Input oblique ascensions must already be established by a separately
    authenticated source method; this function doesn't invent them.
    Do not call the shorter reverse arc a source-defined converse
    without independent documentary confirmation.
    """
    axis = AngularAxis(axis)
    for num in (significator_coordinate_deg, promissor_coordinate_deg):
        if not math.isfinite(num) or not 0.0 <= num < 360.0:
            raise ValueError("right/oblique ascension must be finite [0,360)")
    diff = (promissor_coordinate_deg - significator_coordinate_deg) % 360.0
    return ProgressionArc(
        axis=axis.value,
        significator_coordinate_deg=significator_coordinate_deg,
        promissor_coordinate_deg=promissor_coordinate_deg,
        forward_source_arc_degrees=diff,
        original_printed_page=515 if axis is AngularAxis.MC_RIGHT_ASCENSION else 517,
    )
