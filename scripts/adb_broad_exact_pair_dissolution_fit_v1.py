#!/usr/bin/env python3
"""Fit the frozen Broad Exact-Pair Dissolution Semi-Markov V1 models.

Scientific freeze:
  reference/research/adb_broad_exact_pair_dissolution_semimarkov_freeze_v1.md
Feature registry:
  reference/research/adb_broad_exact_pair_dissolution_feature_registry_v1.json
Design policy:
  reference/research/adb_broad_exact_pair_dissolution_design_matrix_policy_v1.json

This is development-only. It computes the frozen M0/M1/M2/M3W/M3H/M4 feature
matrix and 5-fold person-component-disjoint held-out predictions. The separately
frozen 500-permutation familywise test is intentionally run by another script
against the committed feature matrix/results.
"""
from __future__ import annotations

import hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path

import numpy as np
import swisseph as swe
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, brier_score_loss

import partner_hd_timing_pilot as hd

REPO=Path(__file__).resolve().parents[1]
EPHE=REPO/'data'/'ephemeris'
SPEC=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_semimarkov_freeze_v1.md'
REG=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_feature_registry_v1.json'
POL=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_design_matrix_policy_v1.json'
READY=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_episode_readiness_v1.json'
UNIV=REPO/'reference'/'research'/'adb_broad_exact_pair_universe_v4.json'
H3=REPO/'reference'/'research'/'adb_broad_exact_pair_history_v4_h3.json'
H4=REPO/'reference'/'research'/'adb_broad_exact_pair_history_v4_h4.json'
OUT=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_fit_results_v1.json'
FMAT=REPO/'reference'/'research'/'adb_broad_exact_pair_dissolution_feature_matrix_v1.json'

ASPECTS=(0.,60.,90.,120.,180.)
C_GRID=(0.001,0.01,0.1,1.0)
TROPICAL_YEAR=365.2422
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED
EPH_MASK=swe.FLG_JPLEPH|swe.FLG_SWIEPH|swe.FLG_MOSEPH
PLANETS={'Sun':swe.SUN,'Moon':swe.MOON,'Mercury':swe.MERCURY,'Venus':swe.VENUS,'Mars':swe.MARS,'Jupiter':swe.JUPITER,'Saturn':swe.SATURN,'Uranus':swe.URANUS,'Neptune':swe.NEPTUNE,'Pluto':swe.PLUTO}
NATAL_NAMES=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')
NATAL_TARGETS=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','ASC','MC')
PROG=('Sun','Moon','Mercury','Venus','Mars')
TRANS=('Jupiter','Saturn','Uranus','Neptune','Pluto')
SIGMA={'Jupiter':2.5,'Saturn':2.0,'Uranus':1.5,'Neptune':1.5,'Pluto':1.5,'Sun':1.0,'Moon':1.5,'Mercury':1.0,'Venus':1.0,'Mars':1.0}
REF_DROP={'m0_duration_eq_0','m0_entry_H1_begin','m0_entry_precision_day','m0_rodden_AA_AA'}


