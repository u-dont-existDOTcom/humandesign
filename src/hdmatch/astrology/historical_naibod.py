"""Literal Naibod table witness, preserved separately from continuous time keys.

SOURCE WITNESS: W. Lilly, Christian Astrology, vol. 3, printed pages 713
(degrees), 714 (minutes), and worked examples p.715 as *re-typeset*
in WorldAstrology 2003 publication, PDF CA-III.pdf, PDF pages 226–228.
Manually checked against the actual PDF screenshots, not OCR alone.

IMPORTANT: These are *literal entries in a modern re-typesetting*, NOT an
independently authenticated diplomatic transcription of the 1647 printing.
Multiple apparent numeric, column-label, and worked-example errors exist.
Preserve them as evidence and never silently repair, interpolate, or use this
diagnostic table as the default astrology time key.

Scope: whole degrees 0–90, integer minutes 0–59; absent minute 27 raises.
The original "years" field simply equals the "degrees" row label; the
degree days rollover at 69° without an added year, a documented anomaly.
The minute table has 60 as a visibly printed row, but 60' is not permitted
by arc D°M' input: use next whole degree instead to prevent ambiguity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Final

SOURCE_WITNESS: Final[str] = (
    "WorldAstrology retypeset Christian Astrology Book III (copyright 2003), "
    "printed pp. 713–715, PDF pages 226–228, not independently verified "
    "against the original 1647 page images"
)

# Exact literal rows: (extra_days, hours) over the printed YEARS = DEGREE
# label. Do not silently carry a year across the 68 -> 69 transition.
_DEGREE_BLOCK_A = (
    (5, 8),
    (10, 17),
    (16, 1),
    (21, 10),
    (26, 18),
    (32, 3),
    (37, 11),
    (42, 20),
    (48, 4),
    (53, 13),
    (58, 21),
    (64, 6),
    (69, 14),
    (74, 23),
    (80, 7),
    (85, 16),
    (91, 0),
    (96, 8),
    (101, 17),
    (107, 1),
    (112, 10),
    (117, 18),
    (123, 3),
    (128, 11),
    (133, 20),
    (139, 4),
    (144, 13),
    (149, 21),
    (155, 6),
    (160, 14),
)
_DEGREE_BLOCK_B = (
    (165, 23),
    (171, 7),
    (176, 16),
    (182, 0),
    (187, 8),
    (192, 17),
    (198, 1),
    (203, 9),
    (208, 18),
    (214, 3),
    (219, 11),
    (224, 20),
    (230, 4),
    (235, 13),
    (240, 21),
    (246, 6),
    (251, 14),
    (256, 23),
    (262, 7),
    (267, 16),
    (273, 0),
    (278, 8),
    (283, 17),
    (289, 1),
    (294, 10),
    (299, 18),
    (305, 3),
    (310, 11),
    (315, 20),
    (321, 4),
)
_DEGREE_BLOCK_C = (
    (326, 13),
    (331, 21),
    (337, 6),
    (342, 14),
    (347, 23),
    (353, 7),
    (358, 16),
    (364, 0),
    (4, 3),
    (9, 11),
    (14, 20),
    (20, 4),
    (25, 13),
    (30, 21),
    (36, 5),
    (41, 14),
    (46, 22),
    (52, 7),
    (57, 15),
    (62, 24),
    (68, 8),
    (73, 17),
    (79, 1),
    (84, 10),
    (89, 19),
    (95, 3),
    (100, 11),
    (105, 20),
    (111, 4),
    (116, 13),
)
DEGREE_COMPONENTS: Final[tuple[tuple[int, int], ...]] = (
    ((0, 0),) + _DEGREE_BLOCK_A + _DEGREE_BLOCK_B + _DEGREE_BLOCK_C
)
assert len(DEGREE_COMPONENTS) == 91

# Literally printed minute rows 1–60. 27' is unprinted; 28'-30' are
# suspiciously shifted: keep the VISIBLE labels rather than extrapolating.
# 60' is recorded as evidence but cannot be entered as D°60'.
MINUTE_COMPONENTS: Final[dict[int, tuple[int, int]]] = {
    0: (0, 0),
    1: (6, 4),
    2: (12, 8),
    3: (18, 13),
    4: (24, 17),
    5: (30, 21),
    6: (37, 1),
    7: (43, 6),
    8: (44, 10),
    9: (55, 14),
    10: (61, 18),
    11: (67, 23),
    12: (74, 3),
    13: (80, 7),
    14: (86, 11),
    15: (92, 16),
    16: (98, 20),
    17: (105, 0),
    18: (111, 4),
    19: (117, 9),
    20: (123, 13),
    21: (129, 17),
    22: (135, 21),
    23: (142, 1),
    24: (148, 6),
    25: (154, 10),
    26: (160, 14),
    28: (166, 18),
    29: (172, 23),
    30: (179, 3),
    31: (191, 11),
    32: (197, 16),
    33: (203, 20),
    34: (210, 0),
    35: (216, 4),
    36: (222, 9),
    37: (228, 13),
    38: (234, 17),
    39: (240, 21),
    40: (247, 2),
    41: (253, 6),
    42: (259, 10),
    43: (265, 14),
    44: (271, 8),
    45: (277, 23),
    46: (284, 3),
    47: (290, 7),
    48: (296, 11),
    49: (302, 16),
    50: (308, 20),
    51: (315, 0),
    52: (321, 4),
    53: (327, 9),
    54: (333, 13),
    55: (339, 17),
    56: (345, 21),
    57: (352, 2),
    58: (358, 6),
    59: (364, 10),
    60: (374, 14),
}

# Evidence is not a silently "corrected" chronology. A human-readable
# warning is emitted for each directly implicated cell or area.
KNOWN_WITNESS_ISSUES: Final[dict[str, str]] = {
    "degree_69_to_90": (
        "At 69°, degree-table DAYS resets from 364 to 4, but printed YEARS "
        "remains 69 rather than carrying one additional year; subsequent "
        "rows through 90° may be one year short if read as written."
    ),
    "degree_80_hour_24": ("80° has printed HR=24, not a normalized 0h with one extra day."),
    "minute_8": (
        "8' has 44d10h, between 7'=43d6h and 9'=55d14h; 49d10h "
        "might be expected, but is NOT substituted."
    ),
    "minute_27_missing": "The printed minute table skips the label 27'.",
    "minute_28_to_30": (
        "Printed 28',29',30' values form the numerical sequence expected "
        "for 27',28',29'. The label 27' is absent; no row silently shifted."
    ),
    "minute_44": ("44' prints 271d8h; adjacent rows suggest an unusual hour value."),
    "minute_60": (
        "60' prints 374d14h; it cannot be equated to one degree's printed "
        "1y5d8h (370d8h with 365-day years)."
    ),
    "example_19_52": (
        "Printed p.715 computes 19y422d21h, then subtracts 365 days "
        "but states 22y57d21h; the stated intermediate arithmetic yields "
        "20y57d21h, a discrepancy of two years."
    ),
}


@dataclass(frozen=True, slots=True)
class LiteralNaibodTime:
    arc_degrees: int
    arc_minutes: int
    literal_degree_years: int
    literal_degree_days: int
    literal_degree_hours: int
    literal_minute_days: int
    literal_minute_hours: int
    resulting_years: int
    resulting_days: int
    resulting_hours: int
    warnings: tuple[str, ...]
    witness: str = SOURCE_WITNESS

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["algorithm"] = "literal sum + normalize by 24h/day and 365d/year"
        result["not_continuous_key"] = True
        result["retypeset_original_not_independently_checked"] = True
        return result


def literal_naibod_lookup(degrees: int, minutes: int) -> LiteralNaibodTime:
    """Preserve the printed table, not an interpolated/verified timing theory."""
    if type(degrees) is not int or type(minutes) is not int:
        raise TypeError("degrees/minutes must be exact integers")
    if not 0 <= degrees <= 90 or not 0 <= minutes <= 59:
        raise ValueError("literal table covers D 0–90, M 0–59 only")
    if minutes not in MINUTE_COMPONENTS:
        raise ValueError("printed Lilly minute-table row is missing: 27'")
    day_degree, hour_degree = DEGREE_COMPONENTS[degrees]
    day_minute, hour_minute = MINUTE_COMPONENTS[minutes]
    total_hours = hour_degree + hour_minute
    total_days = day_degree + day_minute + total_hours // 24
    total_years = degrees + total_days // 365
    days = total_days % 365
    hours = total_hours % 24
    warnings: list[str] = []
    if degrees >= 69:
        warnings.append(KNOWN_WITNESS_ISSUES["degree_69_to_90"])
    if degrees == 80:
        warnings.append(KNOWN_WITNESS_ISSUES["degree_80_hour_24"])
    if minutes == 8:
        warnings.append(KNOWN_WITNESS_ISSUES["minute_8"])
    if minutes in (28, 29, 30):
        warnings.append(KNOWN_WITNESS_ISSUES["minute_28_to_30"])
    if minutes == 44:
        warnings.append(KNOWN_WITNESS_ISSUES["minute_44"])
    if (degrees, minutes) == (19, 52):
        warnings.append(KNOWN_WITNESS_ISSUES["example_19_52"])
    return LiteralNaibodTime(
        arc_degrees=degrees,
        arc_minutes=minutes,
        literal_degree_years=degrees,
        literal_degree_days=day_degree,
        literal_degree_hours=hour_degree,
        literal_minute_days=day_minute,
        literal_minute_hours=hour_minute,
        resulting_years=total_years,
        resulting_days=days,
        resulting_hours=hours,
        warnings=tuple(warnings),
    )


def source_issues() -> dict[str, str]:
    """Return unchanged, citable integrity objections to this particular scan."""
    return dict(KNOWN_WITNESS_ISSUES)


def main(argv: list[str] | None = None) -> int:
    """Inspect exact displayed D°M' cells; this is NOT an astrology time-key CLI."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description=(
            "Audit *literal* 2003 Lilly/Naibod printed-table cells; "
            "known numerical anomalies are retained"
        )
    )
    parser.add_argument("--degrees", type=int, required=True)
    parser.add_argument("--minutes", type=int, required=True)
    try:
        value = literal_naibod_lookup(
            degrees=parser.parse_args(argv).degrees,
            minutes=parser.parse_args(argv).minutes,
        )
    except (ValueError, TypeError) as exc:
        parser.exit(status=2, message=f"unavailable literal table cell: {exc}\n")
    print(json.dumps(value.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
