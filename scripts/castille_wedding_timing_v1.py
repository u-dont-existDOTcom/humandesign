#!/usr/bin/env python3
"""Large-N independent wedding-timing test on Didier Castille a00 data.

Frozen spec: reference/research/castille_wedding_timing_freeze_v1.md
Only aggregate results are committed. No astrology enters split/control creation.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import swisseph as swe
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

import castille_static_synastry_v1 as static

REPO=Path(__file__).resolve().parents[1]
EPHE=REPO/"data"/"ephemeris"
FREEZE=REPO/"reference"/"research"/"castille_wedding_timing_freeze_v1.md"
OUT=REPO/"reference"/"research"/"castille_wedding_timing_results_v1.json"
SEED=202608261433
ALPHAS=(1e-5,1e-4,1e-3,1e-2)
CAPS={"discovery":60_000,"validation":30_000,"final":60_000}
RISK_TASKS=20_000
SHIFTS=tuple(range(-10,0))+tuple(range(1,11))
ASPECTS=np.asarray([0.,60.,90.,120.,180.],dtype=np.float64)
SIGMA=3.0
TROPICAL_YEAR=365.2422
FLAGS=swe.FLG_SWIEPH
EPH_MASK=swe.FLG_JPLEPH|swe.FLG_SWIEPH|swe.FLG_MOSEPH
NATAL_NAMES=("Sun","Mercury","Venus","Mars","Jupiter","Saturn")
NATAL_IDS=(swe.SUN,swe.MERCURY,swe.VENUS,swe.MARS,swe.JUPITER,swe.SATURN)
PROG_NAMES=("Sun","Mercury","Venus","Mars")
PROG_IDS=(swe.SUN,swe.MERCURY,swe.VENUS,swe.MARS)
TRANSIT_NAMES=("Jupiter","Saturn","Uranus","Neptune","Pluto")
TRANSIT_IDS=(swe.JUPITER,swe.SATURN,swe.URANUS,swe.NEPTUNE,swe.PLUTO)
P0=6
P1=P0 + 2*(5*6*5 + 4*6*5)
P3=P1 + 2*(4*6*5) + (4*4*5) + (5*6*5) + (5*4*5)
MODEL_DIMS={"M0T":P0,"M1T":P1,"M3T":P3}


@dataclass(frozen=True)
class TRecord:
    mother:tuple[int,int,int]
    father:tuple[int,int,int]
    wedding:tuple[int,int,int]
    canonical:str
    digest:str
    split:str


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()


def timing_digest(canon:str)->str:
    return hashlib.sha256(("wedding-timing-v1|"+canon).encode()).hexdigest()


def split_for(dig:str)->str:
    b=int(dig[:8],16)%100
    return "discovery" if b<=39 else "validation" if b<=59 else "final"


def timing_records()->tuple[list[TRecord],int,dict]:
    base_records,raw_bytes,audit=static.download_records()
    out=[]
    for r in base_records:
        c=r.canonical; d=timing_digest(c)
        out.append(TRecord(r.mother,r.father,r.wedding,c,d,split_for(d)))
    return out,raw_bytes,audit


def safe_shift(w:tuple[int,int,int],dy:int)->tuple[tuple[int,int,int],bool]|None:
    y,m,d=w; y2=y+dy
    try:return (y2,m,d),False
    except Exception:pass
    # The tuple itself does not validate; explicitly construct date.
    try:
        date(y2,m,d);return (y2,m,d),False
    except ValueError:
        if m==2 and d==29:
            return (y2,2,28),True
        return None


def valid_shifts(r:TRecord)->list[tuple[int,tuple[int,int,int],bool]]:
    vals=[]
    for dy in SHIFTS:
        y,m,d=r.wedding[0]+dy,r.wedding[1],r.wedding[2]
        adjusted=False
        try:date(y,m,d)
        except ValueError:
            if m==2 and d==29:d=28;adjusted=True
            else:continue
        cand=(y,m,d)
        ma=static.age_years(r.mother,cand);fa=static.age_years(r.father,cand)
        if 14<=ma<=85 and 14<=fa<=85:vals.append((dy,cand,adjusted))
    return vals


def cap_splits(records):
    out={}
    for s,cap in CAPS.items():
        vals=sorted((r for r in records if r.split==s),key=lambda r:(r.digest,r.canonical))
        out[s]=vals[:cap]
    return out


def choose_control(r:TRecord)->tuple[int,int,int]|None:
    vals=valid_shifts(r)
    if not vals:return None
    h=int(hashlib.sha256(("control|"+r.canonical).encode()).hexdigest(),16)
    return vals[h%len(vals)][1]


def make_binary_cases(rows):
    out=[];drop=defaultdict(int)
    for r in rows:
        c=choose_control(r)
        if c is None:drop["no_valid_shift_control"]+=1
        else:out.append((r,c))
    return out,dict(drop)


def jd_date(dob:tuple[int,int,int],hour:float=12.0)->float:
    return swe.julday(dob[0],dob[1],dob[2],hour,swe.GREG_CAL)


def calc(jd:float,body:int)->float:
    xx,ret=swe.calc_ut(jd,body,FLAGS);used=ret&EPH_MASK
    if used!=swe.FLG_SWIEPH:raise RuntimeError(f"EPHEMERIS_FALLBACK jd={jd} body={body} used={used} ret={ret}")
    return float(xx[0]%360.0)


def natal_positions(dates:set[tuple[int,int,int]],hour:float)->dict[tuple[int,int,int],np.ndarray]:
    out={}
    for i,d in enumerate(sorted(dates),1):
        j=jd_date(d,hour)
        out[d]=np.asarray([calc(j,b) for b in NATAL_IDS],dtype=np.float32)
        if i%5000==0:print(f"natal cache {i}/{len(dates)} hour={hour}",flush=True)
    return out


def transit_positions(dates:set[tuple[int,int,int]])->dict[tuple[int,int,int],np.ndarray]:
    out={}
    for i,d in enumerate(sorted(dates),1):
        j=jd_date(d,12.0)
        out[d]=np.asarray([calc(j,b) for b in TRANSIT_IDS],dtype=np.float32)
        if i%5000==0:print(f"transit cache {i}/{len(dates)}",flush=True)
    return out


def progressed_positions(birth:tuple[int,int,int],cand:tuple[int,int,int],birth_hour:float)->np.ndarray:
    bj=jd_date(birth,birth_hour);cj=jd_date(cand,12.0)
    age=(cj-bj)/TROPICAL_YEAR;pj=bj+age
    return np.asarray([calc(pj,b) for b in PROG_IDS],dtype=np.float32)


def midpoint(a:np.ndarray,b:np.ndarray)->np.ndarray:
    diff=(b.astype(np.float64)-a.astype(np.float64)+180.0)%360.0-180.0
    return ((a.astype(np.float64)+diff/2.0)%360.0).astype(np.float32)


def aspects(movers:np.ndarray,targets:np.ndarray)->np.ndarray:
    diff=(movers[:,None].astype(np.float64)-targets[None,:].astype(np.float64)+180.0)%360.0-180.0
    out=np.empty((len(movers),len(targets),5),dtype=np.float32)
    for k,asp in enumerate(ASPECTS):
        if asp==0:resid=np.abs(diff)
        elif asp==180:resid=np.abs(np.abs(diff)-180.0)
        else:resid=np.minimum(np.abs(diff-asp),np.abs(diff+asp))
        out[:,:,k]=np.exp(-0.5*(resid/SIGMA)**2).astype(np.float32)
    return out.reshape(-1)


def base_features(r:TRecord,cand:tuple[int,int,int])->np.ndarray:
    ma=static.age_years(r.mother,cand);fa=static.age_years(r.father,cand);signed=ma-fa
    phase=2*math.pi*((cand[1]-1)+(cand[2]-1)/31.0)/12.0
    return np.asarray([ma,fa,signed,abs(signed),(cand[0]-1985.0)/20.0,math.sin(phase)+math.cos(phase)],dtype=np.float32)


def row_features(r:TRecord,cand:tuple[int,int,int],natal,transits,birth_hour:float=12.0,dynamic_shift_years:int=0)->np.ndarray:
    f=np.empty(P3,dtype=np.float32);f[:P0]=base_features(r,cand);off=P0
    # Astrology can be deliberately time-shifted for the frozen falsification while baseline remains at cand.
    dyn=cand
    if dynamic_shift_years:
        y,m,d=cand[0]+dynamic_shift_years,cand[1],cand[2]
        try:date(y,m,d)
        except ValueError:d=28 if m==2 and d==29 else d
        dyn=(y,m,d)
    na=natal[r.mother];nb=natal[r.father];tr=transits[dyn]
    pa=progressed_positions(r.mother,dyn,birth_hour);pb=progressed_positions(r.father,dyn,birth_hour)
    for n,p in ((na,pa),(nb,pb)):
        x=aspects(tr,n);f[off:off+len(x)]=x;off+=len(x)
        x=aspects(p,n);f[off:off+len(x)]=x;off+=len(x)
    x=aspects(pa,nb);f[off:off+len(x)]=x;off+=len(x)
    x=aspects(pb,na);f[off:off+len(x)]=x;off+=len(x)
    x=aspects(pa,pb);f[off:off+len(x)]=x;off+=len(x)
    ncomp=midpoint(na,nb);x=aspects(tr,ncomp);f[off:off+len(x)]=x;off+=len(x)
    pcomp=midpoint(pa,pb);x=aspects(tr,pcomp);f[off:off+len(x)]=x;off+=len(x)
    if off!=P3:raise RuntimeError(f"feature size mismatch {off} vs {P3}")
    return f


def collect_dates(cases,risk_rows=None,shift3=False):
    births=set();events=set()
    for r,c in cases:
        births.update((r.mother,r.father));events.update((r.wedding,c))
    if risk_rows:
        for r in risk_rows:
            births.update((r.mother,r.father));events.add(r.wedding)
            events.update(c for _dy,c,_adj in valid_shifts(r))
    if shift3:
        extra=set()
        for c in events:
            y,m,d=c[0]+3,c[1],c[2]
            try:date(y,m,d)
            except ValueError:
                if m==2 and d==29:d=28
                else:continue
            extra.add((y,m,d))
        events|=extra
    return births,events


def build_binary_matrix(cases,natal,transits,birth_hour=12.0,dynamic_shift_years=0):
    X=np.empty((len(cases)*2,P3),dtype=np.float32);y=np.empty(len(cases)*2,dtype=np.int8)
    for i,(r,c) in enumerate(cases):
        X[2*i]=row_features(r,r.wedding,natal,transits,birth_hour,dynamic_shift_years);y[2*i]=1
        X[2*i+1]=row_features(r,c,natal,transits,birth_hour,dynamic_shift_years);y[2*i+1]=0
        if (i+1)%5000==0:print(f"timing binary features {i+1}/{len(cases)}",flush=True)
    return X,y


def scaler(B):
    mean=B[:,:P0].mean(axis=0,dtype=np.float64).astype(np.float32);sd=B[:,:P0].std(axis=0,dtype=np.float64).astype(np.float32);sd[sd<1e-8]=1
    return mean,sd


def scale_inplace(X,mean,sd):X[:,:P0]=(X[:,:P0]-mean)/sd


def new_model(alpha):
    return SGDClassifier(loss="log_loss",penalty="elasticnet",l1_ratio=0.5,alpha=alpha,max_iter=2000,tol=1e-4,random_state=SEED%(2**32),shuffle=True)


def metrics(y,dec):
    prob=1/(1+np.exp(-np.clip(dec.astype(np.float64),-50,50)))
    return {"roc_auc":float(roc_auc_score(y,dec)),"log_loss":float(log_loss(y,prob,labels=[0,1])),"brier":float(brier_score_loss(y,prob))}


def select_alpha(Xd,yd,Xv,yv,dim):
    trials=[]
    for a in ALPHAS:
        clf=new_model(a).fit(Xd[:,:dim],yd);dec=clf.decision_function(Xv[:,:dim]);met=metrics(yv,dec)
        trials.append({"alpha":a,**met,"nonzero":int(np.sum(np.abs(clf.coef_[0])>1e-10))})
        print(f"timing validation dim={dim} alpha={a} auc={met['roc_auc']:.6f}",flush=True)
    best=max(t["roc_auc"] for t in trials);elig=[t for t in trials if best-t["roc_auc"]<=1e-4];sel=max(elig,key=lambda t:t["alpha"])
    return {"trials":trials,"selected_alpha":sel["alpha"],"selected_validation":sel}


def fit_final(Xtrain,ytrain,Xfinal,yfinal,dim,alpha):
    clf=new_model(alpha).fit(Xtrain[:,:dim],ytrain);dec=clf.decision_function(Xfinal[:,:dim]);met=metrics(yfinal,dec)
    cal=LogisticRegression(penalty=None,solver="lbfgs",max_iter=2000).fit(dec.reshape(-1,1),yfinal)
    met.update({"calibration_intercept":float(cal.intercept_[0]),"calibration_slope":float(cal.coef_[0][0]),"nonzero":int(np.sum(np.abs(clf.coef_[0])>1e-10))})
    return met,clf,dec


def risk_rows(records):
    vals=sorted((r for r in records if r.split=="final"),key=lambda r:(r.digest,r.canonical))
    return vals[:RISK_TASKS]


def risk_metrics(rows,natal,transits,clf,mean,sd,dim,birth_hour=12.0,dynamic_shift_years=0,batch=250):
    ranks=[];pcts=[];used=0;drop=0
    for start in range(0,len(rows),batch):
        chunk=rows[start:start+batch];feat=[];sizes=[]
        for r in chunk:
            cands=[r.wedding]+[c for _dy,c,_adj in valid_shifts(r)]
            if len(cands)<2:drop+=1;continue
            arr=np.vstack([row_features(r,c,natal,transits,birth_hour,dynamic_shift_years) for c in cands]);arr[:,:P0]=(arr[:,:P0]-mean)/sd;feat.append(arr);sizes.append(len(cands))
        if not feat:continue
        big=np.vstack(feat);scores=clf.decision_function(big[:,:dim]);pos=0
        for n in sizes:
            arr=scores[pos:pos+n];pos+=n;true=float(arr[0]);ctl=arr[1:];higher=int(np.sum(ctl>true+1e-12));tied=int(np.sum(np.abs(ctl-true)<=1e-12));rank=1+higher+0.5*tied;pct=100*(len(ctl)-higher-0.5*tied)/len(ctl);ranks.append(rank);pcts.append(pct);used+=1
        print(f"timing risk {min(start+batch,len(rows))}/{len(rows)} dim={dim}",flush=True)
    return {"tasks":used,"dropped":drop,"mean_true_date_percentile":float(np.mean(pcts)),"median_true_date_percentile":float(np.median(pcts)),"top1_rate":float(np.mean([r<=1+1e-12 for r in ranks])),"top3_rate":float(np.mean([r<=3+1e-12 for r in ranks])),"mean_reciprocal_rank":float(np.mean([1/r for r in ranks]))}


def permutation(dec,n_pairs=20_000,n=200):
    k=min(n_pairs,len(dec)//2);scores=dec[:2*k].reshape(k,2);obs=float(roc_auc_score(np.tile([1,0],k),scores.reshape(-1)));rng=random.Random(SEED);vals=[]
    for _ in range(n):
        lab=np.empty((k,2),dtype=np.int8)
        for i in range(k):lab[i]=[1,0] if rng.random()<.5 else [0,1]
        vals.append(float(roc_auc_score(lab.reshape(-1),scores.reshape(-1))))
    ge=sum(v>=obs-1e-12 for v in vals)
    return {"pairs":k,"n":n,"observed_auc":obs,"null_mean_auc":statistics.fmean(vals),"null_sd_auc":statistics.stdev(vals),"empirical_p_ge_observed":(ge+1)/(n+1)}


def main():
    for p in (EPHE/"sepl_18.se1",EPHE/"semo_18.se1"):
        if not p.is_file():raise SystemExit("Missing Swiss file "+str(p))
    swe.set_ephe_path(str(EPHE))
    records,raw_bytes,audit=timing_records();splits=cap_splits(records);cases={};drops={}
    for s,rs in splits.items():cases[s],drops[s]=make_binary_cases(rs);print(s,len(rs),len(cases[s]),flush=True)
    rr=risk_rows(records);births,events=collect_dates(cases["discovery"]+cases["validation"]+cases["final"],rr,True);natal=natal_positions(births,12.0);transits=transit_positions(events)
    Xd,yd=build_binary_matrix(cases["discovery"],natal,transits);Xv,yv=build_binary_matrix(cases["validation"],natal,transits);Xf,yf=build_binary_matrix(cases["final"],natal,transits)
    Bd=Xd[:,:P0].copy();Bv=Xv[:,:P0].copy();Bf=Xf[:,:P0].copy();md,sd=scaler(Xd);scale_inplace(Xd,md,sd);scale_inplace(Xv,md,sd)
    selections={m:select_alpha(Xd,yd,Xv,yv,dim) for m,dim in MODEL_DIMS.items()}
    Btrain=np.vstack([Bd,Bv]);mr=Btrain.mean(axis=0,dtype=np.float64).astype(np.float32);sr=Btrain.std(axis=0,dtype=np.float64).astype(np.float32);sr[sr<1e-8]=1
    Xd[:,:P0]=(Bd-mr)/sr;Xv[:,:P0]=(Bv-mr)/sr;Xf[:,:P0]=(Bf-mr)/sr;Xtrain=np.vstack([Xd,Xv]);ytrain=np.concatenate([yd,yv]);del Xd,Xv,Bd,Bv,Btrain
    final={};models={};decisions={}
    for m,dim in MODEL_DIMS.items():
        met,clf,dec=fit_final(Xtrain,ytrain,Xf,yf,dim,selections[m]["selected_alpha"]);final[m]=met;models[m]=clf;decisions[m]=dec
    risk={m:risk_metrics(rr,natal,transits,models[m],mr,sr,dim) for m,dim in MODEL_DIMS.items()}
    d1=final["M1T"]["roc_auc"]-final["M0T"]["roc_auc"];l1=final["M1T"]["log_loss"]-final["M0T"]["log_loss"];r1=risk["M1T"]["mean_true_date_percentile"]
    d3=final["M3T"]["roc_auc"]-final["M1T"]["roc_auc"];l3=final["M3T"]["log_loss"]-final["M1T"]["log_loss"];r3=risk["M3T"]["mean_true_date_percentile"]-risk["M1T"]["mean_true_date_percentile"]
    promising1=final["M1T"]["roc_auc"]>=.52 and d1>=.01 and l1<=-.002 and r1>=55
    promising3=final["M3T"]["roc_auc"]>=.52 and d3>=.01 and l3<=-.002 and risk["M3T"]["mean_true_date_percentile"]>=55 and r3>=5
    strong3=d3>=.03 and r3>=10
    selected="M3T" if d3>=d1 else "M1T";perm=permutation(decisions[selected])
    # +3y falsification, same primary noon natal cache and frozen models; baseline remains candidate date.
    Xshift,yshift=build_binary_matrix(cases["final"],natal,transits,12.0,3);Xshift[:,:P0]=(Bf-mr)/sr;shift={m:metrics(yshift,models[m].decision_function(Xshift[:,:dim])) for m,dim in MODEL_DIMS.items() if m!="M0T"}
    # Birth-time sensitivity uses same trained models, recomputed natal/progressions at alternate birth-date hours.
    sensitivity={}
    for label,hour in (("00UTC",0.0),("2359UTC",23+59/60)):
        nalt=natal_positions(births,hour);Xalt,yalt=build_binary_matrix(cases["final"],nalt,transits,hour);Xalt[:,:P0]=(Bf-mr)/sr;sensitivity[label]={m:metrics(yalt,models[m].decision_function(Xalt[:,:dim])) for m,dim in MODEL_DIMS.items() if m!="M0T"}
    out={"status":"independent_large_n_wedding_timing_final_complete","freeze_spec":str(FREEZE.relative_to(REPO)),"freeze_sha256":static.sha256_file(FREEZE),"source":static.URL,"source_raw_bytes":raw_bytes,"data_audit":audit,"split_counts":{s:{"capped_real":len(splits[s]),"binary_cases":len(cases[s]),"drop":drops[s]} for s in splits},"feature_dimensions":MODEL_DIMS,"selections":selections,"final_binary":final,"final_full_timing_risk_set":risk,"incremental":{"M1T_delta_auc_vs_M0T":d1,"M1T_delta_logloss_vs_M0T":l1,"M1T_promising":promising1,"M3T_delta_auc_vs_M1T":d3,"M3T_delta_logloss_vs_M1T":l3,"M3T_delta_risk_percentile_vs_M1T":r3,"M3T_promising":promising3,"M3T_strong":strong3},"selected_for_permutation":selected,"permutation_diagnostic":perm,"time_shift_plus3y_falsification":shift,"birth_time_sensitivity":sensitivity,"ephemeris":{"requested":"SWIEPH","returned":"SWIEPH or abort","sepl_18_sha256":static.sha256_file(EPHE/"sepl_18.se1"),"semo_18_sha256":static.sha256_file(EPHE/"semo_18.se1")},"interpretation_rule":"Promote only families meeting frozen promising thresholds; otherwise preserve negative/small effect without coefficient mining."}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(out,indent=2,sort_keys=True),flush=True);print("wrote",OUT,"sha256",static.sha256_file(OUT),flush=True)

if __name__=="__main__":main()
