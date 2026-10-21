"""Research-only *symbolic attribute* subset of Tibetan calendar formulae.

Source: Svante Janson (2014), "Tibetan calendar mathematics", §5.2,
Appendix E.1–E.3, A.2; Cornu (1997 English) printed pp. 49–52, 115–119.

Deliberate exclusion: This module does NOT convert a UTC/civil birth time
to a Tibetan calendar date, compute Losar, a tithi from planetary
longitude, a Julian-day calendar-day feature, or validate astrology.
Every caller must supply a verified Tibetan year label (year of Losar),
lunar month (1–12), lunar day (1–30), or named traditional hour.
"""
from __future__ import annotations

from typing import Literal

ELEMENTS: tuple[str, ...] = ("wood", "fire", "earth", "iron", "water")
ANIMALS: tuple[str, ...] = (
    "mouse", "ox", "tiger", "hare", "dragon", "snake",
    "horse", "sheep", "monkey", "bird", "dog", "pig",
)
TRIGRAMS: tuple[str, ...] = (
    "Li", "Khon", "Dwa", "Khen", "Kham", "Gin", "Zin", "Zon",
)
HOURS_FROM_HARE: tuple[str, ...] = (
    "hare", "dragon", "snake", "horse", "sheep", "monkey",
    "bird", "dog", "pig", "mouse", "ox", "tiger",
)
Policy = Literal["phugpa", "tsurphu"]

EPOCH_BETA: dict[str, dict[int, int]] = {
    "phugpa": {806: 61, 1927: 55, 1987: 0},
    "tsurphu": {1732: 59, 1852: 14},
}

LIFE_FROM_ANIMAL = {
    "mouse": "water", "ox": "earth", "tiger": "wood",
    "hare": "wood", "dragon": "earth", "snake": "fire",
    "horse": "fire", "sheep": "earth", "monkey": "iron",
    "bird": "iron", "dog": "earth", "pig": "water",
}
FORTUNE_FROM_ANIMAL = {
    "mouse": "wood", "dragon": "wood", "monkey": "wood",
    "ox": "water", "snake": "water", "bird": "water",
    "tiger": "iron", "horse": "iron", "dog": "iron",
    "hare": "fire", "sheep": "fire", "pig": "fire",
}
BODY_REFERENCE = {
    "mouse": "wood", "horse": "wood", "ox": "wood", "sheep": "wood",
    "tiger": "water", "monkey": "water", "hare": "water", "bird": "water",
    "dragon": "iron", "dog": "iron", "snake": "iron", "pig": "iron",
}
BODY_FOR_DIFFERENCE = ("iron", "water", "fire", "earth", "wood")


