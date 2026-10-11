#!/usr/bin/env python3
"""Reproducible geocentric tropical Moshier (NOT canonical SWIEPH) outer-planet transit chronology.
Samples every <=2 days, bracketed roots for longitude aspects/ingresses. 2036-01-01 through 2087-01-01.

Run: python scripts/research/mundane_outer_cycles_2036_2086.py OUTPUT.json
Requires: pyswisseph, numpy, scipy. Uses independent Moshier ephemeris;
not a verified canonical Swiss-ephemeris production calculation.
"""
import sys, json, math, datetime as dt
import numpy as np
from scipy.optimize import brentq
import swisseph as swe

START = (2036,1,1)
END = (2087,1,1)
FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED
BODIES={'Jupiter':swe.JUPITER,'Saturn':swe.SATURN,'Uranus':swe.URANUS,'Neptune':swe.NEPTUNE,'Pluto':swe.PLUTO}
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
J0 = swe.julday(*START,0)
J1 = swe.julday(*END,0)
TIMES = np.linspace(J0,J1,round((J1-J0)/2)+1)

CACHE={}
for name,p in BODIES.items():
    vals=[]
    for t in TIMES:
        values,returned=swe.calc_ut(float(t),p,FLAGS)
        if not (returned & swe.FLG_MOSEPH): raise RuntimeError(f'Moshier not returned for {name}: {returned}')
        vals.append(values[0])
    CACHE[name]=np.array(vals)

def lon(name,jd):
    vals,returned=swe.calc_ut(float(jd),BODIES[name],FLAGS)
    assert returned & swe.FLG_MOSEPH
    return vals[0]

def isotime(j):
    year,month,day,hour=swe.revjul(float(j),swe.GREG_CAL)
    return (dt.datetime(year,month,day,tzinfo=dt.timezone.utc)+dt.timedelta(hours=hour)).isoformat(timespec='minutes')

def wrapped_to_near(wrapped,reference):
    return wrapped + 360*round((reference-wrapped)/360)

def crossing(name,values,mode):
    events=[]
    un=np.rad2deg(np.unwrap(np.deg2rad(values),discont=np.pi))
    for i,(t0,t1) in enumerate(zip(TIMES[:-1],TIMES[1:])):
        left,right=un[i],un[i+1]
        amin,amax=min(left,right),max(left,right)
        if mode=='signs':
            thresholds=range(math.ceil(amin/30),math.floor(amax/30)+1)
            targets=[k*30 for k in thresholds]
        else:
            a,b=amin-360,amax+360
            targets=[360*k+deg for k in range(math.floor(a/360),math.ceil(b/360)+1) for deg in (0,60,90,120,180,240,270,300)]
        for target in targets:
            if not amin-1e-12 <= target <= amax+1e-12:continue
            if mode=='signs':
                def evalfunc(j,tar=target,base=left):return wrapped_to_near(lon(name,j),base)-tar
            else:
                body1,body2=name
                def evalfunc(j,tar=target,base=left):return wrapped_to_near((lon(body1,j)-lon(body2,j))%360,base)-tar
            r=brentq(evalfunc,float(t0),float(t1),xtol=1e-8) if abs(left-target)>1e-10 and abs(right-target)>1e-10 else (float(t0) if abs(left-target)<1e-10 else float(t1))
            if events and abs(events[-1]['jd']-r)<1e-6:continue
            if mode=='signs':
                before=int(((target+(-0.01 if right>left else 0.01))%360)//30)
                after=int(((target+(0.01 if right>left else -0.01))%360)//30)
                e={'planet':name,'from':SIGNS[before],'to':SIGNS[after], 'direction':'direct' if right>left else 'retrograde', 'utc':isotime(r),'jd':r}
            else:
                deg=int(round(target))%360
                major=min(deg,360-deg)
                e={'pair':list(name),'aspect':{0:'conjunction',60:'sextile',90:'square',120:'trine',180:'opposition'}[major], 'degree':major,'utc':isotime(r),'jd':r}
            events.append(e)
    return events

planet_ingresses=[]
for name in BODIES:
    if name=='Jupiter':continue
    planet_ingresses.extend(crossing(name,CACHE[name],'signs'))
planet_ingresses.sort(key=lambda r:r['jd'])

all_aspects=[]
from itertools import combinations
for p1,p2 in combinations(BODIES.keys(),2):
    dif=(CACHE[p1]-CACHE[p2])%360
    all_aspects.extend(crossing((p1,p2),dif,'aspects'))
all_aspects.sort(key=lambda r:r['jd'])

bodypairs=['Jupiter/Saturn','Saturn/Uranus','Saturn/Neptune','Saturn/Pluto','Uranus/Neptune','Uranus/Pluto','Neptune/Pluto']
summary={}
for k in bodypairs:
    aa=[a for a in all_aspects if '/'.join(a['pair'])==k]
    summary[k]=[{z:a[z] for z in ('utc','aspect','degree')} for a in aa]

result={'period':'2036-01-01 to 2087-01-01 UTC','engine':{'swisseph_python':swe.version,'flags_requested':FLAGS,'mode':'MOSEPH','position_frame':'geocentric tropical ecliptic', 'sample_days':(TIMES[1]-TIMES[0]),'root_method':'scipy.optimize.brentq'},'sign_ingresses':[{k:v for k,v in x.items() if k!='jd'} for x in planet_ingresses],'aspects':[{k:v for k,v in x.items() if k!='jd'} for x in all_aspects],'summary':summary}
output = sys.argv[1] if len(sys.argv) > 1 else 'MUNDANE_ASTROLOGY_GLOBAL_2036_2086_EPHEMERIS.json'
with open(output,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,ensure_ascii=False)
print('COUNT ingresses',len(planet_ingresses),'aspects',len(all_aspects))
print('\n===== SIGN INGRESSES =====')
for e in planet_ingresses:
 if e['planet']!='Saturn':print(e['utc'][:10], e['planet'],e['from'],'->',e['to'],e['direction'])
print('\n===== ASPECTS (Outer 3) =====')
for a in all_aspects:
 if set(a['pair'])<=set(['Uranus','Neptune','Pluto']): print(a['utc'][:10],'/'.join(a['pair']),a['aspect'])
print('\n===== ASPECTS (Saturn to Outer 3 & Jupiter-Saturn conjs) =====')
for a in all_aspects:
 if ('Saturn' in a['pair'] and ('Jupiter' not in a['pair'] or a['aspect']=='conjunction')): print(a['utc'][:10],'/'.join(a['pair']),a['aspect'])
