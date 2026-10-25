"""C31: research-only Swiss body + uncertified natal-angle bridge.

Read existing fail-closed SwissEphemerisProvider for Moon and Saturn.
Use existing Placidus houses to compute a DIAGNOSTIC Ascendant only.
The C30 Lot rule is not promoted to human prediction; Ascendant/MC
independent parity and civil-time provenance remain open.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal
from math import atan2, cos, degrees, pi, radians, sin
from pathlib import Path
import sys

_PROJECT_ROOT=Path(__file__).resolve().parents[2]
_SRC=str(_PROJECT_ROOT/"src")
if _SRC not in sys.path:
    sys.path.insert(0,_SRC)

from hellenistic_c30_dorotheus_expedition_lot import (
    CAMPAIGN_INDICATOR_SIGNS,ZODIAC,documentary_claim
)

BODY_STATUS="STRICT_SWISS_RETURNED_FILE_VERIFIED"
ANGLE_STATUS="SWISS_HOUSES_ANGLE_NOT_INDEPENDENTLY_CERTIFIED"

@dataclass(frozen=True)
class VerifiedBodyPair:
    utc:str
    moon:str
    saturn:str
    swiss_version:str
    local_source_hashes:tuple[tuple[str,str],...]
    status:str=BODY_STATUS

def swiss_positions(provider:object,at_utc:datetime)->VerifiedBodyPair:
    """Incumbent provider enforces returned flags and exact used .se1 file."""
    from hdmatch.chart.ephemeris import CelestialBody,SwissEphemerisProvider
    if type(provider) is not SwissEphemerisProvider:
        raise ValueError("require actual fail-closed SwissEphemerisProvider")
    if at_utc.tzinfo is None or at_utc.utcoffset() is None:
        raise ValueError("aware UTC time required")
    utc=at_utc.astimezone(UTC)
    metadata=provider.metadata
    if metadata.provider!="swiss_ephemeris_local_files" or len(metadata.files)<2:
        raise ValueError("no verified .se1 source manifest")
    moon=provider.position(CelestialBody.MOON,utc)
    saturn=provider.position(CelestialBody.SATURN,utc)
    return VerifiedBodyPair(
        utc.isoformat(),str(moon.longitude),str(saturn.longitude),
        metadata.library_version,
        tuple(sorted((Path(f.path).name,f.sha256) for f in metadata.files))
    )

def uncertified_angle_diagnostic(at_utc:datetime,*,lat:float,lon:float)->dict:
    """Swiss angle is explicitly UNVERIFIED by independent angle audit."""
    from hdmatch.relationship.western import placidus_houses
    if at_utc.tzinfo is None or at_utc.utcoffset() is None:
        raise ValueError("aware date required")
    if not (-89<lat<89 and -180<=lon<=180):
        raise ValueError("coordinate outside documented range")
    _,asc,mc=placidus_houses(at_utc.astimezone(UTC),latitude=lat,longitude=lon)
    return {"asc":str(asc),"mc":str(mc),"angle_status":ANGLE_STATUS,
            "independent_angle_parity_certified":False,
            "full_timezone_UT1_EOP_chain_certified":False}

def joined_lot_diagnostic(pair:VerifiedBodyPair,angle:dict)->dict:
    """Non-admissible indicator even if an actual planetary source is verified."""
    if pair.status!=BODY_STATUS or angle.get("angle_status")!=ANGLE_STATUS:
        raise ValueError("typed research provenance is mandatory")
    if angle.get("independent_angle_parity_certified") is not False:
        raise ValueError("this research entrypoint does not allow certified angles")
    if angle.get("full_timezone_UT1_EOP_chain_certified") is not False:
        raise ValueError("unknown UT1 chain must remain explicit")
    result=documentary_claim(
        ascendant=angle["asc"],moon=pair.moon,saturn=pair.saturn)
    return {"lot":result,"bodies":asdict(pair),"angle":angle.copy(),
            "eligible_for_human_prediction":False,
            "evaluated_real_human_outcomes":False,
            "research_status":"PLANETARY_POSITIONS_VERIFIED_ANGLE_AUDIT_PENDING"}


def mean_geometric_angles(at_utc:datetime,*,lat:float,lon:float)->tuple[float,float]:
    """Independent spherical horizon geometry and mean sidereal time.

    Gregorian JD, Meeus GMST polynomial, mean obliquity; UTC approximates
    UT1. No nutation, EOP, original disputed case, timezone disambiguation.
    DO NOT use as a certified Ascendant or human-study oracle.
    """
    if at_utc.tzinfo is None or at_utc.utcoffset() is None:
        raise ValueError("aware date required")
    dt=at_utc.astimezone(UTC)
    if not (1583<=dt.year<=2200 and -89<lat<89 and -180<=lon<=180):
        raise ValueError("synthetic comparison outside supported domain")
    y,m,day=dt.year,dt.month,dt.day
    a=(14-m)//12
    yy=y+4800-a
    mm=m+12*a-3
    jdn=day+(153*mm+2)//5+365*yy+yy//4-yy//100+yy//400-32045
    sec=dt.hour*3600+dt.minute*60+dt.second+dt.microsecond/1e6
    jd=jdn-.5+sec/86400.
    T=(jd-2451545.)/36525.
    gmst=(280.46061837+360.98564736629*(jd-2451545.)
          +.000387933*T*T-T*T*T/38710000.)%360.
    theta=radians((gmst+lon)%360.)
    epsilon=radians(23+26/60+21.448/3600
          -(46.815*T+.00059*T*T-.001813*T*T*T)/3600)
    phi=radians(lat)
    A=cos(phi)*cos(theta)
    B=sin(phi)*sin(epsilon)+cos(phi)*cos(epsilon)*sin(theta)
    asc=atan2(-A,B)
    east=-sin(theta)*cos(asc)+cos(theta)*cos(epsilon)*sin(asc)
    if east<0:
        asc+=pi
    mc=atan2(sin(theta)/cos(epsilon),cos(theta))
    return degrees(asc)%360.,degrees(mc)%360.

def circular_distance(a:float,b:float)->float:
    return abs(((a-b+180.)%360.)-180.)

def synthetic_angle_comparison(at_utc:datetime,*,lat:float,lon:float)->dict:
    """A useful bounded sanity check, NOT independent full-angle certification."""
    sw=uncertified_angle_diagnostic(at_utc,lat=lat,lon=lon)
    asc,mc=mean_geometric_angles(at_utc,lat=lat,lon=lon)
    return {
        "utc":at_utc.astimezone(UTC).isoformat(),"lat":lat,"lon":lon,
        "analytic_mean_asc_deg":asc,"swiss_asc_deg":float(sw["asc"]),
        "analytic_mean_mc_deg":mc,"swiss_mc_deg":float(sw["mc"]),
        "asc_error_arcminutes":circular_distance(asc,float(sw["asc"]))*60.,
        "mc_error_arcminutes":circular_distance(mc,float(sw["mc"]))*60.,
        "UT1_nutation_and_EOP_unverified":True,
        "known_disputed_case_compared":False,
        "human_prediction_angles_certified":False
    }


def closed_lot_indicator_envelope(
    *, asc:tuple[str,str], moon:tuple[str,str], saturn:tuple[str,str],
    bounds_continuously_certified:bool=False
)->dict:
    """Compute ALL possible indicated/unindicated categories in three bounds.

    Unwrapped closed longitude envelopes must contain every plausible state,
    NOT merely sampled chart points. A stable logical result is conditional
    on *proven* input enclosures. The project's Ascendant angle audit is
    unresolved, so C31 NEVER upgrades this result to human test readiness.
    """
    if type(bounds_continuously_certified) is not bool:
        raise ValueError("continuous-envelope certification must be boolean")
    def bounds(pair:tuple[str,str])->tuple[Decimal,Decimal]:
        if len(pair)!=2:
            raise ValueError("closed envelope requires two endpoints")
        a,b=(Decimal(str(x)) for x in pair)
        if not a.is_finite() or not b.is_finite() or a>b:
            raise ValueError("non-finite or unordered envelope")
        return a,b
    a0,a1=bounds(asc)
    m0,m1=bounds(moon)
    s0,s1=bounds(saturn)
    lo=a0+m0-s1
    hi=a1+m1-s0
    def sign(x:Decimal)->str:
        normalized=((x%Decimal(360))+Decimal(360))%Decimal(360)
        return ZODIAC[int(normalized//Decimal(30))]
    if hi-lo>=360:
        signs=set(ZODIAC)
    else:
        # Include BOTH sides of each 30° boundary that can be attained.
        k0=int(lo//Decimal(30))
        k1=int(hi//Decimal(30))+1
        cuts=[Decimal(30)*k for k in range(k0,k1+1)
              if lo<Decimal(30)*k<hi]
        parts=[lo]+cuts+[hi]
        samples={lo,hi}
        for left,right in zip(parts,parts[1:]):
            samples.add((left+right)/2)
        signs={sign(x) for x in samples}
    indicators=sorted({name in CAMPAIGN_INDICATOR_SIGNS for name in signs})
    return {
        "unwrapped_lot_min_deg":str(lo),
        "unwrapped_lot_max_deg":str(hi),
        "possible_signs":sorted(signs),
        "possible_indicator_values":indicators,
        "constant_indicator_if_envelopes_proven":len(indicators)==1,
        "input_enclosures_certified":bounds_continuously_certified,
        "Ascendant_angle_audit_complete":False,
        "real_person_claim_allowed":False
    }
