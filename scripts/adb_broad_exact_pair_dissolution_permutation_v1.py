#!/usr/bin/env python3
"""500-permutation max-T test for frozen dissolution semi-Markov V1.

Uses the already committed frozen feature matrix. No astrology/HD feature is
recomputed or changed here.
"""
from __future__ import annotations
import json, math, random, statistics, hashlib
from collections import defaultdict
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

REPO=Path(__file__).resolve().parents[1]
POL=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_permutation_policy_v1.json'
REG=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_feature_registry_v1.json'
DM=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_design_matrix_policy_v1.json'
FM=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_feature_matrix_v1.json'
FIT=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_fit_results_v1.json'
OUT=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_permutation_results_v1.json'
C_GRID=(0.001,0.01,0.1,1.0)
REF_DROP={'m0_duration_eq_0','m0_entry_H1_begin','m0_entry_precision_day','m0_rodden_AA_AA'}

def sha256(p):
    h=hashlib.sha256();
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def components(rows,pairs=None):
    parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb:parent[max(ra,rb)]=min(ra,rb)
    seen=set()
    for r in rows:
        pk=r['pair_key']
        if pairs is not None and pk not in pairs:continue
        if pk in seen:continue
        seen.add(pk);union(int(r['person_a_id']),int(r['person_b_id']))
    p2root={}
    for r in rows:
        if pairs is not None and r['pair_key'] not in pairs:continue
        p2root[r['pair_key']]=find(int(r['person_a_id']))
    return p2root

def inner_folds(rows,outer_train,event_pair_set,nfold=5):
    train_pairs={rows[i]['pair_key'] for i in outer_train};p2root=components(rows,train_pairs);by=defaultdict(set)
    for pk,root in p2root.items():by[root].add(pk)
    stats=[]
    for root,pks in by.items():
        ev=sum(pk in event_pair_set for pk in pks);nr=sum(1 for i in outer_train if rows[i]['pair_key'] in pks);hh=hashlib.sha256('|'.join(sorted(pks)).encode()).hexdigest();stats.append((root,ev,nr,hh,pks))
    nf=min(nfold,max(2,len(stats)));state=[{'ev':0,'rows':0,'roots':[]} for _ in range(nf)]
    for root,ev,nr,hh,pks in sorted(stats,key=lambda z:(-z[1],-z[2],z[3])):
        f=min(range(nf),key=lambda q:(state[q]['ev'],state[q]['rows'],q));state[f]['ev']+=ev;state[f]['rows']+=nr;state[f]['roots'].append(root)
    p2f={}
    for f,s in enumerate(state):
        for root in s['roots']:
            for pk in by[root]:p2f[pk]=f
    return p2f

def fit_predict(X,y,tr,va,cols,C,names):
    Xt=X[np.ix_(tr,cols)].copy();Xv=X[np.ix_(va,cols)].copy();ns=[names[i] for i in cols]
    cont=[j for j,n in enumerate(ns) if (not n.startswith('m0_')) or n in {'m0_age_younger','m0_age_older','m0_age_difference','m0_calendar_year_centered_1950','m0_calendar_year_centered_1950_squared'}]
    if cont:
        mu=Xt[:,cont].mean(0);sd=Xt[:,cont].std(0);sd[sd==0]=1.;Xt[:,cont]=(Xt[:,cont]-mu)/sd;Xv[:,cont]=(Xv[:,cont]-mu)/sd
    m=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=3000,fit_intercept=True).fit(Xt,y[tr]);return m.predict_proba(Xv)[:,1]
def choose_c(X,y,train,cols,rows,event_pairs,names):
    p2f=inner_folds(rows,train,event_pairs,5);best=(float('inf'),None)
    for C in C_GRID:
        ls=[]
        for f in sorted(set(p2f.values())):
            va=np.array([i for i in train if p2f.get(rows[i]['pair_key'])==f],int);tr=np.array([i for i in train if p2f.get(rows[i]['pair_key'])!=f],int)
            if not len(va) or not len(tr) or len(set(y[tr]))<2:continue
            p=fit_predict(X,y,tr,va,cols,C,names);ls.append(log_loss(y[va],p,labels=[0,1]))
        s=statistics.fmean(ls) if ls else float('inf')
        if s<best[0]-1e-12 or (abs(s-best[0])<=1e-12 and (best[1] is None or C<best[1])):best=(s,C)
    return best[1] if best[1] is not None else C_GRID[0]
