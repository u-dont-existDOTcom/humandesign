"""Partial, testable Zi Wei Dou Shu Quan Shu Vol.II historical star placements.

Only isolated mechanical examples were checked against Wikisource revision 1963110.
Not a complete chart calculator, does not resolve lunar leap months, true solar
time, birth-year conventions, or modern alternative Si Hua tables.
Nothing in this module validates individual predictions.
"""

from __future__ import annotations

BRANCHES: tuple[str, ...] = (
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
STEMS: tuple[str, ...] = (
    "Jia",
    "Yi",
    "Bing",
    "Ding",
    "Wu",
    "Ji",
    "Geng",
    "Xin",
    "Ren",
    "Gui",
)

LUCUN_BY_STEM = {
    "Jia": "Yin",
    "Yi": "Mao",
    "Bing": "Si",
    "Ding": "Wu",
    "Wu": "Si",
    "Ji": "Wu",
    "Geng": "Shen",
    "Xin": "You",
    "Ren": "Hai",
    "Gui": "Zi",
}

TIANMA_BY_TRINE = {
    "Yin": "Shen",
    "Wu": "Shen",
    "Xu": "Shen",
    "Shen": "Yin",
    "Zi": "Yin",
    "Chen": "Yin",
    "Si": "Hai",
    "You": "Hai",
    "Chou": "Hai",
    "Hai": "Si",
    "Mao": "Si",
    "Wei": "Si",
}

PALACE_NAMES = (
    "Life",
    "Siblings",
    "Spouse",
    "Children",
    "Wealth",
    "Illness",
    "Travel",
    "Associates",
    "Career",
    "Property",
    "Fortune",
    "Parents",
)


def move(palace: str, steps: int) -> str:
    """Traditional clockwise succession Zi -> Chou -> ... -> Hai."""
    if palace not in BRANCHES or isinstance(steps, bool) or not isinstance(steps, int):
        raise ValueError("Expected known palace and integer steps")
    return BRANCHES[(BRANCHES.index(palace) + steps) % 12]


def _ordinal(branch: str) -> int:
    if branch not in BRANCHES:
        raise ValueError(f"Unknown Earthly Branch: {branch}")
    return BRANCHES.index(branch)


def _month(month: int) -> int:
    if isinstance(month, bool) or not isinstance(month, int) or not 1 <= month <= 12:
        raise ValueError("Expected a resolved lunar birth month 1..12")
    return month - 1


def _day(day: int) -> int:
    if isinstance(day, bool) or not isinstance(day, int) or not 1 <= day <= 30:
        raise ValueError("Expected a resolved lunar birth day 1..30")
    return day - 1


def wen_chang(hour_branch: str) -> str:
    """子时戌上起文昌, count backward."""
    return move("Xu", -_ordinal(hour_branch))


def wen_qu(hour_branch: str) -> str:
    """文曲数从辰上起, count forward."""
    return move("Chen", _ordinal(hour_branch))


def zuo_fu(lunar_month: int) -> str:
    """左辅正月起于辰, forward. Intercalary handling externally resolved."""
    return move("Chen", _month(lunar_month))


def you_bi(lunar_month: int) -> str:
    """右弼从戌宫逆转; intercalary handling externally resolved."""
    return move("Xu", -_month(lunar_month))


def tian_xing(lunar_month: int) -> str:
    """Tian Xing: lunar first month at You, then forward."""
    return move("You", _month(lunar_month))


def tian_yao(lunar_month: int) -> str:
    """Tian Yao: lunar first month at Chou, then forward."""
    return move("Chou", _month(lunar_month))


def di_jie(hour_branch: str) -> str:
    """地劫: Zi hour at Hai, advances across hour branches."""
    return move("Hai", _ordinal(hour_branch))


def tian_kong(hour_branch: str) -> str:
    """天空: Zi hour at Hai, reverse through the hour cycle."""
    return move("Hai", -_ordinal(hour_branch))


def lu_cun(year_stem: str) -> str:
    """Year stem -> Lu Cun, with Bing/Wu and Ding/Ji paired."""
    try:
        return LUCUN_BY_STEM[year_stem]
    except KeyError as exc:
        raise ValueError("Unknown year Heavenly Stem") from exc


def qing_yang_and_tuo_luo(year_stem: str) -> tuple[str, str]:
    """Qing Yang forward +1, Tuo Luo backward -1 of Lu Cun."""
    base = lu_cun(year_stem)
    return move(base, 1), move(base, -1)


def tian_ma(year_branch: str) -> str:
    """Tian Ma from four year-branch trines."""
    try:
        return TIANMA_BY_TRINE[year_branch]
    except KeyError as exc:
        raise ValueError("Unknown year Earthly Branch") from exc


def san_tai(lunar_month: int, lunar_day: int) -> str:
    """初一 left-support palace, subsequent birth lunar days forwards."""
    return move(zuo_fu(lunar_month), _day(lunar_day))


def ba_zuo(lunar_month: int, lunar_day: int) -> str:
    """初一 right-support palace, subsequent birth lunar days backwards."""
    return move(you_bi(lunar_month), -_day(lunar_day))


def tian_ku(year_branch: str) -> str:
    """Year-Zi at Wu, reverse each year branch (Tian Ku)."""
    return move("Wu", -_ordinal(year_branch))


def tian_xu(year_branch: str) -> str:
    """Year-Zi at Wu, forward each year branch (Tian Xu)."""
    return move("Wu", _ordinal(year_branch))


def long_chi(year_branch: str) -> str:
    """Year-Zi at Chen, forward each year branch (Long Chi)."""
    return move("Chen", _ordinal(year_branch))


def natal_palace(life_branch: str, domain: str) -> str:
    """Twelve named palaces retrograde from Life. Not star placement."""
    if domain not in PALACE_NAMES:
        raise ValueError(f"Unknown palace domain: {domain}")
    return move(life_branch, -PALACE_NAMES.index(domain))


def tian_shang_and_tian_shi(life_branch: str) -> tuple[str, str]:
    """Explicit Associates and Illness house names; death/illness claims NOT inferred."""
    return natal_palace(life_branch, "Associates"), natal_palace(life_branch, "Illness")


def jia_four_transformations() -> tuple[str, str, str, str]:
    """Jia four transformation stars (Lu, Quan, Ke, Ji) from transmitted verse.

    No inference from this one verified row to other year stems or schools.
    """
    return ("LianZhen", "PoJun", "WuQu", "TaiYang")


def declared_method_status() -> dict[str, object]:
    return {
        "source_revision": 1963110,
        "scope": "bounded-original-source-mechanics",
        "complete_birth_chart_engine": False,
        "independent_calendar_engine_verified": False,
        "leap_lunar_month_variant_resolved": False,
        "si_hua_full_table_parity_verified": False,
        "individual_human_prediction_validated": False,
    }
