"""Bounded Chinese Zi Wei Dou Shu Quan Shu volume II auxiliary star placements.

These are historical sexagenary/chinese-lunar palace mechanics, NOT a complete
calendar, natal chart, identity determination, prognostic tool or empirical
validation. All inputs must already be separately calendar-resolved.
Source: pinned Wikisource raw Volume II oldid 1963110, sha256
1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72.
"""

from __future__ import annotations

from quan_shu_vol2_placements import BRANCHES, STEMS, move

CHANGSHENG_STAGES = (
    "ChangSheng",
    "MuYu",
    "GuanDai",
    "LinGuan",
    "DiWang",
    "Shuai",
    "Bing",
    "Si",
    "Mu",
    "Jue",
    "Tai",
    "Yang",
)
BUREAU_BASE = {
    "fire": "Yin",
    "wood": "Hai",
    "water": "Shen",
    "metal": "Si",
    "earth": "Shen",
}
HISTORICAL_DIRECTION = {"male": 1, "female": -1}
XUN_KONG = {
    "Zi": ("Xu", "Hai"),
    "Yin": ("Zi", "Chou"),
    "Chen": ("Yin", "Mao"),
    "Wu": ("Chen", "Si"),
    "Shen": ("Wu", "Wei"),
    "Xu": ("Shen", "You"),
}
JIE_LU_KONG = {
    "Jia": ("Shen", "You"),
    "Ji": ("Shen", "You"),
    "Yi": ("Wu", "Wei"),
    "Geng": ("Wu", "Wei"),
    "Bing": ("Chen", "Si"),
    "Xin": ("Chen", "Si"),
    "Ding": ("Yin", "Mao"),
    "Ren": ("Yin", "Mao"),
    "Wu": ("Zi", "Chou"),
    "Gui": ("Zi", "Chou"),
}
XIAO_XIAN_START = {
    "Yin": "Chen",
    "Wu": "Chen",
    "Xu": "Chen",
    "Shen": "Xu",
    "Zi": "Xu",
    "Chen": "Xu",
    "Si": "Wei",
    "You": "Wei",
    "Chou": "Wei",
    "Hai": "Chou",
    "Mao": "Chou",
    "Wei": "Chou",
}


def _branch_index(branch: str) -> int:
    if branch not in BRANCHES:
        raise ValueError("A separately verified Earthly Branch is required")
    return BRANCHES.index(branch)


def _historical_gender_direction(source_class: str) -> int:
    if source_class not in HISTORICAL_DIRECTION:
        raise ValueError("Historical source sex-coded category must be explicit")
    return HISTORICAL_DIRECTION[source_class]


def feng_ge(natal_year_branch: str) -> str:
    """凤阁子戌逆 — birth Zi at Xu, reverse for next birth year branches."""
    return move("Xu", -_branch_index(natal_year_branch))


def tai_fu(natal_hour_branch: str) -> str:
    """由午宫起子顺数至本生时 — birth Zi-hour at Wu, count forward."""
    return move("Wu", _branch_index(natal_hour_branch))


def feng_gao(natal_hour_branch: str) -> str:
    """由寅起宫子顺数至本生时 — birth Zi-hour at Yin, forward."""
    return move("Yin", _branch_index(natal_hour_branch))


def changsheng(bureau: str, stage: str, historic_source_sex_class: str) -> str:
    """Start from bureau-specific birth palace, cycle forward/back per old convention."""
    if bureau not in BUREAU_BASE:
        raise ValueError("Five-Element bureau must be precomputed")
    if stage not in CHANGSHENG_STAGES:
        raise ValueError("Not one of the source's twelve growth stages")
    direction = _historical_gender_direction(historic_source_sex_class)
    return move(BUREAU_BASE[bureau], direction * CHANGSHENG_STAGES.index(stage))


def hong_luan(natal_year_branch: str) -> str:
    """卯上起子逆数 — Zi year at Mao, backward branch progression."""
    return move("Mao", -_branch_index(natal_year_branch))


def tian_xi(natal_year_branch: str) -> str:
    """对宫天喜 — opposite Hong Luan in the twelve-palace zodiac."""
    return move(hong_luan(natal_year_branch), 6)


def annual_sang_diao_bai_guan(annual_tai_sui_branch: str) -> dict[str, str]:
    """Sang Men = Tai Sui +2, Diao Ke=-2, opposite Bai Hu and Guan Fu."""
    _branch_index(annual_tai_sui_branch)
    sang = move(annual_tai_sui_branch, 2)
    diao = move(annual_tai_sui_branch, -2)
    return {
        "SangMen": sang,
        "DiaoKe": diao,
        "BaiHu": move(sang, 6),
        "GuanFu": move(diao, 6),
    }


def dou_jun(
    annual_tai_sui_branch: str, natal_lunar_month: int, natal_birth_hour_branch: str
) -> str:
    """太岁正月逆数至生月 then Zi forward to birth hour (two stages)."""
    _branch_index(annual_tai_sui_branch)
    hour = _branch_index(natal_birth_hour_branch)
    if type(natal_lunar_month) is not int or not 1 <= natal_lunar_month <= 12:
        raise ValueError("Resolved natal lunar month one through twelve required")
    after_month = move(annual_tai_sui_branch, -(natal_lunar_month - 1))
    return move(after_month, hour)


def tian_de(annual_tai_sui_branch: str) -> str:
    return move("You", _branch_index(annual_tai_sui_branch))


def yue_de(annual_tai_sui_branch: str) -> str:
    return move("Zi", _branch_index(annual_tai_sui_branch))


def jie_shen(natal_year_branch: str) -> str:
    return move("Xu", -_branch_index(natal_year_branch))


def jie_lu_kong(year_heavenly_stem: str) -> tuple[str, str]:
    """Historical Jie Lu Kong Wang twin destinations, source year stems."""
    if year_heavenly_stem not in STEMS:
        raise ValueError("Require one of ten resolved natal Heavenly Stems")
    return JIE_LU_KONG[year_heavenly_stem]


def xun_kong(start_jia_branch: str) -> tuple[str, str]:
    """Six Jia ten-day cycle start branches, not an arbitrary natal year."""
    if start_jia_branch not in XUN_KONG:
        raise ValueError("Jia ten-day xun start branch required")
    return XUN_KONG[start_jia_branch]


def xiao_xian_start(natal_year_branch: str) -> str:
    """Small-cycle start according to original year-branch trine groups."""
    _branch_index(natal_year_branch)
    return XIAO_XIAN_START[natal_year_branch]


def method_limits() -> dict[str, object]:
    return {
        "wikisource_revision": 1963110,
        "historical_auxiliary_mechanics_only": True,
        "calendar_chinese_new_year_leap_month_verified": False,
        "natal_14_main_stars_full_layout_verified": False,
        "flying_three_sha_star_order_individually_verified": False,
        "birth_hour_late_zi_and_true_solar_time_resolved": False,
        "historical_sex_coded_rules_are_modern_gender_claims": False,
        "independent_real_human_predictions_validated": 0,
        "runtime_prediction_promotions": 0,
    }
