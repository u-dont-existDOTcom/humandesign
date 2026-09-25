#!/usr/bin/env python3
"""Exact minute-grid maximum search of the unchanged six-rule model.

Every grid time is evaluated directly. Early rejection uses necessary conditions,
not interpolated positions. This is a maximum/tie scan, not all-score sorting.
"""
from __future__ import annotations
import argparse, ctypes as ct, fcntl, hashlib, json, os, subprocess, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import UTC, datetime, timedelta
from pathlib import Path
import numpy as np
import swisseph as swe
from hdmatch.evaluation.astrohd_v13_traditions import build_snapshot, datetime_to_jd
from hdmatch.evaluation.astrohd_v14_rules import registry, feature_row
from owner_method_admission import admit
from run_astrohd_v14_staged import dump
ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT/'tasks/scenario-owner-recovery-calibration-20260923'
START = datetime(1926,8,24,10,42,tzinfo=UTC)
END = datetime(2026,8,24,10,42,tzinfo=UTC)
COUNT = int((END-START).total_seconds()/60)+1
EXPECTED = ['lilly/lord:3/house_1_10','lilly/planet:saturn/benefic_trine',
 'lilly/planet:venus/house_2_5','phaladeepika/planet:venus/directional',
 'lilly/lord:10/benefic_conjunction','lilly/lord:7/house_4_7_11']

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

class Native:
    def __init__(self, binary, ephe):
        self.lib=ct.CDLL(str(binary))
        self.lib.scan_init.argtypes=[ct.c_char_p,ct.c_char_p]
        self.lib.scan_error.restype=ct.c_char_p
        self.lib.scan_mask.argtypes=[ct.c_double,ct.c_double,ct.c_double,ct.c_int,ct.POINTER(ct.c_int)]
        ptr=ct.POINTER(ct.c_int64)
        self.lib.scan_range.argtypes=[ct.c_double,ct.c_int64,ct.c_int64,ct.c_double,ct.c_double,ptr,ct.c_int64,ptr]
        self.lib.scan_range.restype=ct.c_int64
        if self.lib.scan_init(swe.__file__.encode(),str(ephe).encode()):
            raise RuntimeError(self.lib.scan_error().decode())
    def mask(self,when,fast=0):
        trace=ct.c_int()
        result=self.lib.scan_mask(datetime_to_jd(when),39.9526,-75.1652,fast,ct.byref(trace))
        if result<0: raise RuntimeError(self.lib.scan_error().decode())
        return result
    def scan(self,first,end):
        hits=np.empty(end-first,dtype=np.int64); counts=np.zeros(7,dtype=np.int64)
        begin=time.monotonic(); ptr=ct.POINTER(ct.c_int64)
        n=self.lib.scan_range(datetime_to_jd(START),first,end,39.9526,-75.1652,
             hits.ctypes.data_as(ptr),len(hits),counts.ctypes.data_as(ptr))
        if n<0: raise RuntimeError(self.lib.scan_error().decode())
        if int(counts.sum())!=end-first or counts[6]!=n:
            raise RuntimeError('coverage accounting failed')
        return {'first':first,'end':end,'count':end-first,'hits':hits[:n].tolist(),
                'rejection_and_maximum_counts':counts.tolist(),'seconds':time.monotonic()-begin}

