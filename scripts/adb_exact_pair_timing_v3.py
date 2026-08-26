#!/usr/bin/env python3
"""Frozen exact-time ADB relationship timing model V3.

Spec: reference/research/adb_exact_pair_timing_freeze_v3.md
Development/model-discovery only. Verified SWIEPH; fallback aborts.
"""
from __future__ import annotations

import hashlib, json, math, random, re, statistics, urllib.request, xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import swisseph as swe
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

import partner_hd_timing_pilot as hd

REPO=Path(__file__).resolve().parents[1]
EPHE=REPO/'data'/'ephemeris'
FREEZE=REPO/'reference'/'research'/'adb_exact_pair_timing_freeze_v3.md'
RECOVERY=REPO/'reference'/'research'/'adb_external_eventlinked_exact_recovery_v1.json'
OUT=REPO/'reference'/'research'/'adb_exact_pair_timing_results_v3.json'
URL='https://www.astro.com/adbexport/c_sample.xml'
UA='humandesign-exact-pair-v3/1.0'
HIGH_RR={'AA','A'}
ROMANTIC={843,858,859}
FORMATION={807:'meet',808:'begin',810:'marriage'}
DISSOLUTION={809:'end',811:'divorce'}
EVENTS={**FORMATION,**DISSOLUTION}
SHIFT_YEARS=tuple(range(-10,0))+tuple(range(1,11))
TROPICAL_YEAR=365.2422
ASPECTS=(0,60,90,120,180)
C_GRID=(0.001,0.01,0.1,1.0)
SEED=202608261843
SK_SEED=SEED%(2**32)
MODELS=('M0EX','M1DATE','M1EX','XEX','NCOMPEX','PCOMPEX','DAVEX','HDEX','WESTEX','ALLSYS')
NATAL_IDS={'Sun':swe.SUN,'Moon':swe.MOON,'Mercury':swe.MERCURY,'Venus':swe.VENUS,'Mars':swe.MARS,'Jupiter':swe.JUPITER,'Saturn':swe.SATURN}
PROG_IDS={'Sun':swe.SUN,'Moon':swe.MOON,'Mercury':swe.MERCURY,'Venus':swe.VENUS,'Mars':swe.MARS}
TRANSIT_IDS={'Jupiter':swe.JUPITER,'Saturn':swe.SATURN,'Uranus':swe.URANUS,'Neptune':swe.NEPTUNE,'Pluto':swe.PLUTO}
SIGMA_TR={'Jupiter':2.5,'Saturn':2.0,'Uranus':1.5,'Neptune':1.5,'Pluto':1.5}
SIGMA_PR={'Sun':1.0,'Moon':1.5,'Mercury':1.0,'Venus':1.0,'Mars':1.0}
EPH_MASK=swe.FLG_JPLEPH|swe.FLG_SWIEPH|swe.FLG_MOSEPH
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED


def sha256(p:Path)->str:
    h=hashlib.sha256();
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def get(url,timeout=120):
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()


def calc(jd,body):
    xx,ret=swe.calc_ut(jd,body,FLAGS); used=ret&EPH_MASK
    if used!=swe.FLG_SWIEPH: raise RuntimeError(f'EPHEMERIS_FALLBACK body={body} jd={jd} ret={ret}')
    return xx[0]%360


def wrap180(x):return (x+180)%360-180

def aspect_residual(m,t,a):
    if a==0:return abs(wrap180(m-t))
    if a==180:return abs(wrap180(m-t-180))
    return min(abs(wrap180(m-t-a)),abs(wrap180(m-t+a)))

def kernel(m,t,a,sigma):
    r=aspect_residual(m,t,a);return math.exp(-.5*(r/sigma)**2)

def midpoint(a,b):return (a+wrap180(b-a)/2)%360


def parse_clock(s:str)->float:
    p=[float(x) for x in s.strip().split(':')]
    return p[0]+(p[1] if len(p)>1 else 0)/60+(p[2] if len(p)>2 else 0)/3600


