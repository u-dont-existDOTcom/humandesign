"""Bounded Lilly II.XXVII references, not a forecast or a frame selector.

Source: the 1647 Wellcome b30338724 witness, PDF pages 201 and 207–210.
The functions implement only the explicitly named source profiles. They do
not choose a question frame from a chart, resolve undefined timing thresholds,
or convert symbolic time into a civil date.
"""

from fractions import Fraction
from types import MappingProxyType


SOURCE_ID = "LILLY1647_WELLCOME_B30338724"
WEALTH_TIMING_PROFILE = "LILLY_II_XXVII_WEALTH_HOUSE_PAIRS"
LONG_BUSINESS_NOTE = (
    "long business may warrant years, threshold undefined, not chosen here"
)
ZODIAC = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
_SIGN_INDEX = MappingProxyType({sign: index for index, sign in enumerate(ZODIAC)})
_FRAMES = MappingProxyType({
    "general_wealth": (None, None, (201,), None),
    "ordinary_specific_counterparty": (
        7, 8, (207, 208), "comparable ordinary parties"
    ),
    "powerful_superior_payment": (
        10, 11, (208, 209), "querent much inferior to payment source"
    ),
})
_HOUSE_KINDS = frozenset(("cadent", "succedent", "angular"))
_PAIR_UNITS = MappingProxyType({
    ("cadent", "cadent"): "days",
    ("succedent", "succedent"): "weeks",
    ("angular", "angular"): "months",
    ("angular", "succedent"): "months",
    ("angular", "cadent"): "months",
    ("cadent", "succedent"): "weeks",
})


def _integer(value: int, name: str, *, minimum: int, maximum=None) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer, excluding booleans")
    if value < minimum or (maximum is not None and value > maximum):
        bounds = f"{minimum} or greater" if maximum is None else f"{minimum}..{maximum}"
        raise ValueError(f"{name} must be {bounds}")
    return value


def query_frame(name: str) -> dict:
    """Return a selected source frame; the caller must choose its question first."""
    if not isinstance(name, str):
        raise TypeError("name must be an explicit source frame name")
    if name not in _FRAMES:
        raise ValueError(f"unknown query frame: {name!r}")
    other, money, pages, precondition = _FRAMES[name]
    result = {
        "profile": name,
        "source_id": SOURCE_ID,
        "querent_house": 1,
        "querent_money_house": 2,
        "counterparty_house": other,
        "counterparty_money_house": money,
        "pages": list(pages),
        "is_forecast": False,
    }
    if precondition is not None:
        result["precondition"] = precondition
    return result


def wealth_symbolic_interval(
    distance_arcminutes: int,
    first_house_kind: str,
    second_house_kind: str,
    *,
    profile: str,
) -> dict:
    """Return exact degrees with the named wealth profile's symbolic unit.

    House pairs are unordered. This is not an elapsed astronomical interval;
    the caller must supply a previously established nonnegative source distance.
    The source's undefined long-business override is retained but never selected.
    """
    if profile != WEALTH_TIMING_PROFILE:
        raise ValueError(f"profile must be {WEALTH_TIMING_PROFILE!r}")
    distance = _integer(distance_arcminutes, "distance_arcminutes", minimum=0)
    for name, kind in (
        ("first_house_kind", first_house_kind),
        ("second_house_kind", second_house_kind),
    ):
        if not isinstance(kind, str):
            raise TypeError(f"{name} must be an explicit house category")
        if kind not in _HOUSE_KINDS:
            raise ValueError(f"unknown {name}: {kind!r}")
    pair = tuple(sorted((first_house_kind, second_house_kind)))
    return {
        "profile": profile,
        "source_id": SOURCE_ID,
        "distance_arcminutes": distance,
        "interval": str(Fraction(distance, 60)),
        "unit": _PAIR_UNITS[pair],
        "pages": [209, 210],
        "civil_dates_computed": False,
        "is_forecast": False,
        "source_note": LONG_BUSINESS_NOTE,
    }


def degree(sign: str, degrees: int, minutes: int) -> int:
    """Convert an explicit zodiac sign, 0..29 degrees and 0..59 minutes to arcminutes.

    No out-of-range position, rounded degree, or absent minute is normalized.
    """
    if not isinstance(sign, str):
        raise TypeError("sign must be an explicit canonical zodiac sign name")
    if sign not in _SIGN_INDEX:
        raise ValueError(f"unknown zodiac sign: {sign!r}")
    degrees = _integer(degrees, "degrees", minimum=0, maximum=29)
    minutes = _integer(minutes, "minutes", minimum=0, maximum=59)
    return _SIGN_INDEX[sign] * 1800 + degrees * 60 + minutes