def worker(binary,ephe,first,end):
    return Native(binary,ephe).scan(first,end)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ephemeris-root',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--prior-screen',type=Path)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--audit-only',action='store_true')
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    lock=(args.output_dir/'runner.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if (args.output_dir/'freeze.json').exists():
        raise ValueError('Use a new output directory; never overwrite a frozen run')
    model_path=TASK/'ASTROHD-V14-SIX-RULE-MODEL-20260925.json'
    model=json.loads(model_path.read_text())
    assert model['selected_rule_ids']==EXPECTED and model['weight_per_selected_rule']==1
    assert digest(ROOT/model['rule_module'])==model['rule_module_sha256']
    assert digest(ROOT/model['source_map_path'])==model['source_map_sha256']
    contract=json.loads((TASK/'ASTROHD-V14-EXACT-SCAN-CONTRACT-20260925.json').read_text())
    operation={'owner_outcome_id':contract['owner_outcome_id'], 'protected_dimensions':{'model_sha256':digest(model_path),'rule_ids':model['selected_rule_ids'],'cadence_seconds':60,'model_refit':False,'interpolation_used':False},'operations':['exact_minute_maximum_search'],'parent_outcome_status':'OPEN'}
    admit(contract,operation)
    source=ROOT/'src/hdmatch/evaluation/astrohd_v14_exact_scan.c'
    binary=args.output_dir/'exact_scan.so'
    command=['gcc','-O3','-Wall','-Wextra','-shared','-fPIC',str(source),'-o',str(binary),'-ldl','-lm']
    subprocess.run(command,check=True)
    native=Native(binary,args.ephemeris_root)
    consensus=json.loads((ROOT/model['source_map_path']).read_text())
    lookup={r['rule_id']:r for r in registry(consensus,{d['domain_id'] for d in consensus['domains']})}
    rules=[lookup[r] for r in EXPECTED]
    times=[START,END,datetime(1985,1,29,10,25,tzinfo=UTC),datetime(2013,1,28,8,30,tzinfo=UTC)]
    rng=np.random.default_rng(2026092502)
    times += [START+timedelta(minutes=int(m)) for m in rng.integers(0,COUNT,size=512)]
    times += [datetime(1985,1,29,10,0,tzinfo=UTC)+timedelta(seconds=s) for s in range(900,1741)]
    if args.prior_screen:
        old=json.loads(args.prior_screen.read_text())
        times += [datetime.fromisoformat(row['utc']) for row in old['hits']]
    for when in times:
        snapshot=build_snapshot(when,latitude=39.9526,longitude=-75.1652,ephemeris_root=args.ephemeris_root)
        values=feature_row(snapshot,rules).tolist()
        expected=sum(int(value)<<i for i,value in enumerate(values))
        got=native.mask(when)
        if got!=expected or ((native.mask(when,1)==63)!=(expected==63)):
            raise RuntimeError(f'Native/reference mismatch at {when}: {got} != {expected}')
    benchmark=native.scan(0,10000)
    audit={'native_reference_cases':len(times),'all_six_bits_match':True,
           'fast_rejection_matches_full_reference':True,'benchmark':benchmark}
    dump(args.output_dir/'parity.json',audit)
    print(json.dumps({'audit':'PASS','cases':len(times),'10000_minutes_seconds':benchmark['seconds']}),flush=True)
    freeze={'created_utc':datetime.now(UTC).isoformat(),'model_sha256':digest(model_path),
      'native_source_sha256':digest(source),'native_binary_sha256':digest(binary),
      'runner_sha256':digest(__file__),'swisseph_version':swe.version,
      'swisseph_binary_sha256':digest(swe.__file__),'compiler_command':command,
      'ephemeris_hashes':{p.name:digest(p) for p in args.ephemeris_root.glob('*.se1')},
      'start':START.isoformat(),'end':END.isoformat(),'count':COUNT,'cadence_seconds':60,
      'model_changed':False,'survey_changed':False,'interpolation_used':False,
      'exact_logical_pruning':'one failed clause implies score<=5; target score=6',
      'scope':'maximum/tie enumeration on every minute; not continuous-time exhaustiveness',
      'workers':args.workers,'parity_sha256':digest(args.output_dir/'parity.json')}
    dump(args.output_dir/'freeze.json',freeze)
    if args.audit_only: return
    chunks=[(first,min(COUNT,first+200000)) for first in range(0,COUNT,200000)]
    begin=time.monotonic(); completed=[]; checked=0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(worker,str(binary),str(args.ephemeris_root),a,b):(a,b) for a,b in chunks}
        for job in as_completed(jobs):
            row=job.result(); completed.append(row); checked+=row['count']
            dump(args.output_dir/f"chunk-{row['first']:08d}.json",row)
            status={'checked_minutes':checked,'total':COUNT,'chunks_completed':len(completed),
                'chunks_total':len(chunks),'seconds':round(time.monotonic()-begin,3),
                'maximum_hits_so_far':sum(len(r['hits']) for r in completed)}
            dump(args.output_dir/'progress.json',status)
            if len(completed)%10==0 or checked==COUNT:
                print(json.dumps(status),flush=True)
    completed.sort(key=lambda r:r['first'])
    if [(r['first'],r['end']) for r in completed]!=chunks or checked!=COUNT:
        raise RuntimeError('grid coverage has a gap or duplicate')
    indices=sorted(i for row in completed for i in row['hits'])
    hits=[(START+timedelta(minutes=i)).isoformat() for i in indices]
    for stamp in hits:
        snap=build_snapshot(datetime.fromisoformat(stamp),latitude=39.9526,longitude=-75.1652,ephemeris_root=args.ephemeris_root)
        if int(feature_row(snap,rules).sum())!=6: raise RuntimeError('cold survivor verification failed')
    result={'status':'COMPLETE','freeze_sha256':digest(args.output_dir/'freeze.json'),
      'exact_grid_count':COUNT,'unique_offsets_verified':True,'maximum_score':6,
      'maximum_count':len(hits),'maximum_instants':hits,'maximum_dates':sorted({s[:10] for s in hits}),
      'higher_than_target':0,'target_rank_best':1,'target_rank_worst':len(hits),
      'interpolation_used':False,'ephemeris_fallbacks':0,'model_refitted':False,
      'seconds':time.monotonic()-begin,'raw_and_deduplicated_identical':True,
      'continuous_time_exhaustiveness_proved':False,'runtime_survey_decoder_complete':False,
      'classification':'single-owner target-aware development signature, not human validation'}
    dump(args.output_dir/'result.json',result)
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    main()
