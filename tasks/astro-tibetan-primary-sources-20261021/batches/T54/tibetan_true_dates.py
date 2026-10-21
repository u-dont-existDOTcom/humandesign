"""Traditional Tibetan Phugpa and Tsurphu calendar-date mathematics.

Original implementation of Svante Janson (2014), 'Tibetan calendar
mathematics', equations 5.2–5.9, 7.1–7.24, 8.1, and Appendix A.2.
License for this new implementation: MIT (see T54/README.md).

This is a *traditional mathematical calendar*, not a modern astronomical
ephemeris, not a lunar phase observation, and NOT evidence of astrological
prediction. Gregorian dates denote conventional civil-day labels; this code
does not convert a precise UTC birth instant to a Tibetan dawn-to-dawn day.
An independent timezone/daybreak/observer rule is still required for that.

Do not silently combine the common rounded lunar-anomaly increment with
Henning's Dharmashri exact-increment variant: anomaly_policy is mandatory.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from fractions import Fraction as F
from functools import lru_cache
from typing import Literal

System = Literal["phugpa", "tsurphu"]
Anomaly = Literal["rounded", "dharmashri_exact"]

_JDN_GREGORIAN_OFFSET = 1721425
_LUNAR_MONTH_LENGTH = F(167025, 5656)
_LUNAR_DAY_LENGTH = _LUNAR_MONTH_LENGTH / 30
_SOLAR_MONTH_MOTION = F(65, 804)
_SOLAR_DAY_MOTION = _SOLAR_MONTH_MOTION / 30
_LUNAR_ANOMALY_MONTH = F(253, 3528)
_LUNAR_ANOMALY_ROUNDED = F(1, 28)
_LUNAR_ANOMALY_EXACT = F(3781, 105840)

# (solar-year epoch, phase beta*, mean date, mean Sun, lunar anomaly).
# All values from Janson's original paper, not from upstream OSS converters.
_EPOCHS: dict[tuple[str, int], tuple[int, F, F, F]] = {
    ("phugpa", 806): (
        61, F(2015501) + F(4783, 5656), F(743, 804), F(475, 3528)
    ),
    ("phugpa", 1927): (
        55, F(2424972) + F(5457, 5656), F(749, 804), F(1741, 3528)
    ),
    ("phugpa", 1987): (
        0, F(2446914) + F(135, 707), F(0), F(38, 49)
    ),
    ("tsurphu", 1732): (
        59, F(2353745) + F(1795153, 7635600), -F(5983, 108540), F(207, 392)
    ),
    ("tsurphu", 1852): (
        14, F(2397598) + F(1197103, 7635600), F(23, 27135), F(1, 49)
    ),
}
_MOON_SAMPLES = (0, 5, 10, 15, 19, 22, 24, 25)
_SUN_SAMPLES = (0, 6, 10, 11)


def _as_int(val: object, name: str) -> int:
    if type(val) is not int:
        raise ValueError(f"{name} must be an integer, not {type(val).__name__}")
    return val


def _required_source(system: str, epoch: int, policy: str) -> tuple[int, F, F, F]:
    _as_int(epoch, "epoch")
    if (system, epoch) not in _EPOCHS:
        raise ValueError(f"Unsupported explicit calendar system/epoch: {(system, epoch)}")
    if policy not in ("rounded", "dharmashri_exact"):
        raise ValueError("Anomaly policy must be 'rounded' or 'dharmashri_exact'")
    return _EPOCHS[(system, epoch)]


def _modes(system: str, epoch: int) -> tuple[int, F, F, F]:
    if (system, epoch) not in _EPOCHS:
        raise ValueError("Unsupported explicit system/epoch combination")
    return _EPOCHS[(system, epoch)]


def _sample(period: int, positive: tuple[int, ...], x: F) -> F:
    """Antisymmetric discrete sine-like lookup, with exact linear interpolation."""
    x = x % period
    k = x.numerator // x.denominator
    remainder = x - k
    half = period // 2
    quarter = period // 4

    def item(i: int) -> int:
        i %= period
        if i <= quarter:
            return positive[i]
        if i <= half:
            return positive[half - i]
        if i <= half + quarter:
            return -positive[i - half]
        return -positive[period - i]

    return F(item(k)) + (item(k + 1) - item(k)) * remainder


def true_date(day: int, true_month: int, *, system: System, epoch: int,
              anomaly_policy: Anomaly) -> F:
    """Janson eq. 7.22: fractional JDN at end of given lunar day.

    A float would lose the exact boundary and is deliberately never used.
    """
    d = _as_int(day, "lunar day")
    n = _as_int(true_month, "true month")
    if not 0 <= d <= 30:
        raise ValueError("lunar day for true_date must be 0–30")
    _, m0, s0, a0 = _required_source(system, epoch, anomaly_policy)
    a2 = (_LUNAR_ANOMALY_ROUNDED if anomaly_policy == "rounded"
          else _LUNAR_ANOMALY_EXACT)
    mean_calendar_day = m0 + _LUNAR_MONTH_LENGTH * n + _LUNAR_DAY_LENGTH * d
    mean_solar_circle = s0 + _SOLAR_MONTH_MOTION * n + _SOLAR_DAY_MOTION * d
    moon_apogee_phase = a0 + _LUNAR_ANOMALY_MONTH * n + a2 * d
    corrected_moon = _sample(28, _MOON_SAMPLES, 28 * moon_apogee_phase)
    corrected_sun = _sample(12, _SUN_SAMPLES, 12 * (mean_solar_circle - F(1, 4)))
    return mean_calendar_day + (corrected_moon - corrected_sun) / 60


def true_date_jdn(day: int, true_month: int, *, system: System,
                  epoch: int, anomaly_policy: Anomaly) -> int:
    x = true_date(day, true_month, system=system, epoch=epoch,
                  anomaly_policy=anomaly_policy)
    return x.numerator // x.denominator


def month_instances(year: int, month: int, *, system: System, epoch: int
                    ) -> tuple[tuple[int, bool], ...]:
    """Tibetan month name -> actual true-month ordinal(s), leap first."""
    y = _as_int(year, "Tibetan year label")
    m = _as_int(month, "Tibetan month number")
    if not 1 <= m <= 12:
        raise ValueError("Month number 1–12 required")
    beta, _, _, _ = _modes(system, epoch)
    month_linear = 12 * (y - epoch) + m - 3
    integer, index = divmod(67 * month_linear + beta, 65)
    if system == "phugpa":
        leap = index in (48, 49)
        if leap:
            return ((integer, True), (integer + 1, False))
        return ((integer + (index >= 48), False),)
    leap = index in (0, 1)
    return ((integer - 1, True), (integer, False)) if leap else ((integer, False),)


@dataclass(frozen=True)
class TraditionalDate:
    year: int
    month: int
    leap_month: bool
    lunar_day: int
    leap_day: bool
    jdn: int | None   # skipped lunar-day label has no civil-day JDN
    skipped: bool = False

    @property
    def gregorian_date(self) -> date | None:
        if self.jdn is None:
            return None
        return date.fromordinal(self.jdn - _JDN_GREGORIAN_OFFSET)


@lru_cache(maxsize=3000)
def month_days(year: int, month: int, *, leap_month: bool,
               system: System, epoch: int, anomaly_policy: Anomaly
               ) -> tuple[TraditionalDate, ...]:
    _required_source(system, epoch, anomaly_policy)
    matches = [n for n, flag in month_instances(year, month, system=system, epoch=epoch)
               if flag is leap_month]
    if len(matches) != 1:
        raise ValueError("Requested leap/regular month does not exist")
    n = matches[0]
    ends = [true_date_jdn(d, n, system=system, epoch=epoch,
                          anomaly_policy=anomaly_policy) for d in range(1, 31)]
    # The previous month's *end* controls day1 at the month boundary;
    # Janson section 8 explicitly defines beginning of a month from it.
    prev = true_date_jdn(30, n - 1, system=system, epoch=epoch,
                         anomaly_policy=anomaly_policy)
    calendar: list[TraditionalDate] = []
    for d, end_jdn in enumerate(ends, 1):
        delta = end_jdn - prev
        if delta not in (0, 1, 2):
            raise ValueError(f"Unexpected tithi interval {delta}: n={n}, d={d}")
        if delta == 0:
            calendar.append(TraditionalDate(year, month, leap_month, d, False,
                                            None, skipped=True))
        elif delta == 1:
            calendar.append(TraditionalDate(year, month, leap_month, d, False,
                                            end_jdn))
        else:
            calendar.append(TraditionalDate(year, month, leap_month, d, True,
                                            prev + 1))
            calendar.append(TraditionalDate(year, month, leap_month, d, False,
                                            end_jdn))
        prev = end_jdn
    return tuple(calendar)


@lru_cache(maxsize=2000)
def losar_jdn(year: int, *, system: System, epoch: int,
              anomaly_policy: Anomaly) -> int:
    """Janson 8.3: JD of last (regular) lunar day 30 of prev year, plus 1."""
    _as_int(year, "Tibetan year start label")
    _required_source(system, epoch, anomaly_policy)
    previous_regular = month_instances(year - 1, 12, system=system, epoch=epoch)[-1]
    if previous_regular[1] is not False:
        raise AssertionError("Expected final instance to be regular month")
    return 1 + true_date_jdn(30, previous_regular[0], system=system,
                             epoch=epoch, anomaly_policy=anomaly_policy)


def losar_date(year: int, *, system: System, epoch: int,
               anomaly_policy: Anomaly) -> date:
    return date.fromordinal(losar_jdn(year, system=system, epoch=epoch,
                                     anomaly_policy=anomaly_policy)
                            - _JDN_GREGORIAN_OFFSET)


def tibetan_date_to_jdn(year: int, month: int, lunar_day: int, *,
                        leap_month: bool, leap_day: bool, system: System,
                        epoch: int, anomaly_policy: Anomaly) -> int:
    """Reject skipped/impossible days; leap flags mandatory, never guessed."""
    _as_int(lunar_day, "lunar day")
    if type(leap_month) is not bool or type(leap_day) is not bool:
        raise ValueError("Leap month and leap day flags must be explicit booleans")
    if not 1 <= lunar_day <= 30:
        raise ValueError("Lunar day must be 1–30")
    matches = [d for d in month_days(year, month, leap_month=leap_month,
                                    system=system, epoch=epoch, anomaly_policy=anomaly_policy)
               if d.lunar_day == lunar_day and d.leap_day is leap_day and not d.skipped]
    if len(matches) != 1 or matches[0].jdn is None:
        raise ValueError("Tibetan lunar date is skipped, invalid or mismatched leap flags")
    return matches[0].jdn


def jdn_to_tibetan(jdn: int, *, system: System, epoch: int,
                   anomaly_policy: Anomaly) -> TraditionalDate:
    """Find Tibetan date for a *known* local civil-day JDN (not UTC instant)."""
    j = _as_int(jdn, "integer civil-day JDN")
    _required_source(system, epoch, anomaly_policy)
    if not 1721426 <= j <= 3200000:
        raise ValueError("JDN outside supported proleptic Gregorian conversion range")
    civil_year = date.fromordinal(j - _JDN_GREGORIAN_OFFSET).year
    year = civil_year - (j < losar_jdn(civil_year, system=system, epoch=epoch,
                                     anomaly_policy=anomaly_policy))
    for m in range(1, 13):
        for n, flag in month_instances(year, m, system=system, epoch=epoch):
            prior = true_date_jdn(30, n - 1, system=system, epoch=epoch,
                                  anomaly_policy=anomaly_policy)
            final = true_date_jdn(30, n, system=system, epoch=epoch,
                                  anomaly_policy=anomaly_policy)
            if prior < j <= final:
                found = [d for d in month_days(year, m, leap_month=flag, system=system,
                                              epoch=epoch, anomaly_policy=anomaly_policy)
                         if d.jdn == j and not d.skipped]
                if len(found) == 1:
                    return found[0]
                raise ArithmeticError(f"No unique Tibetan day at JDN {j} in {(year, m)}")
    raise ArithmeticError(f"Cannot resolve Tibetan date for JDN {j}")


def gregorian_day_to_tibetan(civil_date: date, *, system: System, epoch: int,
                             anomaly_policy: Anomaly) -> TraditionalDate:
    """Gregorian day LABEL -> Tibetan day LABEL, without instant/dawn conversion."""
    if type(civil_date) is not date:
        raise ValueError("A datetime/UTC instant is not a Gregorian civil date label")
    return jdn_to_tibetan(civil_date.toordinal() + _JDN_GREGORIAN_OFFSET,
                          system=system, epoch=epoch, anomaly_policy=anomaly_policy)
