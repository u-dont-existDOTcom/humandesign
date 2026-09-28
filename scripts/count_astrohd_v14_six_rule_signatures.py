#!/usr/bin/env python3
"""Count all V1.4d six-rule Boolean signatures on an exact UTC minute grid."""
from __future__ import annotations
import argparse, json, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
import swisseph as swe
from hdmatch.evaluation.astrohd_v13_traditions import BODY_IDS, RULERS, SIGNS, datetime_to_jd
from hdmatch.relationship.western import house_for_longitude

ROOT=Path(__file__).resolve().parents[1]
LATITUDE,LONGITUDE=39.9526,-75.1652
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED
SID_FLAGS=FLAGS|swe.FLG_SIDEREAL
SIGN_RULERS=tuple(BODY_IDS[RULERS[s]] for s in SIGNS)

def initialize(ephe:str)->None:
    swe.set_ephe_path(ephe); swe.set_sid_mode(swe.SIDM_LAHIRI)

def longitude(jd:float, body:int, flags:int=FLAGS)->float:
    x,ret=swe.calc_ut(jd,body,flags)
    if not ret&swe.FLG_SWIEPH or ret&swe.FLG_MOSEPH:
        raise RuntimeError(f"ephemeris fallback {jd} {body} {ret}")
    return float(x[0])%360.0
def sep(a:float,b:float)->float:
    return abs((a-b+180.0)%360.0-180.0)

def signature(jd:float)->int:
    venus_sid=longitude(jd,swe.VENUS,SID_FLAGS)
    _,sid_asc=swe.houses_ex(jd,LATITUDE,LONGITUDE,b'P',swe.FLG_SIDEREAL)
    directional=int((int(venus_sid//30)-int((sid_asc[0]%360)//30))%12==3)
    raw,_=swe.houses_ex(jd,LATITUDE,LONGITUDE,b'R',0)
    cusps=tuple(float(x)%360.0 for x in raw[:12])
    cache={}
    def planet(body:int)->float:
        if body not in cache: cache[body]=longitude(jd,body)
        return cache[body]
    venus=planet(swe.VENUS); saturn=planet(swe.SATURN); jupiter=planet(swe.JUPITER)
    venus_house=int(house_for_longitude(venus,cusps) in {2,5})
    saturn_trine=int(any(abs(sep(saturn,x)-120.0)<=1.0 for x in (jupiter,venus)))
    lord3=SIGN_RULERS[int(cusps[2]//30)]
    lord3_house=int(house_for_longitude(planet(lord3),cusps) in {1,10})
    lord10=SIGN_RULERS[int(cusps[9]//30)]
    lord10_conj=int(any(other!=lord10 and sep(planet(lord10),planet(other))<=1.0
                        for other in (swe.JUPITER,swe.VENUS)))
    lord7=SIGN_RULERS[int(cusps[6]//30)]
    lord7_house=int(house_for_longitude(planet(lord7),cusps) in {4,7,11})
    bits=(lord3_house,saturn_trine,venus_house,directional,lord10_conj,lord7_house)
    return sum(bit<<i for i,bit in enumerate(bits))

def run_chunk(start_jd:float,first:int,stop:int)->dict:
    t=time.perf_counter(); counts=[0]*64
    for i in range(first,stop): counts[signature(start_jd+i/1440.0)]+=1
    return {'first':first,'stop':stop,'counts':counts,'elapsed':time.perf_counter()-t}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ephemeris-root',type=Path,required=True)
    p.add_argument('--start',default='1926-08-24T10:42:00Z')
    p.add_argument('--count',type=int,default=52596001)
    p.add_argument('--workers',type=int,default=6)
    p.add_argument('--chunk-size',type=int,default=100000)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); start=datetime.fromisoformat(a.start.replace('Z','+00:00'))
    start_jd=datetime_to_jd(start); initialize(str(a.ephemeris_root))
    chunks=[(x,min(a.count,x+a.chunk_size)) for x in range(0,a.count,a.chunk_size)]
    total=[0]*64; t=time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers,initializer=initialize,
                             initargs=(str(a.ephemeris_root),)) as pool:
        futs=[pool.submit(run_chunk,start_jd,x,y) for x,y in chunks]
        done=0
        for f in as_completed(futs):
            r=f.result(); total=[x+y for x,y in zip(total,r['counts'])]; done+=r['stop']-r['first']
            if done%1000000==0 or done==a.count:
                print(json.dumps({'done':done,'total':a.count,'elapsed':round(time.perf_counter()-t,3)}),flush=True)
    elapsed=time.perf_counter()-t
    result={'start':start.isoformat(),'count':a.count,'workers':a.workers,
            'elapsed_seconds':elapsed,'minutes_per_second':a.count/elapsed,
            'signature_counts':total,'distinct_signatures':sum(x>0 for x in total)}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()