def meridian_offset_hours(s:str)->float:
    s=(s or '').strip().lower()
    if not s: raise ValueError('empty stmerid')
    kind=s[0]; rest=s[1:]
    m=re.fullmatch(r'(\d+)([ew])(\d*)',rest)
    if not m: raise ValueError(f'bad stmerid {s}')
    major=int(m.group(1)); direction=m.group(2); tail=m.group(3)
    if kind=='h':
        minutes=int(tail[:2]) if len(tail)>=2 else 0
        seconds=int(tail[2:4]) if len(tail)>=4 else 0
        off=major+minutes/60+seconds/3600
    elif kind=='m':
        minutes=int(tail[:2]) if len(tail)>=2 else 0
        seconds=int(tail[2:4]) if len(tail)>=4 else 0
        deg=major+minutes/60+seconds/3600
        off=deg/15
    else: raise ValueError(f'bad stmerid kind {s}')
    return off if direction=='e' else -off


def local_to_jd(y,m,d,clock,calendar,stmerid):
    cal=swe.JUL_CAL if calendar=='j' else swe.GREG_CAL
    local=swe.julday(y,m,d,parse_clock(clock),cal)
    return local-meridian_offset_hours(stmerid)/24


def parse_coord(s:str,lat=True)->float:
    s=(s or '').strip().lower(); m=re.fullmatch(r'(\d+)([nsew])(\d*)',s)
    if not m: raise ValueError(f'bad coord {s}')
    deg=int(m.group(1)); dire=m.group(2); tail=m.group(3)
    minute=int(tail[:2]) if len(tail)>=2 else 0; sec=int(tail[2:4]) if len(tail)>=4 else 0
    v=deg+minute/60+sec/3600
    return -v if dire in {'s','w'} else v


def houses(jd,lat,lon):
    cusps,ascmc=swe.houses_ex(jd,lat,lon,b'P',0)
    asc=float(ascmc[0]%360); mc=float(ascmc[1]%360)
    return {'ASC':asc,'DSC':(asc+180)%360,'MC':mc,'IC':(mc+180)%360,'H5':float(cusps[4]%360),'H7':float(cusps[6]%360)}


def natal(jd):return {n:calc(jd,b) for n,b in NATAL_IDS.items()}
def progressed(birth_jd,event_jd):
    age=(event_jd-birth_jd)/TROPICAL_YEAR; pj=birth_jd+age
    return {n:calc(pj,b) for n,b in PROG_IDS.items()}


def norm(s):return re.sub(r'[^a-z0-9]+',' ',(s or '').casefold()).strip()
def tokens(s):
    stop={'relationship','spouse','lover','with','born','family','associates'}
    return {t for t in norm(s).split() if len(t)>=4 and t not in stop}
def event_match(ev,toks):
    words=set(norm((ev.get('notes') or '')+' '+(ev.get('sevcode') or '')).split());return bool(toks&words)

@dataclass(frozen=True)
class Person:
    key:str; jd:float; lat:float; lon:float; rr:str

@dataclass(frozen=True)
class Event:
    pair_key:str; a:Person; b:Person; event_id:int; event_type:str; transition:str; year:int; month:int; day:int; precision:str


