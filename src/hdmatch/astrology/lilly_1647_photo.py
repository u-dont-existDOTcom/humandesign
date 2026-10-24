"""Independently checked photographic readings of Lilly's Naibod tables (1647).

This edition-scoped research diagnostic is NOT a timeline timing key.

Two independent FIRST-EDITION source copies:
  1. Wellcome Collection IIIF b30338724, printed pp 713–715; exact source
     images and SHA-256 in the accompanying collation document.
  2. Internet Archive ca-william-lilly, printed pp 713–715;
     earlier first-edition source images in existing research checkpoint.

The whole degree TABLE (1..90) was checked against the Wellcome printed
page 713, including its extra year at 69..90. The minute TABLE (1..60,
with absent 27) was checked on printed p714. Faint/damaged values are
marked UNRESOLVED and never silently filled with modern retyping or a
mathematically inferred Naibod progression.

Most important new source divergence: original FIRST-EDITION minute 1'
PRINTS 5 days 4 hours, while the separate 2003 retypeset transcript
PRINTS 6 days 4 hours. This observation says nothing about what Lilly
mathematically intended: the printed table itself has inconsistencies.
Original 8'=44d10h and absent 27' are also preserved, not corrected.

Values for 1647 source are supplied explicitly below, NOT derived from
the 2003 transcription. This is a critical-source arithmetic aid,
NOT a historical method-complete prediction engine or endorsement.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Final


class SourceWitnessUnavailable(ValueError):
    """The printed source does not securely provide the requested literal cell."""


class SourceCellStatus(StrEnum):
    PHOTOGRAPH_CONFIRMED = "photograph_confirmed"
    PHOTO_PARTIALLY_LEGIBLE = "photo_partially_legible"
    LABEL_ABSENT = "label_absent_in_print"
    ADDED_ZERO_IDENTITY = "added_zero_identity"


SOURCE_1647: Final[str] = (
    "William Lilly Christian Astrology first edition 1647, printed pp.713–715; "
    "independent Wellcome b30338724 high-resolution colored source and "
    "Internet Archive ca-william-lilly 1647 source image; both direct photographs"
)

# Source-independent manual transcription of the 90 physical degree/day/hour
# rows photographed in the Wellcome 1647 source (page 713).
# The printed YEARS=DEGREES through 68°, thereafter YEARS=DEGREES+1.
# Entry zero is an editorial zero-arc identity not physically printed.
_DEGREE_PHOTO_BLOCK_1: Final[tuple[tuple[int, int], ...]] = (
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
_DEGREE_PHOTO_BLOCK_2: Final[tuple[tuple[int, int], ...]] = (
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
_DEGREE_PHOTO_BLOCK_3: Final[tuple[tuple[int, int], ...]] = (
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
DEGREE_PHOTO_COMPONENTS: Final[tuple[tuple[int, int], ...]] = (
    ((0, 0),) + _DEGREE_PHOTO_BLOCK_1 + _DEGREE_PHOTO_BLOCK_2 + _DEGREE_PHOTO_BLOCK_3
)
assert len(DEGREE_PHOTO_COMPONENTS) == 91

DEGREE_PHOTO_YEARS: Final[tuple[int, ...]] = tuple(
    degree if degree <= 68 else degree + 1 for degree in range(91)
)

# One-minute rows. Entries physically faint in BOTH examined copies are
# intentionally excluded from the authoritative original-day/hour map.
# Their *probable* values appear in the separate modern-witness column
# of the CSV, NOT here. An absent label (27') is different from a faint row.
MINUTE_PARTIALLY_LEGIBLE: Final[frozenset[int]] = frozenset(
    {
        25,
        28,
        39,
        41,
        44,
        48,
    }
)
MINUTE_LABEL_ABSENT: Final[frozenset[int]] = frozenset({27})

# Independently read Wellcome page 714, except uncertain entries above.
# Source prints 1' = 5d4h, NOT the separate 2003 retype's 6d4h.
MINUTE_PHOTO_COMPONENTS: Final[dict[int, tuple[int, int]]] = {
    0: (0, 0),
    1: (5, 4),
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
    26: (160, 14),
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
    40: (247, 2),
    42: (259, 10),
    43: (265, 14),
    45: (277, 23),
    46: (284, 3),
    47: (290, 7),
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
assert set(range(61)) == (
    set(MINUTE_PHOTO_COMPONENTS) | MINUTE_PARTIALLY_LEGIBLE | MINUTE_LABEL_ABSENT
)
assert not (set(MINUTE_PHOTO_COMPONENTS) & MINUTE_PARTIALLY_LEGIBLE)


def minute_status(minute: int) -> SourceCellStatus:
    if type(minute) is not int or minute < 0 or minute > 60:
        raise ValueError("integer minute row must be 0..60")
    if minute == 0:
        return SourceCellStatus.ADDED_ZERO_IDENTITY
    if minute in MINUTE_LABEL_ABSENT:
        return SourceCellStatus.LABEL_ABSENT
    if minute in MINUTE_PARTIALLY_LEGIBLE:
        return SourceCellStatus.PHOTO_PARTIALLY_LEGIBLE
    return SourceCellStatus.PHOTOGRAPH_CONFIRMED


@dataclass(frozen=True, slots=True)
class Original1647LiteralTime:
    degrees: int
    minutes: int
    source_years: int
    source_degree_days: int
    source_degree_hours: int
    source_minute_days: int
    source_minute_hours: int
    result_years: int
    result_days: int
    result_hours: int
    original_minute_status: str
    witness: str = SOURCE_1647

    def to_dict(self) -> dict[str, object]:
        out = asdict(self)
        out["source_method"] = "literal_1647_printed_cells_normalized_365_days_year"
        out["not_continuous_time_key"] = True
        out["possible_original_printing_anomalies"] = [
            "1'=5d4h despite nearby arithmetic progression",
            "8'=44d10h despite sequence",
            "27' absent from printed row labels",
            "60'=374d14h inconsistent with degree1",
            "80degree row prints 24 hours",
        ]
        return out


def independent_photo_lookup(degrees: int, minutes: int) -> Original1647LiteralTime:
    """Return independently verified *printed* cells only; missing/faint fail.

    Supported within 0–90 whole degrees and 0–59 whole minutes; seconds
    and fractional interpolation are NOT part of the printed table.
    """
    if type(degrees) is not int or type(minutes) is not int:
        raise TypeError("original source lookup needs integer degree and minute")
    if not 0 <= degrees <= 90 or not 0 <= minutes < 60:
        raise ValueError("original 1647 witness lookup range D=0..90, M=0..59")
    if minutes in MINUTE_LABEL_ABSENT:
        raise SourceWitnessUnavailable("27' label is absent in the 1647 print")
    if minutes in MINUTE_PARTIALLY_LEGIBLE:
        raise SourceWitnessUnavailable(
            f"1647 printed {minutes}' day/hour digits are not securely legible "
            "in both independent photographs; do not infer them from the 2003 text"
        )
    degree_days, degree_hours = DEGREE_PHOTO_COMPONENTS[degrees]
    minute_days, minute_hours = MINUTE_PHOTO_COMPONENTS[minutes]
    original_years = DEGREE_PHOTO_YEARS[degrees]
    cumulative_hours = degree_hours + minute_hours
    cumulative_days = degree_days + minute_days + cumulative_hours // 24
    years = original_years + cumulative_days // 365
    days = cumulative_days % 365
    hours = cumulative_hours % 24
    return Original1647LiteralTime(
        degrees=degrees,
        minutes=minutes,
        source_years=original_years,
        source_degree_days=degree_days,
        source_degree_hours=degree_hours,
        source_minute_days=minute_days,
        source_minute_hours=minute_hours,
        result_years=years,
        result_days=days,
        result_hours=hours,
        original_minute_status=minute_status(minutes).value,
    )


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Source-scoped 1647 Lilly Naibod photographic lookup; no interpolation"
    )
    parser.add_argument("--degrees", required=True, type=int)
    parser.add_argument("--minutes", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        value = independent_photo_lookup(args.degrees, args.minutes)
    except (SourceWitnessUnavailable, ValueError, TypeError) as exc:
        parser.exit(2, f"original 1647 cell unavailable: {exc}\n")
    print(json.dumps(value.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
