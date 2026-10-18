"""Bounded exact arithmetic reproducing Lilly's printed 1647 directions-time examples.

This module does not construct natal charts or make predictions. It distinguishes
the text's original statements, calculated arithmetic and internal discrepancies.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Angle:
    degree: int
    minute: int = 0
    second: int = 0

    def __post_init__(self):
        if not all(
            isinstance(v, int) and not isinstance(v, bool)
            for v in (self.degree, self.minute, self.second)
        ):
            raise ValueError("Angular components must be integers")
        if not 0 <= self.degree <= 360 or not 0 <= self.minute < 60 or not 0 <= self.second < 60:
            raise ValueError("Illegal sexagesimal angle")
        if self.degree == 360 and (self.minute or self.second):
            raise ValueError("360 degrees cannot have fractional arc")

    def arcseconds(self) -> int:
        return (self.degree * 60 + self.minute) * 60 + self.second

    @staticmethod
    def from_arcseconds(amount: int) -> Angle:
        if amount < 0:
            raise ValueError("Negative arc not admitted in this bounded demonstration")
        deg, sec = divmod(amount, 3600)
        minute, second = divmod(sec, 60)
        return Angle(deg, minute, second)


def difference(promittor: Angle, natal_angle: Angle) -> Angle:
    """Undirected difference in original worked example; not zodiac wrapping."""
    diff = promittor.arcseconds() - natal_angle.arcseconds()
    if diff < 0:
        raise ValueError("Wrap-around needs an independently declared direction convention")
    return Angle.from_arcseconds(diff)


def ptolemy_360_days(arc: Angle) -> tuple[int, int, int]:
    """Old source: 1 degree per year; 1 arcminute = 6 days, month = 30 days."""
    if arc.second:
        raise ValueError("First-edition example gives no fractional arcseconds")
    d = 6 * arc.minute
    months, days = divmod(d, 30)
    return arc.degree, months, days


def annual_rate_division(arc: Angle, yearly_arc: Angle) -> tuple[int, Angle]:
    """Calculate fully completed years and remaining arc at given declared rate."""
    if yearly_arc.arcseconds() <= 0:
        raise ValueError("Annual arc must be positive")
    completed, rem = divmod(arc.arcseconds(), yearly_arc.arcseconds())
    return completed, Angle.from_arcseconds(rem)


def fraction_of_year_of_remainder(rem: Angle, annual_rate: Angle) -> Fraction:
    """Fraction not a historical calendar date; exact rational angular ratio."""
    if annual_rate.arcseconds() <= 0:
        raise ValueError("Annual arc must be positive")
    return Fraction(rem.arcseconds(), annual_rate.arcseconds())


@dataclass(frozen=True)
class OldTabularTime:
    years: int
    days: int
    hours: int

    def __post_init__(self):
        if any(type(v) is not int or v < 0 for v in (self.years, self.days, self.hours)):
            raise ValueError("Year/day/hour input must be nonnegative integers")


def naibod_recombine(
    degree_lookup: OldTabularTime, minute_lookup: OldTabularTime, year_days: int = 365
) -> OldTabularTime:
    """Carry hours to days and complete 365-day years as Lilly does on PDF749."""
    if year_days != 365:
        raise ValueError("Lilly worked conversion explicitly subtracts 365 days")
    hours = degree_lookup.hours + minute_lookup.hours
    extra_days, remaining_hours = divmod(hours, 24)
    days = degree_lookup.days + minute_lookup.days + extra_days
    extra_years, remaining_days = divmod(days, year_days)
    return OldTabularTime(
        degree_lookup.years + minute_lookup.years + extra_years,
        remaining_days,
        remaining_hours,
    )


def source_demo_cases() -> dict[str, object]:
    """Literal source anchors with separately derived arithmetic; no person claims."""
    asc = Angle(312, 10)
    mars_terms = difference(Angle(324, 5), asc)
    mars_opposition = difference(Angle(332, 2), asc)
    assert mars_terms == Angle(11, 55)
    assert mars_opposition == Angle(19, 52)
    annual_rounded = Angle(0, 54)
    annual_from_sign_table = Angle(0, 54, 25)

    # Printed Maginus's table at the rounded 54' rate gives 13y ->11°42';
    # 22y ->19°48'. Text later uses 42' and 48' instead of the residuals.
    mag_a = annual_rate_division(mars_terms, annual_rounded)
    mag_b = annual_rate_division(mars_opposition, annual_rounded)

    return {
        "scope": "historical first-edition sexagesimal arithmetic only",
        "not_validated_astronomy_or_birth_chart": True,
        "not_a_real_human_forecast": True,
        "natal_oblique_ascension": asc.__dict__,
        "terms_arc": mars_terms.__dict__,
        "opposition_arc": mars_opposition.__dict__,
        "ptolemy_360_day_months_terms": ptolemy_360_days(mars_terms),
        "ptolemy_360_day_months_opposition": ptolemy_360_days(mars_opposition),
        "maginus_original_annual_rate_rounded": annual_rounded.__dict__,
        "maginus_original_separate_table_rate_7_libra": annual_from_sign_table.__dict__,
        "maginus_at_rounded_rate_terms": {
            "completed_years": mag_a[0],
            "remaining_arc": mag_a[1].__dict__,
            "remainder_year_fraction": str(fraction_of_year_of_remainder(mag_a[1], annual_rounded)),
            "original_worked_paragraph_uses_minutes": 42,
            "actual_difference_from_target_minutes": 13,
        },
        "maginus_at_rounded_rate_opposition": {
            "completed_years": mag_b[0],
            "remaining_arc": mag_b[1].__dict__,
            "remainder_year_fraction": str(fraction_of_year_of_remainder(mag_b[1], annual_rounded)),
            "original_worked_paragraph_uses_minutes": 48,
            "actual_difference_from_target_minutes": 4,
        },
        "maginus_if_annual_table_rate_used": {
            "terms": {
                "years": annual_rate_division(mars_terms, annual_from_sign_table)[0],
                "remainder": annual_rate_division(mars_terms, annual_from_sign_table)[1].__dict__,
            },
            "opposition": {
                "years": annual_rate_division(mars_opposition, annual_from_sign_table)[0],
                "remainder": annual_rate_division(mars_opposition, annual_from_sign_table)[
                    1
                ].__dict__,
            },
        },
        "naibod_original_source_degree_11": OldTabularTime(11, 58, 21).__dict__,
        "naibod_original_source_minute_55": OldTabularTime(0, 339, 17).__dict__,
        "naibod_original_result_terms": naibod_recombine(
            OldTabularTime(11, 58, 21), OldTabularTime(0, 339, 17)
        ).__dict__,
        "naibod_original_result_opposition": naibod_recombine(
            OldTabularTime(19, 101, 17), OldTabularTime(0, 321, 4)
        ).__dict__,
    }