def parse_csample(xml_bytes):
    root=ET.fromstring(xml_bytes); entries={}; validation=[]
    for e in root.findall('adb_entry'):
        aid=int(e.attrib['adb_id']); pub=e.find('public_data')
        if pub is None:continue
        rr=(pub.findtext('roddenrating') or '').strip(); name=(pub.findtext('name') or '').strip()
        bd=pub.find('bdata'); jd=None; lat=lon=None; local=None
        if bd is not None:
            sd=bd.find('sbdate'); st=bd.find('sbtime'); pl=bd.find('place')
            if sd is not None and st is not None and (st.text or '').strip() and st.attrib.get('jd_ut') and pl is not None:
                try:
                    jd=float(st.attrib['jd_ut']); lat=parse_coord(pl.attrib.get('slati','')); lon=parse_coord(pl.attrib.get('slong',''),False)
                    local={'y':int(sd.attrib['iyear']),'m':int(sd.attrib['imonth']),'d':int(sd.attrib['iday']),'calendar':sd.attrib.get('ccalendar','g'),'clock':(st.text or '').strip(),'stmerid':st.attrib.get('stmerid','')}
                    validation.append((jd,local))
                except Exception:pass
        rels=[]; evs=[]; res=e.find('research_data')
        if res is not None:
            rp=res.find('relationships')
            if rp is not None:
                for r in rp.findall('relationship'):
                    try:rid=int(r.attrib.get('rel_id','0'));other=int(r.attrib.get('rel_adb_id','0'))
                    except:continue
                    rels.append({'rid':rid,'other':other,'text':(r.text or '').strip()})
            ep=res.find('events')
            if ep is not None:
                for v in ep.findall('event'):
                    try:eid=int(v.attrib.get('evn_id','0'))
                    except:continue
                    sd=v.find('./event_data/sbdate'); y=m=d=None
                    if sd is not None:
                        try:
                            y=int(sd.attrib['iyear']);m=int(sd.attrib.get('imonth','0')) or None;d=int(sd.attrib.get('iday','0')) or None
                        except:pass
                    evs.append({'eid':eid,'sevcode':v.attrib.get('sevcode',''),'notes':v.attrib.get('evnotes',''),'y':y,'m':m,'d':d})
        entries[aid]={'id':aid,'name':name,'rr':rr,'jd':jd,'lat':lat,'lon':lon,'rels':rels,'events':evs}
    return entries,validation


def recovered_people():
    data=json.loads(RECOVERY.read_text(encoding='utf-8')); out={}
    for row in data.get('records',[]):
        mat=row.get('matched') or {}
        if row.get('status')!='exact_time' or mat.get('sroddenrating') not in HIGH_RR:continue
        try:
            y,m,d=map(int,mat['sbdate'].split('/')); jd=local_to_jd(y,m,d,mat['sbtime'],mat.get('ccalendar') or 'g',mat['stmerid'])
            lat=parse_coord(mat['slati']);lon=parse_coord(mat['slong'],False)
        except Exception as ex:
            print('skip recovered',row.get('adb_id'),ex,flush=True);continue
        out[int(row['adb_id'])]=Person(f"adb:{row['adb_id']}",jd,lat,lon,mat['sroddenrating'])
    return out


def make_events(entries,recovered):
    persons={}
    for aid,r in entries.items():
        if r['rr'] in HIGH_RR and r['jd'] is not None:
            persons[aid]=Person(f'adb:{aid}',r['jd'],r['lat'],r['lon'],r['rr'])
    persons.update(recovered)
    internal_ids=set(entries); seen=set(); out=[]
    # iterate directed relationship links, but de-duplicate mirrored events
    for aid,r in entries.items():
        if aid not in persons:continue
        for rel in r['rels']:
            if rel['rid'] not in ROMANTIC:continue
            bid=rel['other']
            if bid not in persons:continue
            # For internal partner use true record name; external parse name after 'with'.
            if bid in entries:
                btoks=tokens(entries[bid]['name'])
            else:
                mm=re.search(r'\bwith\s+(.+?)(?:,\s*born:|$)',rel['text'],re.I);btoks=tokens(mm.group(1) if mm else rel['text'])
            for ev in r['events']:
                if ev['eid'] not in EVENTS or not event_match(ev,btoks) or ev['y'] is None or ev['m'] is None:continue
                day=ev['d'] or 15; precision='day' if ev['d'] else 'month'; transition='formation' if ev['eid'] in FORMATION else 'dissolution'
                pk='|'.join(sorted((persons[aid].key,persons[bid].key)))
                key=(pk,ev['eid'],ev['y'],ev['m'],day)
                if key in seen:continue
                seen.add(key);out.append(Event(pk,persons[aid],persons[bid],ev['eid'],EVENTS[ev['eid']],transition,ev['y'],ev['m'],day,precision))
    return out


