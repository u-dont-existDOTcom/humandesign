#!/usr/bin/env python3
"""Deterministic two-worker execution adapter for frozen permutation V1.

The null vectors are generated serially from the already frozen seed using the
same perm_y() function/order as the original runner, then only model evaluation
is parallelized. Scientific inputs and results are identical to serial execution.
"""
from __future__ import annotations
import json, random, statistics, multiprocessing as mp
from pathlib import Path
import numpy as np
import adb_broad_exact_pair_dissolution_permutation_v1 as p

G={}
def worker(y_list_item):
    idx,yp=y_list_item
    l2=p.eval_model(G['X'],yp,G['c2'],G['rows'],G['event_pairs'],G['names'])
    lw=p.eval_model(G['X'],yp,G['cw'],G['rows'],G['event_pairs'],G['names'])
    lh=p.eval_model(G['X'],yp,G['ch'],G['rows'],G['event_pairs'],G['names'])
    return idx,l2-lw,l2-lh

def main():
    policy=json.loads(p.POL.read_text());fm=json.loads(p.FM.read_text());fit=json.loads(p.FIT.read_text());reg=json.loads(p.REG.read_text())
    if p.sha256(p.FM)!=fit['feature_matrix_sha256_after_write']:raise RuntimeError('feature matrix hash mismatch')
    B=int(policy['permutations']);seed=int(policy['seed']);rows=fm['rows'];names=fm['feature_names'];X=np.array([r['features'] for r in rows],float)
    event_pairs={r['pair_key'] for r in rows if r['event']==1};groups=reg['feature_groups'];models=reg['models']
    def cols(m):
        ns=[]
        for g in models[m]['groups']:ns.extend(groups[g]['features'])
        return [names.index(n) for n in ns if n not in p.REF_DROP]
    c2,cw,ch=cols('M2'),cols('M3W'),cols('M3H')
    obsW=fit['comparisons']['M3W-M2']['pooled_log_loss_improvement'];obsH=fit['comparisons']['M3H-M2']['pooled_log_loss_improvement']
    rng=random.Random(seed)
    jobs=[(i,p.perm_y(rows,event_pairs,rng)) for i in range(B)]
    G.update({'X':X,'rows':rows,'names':names,'event_pairs':event_pairs,'c2':c2,'cw':cw,'ch':ch})
    ctx=mp.get_context('fork')
    outrows=[]
    with ctx.Pool(processes=2) as pool:
        for n,res in enumerate(pool.imap_unordered(worker,jobs,chunksize=1),1):
            outrows.append(res)
            if n%25==0:print('permutations',n,'/',B,flush=True)
    outrows.sort();nullW=[x[1] for x in outrows];nullH=[x[2] for x in outrows];nullMax=[max(a,b) for a,b in zip(nullW,nullH)]
    adjW=(1+sum(x>=obsW for x in nullMax))/(B+1);adjH=(1+sum(x>=obsH for x in nullMax))/(B+1);globalp=(1+sum(x>=max(obsW,obsH) for x in nullMax))/(B+1)
    preW=fit['co_primary_decision_pre_permutation']['M3W_vs_M2_passes_loss_loglik_fold_parts'];preH=fit['co_primary_decision_pre_permutation']['M3H_vs_M2_passes_loss_loglik_fold_parts']
    result={'status':'development_permutation_complete','execution':'deterministic_two_worker_adapter_same_serial_draws','policy_sha256':p.sha256(p.POL),'feature_matrix_sha256':p.sha256(p.FM),'fit_results_sha256':p.sha256(p.FIT),'B':B,'seed':seed,'observed':{'M3W-M2_log_loss_improvement':obsW,'M3H-M2_log_loss_improvement':obsH},'null_summary':{'M3W':{'mean':statistics.fmean(nullW),'sd':statistics.stdev(nullW),'q025':float(np.quantile(nullW,.025)),'q50':float(np.quantile(nullW,.5)),'q975':float(np.quantile(nullW,.975))},'M3H':{'mean':statistics.fmean(nullH),'sd':statistics.stdev(nullH),'q025':float(np.quantile(nullH,.025)),'q50':float(np.quantile(nullH,.5)),'q975':float(np.quantile(nullH,.975))},'maxT':{'mean':statistics.fmean(nullMax),'sd':statistics.stdev(nullMax),'q95':float(np.quantile(nullMax,.95)),'q975':float(np.quantile(nullMax,.975))}},'familywise_adjusted_p':{'M3W-M2':adjW,'M3H-M2':adjH,'global_any_pair_dynamic':globalp},'frozen_development_lead_decision':{'M3W':bool(preW and adjW<=.05),'M3H':bool(preH and adjH<=.05)},'raw_null':{'M3W':nullW,'M3H':nullH,'maxT':nullMax},'limitations':['Development-only ADB-derived data.','Familywise p uses frozen max-T rule across two co-primary dynamic families.','No relationship-quality outcome is tested.','Independent external replication remains mandatory.']}
    p.OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='raw_null'},indent=2),flush=True)
if __name__=='__main__':main()
