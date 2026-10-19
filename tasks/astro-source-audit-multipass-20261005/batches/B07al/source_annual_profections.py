"""Bounded Lilly original 1647 annual-profection source-only sign rotation.

Inputs are already independently known zodiac sign, natal degree/minute and
completed annual solar-return years. Does NOT determine solar-return dates,
original chart placements or predict actual people/events.
"""

SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)


def sign_after_completed_solar_return_years(natal_sign: str, completed_solar_years: int) -> str:
    if natal_sign not in SIGNS:
        raise ValueError("Independently verified natal tropical zodiac sign required")
    if type(completed_solar_years) is not int or not 0 <= completed_solar_years <= 200:
        raise ValueError("Whole completed solar-return years 0–200 required")
    return SIGNS[(SIGNS.index(natal_sign) + completed_solar_years) % 12]


def projected_sign_degree_minute(
    natal_sign: str, natal_degree: int, natal_minute: int, completed_solar_years: int
) -> dict[str, object]:
    if type(natal_degree) is not int or not 0 <= natal_degree < 30:
        raise ValueError("Natal within-sign degree 0–29 required")
    if type(natal_minute) is not int or not 0 <= natal_minute < 60:
        raise ValueError("Natal within-degree arcminute 0–59 required")
    return {
        "sign": sign_after_completed_solar_return_years(natal_sign, completed_solar_years),
        "degree": natal_degree,
        "minute": natal_minute,
        "valid_calendar_solar_return_time_calculated": False,
        "real_person_chart_prediction_validated": False,
        "source": "Lilly printed annual Profections second distinct CHAP CLXVI",
    }


def completed_years_to_enter_for_current_ordinal_year(year_number: int) -> int:
    if type(year_number) is not int or not 1 <= year_number <= 201:
        raise ValueError("Ordinal current solar-return year 1–201 only")
    return year_number - 1


def source_nominal_degree_time_minutes() -> int:
    # Source explicitly says 12 days 4 hours 12 minutes per one degree.
    return (12 * 24 + 4) * 60 + 12


def source_method_limits() -> dict[str, object]:
    return {
        "source_printed_monthly_thirteen_parts": 13,
        "source_printed_daily_sign_days_hours_minutes": [2, 3, 54],
        "source_annual_year_requires_solar_return_to_natal_sun": True,
        "Gregorian_birthday_is_verified_exact_solar_return": False,
        "full_monthly_or_diurnal_profection_engine_proven": False,
        "72_year_merchant_zodiac_table_all_cells_source_transcribed": False,
        "original_1647_chart_ascendant_mid_heaven_full_natal_engine_validated": False,
        "independent_actual_human_prediction_validations": 0,
        "runtime_promotions": 0,
    }
