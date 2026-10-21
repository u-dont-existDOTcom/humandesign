"""Traditional Phugpa five-planet and Rahu arithmetic, source-faithful subset.

Source: Svante Janson (2014), Tibetan calendar mathematics, Appendix D,
eqs D.1-D.20 and Tables 11-13. Independent numerical examples:
Edward Henning (2007), Kalacakra and the Tibetan Calendar, Chapter II,
printed pp.57-86, especially 1 March 1995 (general day 24,806).

No modern physically observed planetary ephemeris and no evidence that
astrology predicts human traits/events. Phugpa E1927 five-planet method
ONLY: other epochs and Tsurphu planetary methods are intentionally
unsupported until their own source constants are read.

Do NOT mistake planet 'birth-sign' (modeled orbital aphelion) for a
person's natal sign. Do NOT confuse karaṇa astronomical method with
eleven half-tithi karaṇas.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from typing import Literal
from pathlib import Path
import sys

_TASK_DIR=Path(__file__).resolve().parents[2]
_T54=_TASK_DIR/"batches"/"T54"
if str(_T54) not in sys.path:
    sys.path.insert(0,str(_T54))
import tibetan_true_dates as t54

Planet = Literal["Mercury","Venus","Mars","Jupiter","Saturn"]
_NAMES=("Mercury","Venus","Mars","Jupiter","Saturn")

# Janson Appendix D Table 11, Phugpa E1927.
_PERIODS=(8797,2247,687,4332,10766)
_OFFSETS=(4639,301,157,3964,6286)
_FINAL_RADIX=(8797,749,229,361,5383)
_BIRTHSIGN=(F(11,18),F(2,9),F(19,54),F(4,9),F(2,3))
_SLOW_SAMPLES=(
    (0,10,17,20),(0,5,9,10),(0,25,43,50),
    (0,11,20,23),(0,22,37,43)
)
_FAST_SAMPLES=(
    (0,16,32,47,61,74,85,92,97,97,93,82,62,34),
    (0,25,50,75,99,123,145,167,185,200,208,202,172,83),
    (0,24,47,70,93,114,135,153,168,179,182,171,133,53),
    (0,10,20,29,37,43,49,51,52,49,43,34,23,7),
    (0,6,11,16,20,24,26,28,28,26,22,17,11,3),
)

_PLANETARY_EPOCH_JDN=2424972
_SOLAR_RATE=F(18382,6714405)
_SOLAR_EPOCH_CANDIDATES={
    'janson_D9_literal_458772':F(1)-F(458772,6714405),
    'henning_and_Janson_mixed_radix_458672':F(1)-F(458672,6714405),
}
# Janson Appendix D.9 itself is inconsistent: its mixed radix
# 25;9,20,0,97440 agrees with Henning's 458672, not Janson's
# separately printed rational numerator 458772. TIB-CONFLICT-012.


def _integer(n:object,name:str)->int:
    if type(n) is not int:
        raise ValueError(f"{name} must be an integer")
    return n


def _table_value(values:tuple[int,...],idx:int,period:int)->int:
    x=idx%period
    if period==12:
        if x<=3: return values[x]
        if x<=6: return values[6-x]
        if x<=9: return -values[x-6]
        return -values[12-x]
    if period==27:
        return values[x] if x<=13 else -values[27-x]
    raise ValueError("Unsupported table symmetry")


def _interpolate(values:tuple[int,...],phase:F,period:int)->F:
    """Exactly linearly interpolate signed, symmetric source tables."""
    f=F(phase)%period
    low=f.numerator//f.denominator
    x=f-low
    return F(_table_value(values,low,period)) + (
        _table_value(values,low+1,period)-_table_value(values,low,period)
    )*x


@dataclass(frozen=True)
class PlanetResult:
    planet:str
    solar_epoch_policy:str
    integer_calendar_JDN:int
    general_day:int
    particular_day:int
    mean_heliocentric_circle:F
    mean_sun_circle:F
    mean_slow_circle:F
    step_index_circle:F
    birth_sign_reference_circle:F
    slow_table_correction_nadi:F
    true_slow_circle:F
    fast_table_correction_nadi:F
    traditional_geocentric_circle:F
    provenance:str="Janson Appendix D Phugpa E1927 historical mathematical model; NOT physical ephemeris"

    @property
    def longitude_degrees(self)->F:
        return self.traditional_geocentric_circle*360


def five_planets_at_JDN(jdn:int,*,system:str,epoch:int,
                        solar_epoch_policy:str)->tuple[PlanetResult,...]:
    """Calculate model longitudes for END of an already known civil-day JDN.

    No UTC-instant, longitude, observer-latitude, birth-time or real-planet
    calculation. Only documented source policy is accepted.
    """
    day=_integer(jdn,"Julian day number")
    if (system,epoch)!=("phugpa",1927):
        raise ValueError("Only source-defined planetary Phugpa E1927 implemented")
    if solar_epoch_policy not in _SOLAR_EPOCH_CANDIDATES:
        raise ValueError('Explicit E1927 solar epoch source variant required')
    gd=day-_PLANETARY_EPOCH_JDN
    mean_sun=(_SOLAR_RATE*gd+_SOLAR_EPOCH_CANDIDATES[solar_epoch_policy])%1
    out=[]
    for i,name in enumerate(_NAMES):
        multiple=100 if i==0 else 10 if i==1 else 1
        r=_PERIODS[i]
        particular=(multiple*gd+_OFFSETS[i])%r
        helio=F(particular,r)
        inner=i<2
        slow_mean=mean_sun if inner else helio
        index=helio if inner else mean_sun
        slow_anomaly=(slow_mean-_BIRTHSIGN[i])%1
        slow_correction=_interpolate(_SLOW_SAMPLES[i],12*slow_anomaly,12)
        true_slow=(slow_mean-slow_correction/F(27*60))%1
        diff=(index-true_slow)%1
        fast_correction=_interpolate(_FAST_SAMPLES[i],27*diff,27)
        geocentric=(true_slow+fast_correction/F(27*60))%1
        out.append(PlanetResult(
            name,solar_epoch_policy,day,gd,particular,helio,mean_sun,slow_mean,
            index,_BIRTHSIGN[i],slow_correction,true_slow,
            fast_correction,geocentric
        ))
    return tuple(out)


@dataclass(frozen=True)
class RahuResult:
    year:int
    month:int
    leap_month:bool
    lunar_day:int
    epoch:int
    true_month:int
    elapsed_lunar_days:int
    head_longitude_circle:F
    tail_longitude_circle:F
    note:str="Janson D.18–D.20 nodes of Moon; retrograde model; NOT a physical planet"


def rahu_at_lunar_day(year:int,month:int,lunar_day:int,*,leap_month:bool,
                       system:str,epoch:int)->RahuResult:
    """Rahu from E1927 or E1987 Phugpa n and tithi. No solar-day replacement."""
    if system!="phugpa" or epoch not in (1927,1987):
        raise ValueError("No source epoch Rahu constants except Phugpa E1927/E1987")
    if type(leap_month) is not bool:
        raise ValueError("leap_month must be explicit Boolean")
    d=_integer(lunar_day,"lunar_day")
    if not 1<=d<=30:
        raise ValueError("lunar_day must be 1–30")
    instances=t54.month_instances(year,month,system=system,epoch=epoch)
    found=[n for n,leap in instances if leap is leap_month]
    if len(found)!=1:
        raise ValueError("nonexistent month / leap status")
    n=found[0]
    rd=187 if epoch==1927 else 10
    x=30*(n+rd)+d
    head=(-F(x,6900))%1
    return RahuResult(year,month,leap_month,d,epoch,n,x,head,(head+F(1,2))%1)


def circle_to_mansions_3(value:F)->tuple[int,int,int]:
    """Truncate source model circle longitude to 3 mixed radix terms.
    Values are (mansion, nāḍī, pala) with radices (27,60,60).
    """
    f=(F(value)%1)*27
    a=int(f)
    y=(f-a)*60
    b=int(y)
    z=(y-b)*60
    return (a,b,int(z))
