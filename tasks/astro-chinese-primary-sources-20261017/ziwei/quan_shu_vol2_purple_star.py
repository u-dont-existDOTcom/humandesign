"""Source-locked 紫微 primary-star day/bureau placement diagrams, with variants.

This limited calculator accepts an ALREADY-determined Chinese lunar day and
NaYin elemental bureau. It neither calculates the civil/lunar calendar nor
a complete, independently validated 14-star natal chart.
The oldid1963110 printed diagrams have two source defects. They remain
visible by default; separate opted-in amendments are qualified as modern
collation or independent-rule inference, NOT authenticated early source.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
import re

from quan_shu_vol2_nayin_bureau import SOURCE_PATH, SOURCE_SHA256
from ziwei_source_mechanics import BRANCHES

BUREAU_NAMES = {2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "火六局"}
ZH_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
DIGITS = dict(zip("一二三四五六七八九十", range(1, 11)))
ROW_INDICES = (2, 8, 14, 20)
PREFIX = {"初": 0, "十": 10, "廿": 20, "二": 10, "三": 20}


@dataclass(frozen=True)
class PurpleStarResult:
    bureau: int
    lunar_day: int
    palace: str | None
    source_status: str  # direct | modern_collation | ambiguity_resolved | rule_inference | ambiguous | missing


def original_bureau_diagrams() -> dict[int, dict[int, tuple[str, ...]]]:
    """Parse five exact vertical-number column diagrams from pinned full source.

    A day may map to two palaces in the original; do NOT silently pick one.
    """
    blob = SOURCE_PATH.read_bytes()
    if sha256(blob).hexdigest() != SOURCE_SHA256:
        raise ValueError("Pinned Zi Wei source SHA256 changed")
    raw = blob.decode("utf-8")
    blocks = re.findall(r"<nowiki>(.*?)</nowiki>", raw, flags=re.S)
    out: dict[int, dict[int, tuple[str, ...]]] = {}
    for bureau, marker in BUREAU_NAMES.items():
        matches = [b for b in blocks if marker in b]
        if len(matches) != 1:
            raise ValueError(f"Expected one exact original diagram for {marker}")
        lines = matches[0].splitlines()
        if len(lines) != 25:
            raise ValueError(f"Original diagram row count changed for {marker}")
        positions: dict[int, list[str]] = defaultdict(list)
        for start in ROW_INDICES:
            headings = [x.strip() for x in lines[start].split("|")[1:-1]]
            lower = [x.strip() for x in lines[start + 1].split("|")[1:-1]]
            branches = [x.strip() for x in lines[start + 3].split("|")[1:-1]]
            if not len(headings) == len(lower) == len(branches):
                raise ValueError("Malformed original diagram columns")
            for top, bottom, branch in zip(headings, lower, branches):
                if not branch:
                    if top or bottom:
                        raise ValueError("Diagram day without palace label")
                    continue
                if branch not in ZH_BRANCHES or len(top) != len(bottom):
                    raise ValueError("Unexpected original branch or number pairing")
                for prefix, digit in zip(top, bottom):
                    if prefix not in PREFIX or digit not in DIGITS:
                        raise ValueError("Unexpected original numeral glyph")
                    if prefix in ("二", "三") and digit != "十":
                        raise ValueError("Unexpected abbreviated 20/30 spelling")
                    day = PREFIX[prefix] + DIGITS[digit]
                    if not 1 <= day <= 30:
                        raise ValueError("Diagram lunar day out of bounds")
                    positions[day].append(BRANCHES[ZH_BRANCHES.index(branch)])
        out[bureau] = {day: tuple(houses) for day, houses in positions.items()}
    if set(out) != set(BUREAU_NAMES):
        raise ValueError("Missing five bureau diagrams")
    return out


def corrected_bureau_diagrams() -> dict[int, dict[int, tuple[str, ...]]]:
    """Apply only two explicitly recorded source-variant hypotheses.

    Wood-3: a spurious 寅/9 is really 寅/5 (textual collation).
    Metal-4: missing 亥/30 is inferred from division rule and later table.
    """
    out = original_bureau_diagrams()
    if out[3].get(9) != ("Chen", "Yin") or 5 in out[3]:
        raise ValueError("Known original Wood-3 anomaly no longer matches")
    if 30 in out[4]:
        raise ValueError("Known original Metal-4 omission no longer matches")
    out[3][9] = ("Chen",)
    out[3][5] = ("Yin",)
    out[4][30] = ("Hai",)
    for bureau, days in out.items():
        if set(days) != set(range(1, 31)) or any(len(branches) != 1 for branches in days.values()):
            raise ValueError(f"Corrected {bureau} diagram does not cover unique days 1..30")
    return out


def purple_palace_by_diagram(
    bureau: int, lunar_day: int, *, documented_corrections: bool = False
) -> PurpleStarResult:
    """Direct original diagram only by default; no guessing on conflicts."""
    _check_inputs(bureau, lunar_day)
    m = corrected_bureau_diagrams() if documented_corrections else original_bureau_diagrams()
    houses = m[bureau].get(lunar_day, ())
    if not houses:
        return PurpleStarResult(bureau, lunar_day, None, "missing")
    if len(houses) > 1:
        return PurpleStarResult(bureau, lunar_day, None, "ambiguous")
    if documented_corrections and (bureau, lunar_day) == (3, 5):
        status = "modern_collation"
    elif documented_corrections and (bureau, lunar_day) == (3, 9):
        # Source explicitly put this day in TWO palaces. Keeping the one
        # consistent with the modern comparator requires interpretation.
        status = "ambiguity_resolved"
    elif documented_corrections and (bureau, lunar_day) == (4, 30):
        status = "rule_inference"
    else:
        status = "direct"
    return PurpleStarResult(bureau, lunar_day, houses[0], status)


def purple_palace_by_division(bureau: int, lunar_day: int) -> str:
    """Independent-of-diagram modern remainder/complement formula.

    Round d upward to a multiple of bureau n. Start with quotient q at
    Yin+(q-1) and move by complement: even forward, odd backward.
    A modern algorithmic comparator, NOT an independently authenticated
    classical original or empirical prediction validation.
    """
    _check_inputs(bureau, lunar_day)
    complement = (-lunar_day) % bureau
    quotient = (lunar_day + complement) // bureau
    offset = (quotient - 1) + (complement if complement % 2 == 0 else -complement)
    return BRANCHES[(BRANCHES.index("Yin") + offset) % 12]


def _check_inputs(bureau: int, lunar_day: int) -> None:
    if type(bureau) is not int or bureau not in BUREAU_NAMES:
        raise ValueError("Bureau must be one of five original source values 2..6")
    if type(lunar_day) is not int or not 1 <= lunar_day <= 30:
        raise ValueError("Separately determined lunar day 1..30 is required")


ENGINE_SCOPE = {
    "source_diagram_to_palace_replay": True,
    "original_unambiguous_bureau_day_pairs": 147,
    "possible_bureau_day_pairs": 150,
    "documented_corrections_complete_150_pairs": True,
    "modern_comparator_not_independent_classical_authentication": True,
    "civil_to_lunar_conversion": False,
    "14_principal_star_full_layout": False,
    "real_human_predictive_validations": 0,
    "runtime_promotions": 0,
}
