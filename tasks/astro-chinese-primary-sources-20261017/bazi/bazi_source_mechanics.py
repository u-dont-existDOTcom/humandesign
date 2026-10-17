"""Bounded deterministic BaZi source mechanics, NOT predictive natal astrology.

Source: Joey Yap, The Destiny Code (2005), printed pp 21-100;
The Destiny Code Revealed (2006), pp 82-98.
Lacks Gregorian->sexagenary calendar calculations, precision solar terms,
ten-god strength, hidden-stem weighting and any empirically validated forecasts.
"""

from __future__ import annotations

STEMS = ("Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui")
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
PHASES = ("Wood", "Fire", "Earth", "Metal", "Water")
PHASE_BY_STEM = dict(zip(STEMS, (p for p in PHASES for _ in range(2)), strict=True))
SAN_HE = {
    frozenset(("Shen", "Zi", "Chen")): "Water",
    frozenset(("Hai", "Mao", "Wei")): "Wood",
    frozenset(("Yin", "Wu", "Xu")): "Fire",
    frozenset(("Si", "You", "Chou")): "Metal",
}
SAN_HUI = {
    frozenset(("Yin", "Mao", "Chen")): "Spring",
    frozenset(("Si", "Wu", "Wei")): "Summer",
    frozenset(("Shen", "You", "Xu")): "Autumn",
    frozenset(("Hai", "Zi", "Chou")): "Winter",
}


def heavenly_stem_polarity(stem: str) -> str:
    """Year polarity for author-defined historical luck-direction rule."""
    return "Yang" if STEMS.index(stem) % 2 == 0 else "Yin"


def two_hour_branch(hour: int, minute: int = 0) -> str:
    """Source-defined 2h clock branch, no true-solar-time adjustment."""
    if not 0 <= hour < 24 or not 0 <= minute < 60:
        raise ValueError("Invalid civil time")
    return BRANCHES[((hour + 1) % 24) // 2]


def hour_pillar_from_day_stem(
    day_stem: str,
    hour: int,
    minute: int = 0,
    *,
    late_zi_policy: str = "joey_yap_book1_next_day_hour_stem",
) -> tuple[str, str]:
    """Compute HOUR pillar only, assuming a separately verified DAY stem.

    In Book 1, 23:00-23:59 retains current calendar day but uses the
    next day-stem hour-stem group. The competing day-change-at-23:00
    method must not be silently substituted.
    """
    day_index = STEMS.index(day_stem)
    branch = two_hour_branch(hour, minute)
    if hour == 23:
        if late_zi_policy != "joey_yap_book1_next_day_hour_stem":
            raise ValueError("Alternate late Zi chronology not implemented")
        day_index = (day_index + 1) % 10
    else:
        if late_zi_policy != "joey_yap_book1_next_day_hour_stem":
            raise ValueError("Alternate late Zi chronology not implemented")
    first_zi_stem = 2 * (day_index % 5)
    branch_index = BRANCHES.index(branch)
    return STEMS[(first_zi_stem + branch_index) % 10], branch


def traditional_luck_direction(year_stem: str, source_sex_code: str) -> str:
    """Source-specific 2005 male/female convention, not gender inference."""
    if source_sex_code not in {"M", "F"}:
        raise ValueError("Source supplies only M/F; no silent gender inference")
    yang = heavenly_stem_polarity(year_stem) == "Yang"
    forward = (source_sex_code == "M") == yang
    return "forward" if forward else "reverse"


def decade_luck_start_age(nearest_term_distance_in_whole_days: int) -> int:
    """Source approximate age = directional civil-day count / 3, nearest integer."""
    if not 0 <= nearest_term_distance_in_whole_days <= 33:
        raise ValueError("Distance is expected 0-33 days; verify actual term")
    return (2 * nearest_term_distance_in_whole_days + 3) // 6


def next_luck_pillar(
    month_stem: str, month_branch: str, direction: str, offset: int
) -> tuple[str, str]:
    """Moves both stem and branch in same direction, skips no cycles."""
    sign = {"forward": 1, "reverse": -1}.get(direction)
    if sign is None or not isinstance(offset, int) or offset <= 0:
        raise ValueError("Invalid direction/offset")
    return (
        STEMS[(STEMS.index(month_stem) + sign * offset) % 10],
        BRANCHES[(BRANCHES.index(month_branch) + sign * offset) % 12],
    )


def five_factor(day_stem: str, observed_phase: str) -> str:
    """Source's five factors; does NOT grade strength or predict behavior."""
    day_phase = PHASE_BY_STEM[day_stem]
    self_index, observed_index = PHASES.index(day_phase), PHASES.index(observed_phase)
    delta = (observed_index - self_index) % 5
    return {
        0: "Companion",
        1: "Output",
        2: "Wealth",
        3: "Influence",
        4: "Resource",
    }[delta]


def san_he_complete(*branches: str) -> str | None:
    """Full traditional Three Harmony only. No partial or silent push."""
    for branch in branches:
        if branch not in BRANCHES:
            raise ValueError(f"Unknown branch: {branch}")
    return SAN_HE.get(frozenset(branches)) if len(branches) == 3 else None


def san_hui_complete(*branches: str) -> str | None:
    """Full Directional Three meeting from Book 2."""
    for branch in branches:
        if branch not in BRANCHES:
            raise ValueError(f"Unknown branch: {branch}")
    return SAN_HUI.get(frozenset(branches)) if len(branches) == 3 else None


ENGINE_SCOPE = {
    "birth_year_month_day_conversion": False,
    "exact_solar_terms": False,
    "fortune_prediction": False,
    "person_level_moral_diagnostic": False,
    "original_classical_line_collation": False,
    "partial_bazi_mechanics": True,
    "validated_human_predictions": 0,
    "runtime_promotions": 0,
}
