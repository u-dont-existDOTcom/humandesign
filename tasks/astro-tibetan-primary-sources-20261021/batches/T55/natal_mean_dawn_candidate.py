"""Research hypothesis: birth-UTC -> Tibetan four animal/element features.

NOT a culturally verified universal natal policy. Project-level explicit
candidate rule: extrapolate the theoretical Tibetan calendar dawn of
05:00 local MEAN solar time (Janson §6 Remark 6; Henning pp10–11)
to an independently supplied longitude. This extrapolation outside Tibet
is a test *hypothesis*, not a recovered historical Tibetan instruction.

Clock inputs MUST already be disambiguated into an aware UTC datetime,
including historical political timezone and daylight-saving rules.
Earth longitude is caller-supplied; it is NEVER inferred or geolocated.

No human predictive validity is implied.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Literal
import sys

P=Path(__file__).resolve().parent.parent
for folder in ("T53","T54"):
    path=str(P / folder)
    if path not in sys.path:
        sys.path.insert(0,path)
from tibetan_true_dates import gregorian_day_to_tibetan, TraditionalDate
from tibetan_calendar_reference import (
    HOURS_FROM_HARE, year_features, month_features,
    lunar_day_features, hour_element_from_day
)

BoundaryPolicy = Literal["project_extension_05_LMT_dawn"]
_POSSIBLE_POLICY="project_extension_05_LMT_dawn"


def _validated_longitude(longitude: str | float | Decimal) -> Decimal:
    if isinstance(longitude,bool):
        raise ValueError("longitude cannot be boolean")
    try:
        val=Decimal(str(longitude))
    except (InvalidOperation,ValueError):
        raise ValueError("longitude must be finite numerical degrees East") from None
    if not val.is_finite() or not -180 <= val <= 180:
        raise ValueError("longitude degrees must be finite and between -180,180")
    return val


def _utc_datetime(inst: datetime) -> datetime:
    if type(inst) is not datetime or inst.tzinfo is None or inst.utcoffset() is None:
        raise ValueError("UTC-aware datetime required; local clock and DST must be resolved")
    if inst.utcoffset() != timedelta(0):
        raise ValueError("Normalize an aware local clock to UTC before this stage")
    return inst.astimezone(timezone.utc)


@dataclass(frozen=True)
class BirthFourPillars:
    source_policy: str
    calendar_system: str
    epoch: int
    lunar_anomaly_policy: str
    utc_instant: str
    site_longitude_degrees_East: str
    longitude_mean_solar_offset_seconds: str
    local_mean_solar_clock: str
    theoretical_dawn_day_label: str
    year_label: int
    month: int
    leap_month: bool
    lunar_day: int
    leap_day: bool
    traditional_hour_animal: str
    four_animal_element_pairs: tuple[tuple[str,str],...]
    five_year_forces: dict[str,object]
    year_mewa: int
    lunar_day_mewa: int
    caution: str

    def serializable(self) -> dict:
        return asdict(self)


def calculate_mean_dawn_candidate(
    *, utc_instant: datetime,
    site_longitude_East: str | float | Decimal,
    mean_dawn_policy: BoundaryPolicy,
    calendar_system: Literal["phugpa","tsurphu"],
    calendar_epoch: int,
    lunar_anomaly_policy: Literal["rounded","dharmashri_exact"]
) -> BirthFourPillars:
    """Compute source-style year/month/tithi/double-hour animal+element pairs.

    This is an explicitly-named PROJECT POLICY combining author sources, not
    proof historical Tibetan astrologers applied this policy to all places.
    """
    if mean_dawn_policy != _POSSIBLE_POLICY:
        raise ValueError("Must specify the experimental 05:00 local-mean-solar policy")
    t=_utc_datetime(utc_instant)
    lon=_validated_longitude(site_longitude_East)
    seconds=lon*Decimal(240)
    # Time offsets are exactly 4 mean solar minutes/degree; implement to microsecond.
    micros=int((seconds*Decimal(1_000_000)).to_integral_value())
    mean_solar=t+timedelta(microseconds=micros)
    label=(mean_solar - timedelta(hours=5)).date()
    tb=gregorian_day_to_tibetan(label,system=calendar_system,
                                epoch=calendar_epoch,anomaly_policy=lunar_anomaly_policy)
    minute=mean_solar.hour*60+mean_solar.minute
    idx=((minute-5*60)%1440)//120
    hour=HOURS_FROM_HARE[idx]
    yr=year_features(tb.year)
    mon=month_features(tb.year,tb.month,policy=calendar_system)
    day=lunar_day_features(tb.year,tb.month,tb.lunar_day,policy=calendar_system)
    h_elem=hour_element_from_day(str(day["element"]),hour)
    return BirthFourPillars(
        source_policy=mean_dawn_policy,
        calendar_system=calendar_system,epoch=calendar_epoch,
        lunar_anomaly_policy=lunar_anomaly_policy,
        utc_instant=t.isoformat(),
        site_longitude_degrees_East=str(lon),
        longitude_mean_solar_offset_seconds=str(seconds),
        # Deliberately no timezone suffix: mean solar is a local clock, not UTC.
        local_mean_solar_clock=mean_solar.replace(tzinfo=None).isoformat(timespec="milliseconds"),
        theoretical_dawn_day_label=label.isoformat(),
        year_label=tb.year,
        month=tb.month,leap_month=tb.leap_month,
        lunar_day=tb.lunar_day,leap_day=tb.leap_day,
        traditional_hour_animal=hour,
        four_animal_element_pairs=(
            (str(yr["animal"]),str(yr["power_element"])),
            (str(mon["animal"]),str(mon["element"])),
            (str(day["animal"]),str(day["element"])),
            (hour,h_elem)
        ),
        five_year_forces={
            "life":yr["life_element"],
            "body":yr["body_element"],
            "power":yr["power_element"],
            "fortune":yr["fortune_element"],
            "spirit":yr["spirit_element"]
        },
        year_mewa=int(yr["central_mewa"]),
        lunar_day_mewa=int(day["mewa"]),
        caution=(
            "Unvalidated project extrapolation of theoretical Tibetan 05:00 "
            "local-mean-solar daybreak outside Tibet; conventional calendar "
            "year/month/day, not observed Sun/Moon ephemerides or predictive evidence."
        )
    )
