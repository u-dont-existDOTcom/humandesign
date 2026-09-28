#!/usr/bin/env python3
import json, math
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import swisseph as swe

N=10000
SEED=20260928
START=datetime(1926,8,24,10,42,tzinfo=timezone.utc)
END=datetime(2026,8,24,10,42,tzinfo=timezone.utc)
OWNER=datetime(1985,1,29,10,25,tzinfo=timezone.utc)
OWNER_OPT=datetime(1985,1,29,10,36,tzinfo=timezone.utc)
LAT=39.9526
LON=-75.1652
EPHE='/home/joel/humandesign-century-runtime-20260925/ephe'
OUT=Path('experiments/astrohd/owner_orb_tightness_10k_20260928.json')
BODIES=[
 ('Sun',swe.SUN),('Moon',swe.MOON),('Mercury',swe.MERCURY),('Venus',swe.VENUS),
 ('Mars',swe.MARS),('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Uranus',swe.URANUS),
 ('Neptune',swe.NEPTUNE),('Pluto',swe.PLUTO)
]
TARGETS=np.array([0.,60.,90.,120.,180.])
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED

def jd(dt):
    h=dt.hour+dt.minute/60+dt.second/3600+dt.microsecond/3.6e9
    return swe.julday(dt.year,dt.month,dt.day,h,swe.GREG_CAL)

def circ(a,b):
    return abs((a-b+180.0)%360.0-180.0)

def chart_metrics(j):
    longs={}
    for name,bid in BODIES:
        x,ret=swe.calc_ut(float(j),bid,FLAGS)
        if ret & swe.FLG_MOSEPH or not ret & swe.FLG_SWIEPH:
            raise RuntimeError(f'ephemeris fallback at JD {j}: {name}, flags={ret}')
        longs[name]=float(x[0])%360.0
    vals=np.array([longs[n] for n,_ in BODIES])
    orbs=[]
    for i in range(len(vals)):
        for k in range(i+1,len(vals)):
            sep=circ(vals[i],vals[k])
            orbs.append(float(np.min(np.abs(TARGETS-sep))))
    orbs=np.array(orbs)
    _,ascmc=swe.houses_ex(float(j),LAT,LON,b'P',0)
    asc=float(ascmc[0])%360.0
    mc=float(ascmc[1])%360.0
    angles=np.array([asc,mc,(asc+180)%360,(mc+180)%360])
    ad=np.array([min(circ(v,a) for a in angles) for v in vals])
    return {
      'n_le_0_5':int(np.sum(orbs<=0.5)),
      'n_le_1':int(np.sum(orbs<=1.0)),
      'n_le_2':int(np.sum(orbs<=2.0)),
      'n_le_3':int(np.sum(orbs<=3.0)),
      'excess_exactness_3deg':float(np.sum(np.maximum(0.0,3.0-orbs))),
      'minimum_major_orb':float(np.min(orbs)),
      'angular_n_le_1':int(np.sum(ad<=1.0)),
      'angular_n_le_3':int(np.sum(ad<=3.0)),
      'angular_n_le_5':int(np.sum(ad<=5.0)),
      'minimum_angular_distance':float(np.min(ad)),
      'pluto_mc_distance':float(circ(longs['Pluto'],mc)),
      'asc':asc,'mc':mc,'pluto':longs['Pluto']
    }

def wilson(k,n,z=1.959963984540054):
    if n==0:return [None,None]
    p=k/n
    den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [center-half,center+half]

def ge(arr,x):
    k=int(np.sum(arr>=x)); return {'count':k,'fraction':k/len(arr),'wilson95':wilson(k,len(arr))}
def le(arr,x):
    k=int(np.sum(arr<=x)); return {'count':k,'fraction':k/len(arr),'wilson95':wilson(k,len(arr))}

swe.set_ephe_path(EPHE)
owner=chart_metrics(jd(OWNER))
opt=chart_metrics(jd(OWNER_OPT))
rng=np.random.default_rng(SEED)
j0,j1=jd(START),jd(END)
sample_jds=rng.uniform(j0,j1,N)
keys=['n_le_0_5','n_le_1','n_le_2','n_le_3','excess_exactness_3deg','minimum_major_orb',
      'angular_n_le_1','angular_n_le_3','angular_n_le_5','minimum_angular_distance','pluto_mc_distance']
data={k:np.empty(N) for k in keys}
for idx,j in enumerate(sample_jds):
    m=chart_metrics(j)
    for k in keys:data[k][idx]=m[k]
    if (idx+1)%1000==0: print(idx+1,flush=True)

comparisons={
 'tight_counts':{
   'n_le_0_5_ge_owner':ge(data['n_le_0_5'],owner['n_le_0_5']),
   'n_le_1_ge_owner':ge(data['n_le_1'],owner['n_le_1']),
   'n_le_2_ge_owner':ge(data['n_le_2'],owner['n_le_2']),
   'n_le_3_ge_owner':ge(data['n_le_3'],owner['n_le_3']),
   'excess_exactness_ge_owner':ge(data['excess_exactness_3deg'],owner['excess_exactness_3deg'])
 },
 'angularity':{
   'minimum_angle_le_owner':le(data['minimum_angular_distance'],owner['minimum_angular_distance']),
   'pluto_mc_le_owner':le(data['pluto_mc_distance'],owner['pluto_mc_distance']),
   'pluto_mc_le_10_36_optimum':le(data['pluto_mc_distance'],opt['pluto_mc_distance']),
   'angular_n_le_3_ge_owner':ge(data['angular_n_le_3'],owner['angular_n_le_3'])
 }
}
mask=(data['n_le_1']>=owner['n_le_1'])&(data['n_le_2']>=owner['n_le_2'])&(data['n_le_3']>=owner['n_le_3'])
mask2=mask&(data['pluto_mc_distance']<=owner['pluto_mc_distance'])
comparisons['combined']={
 'all_three_tight_counts_ge_owner':{'count':int(mask.sum()),'fraction':float(mask.mean()),'wilson95':wilson(int(mask.sum()),N)},
 'tight_counts_and_pluto_mc_at_least_as_close':{'count':int(mask2.sum()),'fraction':float(mask2.mean()),'wilson95':wilson(int(mask2.sum()),N)}
}
summary={}
for k,a in data.items():
    summary[k]={'mean':float(np.mean(a)),'median':float(np.median(a)),
                'p90':float(np.quantile(a,.9)),'p95':float(np.quantile(a,.95)),
                'p99':float(np.quantile(a,.99)),'max':float(np.max(a)),'min':float(np.min(a))}
result={
 'method':{
  'sample_n':N,'seed':SEED,'sampling':'uniform random UTC instants over century interval',
  'start_utc':START.isoformat(),'end_utc':END.isoformat(),
  'location_for_angles':{'latitude':LAT,'longitude':LON,'label':'Philadelphia, PA'},
  'bodies':[n for n,_ in BODIES],
  'major_aspects_degrees':TARGETS.tolist(),
  'ephemeris':'Swiss Ephemeris files; FLG_SWIEPH|FLG_SPEED',
  'note':'Counts use each of the 45 planet pairs once and the nearest of 0/60/90/120/180. Angular distances use ASC/MC/DSC/IC.'
 },
 'owner_10_25':owner,'owner_local_optimum_10_36':opt,
 'sample_summary':summary,'comparisons':comparisons
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'owner':owner,'opt':opt,'comparisons':comparisons},indent=2))
print(OUT)