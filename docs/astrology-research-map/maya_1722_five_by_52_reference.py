#!/usr/bin/env python3
"""Source-limited 1722 K'iche' AHILABALZIH 5×52 intervalic grouping.

The photographed Berendt 1877 copy of the 1722 K'iche' calendar
(groups on folios 23-26) writes five day-sign/numeral combinations
in each group. For a 260-day sequence indexed from 1 Imox, five
equally spaced 52-day positions share each group.

This is a mathematical text-structure reference only. It does NOT
read or translate the adjacent K'iche' augury sentences, does NOT
map a person to a personality, and does NOT prove Dresden/Madrid
direct textual transmission.
"""
from __future__ import annotations

from dataclasses import dataclass

from maya_calendar_reference import KICHE_DAY_NAMES_BY_YUCATEC

CYCLE_DAYS = 260
SOURCE_INTERVAL = 52
GROUP_SIZE = 5
NUMBER_CYCLE = 13
NAME_CYCLE = 20
GROUP_COUNT = CYCLE_DAYS // GROUP_SIZE


@dataclass(frozen=True)
class NumberedKicheDay:
    reference_position_1_based: int
    number: int
    kiche_name: str


def reference_1722_almanac_group(group_1_based: int) -> tuple[NumberedKicheDay, ...]:
    """Return one group by mathematical distance, not a natal reading."""
    if type(group_1_based) is not int or not 1 <= group_1_based <= GROUP_COUNT:
        raise ValueError("group must be a numbered 1..52 manuscript row")
    first = group_1_based - 1
    out=[]
    for i in range(GROUP_SIZE):
        absolute_day_index = first + i * SOURCE_INTERVAL
        out.append(NumberedKicheDay(
            reference_position_1_based=absolute_day_index+1,
            number=(absolute_day_index % NUMBER_CYCLE)+1,
            kiche_name=KICHE_DAY_NAMES_BY_YUCATEC[absolute_day_index % NAME_CYCLE]
        ))
    return tuple(out)


def all_reference_1722_almanac_groups() -> tuple[tuple[NumberedKicheDay, ...], ...]:
    """Construct the 52 groups, covering 260 distinct sacred-day states once."""
    return tuple(reference_1722_almanac_group(i) for i in range(1,GROUP_COUNT+1))


if __name__=="__main__":
    # Only a source-math demonstration, not a human horoscope.
    for group in all_reference_1722_almanac_groups()[:4]:
        print([(i.number,i.kiche_name,i.reference_position_1_based) for i in group])
