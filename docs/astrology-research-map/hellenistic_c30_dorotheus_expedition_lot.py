"""C30: Dorothean Lot of Expedition (one-directional historical claim).

Documentary arithmetic only. Not a modern professional recommendation,
historical military appraisal, human forecast, or production scoring model.

Greek source: Dorotheus fragment preserved by Hephaistio II.19; calculate
zodiacal distance SATURN -> MOON, projected from ASCENDANT.
Only a lot in Aries/Scorpio/Capricorn/Aquarius is affirmatively designated
"campaigning" by the recovered verse. The converse is NOT stated.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Iterable

ZODIAC = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
CAMPAIGN_INDICATOR_SIGNS = frozenset(
    {"Aries", "Scorpio", "Capricorn", "Aquarius"}
)
FULL_CIRCLE = Decimal("360")
SIGN_ARC = Decimal("30")


def _longitude(value: int | float | Decimal | str) -> Decimal:
    """Require exact documented longitudes; do not truncate/normalize bad input."""
    if isinstance(value, bool) or not isinstance(
        value, (int, float, Decimal, str)
    ):
        raise ValueError("longitude needs numeric input, not bool/unknown object")
    if isinstance(value, str) and not value.strip():
        raise ValueError("empty longitude string")
    try:
        out = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid longitude input") from exc
    if not out.is_finite() or not Decimal(0) <= out < FULL_CIRCLE:
        raise ValueError("longitude must be finite within [0,360) degrees")
    return out


def lot_of_expedition(
    *, ascendant: int | float | Decimal | str,
    saturn: int | float | Decimal | str,
    moon: int | float | Decimal | str,
) -> Decimal:
    """Historical forward arc: (ASC + (MOON - SATURN)) mod 360.

    Source verse contains no night-specific direction reversal. Inputs must
    already be astronomically verified geocentric ecliptic longitudes (ASC is
    a geographic angle). This function neither computes nor verifies charts.
    """
    a, s, m = (_longitude(ascendant), _longitude(saturn), _longitude(moon))
    return (a + ((m - s) % FULL_CIRCLE + FULL_CIRCLE) % FULL_CIRCLE) % FULL_CIRCLE


def lot_sign(lot: int | float | Decimal | str) -> str:
    """Twelve 30-degree zodiac signs, lower-inclusive, upper-exclusive."""
    return ZODIAC[int(_longitude(lot) // SIGN_ARC)]


def documentary_claim(
    *, ascendant: int | float | Decimal | str,
    saturn: int | float | Decimal | str,
    moon: int | float | Decimal | str,
) -> dict:
    """Return one-way positive condition; all other signs are unknown, not negative."""
    value = lot_of_expedition(ascendant=ascendant, saturn=saturn, moon=moon)
    sign = lot_sign(value)
    enabled = sign in CAMPAIGN_INDICATOR_SIGNS
    return {
        "lot_degrees": str(value),
        "lot_sign": sign,
        "source_positive_condition": enabled,
        "source_claim_status": (
            "SOURCE_PREDICTS_MILITARY_CAMPAIGN" if enabled
            else "NO_POSITIVE_CLAIM_FROM_THIS_CONDITION"
        ),
        "not_source_claiming_no_campaign_when_false": True,
        "translation_is_ancient_context_not_verified_modern_outcome": True,
        "historical_source_reference": "DOROTHEUS_HEPHAISTIO_II_19",
        "research_only": True,
        "human_predictive_validation": False,
    }


def sampled_birth_uncertainty(
    samples: Iterable[tuple[int | float | Decimal | str,
                            int | float | Decimal | str,
                            int | float | Decimal | str]],
) -> dict:
    """Inspect a FINITE set of supplied (ASC, Saturn, Moon) samples.

    Agreement at sample points never certifies stability over a continuous
    birth-time interval; that requires separate astronomical boundary proof.
    """
    observed = [documentary_claim(ascendant=a, saturn=s, moon=m)
                for a, s, m in samples]
    if not observed:
        raise ValueError("at least one sampled chart is required")
    statuses = {x["source_positive_condition"] for x in observed}
    return {
        "samples_count": len(observed),
        "sampled_lot_signs": sorted(set(x["lot_sign"] for x in observed)),
        "sampled_condition_values": sorted(statuses),
        "sampled_condition_consistent": len(statuses) == 1,
        "certified_full_birth_interval_stability": False,
        "unobserved_intermediate_crossings_excluded": False,
        "eligible_for_prospective_claim_freeze": False,
    }
