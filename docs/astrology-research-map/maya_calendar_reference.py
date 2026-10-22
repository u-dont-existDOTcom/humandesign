#!/usr/bin/env python3
"""Small reference-only Lowland Maya Long Count, Tzolk'in and Haab converter.

Strictly proleptic Gregorian civil *dates* (CE 1..9999); NOT a birth clock,
culturally authorized daykeeper reading, historic local-day boundary, validated
Maya horoscope, celestial ephemeris, or real-person prediction.

GMT correlation 584283 is a DECLARED SOURCE CHOICE. 584285 is an explicit
alternative sensitivity case, not picked according to a participant's answers.
Institutional test examples: Smithsonian NMAI Living Maya Time calendar pages.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

CORRELATIONS: tuple[int, int] = (584283, 584285)
BASE_TZOLKIN_NUMBER = 4  # 4 Ajaw on Long Count creation 13.0.0.0.0
BASE_TZOLKIN_NAME_INDEX = 19  # Ajaw in canonical 20-name Yucatec sequence
BASE_HAAB_DAY = 17 * 20 + 8  # 8 Kumk'u (Kumk'u = month 17)

# Names correspond to the Smithsonian National Museum of the American Indian
# publication by the K'iche' group Komon Tohil, 3-page source. The K'iche'
# names are a linguistic crosswalk, NOT proof of a living-count epoch.
YUCATEC_DAYS: tuple[str, ...] = (
    "IMIX’", "IK’", "AK’B’AL", "K’AN", "CHIKCHAN",
    "KIMI", "MANIK’", "LAMAT", "MULUK", "OK",
    "CHUWEN", "EB’", "B’EN", "IX", "MEN",
    "K’IB’", "KAB’AN", "ETZ’NAB’", "KAWAK", "AJAW",
)
KICHE_DAY_NAMES_BY_YUCATEC: tuple[str, ...] = (
    "IMOX", "IQ’", "AQ’AB’AL", "K’AT", "KAN",
    "KAME", "KEJ", "Q’ANIL", "TOJ", "TZ’I’",
    "B’ATZ’", "E", "AJ", "I’X", "TZ’IKIN",
    "AJMAQ", "NO’J", "TIJAX", "KAWOQ", "AJPU’",
)
HAAB_MONTHS: tuple[str, ...] = (
    "POP", "WO’", "SIP", "SOTZ’", "SEK", "XUL", "YAXK’IN",
    "MOL", "CH’EN", "YAX", "SAK’", "KEH", "MAK",
    "K’ANK’IN", "MUWAN", "PAX", "K’AYAB", "KUMK’U", "WAYEB",
)


class CalendarScopeError(ValueError):
    """Unsupported clock/school/correlation under the intentionally narrow scope."""


def proleptic_gregorian_jdn(civil_day: date) -> int:
    """Integer astronomical Julian Day Number for a proleptic Gregorian DATE.

    Julian vs Gregorian historical use is a separate upstream input-policy
    question. A datetime object is rejected so a person's local clock is never
    silently converted at midnight in the wrong cultural/day-boundary system.
    """
    if type(civil_day) is not date:  # not a datetime, string or unknown class
        raise CalendarScopeError("Only an explicit civil DATE, not a birth datetime")
    year, month, day = civil_day.year, civil_day.month, civil_day.day
    if not 1 <= year <= 9999:
        raise CalendarScopeError("Only CE years 1..9999 are in this limited program")
    offset = (14 - month) // 12
    y = year + 4800 - offset
    m = month + 12 * offset - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def reference_calendar_for_date(civil_day: date, *, correlation: int = 584283) -> dict[str, Any]:
    """Compute date-only Long Count/Haab/Tzolk'in under explicit declared policy."""
    if correlation not in CORRELATIONS or type(correlation) is not int:
        raise CalendarScopeError("Correlation must be explicitly 584283 or 584285")
    jdn = proleptic_gregorian_jdn(civil_day)
    elapsed = jdn - correlation
    if elapsed < 0:
        raise CalendarScopeError("Dates before the mythical correlation anchor unsupported")
    original_elapsed = elapsed
    baktun, elapsed = divmod(elapsed, 144000)
    katun, elapsed = divmod(elapsed, 7200)
    tun, elapsed = divmod(elapsed, 360)
    uinal, kin = divmod(elapsed, 20)
    tz_number = (BASE_TZOLKIN_NUMBER - 1 + original_elapsed) % 13 + 1
    tz_name_index = (BASE_TZOLKIN_NAME_INDEX + original_elapsed) % 20
    absolute_haab = (BASE_HAAB_DAY + original_elapsed) % 365
    month_index = min(18, absolute_haab // 20)
    haab_day = absolute_haab - month_index * 20
    return {
        "status": "LOWLAND_REFERENCE_CALENDAR_ARITHMETIC_ONLY",
        "civil_date_proleptic_gregorian": civil_day.isoformat(),
        "julian_day_number_integer": jdn,
        "GMT_correlation_JDN": correlation,
        "long_count": f"{baktun}.{katun}.{tun}.{uinal}.{kin}",
        "tzolkin_number": tz_number,
        "tzolkin_yucatec_name": YUCATEC_DAYS[tz_name_index],
        "kiche_label_from_practitioner_crosswalk_only": KICHE_DAY_NAMES_BY_YUCATEC[tz_name_index],
        "kiche_living_count_epoch_independently_verified": False,
        "haab_day": haab_day,
        "haab_month": HAAB_MONTHS[month_index],
        "birth_time_and_local_day_start_handled": False,
        "personality_or_fate_prediction_validated": False,
        "eligible_to_score_a_human": False,
    }


if __name__ == "__main__":
    import json

    # Historical published reference examples only, no living participant DOB.
    for day in (date(2000, 1, 1), date(2012, 12, 20), date(2012, 12, 21)):
        print(json.dumps(reference_calendar_for_date(day), ensure_ascii=False, sort_keys=True))