def validate_utc(validation):
    errs=[];bad=[]
    for known,loc in validation[:500]:
        try:calcjd=local_to_jd(loc['y'],loc['m'],loc['d'],loc['clock'],loc['calendar'],loc['stmerid'])
        except Exception as ex:bad.append(str(ex));continue
        errs.append(abs(calcjd-known)*86400)
    if len(errs)<100:raise RuntimeError(f'UTC validation only {len(errs)} parseable records')
    med=float(np.median(errs));mx=max(errs)
    if med>1 or mx>5:raise RuntimeError(f'UTC reconstruction failed median={med}s max={mx}s bad={bad[:5]}')
    return {'n':len(errs),'median_abs_error_seconds':med,'max_abs_error_seconds':mx,'parse_failures':len(bad)}


def safe_shift(y,m,d,dy):
    yy=y+dy
    try:swe.julday(yy,m,d,12,swe.GREG_CAL);return yy,m,d,False
    except:return None


def date_jd(y,m,d):return swe.julday(y,m,d,12.0,swe.GREG_CAL)


def add_aspects(f,prefix,movers,targets,sigmas):
    for mn,ml in movers.items():
        sg=sigmas[mn]
        for tn,tl in targets.items():
            for a in ASPECTS:f[f'{prefix}_{mn}_{tn}_a{a}']=kernel(ml,tl,a,sg)


def hd_features(a:Person,b:Person,event_jd):
    ag=hd.natal_gates(hd.dt_from_jd(a.jd));bg=hd.natal_gates(hd.dt_from_jd(b.jd));_,tg=hd.transit_gate_state(hd.dt_from_jd(event_jd));fp=hd.fingerprint(ag|bg|tg)
    n=fp['defined_center_count']; comp=fp['definition_components']; ch=len(fp['channels'])
    return {'hd_center_count':float(n),'hd_components':float(comp),'hd_single':float(comp==1),'hd_8plus1':float(n==8),'hd_9plus0':float(n==9),'hd_channel_count':float(ch)}


def raw_features(ev:Event,cj):
    na=natal(ev.a.jd);nb=natal(ev.b.jd);ha=houses(ev.a.jd,ev.a.lat,ev.a.lon);hb=houses(ev.b.jd,ev.b.lat,ev.b.lon)
    pa=progressed(ev.a.jd,cj);pb=progressed(ev.b.jd,cj);tr={n:calc(cj,b) for n,b in TRANSIT_IDS.items()}
    f={'m0_age_a':(cj-ev.a.jd)/TROPICAL_YEAR,'m0_age_b':(cj-ev.b.jd)/TROPICAL_YEAR,'m0_year_scaled':(swe.revjul(cj,swe.GREG_CAL)[0]-1950)/50,
       f'm0_event_{ev.event_type}':1.0,f'm0_precision_{ev.precision}':1.0}
    # date-stable individual baseline
    base_targets=('Sun','Mercury','Venus','Mars','Jupiter','Saturn')
    for side,nat,prog in (('a',na,pa),('b',nb,pb)):
        add_aspects(f,f'm1d_{side}_tr',tr,{x:nat[x] for x in base_targets},SIGMA_TR)
        add_aspects(f,f'm1d_{side}_pr',{x:prog[x] for x in ('Sun','Mercury','Venus','Mars')},{x:nat[x] for x in base_targets},SIGMA_PR)
    # exact individual Moon/angles/houses
    ex_targets_a={'Moon':na['Moon'],**ha};ex_targets_b={'Moon':nb['Moon'],**hb}
    for side,ext,prog in (('a',ex_targets_a,pa),('b',ex_targets_b,pb)):
        add_aspects(f,f'm1x_{side}_tr',tr,ext,SIGMA_TR);add_aspects(f,f'm1x_{side}_pr',prog,ext,SIGMA_PR)
    # cross progressions exact
    ta={**na,**ha};tb={**nb,**hb}
    add_aspects(f,'x_pa_nb',pa,tb,SIGMA_PR);add_aspects(f,'x_pb_na',pb,ta,SIGMA_PR);add_aspects(f,'x_pa_pb',pa,pb,SIGMA_PR)
    # natal midpoint composite
    ncomp={n:midpoint(na[n],nb[n]) for n in NATAL_IDS};add_aspects(f,'nc_tr',tr,ncomp,SIGMA_TR)
    # progressed midpoint composite
    pcomp={n:midpoint(pa[n],pb[n]) for n in PROG_IDS};add_aspects(f,'pc_tr',tr,pcomp,SIGMA_TR)
    # Davison time + geographic midpoint
    dj=(ev.a.jd+ev.b.jd)/2; dlat=(ev.a.lat+ev.b.lat)/2; dlon=midpoint(ev.a.lon%360,ev.b.lon%360); dlon=wrap180(dlon)
    dn=natal(dj);dh=houses(dj,dlat,dlon);dt={**dn,**dh};add_aspects(f,'dav_tr',tr,dt,SIGMA_TR)
    # HD low-dimensional pair weather
    f.update(hd_features(ev.a,ev.b,cj))
    return f


