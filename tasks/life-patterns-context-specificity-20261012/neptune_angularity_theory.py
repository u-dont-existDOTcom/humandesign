"""Historic angular-Neptune hypothesis: geometry only, never a behavioral diagnosis."""

from __future__ import annotations

import math
from dataclasses import dataclass

HISTORICAL_SOURCE = "Heindel & Heindel, The Message of the Stars (1918), Chapter IV"
DEFAULT_ORB_DEGREES = 6.0


@dataclass(frozen=True)
class AngularNeptuneResult:
    qualified: bool
    signed_before_ascendant_degrees: float
    actual_house: int
    maximum_orb_degrees: float
    interpretive_status: str = "THEORY_ONLY_NOT_PREDICTIVE_EVIDENCE"


def twelfth_side_neptune_near_ascendant(
    ascendant_tropical_longitude: float,
    neptune_tropical_longitude: float,
    neptune_placidus_house: int,
    maximum_orb_degrees: float = DEFAULT_ORB_DEGREES,
) -> AngularNeptuneResult:
    """Apply exactly the historic twelfth-house six-degree Ascendant convention.

    A *behind-Ascendant* placement means Neptune's ecliptic longitude occurs
    shortly BEFORE the Ascendant's longitude (modulo 360). This function also
    requires an independently calculated 12th Placidus house assignment, and
    should never be used as a substitute for a validated house calculator.

    It returns geometry, not a spiritual, substance-use or clinical prediction.
    """
    values = [ascendant_tropical_longitude, neptune_tropical_longitude, maximum_orb_degrees]
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError("Longitude and orb must be finite numbers.")
    if maximum_orb_degrees <= 0 or maximum_orb_degrees >= 30:
        raise ValueError("Orb must be positive and less than 30 degrees.")
    if not (1 <= int(neptune_placidus_house) <= 12):
        raise ValueError("House must be 1..12.")
    if not isinstance(neptune_placidus_house, int):
        raise ValueError("House must be an integer.")
    gap = (ascendant_tropical_longitude - neptune_tropical_longitude) % 360.0
    qualifies = neptune_placidus_house == 12 and gap <= maximum_orb_degrees
    return AngularNeptuneResult(
        qualified=qualifies,
        signed_before_ascendant_degrees=gap,
        actual_house=neptune_placidus_house,
        maximum_orb_degrees=maximum_orb_degrees,
    )
