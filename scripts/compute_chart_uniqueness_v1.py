#!/usr/bin/env python3
"""Compute frozen target-independent chart uniqueness v1."""
from __future__ import annotations
import argparse,json,time,math
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime,timezone,timedelta
from pathlib import Path
import numpy as np
import swisseph as swe
from scipy.stats import rankdata,norm

ROOT=Path(__file__).resolve().parents[1]
EPHE=Path('/home/joel/humandesign-century-runtime-20260925/ephe')
OUT=ROOT/'experiments/astrohd/chart_uniqueness_v1_owner_20260928.json'
START=datetime(1926,8,24,10,42,tzinfo=timezone.utc)
END=datetime(2026,8,24,10,42,tzinfo=timezone.utc)
OWNER=datetime(1985,1,29,10,25,tzinfo=timezone.utc)
LAT,LON=39.9526,-75.1652
B=100000; C=50000; SEED=20260928; WORKERS=8
TARGETS=np.array([0.,60.,90.,120.,180.])
BODIES=[swe.SUN,swe.MOON,swe.MERCURY,swe.VENUS,swe.MARS,swe.JUPITER,swe.SATURN,swe.URANUS,swe.NEPTUNE,swe.PLUTO]
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED

def initialize():
    swe.set_ephe_path(str(EPHE))
def jd(dt):
    h=dt.hour+dt.minute/60+dt.second/3600+dt.microsecond/3.6e9
    return swe.julday(dt.year,dt.month,dt.day,h,swe.GREG_CAL)

def circ(a,b):
    return abs((a-b+180.0)%360.0-180.0)

def features_from_jd(j):
    vals=np.empty(10)
    for i,b in enumerate(BODIES):
        x,ret=swe.calc_ut(float(j),b,FLAGS)
        if ret&swe.FLG_MOSEPH or not ret&swe.FLG_SWIEPH:
            raise RuntimeError(f'ephemeris fallback jd={j} body={b} flags={ret}')
        vals[i]=float(x[0])%360.0
    out=np.empty(55,dtype=np.float32); k=0
    for i in range(10):
        for m in range(i+1,10):
            s=circ(vals[i],vals[m])
            out[k]=float(np.min(np.abs(TARGETS-s))); k+=1
    _,a=swe.houses_ex(float(j),LAT,LON,b'P',0)
    asc=float(a[0])%360.; mc=float(a[1])%360.
    angles=(asc,mc,(asc+180)%360,(mc+180)%360)
    for i in range(10):
        out[k]=min(circ(vals[i],x) for x in angles); k+=1
    return out

def worker(indices,start_jd):
    initialize(); arr=np.empty((len(indices),55),dtype=np.float32)
    for i,idx in enumerate(indices): arr[i]=features_from_jd(start_jd+int(idx)/1440.0)
    return arr
def generate(indices,start_jd):
    parts=np.array_split(indices,WORKERS)
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        arrays=list(pool.map(worker,parts,[start_jd]*len(parts)))
    return np.vstack(arrays)

def baseline_transform(x):
    n=x.shape[0]; z=np.empty_like(x,dtype=np.float64)
    lo=.5/n; hi=1-.5/n
    for j in range(x.shape[1]):
        q=(rankdata(x[:,j],method='average')-.5)/n
        z[:,j]=norm.ppf(np.clip(q,lo,hi))
    return z

def apply_transform(base,x):
    n=base.shape[0]; z=np.empty_like(x,dtype=np.float64); qout=np.empty_like(x,dtype=np.float64)
    lo=.5/n; hi=1-.5/n
    for j in range(base.shape[1]):
        s=np.sort(base[:,j])
        q=(np.searchsorted(s,x[:,j],side='right')-.5)/n
        q=np.clip(q,lo,hi); qout[:,j]=q; z[:,j]=norm.ppf(q)
    return z,qout

def inv_cov(z):
    c=np.cov(z,rowvar=False)
    shr=.9*c+.1*np.eye(c.shape[0])
    return np.linalg.inv(shr)
def d2(z,inv):
    return np.einsum('ij,jk,ik->i',z,inv,z)

def score_family(zb,zc,zq,cols):
    inv=inv_cov(zb[:,cols])
    cal=d2(zc[:,cols],inv); query=float(d2(zq[:,cols],inv)[0])
    pct=(1+int(np.sum(cal<=query)))/(len(cal)+1)
    tail=(1+int(np.sum(cal>=query)))/(len(cal)+1)
    return {'d2':query,'rarity_percentile':pct,'upper_tail_probability':tail,
            'rarity_bits':-math.log2(tail),
            'calibration_median_d2':float(np.median(cal)),
            'calibration_p95_d2':float(np.quantile(cal,.95)),
            'calibration_p99_d2':float(np.quantile(cal,.99)),
            'calibration_max_d2':float(np.max(cal))}

def main():
    initialize(); start_jd=jd(START)
    total=round((END-START).total_seconds()/60)+1
    rng=np.random.Generator(np.random.PCG64(SEED))
    ids=rng.choice(total,size=B+C,replace=False)
    t=time.perf_counter(); base=generate(ids[:B],start_jd); mid=time.perf_counter()
    cal=generate(ids[B:],start_jd); generated=time.perf_counter()
    owner=np.asarray([features_from_jd(jd(OWNER))],dtype=np.float32)
    zb=baseline_transform(base); zc,qc=apply_transform(base,cal); zq,qq=apply_transform(base,owner)
    all_score=score_family(zb,zc,zq,np.arange(55))
    planet_score=score_family(zb,zc,zq,np.arange(45))
    angle_score=score_family(zb,zc,zq,np.arange(45,55))
    def marginal_surprisal(q):
        p=np.maximum(2*np.minimum(q,1-q),1/B)
        return np.mean(-np.log2(p),axis=1)
    cal_ms=marginal_surprisal(qc); owner_ms=float(marginal_surprisal(qq)[0])
    ms_tail=(1+int(np.sum(cal_ms>=owner_ms)))/(C+1)
    result={
      'schema':'target-independent-chart-uniqueness-v1-result',
      'manifest':'reference/research/chart_uniqueness_metric_v1_manifest.json',
      'reference':{'baseline_n':B,'calibration_n':C,'seed':SEED,'latitude':LAT,'longitude':LON,
                   'universe_minutes':total},
      'runtime':{'baseline_seconds':mid-t,'calibration_seconds':generated-mid,
                 'total_feature_generation_seconds':generated-t},
      'owner':{'utc':OWNER.isoformat(),'primary_all55':all_score,
               'planetary_only45':planet_score,'angle_only10':angle_score,
               'mean_marginal_surprisal':{'score':owner_ms,'upper_tail_probability':ms_tail,
                  'rarity_percentile':1-ms_tail+1/(C+1),'rarity_bits':-math.log2(ms_tail)},
               'raw_features':owner[0].astype(float).tolist()},
      'calibration':{'mean_marginal_surprisal_median':float(np.median(cal_ms)),
                     'mean_marginal_surprisal_p95':float(np.quantile(cal_ms,.95)),
                     'mean_marginal_surprisal_p99':float(np.quantile(cal_ms,.99)),
                     'mean_marginal_surprisal_max':float(np.max(cal_ms))}
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    print('OUTPUT',OUT)
if __name__=='__main__': main()