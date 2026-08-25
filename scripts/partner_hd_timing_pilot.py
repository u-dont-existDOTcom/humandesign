#!/usr/bin/env python3
"""Generate slow-transit Human Design connection-state periods for the partner pilot.

Uses verified SWIEPH and exact 88-degree Design roots for natal charts. Current
slow planetary transit gates are overlaid on the static connection chart. The
output is exploratory relationship-conditioning data and does not modify natal
V4.3 NetInformation.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import swisseph as swe

REPO = Path(__file__).resolve().parents[1]
EPHE = REPO / "data" / "ephemeris"
OUT = REPO / "reference" / "research" / "partner_future_joel_bee_2026_2040_hd_raw.json"

FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
EPH_MASK = swe.FLG_JPLEPH | swe.FLG_SWIEPH | swe.FLG_MOSEPH
WHEEL_START = 302.0
GATE_SPAN = 360.0 / 64.0
GATE_SEQ = [41,19,13,49,30,55,37,63,22,36,25,17,21,51,42,3,27,24,2,23,8,20,16,35,45,12,15,52,39,53,62,56,31,33,7,4,29,59,40,64,47,6,46,18,48,57,32,50,28,44,1,43,14,34,9,5,26,11,10,58,38,54,61,60]
OPP = {GATE_SEQ[i]: GATE_SEQ[(i + 32) % 64] for i in range(64)}
BODIES = {
    "sun": swe.SUN, "moon": swe.MOON, "mercury": swe.MERCURY,
    "venus": swe.VENUS, "mars": swe.MARS, "jupiter": swe.JUPITER,
    "saturn": swe.SATURN, "uranus": swe.URANUS, "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO, "north_node": swe.TRUE_NODE,
}
SLOW_TRANSITS = {
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
    "north_node": swe.TRUE_NODE,
}
CHANNELS = [
    (4,63),(24,61),(47,64),(11,56),(17,62),(23,43),(1,8),(7,31),(10,20),(13,33),
    (12,22),(16,48),(20,34),(20,57),(21,45),(35,36),(2,14),(5,15),(10,34),(29,46),
    (10,57),(25,51),(3,60),(9,52),(42,53),(6,59),(27,50),(34,57),(18,58),(19,49),
    (28,38),(30,41),(32,54),(37,40),(39,55),(26,44),
]
CHANNELS = [tuple(sorted(c)) for c in CHANNELS]
GC = {
64:'Head',61:'Head',63:'Head',47:'Ajna',24:'Ajna',4:'Ajna',43:'Ajna',17:'Ajna',11:'Ajna',
62:'Throat',23:'Throat',56:'Throat',35:'Throat',12:'Throat',45:'Throat',33:'Throat',31:'Throat',8:'Throat',20:'Throat',16:'Throat',
1:'G',2:'G',7:'G',10:'G',13:'G',15:'G',25:'G',46:'G',21:'Heart',26:'Heart',40:'Heart',51:'Heart',
36:'SolarPlexus',22:'SolarPlexus',37:'SolarPlexus',6:'SolarPlexus',49:'SolarPlexus',55:'SolarPlexus',30:'SolarPlexus',
5:'Sacral',14:'Sacral',29:'Sacral',34:'Sacral',59:'Sacral',9:'Sacral',3:'Sacral',42:'Sacral',27:'Sacral',
48:'Spleen',57:'Spleen',44:'Spleen',50:'Spleen',32:'Spleen',28:'Spleen',18:'Spleen',
58:'Root',38:'Root',54:'Root',53:'Root',60:'Root',52:'Root',19:'Root',39:'Root',41:'Root'
}
ALL_CENTERS = ['Head','Ajna','Throat','G','Heart','SolarPlexus','Sacral','Spleen','Root']
START = datetime(2026,1,1,tzinfo=timezone.utc)
END = datetime(2041,1,1,tzinfo=timezone.utc)


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def jd(dt: datetime) -> float:
    dt=dt.astimezone(timezone.utc)
    hh=dt.hour+dt.minute/60+dt.second/3600+dt.microsecond/3.6e9
    return swe.julday(dt.year,dt.month,dt.day,hh,swe.GREG_CAL)


def dt_from_jd(x: float) -> datetime:
    y,m,d,hh=swe.revjul(x,swe.GREG_CAL); h=int(hh); mf=(hh-h)*60; mi=int(mf); sf=(mf-mi)*60; s=int(sf); us=int(round((sf-s)*1e6))
    if us>=1_000_000: s+=1; us-=1_000_000
    return datetime(y,m,d,h,mi,s,us,tzinfo=timezone.utc)


def calc(x: float, body: int) -> tuple[float,float]:
    xx,ret=swe.calc_ut(x,body,FLAGS); used=ret&EPH_MASK
    if used!=swe.FLG_SWIEPH:
        raise RuntimeError(f'EPHEMERIS_FALLBACK body={body} jd={x} used={used} ret={ret}')
    return xx[0]%360,xx[3]


def gate(lon: float) -> int:
    i=int(math.floor(((lon-WHEEL_START)%360)/GATE_SPAN))%64
    return GATE_SEQ[i]


def design_jd(birth: float) -> float:
    lb,_=calc(birth,swe.SUN); x=birth-89.3
    for _ in range(10):
        ld,sp=calc(x,swe.SUN); f=((lb-ld)%360)-88.0
        if abs(f)<1e-10: return x
        x += f/max(abs(sp),1e-9)
    lo,hi=birth-100,birth-75
    def f(t): return ((lb-calc(t,swe.SUN)[0])%360)-88.0
    flo=f(lo)
    for _ in range(80):
        mid=(lo+hi)/2; fm=f(mid)
        if abs(fm)<1e-10 or (hi-lo)*86400<0.1: return mid
        if flo*fm<=0: hi=mid
        else: lo=mid; flo=fm
    return (lo+hi)/2


def natal_gates(dt: datetime) -> set[int]:
    bj=jd(dt); dj=design_jd(bj); gates=set()
    for t in (bj,dj):
        for name,b in BODIES.items():
            g=gate(calc(t,b)[0]); gates.add(g)
            if name in ('sun','north_node'): gates.add(OPP[g])
    return gates


def fingerprint(gates: set[int]) -> dict:
    channels=[c for c in CHANNELS if c[0] in gates and c[1] in gates]
    centers=set(); adj={}
    for a,b in channels:
        x,y=GC[a],GC[b]; centers|={x,y}; adj.setdefault(x,set()).add(y); adj.setdefault(y,set()).add(x)
    seen=set(); components=0
    for c in centers:
        if c in seen: continue
        components+=1; stack=[c]; seen.add(c)
        while stack:
            x=stack.pop()
            for y in adj.get(x,()):
                if y not in seen: seen.add(y); stack.append(y)
    n=len(centers)
    label={9:'9+0 Nowhere to go',8:'8+1 Have some fun',7:'7+2 Work to do',6:'6+3 Better to be free',5:'5+4 Not a relationship anymore'}.get(n,f'{n}+{9-n}')
    return {
        'defined_center_count':n,
        'open_centers':[c for c in ALL_CENTERS if c not in centers],
        'definition_components':components,
        'surface_label':label,
        'channels':['-'.join(map(str,c)) for c in channels],
    }


def transit_gate_state(dt: datetime) -> tuple[dict[str,int],set[int]]:
    x=jd(dt); by={name:gate(calc(x,b)[0]) for name,b in SLOW_TRANSITS.items()}
    return by,set(by.values())


def exact_gate_events() -> list[float]:
    sj,ej=jd(START),jd(END); events=[]
    for name,b in SLOW_TRANSITS.items():
        t=sj; l0,s0=calc(t,b); g0=gate(l0)
        step=0.25 if name=='jupiter' else 0.5
        while t<ej:
            u=min(t+step,ej); l1,s1=calc(u,b); g1=gate(l1)
            if g1!=g0:
                # State bisection works even for retrograde crossings when one crossing occurs in step.
                lo,hi=t,u; old=g0
                for _ in range(50):
                    if (hi-lo)*86400<0.25: break
                    m=(lo+hi)/2
                    if gate(calc(m,b)[0])==old: lo=m
                    else: hi=m
                events.append((lo+hi)/2)
            t=u; g0=g1
    events=sorted(events)
    ded=[]
    for e in events:
        if not ded or abs(e-ded[-1])*86400>0.5: ded.append(e)
    return ded


def periods_for_pair(a_gates: set[int], b_gates: set[int], boundaries: list[float]) -> list[dict]:
    static=a_gates|b_gates
    bounds=[jd(START)]+[x for x in boundaries if jd(START)<x<jd(END)]+[jd(END)]
    rows=[]
    for a,b in zip(bounds[:-1],bounds[1:]):
        mid=dt_from_jd((a+b)/2); by,tg=transit_gate_state(mid); fp=fingerprint(static|tg)
        row={
            'start_utc':dt_from_jd(a).isoformat(),
            'end_utc':dt_from_jd(b).isoformat(),
            'transit_gates':by,
            **fp,
        }
        sig=(fp['defined_center_count'],tuple(fp['open_centers']),fp['definition_components'],fp['surface_label'],tuple(fp['channels']),tuple(sorted(by.items())))
        if rows and rows[-1]['_sig']==sig:
            rows[-1]['end_utc']=row['end_utc']
        else:
            row['_sig']=sig; rows.append(row)
    for r in rows: r.pop('_sig',None)
    return rows


def main() -> None:
    for p in (EPHE/'sepl_18.se1',EPHE/'semo_18.se1'):
        if not p.is_file(): raise SystemExit('Missing Swiss file: '+str(p))
    swe.set_ephe_path(str(EPHE))
    # Probes
    for d in (datetime(1985,1,29,10,25,tzinfo=timezone.utc),datetime(1989,6,19,12,tzinfo=timezone.utc),START,END-timedelta(days=1)):
        for b in SLOW_TRANSITS.values(): calc(jd(d),b)

    A_dt=datetime(1985,1,29,10,25,tzinfo=timezone.utc)
    A=natal_gates(A_dt)
    douala=ZoneInfo('Africa/Douala')
    B_times={
        'B_early':datetime(1989,6,19,6,0,tzinfo=douala).astimezone(timezone.utc),
        'B_mid':datetime(1989,6,19,13,0,tzinfo=douala).astimezone(timezone.utc),
        'B_late':datetime(1989,6,19,18,0,tzinfo=douala).astimezone(timezone.utc),
    }
    boundaries=exact_gate_events()
    bdata={}
    for label,bdt in B_times.items():
        bg=natal_gates(bdt)
        bdata[label]={
            'birth_utc':bdt.isoformat(),
            'natal_gates':sorted(bg),
            'static_connection':fingerprint(A|bg),
            'slow_transit_periods':periods_for_pair(A,bg,boundaries),
        }

    data={
        'protocol':'partner-future-concordance-v1-exploratory-HD',
        'status':'raw_pair_specific_corroboration_after_individual_Western_generation',
        'horizon':[START.isoformat(),END.isoformat()],
        'ephemeris':{
            'requested':'SWIEPH','returned':'SWIEPH or abort',
            'sepl_18_sha256':sha256(EPHE/'sepl_18.se1'),
            'semo_18_sha256':sha256(EPHE/'semo_18.se1'),
        },
        'person_A_natal_gates':sorted(A),
        'person_B_time_states':bdata,
        'transits_included':list(SLOW_TRANSITS),
        'notes':[
            'Slow-transit gates are treated as temporary conditioning/weather, not fate.',
            'Bee time state is not selected from pair fit.',
            'This is pair-specific corroboration and does not alter natal V4.3 scoring.',
        ],
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('wrote',OUT,'sha256',sha256(OUT),'boundary_count',len(boundaries))
    for label,rec in bdata.items():
        print(label,'static',rec['static_connection']['surface_label'],'components',rec['static_connection']['definition_components'],'periods',len(rec['slow_transit_periods']))

if __name__=='__main__': main()
