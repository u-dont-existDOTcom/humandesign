#!/usr/bin/env python3
"""Sample exact V1.4d six-rule signatures uniformly across the century minute grid."""
from __future__ import annotations
import json,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from datetime import datetime
from pathlib import Path
import numpy as np
from count_astrohd_v14_six_rule_signatures import initialize,signature
from hdmatch.evaluation.astrohd_v13_traditions import datetime_to_jd

ROOT=Path(__file__).resolve().parents[1]
EPHE=Path('/home/joel/humandesign-century-runtime-20260925/ephe')
OUT=ROOT/'experiments/astrohd/six_rule_signature_random_1m_20260928.json'
START=datetime.fromisoformat('1926-08-24T10:42:00+00:00')
TOTAL=52596001
N=1000000
WORKERS=8
SEED=20260928

def worker(start_jd,n,seed):
    rng=np.random.Generator(np.random.PCG64(seed)); counts=[0]*64
    for _ in range(n):
        idx=int(rng.integers(0,TOTAL))
        counts[signature(start_jd+idx/1440.0)]+=1
    return counts
def main():
    start_jd=datetime_to_jd(START); initialize(str(EPHE))
    sizes=[N//WORKERS+(i<N%WORKERS) for i in range(WORKERS)]
    seeds=np.random.SeedSequence(SEED).spawn(WORKERS)
    t=time.perf_counter(); total=[0]*64
    with ProcessPoolExecutor(max_workers=WORKERS,initializer=initialize,
                             initargs=(str(EPHE),)) as pool:
        futs=[pool.submit(worker,start_jd,n,int(s.generate_state(1)[0]))
              for n,s in zip(sizes,seeds)]
        done=0
        for f,n in zip(futs,sizes):
            c=f.result(); total=[a+b for a,b in zip(total,c)]; done+=n
            print(json.dumps({'done':done,'total':N}),flush=True)
    elapsed=time.perf_counter()-t
    nonzero=[{'signature':i,'count':c,'fraction':c/N}
             for i,c in enumerate(total) if c]
    result={'sample_n':N,'seed':SEED,'sampling':'uniform with replacement over exact century minute grid',
            'total_minute_universe':TOTAL,'workers':WORKERS,'elapsed_seconds':elapsed,
            'charts_per_second':N/elapsed,'distinct_signatures':len(nonzero),
            'signature_counts':total,'nonzero_signatures':nonzero}
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()