def _integer(value: object, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer, not {type(value).__name__}")
    return value


def amod(n: int, modulus: int) -> int:
    """Janson's 1-based modulus. Defined for negative integers too."""
    _integer(n, "n")
    if _integer(modulus, "modulus") <= 0:
        raise ValueError("modulus must be positive")
    return 1 + ((n - 1) % modulus)


def _policy(name: str) -> str:
    if name not in EPOCH_BETA:
        raise ValueError("policy must explicitly be 'phugpa' or 'tsurphu'")
    return name


def _month(m: int) -> int:
    m = _integer(m, "lunar month")
    if not 1 <= m <= 12:
        raise ValueError("Tibetan lunar month must be 1–12")
    return m


def _year(y: int) -> int:
    return _integer(y, "Tibetan year start label")


def year_features(year_start_label: int) -> dict[str, object]:
    """Janson E.1; year label = Gregorian year in which Losar *begins*.

    This does not discover Losar. Applying Gregorian civil year directly to a
    timestamp before Losar would be an invalid use of these formulas.
    """
    y = _year(year_start_label)
    idx = (y - 4) % 60  # 1984 = Wood Mouse, Chinese sexagenary position 1
    animal = ANIMALS[idx % 12]
    power = ELEMENTS[(idx // 2) % 5]
    life = LIFE_FROM_ANIMAL[animal]
    fortune = FORTUNE_FROM_ANIMAL[animal]
    intermediate = BODY_REFERENCE[animal]
    difference = (ELEMENTS.index(power) - ELEMENTS.index(intermediate)) % 5
    return {
        "year_start_label": y,
        "sexagenary_position": idx + 1,
        "animal": animal,
        "polarity": "masculine" if idx % 2 == 0 else "feminine",
        "power_element": power,
        "life_element": life,
        "body_element": BODY_FOR_DIFFERENCE[difference],
        "fortune_element": fortune,
        "spirit_element": ELEMENTS[(ELEMENTS.index(life) - 1) % 5],
        "central_mewa": amod(2 - y, 9),
        "life_mewa": amod(8 - y, 9),
        "power_mewa": amod(5 - y, 9),
    }


def month_features(
    year_start_label: int, lunar_month: int, *, policy: Policy
) -> dict[str, object]:
    """Janson E.2. Only month labels; not Gregorian date conversion."""
    y, m = _year(year_start_label), _month(lunar_month)
    p = _policy(policy)
    animal = ANIMALS[(m + (3 if p == "phugpa" else 1)) % 12]
    if p == "phugpa":
        if m <= 10:
            elm = amod(-(-(y - 1) // 2) + (m + 1) // 2, 5)
        else:
            elm = amod(-(-y // 2) + (m - 11) // 2, 5)
        mewa = None  # Not specified as a month number for Phugpa in E.2
    else:
        elm = amod(y - 2 + (m - 1) // 2, 5)
        mewa = amod(3 - (12 * y + m), 9)  # E.8, Tsurphu only
    return {
        "year_start_label": y, "month": m, "policy": p,
        "animal": animal, "polarity": "masculine" if m % 2 else "feminine",
        "element": ELEMENTS[elm - 1], "element_index": elm,
        "tsurphu_month_mewa": mewa,
    }


def lunar_day_features(
    year_start_label: int, lunar_month: int, lunar_day: int, *, policy: Policy
) -> dict[str, object]:
    """Janson E.9–E.11; lunar *day* is not the civil/calendar day."""
    m = month_features(year_start_label, lunar_month, policy=policy)
    d = _integer(lunar_day, "lunar day")
    if not 1 <= d <= 30:
        raise ValueError("lunar day must be 1–30")
    animal_i = amod(d + 6 * lunar_month + 8, 12)
    month_animal_i = ANIMALS.index(str(m["animal"])) + 1
    elem_i = amod(int(m["element_index"]) + d, 5)
    return {
        "lunar_day": d,
        "animal": ANIMALS[animal_i - 1],
        "element": ELEMENTS[elem_i - 1],
        "trigram": TRIGRAMS[amod(d + 6 * month_animal_i + 6, 8) - 1],
        "mewa": amod(d + 3 * month_animal_i, 9),
        "calendar_day_equivalent_not_established": True,
    }


def leap_month_info(
    year_start_label: int, lunar_month: int, *, policy: Policy,
    epoch: int
) -> dict[str, int | bool | None | str]:
    """Janson §5.2, Appendix A.2: *month numbering*, not actual date.

    Phugpa: index 48/49 leap, first occurrence count floor, second ceil.
    Tsurphu: index 0/1 leap, first count floor-1, second floor.
    """
    y, m = _year(year_start_label), _month(lunar_month)
    p = _policy(policy)
    e = _integer(epoch, "epoch")
    if e not in EPOCH_BETA[p]:
        raise ValueError(f"unsupported epoch for {p}: {e}")
    mstar = 12 * (y - e) + m - 3
    k, ix = divmod(67 * mstar + EPOCH_BETA[p][e], 65)
    if p == "phugpa":
        leap = ix in (48, 49)
        regular = k if ix < 48 else k + 1
        leap_count = k if leap else None
    else:
        leap = ix in (0, 1)
        regular = k
        leap_count = k - 1 if leap else None
    return {
        "year_start_label": y, "month": m,
        "policy": p, "epoch": e,
        "solar_month_offset": mstar,
        "preliminary_intercalation_index": ix,
        "leap_month_present": leap,
        "regular_true_month_count": regular,
        "leap_true_month_count": leap_count,
    }


def hour_element_from_day(day_element: str, traditional_hour_animal: str) -> str:
    """Cornu: Hare hour is *son* of the lunar-day element, then advances.

    This is NOT a clock→hour-animal/timezone or tithi→calendar-day converter.
    """
    if day_element not in ELEMENTS:
        raise ValueError("day element must be one of five named elements")
    if traditional_hour_animal not in HOURS_FROM_HARE:
        raise ValueError("traditional animal double-hour must be supplied")
    element_offset = (1 + HOURS_FROM_HARE.index(traditional_hour_animal)) % 5
    return ELEMENTS[(ELEMENTS.index(day_element) + element_offset) % 5]


def calendar_day_features(julian_day_number: int, *, policy: Policy) -> dict[str, object]:
    """Janson E.4, given an already-resolved Tibetan *calendar-day JDN*.

    IMPORTANT: JDN is a fixed integer calendar date, not Julian Date (a
    floating-point UTC instant), and the Tibetan day starts at dawn.
    We DO NOT solve the UTC instant or local sunrise boundary here.

    Tsurphu assigns its daily mewa around solstices with a reversal; that
    mewa is deliberately left unknown, not replaced with Phugpa's.
    """
    j = _integer(julian_day_number, "Julian day number")
    p = _policy(policy)
    # ceil(j / 2) in integer arithmetic, also well-defined for BCE values.
    element_i = amod(-(-j // 2), 5)
    animal_i = amod(j + 2, 12)
    trigram_i = amod(j + 2, 8)
    num = amod(-j, 9) if p == "phugpa" else None

    # Janson Remark 36: JDN's 60-day element+animal pair is row
    # amod(JDN - 10, 60) of Table 23.
    row_zero_based = amod(j - 10, 60) - 1
    one_cycle_year = year_features(1984 + row_zero_based)
    assert ELEMENTS[element_i - 1] == one_cycle_year["power_element"]
    assert ANIMALS[animal_i - 1] == one_cycle_year["animal"]
    return {
        "julian_day_number": j,
        "policy": p,
        "power_element": ELEMENTS[element_i - 1],
        "animal": ANIMALS[animal_i - 1],
        "polarity": "masculine" if j % 2 else "feminine",
        "trigram": TRIGRAMS[trigram_i - 1],
        "mewa": num,
        "tsurphu_mewa_requires_solstice_rule": p == "tsurphu",
        "life_element": one_cycle_year["life_element"],
        "body_element": one_cycle_year["body_element"],
        "fortune_element": one_cycle_year["fortune_element"],
        "spirit_element": one_cycle_year["spirit_element"],
        "civil_datetime_to_tibetan_day_unresolved": True,
    }