def eval_model(X,y,cols,rows,event_pairs,names):
    pred=np.full(len(y),np.nan)
    for f in range(5):
        va=np.array([i for i,r in enumerate(rows) if r['outer_fold']==f],int);tr=np.array([i for i,r in enumerate(rows) if r['outer_fold']!=f],int)
        C=choose_c(X,y,tr,cols,rows,event_pairs,names);pred[va]=fit_predict(X,y,tr,va,cols,C,names)
    return float(log_loss(y,pred,labels=[0,1]))
def perm_y(rows,event_pairs,rng):
    y=np.zeros(len(rows),dtype=int);by=defaultdict(list)
    for i,r in enumerate(rows):by[r['pair_key']].append(i)
    for pk in event_pairs:y[rng.choice(by[pk])]=1
    return y

def main():
    policy=json.loads(POL.read_text());fm=json.loads(FM.read_text());fit=json.loads(FIT.read_text());reg=json.loads(REG.read_text())
    if sha256(FM)!=fit['feature_matrix_sha256_after_write']:raise RuntimeError('feature matrix hash mismatch')
    B=int(policy['permutations']);seed=int(policy['seed']);rows=fm['rows'];names=fm['feature_names'];X=np.array([r['features'] for r in rows],float);y0=np.array([r['event'] for r in rows],int)
    event_pairs={r['pair_key'] for r in rows if r['event']==1}
    groups=reg['feature_groups'];models=reg['models']
    def cols(m):
        ns=[]
        for g in models[m]['groups']:ns.extend(groups[g]['features'])
        return [names.index(n) for n in ns if n not in REF_DROP]
    c2,cw,ch=cols('M2'),cols('M3W'),cols('M3H')
    obsW=fit['comparisons']['M3W-M2']['pooled_log_loss_improvement'];obsH=fit['comparisons']['M3H-M2']['pooled_log_loss_improvement']
    rng=random.Random(seed);nullW=[];nullH=[];nullMax=[]
    for b in range(B):
        yp=perm_y(rows,event_pairs,rng);l2=eval_model(X,yp,c2,rows,event_pairs,names);lw=eval_model(X,yp,cw,rows,event_pairs,names);lh=eval_model(X,yp,ch,rows,event_pairs,names);dw=l2-lw;dh=l2-lh;nullW.append(dw);nullH.append(dh);nullMax.append(max(dw,dh))
        if (b+1)%25==0:print('permutations',b+1,'/',B,'meanMax',statistics.fmean(nullMax),flush=True)
    adjW=(1+sum(x>=obsW for x in nullMax))/(B+1);adjH=(1+sum(x>=obsH for x in nullMax))/(B+1);globalp=(1+sum(x>=max(obsW,obsH) for x in nullMax))/(B+1)
    preW=fit['co_primary_decision_pre_permutation']['M3W_vs_M2_passes_loss_loglik_fold_parts'];preH=fit['co_primary_decision_pre_permutation']['M3H_vs_M2_passes_loss_loglik_fold_parts']
    out={'status':'development_permutation_complete','policy_sha256':sha256(POL),'feature_matrix_sha256':sha256(FM),'fit_results_sha256':sha256(FIT),'B':B,'seed':seed,'observed':{'M3W-M2_log_loss_improvement':obsW,'M3H-M2_log_loss_improvement':obsH},'null_summary':{'M3W':{'mean':statistics.fmean(nullW),'sd':statistics.stdev(nullW),'q025':float(np.quantile(nullW,.025)),'q50':float(np.quantile(nullW,.5)),'q975':float(np.quantile(nullW,.975))},'M3H':{'mean':statistics.fmean(nullH),'sd':statistics.stdev(nullH),'q025':float(np.quantile(nullH,.025)),'q50':float(np.quantile(nullH,.5)),'q975':float(np.quantile(nullH,.975))},'maxT':{'mean':statistics.fmean(nullMax),'sd':statistics.stdev(nullMax),'q95':float(np.quantile(nullMax,.95)),'q975':float(np.quantile(nullMax,.975))}},'familywise_adjusted_p':{'M3W-M2':adjW,'M3H-M2':adjH,'global_any_pair_dynamic':globalp},'frozen_development_lead_decision':{'M3W':bool(preW and adjW<=.05),'M3H':bool(preH and adjH<=.05)},'raw_null':{'M3W':nullW,'M3H':nullH,'maxT':nullMax},'limitations':['Development-only ADB-derived data.','Familywise p uses frozen max-T rule across two co-primary dynamic families.','No relationship-quality outcome is tested.','Independent external replication remains mandatory.']}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='raw_null'},indent=2),flush=True)
if __name__=='__main__':main()