def build_rows(events,transition):
    rows=[];counts=Counter()
    for ev in events:
        if ev.transition!=transition:continue
        candidates=[(ev.year,ev.month,ev.day,1)]
        for dy in SHIFT_YEARS:
            sh=safe_shift(ev.year,ev.month,ev.day,dy)
            if not sh:continue
            y,m,d,_=sh;cj=date_jd(y,m,d);aa=(cj-ev.a.jd)/TROPICAL_YEAR;bb=(cj-ev.b.jd)/TROPICAL_YEAR
            if not(16<=aa<=85 and 16<=bb<=85):counts['age_excluded']+=1;continue
            candidates.append((y,m,d,0))
        if len(candidates)<6:counts['too_few_controls']+=1;continue
        ek=f'{ev.pair_key}|{ev.event_id}|{ev.year:04d}-{ev.month:02d}-{ev.day:02d}'
        for y,m,d,actual in candidates:
            rows.append({'event_key':ek,'pair_key':ev.pair_key,'actual':actual,'features':raw_features(ev,date_jd(y,m,d))})
    return rows,dict(counts)


def model_names(model,alln):
    out=[]
    for n in alln:
        if n.startswith('m0_'):out.append(n)
        if model!='M0EX' and n.startswith('m1d_'):out.append(n)
        if model in {'M1EX','WESTEX','ALLSYS'} and n.startswith('m1x_'):out.append(n)
        if model in {'XEX','WESTEX','ALLSYS'} and n.startswith('x_'):out.append(n)
        if model in {'NCOMPEX','WESTEX','ALLSYS'} and n.startswith('nc_'):out.append(n)
        if model in {'PCOMPEX','WESTEX','ALLSYS'} and n.startswith('pc_'):out.append(n)
        if model in {'DAVEX','WESTEX','ALLSYS'} and n.startswith('dav_'):out.append(n)
        if model in {'HDEX','ALLSYS'} and n.startswith('hd_'):out.append(n)
    return sorted(set(out))


def metric(rows,scores):
    by=defaultdict(list)
    for r,s in zip(rows,scores):by[r['event_key']].append((float(s),int(r['actual'])))
    pcts=[];ranks=[];loss=[]
    for vals in by.values():
        actual_score=next(s for s,y in vals if y==1);scores0=[s for s,_ in vals];gt=sum(s>actual_score+1e-12 for s in scores0);eq=sum(abs(s-actual_score)<=1e-12 for s in scores0)
        avg_rank=gt+(eq+1)/2;n=len(vals);pct=50.0 if n==1 else 100*(n-avg_rank)/(n-1);pcts.append(pct);ranks.append(avg_rank)
        arr=np.array(scores0);arr-=arr.max();pr=np.exp(arr);pr/=pr.sum();idx=next(i for i,(_,y) in enumerate(vals) if y==1);loss.append(-math.log(max(float(pr[idx]),1e-15)))
    return {'events':len(pcts),'mean_true_date_percentile':float(np.mean(pcts)),'median_true_date_percentile':float(np.median(pcts)),'top1_rate':float(np.mean([r<=1+1e-12 for r in ranks])),'top3_rate':float(np.mean([r<=3 for r in ranks])),'mean_reciprocal_rank':float(np.mean([1/r for r in ranks])),'softmax_log_loss':float(np.mean(loss))}


