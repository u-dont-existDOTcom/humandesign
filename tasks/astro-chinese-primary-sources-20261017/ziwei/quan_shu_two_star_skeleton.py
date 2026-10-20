"""Two of 14 principal Zi Wei stars from separately provided lunar inputs.

Combines source-locked life/body + palace stem, the traditional NaYin bureau,
the original five day-to-ZiWei diagrams and the original Tian Fu reflection.
No local birth date/time conversion, predictions or full 14-star chart.
"""

from dataclasses import dataclass

from quan_shu_vol2_nayin_bureau import BureauResult, life_palace_bureau
from quan_shu_vol2_purple_star import PurpleStarResult, purple_palace_by_diagram
from ziwei_source_mechanics import BRANCHES, life_and_body_palaces


@dataclass(frozen=True)
class TwoStarSkeleton:
    life_palace: str
    body_palace: str
    bureau: BureauResult
    purple_star: PurpleStarResult | None
    tian_fu_palace: str | None
    qualified_status: str


def tian_fu_from_purple(purple_palace: str) -> str:
    """Original Volume II 安天府图: Purple/Fu reflect across Yin–Shen.

    Zi Wei at Yin or Shen => both stars share the palace. A specific
    original textual example says Zi Wei Chou => Tian Fu Mao.
    """
    if purple_palace not in BRANCHES:
        raise ValueError("Require independently resolved Zi Wei palace branch")
    return BRANCHES[(4 - BRANCHES.index(purple_palace)) % 12]


def two_star_from_lunar_inputs(
    year_stem: str,
    lunar_month: int,
    natal_hour_branch: str,
    lunar_day: int,
    *,
    is_leap_month: bool = False,
    documented_nayin_emendations: bool = False,
    documented_diagram_corrections: bool = False,
) -> TwoStarSkeleton:
    """No automatic lunar calendar: all four birth inputs must be resolved.

    Original raw mode reports missing/ambiguous palace as unknown.
    Historical leap rule is the selected transmitted Quan Shu convention,
    not silently changed to a different school's leap-month treatment.
    """
    if type(lunar_day) is not int or not 1 <= lunar_day <= 30:
        raise ValueError("Require lunar day 1..30 already calendar resolved")
    life, body = life_and_body_palaces(
        lunar_month, natal_hour_branch, is_leap_month=is_leap_month
    )
    bureau = life_palace_bureau(
        year_stem, life, documented_emendations=documented_nayin_emendations
    )
    if bureau.bureau_number is None:
        return TwoStarSkeleton(life, body, bureau, None, None, "unresolved_bureau")
    purple = purple_palace_by_diagram(
        bureau.bureau_number, lunar_day,
        documented_corrections=documented_diagram_corrections
    )
    if purple.palace is None:
        return TwoStarSkeleton(life, body, bureau, purple, None, "unresolved_purple_star")
    fu = tian_fu_from_purple(purple.palace)
    if bureau.source_status != "direct" or purple.source_status != "direct":
        status = "qualified_source_variant"
    else:
        status = "original_transcription_only"
    return TwoStarSkeleton(life, body, bureau, purple, fu, status)


ENGINE_SCOPE = {
    "input_is_already_resolved_lunar_year_stem_month_hour_day": True,
    "partial_two_of_fourteen_principal_stars": True,
    "complete_fourteen_star_chart": False,
    "civil_time_to_chinese_lunar": False,
    "authenticated_ancient_original_book": False,
    "independent_real_human_validations": 0,
    "runtime_promotions": 0,
}