def sha256(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def wrap180(x): return (x+180.)%360.-180.
def midpoint(a,b): return (a+wrap180(b-a)/2.)%360.
def residual(m,t,a):
    if a==0:return abs(wrap180(m-t))
    if a==180:return abs(wrap180(m-t-180))
    return min(abs(wrap180(m-t-a)),abs(wrap180(m-t+a)))
def kmax(m,targets,sigma):
    return max(math.exp(-.5*(residual(m,t,a)/sigma)**2) for t in targets for a in ASPECTS)
def calc(jd,body):
    xx,ret=swe.calc_ut(jd,body,FLAGS)
    if (ret&EPH_MASK)!=swe.FLG_SWIEPH: raise RuntimeError(f'EPHEMERIS_FALLBACK body={body} jd={jd} ret={ret}')
    return float(xx[0]%360.)
def anchor_jds(y): return [swe.julday(y,m,d,12.0,swe.GREG_CAL) for m in range(1,13) for d in (1,15)]
def age_at_jd(birth,jd): return (jd-birth)/TROPICAL_YEAR

def natal_chart(p):
    n={x:calc(p['jd_ut'],PLANETS[x]) for x in NATAL_NAMES}
    cusps,ascmc=swe.houses_ex(p['jd_ut'],p['lat'],p['lon'],b'P',0)
    n['ASC']=float(ascmc[0]%360);n['MC']=float(ascmc[1]%360)
    return n

def progressed(p,jd):
    pj=p['jd_ut']+(jd-p['jd_ut'])/TROPICAL_YEAR
    return {x:calc(pj,PLANETS[x]) for x in PROG}

def transit(jd): return {x:calc(jd,PLANETS[x]) for x in TRANS}

# HD helpers use the repository's frozen gate wheel/channel graph.
def natal_gates_jd(bj):
    dj=hd.design_jd(bj); gs=set()
    for t in (bj,dj):
        for name,b in hd.BODIES.items():
            g=hd.gate(hd.calc(t,b)[0]); gs.add(g)
            if name in ('sun','north_node'): gs.add(hd.OPP[g])
    return gs

def transit_gates_full(jd):
    gs=set()
    for name,b in hd.BODIES.items():
        g=hd.gate(hd.calc(jd,b)[0]);gs.add(g)
        if name in ('sun','north_node'):gs.add(hd.OPP[g])
    return gs

def fp(gs): return hd.fingerprint(gs)
def channel_set(gs): return {tuple(sorted(c)) for c in hd.CHANNELS if c[0] in gs and c[1] in gs}
def center_set(gs):
    out=set()
    for a,b in channel_set(gs):out.add(hd.GC[a]);out.add(hd.GC[b])
    return out

def static_hd_pair(ga,gb):
    ua=channel_set(ga);ub=channel_set(gb);u=ga|gb;f=fp(u)
    em=comp=dom=compromise=0
    for c in hd.CHANNELS:
        a,b=c; af=c in ua;bf=c in ub
        if af and bf: comp+=1
        elif af:
            present=int(a in gb)+int(b in gb)
            if present==0:dom+=1
            elif present==1:compromise+=1
        elif bf:
            present=int(a in ga)+int(b in ga)
            if present==0:dom+=1
            elif present==1:compromise+=1
        else:
            if ((a in ga and b in gb) or (b in ga and a in gb)) and not ((a in ga and b in ga) or (a in gb and b in gb)):em+=1
    return {
      'm2h_static_defined_centers':f['defined_center_count'],
      'm2h_static_definition_components':f['definition_components'],
      'm2h_static_channel_count':len(channel_set(u)),
      'm2h_static_electromagnetic_count':em,
      'm2h_static_companionship_count':comp,
      'm2h_static_dominance_count':dom,
      'm2h_static_compromise_count':compromise,
    }

def static_west(na,nb):
    lum=[(na[x],nb[y]) for x in ('Sun','Moon') for y in ('Sun','Moon')]
    att=[(na[x],nb[y]) for x in ('Venus','Mars') for y in ('Venus','Mars')]
    comm=[(na['Mercury'],nb[y]) for y in ('Sun','Moon','Mercury')]+[(nb['Mercury'],na[y]) for y in ('Sun','Moon','Mercury')]
    ang=[(na[x],nb[y]) for x in ('Sun','Moon','Mercury','Venus','Mars') for y in ('ASC','MC')]+[(nb[x],na[y]) for x in ('Sun','Moon','Mercury','Venus','Mars') for y in ('ASC','MC')]
    km=lambda pairs:max(max(math.exp(-.5*(residual(a,b,z)/2.0)**2) for z in ASPECTS) for a,b in pairs)
    return {'m2w_static_luminary_activation':km(lum),'m2w_static_attraction_activation':km(att),'m2w_static_communication_activation':km(comm),'m2w_static_angle_activation':km(ang)}

def hd_connection_coverage(pair_h3,pair_h4):
    i3a=pair_h3.get('wikipedia_identity_a') or {};i3b=pair_h3.get('wikipedia_identity_b') or {}
    h3ok=int(bool(i3a.get('canonical_wikipedia_title') and i3b.get('canonical_wikipedia_title')))
    # H4 exact linked identities are represented by QIDs/statement directions in pair artifact.
    qids=set()
    for key in ('H4_new_nonfatal_endpoints','H4_corroborating_endpoints','H4_nonqualifying_statements'):
        for s in pair_h4.get(key,[]) or []:
            if s.get('source_qid'):qids.add(s['source_qid'])
            if s.get('other_qid'):qids.add(s['other_qid'])
    h4ok=int(len(qids)>=2)
    return h3ok,h4ok

def person_year_individual(p,nat,ng,y,cache_trans):
    anchors=anchor_jds(y)
    own={x:0. for x in TRANS+PROG}
    hdvals={'new_channels':[],'new_centers':[],'components':[],'defined_centers':[]}
    nch=channel_set(ng);nce=center_set(ng)
    for j in anchors:
        tr=cache_trans.setdefault(j,transit(j))
        pr=progressed(p,j)
        for x in TRANS:own[x]=max(own[x],kmax(tr[x],[nat[t] for t in NATAL_TARGETS],SIGMA[x]))
        for x in PROG:own[x]=max(own[x],kmax(pr[x],[nat[t] for t in NATAL_TARGETS],SIGMA[x]))
        tg=transit_gates_full(j);ov=ng|tg;f=fp(ov)
        hdvals['new_channels'].append(len(channel_set(ov)-nch));hdvals['new_centers'].append(len(center_set(ov)-nce));hdvals['components'].append(f['definition_components']);hdvals['defined_centers'].append(f['defined_center_count'])
    return own,{k:statistics.fmean(v) for k,v in hdvals.items()}
def pair_year_dynamic(pa,pb,na,nb,ga,gb,y,cache_trans):
    anchors=anchor_jds(y)
    cross={x:[0.,0.] for x in PROG};mut={x:0. for x in PROG};nc={x:0. for x in TRANS};pc={x:0. for x in TRANS}
    natalcomp={x:midpoint(na[x],nb[x]) for x in NATAL_NAMES}
    sg=ga|gb;sf=fp(sg);sch=channel_set(sg);sce=center_set(sg)
    hv={'centers':[],'channels':[],'components':[],'single':[],'eight':[],'nine':[],'bridge':[]}
    for j in anchors:
        tr=cache_trans.setdefault(j,transit(j));pra=progressed(pa,j);prb=progressed(pb,j)
        for x in PROG:
            cross[x][0]=max(cross[x][0],kmax(pra[x],[nb[t] for t in NATAL_TARGETS],SIGMA[x]))
            cross[x][1]=max(cross[x][1],kmax(prb[x],[na[t] for t in NATAL_TARGETS],SIGMA[x]))
            mut[x]=max(mut[x],kmax(pra[x],[prb[t] for t in PROG],SIGMA[x]),kmax(prb[x],[pra[t] for t in PROG],SIGMA[x]))
        progcomp={x:midpoint(pra[x],prb[x]) for x in PROG}
        for x in TRANS:
            nc[x]=max(nc[x],kmax(tr[x],[natalcomp[t] for t in NATAL_NAMES],SIGMA[x]))
            pc[x]=max(pc[x],kmax(tr[x],[progcomp[t] for t in PROG],SIGMA[x]))
        tg=transit_gates_full(j);ov=sg|tg;f=fp(ov)
        hv['centers'].append(len(center_set(ov)-sce));hv['channels'].append(len(channel_set(ov)-sch));hv['components'].append(f['definition_components']);hv['single'].append(int(f['definition_components']==1));hv['eight'].append(int(f['defined_center_count']==8));hv['nine'].append(int(f['defined_center_count']==9));hv['bridge'].append(max(0,sf['definition_components']-f['definition_components']))
    out={}
    for x in PROG:
        out[f'm3w_prog_{x}_to_partner_natal_mean']=statistics.fmean(cross[x]);out[f'm3w_prog_{x}_to_partner_natal_max']=max(cross[x]);out[f'm3w_prog_{x}_to_partner_progressed_mutual_max']=mut[x]
    for x in TRANS:
        out[f'm3w_transit_{x}_to_natal_midpoint_composite']=nc[x];out[f'm3w_transit_{x}_to_progressed_midpoint_composite']=pc[x]
    out.update({'m3h_added_defined_centers_mean':statistics.fmean(hv['centers']),'m3h_added_channels_mean':statistics.fmean(hv['channels']),'m3h_definition_components_mean':statistics.fmean(hv['components']),'m3h_fraction_single_definition':statistics.fmean(hv['single']),'m3h_fraction_exactly_8_defined_centers':statistics.fmean(hv['eight']),'m3h_fraction_all_9_centers_defined':statistics.fmean(hv['nine']),'m3h_split_bridge_reduction_mean':statistics.fmean(hv['bridge'])})
    return out

def m0_features(row,ep,pa,pb,h3ok,h4ok):
    d=row['duration_since_entry_year'];y=row['calendar_year'];j=swe.julday(y,7,1,12.0,swe.GREG_CAL);ages=sorted([age_at_jd(pa['jd_ut'],j),age_at_jd(pb['jd_ut'],j)])
    rel=set(ep.get('relation_codes') or []);src=row['entry_source'];prec=row['entry_precision'];rr=sorted([pa['rr'],pb['rr']])
    out={
      'm0_duration_eq_0':int(d==0),'m0_duration_eq_1':int(d==1),'m0_duration_eq_2':int(d==2),'m0_duration_3_4':int(3<=d<=4),'m0_duration_5_9':int(5<=d<=9),'m0_duration_10_19':int(10<=d<=19),'m0_duration_20_29':int(20<=d<=29),'m0_duration_30_plus':int(d>=30),
      'm0_age_younger':ages[0],'m0_age_older':ages[1],'m0_age_difference':ages[1]-ages[0],'m0_calendar_year_centered_1950':y-1950,'m0_calendar_year_centered_1950_squared':(y-1950)**2,
      'm0_relation_spouse':int(843 in rel),'m0_relation_lover':int(858 in rel),'m0_relation_spousal_equivalent':int(859 in rel),
      'm0_entry_H1_begin':int(src=='H1_begin'),'m0_entry_H1_range_start':int(src=='H1_range_start'),'m0_entry_H1_marriage':int(src=='H1_marriage'),'m0_entry_H4_P580':int(src=='H4_P580'),
      'm0_entry_precision_day':int(prec=='day'),'m0_entry_precision_month':int(prec=='month'),'m0_entry_precision_year':int(prec=='year'),
      'm0_rodden_AA_AA':int(rr==['AA','AA']),'m0_rodden_AA_A':int(rr==['A','AA']),'m0_rodden_A_A':int(rr==['A','A']),
      'm0_coverage_H1_both_exact_ADB':1,'m0_coverage_H3_both_linked_wikipedia':h3ok,'m0_coverage_H4_both_linked_wikidata':h4ok,
    }
    return out

def sym_ind(a,b):
    out={}
    for x in TRANS:
        vals=[a[0][x],b[0][x]];out[f'm1w_transit_{x}_own_activation_pair_mean']=statistics.fmean(vals);out[f'm1w_transit_{x}_own_activation_pair_max']=max(vals)
    for x in PROG:
        vals=[a[0][x],b[0][x]];out[f'm1w_progressed_{x}_own_activation_pair_mean']=statistics.fmean(vals);out[f'm1w_progressed_{x}_own_activation_pair_max']=max(vals)
    names=[('new_channels','new_channels'),('new_centers','new_centers'),('overlay_components','components'),('overlay_defined_centers','defined_centers')]
    for label,k in names:
        vals=[a[1][k],b[1][k]];out[f'm1h_{label}_pair_mean']=statistics.fmean(vals);out[f'm1h_{label}_pair_max']=max(vals)
    return out

def component_folds(episodes,nfold=5):
    parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb:parent[max(ra,rb)]=min(ra,rb)
    for e in episodes:union(e['person_a_id'],e['person_b_id'])
    comps=defaultdict(list)
    for e in episodes:comps[find(e['person_a_id'])].append(e)
    items=[]
    for root,es in comps.items():
        ev=sum(x['outcome']=='event' for x in es);rows=sum(x['duration_years']+1 for x in es);keys=sorted(x['pair_key'] for x in es);hh=hashlib.sha256('|'.join(keys).encode()).hexdigest();items.append((root,ev,rows,hh,keys))
    items.sort(key=lambda z:(-z[1],-z[2],z[3]))
    state=[{'ev':0,'rows':0,'roots':[]} for _ in range(nfold)]
    for root,ev,rows,hh,keys in items:
        i=min(range(nfold),key=lambda q:(state[q]['ev'],state[q]['rows'],q));state[i]['ev']+=ev;state[i]['rows']+=rows;state[i]['roots'].append(root)
    p2f={}
    for i,s in enumerate(state):
        roots=set(s['roots'])
        for root,ev,rows,hh,keys in items:
            if root in roots:
                for pk in keys:p2f[pk]=i
    return p2f,state

def fit_one(X,y,train,test,cols,C):
    Xt=X[np.ix_(train,cols)].copy();Xv=X[np.ix_(test,cols)].copy()
    # continuous = all non-M0-indicator columns plus named continuous M0 fields
    names=[ALL_FEATURES[i] for i in cols]
    cont=[j for j,n in enumerate(names) if (not n.startswith('m0_')) or n in {'m0_age_younger','m0_age_older','m0_age_difference','m0_calendar_year_centered_1950','m0_calendar_year_centered_1950_squared'}]
    if cont:
        mu=Xt[:,cont].mean(0);sd=Xt[:,cont].std(0);sd[sd==0]=1;Xt[:,cont]=(Xt[:,cont]-mu)/sd;Xv[:,cont]=(Xv[:,cont]-mu)/sd
    model=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=5000,fit_intercept=True)
    model.fit(Xt,y[train]);return model.predict_proba(Xv)[:,1]