def fit(Xt,yt,Xv,c):
    sc=StandardScaler().fit(Xt);a=sc.transform(Xt);b=sc.transform(Xv);cl=LogisticRegression(C=c,penalty='l1',solver='liblinear',class_weight='balanced',max_iter=5000,random_state=SK_SEED).fit(a,yt);return cl,cl.decision_function(b)


def choose_c(rows,names):
    groups=np.array([r['pair_key'] for r in rows]);X=np.array([[r['features'].get(n,0) for n in names] for r in rows]);y=np.array([r['actual'] for r in rows]);u=len(set(groups));spl=min(3,max(2,u//5));best=None
    for c in C_GRID:
        fs=[]
        for ti,vi in GroupKFold(spl).split(X,y,groups):_,pred=fit(X[ti],y[ti],X[vi],c);fs.append(metric([rows[i] for i in vi],pred)['mean_true_date_percentile'])
        z=statistics.fmean(fs)
        if best is None or z>best[0]+1e-12 or(abs(z-best[0])<1e-12 and c<best[1]):best=(z,c)
    return best[1]


def evaluate(rows,model,fixed_c=None):
    alln=sorted(rows[0]['features']);names=model_names(model,alln);groups=np.array([r['pair_key'] for r in rows]);X=np.array([[r['features'].get(n,0) for n in names] for r in rows]);y=np.array([r['actual'] for r in rows]);spl=min(5,len(set(groups))//5);oof=np.zeros(len(rows));cs=[];foldpct=[];coefs=[]
    for ti,vi in GroupKFold(spl).split(X,y,groups):
        tr=[rows[i] for i in ti];c=fixed_c if fixed_c is not None else choose_c(tr,names);cl,p=fit(X[ti],y[ti],X[vi],c);oof[vi]=p;cs.append(float(c));foldpct.append(metric([rows[i] for i in vi],p)['mean_true_date_percentile']);coefs.append({n:float(v) for n,v in zip(names,cl.coef_[0]) if abs(v)>1e-10})
    met=metric(rows,oof);stable=[]
    agg=defaultdict(list)
    for c in coefs:
        for n,v in c.items():agg[n].append(v)
    for n,vs in agg.items():stable.append({'feature':n,'selected_folds':len(vs),'sign_consistent':all(v>0 for v in vs) or all(v<0 for v in vs),'mean_coef':statistics.fmean(vs),'mean_abs_coef':statistics.fmean(abs(v) for v in vs)})
    stable.sort(key=lambda x:(x['selected_folds'],x['sign_consistent'],x['mean_abs_coef']),reverse=True)
    met.update({'model':model,'feature_count':len(names),'outer_folds':spl,'selected_C_by_fold':cs,'mean_true_date_percentile_by_fold':foldpct,'stable_selected_features':stable[:30]});return met


def modal(xs):
    c=Counter(xs);mx=max(c.values());return min(x for x,n in c.items() if n==mx)


def permute(rows,model,obs,n=200):
    rng=random.Random(SEED);by=defaultdict(list)
    for i,r in enumerate(rows):by[r['event_key']].append(i)
    c=modal(obs['selected_C_by_fold']);null=[]
    for k in range(n):
        rr=[dict(r) for r in rows]
        for idxs in by.values():
            pick=rng.choice(idxs)
            for i in idxs:rr[i]['actual']=int(i==pick)
        null.append(evaluate(rr,model,fixed_c=c)['mean_true_date_percentile'])
        if(k+1)%20==0:print('perm',k+1,flush=True)
    o=obs['mean_true_date_percentile'];ge=sum(x>=o-1e-12 for x in null);return {'n':n,'fixed_C':c,'observed':o,'null_mean':statistics.fmean(null),'null_sd':statistics.stdev(null),'null_ge_observed':ge,'empirical_p_ge_observed':(ge+1)/(n+1)}


def main():
    for p in (EPHE/'sepl_18.se1',EPHE/'semo_18.se1'):
        if not p.is_file():raise SystemExit('missing '+str(p))
    swe.set_ephe_path(str(EPHE));xml=get(URL);entries,val=parse_csample(xml);utc=validate_utc(val);print('UTC',utc,flush=True)
    rec=recovered_people();events=make_events(entries,rec);counts=Counter(e.transition for e in events);print('events',len(events),counts,'pairs',len(set(e.pair_key for e in events)),flush=True)
    form_rows,form_ex=build_rows(events,'formation');print('formation rows',len(form_rows),flush=True)
    if len(set(r['event_key'] for r in form_rows))<30:raise RuntimeError('too few formation events')
    results={}
    for m in MODELS:
        print('evaluate',m,flush=True);results[m]=evaluate(form_rows,m)
    base=results['M1DATE'];
    for m in MODELS:
        if m in {'M0EX','M1DATE'}:continue
        r=results[m];d=r['mean_true_date_percentile']-base['mean_true_date_percentile'];dl=r['softmax_log_loss']-base['softmax_log_loss'];fd=[x-y for x,y in zip(r['mean_true_date_percentile_by_fold'],base['mean_true_date_percentile_by_fold'])];r['delta_vs_M1DATE']=d;r['delta_loss_vs_M1DATE']=dl;r['positive_improvement_folds']=sum(x>0 for x in fd);r['clears_frozen_threshold']=d>=5 and dl<=.05 and sum(x>0 for x in fd)>=3
    candidates=[m for m in MODELS if m not in {'M0EX','M1DATE'}];best=max(candidates,key=lambda m:results[m]['mean_true_date_percentile']-base['mean_true_date_percentile']);perm=permute(form_rows,best,results[best],200)
    diss=None
    if counts['dissolution']>=30:
        dr,_=build_rows(events,'dissolution');diss={m:evaluate(dr,m) for m in MODELS}
    data={'status':'development_model_discovery','freeze_spec':str(FREEZE.relative_to(REPO)),'freeze_sha256':sha256(FREEZE),'ephemeris':{'requested':'SWIEPH','returned':'SWIEPH or abort','sepl_18_sha256':sha256(EPHE/'sepl_18.se1'),'semo_18_sha256':sha256(EPHE/'semo_18.se1')},'utc_reconstruction_validation':utc,'dataset':{'recovered_high_rr_exact_external_people':len(rec),'events':len(events),'pairs':len(set(e.pair_key for e in events)),'transition_counts':dict(counts),'formation_candidate_rows':len(form_rows),'formation_exclusions':form_ex},'formation_results':results,'best_exact_family_by_delta_vs_M1DATE':best,'best_family_permutation':perm,'any_family_clears_frozen_threshold':any(results[m].get('clears_frozen_threshold') for m in candidates),'dissolution_results':diss,'limitations':['C-sample-derived development dataset; not independent validation.','Case-crossover event-date precursor, not full semi-Markov state-duration hazard.','Relationship events are likely dominated by marriage and public-figure documentation patterns.']}
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps({'utc':utc,'dataset':data['dataset'],'best':best,'perm':perm,'summary':{m:{k:results[m].get(k) for k in ('mean_true_date_percentile','softmax_log_loss','delta_vs_M1DATE','positive_improvement_folds','clears_frozen_threshold')} for m in MODELS}},indent=2),flush=True)

if __name__=='__main__':main()
