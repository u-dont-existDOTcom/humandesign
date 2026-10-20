"""Chinese official lunar-date parity, with two pinned outside implementations.

HKO dates mean a Chinese official calendar reference day. There is NO
timezone/birthplace conversion; a foreign civil birth date must not be fed in
as if it were already a Hong Kong calendar date. Astrology lineages disagree
about Chinese New Year versus Li Chun year stem: only the official lunar-year
convention is implemented here; no guessing for the other convention.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path

from quan_shu_fourteen_stars import FourteenStarLayout, fourteen_from_lunar_inputs
from ziwei_source_mechanics import STEMS

BASE = Path(__file__).resolve().parents[1]
HKO_WITNESS = BASE / "batches/ChineseAstro-11/HKO_10_EXACT_RESPONSE_AND_TWO_LIBRARY_CALENDAR_PARITY_V1.json"
HKO_EVIDENCE_DIR = BASE / "batches/ChineseAstro-11/evidence"
HAN_STEMS = "甲乙丙丁戊己庚辛壬癸"
HAN_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
HAN_NUMBERS = "一二三四五六七八九"
REQUIRED_LIBRARY_VERSIONS = {"lunar_python": "1.4.8", "sxtwl": "2.0.7"}
REFERENCE_ZONE_ONLY = "Asia/Hong_Kong calendar date, independently resolved"
LUNAR_NEW_YEAR_POLICY = "official_chinese_lunar_new_year"


class CalendarParityError(ValueError):
    """Preserve discrepancy rather than silently deciding calendar lineage."""


@dataclass(frozen=True)
class OfficialLunarDate:
    year: int
    month: int
    day: int
    is_leap_month: bool
    source: str
    year_method: str = LUNAR_NEW_YEAR_POLICY

    @property
    def year_heavenly_stem(self) -> str:
        return STEMS[(self.year - 1984) % 10]

    @property
    def sexagenary_year(self) -> str:
        i = self.year - 1984
        return HAN_STEMS[i % 10] + HAN_BRANCHES[i % 12]


def _ymd(s: str) -> date:
    if not isinstance(s, str):
        raise CalendarParityError("YYYY-MM-DD string required")
    parsed = date.fromisoformat(s)
    if parsed.isoformat() != s or not (1901 <= parsed.year <= 2100):
        raise CalendarParityError("Exact YYYY-MM-DD in cautious 1901..2100 scope required")
    return parsed


def _day_chinese(s: str) -> int:
    """Decode only HKO's one-/two-character day conventions, fail unknowns."""
    if s == "三十":
        return 30
    if s in ("二十", "廿"):
        return 20
    if s == "十":
        return 10
    if s.startswith("初") and len(s) == 2:
        if s[1] == "十":
            return 10
        if s[1] in HAN_NUMBERS:
            return 1 + HAN_NUMBERS.index(s[1])
    if s.startswith("十") and len(s) == 2 and s[1] in HAN_NUMBERS:
        return 11 + HAN_NUMBERS.index(s[1])
    if s.startswith("廿") and len(s) == 2 and s[1] in HAN_NUMBERS:
        return 21 + HAN_NUMBERS.index(s[1])
    raise CalendarParityError(f"Unsupported original HKO lunar day: {s!r}")


def _month_chinese(s: str) -> tuple[int, bool]:
    leap = False
    if s.startswith(("閏", "闰")):
        s, leap = s[1:], True
    month_map = {"正": 1, "冬": 11, "臘": 12, "腊": 12}
    month_map.update({glyph: i for i, glyph in enumerate(HAN_NUMBERS, 1)})
    month_map.update({"十": 10, "十一": 11, "十二": 12})
    if s not in month_map:
        raise CalendarParityError(f"Unsupported original HKO lunar month: {s!r}")
    return month_map[s], leap


def parse_official_hko_json(reference_date: str, raw_json: dict[str, str]) -> OfficialLunarDate:
    greg = _ymd(reference_date)
    if set(raw_json) != {"LunarYear", "LunarDate"}:
        raise CalendarParityError("Unexpected HKO API record shape")
    year_label = raw_json["LunarYear"][:2]
    matches = [y for y in (greg.year - 1, greg.year)
               if HAN_STEMS[(y - 1984) % 10] + HAN_BRANCHES[(y - 1984) % 12] == year_label]
    if len(matches) != 1 or not raw_json["LunarYear"].startswith(year_label+"年"):
        raise CalendarParityError("HKO LunarYear stem-branch does not match adjacent Gregorian years")
    lunar_s = raw_json["LunarDate"]
    if lunar_s.count("月") != 1:
        raise CalendarParityError("Original HKO lunar month/day split invalid")
    month_s, day_s = lunar_s.split("月", 1)
    month, leap = _month_chinese(month_s)
    lunar_day = _day_chinese(day_s)
    return OfficialLunarDate(matches[0], month, lunar_day, leap, "hko_original_json")