def choose_c(X,y,outer_train,cols,pair_keys,pair_to_outer):
    # Inner groups are connected components; reuse deterministic component assignment on training episodes only.
    train_pairs=set(pair_keys[i] for i in outer_train);eps=[e for e in EPISODES if e['pair_key'] in train_pairs]
    p2f,state=component_folds(eps,min(5,max(2,len(set(e['pair_key'] for e in eps)))))
    best=None
    for C in C_GRID:
        losses=[]
        for f in sorted(set(p2f.values())):
            va=np.array([i for i in outer_train if p2f.get(pair_keys[i])==f],dtype=int);tr=np.array([i for i in outer_train if p2f.get(pair_keys[i])!=f],dtype=int)
            if len(va)==0 or len(tr)==0 or len(set(y[tr]))<2:continue
            pr=fit_one(X,y,tr,va,cols,C);losses.append(log_loss(y[va],pr,labels=[0,1]))
        score=statistics.fmean(losses) if losses else float('inf')
        if best is None or score<best[0]-1e-12 or (abs(score-best[0])<=1e-12 and C<best[1]):best=(score,C)
    return best[1] if best else C_GRID[0]
def calibration(y,p):
    eps=1e-9;z=np.log(np.clip(p,eps,1-eps)/(1-np.clip(p,eps,1-eps))).reshape(-1,1)
    if len(set(y))<2:return {'intercept':None,'slope':None}
    m=LogisticRegression(C=1e9,solver='lbfgs',max_iter=2000).fit(z,y)
    return {'intercept':float(m.intercept_[0]),'slope':float(m.coef_[0,0])}
