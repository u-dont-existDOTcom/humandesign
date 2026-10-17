"""Partial deterministic Zi Wei Quan Shu mechanics, NOT a full natal chart.

Primary source: 紫微斗數全書, 卷二 安身命例 and 起五行寅例.
Inputs are ALREADY converted to source-convention lunar month and branch.
No civil-to-lunar converter, birth-hour normalization, bureau, or stars.
"""

from __future__ import annotations

BRANCHES = (
    "Zi",
    "Chou",
    "Yin",
    "Mao",
    "Chen",
    "Si",
    "Wu",
    "Wei",
    "Shen",
    "You",
    "Xu",
    "Hai",
)
STEMS = ("Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui")
LIFE_BODY_START = BRANCHES.index("Yin")
YEAR_PAIR_FIRST_YIN_STEM = {
    "Jia": "Bing",
    "Ji": "Bing",
    "Yi": "Wu",
    "Geng": "Wu",
    "Bing": "Geng",
    "Xin": "Geng",
    "Ding": "Ren",
    "Ren": "Ren",
    "Wu": "Jia",
    "Gui": "Jia",
}
TWELVE_PALACES_OLD_LABELS = (
    "Life",
    "Siblings",
    "Wives/Concubines",
    "Children",
    "Wealth",
    "Illness",
    "Travel",
    "Servants",
    "Career",
    "Property",
    "Fortune",
    "Parents",
)


def life_and_body_palaces(
    lunar_month: int,
    birth_hour_branch: str,
    *,
    is_leap_month: bool = False,
    leap_rule: str = "quan_shu_as_next",
) -> tuple[str, str]:
    """Original Quan Shu: month forward from Yin, Life backward, Body forward.

    For a leap month, transmitted original text treats the leap month as
    the next month in the palace-setting mnemonic, not a universal rule
    accepted by all Zi Wei lineages. This explicitly chooses ONE version.
    """
    if lunar_month not in range(1, 13):
        raise ValueError("Need normalized lunar month 1..12")
    h = BRANCHES.index(birth_hour_branch)
    if leap_rule != "quan_shu_as_next":
        raise ValueError("Unimplemented leap-month convention")
    normalized = (lunar_month % 12) + 1 if is_leap_month else lunar_month
    month_anchor = (LIFE_BODY_START + normalized - 1) % 12
    return BRANCHES[(month_anchor - h) % 12], BRANCHES[(month_anchor + h) % 12]


def yin_palace_first_stem(birth_year_stem: str) -> str:
    """First palace stem of Yin for pairs Jia/Ji, Yi/Geng, ... per 卷二."""
    return YEAR_PAIR_FIRST_YIN_STEM[birth_year_stem]


def palace_stem_from_yin(birth_year_stem: str, palace_branch: str) -> str:
    """Only Year-Stem->palace-stem mechanical sequence; no stars placed."""
    start = STEMS.index(yin_palace_first_stem(birth_year_stem))
    offset = (BRANCHES.index(palace_branch) - LIFE_BODY_START) % 12
    return STEMS[(start + offset) % 10]


ENGINE_SCOPE = {
    "gregorian_to_lunar_conversion": False,
    "precise_birth_hour_or_time_zone_resolution": False,
    "complete_star_placement": False,
    "four_transformations": False,
    "luck_cycles": False,
    "person_level_forecasts": False,
    "life_body_and_palace_stem_partial_mechanics": True,
    "independent_human_validations": 0,
    "runtime_promotions": 0,
}
