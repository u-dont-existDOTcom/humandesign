"""Historical Zi Wei Quan Shu Volume II Life/Body Lords and textual taxonomy.

This is a bounded SOURCE-CONVENTION transcription: no Gregorian-to-Chinese
calendar, no twenty-eight mansion, no full 14-star layout, no personal fortune
forecast, no inferred modern gender rules. Inputs must be pre-resolved.
Exact source revision oldid1963110, raw SHA-256
1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72.
"""

from __future__ import annotations

from quan_shu_vol2_placements import BRANCHES

SOURCE_LIFE_LORD_BY_LIFE_PALACE = {
    "Zi": "贪狼",
    "Chou": "巨门",
    "Yin": "禄存",
    "Mao": "文曲",
    "Chen": "廉真",
    "Si": "武曲",
    "Wu": "破军",
    "Wei": "武曲",
    "Shen": "廉真",
    "You": "文曲",
    "Xu": "禄存",
    "Hai": "巨门",
}
SOURCE_BODY_LORD_BY_NATAL_YEAR = {
    "Zi": "火玲星",
    "Chou": "天相",
    "Yin": "天梁",
    "Mao": "天同",
    "Chen": "文昌",
    "Si": "天机",
    "Wu": "火玲星",
    "Wei": "天相",
    "Shen": "天梁",
    "You": "天同",
    "Xu": "文昌",
    "Hai": "天机",
}
ORIGINAL_BODY_LORD_AMBIGUOUS_LABEL = "火玲星"
IDLE_SOURCE_PALACES = {
    "紫微": ("Zi", "Chen", "Hai"),
    "贪狼": ("Yin", "Chen"),
    "天相": ("Chen", "Xu"),
    "七杀": ("Chen", "Hai"),
    "天梁": ("Si", "You"),
    "天机": ("Si",),
    "破军": ("Si", "Shen"),
    "武曲": ("Shen",),
}
HISTORIC_CHILD_AGE_PALACES = {
    1: "命",
    2: "财",
    3: "疾厄",
    4: "妻",
    5: "福",
    6: "官禄",
    15: "命",
}
STAR_ELEMENT_LABELS_18_TRANSMITTED = {
    "紫微": ("Earth",),
    "天机": ("Wood",),
    "禄存": ("Earth",),
    "太阳": ("Fire",),
    "天同": ("Water", "Metal"),
    "廉真": ("Fire",),
    "武曲": ("Metal",),
    "天府": ("Earth",),
    "太阴": ("Water",),
    "贪狼": ("Water", "Wood"),
    "巨门": ("Water",),
    "天相": ("Water",),
    "天梁": ("Earth",),
    "七杀": ("Fire", "Metal"),
    "破军": ("Water",),
    "文昌": ("Metal",),
    "文曲": ("Water",),
    "辅弼二星": None,
}
TEXTUAL_ELEMENT_RESTRAINTS = {
    ("Metal", "Fire"),
    ("Fire", "Water"),
    ("Water", "Earth"),
    ("Earth", "Wood"),
}


def _branch(branch: str) -> str:
    if branch not in BRANCHES:
        raise ValueError("Required original lunar year or Life-palace Earthly Branch")
    return branch


def source_life_lord_star_label(natal_life_palace_branch: str) -> str:
    """Chosen star name; not its current chart position."""
    return SOURCE_LIFE_LORD_BY_LIFE_PALACE[_branch(natal_life_palace_branch)]


def source_life_lord_actual_palace(
    natal_life_palace_branch: str,
    independently_verified_star_palaces: dict[str, str],
) -> str:
    """Require externally computed actual selected star position, not Life palace."""
    chosen = source_life_lord_star_label(natal_life_palace_branch)
    if not isinstance(independently_verified_star_palaces, dict):
        raise ValueError("Externally verified Chinese star positions are required")
    palace = independently_verified_star_palaces.get(chosen)
    if palace not in BRANCHES:
        raise ValueError("Actual chosen star position is not yet verified")
    return palace


def source_body_lord_star_label(natal_year_branch: str) -> dict[str, object]:
    """Keep the ambiguous historical 子午 火玲星 source glyph literal."""
    label = SOURCE_BODY_LORD_BY_NATAL_YEAR[_branch(natal_year_branch)]
    return {
        "original_chinese_label": label,
        "raw_text_star_identification_ambiguous": label == ORIGINAL_BODY_LORD_AMBIGUOUS_LABEL,
        "chart_palace_not_computed": True,
        "independently_validated_personality_or_event_prediction": False,
    }


def source_idle_palace_branches(star_chinese_name: str) -> tuple[str, ...]:
    if star_chinese_name not in IDLE_SOURCE_PALACES:
        raise ValueError("The source section lists only eight idle-star cases")
    return IDLE_SOURCE_PALACES[star_chinese_name]


def source_child_limit_palace(historical_age: int) -> str:
    if type(historical_age) is not int or historical_age not in HISTORIC_CHILD_AGE_PALACES:
        raise ValueError("Source explicitly supports only ages one-six and age fifteen")
    return HISTORIC_CHILD_AGE_PALACES[historical_age]


def source_ji_chou_year_annual_example(stem: str, branch: str) -> dict[str, str]:
    """ONE original example, not an algorithm for arbitrary calendar years."""
    if (stem, branch) != ("Ji", "Chou"):
        raise ValueError("Only the original Ji-Chou annual example is documented")
    return {"FlowLu": "Wu", "FlowYang": "Wei", "FlowTuo": "Si"}


def source_classifies_element_as_restrained(star_element: str, palace_element: str) -> bool | None:
    """True for four explicit source combinations, None for all unlisted pairs."""
    valid = {"Metal", "Fire", "Water", "Earth", "Wood"}
    if star_element not in valid or palace_element not in valid:
        raise ValueError("Unknown element labels")
    if (star_element, palace_element) in TEXTUAL_ELEMENT_RESTRAINTS:
        return True
    return None


def source_star_element_labels(star_chinese_name: str) -> tuple[str, ...] | None:
    """The transmitted text prints some mixed categories, Fu/Bi no elements."""
    if star_chinese_name not in STAR_ELEMENT_LABELS_18_TRANSMITTED:
        raise ValueError("Star is outside the source's eighteen enumeration")
    return STAR_ELEMENT_LABELS_18_TRANSMITTED[star_chinese_name]


def source_limits() -> dict[str, object]:
    return {
        "source_pinned_raw_revision": 1963110,
        "literal_1647_or_Ming_imprint_verified": False,
        "full_14_main_star_placement_engine_verified": False,
        "chinese_solar_terms_and_leap_month_calendar_verified": False,
        "hour_boundary_and_true_solar_time_verified": False,
        "natal_life_body_star_chart_locations_computed_without_external_positions": False,
        "historical_sex_and_death_omensation_validated": False,
        "source_eighteen_list_is_the_same_as_modern_fourteen_main_stars": False,
        "real_human_predictive_successes": 0,
        "runtime_promotions": 0,
    }
