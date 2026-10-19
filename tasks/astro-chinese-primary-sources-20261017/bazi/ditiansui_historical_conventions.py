"""Bounded *Di Tian Sui* source classification, not natal forecasting.

Six pinned Chinese Wikisource 2017/2026 revisions are transmitted text and
commentary of disputed physical-edition/author provenance. These routines
represent explicit source enumerations and examples for already verified
stems/branches; not an actual birth, annual luck or predictive model.
"""

from __future__ import annotations

from bazi_source_mechanics import BRANCHES, STEMS

YANG_STEMS = ("Jia", "Bing", "Wu", "Geng", "Ren")
YIN_STEMS = ("Yi", "Ding", "Ji", "Xin", "Gui")
YANG_BRANCHES = ("Zi", "Yin", "Chen", "Wu", "Shen", "Xu")
YIN_BRANCHES = ("Chou", "Mao", "Si", "Wei", "You", "Hai")
FOUR_BIRTH_BRANCHES = ("Yin", "Shen", "Si", "Hai")
FOUR_STOREHOUSE_BRANCHES = ("Chen", "Xu", "Chou", "Wei")
FOUR_DEFEAT_BRANCHES = ("Zi", "Wu", "Mao", "You")
SOURCE_STEM_PATTERNS = {
    "Jia": "Tall-Wood seasonal",
    "Yi": "Flexible-Wood seasonal",
    "Bing": "Strong-Fire conditional",
    "Ding": "Subtle-Fire conditional",
    "Wu": "Heavy-Earth conditional",
    "Ji": "Moist-Earth conditional",
    "Geng": "Hard-Metal conditional",
    "Xin": "Soft-Metal conditional",
    "Ren": "Broad-Water conditional",
    "Gui": "Subtle-Water conditional",
}
# The 03 chapter does not support deterministic auspicious clash results.
TEXTUAL_CHAPTER03_BRANCH_CLASH_WARNING = "陽順陰逆，其理固殊，陽生陰死，其論勿執。"
SOURCE09_EXAMPLES = {
    frozenset(("Yi", "Geng")): ("He", "Metal"),
    frozenset(("Zi", "Chou")): ("He", "Earth"),
}
SOURCE09_AMITY_EXAMPLES = {
    frozenset(("Geng", "Xin")): "Hao",
    frozenset(("Shen", "You")): "Hao",
}


def _stem(value: str) -> str:
    if value not in STEMS:
        raise ValueError("One of ten independently resolved Heavenly Stems required")
    return value


def _branch(value: str) -> str:
    if value not in BRANCHES:
        raise ValueError("One of twelve independently resolved Earthly Branches required")
    return value


def explicit_stem_polarity(stem: str) -> str:
    s = _stem(stem)
    return "Yang" if s in YANG_STEMS else "Yin"


def explicit_branch_polarity(branch: str) -> str:
    b = _branch(branch)
    return "Yang" if b in YANG_BRANCHES else "Yin"


def original_branch_category(branch: str) -> str:
    b = _branch(branch)
    if b in FOUR_BIRTH_BRANCHES:
        return "FourBirth"
    if b in FOUR_STOREHOUSE_BRANCHES:
        return "FourStorehouse"
    return "FourDefeat"


def source_stem_season_metaphor(stem: str) -> str:
    return SOURCE_STEM_PATTERNS[_stem(stem)]


def source09_only_named_harmony_examples(a: str, b: str) -> dict[str, object]:
    """Classify only explicit historical examples; None elsewhere."""
    if a not in STEMS + BRANCHES or b not in STEMS + BRANCHES:
        raise ValueError("Original stem/branch symbols required")
    k = frozenset((a, b))
    if k in SOURCE09_EXAMPLES:
        cat, phase = SOURCE09_EXAMPLES[k]
        return {
            "original_relation": cat,
            "historical_phase_claim": phase,
            "general_universal_harmony_algorithm_implemented": False,
        }
    if k in SOURCE09_AMITY_EXAMPLES:
        return {
            "original_relation": SOURCE09_AMITY_EXAMPLES[k],
            "historical_phase_claim": None,
            "general_universal_harmony_algorithm_implemented": False,
        }
    return {
        "original_relation": None,
        "historical_phase_claim": None,
        "general_universal_harmony_algorithm_implemented": False,
    }


def source_research_limits() -> dict[str, object]:
    return {
        "pinned_transmitted_source_not_authenticated_print": True,
        "historical_textually_claimed_fatalities_are_predictions_of_actual_people": False,
        "source_clashes_can_be_assigned_favorable_outcomes_without_chart_context": False,
        "lunar_solar_term_and_time_zone_engine_verified": False,
        "prognostic_body_strength_and_wealth_patterns_verified": False,
        "complete_60_ganzhi_year_month_day_hour_algorithm_verified": False,
        "human_forward_blind_successes": 0,
        "runtime_promotions": 0,
    }