def event_rank(rows,preds):
    by=defaultdict(list)
    for i,r in enumerate(rows):by[r['pair_key']].append((i,r,preds[i]))
    vals=[]
    for pk,z in by.items():
        ev=[x for x in z if x[1]['event']==1]
        if not ev:continue
        v=ev[0][2];arr=[x[2] for x in z];pct=100*(sum(x<v-1e-12 for x in arr)+.5*sum(abs(x-v)<=1e-12 for x in arr))/len(arr);vals.append(pct)
    return {'n_event_pairs':len(vals),'mean_percentile':statistics.fmean(vals) if vals else None,'median_percentile':statistics.median(vals) if vals else None}
def cumulative_cal(rows,preds,horizon):
    by=defaultdict(list)
    for i,r in enumerate(rows):by[r['pair_key']].append((r,preds[i]))
    ps=[];ys=[]
    for pk,z in by.items():
        z=sorted(z,key=lambda q:q[0]['calendar_year'])
        if len(z)<horizon:continue
        first=z[:horizon];ps.append(1-math.prod(1-p for _,p in first));ys.append(int(any(r['event']==1 for r,_ in first)))
    return {'n':len(ps),'mean_predicted_risk':statistics.fmean(ps) if ps else None,'observed_fraction':statistics.fmean(ys) if ys else None,'brier':statistics.fmean((a-b)**2 for a,b in zip(ps,ys)) if ps else None}

