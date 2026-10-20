"""All 14 traditional Zi Wei principal star *positions*, from source mnemonics.

This is a deterministic bounded layer: it only arranges the 14 major stars
when Zi Wei and Tian Fu anchors are known from separately resolved lunar inputs.
Original volume-II transmission (Wikisource oldid1963110) is source hashed.
No birth-date calendar engine, modern sect variants, all auxiliary stars,
annual luck, personally validated forecasts, or genuine human experiment.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from quan_shu_two_star_skeleton import (
    TwoStarSkeleton, tian_fu_from_purple, two_star_from_lunar_inputs,
)
from quan_shu_vol2_nayin_bureau import SOURCE_PATH, SOURCE_SHA256
from ziwei_source_mechanics import BRANCHES

VERSE = (
    "紫微天机逆行旁，隔一阳武天同当，又隔二位廉贞地，空三复见紫微郎，",
    "天府太阴与贪狼，巨门天相及天梁，七杀空三破军位，八星顺数细推详。",
)

PURPLE_FAMILY_STEPS = {
    "ZiWei": 0,
    "TianJi": -1,
    "TaiYang": -3,
    "WuQu": -4,
    "TianTong": -5,
    "LianZhen": -8,
}
FU_FAMILY_STEPS = {
    "TianFu": 0,
    "TaiYin": 1,
    "TanLang": 2,
    "JuMen": 3,
    "TianXiang": 4,
    "TianLiang": 5,
    "QiSha": 6,
    "PoJun": 10,
}
MAIN_STAR_COUNT = 14


@dataclass(frozen=True)
class FourteenStarLayout:
    """Do not interpret positions as individual-specific predictive evidence."""

    partial_natal: TwoStarSkeleton
    stars: dict[str, str] | None
    placements_by_palace: dict[str, tuple[str, ...]] | None
    status: str


def _verify_original_verse() -> None:
    blob = SOURCE_PATH.read_bytes()
    if sha256(blob).hexdigest() != SOURCE_SHA256:
        raise ValueError("Pinned original 14-star source changed")
    text = blob.decode("utf-8")
    if any(text.count(verse) != 1 for verse in VERSE):
        raise ValueError("Exact original 14-star mnemonic absent or ambiguous")


def fourteen_positions_from_purple(ziwei_palace: str) -> dict[str, str]:
    """Source mnemonic: Purple family counterclockwise; Fu clockwise."""
    _verify_original_verse()
    if ziwei_palace not in BRANCHES:
        raise ValueError("Require source-resolved Zi Wei anchor palace")
    fu_palace = tian_fu_from_purple(ziwei_palace)
    i = BRANCHES.index(ziwei_palace)
    j = BRANCHES.index(fu_palace)
    result = {name: BRANCHES[(i + step) % 12]
              for name, step in PURPLE_FAMILY_STEPS.items()}
    result.update({name: BRANCHES[(j + step) % 12]
                   for name, step in FU_FAMILY_STEPS.items()})
    if len(result) != MAIN_STAR_COUNT or result["TianFu"] != fu_palace:
        raise ValueError("Malformed original principal star family mapping")
    return result


def fourteen_from_lunar_inputs(
    year_stem: str,
    lunar_month: int,
    natal_hour_branch: str,
    lunar_day: int,
    *,
    is_leap_month: bool = False,
    documented_nayin_emendations: bool = False,
    documented_diagram_corrections: bool = False,
) -> FourteenStarLayout:
    """Full *major-star layer* for resolved lunar inputs; NOT a complete chart.

    Propagates raw-source lacunae as unknown; variant-normalized sources
    retain a 'qualified_source_variant' status.
    """
    partial = two_star_from_lunar_inputs(
        year_stem, lunar_month, natal_hour_branch, lunar_day,
        is_leap_month=is_leap_month,
        documented_nayin_emendations=documented_nayin_emendations,
        documented_diagram_corrections=documented_diagram_corrections,
    )
    if partial.purple_star is None or partial.purple_star.palace is None:
        return FourteenStarLayout(partial, None, None, partial.qualified_status)
    stars = fourteen_positions_from_purple(partial.purple_star.palace)
    if stars["TianFu"] != partial.tian_fu_palace:
        raise ValueError("Two-star anchor and 14-star rule disagree")
    by_palace: dict[str, tuple[str, ...]] = {
        palace: tuple(name for name in stars if stars[name] == palace)
        for palace in BRANCHES
    }
    return FourteenStarLayout(partial, stars, by_palace, partial.qualified_status)


ENGINE_SCOPE = {
    "source_verse_original_rev": 1963110,
    "one_bounded_fourteen_main_stars_placement_layer": True,
    "unverified_actual_civil_birth_calendar_conversion": True,
    "not_full_astrological_natal_chart": True,
    "all_minor_and_aux_stars": False,
    "full_four_transformations": False,
    "luck_and_life_cycles": False,
    "independent_original_Ming_imprint": False,
    "independently_blinded_real_human_outcomes": 0,
    "runtime_forecast_promotions": 0,
}
