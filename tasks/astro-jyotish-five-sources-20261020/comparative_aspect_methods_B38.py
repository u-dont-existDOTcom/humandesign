"""Three explicitly separate classical-aspect conventions, exploratory source arithmetic only.

BPHS Ch26.6-9: general exact graha aspect as a function of oriented longitude.
Jaimini 1.1.2 via Rath lesson13: Rasi-to-Rasi aspects (not graha drishti).
Saravali Ch4.32-33: source-restored discrete graha aspect support/fractions.
No birth records, personality predictions, medical or causal outcomes.
"""
from __future__ import annotations
from fractions import Fraction
from math import isfinite

MOVABLE=frozenset((0,3,6,9))
FIXED=frozenset((1,4,7,10))
DUAL=frozenset((2,5,8,11))
SARAVALI_FRACTION={3:Fraction(1,4),10:Fraction(1,4),5:Fraction(1,2),9:Fraction(1,2),4:Fraction(3,4),8:Fraction(3,4),7:Fraction(1,1)}

def _zodiac_sign(n: int)->None:
    if type(n) is not int or n not in range(12):raise ValueError('Expected whole-sign index 0..11')

def jaimini_rasi_aspect(a:int,b:int)->bool:
    """Rath's commentary on Jaimini 1.1.2, not literal single-sutra wording."""
    _zodiac_sign(a);_zodiac_sign(b)
    if a==b:return False
    if a in DUAL:return b in DUAL
    if b in DUAL:return False
    if (a in MOVABLE and b in FIXED) or (a in FIXED and b in MOVABLE):
        return (a-b)%12 not in (1,11)
    return False

def minimum_sign_longitude_gap_deg(a:int,b:int)->int:
    _zodiac_sign(a);_zodiac_sign(b)
    n=min(abs(a-b),12-abs(a-b))
    return max(0,n-1)*30

def saravali_discrete_fraction(a:int,b:int)->Fraction:
    _zodiac_sign(a);_zodiac_sign(b)
    house=(b-a)%12+1
    return SARAVALI_FRACTION.get(house,Fraction(0,1))

def bphs_general_exact_virupas(separation_deg:float)->float:
    """General BPHS graha angle rules Ch26 (not Mars/Jupiter/Saturn exceptions).

    Oriented (target_lon-source_lon)%360, with 0<=sep<360. Piecewise
    0..30 and 300..360 are zero. Do not use a zodiac sign difference here.
    """
    if isinstance(separation_deg,bool) or not isinstance(separation_deg,(int,float)) or not isfinite(separation_deg) or not 0<=separation_deg<360:
        raise ValueError('Expected finite oriented longitude gap 0<=d<360')
    d=float(separation_deg)
    if d<=30 or d>=300:return 0.0
    if d<=60:return (d-30)/2
    if d<=90:return d-45
    if d<=120:return 30+(120-d)/2
    if d<=150:return 150-d
    if d<=180:return 2*(d-150)
    return (300-d)/2

def bound_all_sun_mercury_aspects(max_abs_longitude_gap:float=29.0)->dict[str,object]:
    """Conservative Mercury/Sun longitude separation assumed <30 degrees.

    No ephemerides used. Evaluate two directions and all pairs of 30-deg bins.
    """
    if not 0<max_abs_longitude_gap<30:raise ValueError('Bound must be positive and <30deg')
    ra=[];sa=[];bp=[]
    for sun in range(12):
      for mercury in range(12):
        if minimum_sign_longitude_gap_deg(sun,mercury)>max_abs_longitude_gap:continue
        if jaimini_rasi_aspect(sun,mercury):ra.append((sun,mercury))
        if saravali_discrete_fraction(sun,mercury):sa.append((sun,mercury))
    # All oriented longitudes within +/- Mercury bound; positive direction
    # d in [0,maxgap] or [360-maxgap,360) and BPHS is zero throughout.
    for d in [0.0,max_abs_longitude_gap,360-max_abs_longitude_gap,359.99]:
      if bphs_general_exact_virupas(d)>0:bp.append(d)
    return {'jaimini_rasi_sun_mercury_possibilities':ra,
            'saravali_graha_sun_mercury_possibilities':sa,
            'bphs_exact_positive_boundary_counterexamples':bp,
            'assumption':f'Mercury solar longitude gap <= {max_abs_longitude_gap} degrees'}
