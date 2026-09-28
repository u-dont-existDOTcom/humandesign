#!/usr/bin/env python3
import json, math, time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import swisseph as swe
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot, datetime_to_jd
from hdmatch.evaluation.astrohd_v14_rules import registry, feature_row

ROOT=Path(__file__).resolve().parents[1]
TASK=ROOT/'tasks/scenario-owner-recovery-calibration-20260923'
MODEL=TASK/'ASTROHD-V14-SIX-RULE-MODEL-20260925.json'
EPHE=Path('/home/joel/humandesign-century-runtime-20260925/ephe')
OUT=ROOT/'experiments/astrohd/structural_recoverability_pilot_1000_20260928.json'
START=datetime(1926,8,24,10,42,tzinfo=timezone.utc)
END=datetime(2026,8,24,10,42,tzinfo=timezone.utc)
LAT,LON=39.9526,-75.1652
N=1000
SEED=20260928
ASPECTS=np.array([0.,60.,90.,120.,180.])
BODIES=['sun','moon','mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto']

def circ(a,b):
    return abs((a-b+180.0)%360.0-180.0)

def geom(snapshot):
    longs=dict(snapshot.tropical_longitudes)
    jd=datetime_to_jd(snapshot.when)
    flags=swe.FLG_SWIEPH|swe.FLG_SPEED
    for name,bid in [('uranus',swe.URANUS),('neptune',swe.NEPTUNE),('pluto',swe.PLUTO)]:
        longs[name]=float(swe.calc_ut(jd,bid,flags)[0][0])%360.0
    vals=np.array([longs[b] for b in BODIES])
    orbs=[]
    for i in range(len(vals)):
        for j in range(i+1,len(vals)):
            sep=circ(vals[i],vals[j])
            orbs.append(float(np.min(np.abs(ASPECTS-sep))))
    o=np.array(orbs)
    return {
        'n_le_1':int(np.sum(o<=1.0)),
        'n_le_2':int(np.sum(o<=2.0)),
        'n_le_3':int(np.sum(o<=3.0)),
        'exactness3':float(np.sum(np.maximum(0.0,3.0-o))),
    }

model=json.loads(MODEL.read_text())
consensus=json.loads((ROOT/model['source_map_path']).read_text())
all_rules=registry(consensus,{d['domain_id'] for d in consensus['domains']})
lookup={r['rule_id']:r for r in all_rules}
rules=[lookup[x] for x in model['selected_rule_ids']]

span_minutes=round((END-START).total_seconds()/60)
rng=np.random.Generator(np.random.PCG64(SEED))
indices=np.sort(rng.choice(span_minutes+1,size=N,replace=False))
rows=[]
t0=time.perf_counter()
for k,idx in enumerate(indices):
    when=START + __import__('datetime').timedelta(minutes=int(idx))
    snap=build_snapshot(when,latitude=LAT,longitude=LON,ephemeris_root=EPHE)
    values=feature_row(snap,rules)
    bits=''.join(str(int(v>0)) for v in values)
    signature=sum((int(v>0)<<i) for i,v in enumerate(values))
    rows.append({'minute_index':int(idx),'utc':when.isoformat(),'signature':signature,
                 'bits':bits,'score':int(values.sum()),**geom(snap)})
elapsed=time.perf_counter()-t0

counts=Counter(r['signature'] for r in rows)
for r in rows:
    c=counts[r['signature']]
    r['sample_signature_count']=c
    r['sample_signature_fraction']=c/N
    r['sample_self_information_bits']=-math.log2(c/N)

owner_when=datetime(1985,1,29,10,25,tzinfo=timezone.utc)
owner_snap=build_snapshot(owner_when,latitude=LAT,longitude=LON,ephemeris_root=EPHE)
owner_values=feature_row(owner_snap,rules)
owner_sig=sum((int(v>0)<<i) for i,v in enumerate(owner_values))
owner_geom=geom(owner_snap)
owner_sample_count=counts.get(owner_sig,0)

sig_table=[]
for sig,c in sorted(counts.items(),key=lambda x:(x[1],x[0])):
    sig_table.append({'signature':sig,'count':c,'fraction':c/N,
                      'self_information_bits':-math.log2(c/N)})
info=np.array([r['sample_self_information_bits'] for r in rows])
result={
 'method':{'n':N,'seed':SEED,'start_utc':START.isoformat(),'end_utc_inclusive':END.isoformat(),
           'sampling':'uniform distinct minute-grid samples','model_version':model['version'],
           'selected_rule_ids':model['selected_rule_ids']},
 'runtime':{'elapsed_seconds':elapsed,'charts_per_second':N/elapsed},
 'signature_distribution':{'distinct_observed':len(counts),'table':sig_table,
    'random_chart_information_bits':{'mean':float(info.mean()),'median':float(np.median(info)),
      'p90':float(np.quantile(info,.9)),'p95':float(np.quantile(info,.95)),
      'max':float(info.max())}},

 'owner':{'utc':owner_when.isoformat(),'rule_values':owner_values.tolist(),
          'signature':owner_sig,'sample_signature_count':owner_sample_count,
          'sample_signature_fraction':owner_sample_count/N,**owner_geom},
 'geometry_summary':{
   k:{'mean':float(np.mean([r[k] for r in rows])),
      'median':float(np.median([r[k] for r in rows])),
      'p95':float(np.quantile([r[k] for r in rows],.95))}
   for k in ['n_le_1','n_le_2','n_le_3','exactness3']
 },
 'rows':rows
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
print('OUTPUT',OUT)