def frozen_hko_example(reference_date: str) -> OfficialLunarDate:
    """Return only SHAs and bytes actually frozen from the HKO API; no live calls."""
    d = _ymd(reference_date).isoformat()
    fixture = json.loads(HKO_WITNESS.read_text(encoding="utf-8"))
    rows = [x for x in fixture["samples"] if x["gregorian_date"] == d]
    if len(rows) != 1:
        raise CalendarParityError("No source-locked HKO official observation for this date")
    expected = rows[0]
    raw = (HKO_EVIDENCE_DIR / f"hko_{d}.json").read_bytes()
    if sha256(raw).hexdigest() != expected["hko_response_original_utf8_sha256"]:
        raise CalendarParityError("HKO official frozen bytes changed")
    original = json.loads(raw)
    if original != expected["hko_json"]:
        raise CalendarParityError("Manifest and original HKO response diverged")
    result = parse_official_hko_json(d, original)
    if (result.year, -result.month if result.is_leap_month else result.month, result.day) != (
        expected["lunar_python"]["year"], expected["lunar_python"]["month"],
        expected["lunar_python"]["day"]
    ):
        raise CalendarParityError("Official HKO reading disagrees with frozen 6tail witness")
    s = expected["sxtwl"]
    if (result.year, result.month, result.day, result.is_leap_month) != (
        s["year"], s["month"], s["day"], s["leap_month"]
    ):
        raise CalendarParityError("Official HKO reading disagrees with frozen sxtwl witness")
    return result


def dual_library_reference_date(reference_date: str) -> OfficialLunarDate:
    """Require both separate pinned external tools to agree. Never choose silently.

    These are *software oracles*, not independently authenticated early sources.
    Importing requires intentionally installed optional dependencies. No network.
    """
    d = _ymd(reference_date)
    for pkg, needed in REQUIRED_LIBRARY_VERSIONS.items():
        try:
            found = version(pkg)
        except PackageNotFoundError as exc:
            raise CalendarParityError(f"Optional reference package {pkg} is not installed") from exc
        if found != needed:
            raise CalendarParityError(f"Unexpected {pkg} version {found}; pinned {needed}")
    try:
        from lunar_python import Solar
        import sxtwl
    except ImportError as exc:
        raise CalendarParityError("Both external calendar reference libraries required") from exc
    p = Solar.fromYmd(d.year, d.month, d.day).getLunar()
    q = sxtwl.fromSolar(d.year, d.month, d.day)
    p_result = (p.getYear(), abs(p.getMonth()), p.getDay(), p.getMonth() < 0)
    q_result = (q.getLunarYear(), q.getLunarMonth(), q.getLunarDay(), bool(q.isLunarLeap()))
    if p_result != q_result:
        raise CalendarParityError(f"Two calendar implementations disagree: 6tail={p_result}, sxtwl={q_result}")
    year, month, day_, leap = p_result
    if not 1 <= month <= 12 or not 1 <= day_ <= 30:
        raise CalendarParityError("External calendar fields invalid")
    if p.getYearInGanZhi() != (
        HAN_STEMS[(year - 1984) % 10] + HAN_BRANCHES[(year - 1984) % 12]
    ):
        raise CalendarParityError("6tail lunar-year Gan-Zhi disagrees with official-year cycle")
    return OfficialLunarDate(year, month, day_, leap, "dual_6tail_sxtwl_pinned")


def fourteen_from_reference_calendar_day(
    reference_date: str, natal_hour_branch: str,
    *,
    calendar_reference: str,
    year_boundary: str,
    documented_nayin_emendations: bool = False,
    documented_diagram_corrections: bool = False,
) -> FourteenStarLayout:
    """This is NOT a birth-time converter. Date is already an HKO calendar day.

    Explicit two crucial conventions are mandatory: reference Gregorian
    calendar date in Asia/Hong_Kong, official lunar New Year's year
    (not Li Chun). Birthplace local clock or astronomical true-solar-hour
    normalization is absent. Never derive natal hour without separate proof.
    """
    if calendar_reference != REFERENCE_ZONE_ONLY:
        raise CalendarParityError("Explicit pre-resolved Asia/Hong_Kong calendar day required")
    if year_boundary != LUNAR_NEW_YEAR_POLICY:
        raise CalendarParityError("Only official lunar New Year stem-year implemented, not Li Chun")
    lunar = dual_library_reference_date(reference_date)
    return fourteen_from_lunar_inputs(
        lunar.year_heavenly_stem,
        lunar.month,
        natal_hour_branch,
        lunar.day,
        is_leap_month=lunar.is_leap_month,
        documented_nayin_emendations=documented_nayin_emendations,
        documented_diagram_corrections=documented_diagram_corrections,
    )


ENGINE_SCOPE = {
    "two_external_calendar_libraries_version_pinned": True,
    "official_HKO_source_frozen_api_cases": 10,
    "calendar_reference_zone_explicitly_required": True,
    "official_new_year_convention_only": True,
    "li_chun_annual_boundary_implemented": False,
    "local_birth_time_to_reference_city_date_implemented": False,
    "historically_accurate_local_lunar_month": False,
    "first_14_principal_star_placement_after_reference_date": True,
    "complete_prediction_chart": False,
    "blinded_human_predictions": 0,
    "production_runtime_promotions": 0,
}
