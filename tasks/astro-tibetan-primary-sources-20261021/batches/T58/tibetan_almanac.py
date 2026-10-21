"""Janson-style Tibetan almanac components. Historical mathematical reconstruction.

Source: Svante Janson (2007, revised 2014), 'Tibetan calendar mathematics',
§7 eqs 7.5, 7.19–7.23 and §10 eqs 10.1–10.5.

These are model positions, not physically observed planetary coordinates:
* The day-start Moon is corrected from Moon at tithi end, approximately.
* The Sun is still at tithi end, not contemporaneous with the Moon.
* Yoga consequently combines non-simultaneous traditional model longitudes.
* Named karanas require Appendix I / separate naming witness; stored by IDs.
* Karana at daybreak has an EXPLICIT equal-duration half-tithi policy, not
  a confirmed universal traditional rule; Janson records uncertainty.

This module must not be used as evidence for predictions about humans.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Literal
from pathlib import Path
import sys

# Reuse existing T54 exact arithmetic (same source witness, avoids duplicate
# astronomical constants and keeps its explicit epoch and anomaly policy).
_DIR=Path(__file__).resolve().parent.parent
if str(_DIR/"T54") not in sys.path:
    sys.path.insert(0,str(_DIR/"T54"))
import tibetan_true_dates as t54

HalfPolicy=Literal["undetermined", "henning_equal_duration"]
_WEEKDAY=("Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday")


@dataclass(frozen=True)
class Karana:
    """Source category ID, NOT a Sanskrit name or evidenced auspiciousness."""
    half_position: int
    type_id: str
    fixed: bool


def karana_from_half_position(half_position: int) -> Karana:
    """Janson §10(viii), H=1..60. H=58 (not 57) is fixed."""
    h=t54._as_int(half_position,"half-tithi position")
    if not 1<=h<=60:
        raise ValueError("half position 1..60 required")
    if h in (1,58,59,60):
        return Karana(h,f"fixed_{h}",True)
    # (H-1) amod 7 = 1+((H-2) mod 7).
    return Karana(h,f"changing_{1+(h-2)%7}",False)


def karana_for_tithi(tithi: int) -> tuple[Karana,Karana]:
    d=t54._as_int(tithi,"tithi")
    if not 1<=d<=30:
        raise ValueError("tithi 1–30 required")
    return (karana_from_half_position(2*d-1),
            karana_from_half_position(2*d))


def _floor(q: F) -> int:
    return q.numerator//q.denominator


def mixed_radix_truncate(value: F, *, top_radix: int,
                         lower_radices: tuple[int,...],
                         number_terms: int) -> tuple[int,...]:
    """Truncate, do not round, like most quoted almanacs (§10).
    Values are non-negative mod top_radix, e.g. full-circle longitudes
    have 27 lunar mansions as their top digit.
    """
    t54._as_int(top_radix,"top radix")
    t54._as_int(number_terms,"number of terms")
    if top_radix<=0 or not 1<=number_terms<=1+len(lower_radices):
        raise ValueError("invalid mixed radix parameters")
    x=F(value)%top_radix
    vals=[_floor(x)]
    for radix in lower_radices[:number_terms-1]:
        t54._as_int(radix,"radix")
        if radix<=0:
            raise ValueError("invalid radix")
        x=(x-_floor(x))*radix
        vals.append(_floor(x))
    return tuple(vals)


def _month_true_index(year:int,month:int,leap_month:bool,system:str,
                      epoch:int) -> int:
    if type(leap_month) is not bool:
        raise ValueError("leap_month must be an explicit boolean")
    found=[n for n,flag in t54.month_instances(year,month,system=system,epoch=epoch)
           if flag is leap_month]
    if len(found)!=1:
        raise ValueError("No such named month and leap flag under selected tradition")
    return found[0]


def true_sun_circle(day:int,true_month:int,*,system:str,epoch:int,
                    anomaly_policy:str) -> F:
    """Janson eq 7.23, model Sun longitude (full circles, modulo 1)."""
    d=t54._as_int(day,"lunar day")
    n=t54._as_int(true_month,"true month")
    if not 0<=d<=30:
        raise ValueError("d must be 0–30")
    _,_,s0,_=t54._required_source(system,epoch,anomaly_policy)
    mean_sun=(s0+t54._SOLAR_MONTH_MOTION*n+t54._SOLAR_DAY_MOTION*d)
    sun_equ=t54._sample(12,t54._SUN_SAMPLES,
                         12*(mean_sun-F(1,4)))
    return (mean_sun-sun_equ/F(27*60))%1


def mean_sun_circle(day:int,true_month:int,*,system:str,epoch:int,
                    anomaly_policy:str) -> F:
    """Separate model mean solar longitude, Janson eq 7.5."""
    d=t54._as_int(day,"lunar day")
    n=t54._as_int(true_month,"true month")
    if not 0<=d<=30:
        raise ValueError("d must be 0–30")
    _,_,s0,_=t54._required_source(system,epoch,anomaly_policy)
    return (s0+t54._SOLAR_MONTH_MOTION*n+t54._SOLAR_DAY_MOTION*d)%1


@dataclass(frozen=True)
class Almanac:
    """All coordinates are source-defined circle fractions, not modern sky."""
    system: str
    epoch: int
    anomaly_policy: str
    year: int
    month: int
    leap_month: bool
    lunar_day: int
    leap_day: bool
    skipped: bool
    calendar_jdn: int|None
    weekday_name: str|None
    weekday_number: int|None
    tithi_end_true_weekday: F
    tithi_end_fraction: F
    model_mean_sun_circle: F
    model_true_sun_circle: F
    model_moon_tithi_end_circle: F
    model_moon_calendar_start_circle: F|None
    mansion_index_0_to_26: int|None
    yoga_circle: F|None
    yoga_index_0_to_26: int|None
    almanac_moon_position_policy: str
    model_half_tithi_policy: str
    karana_at_dawn_id: str|None
    source_precision_note: str

    def weekday_mixed_radix(self,terms:int=3)->tuple[int,...]:
        """Source §10: first repeated day uses unusual x;60,0 display,
        whereas second/ordinary/skipped lunar days use tithi-end fraction.
        This is not an ordinary normalized sexagesimal tuple.
        """
        if terms != 3:
            raise ValueError("weekday display in this source fixture uses 3 terms")
        if self.leap_day and not self.skipped:
            assert self.weekday_number is not None
            return (self.weekday_number,60,0)
        return mixed_radix_truncate(self.tithi_end_true_weekday,
                                    top_radix=7,lower_radices=(60,60,6,707),
                                    number_terms=terms)

    def mansion_mixed_radix(self,terms:int=3)->tuple[int,...]|None:
        if self.model_moon_calendar_start_circle is None:
            return None
        return mixed_radix_truncate(self.model_moon_calendar_start_circle*27,
                                    top_radix=27,lower_radices=(60,60,6,67),
                                    number_terms=terms)

    def yoga_mixed_radix(self,terms:int=3)->tuple[int,...]|None:
        if self.yoga_circle is None:
            return None
        return mixed_radix_truncate(self.yoga_circle*27,top_radix=27,
                                    lower_radices=(60,60,6,67),
                                    number_terms=terms)


def _karana_at_dawn_equal_duration(day:int,true_month:int,jdn:int,*,
                                   system:str,epoch:int,anomaly_policy:str)->Karana:
    # Henning's equal-half policy is an OPTION, not a source-proven universal
    # clock boundary. Use each tithi's individual true start and end instants.
    if day==1:
        begin=t54.true_date(30,true_month-1,system=system,epoch=epoch,
                            anomaly_policy=anomaly_policy)
    else:
        begin=t54.true_date(day-1,true_month,system=system,epoch=epoch,
                            anomaly_policy=anomaly_policy)
    end=t54.true_date(day,true_month,system=system,epoch=epoch,
                      anomaly_policy=anomaly_policy)
    if not begin<jdn<end:
        raise ArithmeticError("Civil daybreak outside source tithi interval")
    second_half=F(jdn)>=(begin+end)/2
    return karana_from_half_position(2*day if second_half else 2*day-1)


def almanac_for_tibetan_day(year:int,month:int,lunar_day:int,*,leap_month:bool,
                            leap_day:bool,system:str,epoch:int,
                            anomaly_policy:str,
                            karana_time_policy:HalfPolicy) -> Almanac:
    """Exact Janson source maths, and explicitly optional karaṇa clock policy.

    Skipped lunar days yield just tithi-end Sun/weekday references. Repeated
    day FIRST occurrence uses source special Moon-end minus 1/27; SECOND
    uses regular fractional end-time correction.
    """
    if karana_time_policy not in ("undetermined","henning_equal_duration"):
        raise ValueError("Source-specific karaṇa half-duration policy required")
    if type(leap_day) is not bool:
        raise ValueError("leap_day boolean must be explicit")
    n=_month_true_index(year,month,leap_month,system,epoch)
    day=t54._as_int(lunar_day,"lunar_day")
    if not 1<=day<=30:
        raise ValueError("lunar day 1–30 required")
    candidates=[r for r in t54.month_days(year,month,leap_month=leap_month,
                    system=system,epoch=epoch,anomaly_policy=anomaly_policy)
                if r.lunar_day==day and r.leap_day is leap_day]
    if len(candidates)!=1:
        raise ValueError("Invalid lunar day, leap month/day combination")
    entry=candidates[0]
    td=t54.true_date(day,n,system=system,epoch=epoch,
                      anomaly_policy=anomaly_policy)
    frac=td-_floor(td)
    sun=true_sun_circle(day,n,system=system,epoch=epoch,
                         anomaly_policy=anomaly_policy)
    mean=mean_sun_circle(day,n,system=system,epoch=epoch,
                         anomaly_policy=anomaly_policy)
    moon_end=(sun+F(day,30))%1
    true_week=(td+2)%7
    if entry.skipped:
        moon_start=None
        mansion=None
        yoga=None
        yoga_idx=None
        wname=None
        widx=None
        moon_policy="skipped_day_no_calendar_day"
        karana=None
    else:
        # On repeated first day, Janson says use -1/27 instead of -frac/27.
        moon_policy=("leap_day_first_moon_minus_one_mansion"
                     if leap_day else "normal_fractional_tithi_end_correction")
        moon_start=(moon_end - (F(1) if leap_day else frac)/27)%1
        mansion=_floor(moon_start*27)
        yoga=(moon_start+sun)%1
        yoga_idx=_floor(yoga*27)
        widx=(entry.jdn+2)%7
        wname=_WEEKDAY[widx]
        karana=(_karana_at_dawn_equal_duration(day,n,entry.jdn,system=system,
                         epoch=epoch,anomaly_policy=anomaly_policy).type_id
                 if karana_time_policy=="henning_equal_duration" else None)
    return Almanac(system,epoch,anomaly_policy,year,month,leap_month,day,
                   leap_day,entry.skipped,entry.jdn,wname,widx,
                   true_week,frac,mean,sun,moon_end,moon_start,
                   mansion,yoga,yoga_idx,moon_policy,karana_time_policy,karana,
                   "source almanac: solar angle end of tithi; moon start of civil "
                   "day approximated, non-simultaneous yoga; not observed sky")


def almanac_for_civil_day(jdn:int,*,system:str,epoch:int,
                          anomaly_policy:str,
                          karana_time_policy:HalfPolicy)->Almanac:
    """Requires integer **local civil-day JDN**, not a UTC timestamp."""
    x=t54.jdn_to_tibetan(jdn,system=system,epoch=epoch,
                         anomaly_policy=anomaly_policy)
    return almanac_for_tibetan_day(x.year,x.month,x.lunar_day,
                                   leap_month=x.leap_month,leap_day=x.leap_day,
                                   system=system,epoch=epoch,
                                   anomaly_policy=anomaly_policy,
                                   karana_time_policy=karana_time_policy)
