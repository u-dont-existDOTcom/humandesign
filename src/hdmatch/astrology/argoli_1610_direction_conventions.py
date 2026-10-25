"""Bounded 1610 Argoli source-arithmetic and converse-role comparison.

Based on original 1610 printed chapters XIV–XVI (BSB leaves 55–59),
compared to original 1667 printed chapters XVI–XVII (Michigan leaves 44–46).

What the 1610 converse passage establishes:
- Use a promissor position circle, not the significator's, when directing
  converse (p47); compare opposite right/oblique ascensional coordinates.

This module uses the existing Regiomontanian research geometry under swapped
roles as an *experimental operationalization* of that statement. It is NOT
an independently authenticated full Argoli/Lilly timing algorithm and has
no human birth or event semantics.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .geometry import EquatorialPoint, GeometryMethod, direction_arc


def wrapped_source_arc(minuend: tuple[int, int], subtrahend: tuple[int, int]) -> tuple[int, int]:
    """Exact source-compatible 360° borrowing for extended oblique descension.

    Original p44/p31 may express 21°20′ but explicitly add 360 degrees
    before subtracting 340°03′. An extended 381°20′ works identically.
    Does NOT choose a converse time-key or reinterpret original readings.
    """
    vals = (*minuend, *subtrahend)
    if any(type(v) is not int for v in vals):
        raise ValueError("original source integer D/M operands required")
    if not (0 <= minuend[0] <= 720 and 0 <= subtrahend[0] <= 720):
        raise ValueError("extended positive source degrees must be 0..720")
    if not (0 <= minuend[1] < 60 and 0 <= subtrahend[1] < 60):
        raise ValueError("minute component outside source's 0..59 range")
    minutes = ((minuend[0] * 60 + minuend[1]) - (subtrahend[0] * 60 + subtrahend[1])) % (360 * 60)
    return divmod(minutes, 60)


def angular_separation_deg(first: float, second: float) -> float:
    if not math.isfinite(first) or not math.isfinite(second):
        raise ValueError("finite directions required")
    return abs((first - second + 180.0) % 360.0 - 180.0)


@dataclass(frozen=True, slots=True)
class ConversaResearchComparison:
    direct_using_significator_circle_deg: float
    converse_using_promissor_circle_deg: float
    naive_360_minus_direct_deg: float
    absolute_difference_converse_vs_naive_deg: float
    method: str = "regiomontanian_position_circle"
    historical_source: str = "Argoli 1610 p47, Caput XVI, promissor position circle"
    authenticity: str = "SOURCE_MOTIVATED_RESEARCH_VARIANT_NOT_COMPLETE_ARGOLI"
    human_prediction_accuracy: str = "UNTESTED"

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)


def source_motivated_converse_comparison(
    latitude_deg: float,
    ramc_deg: float,
    significator: EquatorialPoint,
    promissor: EquatorialPoint,
) -> ConversaResearchComparison:
    """Compare role-swap under the promissor circle vs naive arc reversal.

    Geometry convention follows the modern implementation's own fully
    specified position-circle model, not the whole historical radix/timing
    conventions. This does not assert that every planet is eligible for
    converse according to Argoli's conditional original p47 language.
    """
    method = GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE
    direct = direction_arc(method, latitude_deg, ramc_deg, significator, promissor)
    switched = direction_arc(method, latitude_deg, ramc_deg, promissor, significator)
    naive = (360.0 - direct) % 360.0
    return ConversaResearchComparison(
        direct_using_significator_circle_deg=direct,
        converse_using_promissor_circle_deg=switched,
        naive_360_minus_direct_deg=naive,
        absolute_difference_converse_vs_naive_deg=angular_separation_deg(switched, naive),
    )