def main():
    global ALL_FEATURES,EPISODES
    for p in (EPHE/'sepl_18.se1',EPHE/'semo_18.se1'):
        if not p.is_file():raise SystemExit('missing '+str(p))
    swe.set_ephe_path(str(EPHE));hd.swe.set_ephe_path(str(EPHE))
    reg=json.loads(REG.read_text());pol=json.loads(POL.read_text());rd=json.loads(READY.read_text());u=json.loads(UNIV.read_text());h3=json.loads(H3.read_text());h4=json.loads(H4.read_text())
    if not rd['readiness']['READY_FOR_FEATURE_REGISTRY_FREEZE']:raise RuntimeError('readiness gate not passed')
    # hard frozen-input/hash checks
    if reg['scientific_model_spec_sha256']!=sha256(SPEC):raise RuntimeError('model spec hash mismatch')
    if reg['ephemeris']['planetary_sha256']!=sha256(EPHE/'sepl_18.se1') or reg['ephemeris']['moon_sha256']!=sha256(EPHE/'semo_18.se1'):raise RuntimeError('ephemeris hash mismatch')
    pairs={x['pair_key']:x for x in u['pairs']};h3b={x['pair_key']:x for x in h3['pairs']};h4b={x['pair_key']:x for x in h4['pairs']};EPISODES=rd['episodes'];rows=rd['pair_year_rows'];epb={x['pair_key']:x for x in EPISODES}
    # person records from pair objects
    people={}
    for q in u['pairs']:
        for side in ('person_a','person_b'):
            p=q[side];people[int(p['adb_id'])]=p
    nat={};ng={};pind={};pstatic={};cache_trans={};feature_rows=[]
    for pid,p in people.items():
        if 'jd_ut' in p and p.get('model_eligible_birth_and_swieph',True):
            try:nat[pid]=natal_chart(p);ng[pid]=natal_gates_jd(p['jd_ut'])
            except Exception:pass
    for idx,row in enumerate(rows,1):
        ep=epb[row['pair_key']];pa=people[row['person_a_id']];pb=people[row['person_b_id']];a=row['person_a_id'];b=row['person_b_id'];y=row['calendar_year']
        if a not in nat or b not in nat:raise RuntimeError(f'missing natal {a} {b}')
        sk=row['pair_key']
        if sk not in pstatic:
            h3ok,h4ok=hd_connection_coverage(h3b[sk],h4b[sk]);pstatic[sk]=(static_west(nat[a],nat[b]),static_hd_pair(ng[a],ng[b]),h3ok,h4ok)
        sw,sh,h3ok,h4ok=pstatic[sk]
        for pid,p in ((a,pa),(b,pb)):
            key=(pid,y)
            if key not in pind:pind[key]=person_year_individual(p,nat[pid],ng[pid],y,cache_trans)
        feats=m0_features(row,ep,pa,pb,h3ok,h4ok);feats.update(sym_ind(pind[(a,y)],pind[(b,y)]));feats.update(sw);feats.update(sh);feats.update(pair_year_dynamic(pa,pb,nat[a],nat[b],ng[a],ng[b],y,cache_trans))
        feature_rows.append(feats)
        if idx%250==0:print('features',idx,'/',len(rows),flush=True)
    groups=reg['feature_groups'];ALL_FEATURES=[]
    for g in ('M0','M1_WESTERN_INDIVIDUAL','M1_HD_INDIVIDUAL','M2_WESTERN_STATIC','M2_HD_STATIC','M3W_DYNAMIC_PAIR','M3H_DYNAMIC_PAIR'):ALL_FEATURES.extend(groups[g]['features'])
    if len(ALL_FEATURES)!=100 or len(set(ALL_FEATURES))!=100:raise RuntimeError('registry flatten mismatch')
    for i,f in enumerate(feature_rows):
        miss=[x for x in ALL_FEATURES if x not in f]
        if miss:raise RuntimeError(f'missing features row {i}: {miss[:5]}')
    X=np.array([[float(f[n]) for n in ALL_FEATURES] for f in feature_rows]);y=np.array([int(r['event']) for r in rows]);pair_keys=[r['pair_key'] for r in rows]
    if not np.isfinite(X).all():raise RuntimeError('nonfinite X')
    # Model feature lists exactly from frozen registry, with reference columns dropped only at fit.
    model_groups=reg['models'];model_cols={}
    for m,s in model_groups.items():
        names=[]
        for g in s['groups']:names.extend(groups[g]['features'])
        names=[n for n in names if n not in REF_DROP];model_cols[m]=[ALL_FEATURES.index(n) for n in names]
    p2f,foldstate=component_folds(EPISODES,5)
    predictions={m:np.full(len(rows),np.nan) for m in ('M0','M1','M2','M3W','M3H','M4')};chosen={m:[] for m in predictions};fold_losses={m:[] for m in predictions}
    for f in range(5):
        test=np.array([i for i,pk in enumerate(pair_keys) if p2f[pk]==f],dtype=int);train=np.array([i for i,pk in enumerate(pair_keys) if p2f[pk]!=f],dtype=int)
        if len(set(y[train]))<2:raise RuntimeError('outer train one class')
        for m in predictions:
            C=choose_c(X,y,train,model_cols[m],pair_keys,p2f);pr=fit_one(X,y,train,test,model_cols[m],C);predictions[m][test]=pr;chosen[m].append(C);fold_losses[m].append(log_loss(y[test],pr,labels=[0,1]))
        print('fold',f,'done',flush=True)
    results={}
    for m,p in predictions.items():
        if np.isnan(p).any():raise RuntimeError('missing predictions '+m)
        ll=-float(np.sum(-(y*np.log(np.clip(p,1e-15,1))+(1-y)*np.log(np.clip(1-p,1e-15,1)))))
        # ll above accidentally positive NLL if negated; compute true log likelihood explicitly.
        loglik=float(np.sum(y*np.log(np.clip(p,1e-15,1))+(1-y)*np.log(np.clip(1-p,1e-15,1))))
        results[m]={'pair_year_log_loss':float(log_loss(y,p,labels=[0,1])),'heldout_total_log_likelihood':loglik,'brier_score':float(brier_score_loss(y,p)),'calibration':calibration(y,p),'event_year_rank':event_rank(rows,p),'cumulative_risk':{'1y':cumulative_cal(rows,p,1),'2y':cumulative_cal(rows,p,2),'5y':cumulative_cal(rows,p,5)},'chosen_C_by_fold':chosen[m],'fold_log_loss':fold_losses[m]}
    comparisons={}
    for a,b in [('M1','M0'),('M2','M1'),('M3W','M2'),('M3H','M2'),('M4','M2'),('M4','M3W'),('M4','M3H')]:
        comparisons[f'{a}-{b}']={'pooled_log_loss_improvement':results[b]['pair_year_log_loss']-results[a]['pair_year_log_loss'],'heldout_loglik_improvement':results[a]['heldout_total_log_likelihood']-results[b]['heldout_total_log_likelihood'],'folds_with_positive_log_loss_improvement':sum(x<z for x,z in zip(results[a]['fold_log_loss'],results[b]['fold_log_loss'])),'fold_log_loss_delta_new_minus_old':[x-z for x,z in zip(results[a]['fold_log_loss'],results[b]['fold_log_loss'])]}
    compact_rows=[]
    for i,r in enumerate(rows):compact_rows.append({'pair_key':r['pair_key'],'person_a_id':r['person_a_id'],'person_b_id':r['person_b_id'],'calendar_year':r['calendar_year'],'duration_since_entry_year':r['duration_since_entry_year'],'event':r['event'],'outer_fold':p2f[r['pair_key']],'features':[float(x) for x in X[i]]})
    fmat={'status':'frozen_feature_matrix_before_permutation','spec_sha256':sha256(SPEC),'registry_sha256':sha256(REG),'policy_sha256':sha256(POL),'readiness_sha256':sha256(READY),'feature_names':ALL_FEATURES,'reference_drop_fit_only':sorted(REF_DROP),'rows':compact_rows}
    FMAT.write_text(json.dumps(fmat,separators=(',',':'))+'\n')
    out={'status':'development_fit_complete_permutation_pending','model_spec':str(SPEC.relative_to(REPO)),'input_hashes':{'spec':sha256(SPEC),'registry':sha256(REG),'policy':sha256(POL),'readiness':sha256(READY),'universe':sha256(UNIV),'H3':sha256(H3),'H4':sha256(H4)},'data':{'pair_year_rows':len(rows),'episodes':len(EPISODES),'event_pairs':sum(e['outcome']=='event' for e in EPISODES),'censored_pairs':sum(e['outcome']=='censor' for e in EPISODES),'positive_pair_year_rows':int(y.sum()),'outer_fold_state':foldstate},'models':results,'comparisons':comparisons,'co_primary_decision_pre_permutation':{'M3W_vs_M2_passes_loss_loglik_fold_parts':bool(comparisons['M3W-M2']['pooled_log_loss_improvement']>0 and comparisons['M3W-M2']['heldout_loglik_improvement']>0 and comparisons['M3W-M2']['folds_with_positive_log_loss_improvement']>=4),'M3H_vs_M2_passes_loss_loglik_fold_parts':bool(comparisons['M3H-M2']['pooled_log_loss_improvement']>0 and comparisons['M3H-M2']['heldout_loglik_improvement']>0 and comparisons['M3H-M2']['folds_with_positive_log_loss_improvement']>=4),'note':'500-permutation familywise p-value still required by frozen rule'},'feature_matrix_sha256_after_write':sha256(FMAT),'limitations':['Development data only; not independent validation.','Track T transition timing only, not relationship quality.','No Joel/Bee case used in feature selection or fitting.','Permutation/falsification suite is separate and still required before any development lead can be declared.']}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'data':out['data'],'comparisons':comparisons,'co_primary':out['co_primary_decision_pre_permutation'],'feature_matrix_sha256':out['feature_matrix_sha256_after_write']},indent=2),flush=True)

if __name__=='__main__':main()
